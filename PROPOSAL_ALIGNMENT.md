# Project Proposal vs Implementation Alignment

## Summary
Your **current implementation meets the minimum requirements** for a passing project according to your teacher. However, your **proposal is significantly more ambitious** than what's currently built.

---

## Feature Comparison Matrix

| Feature | Proposal | Current Code | Priority | Effort |
|---------|----------|--------------|----------|--------|
| **GitHub Integration** | ✅ | ✅ | CORE | Done |
| **Google Calendar** | ✅ | ✅ | CORE | Done |
| **Task Breakdown (LLM)** | ✅ | ✅ | CORE | Done |
| **Dependency Scheduling** | ✅ | ✅ | CORE | Done |
| **Jira Integration** | ✅ | ❌ | HIGH | 2-3 days |
| **Slack Notifications** | ✅ | ❌ | MEDIUM | 1-2 days |
| **Multi-user Workload** | ✅ | ❌ | LOW | 3-5 days |
| **Project State Store** | ✅ | ❌ | LOW | 2-3 days |
| **Rescheduling Logic** | ✅ | ❌ | MEDIUM | 2-3 days |
| **Agent Orchestrator** | ✅ | ❌ | LOW | 3-4 days |

---

## Current Implementation (What You Have) ✅

### Architecture
```
GitHub API → TaskBreakdown (LLM) → Scheduler → Google Calendar
              ↓
         Jinja Template
```

### Components
1. **GitHub Integration** (`mcp_server.py:github_get_issues`)
   - Fetches issues via REST API
   - Filters out PRs
   - Returns title + body

2. **Task Breakdown** (`task_breakdown.py`)
   - Uses Jinja2 template
   - Calls Gemini 2.5 Flash via OpenAI-compatible API
   - Parses JSON response with task, duration, depends_on

3. **Scheduler** (`scheduler.py`)
   - Topological sort for dependencies
   - Business hours: 8-12, 14-17
   - Max 5 tasks per run
   - No overlaps

4. **Calendar Integration** (`mcp_server.py:calendar_create_event`)
   - OAuth2 with Google Calendar API
   - Creates events with ISO8601 timestamps
   - Timezone: Europe/Zurich

5. **MCP Architecture**
   - Server: FastMCP on port 5000
   - Client: Async MCP client
   - Tools: github_get_issues, tasks_breakdown, tasks_schedule, calendar_create_event

### Strengths
- ✅ Clean separation of concerns
- ✅ Uses modern MCP protocol
- ✅ LLM-driven task generation
- ✅ Respects dependencies
- ✅ Professional scheduling logic

### Limitations
- ❌ No persistence (state lost between runs)
- ❌ No error recovery
- ❌ Single-user only
- ❌ One-time scheduling (no updates/deletes)
- ❌ Hardcoded timezone
- ❌ No Jira or Slack integration

---

## Proposed Architecture (From Your Proposal) 🎯

### Components Described in Proposal

1. **Integration Layer**
   - GitHub (PR, commits) ← Partially done (only issues)
   - Jira (issues, status, priorities) ← Missing
   - Calendar (events, availability) ← Partially done (only create)
   - Slack (notifications) ← Missing

2. **Project State Store** ← Missing entirely
   - Current tasks
   - PR statuses
   - Team priorities
   - Workload per person
   - Calendar availability
   - Deadlines

3. **LLM Layer**
   - Context Builder ← Missing (no context management)
   - Decision Engine ← Partially done (only task breakdown)

4. **Agent Orchestrator** ← Missing
   - Event-driven activation
   - Priority management
   - Reassignment logic
   - Calendar constraint handling

5. **Action Executor** ← Partially done
   - Update Jira ← Missing
   - Comment on GitHub ← Missing
   - Send Slack messages ← Missing
   - Schedule calendar blocks ← Done (create only)
   - Create new issues ← Missing

---

## Recommended Phased Approach 🚀

### Phase 1: VALIDATE CURRENT SYSTEM (1 week) 🔥 PRIORITY
**Status:** This is what you should do FIRST!

**Goals:**
- ✅ Prove current implementation works
- ✅ Create test scenarios
- ✅ Document results
- ✅ Get teacher feedback

**Tasks:**
1. Create test repository with 5-6 sample issues (see TEST_SCENARIOS.md)
2. Setup .env, credentials.json (see SETUP_GUIDE.md)
3. Run system end-to-end
4. Document results with screenshots
5. Identify bugs and fix them

**Deliverables:**
- Working demo
- Test results document
- Screenshots of calendar
- Video recording of agent running

**This phase alone = PASSING GRADE** ✅

---

### Phase 2: ADD JIRA INTEGRATION (1-2 weeks)
**Goal:** Unify GitHub + Jira as task sources

**Why Jira:**
- Teacher specifically recommended it
- Jira is heavily used in industry
- Similar API to GitHub (REST)
- Adds meaningful complexity

**Implementation:**
1. Add Jira credentials to .env:
   ```env
   JIRA_URL=https://your-domain.atlassian.net
   JIRA_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your_jira_token
   ```

2. Create new MCP tool:
   ```python
   @MCP.tool()
   def jira_get_issues(project_key: str) -> str:
       """Fetch issues from Jira project"""
   ```

3. Unified task model:
   ```python
   {
       "source": "github" | "jira",
       "id": "PROJ-123" | "issue-456",
       "title": "...",
       "body": "...",
       "priority": "high" | "medium" | "low",
       "assignee": "..."
   }
   ```

4. Update agent to handle both sources:
   ```python
   # Fetch from both
   github_issues = await session.call_tool("github_get_issues", ...)
   jira_issues = await session.call_tool("jira_get_issues", ...)
   
   # Merge and process
   all_issues = github_issues + jira_issues
   ```

