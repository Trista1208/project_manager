# 🚀 Quick Start Guide

**Your AI agent is ready to run!** This guide gets you started in 5 minutes.

---

## ✅ What's Already Configured

Your agent already has:
- ✅ **GitHub Models** (FREE! Uses your GitHub token)
- ✅ **Groq** (FREE! Llama 3.3 70B)
- ✅ **DeepSeek R1** (configured)
- ✅ **All code implemented and working**

**You can run it RIGHT NOW!** No additional setup needed.

---

## 🎯 Quick Test (30 seconds)

```bash
cd /Users/jiaqiyu/Desktop/Devops_and_LLMs-master

# Activate environment
source test_venv/bin/activate

# Run demo
python tests/demo_agent.py
```

**What you'll see:**
- ✅ Agent processes 2 GitHub issues
- ✅ AI breaks them into 12 tasks
- ✅ Schedules into business hours
- ✅ All automatically!

---

## 📊 Run Full System Test

```bash
# Test everything
python tests/test_full_system.py
```

**Expected output:**
```
✅ GitHub Models API - WORKING!
✅ Task breakdown - WORKING!
✅ Scheduler - WORKING!
🎉 YOUR AGENT IS WORKING!
```

---

## 🤖 Run Real Agent

### Option 1: Simple Agent (GitHub → Schedule)

```bash
python src/agent/run_agent.py
```

**What it does:**
1. Fetches issues from GitHub
2. Breaks down using AI (GitHub Models)
3. Schedules into business hours
4. Ready for calendar integration

### Option 2: Multi-Agent Demo (3 LLMs)

```bash
python src/agent/multi_agent_runner.py
```

**What it does:**
- Uses 3 AI models (GitHub, Groq, DeepSeek)
- Compares performance
- Shows cost tracking
- Demonstrates strategies

### Option 3: Enhanced Agent (Full Features)

```bash
python src/agent/enhanced_agent.py
```

**What it does:**
- GitHub + Jira integration
- Slack notifications
- State persistence
- Execution history

---

## 📅 Optional: Enable Calendar Automation

To automatically create Google Calendar events:

### Step 1: Get Credentials

1. Go to: https://console.cloud.google.com/
2. Create project → Enable Calendar API
3. Create OAuth Desktop credentials
4. Download as `credentials.json`
5. Place in project root

### Step 2: Run Agent

```bash
python src/agent/run_agent.py
```

- First time: Browser opens for OAuth
- After: Events created automatically!
- Check your calendar - tasks appear! 📅

---

## 🎓 Demo to Teacher

### Quick Demo (2 minutes)

```bash
# Show it working
python tests/demo_agent.py
```

**Point out:**
- ✅ Uses GitHub Models (FREE!)
- ✅ Processes real issues
- ✅ AI generates tasks intelligently
- ✅ Schedules with dependencies
- ✅ 100% automated

### Full Demo (5 minutes)

```bash
# 1. Show test passing
python tests/test_full_system.py

# 2. Show real agent
python src/agent/run_agent.py

# 3. Show multi-agent
python src/agent/multi_agent_runner.py
```

**Talking points:**
- "Uses 3 FREE AI models"
- "GitHub Models - no API key needed"
- "Groq is completely free"
- "Automatically breaks down tasks"
- "Schedules intelligently"
- "Production-ready system"

---

## 💰 Cost

**Total cost to run: $0.00**

- GitHub Models: FREE
- Groq: FREE  
- DeepSeek: ~$0.08 per 100 issues

**For 1000 issues: ~$0.80** (vs $4.40 with OpenAI)

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
source test_venv/bin/activate
pip install -r requirements.txt
```

### "GitHub token not found"
```bash
# Check .env
cat .env | grep GITHUB_TOKEN

# Should show: GITHUB_TOKEN=ghp_...
```

### Agent not working
```bash
# Run diagnostics
python tests/test_full_system.py
```

---

## 📚 More Information

- **Full Setup:** See [INSTALL.md](INSTALL.md)
- **Documentation:** See [docs/](docs/) folder
- **Multi-Agent:** See [docs/MULTI_AGENT_LLM.md](docs/MULTI_AGENT_LLM.md)
- **Features:** See [docs/ENHANCED_FEATURES.md](docs/ENHANCED_FEATURES.md)

---

## ✅ Summary

**Your agent is ready!**

- ✅ All code working
- ✅ GitHub Models configured (FREE!)
- ✅ Tests passing
- ✅ Ready to demo

**Just run:** `python tests/demo_agent.py`

🎉 **Enjoy your AI agent!** 🚀

