# 🚀 Kids Education App - Complete Setup Guide

This is your step-by-step guide to get the Kids Education AI-Powered Question Generator running on your Mac!

## 📋 Pre-Requisites

- ✅ macOS 10.14 or later
- ✅ Python 3.9+ (check with `python3 --version`)
- ✅ At least 4GB free RAM
- ✅ Internet connection for initial setup

---

## 🎯 Complete Setup Instructions

### **Step 1: Install Ollama (The AI Engine)**

Ollama is a free, open-source tool that runs AI models locally on your machine.

1. Visit: https://ollama.ai
2. Click **Download for Mac**
3. Select **Apple Silicon (M1/M2/M3)** or **Intel** based on your Mac
4. Open the downloaded `.dmg` file
5. Drag Ollama to Applications
6. Open Ollama from Applications (you'll see it in the menu bar)

#### Download a Model (Choose ONE)

Open **Terminal** and run one of these commands:

```bash
# Option 1: Mistral 7B (RECOMMENDED - Faster, 4GB)
ollama pull mistral

# Option 2: Llama 2 (More thorough, 7GB)
ollama pull llama2

# Option 3: Neural Chat (Lightweight, 3GB)
ollama pull neural-chat
```

**Recommendation**: Use **Mistral** for the best balance of speed and accuracy.

#### Start Ollama Service

Ollama should auto-start, but you can verify:

```bash
curl http://localhost:11434/api/tags
```

If you see a list of models, you're good! ✅

---

### **Step 2: Setup the Kids Education App**

#### Option A: Easy Setup (Using the run.sh script)

```bash
# 1. Navigate to the KidsEducation folder
cd "/Users/$(whoami)/Desktop/sathish-ai-Usecase/Sathish Personal APP/KidsEducation"

# 2. Make the script executable (one-time only)
chmod +x run.sh

# 3. Run the app
./run.sh
```

#### Option B: Manual Setup

```bash
# 1. Navigate to the KidsEducation folder
cd "/Users/$(whoami)/Desktop/sathish-ai-Usecase/Sathish Personal APP/KidsEducation"

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python3 app/main.py
```

---

## 🎓 Using the App

### **Admin Panel (Generate Question Papers)**

**Credentials:**
- Username: `sateesh92004`
- Password: `Pandu12`

**Steps:**
1. Launch the app
2. Click **Admin** tab
3. Enter credentials
4. Select Grade (3, 4, or 8)
5. Select Subject (Maths or Science)
6. Enter Topic name (e.g., "Algebra", "Photosynthesis")
7. Click **Generate 10 Question Papers**
8. Wait for generation (this takes a few minutes)
9. Papers are saved in `app/data/TestPapers/`

### **Student Portal (Take Tests)**

**First Time Users:**
1. Launch the app
2. Click **Student** → **Register**
3. Choose a username (3-20 characters, alphanumeric)
4. Choose a password (minimum 4 characters)
5. Confirm password
6. Click **Register**

**Returning Students:**
1. Click **Student** → **Login**
2. Enter username and password
3. Click **Login**

**Taking a Test:**
1. Select Grade from dropdown
2. Select Subject from dropdown
3. Select Topic from dropdown
4. Click **Start Test**
5. Answer all 30 multiple-choice questions
6. Click **Submit Test**
7. View your score!

---

## 📁 Data Location

All your data is saved locally:

```
KidsEducation/app/data/
├── users_credentials.xlsx          # Student login info
├── test_results.xlsx               # Test scores & results
└── TestPapers/
    ├── paper_8_Maths_Algebra_p1.json        # Question papers
    ├── answers_8_Maths_Algebra_p1.json      # Answer keys
    └── ...
```

**You can open Excel files directly to view results!**

---

## 🔧 Troubleshooting

### **Problem: "Ollama is not running" Error**

**Solution:**
```bash
# Make sure Ollama is started
# Check Terminal for Ollama output, or
# Open Ollama from Applications → Keep it running

# In a new Terminal, verify:
curl http://localhost:11434/api/tags
```

### **Problem: Python not found**

**Solution:**
```bash
# Check Python version
python3 --version  # Should be 3.9 or higher

# If not installed, install from: https://www.python.org
```

### **Problem: Module not found errors**

**Solution:**
```bash
# Make sure you activated the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### **Problem: Excel file is locked**

**Solution:**
- Close Excel or Numbers app
- Close any spreadsheet applications
- Try again

### **Problem: Question generation is slow**

**Solution:**
- This is normal! LLM generation takes 2-5 minutes per paper
- Mistral is faster than Llama2
- Ensure Ollama is using GPU (check terminal output)

---

## ⚙️ Configuration

To customize the app, edit `app/utils/constants.py`:

```python
# Change available grades
GRADES = ["3", "4", "8", "10"]  # Add grade 10

# Change available subjects
SUBJECTS = ["Maths", "Science", "English"]  # Add English

# Change LLM model
OLLAMA_MODEL = "llama2"  # Switch to llama2

# Change number of papers generated per request
PAPERS_PER_GENERATION = 5  # Generate 5 instead of 10
```

---

## 🎨 UI Customization

Edit `app/ui/base_window.py` to change colors:

```python
def get_button_style(self) -> str:
    return """
        QPushButton {
            background-color: #4472C4;  # Change this color
            color: white;
            ...
        }
    """
```

---

## 📊 File Locations

| File | Purpose | Location |
|------|---------|----------|
| users_credentials.xlsx | Student login data | `app/data/` |
| test_results.xlsx | Test scores | `app/data/` |
| Question Papers | Generated MCQs | `app/data/TestPapers/` |
| Answer Keys | Correct answers | `app/data/TestPapers/` |

---

## 🚀 Quick Commands

```bash
# Start the app
cd "path/to/KidsEducation"
./run.sh

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app directly
python3 app/main.py

# Start Ollama
ollama serve

# Pull a model
ollama pull mistral
```

---

## 📞 Support

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Verify Ollama is running
3. Check Python version (must be 3.9+)
4. Ensure all dependencies are installed

---

## ✨ Features Summary

✅ Beautiful PyQt6 desktop UI  
✅ Student registration & login  
✅ 30-question MCQ tests  
✅ Instant scoring  
✅ AI-generated questions using Ollama  
✅ Admin panel for paper generation  
✅ Excel storage of credentials & results  
✅ Grade/Subject/Topic filtering  
✅ Answer key management  
✅ Test history tracking  

---

## 🎯 Next Steps

1. ✅ Install Ollama (Download → Install → Run)
2. ✅ Setup the app (Navigate → Run setup script)
3. ✅ Generate test papers (Admin → Create papers)
4. ✅ Take tests (Student → Login → Select topic → Start test)

---

**Happy Learning! 🎓**

*Created by Sathish - December 2025*