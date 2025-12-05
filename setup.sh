#!/bin/bash
# Complete setup script for the project

set -e  # Exit on error

echo "🚀 Setting up Devops_and_LLMs project..."
echo ""

# Check if we're in the right directory
if [ ! -f "environment.yml" ]; then
    echo "❌ Error: environment.yml not found. Please run this script from the project root."
    exit 1
fi

# Step 1: Create conda environment
echo "📦 Step 1: Setting up conda environment..."
if conda env list | grep -q "agent-env"; then
    echo "⚠️  Environment 'agent-env' already exists. Updating..."
    conda env update -f environment.yml --prune
else
    echo "Creating new environment 'agent-env'..."
    conda env create -f environment.yml
fi
echo "✅ Conda environment ready"
echo ""

# Step 2: Install pip dependencies
echo "📦 Step 2: Installing Python dependencies..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate agent-env
pip install -r requirements.txt
echo "✅ Python dependencies installed"
echo ""

# Step 3: Check for .env file
echo "🔑 Step 3: Checking configuration..."
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    ./CREATE_ENV.sh
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
    echo "   Required: GOOGLE_API_KEY"
    echo "   Optional: DEEPSEEK_API_KEY, GROQ_API_KEY"
    echo ""
else
    echo "✅ .env file exists"
fi
echo ""

# Step 4: Check for credentials.json
echo "🔑 Step 4: Checking Google Calendar credentials..."
if [ ! -f "credentials.json" ]; then
    echo "⚠️  No credentials.json found"
    echo ""
    echo "To use Google Calendar integration:"
    echo "  1. Go to: https://console.cloud.google.com/"
    echo "  2. Create project → Enable Calendar API"
    echo "  3. Create OAuth Desktop credentials"
    echo "  4. Download as 'credentials.json' to project root"
    echo ""
else
    echo "✅ credentials.json exists"
fi
echo ""

# Step 5: Test imports
echo "🧪 Step 5: Testing imports..."
python -c "
try:
    from src.core.task_breakdown import TaskBreakdown
    from src.core.scheduler import Scheduler
    from src.core.llm_factory import LLMFactory
    print('✅ All core imports successful!')
except Exception as e:
    print(f'❌ Import error: {e}')
    exit(1)
"
echo ""

# Summary
echo "============================================================"
echo "🎉 Setup Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Activate environment:"
echo "   conda activate agent-env"
echo ""
echo "2. Add your Gemini API key to .env (if not done)"
echo "   nano .env"
echo ""
echo "3. Test configuration:"
echo "   python test_setup.py"
echo ""
echo "4. Run the agent:"
echo "   # Simple (GitHub → Calendar)"
echo "   python src/agent/run_agent.py"
echo ""
echo "   # Multi-agent (3 LLMs comparison)"
echo "   python src/agent/multi_agent_runner.py"
echo ""
echo "============================================================"

