#!/bin/bash

# One-Click Setup Script for Kids Education App Launchers
# This makes both launchers executable so you can double-click them

echo ""
echo "========================================"
echo "🚀 Kids Education App - Launcher Setup"
echo "========================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Make START_APP.command executable
echo "Setting up START_APP.command..."
chmod +x "$SCRIPT_DIR/START_APP.command"
echo "✅ START_APP.command is now ready to double-click!"
echo ""

# Make launcher.py executable
echo "Setting up launcher.py..."
chmod +x "$SCRIPT_DIR/launcher.py"
echo "✅ launcher.py is now ready to double-click!"
echo ""

echo "========================================"
echo "✨ All Done! You Can Now:"
echo "========================================"
echo ""
echo "🚀 Option 1 (Simple):"
echo "   Double-click: START_APP.command"
echo ""
echo "🌟 Option 2 (Fancy UI):"
echo "   Double-click: launcher.py"
echo ""
echo "Both launchers will:"
echo "   ✅ Create Python environment (if needed)"
echo "   ✅ Install dependencies automatically"
echo "   ✅ Check if Ollama is running"
echo "   ✅ Launch Kids Education App!"
echo ""
echo "For more info, read: LAUNCHER_GUIDE.md"
echo ""
echo "========================================"
echo ""

read -p "Press Enter to close this window..."
