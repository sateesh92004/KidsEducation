#!/bin/bash

# Kids Education App - Double-Click Launcher
# This script can be double-clicked to launch the app on macOS

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "========================================"
echo "🎓 Kids Education App Launcher"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "📦 Virtual environment not found. Creating one..."
    cd "$SCRIPT_DIR"
    python3 -m venv venv
    echo "✅ Virtual environment created!"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source "$SCRIPT_DIR/venv/bin/activate"

# Check if dependencies are installed
echo "📚 Checking dependencies..."
if ! pip list | grep -q PyQt6; then
    echo "📦 Installing dependencies (this may take a minute)..."
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r "$SCRIPT_DIR/requirements.txt" > /dev/null 2>&1
    echo "✅ Dependencies installed!"
else
    echo "✅ Dependencies already installed!"
fi

echo ""
echo "========================================"
echo "🚀 Starting Kids Education App..."
echo "========================================"
echo ""

# Check if Ollama is running
echo "🔍 Checking if Ollama is running..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo ""
    echo "⚠️  WARNING: Ollama is not running!"
    echo ""
    echo "The app will still start, but you won't be able to generate questions."
    echo ""
    echo "To start Ollama:"
    echo "  1. Open Applications folder"
    echo "  2. Find and double-click 'Ollama'"
    echo "  3. Wait for it to appear in the menu bar"
    echo ""
    read -p "Press Enter to continue anyway..."
else
    echo "✅ Ollama is running!"
fi

echo ""
echo "Starting application..."
echo ""

# Run the main app
cd "$SCRIPT_DIR"
python3 app/main.py
