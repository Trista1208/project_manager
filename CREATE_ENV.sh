#!/bin/bash
# Script to create your .env file with all configured keys

cat > .env << 'EOF'
# ===== REQUIRED =====

# Google Gemini API Key
# NOTE: Add your Gemini key here (you mentioned having it from initial code)
GOOGLE_API_KEY=your_gemini_api_key_here

# GitHub Personal Access Token - CONFIGURED! ✅
GITHUB_TOKEN=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

# ===== MULTI-AGENT LLM =====

# DeepSeek R1 API Key - CONFIGURED! ✅
DEEPSEEK_API_KEY=sk-fa5b4fc2bd7749a7855a42880dbb914a

# Groq API Key (FREE!) - CONFIGURED! ✅
GROQ_API_KEY=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

# Multi-Agent Strategy
LLM_STRATEGY=specialized

# ===== OPTIONAL =====

# Jira Configuration (optional)
# JIRA_URL=https://your-domain.atlassian.net
# JIRA_EMAIL=your-email@example.com
# JIRA_API_TOKEN=your_jira_api_token

# Slack Configuration (optional)
# SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
# SLACK_CHANNEL=#project-updates

# ===== AGENT CONFIGURATION =====

GITHUB_REPO=BaHu-Git/Task_Manager
MAX_ISSUES=5
EOF

echo "✅ .env file created!"
echo ""
echo "📝 IMPORTANT: Edit .env and add your Gemini API key on line 6"
echo ""
echo "Then run:"
echo "  python src/tools/mcp_server.py"
echo "  python src/agent/multi_agent_runner.py"

