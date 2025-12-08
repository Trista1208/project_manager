# 🤖 AI-Powered DevOps Task Scheduler

An intelligent project management agent that uses AI to automatically break down GitHub/Jira issues into scheduled tasks.

## 🎯 What It Does

The agent automatically:

1. **📥 Fetches Issues** from GitHub (or Jira)
2. **🤖 Breaks Down Tasks** using AI (GitHub Models, Groq, DeepSeek)
3. **📊 Analyzes Dependencies** between tasks
4. **📅 Schedules Intelligently** into business hours (8-12, 14-17)
5. **📆 Creates Calendar Events** in Google Calendar (optional)
6. **💬 Sends Notifications** to Slack (optional)
7. **💾 Tracks History** and execution state

---

## 🚀 Quick Start

### 1. Environment Setup
```bash
git clone -b yu https://github.com/Meupi/Devops_and_LLMs.git
cd Devops_and_LLMs

conda env create -f environment.yml
conda activate agent-env
```

---

### 2. Create .env
Create a file .env in the project root using the env.template file.

--- 

### 3. Google Calendar Setup
Each developer does this once:

1. Go to Google Cloud Console
2. Create or select a project
3. Enable Google Calendar API
4. Go to APIs & Services → Credentials 
- Create OAuth client ID → Desktop app
- Download the `credentials.json`
5. In APIs & Services go to OAuth consent screen -> Audience
- Add your mail address to test users
6. Put your `credentials.json` into the project root
7. Make sure there is no `token.json` yet and run create_token.py
```bash
python src/core/create_token.py
```
8. A browser opens → log into your Google account
- This creates your personal `token.json`
- From now on, events go to your calendar

> `credentials.json` and `token.json` are git-ignored and stay local.

---

### 4. Start MCP Server

Terminal 1:

```bash
conda activate agent-env
python src/tools/mcp_server.py
```

MCP server runs on `http://127.0.0.1:5000/mcp`.

---

### 5. Run the agent

Terminal 2:

```bash
conda activate agent-env

# Simple: GitHub → Schedule
python src/agent/run_agent.py

# Multi-Agent: 3 AI models
python src/agent/multi_agent_runner.py

# Enhanced: + Jira + Slack + State
python src/agent/enhanced_agent.py
```

Test different orchestration strategies:
```bash
# 1. Single (default, cheapest)
LLM_STRATEGY=single python src/agent/multi_agent_runner.py

# 2. Specialized (recommended)
LLM_STRATEGY=specialized python src/agent/multi_agent_runner.py

# 3. Fallback (reliable)
LLM_STRATEGY=fallback python src/agent/multi_agent_runner.py

# 4. Ensemble (most accurate)
LLM_STRATEGY=ensemble python src/agent/multi_agent_runner.py
```

---

The agent will:

- Fetch issues from the GitHub repo and Jira  
- Use LLM to break them into tasks with dependencies + durations  
- Schedule tasks in **08:00–12:00 and 14:00–17:00**, no overlaps, max 5 tasks  
- Create the corresponding events in **your Google Calendar**, sends **Slack notifications** and updates **Jira issues**

---

### Verify Installation

```bash
# Quick check (no dependencies needed)
python check_setup.py

# Full verification (requires dependencies)
python verify_system.py
```
