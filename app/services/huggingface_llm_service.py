"""HuggingFace Inference API Service - Free LLM access"""

import os
import json
import requests
from typing import Dict, Optional
from utils.constants import QUESTIONS_PER_PAPER


class HuggingFaceLLMService:
    """
    Service for generating questions using HuggingFace Inference API
    Free tier available with various open-source models
    """
    
    def __init__(self):
        # Get API key from environment variable
        self.api_key = os.getenv('HUGGINGFACE_API_KEY', '')
        self.base_url = "https://api-inference.huggingface.co/models"
        
        # HuggingFace models (free inference)
        self.model = "mistralai/Mistral-7B-Instruct-v0.2"
        # Alternatives: 
        # - "meta-llama/Llama-2-7b-chat-hf"
        # - "HuggingFaceH4/zephyr-7b-beta"
        
        self.batch_size = 5  # Smaller batches for free tier
        self.timeout = 120
    
    def check_connection(self) -> bool:
        """Check if HuggingFace API is accessible and API key is valid"""
        if not self.api_key:
            print("    ⚠️  HUGGINGFACE_API_KEY not set in environment")
            return False
        
        try:
            # Test with a simple request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}/{self.model}"
            
            response = requests.post(
                url,
                headers=headers,
                json={"inputs": "test", "parameters": {"max_new_tokens": 10}},
                timeout=15
            )
            
            # HuggingFace returns 200 even for loading models
            return response.status_code in [200, 503]  # 503 means model is loading
        except Exception as e:
            print(f"    Error: {str(e)[:50]}")
            return False
    
    def generate_prompt(self, grade: str, subject: str, topic: str, 
                       paper_number: int, num_questions: int) -> str:
        """Generate prompt for HuggingFace"""
        prompt = f"""[INST] You are an expert educator creating multiple-choice questions for Grade {grade} students.

Generate exactly {num_questions} UNIQUE MCQ questions for: {subject} - {topic}
Paper #{paper_number}

REQUIREMENTS:
1. Each question must be COMPLETELY DIFFERENT
2. Vary difficulty levels
3. Age-appropriate for Grade {grade}
4. Four options (A, B, C, D)
5. One correct answer
6. Brief explanation

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question_number": 1,
            "question_text": "What is 5 + 3?",
            "options": {{
                "A": "6",
                "B": "8",
                "C": "7",
                "D": "9"
            }},
            "correct_answer": "B",
            "explanation": "5 + 3 = 8"
        }}
    ]
}}

Generate {num_questions} questions: [/INST]"""
        return prompt
    
    def parse_json_from_response(self, text: str) -> Optional[Dict]:
        """Extract and parse JSON from response"""
        try:
            # Try direct parsing
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Remove instruction tags
        text = text.replace('[INST]', '').replace('[/INST]', '').strip()
        
        # Try to extract JSON block
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                json_str = text[start:end]
                # Clean up common issues
                json_str = json_str.replace('\n', ' ').replace('\r', '')
                return json.loads(json_str)
        except Exception:
            pass
        
        return None
    
    def generate_question_paper(self, grade: str, subject: str, topic: str, 
                          paper_number: int, custom_prompt: str = None) -> Optional[Dict]:
        """Generate questions using HuggingFace API"""
        try:
            if not self.api_key:
                print("      ⚠️  HuggingFace API key not configured")
                return None
            
            all_questions = []
            num_batches = (QUESTIONS_PER_PAPER + self.batch_size - 1) // self.batch_size
            
            for batch_num in range(1, num_batches + 1):
                remaining = QUESTIONS_PER_PAPER - len(all_questions)
                batch_questions = min(self.batch_size, remaining)
                
                prompt = self.generate_prompt(grade, subject, topic, paper_number, batch_questions)
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                url = f"{self.base_url}/{self.model}"
                
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 2000,
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "do_sample": True,
                        "return_full_text": False
                    },
                    "options": {
                        "wait_for_model": True  # Wait if model is loading
                    }
                }
                
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # HuggingFace returns array of results
                    if isinstance(result, list) and len(result) > 0:
                        content = result[0].get('generated_text', '')
                        
                        batch_data = self.parse_json_from_response(content)
                        
                        if batch_data and 'questions' in batch_data:
                            questions = batch_data['questions']
                            
                            # Reindex and validate
                            for i, q in enumerate(questions):
                                if self._validate_question(q):
                                    q['question_number'] = len(all_questions) + 1
                                    all_questions.append(q)
                                    
                                    if len(all_questions) >= QUESTIONS_PER_PAPER:
                                        break
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    print(f"      Model loading, waiting...")
                    import time
                    time.sleep(20)
                    continue
                else:
                    print(f"      HTTP {response.status_code}: {response.text[:100]}")
                    return None
            
            # Create paper structure
            if len(all_questions) >= QUESTIONS_PER_PAPER * 0.8:  # At least 80%
                return {
                    "paper_number": paper_number,
                    "grade": grade,
                    "subject": subject,
                    "topic": topic,
                    "questions": all_questions[:QUESTIONS_PER_PAPER],
                    "generated_by": "huggingface",
                    "model": self.model
                }
            
            return None
            
        except Exception as e:
            print(f"      HuggingFace Error: {str(e)[:100]}")
            return None
    
    def _validate_question(self, question: Dict) -> bool:
        """Validate question structure"""
        required_fields = ['question_text', 'options', 'correct_answer']
        if not all(field in question for field in required_fields):
            return False
        
        options = question.get('options', {})
        if not all(opt in options for opt in ['A', 'B', 'C', 'D']):
            return False
        
        if question.get('correct_answer') not in ['A', 'B', 'C', 'D']:
            return False
        
        return True

    def generate_text(self, prompt: str) -> Optional[str]:
        """Generate generic text response from HuggingFace"""
        try:
            if not self.api_key:
                print("      ⚠️  HuggingFace API key not configured")
                return None
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}/{self.model}"
            
            # Format prompt for Mistral
            formatted_prompt = f"[INST] {prompt} [/INST]"
            
            payload = {
                "inputs": formatted_prompt,
                "parameters": {
                    "max_new_tokens": 2000,
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "do_sample": True,
                    "return_full_text": False
                },
                "options": {
                    "wait_for_model": True
                }
            }
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '')
            else:
                print(f"HuggingFace API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"HuggingFace Text Gen Error: {e}")
            return None
