# Migration Guide: Original → Enhanced Agent

## Overview

You now have **two agents** in your project:

1. **Original Agent** (`run_agent.py`) - Simple, GitHub-only
2. **Enhanced Agent** (`enhanced_agent.py`) - Full-featured with Jira, Slack, state

Both work independently. You can use either or both!

---

## Quick Comparison

| Feature | Original | Enhanced |
|---------|----------|----------|
| GitHub | ✅ | ✅ |
| Jira | ❌ | ✅ |
| Slack | ❌ | ✅ |
| State Persistence | ❌ | ✅ |
| Statistics | ❌ | ✅ |
| History Logging | ❌ | ✅ |
| Configuration | Hardcoded | Environment vars |

---

## Using the Original Agent (No Changes Needed!)

Your original agent still works exactly as before:

```bash
# Terminal 1: Start MCP server
python src/tools/mcp_server.py

# Terminal 2: Run original agent
python src/agent/run_agent.py
```

**What it does:**
- Fetches from `BaHu-Git/Task_Manager` (hardcoded)
- Breaks down issues with Gemini
- Schedules to calendar
- No Jira, no Slack, no state

**When to use:**
- Quick tests
- Simple GitHub-only workflows
- When you don't need persistence

---

## Using the Enhanced Agent

The enhanced agent adds many features but requires configuration:

### Step 1: Update .env

```bash
# Copy template if you haven't
cp env.template .env
```

Edit `.env` and add (as needed):

```env
# Required (you already have these)
GOOGLE_API_KEY=your_key
GITHUB_TOKEN=your_token

# Optional - add if you want Jira
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_token

# Optional - add if you want Slack
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_CHANNEL=#project-updates

# Optional - configure defaults
GITHUB_REPO=owner/repo
JIRA_PROJECT=PROJ
MAX_ISSUES=5
```

### Step 2: Run Enhanced Agent

```bash
# Terminal 1: Start MCP server (same as before)
python src/tools/mcp_server.py

# Terminal 2: Run enhanced agent
python src/agent/enhanced_agent.py
```

**What it does:**
- Fetches from GitHub (if `GITHUB_REPO` set)
- Fetches from Jira (if `JIRA_PROJECT` set)
- Breaks down and schedules (same as original)
- Sends Slack notifications (if configured)
- Saves state to `state/` directory
- Logs execution history

---

## Migration Strategies

### Strategy 1: Gradual (Recommended)

Add features one at a time:

**Week 1: Test original agent**
```bash
python src/agent/run_agent.py
```
Validate basic functionality works.

**Week 2: Add GitHub to enhanced**
```bash
# .env
GITHUB_REPO=your-test-repo

# Run
python src/agent/enhanced_agent.py
```
Verify state persistence works.

**Week 3: Add Jira**
```bash
# .env
GITHUB_REPO=your-test-repo
JIRA_PROJECT=YOUR-PROJ

# Run
python src/agent/enhanced_agent.py
```
Verify Jira integration works.

**Week 4: Add Slack**
```bash
# .env
GITHUB_REPO=your-test-repo
JIRA_PROJECT=YOUR-PROJ
SLACK_BOT_TOKEN=xoxb-...
SLACK_CHANNEL=#updates

# Run
python src/agent/enhanced_agent.py
```
Verify end-to-end workflow.

### Strategy 2: All-In (If time is short)

Configure everything at once:

1. Setup Jira (see `ENHANCED_FEATURES.md`)
2. Setup Slack (see `ENHANCED_FEATURES.md`)
3. Configure `.env` with all credentials
4. Test with small datasets first
5. Run full workflow

---

## Configuration Options

### Environment Variables

The enhanced agent reads these (in order of priority):

1. **Command-line environment**
   ```bash
   GITHUB_REPO="owner/repo" python src/agent/enhanced_agent.py
   ```

2. **Exported variables**
   ```bash
   export GITHUB_REPO="owner/repo"
   python src/agent/enhanced_agent.py
   ```

3. **`.env` file** (recommended)
   ```env
   GITHUB_REPO=owner/repo
   ```

### Flexible Usage

**GitHub only:**
```bash
GITHUB_REPO="owner/repo" python src/agent/enhanced_agent.py
```

**Jira only:**
```bash
JIRA_PROJECT="PROJ" python src/agent/enhanced_agent.py
```

**Both:**
```bash
GITHUB_REPO="owner/repo" JIRA_PROJECT="PROJ" python src/agent/enhanced_agent.py
```

**Limit issues:**
```bash
MAX_ISSUES=3 python src/agent/enhanced_agent.py
```

---

## New Directory Structure

After running the enhanced agent, you'll see:

```
Devops_and_LLMs/
├── state/                          ← NEW! Persistent state
│   ├── project_state.json         ← Current state
│   └── execution_history.json     ← Execution log
├── .env                            ← Your configuration
├── credentials.json                ← Google OAuth (existing)
├── token.json                      ← Google token (existing)
└── src/
    ├── agent/
    │   ├── run_agent.py           ← Original (unchanged)
    │   └── enhanced_agent.py       ← NEW! Enhanced agent
    ├── core/
    │   ├── llm.py                 ← Unchanged
    │   ├── scheduler.py           ← Unchanged
    │   ├── task_breakdown.py      ← Unchanged
    │   └── state_store.py          ← NEW! State management
    └── tools/
        ├── mcp_server.py          ← Enhanced with new tools
        ├── jira_client.py         ← NEW! Jira integration
        └── slack_client.py        ← NEW! Slack integration
```

