#!/usr/bin/env python3
"""
Simple setup checker that works without external dependencies.
"""
import os
import sys

def check_files():
    """Check if required files exist."""
    print("📁 Checking files...")
    files = {
        ".env": "required",
        "environment.yml": "required",
        "requirements.txt": "required",
        "credentials.json": "optional",
        "src/core/llm.py": "required",
        "src/core/scheduler.py": "required",
        "src/tools/mcp_server.py": "required",
    }
    
    all_required_exist = True
    for filepath, status in files.items():
        exists = os.path.exists(filepath)
        symbol = "✅" if exists else ("❌" if status == "required" else "⚠️")
        print(f"  {symbol} {filepath} ({status})")
        if status == "required" and not exists:
            all_required_exist = False
    
    return all_required_exist

def check_env_vars():
    """Check .env file for API keys."""
    print("\n🔑 Checking API keys in .env...")
    
    if not os.path.exists(".env"):
        print("  ❌ .env file not found")
        print("  → Run: ./CREATE_ENV.sh")
        return False
    
    with open(".env", "r") as f:
        content = f.read()
    
    keys_to_check = {
        "GOOGLE_API_KEY": "required",
        "GITHUB_TOKEN": "required",
        "DEEPSEEK_API_KEY": "optional",
        "GROQ_API_KEY": "optional",
    }
    
    all_required_configured = True
    for key, status in keys_to_check.items():
        if key in content and "your_" not in content.split(key)[1].split("\n")[0]:
            # Key exists and doesn't contain placeholder
            print(f"  ✅ {key} ({status})")
        else:
            if status == "required":
                print(f"  ❌ {key} ({status}) - NOT configured")
                all_required_configured = False
            else:
                print(f"  ⚠️  {key} ({status}) - not configured")
    
    return all_required_configured

def check_structure():
    """Check project structure."""
    print("\n📦 Checking project structure...")
    
    dirs = [
        "src/core",
        "src/agent",
        "src/tools",
        "src/templates",
        "src/core/llm_clients",
        "docs",
    ]
    
    all_exist = True
    for dirname in dirs:
        exists = os.path.isdir(dirname)
        symbol = "✅" if exists else "❌"
        print(f"  {symbol} {dirname}/")
        if not exists:
            all_exist = False
    
    return all_exist

def main():
    print("=" * 70)
    print("🔍 SETUP CHECK")
    print("=" * 70)
    print()
    
    files_ok = check_files()
    env_ok = check_env_vars()
    structure_ok = check_structure()
    
    print()
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    if files_ok and env_ok and structure_ok:
        print("\n✅ Basic setup looks good!")
        print("\n📝 Next steps:")
        print("  1. Create conda environment:")
        print("     conda env create -f environment.yml")
        print("     conda activate agent-env")
        print()
        print("  2. Install dependencies:")
        print("     pip install -r requirements.txt")
        print()
        print("  3. Test the system:")
        print("     python verify_system.py")
        print()
        print("  4. Run the agent:")
        print("     python src/agent/run_agent.py")
    else:
        print("\n❌ Some issues found. Please fix them:")
        if not files_ok:
            print("  • Missing required files")
        if not env_ok:
            print("  • API keys not configured - Edit .env file")
        if not structure_ok:
            print("  • Project structure incomplete")
        print()
        print("  Run ./CREATE_ENV.sh to create .env template")
    
    print()
    print("=" * 70)
    
    return 0 if (files_ok and env_ok and structure_ok) else 1

if __name__ == "__main__":
    sys.exit(main())

