# Complete Setup Guide

## Prerequisites
- Conda or Miniconda installed
- GitHub account
- Google account

---

## Step 1: Environment Setup

### 1.1 Create Conda Environment
```bash
conda env create -f environment.yml
conda activate agent-env
```

---

## Step 2: API Keys Configuration

### 2.1 Get Google Gemini API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### 2.2 Get GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scope: `repo` (Full control of private repositories)
4. Generate and copy the token

### 2.3 Create .env File

```bash
cp .env.example .env
```

Edit `.env` and add your keys:
```env
GOOGLE_API_KEY=your_actual_gemini_key
GITHUB_TOKEN=your_actual_github_token
```

---

## Step 3: Google Calendar Setup

### 3.1 Enable Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Navigate to **APIs & Services → Library**
4. Search for "Google Calendar API"
5. Click **Enable**

### 3.2 Create OAuth Credentials

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth client ID**
3. If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: "Task Scheduler Agent"
   - Your email
   - Save and continue through all steps
4. Back to credentials:
   - Application type: **Desktop app**
   - Name: "Task Agent"
5. Click **Create**
6. **Download JSON** → save as `credentials.json` in project root

### 3.3 First-Time OAuth Flow

The first time you run the agent:
1. A browser window will open
2. Log in with your Google account
3. Click "Allow" to grant calendar access
4. A `token.json` file will be created automatically
5. Future runs will use this token (no browser needed)

---

## Step 4: Create Test Repository

### 4.1 Fork or Create Test Repo

Option A: Fork an existing repo
```bash
# On GitHub, fork: https://github.com/BaHu-Git/Task_Manager
```

Option B: Create new test repo
1. Create repo on GitHub: `your-username/agent-test-repo`
2. Clone it locally
3. Add test issues (see TEST_SCENARIOS.md)

### 4.2 Add Test Issues

Go to your repo on GitHub → Issues → New Issue

Create issues from `TEST_SCENARIOS.md` (at least Scenarios 1-3)

---

## Step 5: Configure Agent

Edit `src/agent/run_agent.py` line 61:
```python
asyncio.run(run_agent("your-username/your-test-repo"))
```

---

## Step 6: Run the Agent

### Terminal 1: Start MCP Server
```bash
conda activate agent-env
python src/tools/mcp_server.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:5000
```

### Terminal 2: Run Agent
```bash
conda activate agent-env
python src/agent/run_agent.py
```

Expected output:
```
Pulled 3 issues
ISSUE: Fix typo in README
Raw tasks_json: [{"task": "...", "duration": 0.5, "depends_on": []}]
Parsed 1 tasks
Scheduled 1 tasks
Scheduling event: Fix typo in README.md 2025-12-06T08:00:00 → 2025-12-06T08:30:00
Created event: Fix typo in README.md
...
```

---

## Step 7: Verify in Google Calendar

1. Open Google Calendar: https://calendar.google.com
2. Check for new events created by the agent
3. Verify times are correct (08:00-12:00, 14:00-17:00)

---

## Troubleshooting

### "GOOGLE_API_KEY is not set"
- Check `.env` file exists in project root
- Check no extra spaces around `=`
- Make sure you activated conda environment

### "Failed to fetch GitHub issues"
- Verify `GITHUB_TOKEN` in `.env`
- Check token has `repo` scope
- Make sure repo name format is `owner/repo`

### "Unable to read credentials.json"
- Make sure `credentials.json` is in project root
- Re-download from Google Cloud Console if needed

### "Calendar API error"
- Delete `token.json` and reauthorize
- Check Google Calendar API is enabled
- Verify OAuth consent screen is configured

### Port 5000 already in use
- Check if another process is using port 5000
- Kill the process: `lsof -ti:5000 | xargs kill -9`
- Or change port in `mcp_server.py`

---

## Project Structure

```
Devops_and_LLMs/
├── .env                    # API keys (git-ignored)
├── credentials.json        # Google OAuth (git-ignored)
├── token.json             # Auto-generated (git-ignored)
├── environment.yml        # Conda dependencies
├── README.md              # Main documentation
├── SETUP_GUIDE.md         # This file
├── TEST_SCENARIOS.md      # Test cases
└── src/
    ├── agent/
    │   └── run_agent.py   # Main agent orchestrator
    ├── core/
    │   ├── llm.py         # Gemini LLM client
    │   ├── task_breakdown.py  # Issue → tasks
    │   └── scheduler.py   # Task → calendar slots
    ├── templates/
    │   └── breakdown_prompt.j2  # LLM prompt template
    └── tools/
        └── mcp_server.py  # MCP tool server
```

---

## Next Steps

1. ✅ Complete this setup
2. ✅ Run test scenarios (see TEST_SCENARIOS.md)
3. ✅ Document results
4. 📈 Plan extensions (Jira, Slack, etc.)
5. 🎓 Prepare presentation/demo


