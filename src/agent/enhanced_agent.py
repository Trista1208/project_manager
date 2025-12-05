# src/agent/enhanced_agent.py
"""
Enhanced agent with Jira, Slack, and state persistence.
Supports multiple issue sources and notifications.
"""
import asyncio
import json
import os
from typing import List, Dict, Any, Optional

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

HOST = "http://127.0.0.1:5000/mcp"


class EnhancedAgent:
    """Agent with full integration capabilities."""
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
    
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
        Process a single issue: breakdown → schedule → calendar.
        
        Args:
            issue: Unified issue dict
        
        Returns:
            Processing result with scheduled tasks
        """
        issue_key = f"{issue['source']}:{issue['id']}"
        print(f"\n{'='*60}")
        print(f"🎯 Processing: {issue['title']}")
        print(f"   Source: {issue['source'].upper()}")
        print(f"   Priority: {issue.get('priority', 'N/A')}")
        print(f"{'='*60}")
        
        try:
            # Save issue to state
            await self.session.call_tool(
                "state_add_issue",
                {"issue_json": json.dumps(issue)}
            )
            
            # Breakdown into tasks
            issue_text = f"{issue['title']}\n{issue['body']}"
            breakdown_result = await self.session.call_tool(
                "tasks_breakdown",
                {"issue_text": issue_text}
            )
            tasks = json.loads(breakdown_result.content[0].text)
            print(f"✂️  Broke down into {len(tasks)} tasks")
            
            # Schedule tasks
            schedule_result = await self.session.call_tool(
                "tasks_schedule",
                {"tasks_json": json.dumps(tasks)}
            )
            scheduled = json.loads(schedule_result.content[0].text)
            print(f"📅 Scheduled {len(scheduled)} tasks")
            
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


