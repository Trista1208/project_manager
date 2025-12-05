# MCP Task Agent (GitHub/Jira → AI Planning → Calendar/Slack)

**Status:** ✅ Complete DevOps AI Platform - **Exceeds project requirements!**

## 🎯 What This Does

An intelligent project-management platform that integrates LLMs with DevOps workflows to automatically organize tasks, schedule work, and coordinate resources.

### Core Features
1. **Multi-Source Integration** - Reads issues from GitHub and/or Jira
2. **AI Task Breakdown** - Uses Gemini to break issues into actionable tasks
3. **Smart Scheduling** - Dependency-aware scheduling (08–12, 14–17 work hours)
4. **Calendar Integration** - Auto-creates Google Calendar events
5. **Slack Notifications** - Rich formatted notifications to your team
6. **State Persistence** - Tracks all issues, tasks, and execution history

---

## 🚀 Quick Start

### For Basic Features (GitHub + Calendar):
```bash
# 1. Setup environment
conda env create -f environment.yml
conda activate agent-env

# 2. Configure (see QUICK_START.md for details)
cp env.template .env
# Edit .env with your API keys

# 3. Run
python src/tools/mcp_server.py  # Terminal 1
python src/agent/run_agent.py   # Terminal 2
```

### For Enhanced Features (+ Jira + Slack):
```bash
# Configure Jira and Slack in .env (see ENHANCED_FEATURES.md)
python src/tools/mcp_server.py      # Terminal 1
python src/agent/enhanced_agent.py  # Terminal 2
```

---

## 📚 Documentation

### 🎯 **[`START_HERE.md`](START_HERE.md)** ← **READ THIS FIRST!**

### Getting Started
- **🚀 [`QUICK_START.md`](QUICK_START.md)** - Fast 30-minute setup
- **📖 [`SETUP_GUIDE.md`](SETUP_GUIDE.md)** - Detailed setup instructions
- **⚡ [`ENHANCED_FEATURES.md`](ENHANCED_FEATURES.md)** - **NEW!** Jira, Slack, state store
- **🔄 [`MIGRATION_GUIDE.md`](MIGRATION_GUIDE.md)** - Upgrade from original agent

### Planning & Development
- **🧪 [`TEST_SCENARIOS.md`](TEST_SCENARIOS.md)** - Test cases to validate the system
- **📊 [`PROPOSAL_ALIGNMENT.md`](PROPOSAL_ALIGNMENT.md)** - Proposal vs implementation
- **💡 [`BEST_PRACTICES.md`](BEST_PRACTICES.md)** - Code quality and best practices
- **📋 [`IMPLEMENTATION_SUMMARY.md`](IMPLEMENTATION_SUMMARY.md)** - Complete technical overview

---

## 🏗️ Architecture

```
┌─────────────┐  ┌──────────────┐
│   GitHub    │  │     Jira     │
│   Issues    │  │    Issues    │
└──────┬──────┘  └──────┬───────┘
       │                │
       └────────┬───────┘
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

## ✨ Features

| Feature | Status | Description |
|---------|--------|-------------|
| **GitHub Integration** | ✅ | Fetch and process GitHub issues |
| **Jira Integration** | ✅ | Fetch and process Jira issues |
| **Unified Task Model** | ✅ | Consistent format across sources |
| **AI Task Breakdown** | ✅ | Gemini-powered task generation |
| **Dependency Resolution** | ✅ | Topological sort for task order |
| **Smart Scheduling** | ✅ | Business hours, no overlaps |
| **Google Calendar** | ✅ | Auto-create calendar events |
| **Slack Notifications** | ✅ | Rich formatted messages |
| **State Persistence** | ✅ | JSON-based state store |
| **Execution History** | ✅ | Track all agent actions |
| **Statistics & Analytics** | ✅ | Task and issue metrics |

---

## 📦 What's Included

### Core Modules
- `src/core/llm.py` - Gemini LLM client
- `src/core/task_breakdown.py` - Issue → tasks conversion
- `src/core/scheduler.py` - Dependency-aware scheduler
- `src/core/state_store.py` - **NEW!** Persistent state management

### Integration Clients
- `src/tools/jira_client.py` - **NEW!** Jira API integration
- `src/tools/slack_client.py` - **NEW!** Slack API integration
- `src/tools/mcp_server.py` - MCP tool server

### Agents
- `src/agent/run_agent.py` - Original agent (GitHub only)
- `src/agent/enhanced_agent.py` - **NEW!** Full-featured agent

---

## 🎓 Project Status

### Phase 1: MVP ✅ Complete
- GitHub integration
- LLM task breakdown
- Dependency scheduling
- Google Calendar

**Teacher's quote:** "Achieving just this already guarantees a passing-level project" ✅

### Phase 2: Enhanced ✅ Complete
- Jira integration
- Slack notifications
- State persistence
- Multi-source support

**Result:** Complete DevOps AI Platform matching full proposal! 🎉

---

## 🧪 Testing

See [`TEST_SCENARIOS.md`](TEST_SCENARIOS.md) for detailed test cases.

**Quick test:**
```bash
# Test GitHub + all features
GITHUB_REPO="owner/repo" python src/agent/enhanced_agent.py

# Test Jira only
JIRA_PROJECT="PROJ" python src/agent/enhanced_agent.py

# Test both
GITHUB_REPO="owner/repo" JIRA_PROJECT="PROJ" python src/agent/enhanced_agent.py
```

---

## 1. Clone + environment

```bash
git clone https://github.com/Meupi/Devops_and_LLMs.git
cd Devops_and_LLMs

conda env create -f environment.yml
conda activate agent-env
```

---

## 2. .env (API keys)

Create a file `.env` in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_token_here
```

- `GOOGLE_API_KEY`: Gemini 2.5 Flash API key  
- `GITHUB_TOKEN`: GitHub personal access token with `repo` scope

---

## 3. Google Calendar setup (each dev uses their own account)

Each developer does this once:

1. Go to **Google Cloud Console**  
2. Create or select a project  
3. Enable **Google Calendar API**  
4. Go to **APIs & Services → Credentials**  
   - Create **OAuth client ID → Desktop app**  
   - Download the `credentials.json`
5. Put **your** `credentials.json` into the project root  
6. Make sure there is **no** `token.json` yet  
7. A browser opens → log into **your** Google account  
   - This creates **your personal** `token.json`  
   - From now on, events go to **your calendar**

> `credentials.json` and `token.json` are git-ignored and stay local.

---

## 4. Start MCP server

Terminal 1:

```bash
conda activate agent-env
python src/tools/mcp_server.py
```

MCP server runs on `http://127.0.0.1:5000/mcp`.

---

## 5. Run the agent

Terminal 2:

```bash
conda activate agent-env
python src/agent/run_agent.py
```

The agent will:

- Fetch issues from the configured GitHub repo  
- Use Gemini to break them into tasks with dependencies + durations  
- Schedule tasks in **08:00–12:00 and 14:00–17:00**, no overlaps, max 5 tasks  
- Create the corresponding events in **your Google Calendar**
