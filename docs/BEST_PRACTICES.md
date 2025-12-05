# Best Practices & Tips

## Code Quality

### 1. Error Handling
Currently your code has minimal error handling. Consider adding:

```python
# In mcp_server.py: github_get_issues
try:
    resp = requests.get(...)
    resp.raise_for_status()
except requests.RequestException as e:
    return json.dumps({"error": f"Failed to fetch issues: {str(e)}"})
```

### 2. Configuration Management
Instead of hardcoding values:

```python
# Bad (current)
asyncio.run(run_agent("BaHu-Git/Task_Manager"))

# Good
REPO = os.getenv("GITHUB_REPO", "BaHu-Git/Task_Manager")
asyncio.run(run_agent(REPO))
```

Add to `.env`:
```env
GITHUB_REPO=your-username/your-test-repo
```

### 3. Logging
Replace `print()` with proper logging:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instead of print()
logger.info(f"Pulled {len(issues)} issues")
logger.error(f"Failed to schedule tasks: {e}")
```

### 4. Type Hints
You already use some type hints - continue this practice:

```python
def schedule(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Good! Already typed"""
```

---

## Security

### 1. Never Commit Secrets ✅
Your `.gitignore` is already correct:
- `.env` ✅
- `credentials.json` ✅
- `token.json` ✅

### 2. Validate API Tokens
Add checks:

```python
def __init__(self):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env")
    if not api_key.startswith("AI"):  # Gemini keys start with AI
        logger.warning("GOOGLE_API_KEY format looks incorrect")
```

### 3. Rate Limiting
GitHub has rate limits (60 requests/hour without token, 5000 with token):

```python
import time

def github_get_issues(repo: str, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        resp = requests.get(...)
        
        if resp.status_code == 403:  # Rate limited
            reset_time = int(resp.headers.get('X-RateLimit-Reset', 0))
            sleep_time = max(reset_time - time.time(), 60)
            logger.warning(f"Rate limited. Waiting {sleep_time}s...")
            time.sleep(sleep_time)
            continue
            
        resp.raise_for_status()
        return json.dumps(issues)
    
    raise Exception("Max retries exceeded")
```

---

## LLM Best Practices

### 1. Prompt Engineering
Your current prompt is good! Some tips:

**✅ Do:**
- Specify exact output format (JSON)
- Give examples
- Set constraints (duration ranges)
- Use clear, imperative language

**❌ Don't:**
- Ask for explanations (you only want JSON)
- Use ambiguous terms
- Forget to handle edge cases

### 2. Response Validation
Add more robust validation:

```python
def validate_task(task: Dict) -> bool:
    """Validate a single task object"""
    required_fields = ['task', 'duration', 'depends_on']
    
    if not all(field in task for field in required_fields):
        return False
    
    if not isinstance(task['duration'], (int, float)) or task['duration'] <= 0:
        return False
    
    if not isinstance(task['depends_on'], list):
        return False
    
    return True

def breakdown(self, issue_text: str):
    tasks = json.loads(cleaned)
    
    # Validate each task
    valid_tasks = [t for t in tasks if validate_task(t)]
    
    if len(valid_tasks) < len(tasks):
        logger.warning(f"Filtered {len(tasks) - len(valid_tasks)} invalid tasks")
    
    return valid_tasks
```

### 3. Cost Monitoring
Track LLM API usage:

```python
class LLMClient:
    def __init__(self):
        # ...
        self.total_requests = 0
        self.total_tokens = 0
    
    def run(self, prompt: str) -> str:
        response = self.client.chat.completions.create(...)
        
        self.total_requests += 1
        self.total_tokens += response.usage.total_tokens
        
        logger.info(f"LLM call: {response.usage.total_tokens} tokens")
        logger.info(f"Total: {self.total_requests} requests, {self.total_tokens} tokens")
        
        return response.choices[0].message.content
```

---

## Testing

### 1. Unit Tests
Create `tests/` directory:

```python
# tests/test_scheduler.py
import pytest
from datetime import datetime
from src.core.scheduler import Scheduler

def test_simple_schedule():
    scheduler = Scheduler(start_time=datetime(2025, 12, 6, 8, 0))
    
    tasks = [
        {"task": "Task A", "duration": 2, "depends_on": []}
    ]
    
    result = scheduler.schedule(tasks)
    
    assert len(result) == 1
    assert result[0]["task"] == "Task A"
    assert "start" in result[0]
    assert "end" in result[0]

def test_dependency_order():
    scheduler = Scheduler()
    
    tasks = [
        {"task": "Task B", "duration": 1, "depends_on": ["Task A"]},
        {"task": "Task A", "duration": 1, "depends_on": []}
    ]
    
    result = scheduler.schedule(tasks)
    
    # Task A should come before Task B
    assert result[0]["task"] == "Task A"
    assert result[1]["task"] == "Task B"

def test_max_five_tasks():
    scheduler = Scheduler()
    
    tasks = [{"task": f"Task {i}", "duration": 1, "depends_on": []} for i in range(10)]
    
    result = scheduler.schedule(tasks)
    
    assert len(result) == 5
```

Run tests:
```bash
conda activate agent-env
pip install pytest
pytest tests/
```

### 2. Integration Tests
Test end-to-end with mock data:

```python
# tests/test_integration.py
import json
from src.core.task_breakdown import TaskBreakdown

def test_breakdown_simple_issue():
    breaker = TaskBreakdown()
    
    issue = "Add login page with email and password fields"
    
    tasks = breaker.breakdown(issue)
    
    assert isinstance(tasks, list)
    assert len(tasks) > 0
    assert all("task" in t for t in tasks)
    assert all("duration" in t for t in tasks)
```

### 3. Mock External APIs
Don't call real APIs in tests:

```python
from unittest.mock import Mock, patch

def test_github_issues_success():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"title": "Test", "body": "Description"}
        ]
        mock_get.return_value = mock_response
        
        result = github_get_issues("test/repo")
        
        assert "Test" in result
```

---

## Documentation

### 1. Docstrings
Add detailed docstrings:

```python
def schedule(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Schedule tasks according to dependencies and work hours.
    
    Args:
        tasks: List of task dictionaries with keys:
            - task (str): Task description
            - duration (float): Duration in hours
            - depends_on (List[str]): List of task names this depends on
    
    Returns:
        List of tasks with added 'start' and 'end' ISO8601 timestamps.
        Limited to maximum 5 tasks.
    
    Raises:
        ValueError: If task duration is negative or task names are duplicated
    
    Example:
        >>> tasks = [
        ...     {"task": "Setup", "duration": 1, "depends_on": []},
        ...     {"task": "Build", "duration": 2, "depends_on": ["Setup"]}
        ... ]
        >>> scheduler.schedule(tasks)
        [
            {"task": "Setup", "duration": 1, "depends_on": [], 
             "start": "2025-12-06T08:00:00", "end": "2025-12-06T09:00:00"},
            ...
        ]
    """
```

### 2. Architecture Diagrams
Create visual documentation:

```
# Component Diagram
┌──────────────────────────────────────────────────┐
│                  run_agent.py                    │
│  (Orchestrates the entire workflow via MCP)      │
└────────────────────┬─────────────────────────────┘
                     │ MCP Client
                     ↓
┌──────────────────────────────────────────────────┐
│              mcp_server.py (MCP Server)          │
│  ┌────────────────────────────────────────────┐  │
│  │ Tool: github_get_issues()                  │  │
│  │ Tool: tasks_breakdown()                    │  │
│  │ Tool: tasks_schedule()                     │  │
│  │ Tool: calendar_create_event()              │  │
│  └────────────────────────────────────────────┘  │
└───┬─────────────┬──────────────┬────────────┬───┘
    │             │              │            │
    ↓             ↓              ↓            ↓
┌────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ GitHub │  │   LLM    │  │Scheduler │  │ Calendar │
│  API   │  │ (Gemini) │  │  Logic   │  │   API    │
└────────┘  └──────────┘  └──────────┘  └──────────┘
```

### 3. README Updates
Keep README updated with:
- Recent changes
- Known issues
- Troubleshooting tips
- Links to other docs

---

## Performance

### 1. Caching
Cache LLM responses for identical issues:

```python
import hashlib
import json
from pathlib import Path

class TaskBreakdown:
    def __init__(self):
        # ...
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
    
    def breakdown(self, issue_text: str):
        # Create cache key
        cache_key = hashlib.md5(issue_text.encode()).hexdigest()
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        # Check cache
        if cache_file.exists():
            logger.info("Using cached breakdown")
            return json.loads(cache_file.read_text())
        
        # Call LLM
        tasks = self._call_llm(issue_text)
        
        # Save to cache
        cache_file.write_text(json.dumps(tasks))
        
        return tasks
```

### 2. Parallel Processing
Process multiple issues in parallel:

```python
import asyncio

async def process_issue(session, issue):
    """Process a single issue"""
    # ... breakdown and schedule ...

async def run_agent(repo: str):
    async with streamablehttp_client(HOST) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            issues_result = await session.call_tool("github_get_issues", {"repo": repo})
            issues = json.loads(issues_result.content[0].text)
            
            # Process issues in parallel
            await asyncio.gather(*[
                process_issue(session, issue) 
                for issue in issues
            ])
```

---

## Git Workflow

### 1. Branch Strategy
```bash
# Feature branch
git checkout -b feature/jira-integration

# Make changes...

# Commit with meaningful messages
git add src/tools/jira_client.py
git commit -m "feat: Add Jira API client with issue fetching"

# Push and create PR
git push origin feature/jira-integration
```

### 2. Commit Messages
Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Adding tests
- `refactor:` Code restructuring
- `chore:` Maintenance

Examples:
```
feat: Add Jira integration with issue fetching
fix: Handle timezone conversion in scheduler
docs: Update setup guide with Jira configuration
test: Add unit tests for scheduler dependency logic
refactor: Extract calendar operations to separate class
```

### 3. Pre-commit Checks
Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.10
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=100]
```

Install:
```bash
pip install pre-commit
pre-commit install
```

---

## Presentation Tips

### 1. Demo Script
Prepare a step-by-step demo:

1. **Show test repository**
   - Display GitHub issues
   - Highlight different complexities

2. **Run the agent**
   - Start MCP server (already running)
   - Run agent with `python src/agent/run_agent.py`
   - Show terminal output

3. **Show results**
   - Open Google Calendar
   - Point out scheduled tasks
   - Highlight dependency ordering
   - Show time slots (8-12, 14-17)

4. **Explain architecture**
   - Show diagram
   - Walk through code flow
   - Highlight key components

5. **Discuss challenges**
   - LLM prompt engineering
   - Dependency resolution
   - Calendar scheduling logic

6. **Demo extensions** (if you've added them)
   - Jira integration
   - Slack notifications

### 2. Backup Plan
Have screenshots/video ready in case of:
- Network issues
- API rate limits
- OAuth token expiration

### 3. Questions to Prepare For
- Why did you choose Gemini over GPT?
- How do you handle circular dependencies?
- What happens if a task takes longer than scheduled?
- How would you scale this to a team?
- What are the limitations of your approach?

---

## Future Extensions Ideas

### 1. Task Status Tracking
- Check calendar events
- Mark GitHub/Jira issues as done
- Send completion notifications

### 2. Analytics Dashboard
- Track task completion rates
- Identify bottlenecks
- Team productivity metrics

### 3. Smart Rescheduling
- Detect calendar conflicts
- Automatically adjust schedules
- Handle priority changes

### 4. Natural Language Interface
- Slack bot: "Schedule issue PROJ-123"
- Query: "What am I working on today?"
- Update: "Reschedule task X to tomorrow"

### 5. Resource Allocation
- Assign tasks to team members
- Balance workload
- Consider skill sets

### 6. Integration Ecosystem
- GitLab support
- Azure DevOps
- Trello
- Asana
- Monday.com

---

## Common Pitfalls to Avoid

❌ **Don't:**
1. Try to implement everything at once
2. Ignore error handling
3. Hardcode configuration values
4. Skip testing until the end
5. Forget to document as you go
6. Commit sensitive data
7. Assume LLM responses are always valid JSON
8. Ignore rate limits
9. Over-engineer before validation
10. Work without backups

✅ **Do:**
1. Start with MVP and iterate
2. Handle errors gracefully
3. Use environment variables
4. Write tests alongside code
5. Document continuously
6. Use .gitignore properly
7. Validate and sanitize LLM output
8. Implement rate limiting
9. Validate before extending
10. Use version control effectively

---

## Resources

### Documentation
- [GitHub REST API](https://docs.github.com/en/rest)
- [Google Calendar API](https://developers.google.com/calendar/api/v3/reference)
- [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [Slack API](https://api.slack.com/)
- [MCP Protocol](https://modelcontextprotocol.io/)

### Python Libraries
- [requests](https://requests.readthedocs.io/)
- [google-api-python-client](https://github.com/googleapis/google-api-python-client)
- [PyGithub](https://pygithub.readthedocs.io/) (alternative to raw requests)
- [jira-python](https://jira.readthedocs.io/)
- [slack-sdk](https://slack.dev/python-slack-sdk/)

### Testing
- [pytest](https://docs.pytest.org/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [responses](https://github.com/getsentry/responses) (for mocking requests)

### Code Quality
- [black](https://black.readthedocs.io/) - Code formatter
- [flake8](https://flake8.pycqa.org/) - Linter
- [mypy](https://mypy.readthedocs.io/) - Type checker
- [pre-commit](https://pre-commit.com/) - Git hooks

---

## Checklist for Submission

### Code
- [ ] All code runs without errors
- [ ] Environment setup documented
- [ ] Configuration via .env (no hardcoded secrets)
- [ ] Error handling implemented
- [ ] Type hints used
- [ ] Docstrings for key functions

### Documentation
- [ ] README.md complete and up-to-date
- [ ] Setup guide (SETUP_GUIDE.md)
- [ ] Test scenarios defined (TEST_SCENARIOS.md)
- [ ] Architecture documented
- [ ] Known issues listed

### Testing
- [ ] Test repository created
- [ ] Test scenarios executed
- [ ] Results documented with screenshots
- [ ] Edge cases considered
- [ ] Demo prepared and rehearsed

### Git
- [ ] .gitignore properly configured
- [ ] No secrets committed
- [ ] Meaningful commit messages
- [ ] Clean git history

### Presentation
- [ ] Demo script prepared
- [ ] Architecture diagram ready
- [ ] Backup screenshots/video
- [ ] Q&A preparation
- [ ] Time management (practice!)

---

Good luck with your project! 🚀



