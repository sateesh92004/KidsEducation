"""Question Service - Manages question retrieval and validation"""

from typing import Dict, List, Optional
from services.db_question_service import DBQuestionService
from services.paper_generation_agent import PaperGenerationAgent
from services.db_user_service import DBUserService

class QuestionService:
    """Service for managing questions using Database"""

    def __init__(self):
        self.db_service = DBQuestionService()
        self.paper_agent = PaperGenerationAgent()
        self.user_service = DBUserService()

    def generate_questions(self, grade: str, subject: str, topic: str) -> bool:
        """Generate questions using the agent (which saves to DB)"""
        papers = self.paper_agent.generate_papers_parallel(grade, subject, topic)
        return len(papers) > 0

    def get_test_questions_for_user(self, username: str, grade: str, subject: str, topic: str) -> Dict:
        """
        Get 20 unique questions for a user from the database
        """
        user = self.user_service.get_user_by_username(username)
        if not user:
            return {"error": "User not found"}
            
        questions, error = self.db_service.get_test_questions_for_user(
            user['id'], grade, subject, topic, limit=20
        )
        
        if error:
            return {"error": error}
            
        return {
            "questions": questions,
            "paper_number": 1,  # Legacy field
            "total_questions": len(questions)
        }

    def mark_questions_answered(self, username: str, grade: str, subject: str, topic: str, question_ids: List[int]):
        """Mark questions as answered by user"""
        user = self.user_service.get_user_by_username(username)
        if user:
            self.db_service.mark_questions_as_answered(user['id'], question_ids)

    def validate_answers(self, questions: List[Dict], user_answers: Dict[int, str]) -> Dict:
        """
        Validate user answers against the provided question objects.
        questions: List of question dicts (must contain 'id', 'question_number', 'correct_answer')
        user_answers: Dict of {question_number: selected_option}
        """
        result = {
            "total_questions": len(user_answers),
            "correct_answers": 0,
            "wrong_answers": 0,
            "score_percentage": 0,
            "details": []
        }
        
        # Create a map of question_number -> question object
        q_map = {q['question_number']: q for q in questions}
        
        for q_num, user_ans in user_answers.items():
            question = q_map.get(q_num)
            if not question:
                continue
                
            correct_ans = question.get('correct_answer')
            is_correct = user_ans == correct_ans
            
            if is_correct:
                result["correct_answers"] += 1
            else:
                result["wrong_answers"] += 1
                
            result["details"].append({
                "id": question.get('id'),  # Important for DB saving
                "question_number": q_num,
                "user_answer": user_ans,
                "correct_answer": correct_ans,
                "is_correct": is_correct,
                "explanation": question.get('explanation', '')
            })
            
        if result["total_questions"] > 0:
            result["score_percentage"] = (result["correct_answers"] / result["total_questions"]) * 100
            
        return result

    def get_available_topics(self, grade: str, subject: str) -> List[str]:
        """Get available topics from DB"""
        return self.db_service.get_available_topics(grade, subject)

    def get_available_papers(self, grade: str, subject: str, topic: str) -> List[int]:
        """
        Check if questions exist for this topic.
        Returns [1] if questions exist, [] otherwise.
        This mimics the old 'papers' behavior for compatibility.
        """
        stats = self.db_service.get_topic_stats(grade, subject, topic)
        if stats['total_questions'] > 0:
            return [1] # Return a dummy paper list so UI thinks papers exist
        return []