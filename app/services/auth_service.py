"""Authentication Service"""

from services.db_user_service import DBUserService

class AuthService:
    """Service for handling user authentication"""

    def __init__(self):
        self.db_user_service = DBUserService()
        self.current_user = None

    def login(self, username, password):
        """Authenticate user"""
        result = self.db_user_service.login_user(username, password)
        if result["success"]:
            self.current_user = result["user"]
        return result

    def register_student(self, username, password, full_name=None):
        """Register a new student"""
        return self.db_user_service.register_user(username, password, 'student', full_name)

    def get_current_user(self):
        """Get currently logged in user"""
        return self.current_user

    def logout(self):
        """Logout current user"""
        self.current_user = None