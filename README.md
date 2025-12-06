# 🎓 Kids Education - AI-Powered Question Generator

A beautiful desktop application that generates complex multiple-choice questions for students using AI (LLM). Students can take tests while admins can generate question papers.

## ✨ Features

### 👤 Student Features
- **User Registration & Login**: Secure credentials stored in Excel
- **Beautiful Dashboard**: Select grade, subject, and topic
- **Interactive Testing**: 30 MCQ tests with instant feedback
- **Score Tracking**: Automatic calculation and storage of test results
- **Test History**: All results saved in Excel for reference

### 🔧 Admin Features
- **Question Paper Generation**: Generate 10 papers per topic using AI
- **LLM Integration**: Uses Ollama (free, open-source) for question generation
- **Bulk Generation**: Generate papers for any grade, subject, and topic combination
- **Answer Keys**: Automatically generated and stored separately

## 📋 System Requirements

- Python 3.9 or higher
- Ollama (for LLM)
- 4GB RAM minimum
- macOS / Linux / Windows

## 🚀 Installation & Setup

### 1. Install Ollama

Download and install Ollama from: https://ollama.ai

After installation, pull a suitable model:
```bash
ollama pull mistral
# or
ollama pull llama2
```

Start Ollama service:
```bash
ollama serve
```

### 2. Create Virtual Environment

```bash
cd "/Users/s0u00g7/Desktop/sathish-ai-Usecase/Sathish Personal APP/KidsEducation"
Python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app/main.py
```

## 📂 Project Structure

```
KidsEducation/
├── app/
│   ├── main.py                 # Application entry point
│   ├── ui/                     # User interface screens
│   │   ├── base_window.py      # Base window with styling
│   │   ├── login_screen.py     # Login and registration
│   │   ├── admin_panel.py      # Admin question generator
│   │   ├── student_dashboard.py # Student main screen
│   │   └── test_screen.py      # Test taking interface
│   ├── services/               # Business logic
│   │   ├── auth_service.py     # Authentication
│   │   ├── llm_service.py      # LLM integration
│   │   ├── question_service.py # Question management
│   │   └── score_service.py    # Score calculation
│   ├── utils/                  # Utilities
│   │   ├── constants.py        # App constants
│   │   └── excel_handler.py    # Excel operations
│   └── data/                   # Data storage
│       ├── users_credentials.xlsx      # User logins
│       ├── test_results.xlsx           # Test scores
│       └── TestPapers/         # Generated question papers
├── requirements.txt
└── README.md
```

## 👥 User Credentials

### Student Users
- Created during registration
- Stored in `app/data/users_credentials.xlsx`

### Admin User
- **Username**: `sateesh92004`
- **Password**: `Pandu12`

## 📊 Data Storage

### Excel Files

1. **users_credentials.xlsx**
   - Username, Password, Registration Date, Last Login

2. **test_results.xlsx**
   - Student ID, Grade, Subject, Topic, Score, Timestamp

3. **questions_*.xlsx**
   - Generated question papers with options and answers

### JSON Files (TestPapers/)

- `paper_*.json` - Full question papers with explanations
- `answers_*.json` - Answer keys only

## 🔄 Workflow

### Admin Workflow
1. Login with admin credentials
2. Select Grade (3, 4, 8)
3. Select Subject (Maths, Science)
4. Enter Topic name
5. Click "Generate 10 Question Papers"
6. System calls LLM to generate 30 MCQs per paper
7. Papers and answer keys saved to TestPapers folder

### Student Workflow
1. Register new account or login
2. Select Grade, Subject, Topic from dropdowns
3. Start Test (30 MCQs from pre-generated papers)
4. Answer all questions
5. Submit test
6. View score and performance
7. Results saved to Excel

## 🤖 LLM Configuration

The app uses **Ollama** with open-source models:

- **Mistral 7B** (Recommended) - Fast and accurate
- **Llama 2** - More thorough responses

Configure in `app/utils/constants.py`:

```python
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral"  # or "llama2"
```

## 📝 Excel Structure

### users_credentials.xlsx
| Username | Password | Registration Date | Last Login |
|----------|----------|-------------------|------------|
| john123  | pass@123 | 2025-01-15 10:30  | -          |

### test_results.xlsx
| Username | Grade | Subject | Topic | Paper # | Q's Answered | Correct | Score % | Date |
|----------|-------|---------|-------|---------|--------------|---------|---------|------|
| john123  | 8     | Maths   | Algebra | 1    | 30           | 24      | 80.00%  | 2025-01-15 14:20 |

## 🎯 Configuration

Edit `app/utils/constants.py` to customize:

```python
GRADES = ["3", "4", "8"]  # Available grades
SUBJECTS = ["Maths", "Science"]  # Available subjects
QUESTIONS_PER_PAPER = 30  # Questions per paper
PAPERS_PER_GENERATION = 10  # Papers per admin request
```

## 🔒 Security Notes

- **Passwords**: Stored as-is in Excel (consider encryption for production)
- **Admin Credentials**: Hardcoded (change in production)
- **Data**: All data stored locally in app/data folder

## 🐛 Troubleshooting

### Ollama Connection Error
```
Error: Ollama is not running
```
**Solution**: Start Ollama service in terminal
```bash
ollama serve
```

### Question Generation Timeout
```
Request timeout - LLM generation took too long
```
**Solution**: Use a faster model (Mistral instead of Llama2) or check your network

### Excel Permission Error
```
PermissionError: file is open in another application
```
**Solution**: Close Excel/spreadsheet apps and try again

## 📈 Future Enhancements

- [ ] Database instead of Excel (PostgreSQL)
- [ ] Web version (Flask/React)
- [ ] Image-based questions support
- [ ] Detailed analytics dashboard
- [ ] Multiple language support
- [ ] Encrypted password storage
- [ ] Email notifications
- [ ] Leaderboard system

## 📄 License

Personal Project - Not for commercial use

## 👨‍💻 Author

Sathish - 2025

---

**Made with ❤️ using Python, PyQt6, and AI** 🚀