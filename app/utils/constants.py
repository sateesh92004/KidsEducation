"""Constants for KidsEducation App"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Admin Credentials (Hardcoded)
ADMIN_USERNAME = "sateesh92004"
ADMIN_PASSWORD = "Pandu12"

# Grades
GRADES = ["3", "4", "8"]

# Subjects
SUBJECTS = ["Mathematics", "Science", "English", "History", "Geography", "Computer Science"]

# Question Configuration
QUESTIONS_PER_PAPER = 100  # Generate 100 questions per topic (question pool)
PAPERS_PER_GENERATION = 1   # Generate 1 large pool per topic
QUESTIONS_PER_TEST = 20     # Each test uses 20 questions from the pool

# File Paths
BASE_DATA_PATH = "./app/data"
EXCEL_USERS_PATH = f"{BASE_DATA_PATH}/users_credentials.xlsx"
EXCEL_ADMIN_PATH = f"{BASE_DATA_PATH}/admin_credentials.xlsx"
EXCEL_TEST_RESULTS_PATH = f"{BASE_DATA_PATH}/test_results.xlsx"
TEST_PAPERS_PATH = f"{BASE_DATA_PATH}/TestPapers"

# UI Configuration
APP_TITLE = "Kids Education - AI Powered Test Generator"
APP_WIDTH = 1000
APP_HEIGHT = 700

# LLM Configuration

# Ollama (Local LLM)
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama2"  # Using Llama 2 for faster question generation

# Groq API (Ultra-fast, free tier)
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GROQ_MODEL = "llama-3.3-70b-versatile"  # Updated to current model

# Google Gemini API (High quality, free tier)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_MODEL = "gemini-1.5-flash"

# HuggingFace Inference API (Free tier)
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
HUGGINGFACE_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

# Difficulty Levels
DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]