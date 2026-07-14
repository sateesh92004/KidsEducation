"""Database User Service - Manages user authentication and profiles"""

from typing import Optional, Dict, List, Any
from database.db_manager import db

class DBUserService:
    """Service for managing users in SQLite database"""
    
    def register_user(self, username: str, password: str, role: str = 'student', full_name: str = None) -> Dict[str, Any]:
        """Register a new user"""
        # Check if user exists
        existing = db.execute_query("SELECT id FROM users WHERE username = ?", (username,))
        if existing:
            return {"success": False, "message": "Username already exists"}
        
        # Hash password
        password_hash = db.hash_password(password)
        
        try:
            user_id = db.execute_insert(
                "INSERT INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)",
                (username, password_hash, role, full_name)
            )
            return {"success": True, "message": "User registered successfully", "user_id": user_id}
        except Exception as e:
            return {"success": False, "message": f"Registration failed: {str(e)}"}

    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user"""
        users = db.execute_query(
            "SELECT id, username, password_hash, role, full_name FROM users WHERE username = ?", 
            (username,)
        )
        
        if not users:
            return {"success": False, "message": "Invalid username or password"}
        
        user = users[0]
        if db.verify_password(password, user['password_hash']):
            # Update last login
            db.execute_update("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (user['id'],))
            
            return {
                "success": True, 
                "message": "Login successful",
                "user": {
                    "id": user['id'],
                    "username": user['username'],
                    "role": user['role'],
                    "full_name": user['full_name']
                }
            }
        
        return {"success": False, "message": "Invalid username or password"}

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user details by username"""
        users = db.execute_query(
            "SELECT id, username, role, full_name, created_at, last_login FROM users WHERE username = ?", 
            (username,)
        )
        return users[0] if users else None

    def get_all_students(self) -> List[Dict]:
        """Get list of all students (for admin)"""
        return db.execute_query(
            "SELECT id, username, full_name, created_at, last_login FROM users WHERE role = 'student' ORDER BY created_at DESC"
        )
