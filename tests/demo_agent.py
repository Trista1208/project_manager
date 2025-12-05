#!/usr/bin/env python3
"""
Simple demo of the agent working without MCP server.
Direct demonstration of task breakdown and scheduling.
"""
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("=" * 70)
print("🚀 REAL AGENT DEMO - DIRECT TEST")
print("=" * 70)
print()

# Import components
print("📦 Loading agent components...")
try:
    from src.core.llm import LLMClient
    from src.core.task_breakdown import TaskBreakdown
    from src.core.scheduler import Scheduler
    print("✅ All components loaded")
except Exception as e:
    print(f"❌ Failed to load components: {e}")
    sys.exit(1)

print()

# Simulate a real GitHub issue
print("📥 Simulating GitHub issue fetch...")
print()

test_issues = [
    {
        "number": 42,
        "title": "Implement user authentication system",
        "body": """
We need to add user authentication to the application.

Requirements:
- User registration with email validation
- Login with JWT tokens
- Password hashing with bcrypt
- Session management
- Logout functionality

This is critical for our MVP launch next week.
"""
    },
    {
        "number": 43,
        "title": "Create admin dashboard",
        "body": """
Build an admin dashboard for managing users and content.

Features needed:
- User management (view, edit, delete)
- Content moderation tools
- Analytics overview
- System health monitoring

Should be responsive and work on tablets.
"""
    }
]

print(f"✅ Found {len(test_issues)} issues")
print()

# Process each issue
for issue in test_issues:
    print("=" * 70)
    print(f"📋 ISSUE #{issue['number']}: {issue['title']}")
    print("=" * 70)
    print()
    
    issue_text = f"{issue['title']}\n\n{issue['body']}"
    
    # Step 1: Break down into tasks
    print("🤖 Step 1: AI Task Breakdown...")
    print(f"   Using: GitHub Models (FREE!)")
    print()
    
    try:
        breaker = TaskBreakdown()
        tasks = breaker.breakdown(issue_text)
        
        print(f"✅ Generated {len(tasks)} tasks:")
        print()
        
        for i, task in enumerate(tasks, 1):
            print(f"   {i}. {task['task']}")
            print(f"      ⏱️  Duration: {task.get('duration', 'N/A')} hours")
            if task.get('depends_on'):
                deps = ', '.join(task['depends_on']) if isinstance(task['depends_on'], list) else task['depends_on']
                print(f"      🔗 Depends on: {deps}")
            print()
        
    except Exception as e:
        print(f"❌ Task breakdown failed: {e}")
        import traceback
        traceback.print_exc()
        continue
    
    # Step 2: Schedule tasks
    print("📅 Step 2: Scheduling tasks...")
    print()
    
    try:
        scheduler = Scheduler()
        schedule = scheduler.schedule(tasks)
        
        print(f"✅ Created {len(schedule)} time blocks:")
        print()
        
        for i, block in enumerate(schedule, 1):
            start = block['start']
            end = block['end']
            print(f"   {i}. {block['task']}")
            print(f"      📅 {start} → {end}")
            print()
        
    except Exception as e:
        print(f"❌ Scheduling failed: {e}")
        import traceback
        traceback.print_exc()
        continue
    
    print("✅ Issue processed successfully!")
    print()

# Summary
print("=" * 70)
print("🎉 DEMO COMPLETE!")
print("=" * 70)
print()
print("✅ What the agent did:")
print("   1. Fetched issues from repository (simulated)")
print("   2. Used AI (GitHub Models) to break down into tasks")
print("   3. Analyzed dependencies between tasks")
print("   4. Scheduled tasks into business hours")
print("   5. Created time blocks respecting dependencies")
print()
print("💡 Next step:")
print("   Add Google Calendar credentials to automatically")
print("   create calendar events for all scheduled tasks!")
print()
print("=" * 70)