**Resources:**
- Jira REST API: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- Python: `requests` library (you already have it)

**Deliverables:**
- Jira integration working
- Updated test scenarios
- Demo with mixed GitHub + Jira issues

**This phase = GOOD GRADE** 📈

---

### Phase 3: ADD SLACK NOTIFICATIONS (1 week)
**Goal:** Send notifications when tasks are scheduled

**Implementation:**
1. Create Slack bot: https://api.slack.com/apps
2. Get bot token
3. Add to .env:
   ```env
   SLACK_BOT_TOKEN=xoxb-your-token
   SLACK_CHANNEL=#project-updates
   ```

4. Add MCP tool:
   ```python
   @MCP.tool()
   def slack_send_message(channel: str, text: str) -> str:
       """Send Slack notification"""
   ```

5. Notify after scheduling:
   ```python
   message = f"Scheduled {len(schedule)} tasks:\n"
   for t in schedule:
       message += f"• {t['task']} ({t['start']} - {t['end']})\n"
   
   await session.call_tool("slack_send_message", {
       "channel": "#team",
       "text": message
   })
   ```

**Deliverables:**
- Slack notifications working
- Rich message formatting
- Screenshots of notifications

**This phase = VERY GOOD GRADE** 🎓

---

### Phase 4: ADVANCED FEATURES (Optional)
**Only if you have extra time!**

**Possible extensions:**
1. **Task Status Updates**
   - Agent checks calendar and marks tasks complete in GitHub/Jira
   - Updates based on time elapsed

2. **Rescheduling Logic**
   - Detect conflicts in calendar
   - Automatically reschedule tasks
   - Handle priority changes

3. **Multi-user Support**
   - Assign tasks to different people
   - Balance workload across team
   - Multiple calendars

4. **Project State Persistence**
   - SQLite or JSON file storage
   - Track task history
   - Analytics dashboard

---

## Revised Proposal Outline

### Suggested Proposal Structure

**1. Introduction**
- Current version (keep it)
- But emphasize "phased approach"

**2. Objectives**
- Phase 1 (Minimum Viable): GitHub → LLM → Calendar ✅
- Phase 2 (Extension): Add Jira integration 📈
- Phase 3 (Advanced): Add Slack + rescheduling 🚀

**3. Architecture**

**Phase 1 Architecture (Current):**
```
┌─────────┐
│ GitHub  │
└────┬────┘
     │
     v
┌──────────────┐
│ LLM Breakdown│
│  (Gemini)    │
└──────┬───────┘
       │
       v
┌──────────────┐
│  Scheduler   │
│ (8-12,14-17) │
└──────┬───────┘
       │
       v
┌──────────────┐
│   Calendar   │
└──────────────┘
```

**Phase 2 Architecture (With Jira):**
```
┌─────────┐  ┌──────┐
│ GitHub  │  │ Jira │
└────┬────┘  └───┬──┘
     │           │
     └─────┬─────┘
           v
    ┌──────────────┐
    │ Task Unifier │
    └──────┬───────┘
           │
           v
    ┌──────────────┐
    │ LLM Breakdown│
    └──────┬───────┘
           │
          ...
```

**Phase 3 Architecture (Full System):**
```
┌─────────┐  ┌──────┐
│ GitHub  │  │ Jira │
└────┬────┘  └───┬──┘
     │           │
     └─────┬─────┘
           v
    ┌──────────────┐
    │    State     │
    │    Store     │
    └──────┬───────┘
           │
           v
    ┌──────────────┐
    │ LLM Decision │
    └──────┬───────┘
           │
     ┌─────┴─────┐
     v           v
┌─────────┐ ┌───────┐
│Calendar │ │ Slack │
└─────────┘ └───────┘
```

**4. Implementation Timeline**
- Week 1-2: Phase 1 validation + testing
- Week 3-4: Phase 2 Jira integration
- Week 5-6: Phase 3 Slack notifications
- Week 7+: Extensions (if time permits)

**5. Expected Outcomes**
- Phase 1: Automated task scheduling from GitHub ✅
- Phase 2: Unified DevOps workflow (GitHub + Jira) 📈
- Phase 3: Team collaboration with Slack 🚀

---

## Critical Next Steps (Priority Order)

### 🔥 URGENT (Do This Week!)
1. ✅ Create `.env` file with your API keys
2. ✅ Setup Google Calendar OAuth (`credentials.json`)
3. ✅ Create test repository with sample issues
4. ✅ Run system end-to-end and verify it works
5. ✅ Take screenshots/video for documentation

### 📋 IMPORTANT (Next Week)
6. Document test results
7. Present current system to teacher for feedback
8. Decide on Phase 2 scope based on feedback

### 📈 FUTURE (After Validation)
9. Start Jira integration
10. Update proposal to reflect phased approach
11. Plan final presentation/demo

---

## Key Takeaways

✅ **Your current implementation is good enough for a passing grade!**

✅ **Your proposal is more ambitious than necessary** - consider scaling it down or making it explicitly phased.

✅ **Focus on validation first** - prove what you have works before adding complexity.

✅ **Jira + Slack are natural extensions** - add them incrementally after Phase 1.

❌ **Don't try to build everything at once** - you'll run out of time and have nothing working.

---

## Teacher's Exact Words (Reminder)

> "A concrete early milestone example could be:
> - The Agent reads issues from a GitHub repo,
> - Breaks them down into smaller tasks,
> - Estimates dependencies,
> - Then populates Google Calendar with task events scheduled according to dependency order and estimated duration.
> 
> **Achieving just this already guarantees a passing-level project**, and you can extend from there, for example with Jira or Slack, to increase complexity."

**You've already achieved this! 🎉 Now validate it with tests!**

