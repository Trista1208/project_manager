# Enhanced Features Guide

## 🚀 New Features Added

Your project now includes all the major features from your proposal:

### ✅ Phase 1 (Original - Complete)
- GitHub issue reading
- LLM task breakdown (Gemini)
- Dependency-aware scheduling
- Google Calendar integration

### ✅ Phase 2 (New - Complete)
- **Jira Integration** - Fetch and process Jira issues
- **Unified Task Model** - Consistent format for GitHub + Jira
- **Slack Notifications** - Rich formatted notifications
- **Project State Store** - Persistent state across runs
- **Enhanced Orchestration** - Better agent logic

---

## Architecture Overview

```
┌─────────────┐  ┌──────────────┐
│   GitHub    │  │     Jira     │
│   Issues    │  │    Issues    │
└──────┬──────┘  └──────┬───────┘
       │                │
       └────────┬───────┘
                │
                ▼
    ┌───────────────────────┐
    │  Enhanced Agent       │
    │  (Orchestrator)       │
    └───────────┬───────────┘
                │
        ┌───────┴────────┐
        │                │
        ▼                ▼
┌───────────────┐  ┌──────────────┐
│ LLM Breakdown │  │  State Store │
│   (Gemini)    │  │ (Persistent) │
└───────┬───────┘  └──────────────┘
        │
        ▼
┌───────────────┐
│   Scheduler   │
│  (8-12,14-17) │
└───────┬───────┘
        │
   ┌────┴──────┐
   │           │
   ▼           ▼
┌──────────┐ ┌────────┐
│ Calendar │ │ Slack  │
│  Events  │ │ Notify │
└──────────┘ └────────┘
```

---

## Setup Instructions

### 1. Update Dependencies

Add to `environment.yml` (if not already present):

```yaml
- pip:
    - requests  # Already present
    # All other dependencies already included
```

### 2. Configure Environment Variables

Copy the template:
```bash
cp env.template .env
```

Edit `.env` with your credentials:

#### Required (for basic functionality):
```env
GOOGLE_API_KEY=your_gemini_key
GITHUB_TOKEN=your_github_token
```

#### Optional (for enhanced features):

**Jira Configuration:**
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Create API token
3. Add to `.env`:
```env
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_api_token
```

**Slack Configuration:**
1. Go to https://api.slack.com/apps
2. Create a new app → "From scratch"
3. Add Bot Token Scopes:
   - `chat:write`
   - `chat:write.public`
4. Install app to workspace
5. Copy Bot User OAuth Token
6. Add to `.env`:
```env
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_CHANNEL=#project-updates
```

---

## Usage

### Option 1: Original Agent (GitHub only)

```bash
python src/agent/run_agent.py
```

Uses hardcoded repo: `BaHu-Git/Task_Manager`

### Option 2: Enhanced Agent (GitHub + Jira + Slack)

```bash
python src/agent/enhanced_agent.py
```

Reads configuration from environment variables or `.env`:
- `GITHUB_REPO` - GitHub repository
- `JIRA_PROJECT` - Jira project key
- `MAX_ISSUES` - Maximum issues to process (default: 5)

**Examples:**

Process GitHub only:
```bash
GITHUB_REPO="owner/repo" python src/agent/enhanced_agent.py
```

Process Jira only:
```bash
JIRA_PROJECT="PROJ" python src/agent/enhanced_agent.py
```

Process both:
```bash
GITHUB_REPO="owner/repo" JIRA_PROJECT="PROJ" python src/agent/enhanced_agent.py
```

---

## New Features in Detail

### 1. Jira Integration

**Capabilities:**
- Fetch issues from Jira projects
- Filter by status (automatically excludes Done)
- Extract priority and assignee information
- Add comments to Jira issues
- Transition issues between statuses

**Usage Example:**
```python
from src.tools.jira_client import JiraClient

client = JiraClient()

# Fetch issues
issues = client.get_issues("PROJ", max_results=10)

# Add comment
client.add_comment("PROJ-123", "Tasks scheduled by agent")

# Transition issue
client.transition_issue("PROJ-123", "In Progress")
```

**MCP Tools:**
- `jira_get_issues(project_key, max_results)` - Fetch issues
- `jira_add_comment(issue_key, comment)` - Add comment

---

### 2. Slack Notifications

**Capabilities:**
- Send formatted task schedules
- Rich message formatting with Block Kit
- Error notifications
- Customizable channels

**Features:**
- 🎯 Header with source system (GitHub/Jira)
- 📋 Issue title
- ⏰ Task schedule with times
- 🔗 Dependency information
- 📊 Duration estimates

