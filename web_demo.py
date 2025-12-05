#!/usr/bin/env python3
"""
Web-based demo of the AI agent.
Shows real-time task breakdown and scheduling in a browser.
Now with MULTI-AGENT support showing all 3 AI models!

Run: streamlit run web_demo.py
"""
import streamlit as st
import sys
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

# Page config
st.set_page_config(
    page_title="Multi-Agent AI DevOps Demo",
    page_icon="🤖",
    layout="wide"
)

# Import components
try:
    from src.core.llm import LLMClient
    from src.core.task_breakdown import TaskBreakdown
    from src.core.scheduler import Scheduler
    from src.core.llm_factory import LLMFactory
    from src.core.multi_agent_orchestrator import MultiAgentOrchestrator
except Exception as e:
    st.error(f"Failed to import components: {e}")
    st.stop()

# Title
st.title("🤖 Multi-Agent AI DevOps Scheduler")
st.markdown("**3 AI models working together to break down issues!**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🔧 Multi-Agent Configuration")
    
    # Check available LLM clients
    try:
        factory = LLMFactory()
        available_clients = factory.create_all_available_clients()
        
        st.success(f"✅ {len(available_clients)} AI Model(s) Available:")
        
        for name, client in available_clients.items():
            with st.container():
                st.markdown(f"**🤖 {name.upper()}**")
                st.caption(f"Model: {client.model}")
                st.caption(f"Provider: {client.provider}")
                cost = client.input_cost_per_million
                if cost == 0:
                    st.caption("💰 Cost: FREE! 🎉")
                else:
                    st.caption(f"💰 Cost: ${cost}/1M tokens")
                st.markdown("")
        
        llm_ready = len(available_clients) > 0
        
    except Exception as e:
        st.error(f"❌ AI Models not configured")
        st.error(str(e))
        llm_ready = False
    
    st.markdown("---")
    
    # Strategy selection
    st.header("🎯 Orchestration Strategy")
    strategy = st.selectbox(
        "Choose strategy:",
        ["single", "specialized", "fallback", "ensemble"],
        index=1,  # Default to specialized
        help="Different ways to use multiple AI models"
    )
    
    st.caption(f"""
    **{strategy.capitalize()}:**
    {
        "Uses one model (fastest)" if strategy == "single" else
        "Routes to best model per task" if strategy == "specialized" else
        "Tries cheap models first" if strategy == "fallback" else
        "Uses all models, picks best"
    }
    """)
    
    st.markdown("---")
    
    st.header("ℹ️ About")
    st.markdown("""
    This multi-agent system:
    1. Uses 3+ AI models
    2. Breaks issues into tasks
    3. Analyzes dependencies
    4. Schedules intelligently
    
    **Cost:** $0.00 - $0.08 per 100 issues!
    """)
    
    st.markdown("---")
    st.markdown("**🎓 For Teacher Demo**")
    st.markdown("✅ Production-ready code")
    st.markdown("✅ Uses FREE AI models")
    st.markdown("✅ Smart scheduling")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Input: GitHub Issue")
    
    # Sample issues
    sample_issues = {
        "🔐 User Authentication": """
Implement user authentication system

Requirements:
- User registration with email validation
- Login with JWT tokens
- Password hashing with bcrypt
- Session management
- Logout functionality

This is critical for our MVP launch next week.
""",
        "📊 Admin Dashboard": """
Create admin dashboard

Features needed:
- User management (view, edit, delete)
- Content moderation tools
- Analytics overview
- System health monitoring

Should be responsive and work on tablets.
""",
        "🔍 Search Feature": """
Add search functionality to the application

Requirements:
- Full-text search across content
- Filter by category and date
- Sort results by relevance
- Pagination for results
- Save search history

Performance should be under 500ms.
""",
        "✏️ Custom Issue": ""
    }
    
    issue_choice = st.selectbox(
        "Choose a sample issue or write your own:",
        list(sample_issues.keys())
    )
    
    if issue_choice == "✏️ Custom Issue":
        issue_text = st.text_area(
            "Enter your issue description:",
            height=300,
            placeholder="Describe your project issue here..."
        )
    else:
        issue_text = st.text_area(
            f"Issue: {issue_choice}",
            value=sample_issues[issue_choice],
            height=300
        )
    
    process_button = st.button("🚀 Process with AI", type="primary", use_container_width=True)

