# ▶️ RUN ME - Complete Instructions

## ✅ Your Configuration Status

**GOOD NEWS:** Your `.env` file is created with all your keys!

```
✅ DeepSeek R1: sk-fa5b4fc2bd7749a7855a42880dbb914a
✅ Groq (FREE): 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
✅ GitHub: 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
⚠️ Gemini: Needs to be added
```

---

## 🚀 **Complete Setup (2 minutes)**

### **Step 1: Activate Environment**

```bash
cd /Users/jiaqiyu/Desktop/Devops_and_LLMs-master

# Activate conda environment
conda activate agent-env
```

### **Step 2: Add Your Gemini Key**

You mentioned you have the Gemini key from the initial code. 

**Edit `.env` and replace line 6:**
```bash
# Open .env in your editor
nano .env
# or
code .env
# or
vim .env
```

**Replace:**
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

**With your actual Gemini key** (starts with `AIza...`)

**If you don't have it yet:**
- Get FREE key at: https://aistudio.google.com/app/apikey (takes 2 minutes)

---

## ▶️ **RUN YOUR MULTI-AGENT SYSTEM**

### **Terminal 1: Start MCP Server**

```bash
conda activate agent-env
python src/tools/mcp_server.py
```

**You should see:**
```
🤖 Initializing multi-agent system with strategy: specialized
✅ Gemini client configured: gemini-2.0-flash-exp
✅ DeepSeek client configured: deepseek-reasoner
✅ Groq client configured: llama-3.3-70b-versatile (FREE!)
🎯 Multi-agent orchestrator created:
   Strategy: specialized
   LLMs: 3 configured

INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:5000
```

**If you see error about Gemini:**
```
ValueError: GOOGLE_API_KEY is not set in .env or environment
```
→ **This means you need to add your Gemini key to `.env` file!**

### **Terminal 2: Run Multi-Agent Demo**

```bash
conda activate agent-env
python src/agent/multi_agent_runner.py
```

**You'll see:**
```
🤖 MULTI-AGENT LLM TASK BREAKDOWN DEMO
============================================================

📥 Fetching issues from: BaHu-Git/Task_Manager
✅ Found 3 issues

🎯 Processing: [Issue Title]

🤖 METHOD 1: Multi-Agent LLM System
------------------------------------------------------------
🤖 Used: Google Gemini (gemini-2.0-flash-exp)
💰 Cost: $0.000123 | ⏱️ Latency: 1234ms
✅ Generated 5 tasks

📊 PERFORMANCE METRICS
Strategy: specialized

🤖 Google Gemini (gemini-2.0-flash-exp)
   Requests: 1
   Success Rate: 100.00%
   Total Cost: $0.0001

🤖 DeepSeek R1 (deepseek-reasoner)
   Requests: 0

🤖 Groq (FREE) (llama-3.3-70b-versatile)
   Requests: 0
   Total Cost: $0.0000 (FREE!)

✅ Demo completed!
```

---

## 🎯 **What the Initial Code Does**

When you run the agent **without a valid Gemini key**, you'll get this error:

```
ValueError: GOOGLE_API_KEY is not set in .env or environment
```

**This error message tells you exactly what's missing!**

That's what your teacher meant - run the code, see the error, then add the key!

---

## ✅ **Your Current Status**

### **What you have:**
```
.env file created ✅
├── DeepSeek key ✅
├── Groq key ✅
├── GitHub token ✅
└── Gemini key ⚠️ (placeholder - needs your actual key)
```

### **What happens when you run:**
1. **With placeholder key:** Error message guides you to add real key
2. **With real key:** System runs perfectly with 3 AI models!

---

## 📝 **Quick Actions**

### **Action 1: Test Current Setup**
```bash
conda activate agent-env
python src/tools/mcp_server.py
```

**Expected:** Error about GOOGLE_API_KEY (this is good! It tells you what to add)

### **Action 2: Add Gemini Key**
```bash
# Edit .env, add your Gemini key on line 6
nano .env
```

### **Action 3: Run Again**
```bash
python src/tools/mcp_server.py
```

**Expected:** All 3 LLMs configured successfully! ✅

---

## 💡 **Understanding the Error Message**

The code in `src/core/llm.py` line 14-15 checks for the key:

```python
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in .env or environment")
```

**This error is helpful!** It tells you:
- ❌ What's missing
- 📝 What to do (add GOOGLE_API_KEY to .env)
- 🔧 How to fix it

---

## 🎉 **Your System is Ready!**

### **All configured:**
- ✅ DeepSeek R1 (advanced reasoning)
- ✅ Groq Llama 3.3 (FREE, ultra-fast)
- ✅ GitHub (fetch issues)

### **Just needs:**
- ⚠️ Gemini API key (you mentioned having it)

### **Then you can:**
- 🚀 Run multi-agent system
- 📊 Compare 3 AI models
- 💰 Save 80% on costs (Groq is FREE!)
- 🎓 Demo to teacher

---

## 🔑 **Add Your Gemini Key**

**Edit `.env` line 6 with your actual Gemini key:**
```bash
# From:
GOOGLE_API_KEY=your_gemini_api_key_here

# To:
GOOGLE_API_KEY=AIza... (your actual key)
```

**If you need to get it:**
https://aistudio.google.com/app/apikey (free, 2 minutes)

---

## ✅ **Verification**

After adding Gemini key, run:
```bash
conda activate agent-env
python test_setup.py
```

Should show: ✅ 4/4 keys configured!

Then run:
```bash
python src/tools/mcp_server.py
```

Should show: 3 LLMs configured successfully!

---

**You're one Gemini key away from running your multi-agent AI system!** 🎉🚀

