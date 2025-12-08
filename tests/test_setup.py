#!/usr/bin/env python
"""
Quick test to check your configuration status.
Run this to see what's configured and what's missing.
"""
import os
from dotenv import load_dotenv

# Try to load .env
load_dotenv()

print("=" * 70)
print("🔍 CONFIGURATION CHECK")
print("=" * 70)
print()

# Check each required key
keys_to_check = {
    "GOOGLE_API_KEY": {
        "name": "Google Gemini",
        "required": True,
        "get_at": "https://aistudio.google.com/app/apikey"
    },
    "GITHUB_TOKEN": {
        "name": "GitHub",
        "required": True,
        "get_at": "https://github.com/settings/tokens"
    },
    "DEEPSEEK_API_KEY": {
        "name": "DeepSeek R1",
        "required": False,
        "get_at": "https://platform.deepseek.com/api_keys"
    },
    "GROQ_API_KEY": {
        "name": "Groq (FREE)",
        "required": False,
        "get_at": "https://console.groq.com/keys"
    }
}

configured_count = 0
missing_required = []
missing_optional = []

for key, info in keys_to_check.items():
    value = os.getenv(key)
    
    if value and value != f"your_{key.lower()}":
        print(f"✅ {info['name']}: Configured")
        print(f"   Key: {value[:10]}...{value[-4:]}")
        configured_count += 1
    else:
        status = "❌" if info["required"] else "⚠️"
        print(f"{status} {info['name']}: NOT configured")
        print(f"   Get from: {info['get_at']}")
        
        if info["required"]:
            missing_required.append(info['name'])
        else:
            missing_optional.append(info['name'])
    
    print()

# Summary
print("=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print(f"✅ Configured: {configured_count}/4 API keys")
print()

if missing_required:
    print("❌ REQUIRED (system won't work without these):")
    for name in missing_required:
        print(f"   - {name}")
    print()

if missing_optional:
    print("⚠️  OPTIONAL (nice to have for multi-agent):")
    for name in missing_optional:
        print(f"   - {name}")
    print()

# Instructions
print("=" * 70)
print("📝 NEXT STEPS")
print("=" * 70)
print()

if not os.path.exists(".env"):
    print("🔧 No .env file found!")
    print()
    print("Run this to create .env with your configured keys:")
    print("   ./CREATE_ENV.sh")
    print()
    print("Then add your Gemini API key to .env")
    print()
elif missing_required:
    print("🔧 Missing required keys!")
    print()
    print("Edit .env and add:")
    for name in missing_required:
        print(f"   - {name}")
    print()
else:
    print("🎉 All required keys configured!")
    print()
    print("You can now run:")
    print("   python src/tools/mcp_server.py      # Terminal 1")
    print("   python src/agent/multi_agent_runner.py  # Terminal 2")
    print()
    
    if missing_optional:
        print("💡 To enable all 3 LLMs, also add:")
        for name in missing_optional:
            print(f"   - {name}")

print("=" * 70)

