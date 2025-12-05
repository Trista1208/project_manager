#!/usr/bin/env python3
"""
Comprehensive system verification script.
Tests all components to ensure the agent can run properly.
"""
import os
import sys
from dotenv import load_dotenv

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def check_file_exists(filepath, required=True):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print_success(f"{filepath} exists")
        return True
    else:
        if required:
            print_error(f"{filepath} NOT FOUND (required)")
        else:
            print_warning(f"{filepath} not found (optional)")
        return False

def check_import(module_name, display_name=None):
    """Try to import a module."""
    if display_name is None:
        display_name = module_name
    
    try:
        __import__(module_name)
        print_success(f"{display_name}")
        return True
    except Exception as e:
        print_error(f"{display_name}: {e}")
        return False

def check_api_key(key_name, required=True):
    """Check if an API key is configured."""
    value = os.getenv(key_name)
    
    if value and value != f"your_{key_name.lower()}" and "your_" not in value:
        masked = f"{value[:10]}...{value[-4:]}" if len(value) > 14 else "***"
        print_success(f"{key_name}: {masked}")
        return True
    else:
        if required:
            print_error(f"{key_name} NOT configured (required)")
        else:
            print_warning(f"{key_name} not configured (optional)")
        return False

def main():
    print_header("🔍 SYSTEM VERIFICATION")
    
    all_passed = True
    
    # 1. Check Python version
    print_header("1️⃣ Python Version")
    python_version = sys.version_info
    if python_version >= (3, 8):
        print_success(f"Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print_error(f"Python {python_version.major}.{python_version.minor} (need >= 3.8)")
        all_passed = False
    
    # 2. Check required files
    print_header("2️⃣ Required Files")
    files_passed = True
    files_passed &= check_file_exists("environment.yml", required=True)
    files_passed &= check_file_exists("requirements.txt", required=True)
    files_passed &= check_file_exists(".env", required=True)
    files_passed &= check_file_exists("credentials.json", required=False)
    files_passed &= check_file_exists("src/core/llm.py", required=True)
    files_passed &= check_file_exists("src/core/scheduler.py", required=True)
    files_passed &= check_file_exists("src/tools/mcp_server.py", required=True)
    
    if not files_passed:
        all_passed = False
    
    # 3. Check Python dependencies
    print_header("3️⃣ Python Dependencies")
    deps_passed = True
    deps_passed &= check_import("openai", "openai")
    deps_passed &= check_import("dotenv", "python-dotenv")
    deps_passed &= check_import("jinja2", "jinja2")
    deps_passed &= check_import("requests", "requests")
    deps_passed &= check_import("google.auth", "google-auth")
    deps_passed &= check_import("googleapiclient", "google-api-python-client")
    deps_passed &= check_import("mcp", "mcp")
    
    if not deps_passed:
        print_warning("Some dependencies missing. Run: pip install -r requirements.txt")
        all_passed = False
    
    # 4. Check core modules
    print_header("4️⃣ Core Modules")
    modules_passed = True
    modules_passed &= check_import("src.core.llm", "LLM Client")
    modules_passed &= check_import("src.core.scheduler", "Scheduler")
    modules_passed &= check_import("src.core.task_breakdown", "Task Breakdown")
    modules_passed &= check_import("src.core.state_store", "State Store")
    
    if not modules_passed:
        all_passed = False
    
    # 5. Check multi-agent modules
    print_header("5️⃣ Multi-Agent System")
    multi_agent_passed = True
    multi_agent_passed &= check_import("src.core.base_llm", "Base LLM")
    multi_agent_passed &= check_import("src.core.llm_factory", "LLM Factory")
    multi_agent_passed &= check_import("src.core.multi_agent_orchestrator", "Multi-Agent Orchestrator")
    multi_agent_passed &= check_import("src.core.llm_clients.gemini_client", "Gemini Client")
    multi_agent_passed &= check_import("src.core.llm_clients.deepseek_client", "DeepSeek Client")
    multi_agent_passed &= check_import("src.core.llm_clients.groq_client", "Groq Client")
    
    if not multi_agent_passed:
        print_warning("Multi-agent system has issues, but basic agent should still work")
    
    # 6. Check tool modules
    print_header("6️⃣ Tool Integrations")
    tools_passed = True
    tools_passed &= check_import("src.tools.jira_client", "Jira Client")
    tools_passed &= check_import("src.tools.slack_client", "Slack Client")
    
    # 7. Check API configuration
    print_header("7️⃣ API Configuration")
    load_dotenv()
    
    # Required keys
    api_passed = True
    print("\n📌 Required (for basic agent):")
    api_passed &= check_api_key("GOOGLE_API_KEY", required=True)
    api_passed &= check_api_key("GITHUB_TOKEN", required=True)
    
    # Optional keys for multi-agent
    print("\n📌 Optional (for multi-agent system):")
    check_api_key("DEEPSEEK_API_KEY", required=False)
    check_api_key("GROQ_API_KEY", required=False)
    
    # Optional keys for enhanced features
    print("\n📌 Optional (for enhanced features):")
    check_api_key("JIRA_URL", required=False)
    check_api_key("SLACK_BOT_TOKEN", required=False)
    
    if not api_passed:
        all_passed = False
    
    # 8. Check agent runners
    print_header("8️⃣ Agent Runners")
    runners_passed = True
    runners_passed &= check_file_exists("src/agent/run_agent.py", required=True)
    runners_passed &= check_file_exists("src/agent/enhanced_agent.py", required=True)
    runners_passed &= check_file_exists("src/agent/multi_agent_runner.py", required=True)
    
    if not runners_passed:
        all_passed = False
    
    # Final summary
    print_header("📊 SUMMARY")
    
    if all_passed:
        print_success("ALL CHECKS PASSED! ✨")
        print(f"\n{GREEN}Your system is ready to run!{RESET}")
        print(f"\n{BLUE}Next steps:{RESET}")
        print("  1. Run MCP server: python src/tools/mcp_server.py")
        print("  2. Run agent: python src/agent/run_agent.py")
        print("  3. Or multi-agent: python src/agent/multi_agent_runner.py")
    else:
        print_error("SOME CHECKS FAILED")
        print(f"\n{YELLOW}Please fix the issues above before running the agent.{RESET}")
        print(f"\n{BLUE}Common fixes:{RESET}")
        print("  • Missing dependencies: pip install -r requirements.txt")
        print("  • Missing .env: ./CREATE_ENV.sh")
        print("  • Missing API keys: Edit .env file")
        print("  • Missing credentials.json: Get from Google Cloud Console")
        return 1
    
    print(f"\n{BLUE}{'='*70}{RESET}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

