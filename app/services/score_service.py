"""Score Calculation and Storage Service"""

from utils.excel_handler import ExcelHandler
from services.question_service import QuestionService


class ScoreService:
    """Service for managing test scores"""

    def __init__(self):
        self.question_service = QuestionService()

    def calculate_score(self, grade: str, subject: str, topic: str, paper_num: int,
                       user_answers: dict) -> dict:
        """
        Calculate score for a test
        Returns detailed result with score percentage and correct answers count
        """
        result = self.question_service.validate_answers(
            grade, subject, topic, paper_num, user_answers
        )
        return result

    def save_score(self, username: str, grade: str, subject: str, topic: str,
                   paper_num: int, total_questions: int, correct_answers: int) -> bool:
        """
        Save test score to Excel
        """
        return ExcelHandler.save_test_result(
            username, grade, subject, topic, paper_num, total_questions, correct_answers
        )

    def process_and_save_test(self, username: str, grade: str, subject: str, topic: str,
                             paper_num: int, user_answers: dict) -> dict:
        """
        Process test answers, calculate score, and save result
        """
        # Calculate score
        score_result = self.calculate_score(grade, subject, topic, paper_num, user_answers)
        
        if "error" in score_result:
            return {"success": False, "message": score_result["error"]}
        
        # Save result to Excel
        save_success = self.save_score(
            username,
            grade,
            subject,
            topic,
            paper_num,
            score_result["total_questions"],
            score_result["correct_answers"]
        )
        
        if save_success:
            return {
                "success": True,
                "message": f"Test completed! Your score: {score_result['score_percentage']:.2f}%",
                "score_percentage": score_result["score_percentage"],
                "correct_answers": score_result["correct_answers"],
                "total_questions": score_result["total_questions"],
                "details": score_result["details"]
            }
        else:
            return {"success": False, "message": "Failed to save test result"}