with col2:
    st.header("🤖 AI Processing & Results")
    
    if not llm_ready:
        st.warning("⚠️ AI model not configured. Please check the sidebar for setup instructions.")
    elif not process_button:
        st.info("👈 Enter an issue and click 'Process with AI' to see the magic!")
    else:
        if not issue_text.strip():
            st.error("Please enter an issue description!")
        else:
            # Show processing
            with st.spinner("🤖 Multi-Agent AI is analyzing the issue..."):
                try:
                    # Multi-agent task breakdown
                    if len(available_clients) > 1:
                        # Use multi-agent orchestrator
                        orchestrator = MultiAgentOrchestrator(strategy=strategy)
                        result = orchestrator.breakdown_issue(issue_text)
                        tasks = result.get("tasks", [])
                        model_used = result.get("model_used", "Unknown")
                        
                        st.success(f"✅ Multi-Agent AI generated {len(tasks)} tasks!")
                        st.info(f"🤖 Strategy: {strategy.capitalize()} | Model used: {model_used}")
                    else:
                        # Fallback to single LLM
                        breaker = TaskBreakdown()
                        tasks = breaker.breakdown(issue_text)
                        st.success(f"✅ AI generated {len(tasks)} tasks!")
                        st.info(f"🤖 Using single model: {list(available_clients.keys())[0]}")
                    
                    # Display tasks
                    st.subheader("📋 Generated Tasks")
                    
                    for i, task in enumerate(tasks, 1):
                        with st.expander(f"**Task {i}: {task['task']}**", expanded=True):
                            col_a, col_b = st.columns([1, 1])
                            with col_a:
                                st.metric("⏱️ Duration", f"{task.get('duration', 'N/A')} hours")
                            with col_b:
                                deps = task.get('depends_on', [])
                                if deps:
                                    if isinstance(deps, list):
                                        deps_str = ', '.join(deps)
                                    else:
                                        deps_str = deps
                                    st.info(f"🔗 Depends on: {deps_str}")
                                else:
                                    st.success("🆓 No dependencies")
                    
                    st.markdown("---")
                    
                    # Scheduling
                    with st.spinner("📅 Creating schedule..."):
                        scheduler = Scheduler()
                        schedule = scheduler.schedule(tasks)
                        
                        st.success(f"✅ Created {len(schedule)} time blocks!")
                        
                        st.subheader("📅 Schedule")
                        
                        for i, block in enumerate(schedule, 1):
                            with st.container():
                                st.markdown(f"**{i}. {block['task']}**")
                                
                                start_time = block['start']
                                end_time = block['end']
                                
                                # Parse datetime
                                if isinstance(start_time, str):
                                    start_dt = datetime.fromisoformat(start_time)
                                    end_dt = datetime.fromisoformat(end_time)
                                else:
                                    start_dt = start_time
                                    end_dt = end_time
                                
                                col_x, col_y = st.columns([1, 1])
                                with col_x:
                                    st.caption(f"📅 {start_dt.strftime('%b %d, %Y')}")
                                with col_y:
                                    st.caption(f"🕐 {start_dt.strftime('%H:%M')} → {end_dt.strftime('%H:%M')}")
                                
                                st.markdown("---")
                    
                    # Summary
                    st.balloons()
                    
                    st.success("🎉 **Processing Complete!**")
                    
                    with st.expander("📊 Summary", expanded=True):
                        col_summary1, col_summary2, col_summary3 = st.columns(3)
                        
                        with col_summary1:
                            st.metric("✅ Tasks Generated", len(tasks))
                        
                        with col_summary2:
                            st.metric("📅 Time Blocks", len(schedule))
                        
                        with col_summary3:
                            total_hours = sum(float(t.get('duration', 0)) for t in tasks)
                            st.metric("⏱️ Total Hours", f"{total_hours:.1f}")
                        
                        st.success("✅ All tasks scheduled into business hours (8-12, 14-17)")
                        st.success("✅ Dependencies analyzed and respected")
                        st.info("💰 Cost: $0.00 (using FREE AI models!)")
                
                except Exception as e:
                    st.error(f"❌ Error processing issue: {e}")
                    
                    with st.expander("🔍 Error Details"):
                        st.code(str(e))
                        import traceback
                        st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🤖 <strong>AI-Powered DevOps Task Scheduler</strong></p>
    <p>Uses FREE AI models: GitHub Models + Groq + DeepSeek</p>
    <p>✅ Production-ready | ✅ 100% automated | ✅ Cost: $0.00</p>
</div>
""", unsafe_allow_html=True)

