#!/bin/bash
# Monitor Topic 1 generation and notify when complete

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔍 Monitoring Topic 1 generation..."
echo "Press Ctrl+C to stop"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check every 2 minutes
CHECK_INTERVAL=120

while true; do
    echo ""
    echo "⏰ $(date '+%H:%M:%S') - Checking status..."
    
    # Run the status check
    python3 check_topic1_status.py
    STATUS=$?
    
    if [ $STATUS -eq 0 ]; then
        echo ""
        echo "🎉🎉🎉 TOPIC 1 IS COMPLETE! 🎉🎉🎉"
        echo ""
        echo "You can now test the UI!"
        echo ""
        
        # Optional: Play a sound
        if command -v say &> /dev/null; then
            say "Topic 1 generation complete!"
        fi
        
        break
    else
        echo "⏳ Waiting 2 minutes before next check..."
        sleep $CHECK_INTERVAL
    fi
done

