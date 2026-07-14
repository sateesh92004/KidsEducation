"""Database Prompt Service - Manages admin custom prompts"""

from typing import List, Dict, Optional
from database.db_manager import db

class DBPromptService:
    """Service for managing custom prompts"""
    
    def save_prompt(self, admin_id: int, grade: str, subject: str, topic: str, 
                   prompt_name: str, custom_prompt: str) -> int:
        """Save a new custom prompt"""
        return db.execute_insert(
            """INSERT INTO custom_prompts 
               (admin_id, grade, subject, topic, prompt_name, custom_prompt)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (admin_id, grade, subject, topic, prompt_name, custom_prompt)
        )

    def get_prompts(self, grade: str = None, subject: str = None, topic: str = None) -> List[Dict]:
        """Get custom prompts, optionally filtered"""
        query = "SELECT * FROM custom_prompts WHERE is_active = 1"
        params = []
        
        if grade:
            query += " AND grade = ?"
            params.append(grade)
        if subject:
            query += " AND subject = ?"
            params.append(subject)
        if topic:
            query += " AND topic = ?"
            params.append(topic)
            
        query += " ORDER BY created_at DESC"
        
        return db.execute_query(query, tuple(params))

    def get_prompt_by_id(self, prompt_id: int) -> Optional[Dict]:
        """Get a specific prompt"""
        result = db.execute_query("SELECT * FROM custom_prompts WHERE id = ?", (prompt_id,))
        return result[0] if result else None

    def delete_prompt(self, prompt_id: int) -> bool:
        """Soft delete a prompt"""
        count = db.execute_update("UPDATE custom_prompts SET is_active = 0 WHERE id = ?", (prompt_id,))
        return count > 0