---

## Backward Compatibility

### ✅ What Still Works

- Original agent (`run_agent.py`) - **unchanged**
- Core modules (LLM, scheduler, breakdown) - **unchanged**
- MCP server - **backward compatible**
- Original MCP tools - **still available**

### 🆕 What's New

- Additional MCP tools (Jira, Slack, state)
- Enhanced agent with orchestration
- State persistence
- Graceful degradation (features disable if not configured)

### 🔒 What Won't Break

The MCP server gracefully handles missing configuration:

```python
# If Jira not configured:
jira_get_issues() → returns {"error": "Jira not configured"}

# If Slack not configured:
slack_notify() → returns {"error": "Slack not configured"}
```

Your original agent ignores these tools, so it's unaffected.

---

## Testing Migration

### Test 1: Verify Original Still Works

```bash
python src/tools/mcp_server.py  # Terminal 1
python src/agent/run_agent.py   # Terminal 2
```

Expected: Works exactly as before.

### Test 2: Enhanced with GitHub Only

```bash
# .env
GITHUB_REPO=BaHu-Git/Task_Manager

# Run
python src/agent/enhanced_agent.py
```

Expected:
- Fetches GitHub issues
- Creates calendar events
- Saves to `state/`
- No Jira/Slack errors

### Test 3: Add Jira

```bash
# .env
GITHUB_REPO=BaHu-Git/Task_Manager
JIRA_PROJECT=YOUR-PROJ

# Run
python src/agent/enhanced_agent.py
```

Expected:
- Fetches from both sources
- Processes all issues
- Unified in state store

### Test 4: Add Slack

```bash
# Configure SLACK_BOT_TOKEN in .env

# Run
python src/agent/enhanced_agent.py
```

Expected:
- Rich notifications in Slack
- Formatted task schedules

---

## Troubleshooting Migration

### "Module not found" errors

**Problem:** Import errors for new modules.

**Solution:**
```bash
# Reinstall environment
conda env update -f environment.yml
conda activate agent-env
```

### Original agent has errors

**Problem:** MCP server changes broke original agent.

**Solution:**
The original agent should still work. If not:
1. Check MCP server starts: `python src/tools/mcp_server.py`
2. Verify tools list with MCP inspector
3. Check for Python syntax errors

### State directory issues

**Problem:** Permission denied writing to `state/`

**Solution:**
```bash
mkdir -p state
chmod 755 state
```

### Jira/Slack not working

**Problem:** Enhanced agent shows errors.

**Solution:**
Features are optional! If not configured:
- Jira: Agent skips Jira fetching
- Slack: Agent skips notifications
- Agent still processes GitHub issues

---

## Rollback Plan

If you need to go back to simpler setup:

### Option 1: Use Original Agent
Just use `run_agent.py` - no changes needed!

### Option 2: Remove Enhanced Features

```bash
# Delete new files
rm src/agent/enhanced_agent.py
rm src/tools/jira_client.py
rm src/tools/slack_client.py
rm src/core/state_store.py

# Restore original mcp_server.py from git
git checkout src/tools/mcp_server.py
```

### Option 3: Keep Both (Recommended)

Keep both agents and use whichever suits your needs:
- Original for simple tests
- Enhanced for full demos

---

## Best Practices

### Development Workflow

1. **Test with original agent first**
   - Verify basic functionality
   - Validate environment setup

2. **Move to enhanced for demos**
   - Show full capabilities
   - Impress your teacher!

3. **Use environment variables for flexibility**
   ```bash
   # Quick test
   MAX_ISSUES=1 python src/agent/enhanced_agent.py
   
   # Full demo
   MAX_ISSUES=5 python src/agent/enhanced_agent.py
   ```

### Configuration Management

Keep multiple `.env` files:

```bash
# .env.basic - Minimum config
GOOGLE_API_KEY=...
GITHUB_TOKEN=...
GITHUB_REPO=test-repo

# .env.full - Everything
GOOGLE_API_KEY=...
GITHUB_TOKEN=...
GITHUB_REPO=test-repo
JIRA_URL=...
JIRA_EMAIL=...
JIRA_API_TOKEN=...
SLACK_BOT_TOKEN=...
SLACK_CHANNEL=#updates

# Switch between them
cp .env.basic .env    # For simple tests
cp .env.full .env     # For full demos
```

### State Management

**Clear state between test runs:**
```python
from src.core.state_store import ProjectStateStore
store = ProjectStateStore()
store.clear_state()
```

**Or manually:**
```bash
rm -rf state/
```

**Export state for analysis:**
```python
store.export_state("backup_state.json")
```

---

## Summary

✅ **Your original agent is unchanged and still works**

✅ **Enhanced agent adds powerful features**

✅ **Both can coexist - use whichever fits your need**

✅ **Migration is gradual - add features when ready**

✅ **Everything is backward compatible**

---

## Next Steps

1. ✅ Test original agent (verify it works)
2. ✅ Try enhanced agent with GitHub only
3. 📈 Add Jira if you have access
4. 📈 Add Slack for notifications
5. 🎓 Demo to teacher with full features!

For detailed setup of new features, see:
- `ENHANCED_FEATURES.md` - Feature documentation
- `SETUP_GUIDE.md` - Setup instructions
- `BEST_PRACTICES.md` - Tips and tricks

