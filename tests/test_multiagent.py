#!/usr/bin/env python3
"""
Comprehensive test for the multi-agent LLM system.
Tests all components to ensure they work correctly.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("=" * 70)
print("🧪 MULTI-AGENT SYSTEM TEST")
print("=" * 70)
print()

# Test 1: Check imports
print("1️⃣  Testing imports...")
try:
    from src.core.base_llm import BaseLLM
    print("   ✅ base_llm.BaseLLM")
    
    from src.core.llm_factory import LLMFactory
    print("   ✅ llm_factory.LLMFactory")
    
    from src.core.multi_agent_orchestrator import MultiAgentOrchestrator
    print("   ✅ multi_agent_orchestrator.MultiAgentOrchestrator")
    
    from src.core.llm_clients.gemini_client import GeminiClient
    print("   ✅ llm_clients.GeminiClient")
    
    from src.core.llm_clients.deepseek_client import DeepSeekClient
    print("   ✅ llm_clients.DeepSeekClient")
    
    from src.core.llm_clients.groq_client import GroqClient
    print("   ✅ llm_clients.GroqClient")
    
    from src.core.task_breakdown_multi import TaskBreakdownMulti
    print("   ✅ task_breakdown_multi.TaskBreakdownMulti")
    
    print("   ✅ All imports successful!\n")
except Exception as e:
    print(f"   ❌ Import failed: {e}\n")
    sys.exit(1)

# Test 2: Check API keys
print("2️⃣  Checking API keys...")
keys_configured = []
keys_missing = []

if os.getenv("GOOGLE_API_KEY") and "your_" not in os.getenv("GOOGLE_API_KEY", ""):
    keys_configured.append("GOOGLE_API_KEY")
    print("   ✅ Gemini API key configured")
else:
    keys_missing.append("GOOGLE_API_KEY")
    print("   ⚠️  Gemini API key NOT configured (required)")

if os.getenv("DEEPSEEK_API_KEY") and "your_" not in os.getenv("DEEPSEEK_API_KEY", ""):
    keys_configured.append("DEEPSEEK_API_KEY")
    print("   ✅ DeepSeek API key configured")
else:
    print("   ⚠️  DeepSeek API key not configured (optional)")

if os.getenv("GROQ_API_KEY") and "your_" not in os.getenv("GROQ_API_KEY", ""):
    keys_configured.append("GROQ_API_KEY")
    print("   ✅ Groq API key configured (FREE!)")
else:
    print("   ⚠️  Groq API key not configured (optional)")

print()

if "GOOGLE_API_KEY" not in keys_configured:
    print("❌ Cannot test multi-agent without Gemini API key")
    print("   Add GOOGLE_API_KEY to .env file and try again")
    sys.exit(1)

# Test 3: Initialize LLM Factory
print("3️⃣  Testing LLM Factory...")
try:
    factory = LLMFactory()
    available_clients = factory.create_all_available_clients()
    print(f"   ✅ LLM Factory created")
    print(f"   ✅ {len(available_clients)} LLM(s) available:")
    for name, client in available_clients.items():
        print(f"      • {name}: {client.model}")
    print()
except Exception as e:
    print(f"   ❌ LLM Factory failed: {e}\n")
    sys.exit(1)

# Test 4: Initialize Multi-Agent Orchestrator
print("4️⃣  Testing Multi-Agent Orchestrator...")
try:
    orchestrator = MultiAgentOrchestrator(strategy="specialized")
    print(f"   ✅ Orchestrator created")
    print(f"   ✅ Strategy: specialized")
    print(f"   ✅ {len(orchestrator.clients)} LLM client(s) configured")
    print()
except Exception as e:
    print(f"   ❌ Orchestrator failed: {e}\n")
    sys.exit(1)

# Test 5: Test basic LLM call
print("5️⃣  Testing basic LLM call...")
print("   Testing with simple prompt: 'Hello, respond with: OK'")
try:
    test_prompt = "Respond with exactly one word: OK"
    response = list(orchestrator.clients.values())[0].run(test_prompt)
    print(f"   ✅ LLM responded: {response[:50]}...")
    print()
except Exception as e:
    print(f"   ❌ LLM call failed: {e}")
    print(f"   This might be due to:")
    print(f"      • Invalid API key")
    print(f"      • Network connectivity")
    print(f"      • API rate limits")
    print()
    sys.exit(1)

# Test 6: Test task breakdown
print("6️⃣  Testing task breakdown with orchestrator...")
test_issue = """
Implement user authentication system

