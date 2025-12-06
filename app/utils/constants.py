"""Constants for KidsEducation App"""

# Admin Credentials (Hardcoded)
ADMIN_USERNAME = "sateesh92004"
ADMIN_PASSWORD = "Pandu12"

# Grades
GRADES = ["3", "4", "8"]

# Subjects
SUBJECTS = ["Maths", "Science"]

# Question Configuration
QUESTIONS_PER_PAPER = 30
PAPERS_PER_GENERATION = 10  # 10 papers per admin request

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
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral"  # or "llama2"

# Difficulty Levels
DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]