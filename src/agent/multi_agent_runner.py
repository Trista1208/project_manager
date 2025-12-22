# src/agent/multi_agent_runner.py
"""
Enhanced agent runner using multi-agent LLM orchestrator.
Demonstrates comparison between single and multi-agent approaches.
"""
import asyncio
import json
import os
from typing import Optional

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

HOST = "http://127.0.0.1:5000/mcp"


async def run_multi_agent_demo(
    repo: str,
    compare_with_single: bool = True
):
    """
    Run the agent using multi-agent LLM system.
    
    Args:
        repo: GitHub repository (owner/repo)
        compare_with_single: If True, also run single-LLM for comparison
    """
    print("=" * 70)
    print("🤖 MULTI-AGENT LLM TASK BREAKDOWN DEMO")
    print("=" * 70)
    print()
    
    async with streamablehttp_client(HOST) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # Fetch issues from GitHub
            print(f"📥 Fetching issues from: {repo}")
            issues_result = await session.call_tool(
                "github_get_issues",
                {"repo": repo}
            )
            issues_json = issues_result.content[0].text
            issues = json.loads(issues_json)
            print(f"✅ Found {len(issues)} issues\n")
            
            if not issues:
                print("❌ No issues found!")
                return
            
            # Process first issue with both methods
            issue = issues[0]
            issue_text = f"{issue['title']}\n{issue['body']}"
            
            print("=" * 70)
            print(f"📋 ISSUE: {issue['title']}")
            print("=" * 70)
            print()
            
            # === MULTI-AGENT BREAKDOWN ===
            print("🤖 METHOD 1: Multi-Agent LLM System")
            print("-" * 70)
            
            try:
                multi_result = await session.call_tool(
                    "tasks_breakdown_multi",
                    {"issue_text": issue_text}
                )
                multi_tasks = json.loads(multi_result.content[0].text)
                
                if isinstance(multi_tasks, dict) and "error" in multi_tasks:
                    print(f"⚠️  Multi-agent error: {multi_tasks['error']}")
                    if "fallback" in multi_tasks:
                        print(f"   {multi_tasks['fallback']}")
                else:
                    print(f"✅ Generated {len(multi_tasks)} tasks")
                    for i, task in enumerate(multi_tasks, 1):
                        print(f"   {i}. {task['task']}")
                        print(f"      Duration: {task.get('duration', 'N/A')}h")
                        if task.get('depends_on'):
                            print(f"      Depends on: {', '.join(task['depends_on'])}")
            except Exception as e:
                print(f"❌ Multi-agent failed: {e}")
            
            print()
            
            # === SINGLE LLM BREAKDOWN (for comparison) ===
            if compare_with_single:
                print("🔹 METHOD 2: Single LLM (Gemini)")
                print("-" * 70)
                
                try:
                    single_result = await session.call_tool(
                        "tasks_breakdown",
                        {"issue_text": issue_text}
                    )
                    single_tasks = json.loads(single_result.content[0].text)
                    
                    print(f"✅ Generated {len(single_tasks)} tasks")
                    for i, task in enumerate(single_tasks, 1):
                        print(f"   {i}. {task['task']}")
                        print(f"      Duration: {task.get('duration', 'N/A')}h")
                except Exception as e:
                    print(f"❌ Single LLM failed: {e}")
                
                print()
            
            # === GET METRICS ===
            print("=" * 70)
            print("📊 PERFORMANCE METRICS")
            print("=" * 70)
            
            try:
                metrics_result = await session.call_tool("llm_get_metrics", {})
                metrics = json.loads(metrics_result.content[0].text)
                
                if isinstance(metrics, dict) and "error" not in metrics:
                    print(f"Strategy: {metrics.get('strategy', 'N/A')}\n")
                    
                    for llm_metrics in metrics.get("llms", []):
                        print(f"🤖 {llm_metrics['provider']} ({llm_metrics['model']})")
                        print(f"   Requests: {llm_metrics['total_requests']}")
                        print(f"   Success Rate: {llm_metrics['success_rate']}")
                        print(f"   Total Cost: {llm_metrics['total_cost']}")
                        print(f"   Avg Latency: {llm_metrics['avg_latency_ms']}")
                        print()
                else:
                    print(f"⚠️  {metrics.get('error', 'Metrics not available')}")
            except Exception as e:
                print(f"⚠️  Could not fetch metrics: {e}")
            
            print("=" * 70)
            print("✅ Demo completed!")
            print("=" * 70)


if __name__ == "__main__":
    # Configuration
    GITHUB_REPO = os.getenv("GITHUB_REPO", "BaHu-Git/Task_Manager")
    COMPARE_MODE = os.getenv("COMPARE_LLMS", "true").lower() == "true"
    
    print(f"\n🔧 Configuration:")
    print(f"   Repository: {GITHUB_REPO}")
    print(f"   Strategy: {os.getenv('LLM_STRATEGY', 'specialized')}")
    print(f"   Compare with single LLM: {COMPARE_MODE}")
    print()
    
    asyncio.run(run_multi_agent_demo(
        repo=GITHUB_REPO,
        compare_with_single=COMPARE_MODE
    ))


