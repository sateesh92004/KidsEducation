"""Database Question Service - Manages questions and user tracking"""

from typing import List, Dict, Tuple, Optional
from database.db_manager import db
import json

class DBQuestionService:
    """Service for managing questions in SQLite database"""
    
    def save_question(self, question_data: Dict) -> int:
        """Save a single question to database"""
        try:
            # Check for duplicates (same grade, subject, topic, question text)
            existing = db.execute_query(
                """SELECT id FROM questions 
                   WHERE grade = ? AND subject = ? AND topic = ? AND question_text = ?""",
                (question_data['grade'], question_data['subject'], 
                 question_data['topic'], question_data['question_text'])
            )
            
            if existing:
                return existing[0]['id']
            
            # Insert new question
            question_id = db.execute_insert(
                """INSERT INTO questions 
                   (grade, subject, topic, question_text, option_a, option_b, option_c, option_d, 
                    correct_answer, explanation, difficulty, question_type, generated_by)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    question_data['grade'],
                    question_data['subject'],
                    question_data['topic'],
                    question_data['question_text'],
                    question_data['options']['A'],
                    question_data['options']['B'],
                    question_data['options']['C'],
                    question_data['options']['D'],
                    question_data['correct_answer'],
                    question_data.get('explanation', ''),
                    question_data.get('difficulty', 'Medium'),
                    question_data.get('question_type', 'conceptual'),
                    question_data.get('generated_by', 'system')
                )
            )
            return question_id
        except Exception as e:
            print(f"Error saving question: {e}")
            return -1

    def save_bulk_questions(self, questions_list: List[Dict]) -> int:
        """Save multiple questions at once"""
        count = 0
        for q in questions_list:
            if self.save_question(q) > 0:
                count += 1
        return count

    def get_test_questions_for_user(self, user_id: int, grade: str, subject: str, topic: str, limit: int = 20) -> Tuple[List[Dict], str]:
        """
        Get unused questions for a specific user.
        Returns (questions_list, error_message)
        """
        query = """
            SELECT q.* 
            FROM questions q
            LEFT JOIN user_answered_questions uaq ON q.id = uaq.question_id AND uaq.user_id = ?
            WHERE q.grade = ? AND q.subject = ? AND q.topic = ?
            AND uaq.id IS NULL
            ORDER BY RANDOM()
            LIMIT ?
        """
        
        questions = db.execute_query(query, (user_id, grade, subject, topic, limit))
        
        if len(questions) < limit:
            total_available = len(questions)
            return [], f"Not enough new questions available. Found {total_available}, needed {limit}. Please ask admin to generate more questions."
            
        # Format questions for UI
        formatted_questions = []
        for q in questions:
            formatted_questions.append({
                "id": q['id'],
                "question_number": len(formatted_questions) + 1,
                "question_text": q['question_text'],
                "options": {
                    "A": q['option_a'],
                    "B": q['option_b'],
                    "C": q['option_c'],
                    "D": q['option_d']
                },
                "correct_answer": q['correct_answer'],
                "explanation": q['explanation'],
                "difficulty": q['difficulty'],
                "question_type": q['question_type']
            })
            
        return formatted_questions, ""

    def mark_questions_as_answered(self, user_id: int, question_ids: List[int]):
        """Mark questions as answered by user"""
        for q_id in question_ids:
            try:
                db.execute_insert(
                    "INSERT OR IGNORE INTO user_answered_questions (user_id, question_id) VALUES (?, ?)",
                    (user_id, q_id)
                )
            except Exception as e:
                print(f"Error marking question {q_id} as answered: {e}")

    def get_topic_stats(self, grade: str, subject: str, topic: str) -> Dict:
        """Get statistics for a topic (total questions, etc)"""
        result = db.execute_query(
            "SELECT COUNT(*) as count FROM questions WHERE grade = ? AND subject = ? AND topic = ?",
            (grade, subject, topic)
        )
        return {"total_questions": result[0]['count'] if result else 0}

    def get_available_topics(self, grade: str, subject: str) -> List[str]:
        """Get list of topics that have questions for this grade/subject"""
        results = db.execute_query(
            "SELECT DISTINCT topic FROM questions WHERE grade = ? AND subject = ? ORDER BY topic",
            (grade, subject)
        )
        return [r['topic'] for r in results]
