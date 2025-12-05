# 📦 Installation Guide

## Quick Install (5 minutes)

### Option 1: Using Conda (Recommended)

```bash
# 1. Clone repository
git clone -b yu https://github.com/Meupi/Devops_and_LLMs.git
cd Devops_and_LLMs

# 2. Create environment
conda env create -f environment.yml
conda activate agent-env

# 3. Install Python packages
pip install -r requirements.txt

# 4. Configure API keys
./CREATE_ENV.sh
nano .env  # Add your GOOGLE_API_KEY

# 5. Verify setup
python check_setup.py

# 6. Run the agent
python src/agent/run_agent.py
```

### Option 2: Using venv

```bash
# 1. Clone repository
git clone -b yu https://github.com/Meupi/Devops_and_LLMs.git
cd Devops_and_LLMs

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
./CREATE_ENV.sh
nano .env  # Add your GOOGLE_API_KEY

# 5. Verify setup
python check_setup.py

# 6. Run the agent
python src/agent/run_agent.py
```

---

## Detailed Setup

### Step 1: Prerequisites

- **Python 3.8+** (Python 3.10+ recommended)
- **Git**
- **Conda** (optional but recommended) or **pip**

### Step 2: Get API Keys

#### Required (for basic functionality):

1. **Google Gemini API Key** (FREE)
   - Go to: https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key (starts with `AIza...`)

2. **GitHub Personal Access Token**
   - Already configured: `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`
   - Or create new: https://github.com/settings/tokens
   - Scopes needed: `repo`, `read:org`

#### Optional (for multi-agent system):

3. **DeepSeek API Key** (Already configured!)
   - `sk-fa5b4fc2bd7749a7855a42880dbb914a`

4. **Groq API Key** (Already configured, FREE!)
   - `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`

#### Optional (for enhanced features):

5. **Google Calendar credentials.json**
   - Go to: https://console.cloud.google.com/
   - Create project → Enable Calendar API
   - Create OAuth Desktop credentials
   - Download as `credentials.json` → place in project root

6. **Jira** (if using Jira integration)
   - `JIRA_URL`: Your Atlassian domain
   - `JIRA_EMAIL`: Your email
   - `JIRA_API_TOKEN`: From account settings

7. **Slack** (if using Slack notifications)
   - `SLACK_BOT_TOKEN`: Bot token from Slack app
   - `SLACK_CHANNEL`: Channel name (e.g., `#project-updates`)

### Step 3: Configure Environment

```bash
# Create .env file
./CREATE_ENV.sh

# Edit .env and add your Gemini API key
nano .env
```

Your `.env` should look like:

```env
# Required
GOOGLE_API_KEY=AIza...  # ← Add your key here
GITHUB_TOKEN=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  # ✅ Configured

# Optional (multi-agent)
DEEPSEEK_API_KEY=sk-fa5b4fc2bd7749a7855a42880dbb914a  # ✅ Configured
GROQ_API_KEY=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  # ✅ Configured
LLM_STRATEGY=specialized

# Optional (enhanced features)
# JIRA_URL=https://your-domain.atlassian.net
# JIRA_EMAIL=your-email@example.com
# JIRA_API_TOKEN=your_token
# SLACK_BOT_TOKEN=xoxb-your-token
# SLACK_CHANNEL=#project-updates
```

### Step 4: Verify Installation

```bash
# Quick check (no dependencies needed)
python check_setup.py

# Full verification (requires dependencies)
python verify_system.py
```

Expected output:

```
✅ All core imports successful!
✅ GOOGLE_API_KEY configured
✅ GITHUB_TOKEN configured
✅ 3/3 LLM clients available
```

---

## Running the Agent

### Option A: Simple Agent (GitHub → Calendar)

```bash
# Terminal 1: Start MCP server
python src/tools/mcp_server.py

# Terminal 2: Run agent
python src/agent/run_agent.py
```

### Option B: Enhanced Agent (with Jira/Slack/State)

```bash
# Terminal 1: Start MCP server
python src/tools/mcp_server.py

# Terminal 2: Run enhanced agent
python src/agent/enhanced_agent.py
```

### Option C: Multi-Agent Demo (3 LLMs comparison)

```bash
# Terminal 1: Start MCP server
python src/tools/mcp_server.py

# Terminal 2: Run multi-agent
python src/agent/multi_agent_runner.py
```

---

## Troubleshooting

### "No module named 'dotenv'"

```bash
# Install dependencies
pip install -r requirements.txt
```

### "GOOGLE_API_KEY is not set"

```bash
# Edit .env and add your Gemini API key
nano .env
```

### "conda: command not found"

```bash
# Use venv instead
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "Port 5000 already in use"

```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or change port in src/tools/mcp_server.py
```

### "ModuleNotFoundError: No module named 'openai'"

```bash
# Activate environment first
conda activate agent-env  # or: source venv/bin/activate
pip install -r requirements.txt
```

### "Multi-agent system not available"

This is OK! The basic agent will work with just Gemini. To enable multi-agent:
- Add `DEEPSEEK_API_KEY` and `GROQ_API_KEY` to `.env`
- Both keys are already configured in your `.env` template!

---

## File Structure After Installation

```
Devops_and_LLMs/
├── .env                   # ✅ Your API keys (created)
├── .venv/ or agent-env/   # ✅ Virtual environment (created)
├── credentials.json       # ⚠️  Optional (for Google Calendar)
├── token.json             # ⚠️  Auto-created on first Calendar use
├── state/                 # Auto-created (stores execution history)
├── environment.yml        # Conda environment spec
├── requirements.txt       # Python dependencies
└── src/                   # Source code (ready to run!)
```

---

## Next Steps

After installation:

1. **Test the setup:**
   ```bash
   python check_setup.py
   ```

2. **Run a simple test:**
   ```bash
   python src/agent/run_agent.py
   ```

3. **Read the documentation:**
   - [START_HERE.md](docs/START_HERE.md) - Project overview
   - [MULTI_AGENT_LLM.md](docs/MULTI_AGENT_LLM.md) - Multi-agent system
   - [TEST_SCENARIOS.md](docs/TEST_SCENARIOS.md) - Test cases

4. **Explore features:**
   - Multi-agent comparison
   - Jira integration
   - Slack notifications
   - State persistence

---

## Quick Reference

**Check setup:**
```bash
python check_setup.py
```

**Run agent:**
```bash
python src/agent/run_agent.py
```

**Run multi-agent:**
```bash
python src/agent/multi_agent_runner.py
```

**View docs:**
```bash
ls docs/
```

---

## Getting Help

**Common issues:**
- Check [README.md](README.md) troubleshooting section
- Run `python check_setup.py` to diagnose
- Check `.env` file has all required keys

**Documentation:**
- [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) - Detailed setup
- [docs/BEST_PRACTICES.md](docs/BEST_PRACTICES.md) - Tips and tricks

---

**You're ready to go! 🚀**

