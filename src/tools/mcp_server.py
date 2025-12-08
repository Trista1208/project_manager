# src/tools/mcp_server.py
import os
import sys
import json
from typing import List, Dict, Any, Optional

# Make `src` importable when running this file directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import requests
from mcp.server import FastMCP
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.core.task_breakdown import TaskBreakdown
from src.core.scheduler import Scheduler
from src.core.state_store import ProjectStateStore

# Multi-agent LLM support
try:
    from src.core.task_breakdown_multi import TaskBreakdownMulti
    from src.core.llm_factory import LLMFactory
    MULTI_AGENT_ENABLED = True
    # Try to create multi-agent breaker
    multi_strategy = os.getenv("LLM_STRATEGY", "specialized")
    print(f"🤖 Initializing multi-agent system with strategy: {multi_strategy}")
    multi_breaker = TaskBreakdownMulti(strategy=multi_strategy)
except Exception as e:
    print(f"⚠️  Multi-agent LLM not available: {e}")
    print(f"   Falling back to single LLM mode")
    MULTI_AGENT_ENABLED = False
    multi_breaker = None

# Import new clients (with error handling for optional features)
try:
    from src.tools.jira_client import JiraClient
    jira_client = JiraClient()
    print("✅ JIRA BASE URL =", jira_client.base_url)
    JIRA_ENABLED = True
except (ImportError, ValueError) as e:
    print(f"Jira not configured: {e}")
    jira_client = None
    JIRA_ENABLED = False

try:
    from src.tools.slack_client import SlackClient
    slack_client = SlackClient()
    SLACK_ENABLED = True
except (ImportError, ValueError) as e:
    print(f"Slack not configured: {e}")
    slack_client = None
    SLACK_ENABLED = False

# One MCP server with all tools
MCP = FastMCP(
    "task-manager-mcp",
    host="127.0.0.1",
    port=5000,
)

breaker = TaskBreakdown()
scheduler = Scheduler()
state_store = ProjectStateStore()


