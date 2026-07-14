"""Groq API Service for generating questions - FAST & FREE"""

import json
from typing import List, Dict, Optional, Generator
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import GROQ_API_KEY, GROQ_MODEL, QUESTIONS_PER_PAPER, PAPERS_PER_GENERATION

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("Warning: groq package not installed. Install with: pip install groq")


class GroqLLMService:
    """Service for LLM operations using Groq API - FASTEST"""

    def __init__(self):
        if not GROQ_AVAILABLE:
            raise ImportError("Groq client not installed")
        
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL
        self.batch_size = 5  # Generate 5 questions at a time

    def check_connection(self) -> bool:
        """Check if Groq API is accessible"""
        try:
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
            print(f"Error connecting to Groq: {e}")
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
                       paper_number: int, batch_number: int, num_questions: int = 5, custom_prompt: str = None) -> str:
        """Generate a prompt for Groq to create diverse, complex MCQs"""
        
        if custom_prompt:
            # Use custom prompt if provided, but append JSON formatting requirements
            return f"""{custom_prompt}

REQUIRED OUTPUT FORMAT:
Return a JSON object with a single key "questions" containing a list of {num_questions} questions.
Each question must have:
- question_text
- options (A, B, C, D)
- correct_answer (A, B, C, or D)
- explanation
- difficulty (Easy, Medium, Hard)
- question_type (word_problem, complex, conceptual, application)

Batch {batch_number}
"""

        prompt = f"""You are an expert educator creating diverse, challenging multiple-choice questions for Grade {grade} students.

Generate exactly {num_questions} UNIQUE, VARIED MCQ questions for: {subject} - {topic}
Paper #{paper_number}, Batch {batch_number}

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

Return ONLY valid JSON in this exact format (NO markdown, NO extra text):
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

    def generate_questions(self, grade: str, subject: str, topic: str, 
                          paper_number: int) -> Optional[Dict]:
        """Generate questions using Groq API"""
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
                            print(f" ⚡ OK ({len(valid_questions)} valid)")
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
        papers = []
        
        for paper_num in range(1, PAPERS_PER_GENERATION + 1):
            print(f"Generating paper {paper_num}/{PAPERS_PER_GENERATION}...")
            questions_data = self.generate_questions(grade, subject, topic, paper_num)
            
            if questions_data:
                papers.append(questions_data)
                print(f"Paper {paper_num} ✅ generated with {len(questions_data['questions'])} questions")
            else:
                print(f"Failed to generate paper {paper_num}")
        
        return papers

    def generate_text(self, prompt: str) -> Optional[str]:
        """Generate generic text response from Groq"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Groq Text Gen Error: {e}")
            return None

    def generate_stream(self, prompt: str) -> Generator[str, None, None]:
        """Generate streaming text from Groq"""
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful and enthusiastic teacher for kids."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"Groq stream error: {e}")
            # Fallback to non-streaming
            text = self.generate_text(prompt)
            if text:
                yield text
