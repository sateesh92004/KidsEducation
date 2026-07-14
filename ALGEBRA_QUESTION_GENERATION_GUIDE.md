# 📚 8th Grade Algebra Question Generation Guide

## Overview

This script generates **100 complex, non-repetitive, multiple-choice questions** for each subtopic in the 8th Grade Algebra syllabus based on the textbook table of contents.

## 📋 Topics Covered

The script covers all 8 chapters with their subtopics:

1. **Chapter 2: Functions, Equations, and Graphs** (9 subtopics)
2. **Chapter 3: Linear Systems** (8 subtopics)
3. **Chapter 4: Quadratic Functions and Equations** (14 subtopics)
4. **Chapter 5: Polynomials and Polynomial Functions** (11 subtopics)
5. **Chapter 6: Radical Functions and Rational Exponents** (10 subtopics)
6. **Chapter 7: Exponential and Logarithmic Functions** (8 subtopics)
7. **Chapter 8: Rational Functions** (8 subtopics)
8. **Chapter 9: Sequences and Series** (7 subtopics)

**Total: ~75 subtopics × 100 questions = ~7,500 questions**

## 🚀 How to Run

### Prerequisites

1. **LLM API Keys**: You need at least one of the following:
   - `GROQ_API_KEY` (recommended - fastest, free tier)
   - `GEMINI_API_KEY` (high quality, free tier)
   - `HUGGINGFACE_API_KEY` (free tier)

2. **Environment Setup**:
   ```bash
   # Activate virtual environment
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   
   # Install dependencies (if not already installed)
   pip install -r requirements.txt
   ```

3. **Set API Keys**:
   ```bash
   # Create .env file if it doesn't exist
   echo "GROQ_API_KEY=your_key_here" >> .env
   # or
   echo "GEMINI_API_KEY=your_key_here" >> .env
   ```

### Running the Script

```bash
python3 generate_algebra_questions.py
```

The script will:
1. Check LLM availability
2. Ask for confirmation
3. Process each topic sequentially
4. Generate 100 questions per subtopic
5. Save questions to the database automatically
6. Show progress and summary

## ⚙️ Features

- **Automatic Duplicate Detection**: Prevents duplicate questions
- **Progress Tracking**: Shows real-time progress for each topic
- **Resume Capability**: Skips topics that already have 100+ questions
- **Error Handling**: Continues even if some topics fail
- **Multiple LLM Support**: Automatically falls back to available LLMs
- **Database Integration**: Questions are saved directly to SQLite database

## 📊 Question Characteristics

Each generated question includes:
- **Question Text**: Clear, age-appropriate problem
- **4 Multiple Choice Options** (A, B, C, D)
- **Correct Answer**: Marked with explanation
- **Explanation**: Why the answer is correct
- **Difficulty Level**: Easy, Medium, or Hard
- **Question Type**: word_problem, complex, conceptual, or application

## ⏱️ Estimated Time

- **Per Topic**: ~2-5 minutes (depending on LLM)
- **Total Time**: ~3-6 hours for all topics (depending on API rate limits)

## 🔍 Monitoring Progress

The script provides detailed output:
- ✅ Success indicators
- 📊 Question counts
- ⚠️ Warnings for incomplete topics
- 📈 Real-time statistics

## 🛠️ Troubleshooting

### No LLM Available
- Check your API keys in `.env` file
- Verify API keys are valid
- Check internet connection

### Rate Limit Errors
- The script will automatically retry
- Consider running in smaller batches
- Wait and resume later (script skips completed topics)

### Database Errors
- Ensure database is initialized
- Check file permissions
- Verify database path

## 📝 Notes

- Questions are generated in batches of 100
- The script checks for existing questions to avoid duplicates
- You can stop and resume - completed topics will be skipped
- All questions are saved to `app/kids_education.db`

## 🎯 Next Steps

After generation:
1. Questions are automatically available in the app
2. Students can take tests on any topic
3. Admin can review questions in the admin panel
4. Questions are tracked per user (no repeats)

---

**Need Help?** Check the main README.md or review the code comments in `generate_algebra_questions.py`