**Usage Example:**
```python
from src.tools.slack_client import SlackClient

client = SlackClient()

# Simple message
client.send_message("Hello from agent!")

# Formatted task notification
client.send_task_schedule_notification(
    issue_source="GitHub",
    issue_title="Add login feature",
    tasks=[...],
    channel="#dev-team"
)
```

**MCP Tools:**
- `slack_notify(message, channel)` - Simple message
- `slack_notify_scheduled_tasks(...)` - Formatted task notification

---

### 3. Project State Store

**Capabilities:**
- Persistent storage of issues and tasks
- Execution history tracking
- Statistics and analytics
- JSON-based file storage

**Stored Data:**
- Issues from all sources (GitHub, Jira)
- Scheduled tasks with timestamps
- Task status (scheduled, in_progress, completed)
- Execution history (last 1000 events)
- Aggregate statistics

**Storage Location:**
```
project_root/state/
├── project_state.json      # Current state
└── execution_history.json  # History log
```

**Usage Example:**
```python
from src.core.state_store import ProjectStateStore

store = ProjectStateStore()

# Add issue
store.add_issue({
    "source": "github",
    "id": "issue-123",
    "title": "..."
})

# Add scheduled tasks
store.add_scheduled_tasks("github:issue-123", tasks)

# Get statistics
stats = store.get_stats()
print(f"Total tasks: {stats['total_scheduled_tasks']}")

# Get history
history = store.get_history(action="process_issue", limit=10)
```

**MCP Tools:**
- `state_get_stats()` - Get statistics
- `state_add_issue(issue_json)` - Store issue
- `state_add_scheduled_tasks(...)` - Store scheduled tasks
- `state_log_execution(...)` - Log execution event

---

### 4. Unified Task Model

All issues are normalized to a consistent format regardless of source:

```json
{
  "source": "github" | "jira",
  "id": "issue-123" | "PROJ-123",
  "title": "Issue title",
  "body": "Issue description",
  "url": "https://...",
  "priority": "high" | "medium" | "low",
  "status": "open" | "in progress" | "done",
  "labels": ["bug", "feature"],  // GitHub only
  "assignee": "John Doe"          // Jira only
}
```

This allows the agent to process issues from any source uniformly.

---

## Feature Comparison

| Feature | Original Agent | Enhanced Agent |
|---------|---------------|----------------|
| GitHub | ✅ | ✅ |
| Jira | ❌ | ✅ |
| Slack | ❌ | ✅ |
| State Persistence | ❌ | ✅ |
| Statistics | ❌ | ✅ |
| Execution History | ❌ | ✅ |
| Multi-source | ❌ | ✅ |
| Error Logging | Limited | ✅ Full |
| Notification | ❌ | ✅ Rich |

---

## Testing the Enhanced Features

### Test 1: GitHub + Slack

1. Configure GitHub and Slack in `.env`
2. Run: `python src/agent/enhanced_agent.py`
3. Check Slack channel for notifications
4. Verify calendar events created

### Test 2: Jira Only

1. Configure Jira in `.env`
2. Run with Jira project:
```bash
JIRA_PROJECT="YOUR-PROJECT" python src/agent/enhanced_agent.py
```
3. Check calendar and Slack

### Test 3: Both Sources

1. Configure both GitHub and Jira
2. Set environment variables:
```bash
export GITHUB_REPO="owner/repo"
export JIRA_PROJECT="PROJ"
export MAX_ISSUES=3
```
3. Run: `python src/agent/enhanced_agent.py`
4. Verify issues from both sources are processed

### Test 4: State Persistence

1. Run agent and note statistics
2. Run again - statistics should accumulate
3. Check state files:
```bash
cat state/project_state.json
cat state/execution_history.json
```

---

## Troubleshooting

### Jira Not Working

**Error:** "Jira not configured"

**Solution:**
1. Check `.env` has `JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`
2. Verify API token is valid
3. Check Jira URL format: `https://domain.atlassian.net` (no trailing slash)

**Error:** "Failed to fetch Jira issues"

**Solution:**
1. Verify project key is correct (e.g., "PROJ", not "proj")
2. Check you have permission to access the project
3. Test Jira API manually:
```bash
curl -u your-email@example.com:your-api-token \
  https://your-domain.atlassian.net/rest/api/3/project
```

### Slack Not Working

**Error:** "Slack not configured"

**Solution:**
1. Check `.env` has `SLACK_BOT_TOKEN`
2. Verify token starts with `xoxb-`
3. Check bot is installed in workspace

**Error:** "channel_not_found"

