"""Authentication Service"""

from utils.excel_handler import ExcelHandler
from utils.constants import ADMIN_USERNAME, ADMIN_PASSWORD


class AuthService:
    """Handles all authentication operations"""

    @staticmethod
    def register_student(username: str, password: str) -> tuple[bool, str]:
        """
        Register a new student
        Returns: (success: bool, message: str)
        """
        # Validate inputs
        if not username or not password:
            return False, "Username and password cannot be empty"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if len(password) < 4:
            return False, "Password must be at least 4 characters long"
        
        # Check if user already exists
        if ExcelHandler.user_exists(username):
            return False, "Username already exists. Please choose a different one."
        
        # Register user
        if ExcelHandler.register_user(username, password):
            return True, "Registration successful! You can now login."
        else:
            return False, "Registration failed. Please try again."

    @staticmethod
    def login_student(username: str, password: str) -> tuple[bool, str]:
        """
        Login a student
        Returns: (success: bool, message: str)
        """
        if not username or not password:
            return False, "Username and password cannot be empty"
        
        if ExcelHandler.validate_user(username, password):
            return True, f"Welcome back, {username}!"
        else:
            return False, "Invalid username or password. Please try again."

    @staticmethod
    def login_admin(username: str, password: str) -> tuple[bool, str]:
        """
        Login admin
        Returns: (success: bool, message: str)
        """
        if not username or not password:
            return False, "Username and password cannot be empty"
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return True, "Admin login successful!"
        else:
            return False, "Invalid admin credentials. Please try again."

    @staticmethod
    def is_valid_username(username: str) -> bool:
        """Check if username is valid format"""
        # Username should be alphanumeric, 3-20 characters
        return 3 <= len(username) <= 20 and username.isalnum()

    @staticmethod
    def is_valid_password(password: str) -> bool:
        """Check if password is valid format"""
        # Password should be at least 4 characters
        return len(password) >= 4