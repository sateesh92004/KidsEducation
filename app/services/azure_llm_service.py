"""Azure OpenAI / Microsoft Copilot Service for generating questions"""

import json
import re
from typing import List, Dict, Optional
from utils.constants import (
    AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, 
    AZURE_DEPLOYMENT_NAME, AZURE_API_VERSION, QUESTIONS_PER_PAPER
)

try:
    from openai import AzureOpenAI
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False
    print("Warning: openai package not installed. Install with: pip install openai")


class AzureLLMService:
    """Service for LLM operations using Azure OpenAI / Microsoft Copilot"""

    def __init__(self):
        if not AZURE_AVAILABLE:
            raise ImportError("Azure OpenAI client not installed")
        
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
        self.model = AZURE_DEPLOYMENT_NAME
        self.batch_size = 5  # Generate 5 questions at a time

    def check_connection(self) -> bool:
        """Check if Azure OpenAI is accessible"""
        try:
            # Test with a simple request
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say hello"}
                ],
                max_tokens=10,
                temperature=0.5
            )
            return response.choices[0].message.content is not None
        except Exception as e:
            print(f"Error connecting to Azure OpenAI: {e}")
            return False

    def parse_json_response(self, json_str: str) -> Optional[Dict]:
        """Safely parse JSON response"""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Try to extract JSON from text
            try:
                start_idx = json_str.find('{')
                end_idx = json_str.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    extracted = json_str[start_idx:end_idx]
                    return json.loads(extracted)
            except:
                pass
        return None

    def generate_prompt(self, grade: str, subject: str, topic: str, 
                       paper_number: int, batch_number: int, num_questions: int = 5) -> str:
        """Generate a prompt for GPT-4 to create MCQs"""
        prompt = f"""You are an expert educator creating multiple-choice questions for Grade {grade} students.

Generate exactly {num_questions} UNIQUE MCQ questions for: {subject} - {topic}
Paper #{paper_number}, Section {batch_number}

CRITICAL: Each question must be COMPLETELY DIFFERENT from others. Vary:
- Topics within {topic}
- Question types (definition, application, problem-solving, analysis)
- Difficulty levels
- Real-world scenarios and examples

For each question, provide:
1. Clear, age-appropriate question text
2. Four distinct options (A, B, C, D)
3. One correct answer
4. Brief explanation of why the answer is correct

Return ONLY valid JSON in this exact format (NO markdown, NO extra text):
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
            "explanation": "Why A is correct"
        }}
    ]
}}

Generate {num_questions} unique questions now:"""
        return prompt

    def generate_questions(self, grade: str, subject: str, topic: str, 
                          paper_number: int) -> Optional[Dict]:
        """Generate questions using Azure OpenAI"""
        try:
            all_questions = []
            num_batches = (QUESTIONS_PER_PAPER + self.batch_size - 1) // self.batch_size
            
            for batch_num in range(1, num_batches + 1):
                remaining = QUESTIONS_PER_PAPER - len(all_questions)
                batch_questions = min(self.batch_size, remaining)
                
                print(f"  Batch {batch_num}/{num_batches} ({batch_questions} questions)...", end="", flush=True)
                
                prompt = self.generate_prompt(grade, subject, topic, paper_number, batch_num, batch_questions)
                
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {
                                "role": "system",
                                "content": "You are an expert teacher creating educational multiple-choice questions. Always respond with valid JSON only."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.7,
                        max_tokens=2000,
                        top_p=0.95
                    )
                    
                    generated_text = response.choices[0].message.content
                    batch_data = self.parse_json_response(generated_text)
                    
                    if batch_data and "questions" in batch_data:
                        batch_questions_list = batch_data["questions"]
                        
                        # Reindex and validate
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
        from utils.constants import PAPERS_PER_GENERATION
        
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