@MCP.tool()
def github_get_issues(repo: str) -> str:
    """
    Return all non-PR issues from a GitHub repo as JSON string.
    repo: 'owner/repo'
    
    Returns unified issue format:
    {
        "source": "github",
        "id": "issue-123",
        "title": "...",
        "body": "...",
        "url": "...",
        "priority": "medium",
        "status": "open"
    }
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}

    resp = requests.get(
        f"https://api.github.com/repos/{repo}/issues",
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()

    # Normalize to unified format
    issues = []
    for i in resp.json():
        if "pull_request" not in i:
            issues.append({
                "source": "github",
                "id": f"issue-{i.get('number', '')}",
                "title": i.get("title", ""),
                "body": i.get("body", "") or "",
                "url": i.get("html_url", ""),
                "priority": _get_github_priority(i),
                "status": i.get("state", "open"),
                "labels": [label["name"] for label in i.get("labels", [])]
            })

    return json.dumps(issues)


def _get_github_priority(issue: Dict[str, Any]) -> str:
    """Extract priority from GitHub issue labels."""
    labels = [label["name"].lower() for label in issue.get("labels", [])]
    
    if any("high" in l or "urgent" in l or "critical" in l for l in labels):
        return "high"
    elif any("low" in l for l in labels):
        return "low"
    else:
        return "medium"


@MCP.tool()
def jira_get_issues(project_key: str, max_results: int = 50) -> str:
    """
    Return issues from a Jira project as JSON string.
    project_key: Jira project key (e.g., 'PROJ')
    max_results: Maximum number of issues to return
    
    Returns unified issue format (same as github_get_issues).
    """
    if not JIRA_ENABLED:
        return json.dumps({"error": "Jira not configured"})
    
    try:
        issues = jira_client.get_issues(project_key, max_results)
        
        # Normalize to unified format
        unified_issues = []
        for issue in issues:
            unified_issues.append({
                "source": "jira",
                "id": issue["key"],
                "title": issue["title"],
                "body": issue["body"],
                "url": issue["url"],
                "priority": issue["priority"].lower() if issue["priority"] else "medium",
                "status": issue["status"],
                "assignee": issue.get("assignee")
            })
        
        return json.dumps(unified_issues)
    except Exception as e:
        return json.dumps({"error": str(e)})


@MCP.tool()
def jira_add_comment(issue_key: str, comment: str) -> str:
    """
    Add a comment to a Jira issue.
    issue_key: Jira issue key (e.g., 'PROJ-123')
    comment: Comment text
    """
    if not JIRA_ENABLED:
        return json.dumps({"error": "Jira not configured"})
    
    try:
        result = jira_client.add_comment(issue_key, comment)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})


@MCP.tool()
def slack_notify(message: str, channel: Optional[str] = None) -> str:
    """
    Send a notification to Slack.
    message: Message text
    channel: Optional channel (defaults to SLACK_CHANNEL from .env)
    """
    if not SLACK_ENABLED:
        return json.dumps({"error": "Slack not configured"})
    
    try:
        result = slack_client.send_message(message, channel)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})


@MCP.tool()
def slack_notify_scheduled_tasks(
    issue_source: str,
    issue_title: str, 
    tasks_json: str,
    channel: Optional[str] = None
) -> str:
    """
    Send a formatted notification about scheduled tasks to Slack.
    issue_source: Source system (e.g., 'GitHub', 'Jira')
    issue_title: Title of the issue
    tasks_json: JSON string of scheduled tasks
    channel: Optional channel override
    """
    if not SLACK_ENABLED:
        return json.dumps({"error": "Slack not configured"})
    
    try:
        tasks = json.loads(tasks_json)
        result = slack_client.send_task_schedule_notification(
            issue_source, issue_title, tasks, channel
        )
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})


@MCP.tool()
def tasks_breakdown(issue_text: str) -> str:
    """
    Use Jinja + Gemini (LLMClient) to break an issue into tasks.
    Returns a JSON string list of tasks.
    
    NOTE: This uses single LLM mode. For multi-agent, use tasks_breakdown_multi.
    """
    tasks = breaker.breakdown(issue_text)
    return json.dumps(tasks)


@MCP.tool()
def tasks_breakdown_multi(issue_text: str) -> str:
    """
    Use multi-agent LLM orchestrator to break an issue into tasks.
    Uses multiple LLMs (Gemini, DeepSeek R1, GPT-4) based on configured strategy.
    Returns a JSON string list of tasks.
    
    Strategies:
    - ensemble: Query all LLMs, pick best result
    - specialized: Use each LLM for what it's best at
    - fallback: Try cheap LLMs first, fallback to expensive
    - single: Use only one LLM (same as tasks_breakdown)
    """
    if not MULTI_AGENT_ENABLED:
        return json.dumps({
            "error": "Multi-agent LLM not configured",
            "fallback": "Using single LLM mode"
        })
    
    try:
        tasks = multi_breaker.breakdown(issue_text)
        return json.dumps(tasks)
    except Exception as e:
        return json.dumps({"error": str(e)})


@MCP.tool()
def llm_get_metrics() -> str:
    """
    Get performance metrics from all configured LLMs.
    Returns JSON with cost, latency, and success rates per LLM.
    """
    if not MULTI_AGENT_ENABLED:
        return json.dumps({"error": "Multi-agent LLM not configured"})
    
    try:
        metrics = multi_breaker.get_metrics()
        return json.dumps({
            "strategy": multi_breaker.strategy,
            "llms": metrics
        })
    except Exception as e:
        return json.dumps({"error": str(e)})


@MCP.tool()
def llm_reset_metrics() -> str:
    """
    Reset performance metrics for all LLMs.
    Useful for starting fresh benchmarking.
    """
    if not MULTI_AGENT_ENABLED:
        return json.dumps({"error": "Multi-agent LLM not configured"})
    
    try:
        multi_breaker.reset_metrics()
        return json.dumps({"success": True, "message": "Metrics reset"})
    except Exception as e:
        return json.dumps({"error": str(e)})


@MCP.tool()
def tasks_schedule(tasks_json: str) -> str:
    """
    Take a JSON string of tasks and return a scheduled list (also JSON string).
    """
    tasks: List[Dict[str, Any]] = json.loads(tasks_json)
    scheduled = scheduler.schedule(tasks)
    return json.dumps(scheduled)


@MCP.tool()
def state_get_stats() -> str:
    """
    Get statistics about the project state.
    Returns JSON with total issues, tasks, and execution stats.
    """
    try:
        stats = state_store.get_stats()
        return json.dumps(stats)
    except Exception as e:
        return json.dumps({"error": str(e)})


@MCP.tool()
def state_add_issue(issue_json: str) -> str:
    """
    Add an issue to the state store.
    issue_json: JSON string of issue data
    """
    try:
        issue = json.loads(issue_json)
        state_store.add_issue(issue)
        return json.dumps({"success": True})
    except Exception as e:
        return json.dumps({"error": str(e)})


@MCP.tool()
def state_add_scheduled_tasks(issue_key: str, tasks_json: str) -> str:
    """
    Add scheduled tasks to the state store.
    issue_key: Issue identifier (source:id)
    tasks_json: JSON string of scheduled tasks
    """
    try:
        tasks = json.loads(tasks_json)
        state_store.add_scheduled_tasks(issue_key, tasks)
        return json.dumps({"success": True})
    except Exception as e:
        return json.dumps({"error": str(e)})


@MCP.tool()
def state_log_execution(action: str, details_json: str, success: bool = True) -> str:
    """
    Log an execution event.
    action: Action name
    details_json: JSON string of action details
    success: Whether action succeeded
    """
    try:
        details = json.loads(details_json)
        state_store.log_execution(action, details, success)
        return json.dumps({"success": True})
    except Exception as e:
        return json.dumps({"error": str(e)})


@MCP.tool()
def calendar_create_event(summary: str, start: str, end: str) -> str:
    from googleapiclient.errors import HttpError

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    token_path = os.path.join(root, "token.json")

    creds = Credentials.from_authorized_user_file(token_path)
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": summary,
        "start": {
            "dateTime": start,
            "timeZone": "Europe/Zurich",
        },
        "end": {
            "dateTime": end,
            "timeZone": "Europe/Zurich",
        },
    }

    try:
        created = service.events().insert(calendarId="primary", body=event).execute()
        print("Created event:", created.get("summary"))
        print("Start:", created.get("start"))
        print("End:", created.get("end"))
        print("Link:", created.get("htmlLink"))
        return "ok"
    except HttpError as e:
        print("Calendar API error:", e)
        return f"error: {e}"

if __name__ == "__main__":
    # HTTP MCP server on http://127.0.0.1:5000/mcp
    MCP.run(transport="streamable-http", mount_path="/mcp")
