"""Score Calculation and Storage Service"""

from services.db_test_service import DBTestService
from services.question_service import QuestionService
from services.db_user_service import DBUserService

class ScoreService:
    """Service for managing test scores"""

    def __init__(self):
        self.question_service = QuestionService()
        self.db_test_service = DBTestService()
        self.user_service = DBUserService()

    def process_and_save_test(self, username: str, grade: str, subject: str, topic: str,
                             questions: list, user_answers: dict) -> dict:
        """
        Process test answers, calculate score, and save result to DB
        """
        # 1. Validate answers
        score_result = self.question_service.validate_answers(questions, user_answers)
        
        # 2. Get user ID
        user = self.user_service.get_user_by_username(username)
        if not user:
            return {"success": False, "message": "User not found"}
            
        # 3. Save result to Database
        result_id = self.db_test_service.save_test_result(
            user['id'],
            grade,
            subject,
            topic,
            score_result["total_questions"],
            score_result["correct_answers"],
            score_result["wrong_answers"],
            score_result["details"]
        )
        
        if result_id > 0:
            return {
                "success": True,
                "message": f"Test completed! Your score: {score_result['score_percentage']:.2f}%",
                "score_percentage": score_result["score_percentage"],
                "correct_answers": score_result["correct_answers"],
                "wrong_answers": score_result["wrong_answers"],
                "total_questions": score_result["total_questions"],
                "details": score_result["details"]
            }
        else:
            return {"success": False, "message": "Failed to save test result"}