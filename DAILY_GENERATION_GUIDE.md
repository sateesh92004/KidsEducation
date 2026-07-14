# 🌱 Daily Question Generation Guide

## Overview

This guide explains how to use the sustainable question generation script that generates questions in small, manageable chunks to avoid API rate limits.

## The Script: `generate_sustainable.py`

### What It Does

- Generates **20 questions per topic** per run
- Processes **3 topics maximum** per run
- Has **long delays** between requests to respect API limits
- Tracks progress and skips completed topics
- Designed to be run **daily or on a schedule**

### Configuration

You can modify these settings in the script:

```python
QUESTIONS_PER_TOPIC = 20  # Questions generated per topic per run
MAX_TOPICS_PER_RUN = 3    # Maximum topics to process per run
DELAY_BETWEEN_TOPICS = 300  # 5 minutes between topics
DELAY_BETWEEN_BATCHES = 60  # 1 minute between batches (in Groq service)
```

## How to Use

### Option 1: Run Manually (Daily)

```bash
# Activate virtual environment
source venv/bin/activate

# Run the script
python3 generate_sustainable.py
```

The script will:
1. Check which topics need questions
2. Process up to 3 topics (20 questions each)
3. Show progress and summary
4. Save all questions to database

### Option 2: Schedule Daily (Automated)

#### On macOS (using launchd):

1. Create a plist file:
```bash
nano ~/Library/LaunchAgents/com.kidseducation.dailygen.plist
```

2. Add this content (adjust paths):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.kidseducation.dailygen</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/sathishkumarudayagiri/Desktop/Sathish-Ai-Projects/KidsEducational-APP/KidsEducation/venv/bin/python3</string>
        <string>/Users/sathishkumarudayagiri/Desktop/Sathish-Ai-Projects/KidsEducational-APP/KidsEducation/generate_sustainable.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/sathishkumarudayagiri/Desktop/Sathish-Ai-Projects/KidsEducational-APP/KidsEducation</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/sathishkumarudayagiri/Desktop/Sathish-Ai-Projects/KidsEducational-APP/KidsEducation/daily_gen.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/sathishkumarudayagiri/Desktop/Sathish-Ai-Projects/KidsEducational-APP/KidsEducation/daily_gen_error.log</string>
</dict>
</plist>
```

3. Load the schedule:
```bash
launchctl load ~/Library/LaunchAgents/com.kidseducation.dailygen.plist
```

#### On Linux (using cron):

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * cd /path/to/KidsEducation && /path/to/venv/bin/python3 generate_sustainable.py >> daily_gen.log 2>&1
```

## Progress Tracking

### Check Current Status

```bash
python3 check_generation_complete.py
```

This shows:
- How many topics are complete (≥100 questions)
- How many topics need more questions
- Total questions generated
- Completion percentage

### Check Progress by Topic

```bash
python3 check_question_progress.py
```

## Expected Timeline

With the default settings:
- **Per run**: 3 topics × 20 questions = 60 questions
- **Per day**: 60 questions
- **Total needed**: 75 topics × 100 questions = 7,500 questions
- **Estimated time**: ~125 days (4 months)

### To Speed Up

You can increase the settings (but watch for rate limits):
- `QUESTIONS_PER_TOPIC = 30` (instead of 20)
- `MAX_TOPICS_PER_RUN = 5` (instead of 3)

**Warning**: Increasing these may cause rate limit errors. Start with defaults and adjust if needed.

## Benefits of This Approach

✅ **Sustainable**: Works within API rate limits  
✅ **Reliable**: Won't get stuck on rate limits  
✅ **Flexible**: Can adjust settings as needed  
✅ **Trackable**: Shows clear progress  
✅ **Resumable**: Skips completed topics automatically  

## Troubleshooting

### Rate Limit Errors

If you see rate limit errors:
1. Increase `DELAY_BETWEEN_TOPICS` to 600 (10 minutes)
2. Reduce `MAX_TOPICS_PER_RUN` to 2
3. Reduce `QUESTIONS_PER_TOPIC` to 15

### Script Stops

The script saves questions as it generates them, so you can:
- Stop anytime (Ctrl+C)
- Resume later - it will skip completed topics
- Run multiple times per day if needed

### No Questions Generated

Check:
1. LLM API keys are set in `.env`
2. Internet connection is working
3. API service is available (check logs)

## Next Steps

1. **Run the script once** to test it works
2. **Check the UI** - topics with questions will appear
3. **Set up daily schedule** if you want automation
4. **Monitor progress** using the check scripts

---

**Remember**: This is a marathon, not a sprint! Slow and steady wins the race. 🐢

