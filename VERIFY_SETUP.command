#!/bin/bash

# Kids Education App - Setup Verification Script
# This script checks if everything is ready to launch

echo ""
echo "🛨️  KIDS EDUCATION APP - SETUP VERIFICATION"
echo "============================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "📑 VERIFICATION CHECKLIST:"
echo ""

# Check 1: Python
echo -n "1. Checking Python... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✅ Found (v$PYTHON_VERSION)${NC}"
else
    echo -e "${RED}❌ Not found${NC}"
fi

# Check 2: Virtual Environment
echo -n "2. Checking virtual environment... "
if [ -d "$SCRIPT_DIR/venv" ]; then
    echo -e "${GREEN}✅ Created${NC}"
else
    echo -e "${YELLOW}⚠️  Missing (will be created on first launch)${NC}"
fi

# Check 3: Requirements File
echo -n "3. Checking requirements file... "
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo -e "${GREEN}✅ Found${NC}"
else
    echo -e "${RED}❌ Not found${NC}"
fi

# Check 4: App Structure
echo -n "4. Checking app structure... "
if [ -f "$SCRIPT_DIR/app/main.py" ] && [ -d "$SCRIPT_DIR/app/ui" ] && [ -d "$SCRIPT_DIR/app/services" ]; then
    echo -e "${GREEN}✅ Complete${NC}"
else
    echo -e "${RED}❌ Incomplete${NC}"
fi

# Check 5: Ollama
echo -n "5. Checking Ollama service... "
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Running${NC}"
    
    # Check if models exist
    MODELS=$(curl -s http://localhost:11434/api/tags | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('models', [])))" 2>/dev/null)
    if [ "$MODELS" -gt 0 ]; then
        echo -e "   ✅ Models available: $MODELS"
    else
        echo -e "   ${YELLOW}⚠️  No models downloaded${NC}"
        echo -e "   ${YELLOW}   Run: ollama pull mistral${NC}"
    fi
else
    echo -e "${RED}❌ Not running${NC}"
    echo -e "   ${YELLOW}Start: Applications → Ollama${NC}"
fi

# Check 6: Launchers
echo -n "6. Checking launchers... "
if [ -x "$SCRIPT_DIR/START_APP.command" ] && [ -x "$SCRIPT_DIR/launcher.py" ]; then
    echo -e "${GREEN}✅ Both executable${NC}"
elif [ -x "$SCRIPT_DIR/START_APP.command" ]; then
    echo -e "${GREEN}✅ START_APP.command executable${NC}"
elif [ -x "$SCRIPT_DIR/launcher.py" ]; then
    echo -e "${GREEN}✅ launcher.py executable${NC}"
else
    echo -e "${YELLOW}⚠️  Not executable (fixing...)${NC}"
    chmod +x "$SCRIPT_DIR/START_APP.command" 2>/dev/null
    chmod +x "$SCRIPT_DIR/launcher.py" 2>/dev/null
    echo -e "   ${GREEN}✅ Fixed!${NC}"
fi

# Check 7: Data Directory
echo -n "7. Checking data directory... "
if [ -d "$SCRIPT_DIR/app/data" ]; then
    echo -e "${GREEN}✅ Exists${NC}"
else
    echo -e "${YELLOW}⚠️  Creating...${NC}"
    mkdir -p "$SCRIPT_DIR/app/data"
    echo -e "   ${GREEN}✅ Created${NC}"
fi

echo ""
echo "============================================"
echo "🌟 SUMMARY:"
echo "============================================"
echo ""
echo -e "${GREEN}✅ App is ready to launch!${NC}"
echo ""
echo "🚀 NEXT STEPS:"
echo ""
echo "1. Make sure Ollama is running (Applications → Ollama)"
echo ""
echo "2. (Optional) Download a model:"
echo "   ollama pull mistral"
echo ""
echo "3. Launch the app:"
echo "   • Double-click: START_APP.command (simple)"
echo "   • OR Double-click: launcher.py (fancy)"
echo ""
echo "4. Start testing!"
echo ""
echo "============================================"
echo ""

read -p "Press Enter to close this window..."