**Solution:**
1. Add bot to the channel in Slack
2. Or use public channel with bot scope `chat:write.public`
3. Verify channel name in `.env` includes `#`

### State Store Issues

**Error:** Permission denied writing to state/

**Solution:**
```bash
mkdir -p state
chmod 755 state
```

**Clear State:**
```python
from src.core.state_store import ProjectStateStore
store = ProjectStateStore()
store.clear_state()
```

---

## Advanced Usage

### Custom Orchestration

Create your own agent logic:

```python
from src.agent.enhanced_agent import EnhancedAgent

async def custom_workflow():
    async with streamablehttp_client(HOST) as streams:
        async with ClientSession(*streams) as session:
            agent = EnhancedAgent()
            await agent.initialize(session)
            
            # Fetch from both sources
            issues = await agent.fetch_issues(
                github_repo="owner/repo",
                jira_project="PROJ"
            )
            
            # Filter high priority only
            high_priority = [
                i for i in issues 
                if i.get("priority") == "high"
            ]
            
            # Process high priority first
            for issue in high_priority:
                await agent.process_issue(issue)
```

### Adding Jira Comments

After scheduling, add comments to Jira:

```python
# In enhanced_agent.py, after calendar creation:
if issue["source"] == "jira":
    comment = f"Tasks scheduled:\n"
    for task in scheduled:
        comment += f"• {task['task']} ({task['start']})\n"
    
    await self.session.call_tool(
        "jira_add_comment",
        {
            "issue_key": issue["id"],
            "comment": comment
        }
    )
```

---

## Performance Considerations

### Rate Limits

- **GitHub:** 5000 requests/hour with token
- **Jira:** Cloud: 1000 requests/hour per IP
- **Slack:** Tier 1: 1 message/second

**Recommendation:** Add delays between issues (already implemented: 0.5s)

### LLM Costs

Gemini 2.0 Flash pricing (as of 2024):
- Input: $0.075 per 1M tokens
- Output: $0.30 per 1M tokens

**Typical issue breakdown:**
- ~500 input tokens
- ~200 output tokens
- Cost: ~$0.0001 per issue

**For 100 issues/day:**
- ~$0.01/day = ~$3.65/year

Very affordable! 💰

---

## Next Steps

Now that you have all enhanced features:

1. ✅ **Test each integration individually**
   - GitHub only
   - Jira only
   - Slack notifications
   - State persistence

2. ✅ **Test combined workflow**
   - GitHub + Jira + Slack + State

3. ✅ **Create demo scenarios**
   - Show teacher full workflow
   - Document results

4. ✅ **Update proposal**
   - Mark Phase 2 as complete
   - Show architecture diagram

5. 📈 **Optional extensions** (if time permits)
   - Rescheduling logic
   - Multi-user support
   - Web dashboard for state

---

## Comparison to Proposal

Your proposal described these components - **all now implemented:**

| Proposal Component | Implementation |
|-------------------|----------------|
| Integration Layer (GitHub, Jira, Calendar, Slack) | ✅ All integrated |
| Project State Store | ✅ `ProjectStateStore` class |
| LLM Decision Engine | ✅ Task breakdown with Gemini |
| Agent Orchestrator | ✅ `EnhancedAgent` class |
| Action Executor | ✅ Calendar + Slack + Jira actions |

**You now have a complete system matching your proposal! 🎉**

---

## Files Added/Modified

### New Files:
- `src/tools/jira_client.py` - Jira API integration
- `src/tools/slack_client.py` - Slack API integration
- `src/core/state_store.py` - Persistent state management
- `src/agent/enhanced_agent.py` - Enhanced orchestrator
- `ENHANCED_FEATURES.md` - This file

### Modified Files:
- `src/tools/mcp_server.py` - Added Jira, Slack, state tools
- `env.template` - Added Jira and Slack configuration

### Unchanged:
- `src/core/llm.py` - Still using Gemini
- `src/core/scheduler.py` - Same scheduling logic
- `src/core/task_breakdown.py` - Same breakdown logic
- `src/agent/run_agent.py` - Original agent still works

---

## Summary

✅ **Your project now includes:**
- ✅ GitHub + Jira integration (unified model)
- ✅ Slack notifications (rich formatting)
- ✅ Persistent state store (JSON-based)
- ✅ Enhanced orchestration (EnhancedAgent)
- ✅ Execution logging and statistics
- ✅ Backward compatible (original agent still works)

**This significantly exceeds the minimum requirements and demonstrates a complete DevOps AI platform!** 🚀

For questions or issues, check `BEST_PRACTICES.md` or `SETUP_GUIDE.md`.

