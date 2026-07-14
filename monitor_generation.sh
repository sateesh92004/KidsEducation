#!/bin/bash
# Monitor question generation and notify when complete

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔍 Starting monitoring of question generation..."
echo "Press Ctrl+C to stop monitoring"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check every 5 minutes
CHECK_INTERVAL=300  # 5 minutes in seconds
LAST_COMPLETED=0

while true; do
    echo ""
    echo "⏰ $(date '+%Y-%m-%d %H:%M:%S') - Checking status..."
    
    # Run the completion check
    python3 check_generation_complete.py
    STATUS=$?
    
    if [ $STATUS -eq 0 ]; then
        echo ""
        echo "🎉🎉🎉 GENERATION COMPLETE! 🎉🎉🎉"
        echo ""
        echo "All questions have been generated and loaded into the database!"
        echo ""
        
        # Optional: Play a sound or send notification
        if command -v say &> /dev/null; then
            say "Question generation complete!"
        fi
        
        # Show final summary
        python3 check_question_progress.py
        
        break
    else
        # Count completed topics
        COMPLETED=$(python3 check_generation_complete.py 2>/dev/null | grep "Completed Topics" | awk '{print $4}' | cut -d'/' -f1)
        
        if [ ! -z "$COMPLETED" ] && [ "$COMPLETED" -gt "$LAST_COMPLETED" ]; then
            echo "📈 Progress: $COMPLETED topics completed!"
            LAST_COMPLETED=$COMPLETED
        fi
        
        echo "⏳ Waiting $((CHECK_INTERVAL / 60)) minutes before next check..."
        sleep $CHECK_INTERVAL
    fi
done

