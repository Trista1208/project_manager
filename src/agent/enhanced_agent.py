# src/agent/enhanced_agent.py
"""
Enhanced agent with Jira, Slack, and state persistence.
Supports multiple issue sources and notifications.
"""
import asyncio
import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from mcp import ClientSession
from src.core.reasoning_controller import ReasoningController
from mcp.client.streamable_http import streamablehttp_client
from src.core.plan_validation import PlanValidator
from src.core.update_check import UpdateChecker


HOST = "http://127.0.0.1:5000/mcp"


class EnhancedAgent:
    """Agent with full integration capabilities."""
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.plan_validator = PlanValidator()
        self.update_checker = UpdateChecker()
        self.reasoning_controller = ReasoningController()
    
    async def initialize(self, session: ClientSession):
        """Initialize the agent with an MCP session."""
        self.session = session
        await session.initialize()
    
    async def fetch_issues(
        self, 
        github_repo: Optional[str] = None,
        jira_project: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch issues from GitHub and/or Jira.
        
        Args:
            github_repo: GitHub repo in format 'owner/repo'
            jira_project: Jira project key
        
        Returns:
            List of unified issue dicts
        """
        all_issues = []
        
        # Fetch from GitHub
        if github_repo:
            print(f"📥 Fetching issues from GitHub: {github_repo}")
            try:
                result = await self.session.call_tool(
                    "github_get_issues",
                    {"repo": github_repo}
                )
                github_issues = json.loads(result.content[0].text)
                
                if isinstance(github_issues, dict) and "error" in github_issues:
                    print(f"⚠️  GitHub error: {github_issues['error']}")
                else:
                    all_issues.extend(github_issues)
                    print(f"✅ Fetched {len(github_issues)} issues from GitHub")
            except Exception as e:
                print(f"❌ Failed to fetch from GitHub: {e}")
        
        # Fetch from Jira
        if jira_project:
            print(f"📥 Fetching issues from Jira: {jira_project}")
            try:
                result = await self.session.call_tool(
                    "jira_get_issues",
                    {"project_key": jira_project}
                )
                jira_issues = json.loads(result.content[0].text)
                
                if isinstance(jira_issues, dict) and "error" in jira_issues:
                    print(f"⚠️  Jira error: {jira_issues['error']}")
                else:
                    all_issues.extend(jira_issues)
                    print(f"✅ Fetched {len(jira_issues)} issues from Jira")
            except Exception as e:
                print(f"❌ Failed to fetch from Jira: {e}")
        
        return all_issues

    async def process_issue(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single issue using LLM-driven orchestration.

        The agent does not follow a fixed pipeline.
        Instead, a reasoning LLM decides which action to take next
        (e.g. task breakdown, scheduling, or stopping) based on the
        current issue state.

        The agent itself only executes the chosen actions and handles
        side effects such as state persistence, calendar creation,
        and Slack notifications.

        Args:
            issue: Unified issue dict (GitHub or Jira)

        Returns:
            Processing result with scheduled tasks if applicable
        """
        issue_key = f"{issue['source']}:{issue['id']}"
        print(f"\n{'='*60}")
        print(f"🎯 Processing: {issue['title']}")
        print(f"   Source: {issue['source'].upper()}")
        print(f"   Priority: {issue.get('priority', 'N/A')}")
        print(f"{'='*60}")


        # === Check if updates ===
        # checks if issue is already scheduled and skips already scheduled issues.
        check_reply = self.update_checker.check(issue_key = issue_key)
        if check_reply["decision"] != "APPROVE":
            print("⛔ Issue already scheduled. Skip Issue.")

            return {
                "success": False,
                "issue_key": issue_key,
                "error": "Issue already in the Project Store and therefore is already scheduled."
            }
        # ========================


        try:
            # Save issue to state
            await self.session.call_tool(
                "state_add_issue",
                {"issue_json": json.dumps(issue)}
            )

            # === DECISION LOOP (Reasoning LLM) ===

            context = {
                "issue_key": issue_key,
                "has_tasks": False,
                "validated": False,
                "scheduled": False
            }

            tasks = None
            scheduled = None

            max_steps = 5
            steps = 0

            done = False

            while not done and steps < max_steps:
                steps += 1

                print("🧠 ReasoningController decide() called")
                decision = self.reasoning_controller.decide(context)
                print("🧠 Decision:", decision)

                actions = decision.get("actions")

                if not isinstance(actions, list):
                    print("⚠️ Invalid actions from reasoning LLM, stopping loop")
                    break

                for action in actions:
                    tool = action.get("tool")

                    if tool == "tasks_breakdown":
                        if context["has_tasks"]:
                            continue

                        issue_text = f"{issue['title']}\n{issue['body']}"
                        result = await self.session.call_tool(
                            "tasks_breakdown",
                            {"issue_text": issue_text}
                        )
                        tasks = json.loads(result.content[0].text)
                        context["has_tasks"] = True

                    elif tool == "plan_validation":
                        validation = self.plan_validator.validate(tasks)
                        if validation["decision"] != "APPROVE":
                            return {
                                "success": False,
                                "issue_key": issue_key,
                                "error": "Plan rejected"
                            }
                        context["validated"] = True

                    elif tool == "tasks_schedule":
                        result = await self.session.call_tool(
                            "tasks_schedule",
                            {"tasks_json": json.dumps(tasks)}
                        )
                        scheduled = json.loads(result.content[0].text)
                        context["scheduled"] = True
                        done = True

                    elif tool == "stop":
                        done = True

            
            # Save to state
            if scheduled is None:
                return {
                    "success": False,
                    "issue_key": issue_key,
                    "error": "No scheduled tasks produced by reasoning loop"
                }

            # Save to state
            await self.session.call_tool(
                "state_add_scheduled_tasks",
                {
                    "issue_key": issue_key,
                    "tasks_json": json.dumps(scheduled)
                }
            )

            # Create calendar events
            for task in scheduled:
                print(f"   📌 {task['task']}: {task['start']} → {task['end']}")
                await self.session.call_tool(
                    "calendar_create_event",
                    {
                        "summary": task["task"],
                        "start": task["start"],
                        "end": task["end"]
                    }
                )

            # Send Slack notification
            try:
                await self.session.call_tool(
                    "slack_notify_scheduled_tasks",
                    {
                        "issue_source": issue["source"].capitalize(),
                        "issue_title": issue["title"],
                        "tasks_json": json.dumps(scheduled)
                    }
                )
                print(f"💬 Sent Slack notification")
            except Exception as e:
                print(f"⚠️  Slack notification failed: {e}")

            
            # Log execution
            await self.session.call_tool(
                "state_log_execution",
                {
                    "action": "process_issue",
                    "details_json": json.dumps({
                        "issue_key": issue_key,
                        "tasks_scheduled": len(scheduled)
                    }),
                    "success": True
                }
            )
            
            return {
                "success": True,
                "issue_key": issue_key,
                "tasks": scheduled
            }
            
        except Exception as e:
            print(f"❌ Error processing issue: {e}")
            
            # Log error
            try:
                await self.session.call_tool(
                    "state_log_execution",
                    {
                        "action": "process_issue",
                        "details_json": json.dumps({
                            "issue_key": issue_key,
                            "error": str(e)
                        }),
                        "success": False
                    }
                )
            except:
                pass
            
            return {
                "success": False,
                "issue_key": issue_key,
                "error": str(e)
            }
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get statistics from state store."""
        result = await self.session.call_tool("state_get_stats", {})
        return json.loads(result.content[0].text)


async def run_enhanced_agent(
    github_repo: Optional[str] = None,
    jira_project: Optional[str] = None,
    max_issues: int = 10
):
    """
    Run the enhanced agent.
    
    Args:
        github_repo: GitHub repo in format 'owner/repo'
        jira_project: Jira project key
        max_issues: Maximum issues to process per run
    """
    print("🚀 Starting Enhanced Agent...")
    print(f"   GitHub: {github_repo or 'Not configured'}")
    print(f"   Jira: {jira_project or 'Not configured'}")
    print()
    
    async with streamablehttp_client(HOST) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            agent = EnhancedAgent()
            await agent.initialize(session)
            
            # Fetch issues
            issues = await agent.fetch_issues(github_repo, jira_project)
            
            if not issues:
                print("❌ No issues found!")
                return
            
            print(f"\n📊 Found {len(issues)} total issues")
            
            # Limit to max_issues
            if len(issues) > max_issues:
                print(f"⚠️  Limiting to {max_issues} issues")
                issues = issues[:max_issues]
            
            # Process each issue
            results = []
            for issue in issues:
                result = await agent.process_issue(issue)
                results.append(result)
                
                # Small delay between issues
                await asyncio.sleep(0.5)
            
            # Summary
            print(f"\n{'='*60}")
            print("📊 SUMMARY")
            print(f"{'='*60}")
            
            successful = sum(1 for r in results if r["success"])
            failed = len(results) - successful
            
            print(f"✅ Successfully processed: {successful}")
            print(f"❌ Failed: {failed}")
            
            # Get stats
            stats = await agent.get_stats()
            print(f"\n📈 Total Statistics:")
            print(f"   Total issues: {stats.get('total_issues', 0)}")
            print(f"   Total tasks scheduled: {stats.get('total_scheduled_tasks', 0)}")
            print(f"   Tasks by status: {stats.get('tasks_by_status', {})}")
            
            print(f"\n✅ Enhanced Agent completed!")


if __name__ == "__main__":
    # Configuration from environment or defaults
    GITHUB_REPO = os.getenv("GITHUB_REPO", "BaHu-Git/Task_Manager")
    JIRA_PROJECT = os.getenv("JIRA_PROJECT", None)
    MAX_ISSUES = int(os.getenv("MAX_ISSUES", "5"))
    
    asyncio.run(run_enhanced_agent(
        github_repo=GITHUB_REPO,
        jira_project=JIRA_PROJECT,
        max_issues=MAX_ISSUES
    ))



