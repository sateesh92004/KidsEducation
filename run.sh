#!/bin/bash

# Kids Education App Startup Script

echo "🎓 Kids Education - AI-Powered Question Generator"
echo "================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔌 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing/updating dependencies..."
pip install -q -r requirements.txt

echo ""
echo "⚠️  IMPORTANT: Make sure Ollama is running!"
echo "   Open a new terminal and run: ollama serve"
echo ""
read -p "Press Enter once Ollama is running..."

echo ""
echo "🚀 Starting Kids Education App..."
echo ""

python3 app/main.py