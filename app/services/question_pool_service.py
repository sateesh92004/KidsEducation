"""Question Pool Service - Manages question pools and user tracking"""

import os
import json
import random
from typing import List, Dict, Set, Tuple
from datetime import datetime
from difflib import SequenceMatcher
from utils.constants import BASE_DATA_PATH, QUESTIONS_PER_TEST


class QuestionPoolService:
    """
    Service for managing question pools with duplicate detection
    and user question tracking
    """
    
    def __init__(self):
        self.user_tracking_file = os.path.join(BASE_DATA_PATH, "user_questions.json")
        self._ensure_tracking_file()
    
    def _ensure_tracking_file(self):
        """Ensure user tracking file exists"""
        if not os.path.exists(self.user_tracking_file):
            os.makedirs(BASE_DATA_PATH, exist_ok=True)
            with open(self.user_tracking_file, 'w') as f:
                json.dump({}, f)
    
    def _load_user_tracking(self) -> Dict:
        """Load user question tracking data"""
        try:
            with open(self.user_tracking_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_user_tracking(self, data: Dict):
        """Save user question tracking data"""
        with open(self.user_tracking_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _get_topic_key(self, grade: str, subject: str, topic: str) -> str:
        """Generate a unique key for a topic"""
        return f"{grade}_{subject}_{topic.replace(' ', '_')}"
    
    def check_duplicate_questions(self, questions: List[Dict], similarity_threshold: float = 0.85) -> Tuple[List[Dict], List[str]]:
        """
        Check for duplicate questions using text similarity
        Returns: (unique_questions, duplicate_report)
        """
        unique_questions = []
        duplicates_found = []
        seen_texts = []
        
        for i, q in enumerate(questions):
            q_text = q.get('question_text', '').lower().strip()
            is_duplicate = False
            
            # Check against all previously seen questions
            for j, seen_text in enumerate(seen_texts):
                similarity = self._text_similarity(q_text, seen_text)
                
                if similarity >= similarity_threshold:
                    is_duplicate = True
                    duplicates_found.append(
                        f"Question {i+1} is {similarity*100:.1f}% similar to Question {j+1}"
                    )
                    break
            
            if not is_duplicate:
                unique_questions.append(q)
                seen_texts.append(q_text)
        
        return unique_questions, duplicates_found
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def get_answered_questions(self, username: str, grade: str, subject: str, topic: str) -> Set[int]:
        """Get set of question numbers that user has already answered"""
        tracking_data = self._load_user_tracking()
        topic_key = self._get_topic_key(grade, subject, topic)
        
        if username not in tracking_data:
            return set()
        
        if topic_key not in tracking_data[username]:
            return set()
        
        return set(tracking_data[username][topic_key].get('answered_questions', []))
    
    def mark_questions_as_answered(self, username: str, grade: str, subject: str, 
                                   topic: str, question_numbers: List[int]):
        """Mark questions as answered by user"""
        tracking_data = self._load_user_tracking()
        topic_key = self._get_topic_key(grade, subject, topic)
        
        # Initialize user data if needed
        if username not in tracking_data:
            tracking_data[username] = {}
        
        if topic_key not in tracking_data[username]:
            tracking_data[username][topic_key] = {
                'answered_questions': [],
                'tests_taken': 0,
                'last_test_date': None
            }
        
        # Add new answered questions
        current_answered = set(tracking_data[username][topic_key]['answered_questions'])
        current_answered.update(question_numbers)
        tracking_data[username][topic_key]['answered_questions'] = sorted(list(current_answered))
        
        # Update metadata
        tracking_data[username][topic_key]['tests_taken'] += 1
        tracking_data[username][topic_key]['last_test_date'] = datetime.now().isoformat()
        
        self._save_user_tracking(tracking_data)
    
    def get_available_questions(self, all_questions: List[Dict], username: str, 
                               grade: str, subject: str, topic: str) -> List[Dict]:
        """
        Get questions that user hasn't answered yet
        """
        answered_q_numbers = self.get_answered_questions(username, grade, subject, topic)
        
        available = [
            q for q in all_questions 
            if q.get('question_number') not in answered_q_numbers
        ]
        
        return available
    
    def select_test_questions(self, all_questions: List[Dict], username: str,
                             grade: str, subject: str, topic: str) -> Tuple[List[Dict], str]:
        """
        Select QUESTIONS_PER_TEST random questions from unused pool
        Returns: (selected_questions, error_message)
        """
        available = self.get_available_questions(all_questions, username, grade, subject, topic)
        
        if len(available) < QUESTIONS_PER_TEST:
            return [], f"Not enough questions available. You need {QUESTIONS_PER_TEST} questions but only {len(available)} are unused. Please ask your admin to generate more questions."
        
        # Randomly select QUESTIONS_PER_TEST questions
        selected = random.sample(available, QUESTIONS_PER_TEST)
        
        # Sort by question number for consistent display
        selected.sort(key=lambda x: x.get('question_number', 0))
        
        return selected, ""
    
    def get_user_stats(self, username: str, grade: str, subject: str, topic: str) -> Dict:
        """Get statistics about user's progress on a topic"""
        tracking_data = self._load_user_tracking()
        topic_key = self._get_topic_key(grade, subject, topic)
        
        if username not in tracking_data or topic_key not in tracking_data[username]:
            return {
                'questions_answered': 0,
                'tests_taken': 0,
                'last_test_date': None
            }
        
        user_topic_data = tracking_data[username][topic_key]
        
        return {
            'questions_answered': len(user_topic_data.get('answered_questions', [])),
            'tests_taken': user_topic_data.get('tests_taken', 0),
            'last_test_date': user_topic_data.get('last_test_date')
        }
    
    def reset_user_progress(self, username: str, grade: str, subject: str, topic: str):
        """Reset user's progress for a specific topic (admin function)"""
        tracking_data = self._load_user_tracking()
        topic_key = self._get_topic_key(grade, subject, topic)
        
        if username in tracking_data and topic_key in tracking_data[username]:
            del tracking_data[username][topic_key]
            self._save_user_tracking(tracking_data)
            return True
        
        return False
