# 🚀 How to Use the DevOps Task Scheduler

## Quick Start Guide

### Prerequisites
1. Activate your conda environment:
   ```bash
   conda activate agent-env
   ```

2. Make sure `.env` file is configured with API keys

---

## 📋 Testing Options

### **Option 1: Simple Demo (Easiest - No MCP Server)**

**What it tests:**
- Task breakdown using AI
- Task scheduling
- Dependency analysis

**How to run:**
```bash
python tests/demo_agent.py
```

**What it does:**
- Uses sample GitHub issues
- Breaks them down into tasks using LLM
- Schedules tasks into time blocks
- Shows results in terminal

---

### **Option 2: System Verification**

**What it tests:**
- All components are installed
- API keys are configured
- Dependencies are available

**How to run:**
```bash
python verify_system.py
```

**What it does:**
- Checks Python version
- Verifies required files exist
- Tests API key configuration
- Tests LLM connectivity
- Tests task breakdown
- Tests scheduling

---

### **Option 3: Full Agent with MCP Server**

**What it tests:**
- Complete workflow: GitHub → LLM → Schedule → Calendar
- Real GitHub API integration
- Calendar event creation

**How to run:**

**Terminal 1 (Start MCP Server):**
```bash
python src/tools/mcp_server.py
```
Wait for: `MCP server runs on http://127.0.0.1:5000/mcp`

**Terminal 2 (Run Agent):**
```bash
python src/agent/run_agent.py
```

**What it does:**
1. Fetches real issues from GitHub repo
2. Breaks down each issue into tasks
3. Schedules tasks
4. Creates Google Calendar events

**Note:** Edit `src/agent/run_agent.py` line 63 to change the repository:
```python
asyncio.run(run_agent("your-username/your-repo"))
```

---

### **Option 4: Multi-Agent Runner**

**What it tests:**
- Multiple LLM providers working together
- Strategy comparison (single, specialized, fallback, ensemble)
- Performance metrics

**How to run:**
```bash
# Default (specialized strategy)
python src/agent/multi_agent_runner.py

# Or specify strategy:
LLM_STRATEGY=single python src/agent/multi_agent_runner.py
LLM_STRATEGY=specialized python src/agent/multi_agent_runner.py
LLM_STRATEGY=fallback python src/agent/multi_agent_runner.py
LLM_STRATEGY=ensemble python src/agent/multi_agent_runner.py
```

**What it does:**
- Fetches GitHub issues
- Compares single vs multi-agent breakdown
- Shows which LLM was used
- Displays performance metrics

---

### **Option 5: Enhanced Agent (Full Features)**

**What it tests:**
- GitHub + Jira integration
- Multi-agent LLM processing
- State persistence
- Slack notifications
- Calendar events
- Reasoning controller

**How to run:**

**Terminal 1 (Start MCP Server):**
```bash
python src/tools/mcp_server.py
```

**Terminal 2 (Run Enhanced Agent):**
```bash
# With GitHub only
GITHUB_REPO=your-username/your-repo python src/agent/enhanced_agent.py

# With Jira only
JIRA_PROJECT=PROJ python src/agent/enhanced_agent.py

# With both
GITHUB_REPO=your-username/your-repo JIRA_PROJECT=PROJ python src/agent/enhanced_agent.py
```

**What it does:**
1. Fetches issues from GitHub and/or Jira
2. Checks state store (prevents duplicates)
3. Uses reasoning controller to decide actions
4. Breaks down with multi-agent LLM
5. Validates plan
6. Schedules tasks
7. Creates calendar events
8. Sends Slack notifications
9. Saves to state store

---

## 🧪 Testing Individual Components

### Test LLM Client
```python
from src.core.llm_factory import LLMFactory

# Create all available clients
clients = LLMFactory.create_all_available_clients()

# Test a specific client
github_client = clients.get("github")
if github_client:
    response = github_client.generate("Hello, test prompt")
    print(response.content)
```

### Test Task Breakdown
```python
from src.core.task_breakdown import TaskBreakdown

breaker = TaskBreakdown()
issue_text = "Implement user login system"
tasks = breaker.breakdown(issue_text)
print(tasks)
```

### Test Scheduler
```python
from src.core.scheduler import Scheduler

scheduler = Scheduler()
tasks = [
    {"task": "Setup database", "duration": 2, "depends_on": []},
    {"task": "Create API", "duration": 3, "depends_on": ["Setup database"]}
]
schedule = scheduler.schedule(tasks)
print(schedule)
```

### Test API Clients
```python
# GitHub (via MCP server)
# See: src/tools/mcp_server.py - github_get_issues()

# Jira
from src.tools.jira_client import JiraClient
jira = JiraClient()
issues = jira.get_issues("PROJ")
print(issues)

# Slack
from src.tools.slack_client import SlackClient
slack = SlackClient()
slack.send_message("Test message", "#general")
```

---

## 📊 Expected Output Examples

### Demo Agent Output:
```
======================================================================
🚀 REAL AGENT DEMO - DIRECT TEST
======================================================================

📦 Loading agent components...
✅ All components loaded

📥 Simulating GitHub issue fetch...
✅ Found 2 issues

======================================================================
📋 ISSUE #42: Implement user authentication system
======================================================================

🤖 Step 1: AI Task Breakdown...
   Using: GitHub Models (FREE!)

✅ Generated 4 tasks:

   1. Setup database schema for users
      ⏱️  Duration: 2 hours
      🔗 Depends on: 

   2. Implement password hashing
      ⏱️  Duration: 1.5 hours
      🔗 Depends on: Setup database schema for users

   ...

📅 Step 2: Scheduling tasks...

✅ Created 4 time blocks:

   1. Setup database schema for users
      📅 2024-01-15T08:00:00 → 2024-01-15T10:00:00

   2. Implement password hashing
      📅 2024-01-15T10:00:00 → 2024-01-15T11:30:00

   ...
```

---

## 🔧 Troubleshooting

### Import Errors
```bash
# Make sure you're in the project root
cd /Users/jiaqiyu/Desktop/Devops_and_LLMs-master

# Activate conda environment
conda activate agent-env

# Set PYTHONPATH if needed
export PYTHONPATH=$PWD:$PYTHONPATH
```

### API Key Errors
- Check `.env` file exists
- Verify API keys are set (no placeholders)
- Run `python verify_system.py` to check

### MCP Server Errors
- Make sure port 5000 is not in use
- Check MCP server is running before running agents
- Verify all dependencies are installed

---

## 📝 Quick Reference

| Test | Command | What It Tests |
|------|---------|---------------|
| Simple Demo | `python tests/demo_agent.py` | Task breakdown + scheduling |
| System Check | `python verify_system.py` | All components |
| Full Agent | `python src/agent/run_agent.py` | Complete workflow |
| Multi-Agent | `python src/agent/multi_agent_runner.py` | Multiple LLMs |
| Enhanced | `python src/agent/enhanced_agent.py` | All features |

---

## 🎯 Recommended Testing Order

1. **Start with:** `python verify_system.py` - Verify everything is set up
2. **Then try:** `python tests/demo_agent.py` - Simple test without MCP
3. **Next:** Start MCP server and run `python src/agent/run_agent.py`
4. **Finally:** Try enhanced agent with all features

---

## 💡 Tips

- Always activate conda environment first
- Check `.env` file has valid API keys
- For MCP-based tests, start server first
- Use `verify_system.py` to diagnose issues
- Check terminal output for detailed error messages




