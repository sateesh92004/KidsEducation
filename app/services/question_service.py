"""Question Management Service"""

import os
import json
from typing import List, Dict, Tuple
from utils.excel_handler import ExcelHandler
from utils.constants import BASE_DATA_PATH, QUESTIONS_PER_PAPER
from services.llm_service import LLMService


class QuestionService:
    """Service for managing questions and papers"""

    def __init__(self):
        self.llm_service = LLMService()

    def get_question_paper_filename(self, grade: str, subject: str, topic: str, paper_num: int) -> str:
        """Get filename for a question paper"""
        safe_topic = topic.replace(" ", "_").replace("/", "_")
        return f"paper_{grade}_{subject}_{safe_topic}_p{paper_num}.json"

    def get_answer_key_filename(self, grade: str, subject: str, topic: str, paper_num: int) -> str:
        """Get filename for answer key"""
        safe_topic = topic.replace(" ", "_").replace("/", "_")
        return f"answers_{grade}_{subject}_{safe_topic}_p{paper_num}.json"

    def save_paper_to_json(self, grade: str, subject: str, topic: str, questions_data: Dict) -> Tuple[bool, str]:
        """Save generated question paper to JSON file"""
        try:
            os.makedirs(BASE_DATA_PATH, exist_ok=True)
            
            paper_num = questions_data.get("paper_number", 1)
            filename = self.get_question_paper_filename(grade, subject, topic, paper_num)
            filepath = os.path.join(BASE_DATA_PATH, filename)
            
            with open(filepath, 'w') as f:
                json.dump(questions_data, f, indent=2)
            
            return True, filepath
        except Exception as e:
            return False, str(e)

    def save_answer_key(self, grade: str, subject: str, topic: str, questions_data: Dict) -> Tuple[bool, str]:
        """Extract and save answer key separately"""
        try:
            os.makedirs(BASE_DATA_PATH, exist_ok=True)
            
            paper_num = questions_data.get("paper_number", 1)
            filename = self.get_answer_key_filename(grade, subject, topic, paper_num)
            filepath = os.path.join(BASE_DATA_PATH, filename)
            
            # Extract answers only
            answer_key = {
                "paper_number": paper_num,
                "grade": grade,
                "subject": subject,
                "topic": topic,
                "answers": []
            }
            
            for q in questions_data.get("questions", []):
                answer_key["answers"].append({
                    "question_number": q.get("question_number"),
                    "correct_answer": q.get("correct_answer"),
                    "explanation": q.get("explanation", "")
                })
            
            with open(filepath, 'w') as f:
                json.dump(answer_key, f, indent=2)
            
            return True, filepath
        except Exception as e:
            return False, str(e)

    def generate_papers_for_topic(self, grade: str, subject: str, topic: str) -> Dict:
        """Generate multiple papers for a topic and save them"""
        result = {
            "success": False,
            "message": "",
            "papers_generated": 0,
            "papers": []
        }
        
        try:
            # Check Ollama connection
            if not self.llm_service.check_ollama_connection():
                result["message"] = "Error: Ollama is not running. Please start Ollama first."
                return result
            
            # Generate papers
            papers = self.llm_service.generate_multiple_papers(grade, subject, topic)
            
            if not papers:
                result["message"] = "Failed to generate question papers. Please try again."
                return result
            
            # Save papers and answer keys
            for paper_data in papers:
                if paper_data:
                    # Save paper
                    success, path = self.save_paper_to_json(grade, subject, topic, paper_data)
                    if not success:
                        continue
                    
                    # Save answer key
                    ans_success, ans_path = self.save_answer_key(grade, subject, topic, paper_data)
                    
                    if success and ans_success:
                        result["papers"].append({
                            "paper_number": paper_data.get("paper_number"),
                            "paper_path": path,
                            "answer_key_path": ans_path
                        })
                        result["papers_generated"] += 1
            
            if result["papers_generated"] > 0:
                result["success"] = True
                result["message"] = f"Successfully generated {result['papers_generated']} question papers!"
            else:
                result["message"] = "Failed to save generated papers."
            
            return result
        except Exception as e:
            result["message"] = f"Error: {str(e)}"
            return result

    def load_paper(self, grade: str, subject: str, topic: str, paper_num: int) -> Dict:
        """Load a question paper from JSON file"""
        try:
            filename = self.get_question_paper_filename(grade, subject, topic, paper_num)
            filepath = os.path.join(BASE_DATA_PATH, filename)
            
            if not os.path.exists(filepath):
                return None
            
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading paper: {e}")
            return None

    def load_answer_key(self, grade: str, subject: str, topic: str, paper_num: int) -> Dict:
        """Load answer key from JSON file"""
        try:
            filename = self.get_answer_key_filename(grade, subject, topic, paper_num)
            filepath = os.path.join(BASE_DATA_PATH, filename)
            
            if not os.path.exists(filepath):
                return None
            
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading answer key: {e}")
            return None

    def get_available_papers(self, grade: str, subject: str, topic: str) -> List[int]:
        """Get list of available paper numbers for a topic"""
        papers = []
        
        for i in range(1, 31):  # Check for up to 30 papers
            if self.load_paper(grade, subject, topic, i) is not None:
                papers.append(i)
            else:
                # If we reach 10+ without finding one, assume we're done
                if i > 10 and not papers:
                    break
        
        return papers

    def get_available_topics(self, grade: str, subject: str) -> List[str]:
        """Discover available topics by scanning saved papers"""
        topics = set()
        
        try:
            if not os.path.exists(BASE_DATA_PATH):
                return []
            
            # Scan all JSON files in the data directory
            for filename in os.listdir(BASE_DATA_PATH):
                if filename.startswith('paper_') and filename.endswith('.json'):
                    # Parse filename: paper_Grade_Subject_Topic_p1.json
                    parts = filename.replace('paper_', '').replace('.json', '').split('_')
                    
                    if len(parts) >= 3:
                        file_grade = parts[0]
                        file_subject = parts[1]
                        # Topic is everything except the last part (which is paper number pX)
                        file_topic = '_'.join(parts[2:-1]).replace('_', ' ')
                        
                        # Match grade and subject
                        if file_grade == grade and file_subject == subject:
                            if file_topic and self.get_available_papers(grade, subject, file_topic):
                                topics.add(file_topic)
            
            return sorted(list(topics))
        except Exception as e:
            print(f"Error discovering topics: {e}")
            return []

    def get_formatted_questions(self, grade: str, subject: str, topic: str, paper_num: int) -> List[Dict]:
        """Get questions formatted for display"""
        paper = self.load_paper(grade, subject, topic, paper_num)
        
        if not paper:
            return []
        
        formatted = []
        for q in paper.get("questions", []):
            formatted.append({
                "question_number": q.get("question_number"),
                "question_text": q.get("question_text"),
                "options": q.get("options", {}),
                "paper_num": paper_num
            })
        
        return formatted

    def validate_answers(self, grade: str, subject: str, topic: str, paper_num: int, 
                        user_answers: Dict[int, str]) -> Dict:
        """Validate user answers against answer key"""
        answer_key = self.load_answer_key(grade, subject, topic, paper_num)
        
        if not answer_key:
            return {"error": "Answer key not found"}
        
        result = {
            "total_questions": len(answer_key.get("answers", [])),
            "correct_answers": 0,
            "score_percentage": 0,
            "details": []
        }
        
        for ans in answer_key.get("answers", []):
            q_num = ans.get("question_number")
            correct_ans = ans.get("correct_answer")
            user_ans = user_answers.get(q_num)
            
            is_correct = user_ans == correct_ans
            if is_correct:
                result["correct_answers"] += 1
            
            result["details"].append({
                "question_number": q_num,
                "user_answer": user_ans,
                "correct_answer": correct_ans,
                "is_correct": is_correct,
                "explanation": ans.get("explanation", "")
            })
        
        result["score_percentage"] = (result["correct_answers"] / result["total_questions"]) * 100
        
        return result