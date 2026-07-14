"""Google Gemini LLM Service - High quality question generation"""

import os
import json
import requests
from typing import Dict, Optional
from utils.constants import QUESTIONS_PER_PAPER


class GeminiLLMService:
    """
    Service for generating questions using Google Gemini API
    Gemini provides high-quality responses with generous free tier
    """
    
    def __init__(self):
        # Get API key from environment variable
        self.api_key = os.getenv('GEMINI_API_KEY', '')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        
        # Gemini models
        self.model = "gemini-1.5-flash"  # Fast and free
        # Alternative: "gemini-1.5-pro" for higher quality
        
        self.batch_size = 10  # Gemini can handle larger batches
        self.timeout = 90
    
    def check_connection(self) -> bool:
        """Check if Gemini API is accessible and API key is valid"""
        if not self.api_key:
            print("    ⚠️  GEMINI_API_KEY not set in environment")
            return False
        
        try:
            # Test with a simple request
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{"text": "test"}]
                    }]
                },
                timeout=10
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"    Error: {str(e)[:50]}")
            return False
    
    def generate_prompt(self, grade: str, subject: str, topic: str, 
                       paper_number: int, num_questions: int) -> str:
        """Generate prompt for Gemini to create diverse, complex MCQs"""
        prompt = f"""You are an expert educator creating diverse, challenging multiple-choice questions for Grade {grade} students.

Generate exactly {num_questions} UNIQUE, VARIED MCQ questions for: {subject} - {topic}
Paper #{paper_number}

CRITICAL REQUIREMENTS FOR QUESTION VARIETY:

1. QUESTION TYPES (Mix these):
   - Word Problems (40%): Real-world scenarios requiring multi-step thinking
   - Complex Problems (30%): Require calculation, analysis, or reasoning
   - Conceptual Questions (20%): Understanding of concepts
   - Application Questions (10%): Apply knowledge to new situations

2. DIFFICULTY LEVELS (Vary across):
   - Easy (20%): Direct recall or simple application
   - Medium (50%): Requires thinking and problem-solving
   - Hard (30%): Multi-step, complex reasoning, or word problems

3. WORD PROBLEM EXAMPLES:
   - Shopping scenarios with money calculations
   - Time and distance problems
   - Measurement and comparison problems
   - Real-life situations students can relate to
   - Problems requiring multiple steps to solve

4. COMPLEXITY REQUIREMENTS:
   - Include problems that require students to:
     * Read carefully and extract information
     * Perform calculations or logical reasoning
     * Apply concepts to solve real problems
     * Think critically before answering
   - Avoid simple, direct questions
   - Make students work to find the answer

5. UNIQUENESS:
   - Each question must be COMPLETELY DIFFERENT
   - Vary contexts, numbers, scenarios
   - No repetitive patterns
   - Different aspects of {topic}

EXAMPLE FORMATS:

Word Problem:
"Sarah has 24 apples. She wants to divide them equally among 6 friends. How many apples will each friend get?"

Complex Problem:
"A rectangle has a length of 12 cm and width of 8 cm. If you double the length and keep the width same, what is the new area?"

For each question, provide:
1. Clear, age-appropriate question text (make it a story/scenario when possible)
2. Four distinct, plausible options (A, B, C, D)
3. One correct answer
4. Detailed explanation showing the solution steps

Return ONLY valid JSON in this exact format (no markdown, no code blocks):
{{
    "questions": [
        {{
            "question_number": 1,
            "question_text": "A detailed word problem or complex question here?",
            "options": {{
                "A": "First option",
                "B": "Second option",
                "C": "Third option",
                "D": "Fourth option"
            }},
            "correct_answer": "A",
            "explanation": "Step-by-step explanation of how to solve this"
        }}
    ]
}}

Generate {num_questions} unique questions now:"""
        return prompt
    
    def parse_json_from_response(self, text: str) -> Optional[Dict]:
        """Extract and parse JSON from response"""
        try:
            # Try direct parsing
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Remove markdown code blocks if present
        text = text.replace('```json', '').replace('```', '').strip()
        
        # Try to extract JSON block
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except Exception:
            pass
        
        return None
    
    def generate_question_paper(self, grade: str, subject: str, topic: str, paper_number: int, custom_prompt: str = None) -> Optional[Dict]:
        """Generate a complete question paper"""
        try:
            if not self.api_key:
                print("      ⚠️  Gemini API key not configured")
                return None
            
            questions = []
            
            # Calculate number of batches needed
            num_batches = QUESTIONS_PER_PAPER // self.batch_size
            
            print(f"  [GEMINI] Generating {QUESTIONS_PER_PAPER} questions in {num_batches} batches...")
            
            for i in range(num_batches):
                batch_prompt = self.generate_prompt(grade, subject, topic, paper_number, self.batch_size, custom_prompt)
                
                try:
                    url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
                    
                    response = requests.post(
                        url,
                        headers={"Content-Type": "application/json"},
                        json={
                            "contents": [{
                                "parts": [{"text": batch_prompt}]
                            }],
                            "generationConfig": {
                                "temperature": 0.7,
                                "response_mime_type": "application/json"
                            }
                        },
                        timeout=self.timeout
                    )
                    
                    if response.status_code != 200:
                        print(f"    Batch {i+1}/{num_batches} Error: {response.status_code} - {response.text[:100]}")
                        continue
                        
                    result = response.json()
                    
                    # Extract text content
                    content = ""
                    try:
                        content = result['candidates'][0]['content']['parts'][0]['text']
                    except (KeyError, IndexError):
                        print(f"    Batch {i+1}/{num_batches}: Unexpected response format")
                        continue
                    
                    data = self.parse_json_from_response(content)
                    
                    if data and "questions" in data:
                        batch_questions = data["questions"]
                        # Add batch info
                        for q in batch_questions:
                            q["generated_by"] = "gemini"
                        questions.extend(batch_questions)
                        print(f"    Batch {i+1}/{num_batches}: Generated {len(batch_questions)} questions")
                    else:
                        print(f"    Batch {i+1}/{num_batches}: Failed to parse JSON")
                        
                except Exception as e:
                    print(f"    Batch {i+1}/{num_batches} Error: {e}")
                    
            if not questions:
                return None
                
            return {
                "grade": grade,
                "subject": subject,
                "topic": topic,
                "paper_number": paper_number,
                "generated_by": "gemini",
                "questions": questions
            }
            
        except Exception as e:
            print(f"      Gemini Error: {str(e)[:100]}")
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
        """Generate generic text response from Gemini"""
        try:
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.7}
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"Gemini API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Gemini Text Gen Error: {e}")
            return None
