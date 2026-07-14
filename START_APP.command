#!/bin/bash

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "🚀 Starting Kids Education App..."
echo "================================="

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    read -p "Press Enter to exit..."
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found, using system python..."
fi

# Run the application
python3 app/main.py

# Keep terminal open if it crashes
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ App crashed or closed unexpectedly."
    read -p "Press Enter to exit..."
fi
