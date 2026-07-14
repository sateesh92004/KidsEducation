"""LLM Service for generating questions using Ollama"""

import requests
import json
import re
from typing import List, Dict, Optional, Generator
from utils.constants import OLLAMA_BASE_URL, OLLAMA_MODEL, QUESTIONS_PER_PAPER, PAPERS_PER_GENERATION


class LLMService:
    """Service for LLM operations using Ollama"""

    def __init__(self):
        self.base_url = OLLAMA_BASE_URL
        self.model = OLLAMA_MODEL
        self.batch_size = 5  # 5 questions per batch for faster generation
        self.retry_attempts = 2  # Retry failed batches

    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            return False

    def clean_json_string(self, json_str: str) -> str:
        """Clean and fix common JSON formatting issues from LLM output"""
        # Remove leading/trailing whitespace
        json_str = json_str.strip()
        
        # Fix newlines within the JSON string - convert actual newlines to spaces
        json_str = re.sub(r'\n+', ' ', json_str)
        
        # Remove trailing commas before closing braces/brackets
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        
        # Fix escaped newlines and carriage returns
        json_str = json_str.replace('\\n', ' ')
        json_str = json_str.replace('\\r', ' ')
        json_str = json_str.replace('\\t', ' ')
        
        # Remove multiple spaces
        json_str = re.sub(r'\s+', ' ', json_str)
        
        return json_str

    def parse_json_response(self, json_str: str) -> Optional[Dict]:
        """Safely parse JSON response with multiple fallback strategies"""
        # Strategy 1: Direct parsing (assume it's clean)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Clean and retry
        try:
            cleaned = self.clean_json_string(json_str)
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            print(f"  Cleaning failed: {str(e)[:50]}")
            pass
        
        # Strategy 3: Try to manually extract and fix
        try:
            # Find the JSON block
            start_idx = json_str.find('{')
            end_idx = json_str.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                extracted = json_str[start_idx:end_idx + 1]
                cleaned = self.clean_json_string(extracted)
                return json.loads(cleaned)
        except Exception as e:
            print(f"  Extraction failed: {str(e)[:50]}")
            pass
        
        return None

    def generate_prompt(self, grade: str, subject: str, topic: str, paper_number: int, 
                       batch_number: int, num_questions: int = 5) -> str:
        """Generate a prompt for neural-chat to create MCQs"""
        prompt = f"""You are an expert educator creating multiple-choice questions for Grade {grade} students.

Generate exactly {num_questions} UNIQUE MCQ questions for: {subject} - {topic}
Paper #{paper_number}, Section {batch_number}

CRITICAL: Each question must be COMPLETELY DIFFERENT from others. Vary:
- Topics within {topic}
- Question types (definition, application, problem-solving, analysis)
- Difficulty levels
- Real-world scenarios

For each question, provide:
1. Clear, age-appropriate question text
2. Four distinct options (A, B, C, D)
3. One correct answer
4. Brief explanation of why the answer is correct

Return ONLY valid JSON in this exact format (no markdown, no explanation):
{{
    "questions": [
        {{
            "question_number": 1,
            "question_text": "Question here?",
            "options": {{
                "A": "First option",
                "B": "Second option", 
                "C": "Third option",
                "D": "Fourth option"
            }},
            "correct_answer": "A",
            "explanation": "Why A is correct and why others are wrong"
        }}
    ]
}}

Generate {num_questions} unique questions now:"""
        return prompt

    def generate_questions(self, grade: str, subject: str, topic: str, paper_number: int) -> Optional[Dict]:
        """Generate questions using Ollama (in batches for reliability)"""
        try:
            all_questions = []
            num_batches = (QUESTIONS_PER_PAPER + self.batch_size - 1) // self.batch_size
            
            for batch_num in range(1, num_batches + 1):
                # Calculate how many questions for this batch
                remaining = QUESTIONS_PER_PAPER - len(all_questions)
                batch_questions = min(self.batch_size, remaining)
                
                print(f"  Batch {batch_num}/{num_batches} ({batch_questions} questions)...", end="", flush=True)
                
                prompt = self.generate_prompt(grade, subject, topic, paper_number, batch_num, batch_questions)
                
                try:
                    response = requests.post(
                        f"{self.base_url}/api/generate",
                        json={
                            "model": self.model,
                            "prompt": prompt,
                            "stream": False,
                            "temperature": 0.6,  # Lower for faster responses
                            "top_p": 0.9,  # Good quality
                        },
                        timeout=120  # 2 minutes per batch for Mistral speed
                    )

                    if response.status_code == 200:
                        result = response.json()
                        generated_text = result.get("response", "")
                        
                        # Extract and parse JSON using robust method
                        json_start = generated_text.find("{")
                        json_end = generated_text.rfind("}") + 1
                        
                        if json_start != -1 and json_end > json_start:
                            json_str = generated_text[json_start:json_end]
                            batch_data = self.parse_json_response(json_str)
                            
                            if batch_data and "questions" in batch_data:
                                batch_questions_list = batch_data["questions"]
                                
                                # Reindex questions and validate
                                valid_questions = []
                                for i, q in enumerate(batch_questions_list):
                                    if isinstance(q, dict) and "question_text" in q and "options" in q:
                                        q["question_number"] = len(all_questions) + i + 1
                                        valid_questions.append(q)
                                
                                if valid_questions:
                                    all_questions.extend(valid_questions)
                                    print(f" OK ({len(valid_questions)} valid)")
                                else:
                                    print(" No valid questions")
                            else:
                                print(" Failed to parse JSON")
                        else:
                            print(" No JSON found")
                    else:
                        print(f" HTTP {response.status_code}")
                except requests.exceptions.Timeout:
                    print(" Timeout - retrying with longer wait...")
                    # Increase timeout for retry
                    import time
                    time.sleep(2)
                    continue
                except Exception as e:
                    print(f" Error: {str(e)[:50]}")
                    continue
            
            # Create final paper structure
            if all_questions:
                paper_data = {
                    "paper_number": paper_number,
                    "grade": grade,
                    "subject": subject,
                    "topic": topic,
                    "questions": all_questions
                }
                return paper_data
            else:
                print("  No questions generated")
                return None
                
        except Exception as e:
            print(f"  Critical Error: {str(e)[:50]}")
            return None

    def generate_multiple_papers(self, grade: str, subject: str, topic: str) -> List[Dict]:
        """Generate multiple question papers"""
        papers = []
        
        for paper_num in range(1, PAPERS_PER_GENERATION + 1):
            print(f"Generating paper {paper_num}/{PAPERS_PER_GENERATION}...")
            questions_data = self.generate_questions(grade, subject, topic, paper_num)
            
            if questions_data:
                papers.append(questions_data)
                print(f"Paper {paper_num} generated with {len(questions_data['questions'])} questions")
            else:
                print(f"Failed to generate paper {paper_num}")
        
        return papers

    def generate_text(self, prompt: str, model: str = None) -> Optional[str]:
        """Generate text using Ollama (non-streaming)"""
        try:
            use_model = model or self.model
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": use_model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                    "top_p": 0.9,
                },
                timeout=120
            )
            if response.status_code == 200:
                return response.json().get("response", "")
            return None
        except Exception as e:
            print(f"Ollama generate_text error: {e}")
            return None

    def generate_stream(self, prompt: str, model: str = None) -> Generator[str, None, None]:
        """Generate streaming text using Ollama"""
        try:
            use_model = model or self.model
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": use_model,
                    "prompt": prompt,
                    "stream": True,
                    "temperature": 0.7,
                    "top_p": 0.9,
                },
                timeout=120,
                stream=True
            )
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        chunk = data.get("response", "")
                        if chunk:
                            yield chunk
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            yield f"\n\n⚠️ Ollama error: {e}"
