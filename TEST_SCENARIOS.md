# Test Scenarios for Task Scheduling Agent

## Purpose
This document defines test scenarios to evaluate the agent's performance across different complexity levels.

## Test Repository Setup

1. **Fork or create a test repository** (e.g., `your-username/agent-test-repo`)
2. **Create the following issues** in your test repo
3. **Run the agent** and document results

---

## Scenario 1: Simple Single-Task Issue
**Title:** Fix typo in README  
**Description:**
```
There's a typo in the README.md file on line 23.
Change "recieve" to "receive".
```

**Expected Outcome:**
- 1 task generated
- Duration: ~0.5 hours
- No dependencies
- Scheduled in next available work slot

---

## Scenario 2: Small Feature (2-3 Tasks)
**Title:** Add dark mode toggle to settings page  
**Description:**
```
Users want to switch between light and dark themes.

Requirements:
- Add a toggle button in the settings page
- Store preference in localStorage
- Apply theme across all pages
```

**Expected Outcome:**
- 2-3 tasks generated
- Total duration: 2-4 hours
- Dependencies: toggle UI → state management → apply theme
- Scheduled sequentially based on dependencies

---

## Scenario 3: Medium Feature (4-5 Tasks)
**Title:** Implement user authentication system  
**Description:**
```
Add basic user authentication with:
- Login page with email/password
- Registration page
- Password hashing (bcrypt)
- JWT token generation
- Protected routes middleware
- Logout functionality
```

**Expected Outcome:**
- 4-5 tasks generated
- Total duration: 6-10 hours
- Multiple dependency chains
- Should hit or approach the 5-task limit
- Scheduled across multiple work blocks (morning/afternoon)

---

## Scenario 4: Complex Multi-Component Feature
**Title:** Build notification system  
**Description:**
```
Create a comprehensive notification system:

Backend:
- Database schema for notifications
- API endpoints (GET, POST, PATCH for marking read)
- Real-time updates via WebSocket

Frontend:
- Notification bell icon in navbar
- Dropdown list with unread count
- Mark as read functionality
- Toast notifications for new items

Must support:
- Different notification types (info, warning, error)
- Pagination for old notifications
```

**Expected Outcome:**
- Should generate >5 tasks
- Agent should limit to 5 most critical tasks
- Duration: 10-15+ hours
- Complex dependency graph
- Demonstrates scheduler's handling of large issues

---

## Scenario 5: Vague/Unclear Requirements
**Title:** Improve performance  
**Description:**
```
The app feels slow. Make it faster.
```

**Expected Outcome:**
- Test LLM's ability to handle ambiguous requirements
- Should generate reasonable analysis tasks:
  - Profile application performance
  - Identify bottlenecks
  - Implement optimization
- Or should break down into concrete investigation steps

---

## Scenario 6: Bug Fix with Investigation
**Title:** User cannot upload files larger than 1MB  
**Description:**
```
Steps to reproduce:
1. Navigate to /upload
2. Select a file > 1MB
3. Click upload
4. Error: "Request entity too large"

Environment:
- Browser: Chrome 120
- OS: macOS
- Backend: Node.js + Express
```

**Expected Outcome:**
- Investigation + fix tasks
- Tasks like:
  - Check nginx/server upload limits
  - Update Express body-parser config
  - Test with various file sizes
  - Update documentation

---

## Evaluation Criteria

For each scenario, document:

### ✅ Task Breakdown Quality
- Are tasks specific and actionable?
- Are durations realistic?
- Are dependencies identified correctly?

### ✅ Scheduling Quality
- Are tasks scheduled in dependency order?
- Do tasks fit within work hours (8-12, 14-17)?
- No overlapping events?
- Proper multi-day scheduling if needed?

### ✅ Calendar Integration
- Events created successfully in Google Calendar?
- Correct start/end times?
- Readable event summaries?

### ✅ Edge Cases
- How does the system handle >5 tasks?
- How does it handle unclear requirements?
- How does it handle dependencies on non-existent tasks?

---

## Results Template

```markdown
## Test Run: [Date]

### Scenario 1: [Title]
- **Tasks Generated:** [number]
- **Total Duration:** [hours]
- **Scheduling:** [success/issues]
- **Calendar Events:** [created/failed]
- **Notes:** [observations]
- **Screenshot:** [link or embedded]

[Repeat for each scenario]
```

---

## How to Run Tests

1. **Setup environment:**
   ```bash
   conda activate agent-env
   ```

2. **Start MCP server (Terminal 1):**
   ```bash
   python src/tools/mcp_server.py
   ```

3. **Update run_agent.py with your test repo:**
   ```python
   asyncio.run(run_agent("your-username/agent-test-repo"))
   ```

4. **Run agent (Terminal 2):**
   ```bash
   python src/agent/run_agent.py
   ```

5. **Document results and check Google Calendar**

6. **Clear calendar before next test** (or use date offsets)

---

## Next Steps

After validating these scenarios:
1. Document any bugs or unexpected behavior
2. Refine prompts or scheduling logic as needed
3. Consider adding automated tests
4. Prepare demo for presentation


