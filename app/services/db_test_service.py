"""Database Test Service - Manages test results"""

from typing import List, Dict, Any
from database.db_manager import db

class DBTestService:
    """Service for managing test results in SQLite database"""
    
    def save_test_result(self, user_id: int, grade: str, subject: str, topic: str, 
                        total_questions: int, correct_answers: int, wrong_answers: int,
                        details: List[Dict]) -> int:
        """Save test result and detailed answers"""
        
        score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        try:
            # 1. Save main result
            result_id = db.execute_insert(
                """INSERT INTO test_results 
                   (user_id, grade, subject, topic, total_questions, correct_answers, wrong_answers, score_percentage)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, grade, subject, topic, total_questions, correct_answers, wrong_answers, score_percentage)
            )
            
            # 2. Save detailed answers
            for detail in details:
                # We need the question ID. If it's passed in details, great. 
                # If not (legacy flow), we might have trouble linking.
                # The DBQuestionService returns 'id' in the question object, so UI should pass it back.
                question_id = detail.get('id') 
                
                if question_id:
                    db.execute_insert(
                        """INSERT INTO test_answers 
                           (test_result_id, question_id, user_answer, is_correct)
                           VALUES (?, ?, ?, ?)""",
                        (result_id, question_id, detail.get('user_answer', ''), detail.get('is_correct', False))
                    )
            
            return result_id
        except Exception as e:
            print(f"Error saving test result: {e}")
            return -1

    def get_user_test_history(self, user_id: int) -> List[Dict]:
        """Get test history for a user"""
        return db.execute_query(
            """SELECT * FROM test_results 
               WHERE user_id = ? 
               ORDER BY test_date DESC""",
            (user_id,)
        )

    def get_test_details(self, result_id: int) -> Dict:
        """Get detailed results for a specific test"""
        result = db.execute_query("SELECT * FROM test_results WHERE id = ?", (result_id,))
        if not result:
            return None
            
        answers = db.execute_query(
            """SELECT ta.*, q.question_text, q.correct_answer as actual_correct, q.explanation,
                      q.option_a, q.option_b, q.option_c, q.option_d
               FROM test_answers ta
               JOIN questions q ON ta.question_id = q.id
               WHERE ta.test_result_id = ?""",
            (result_id,)
        )
        
        return {
            "result": dict(result[0]),
            "answers": [dict(a) for a in answers]
        }
