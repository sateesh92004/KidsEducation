#!/bin/bash

# Quick Setup Script for Kids Education App with Intelligent Agent
# This script helps you set up the environment and API keys

echo "🎓 Kids Education App - Intelligent Agent Setup"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed successfully!"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️  Setting up environment variables..."
    echo ""
    echo "You need at least ONE API key from the following providers:"
    echo ""
    echo "1. GROQ (Recommended - Fastest)"
    echo "   Sign up: https://console.groq.com/"
    echo ""
    echo "2. GOOGLE GEMINI (High Quality)"
    echo "   Get key: https://makersuite.google.com/app/apikey"
    echo ""
    echo "3. HUGGINGFACE (Open Source)"
    echo "   Get token: https://huggingface.co/settings/tokens"
    echo ""
    
    # Create .env file
    cp .env.template .env
    
    echo "📝 .env file created from template"
    echo ""
    echo "Please edit .env file and add your API keys:"
    echo "  nano .env"
    echo ""
    echo "Or use this script to add keys interactively:"
    echo ""
    
    read -p "Do you want to add API keys now? (y/n): " add_keys
    
    if [ "$add_keys" = "y" ] || [ "$add_keys" = "Y" ]; then
        echo ""
        read -p "Enter GROQ API Key (or press Enter to skip): " groq_key
        read -p "Enter GEMINI API Key (or press Enter to skip): " gemini_key
        read -p "Enter HUGGINGFACE API Key (or press Enter to skip): " hf_key
        
        # Update .env file
        if [ ! -z "$groq_key" ]; then
            sed -i '' "s/GROQ_API_KEY=.*/GROQ_API_KEY=$groq_key/" .env
            echo "✓ GROQ API key added"
        fi
        
        if [ ! -z "$gemini_key" ]; then
            sed -i '' "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=$gemini_key/" .env
            echo "✓ GEMINI API key added"
        fi
        
        if [ ! -z "$hf_key" ]; then
            sed -i '' "s/HUGGINGFACE_API_KEY=.*/HUGGINGFACE_API_KEY=$hf_key/" .env
            echo "✓ HUGGINGFACE API key added"
        fi
    fi
else
    echo "✓ .env file already exists"
fi

echo ""
echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Make sure you have at least one API key in .env file"
echo "2. Run the app: python app/main.py"
echo ""
echo "For detailed setup instructions, see: AGENT_SETUP_GUIDE.md"
echo ""
echo "🚀 Ready to generate question papers with AI!"
echo ""
