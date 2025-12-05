# Quick Start - Do This First! 🚀

## Status: Your code already meets minimum requirements! ✅

Your teacher said:
> "Achieving just this already guarantees a passing-level project"

You have:
- ✅ GitHub issue reading
- ✅ LLM task breakdown  
- ✅ Dependency scheduling
- ✅ Google Calendar integration

---

## Your Mission: VALIDATE IT WORKS

### Step 1: Setup (30 minutes)

#### 1.1 Create `.env` file
```bash
cp env.template .env
```

Edit `.env`:
```env
GOOGLE_API_KEY=your_actual_gemini_key_from_https://aistudio.google.com/app/apikey
GITHUB_TOKEN=your_actual_github_token_from_https://github.com/settings/tokens
```

#### 1.2 Get Google Calendar credentials
1. Go to https://console.cloud.google.com/
2. Create project → Enable Calendar API
3. Create OAuth Desktop credentials
4. Download as `credentials.json` → put in project root

See `SETUP_GUIDE.md` for detailed instructions.

---

### Step 2: Create Test Repository (20 minutes)

#### Option A: Create new repo
1. On GitHub: New repository → `your-username/agent-test-repo`
2. Create 3 issues (copy from `TEST_SCENARIOS.md`):
   - **Issue 1:** "Fix typo in README"
   - **Issue 2:** "Add dark mode toggle"
   - **Issue 3:** "Implement user authentication"

#### Option B: Use existing repo
- Keep using `BaHu-Git/Task_Manager` (already configured)

---

### Step 3: Run the Agent (10 minutes)

#### Terminal 1: Start server
```bash
conda activate agent-env
python src/tools/mcp_server.py
```

Wait for: `Uvicorn running on http://127.0.0.1:5000`

#### Terminal 2: Run agent
```bash
conda activate agent-env
python src/agent/run_agent.py
```

First run: Browser opens → Login to Google → Allow calendar access

---

### Step 4: Verify Results (5 minutes)

1. Open https://calendar.google.com
2. Look for scheduled tasks
3. Check times are in work hours (8-12, 14-17)
4. Take screenshots

---

### Step 5: Document (15 minutes)

Create `TEST_RESULTS.md`:
```markdown
# Test Results

## Date: [today's date]

## Test Run 1
- **Repository:** your-username/agent-test-repo
- **Issues processed:** 3
- **Tasks generated:** 8
- **Calendar events created:** 5 (max limit)
- **Status:** ✅ Success

## Screenshots
[Paste screenshots of calendar here]

## Issues Found
- None / [list any issues]

## Notes
[Any observations]
```

---

## ⚠️ If Something Breaks

### "GOOGLE_API_KEY is not set"
→ Check `.env` file exists and has your key

### "GitHub rate limit"
→ Make sure `GITHUB_TOKEN` is set in `.env`

### "Calendar API error"
→ Delete `token.json` and reauthorize

### Port 5000 in use
→ `lsof -ti:5000 | xargs kill -9`

See `SETUP_GUIDE.md` for more troubleshooting.

---

## What's Next?

After successful validation:

1. ✅ **Show results to your teacher** → get feedback
2. 📈 **Read `PROPOSAL_ALIGNMENT.md`** → decide on extensions
3. 🚀 **Plan Phase 2** → Jira integration

---

## File Guide

- `QUICK_START.md` ← **You are here! Start here!**
- `SETUP_GUIDE.md` - Detailed setup instructions
- `TEST_SCENARIOS.md` - Test cases to create
- `PROPOSAL_ALIGNMENT.md` - Proposal vs implementation analysis
- `BEST_PRACTICES.md` - Code quality tips
- `env.template` - Template for `.env` file

---

## Emergency Contacts

**Stuck?** Check these docs in order:
1. `SETUP_GUIDE.md` - Detailed setup
2. `BEST_PRACTICES.md` - Troubleshooting section
3. Teacher/teammates

---

## Time Estimate

- ⏱️ Setup: 30-45 minutes
- ⏱️ First successful run: 1 hour
- ⏱️ Full validation with tests: 2-3 hours
- ⏱️ Documentation: 1 hour

**Total: Half a day to have a working, tested, documented system!**

---

🎯 **Goal for This Week:** Get it running + document results + show teacher

Good luck! 🚀