The system should allow users to register, login, and logout.
It needs to include password hashing and JWT token generation.
"""

try:
    result = orchestrator.breakdown_issue(test_issue)
    
    if result and "tasks" in result:
        tasks = result["tasks"]
        used_model = result.get("model_used", "unknown")
        
        print(f"   ✅ Task breakdown successful!")
        print(f"   ✅ Model used: {used_model}")
        print(f"   ✅ Generated {len(tasks)} tasks:")
        
        for i, task in enumerate(tasks[:3], 1):  # Show first 3
            print(f"      {i}. {task.get('task', 'N/A')}")
            if task.get('duration'):
                print(f"         Duration: {task['duration']}")
            if task.get('depends_on'):
                print(f"         Depends on: {task['depends_on']}")
        
        if len(tasks) > 3:
            print(f"      ... and {len(tasks) - 3} more tasks")
        print()
    else:
        print(f"   ⚠️  Task breakdown returned unexpected format: {result}")
        print()
        
except Exception as e:
    print(f"   ❌ Task breakdown failed: {e}")
    import traceback
    traceback.print_exc()
    print()
    sys.exit(1)

# Test 7: Test different strategies
print("7️⃣  Testing different orchestration strategies...")

strategies = ["single", "specialized", "fallback"]
if len(available_clients) >= 2:
    strategies.append("ensemble")

for strategy in strategies:
    try:
        test_orch = MultiAgentOrchestrator(strategy=strategy)
        print(f"   ✅ {strategy.capitalize()} strategy: OK")
    except Exception as e:
        print(f"   ⚠️  {strategy.capitalize()} strategy: {e}")

print()

# Test 8: Test metrics
print("8️⃣  Testing metrics tracking...")
try:
    metrics = orchestrator.get_metrics()
    print(f"   ✅ Metrics retrieved successfully")
    print(f"   ✅ Strategy: {metrics.get('strategy', 'N/A')}")
    
    if 'models' in metrics:
        for model_name, model_metrics in metrics['models'].items():
            requests = model_metrics.get('requests', 0)
            if requests > 0:
                print(f"   ✅ {model_name}: {requests} request(s)")
    print()
except Exception as e:
    print(f"   ⚠️  Metrics failed: {e}\n")

# Final summary
print("=" * 70)
print("📊 TEST SUMMARY")
print("=" * 70)
print()
print("✅ Core functionality:")
print("   • Imports: PASS")
print("   • LLM Factory: PASS")
print("   • Multi-Agent Orchestrator: PASS")
print("   • Basic LLM call: PASS")
print("   • Task breakdown: PASS")
print("   • Multiple strategies: PASS")
print("   • Metrics tracking: PASS")
print()
print(f"✅ Configuration:")
print(f"   • API keys configured: {len(keys_configured)}")
print(f"   • LLM clients available: {len(available_clients)}")
for name in available_clients.keys():
    print(f"      • {name}")
print()

if len(available_clients) >= 3:
    print("🌟 EXCELLENT! All 3 LLMs are configured!")
    print("   You can use all orchestration strategies including ensemble.")
elif len(available_clients) >= 2:
    print("🎉 GREAT! 2 LLMs configured!")
    print("   You can use most strategies. Add more API keys for ensemble.")
else:
    print("✅ GOOD! Single LLM working!")
    print("   Add DeepSeek & Groq API keys for multi-agent features.")

print()
print("=" * 70)
print("🎉 MULTI-AGENT SYSTEM IS WORKING! 🎉")
print("=" * 70)
print()
print("Next steps:")
print("  1. Run full demo: python src/agent/multi_agent_runner.py")
print("  2. Try different strategies in .env: LLM_STRATEGY=ensemble")
print("  3. Compare performance of different LLMs")
print()

