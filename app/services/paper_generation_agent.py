"""
Intelligent Paper Generation Agent
Automatically manages question paper generation using multiple LLM providers
with fallback, retry logic, and parallel processing.
"""

import asyncio
import json
import time
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from services.groq_llm_service import GroqLLMService
from services.gemini_llm_service import GeminiLLMService
from services.huggingface_llm_service import HuggingFaceLLMService
from services.question_pool_service import QuestionPoolService
from utils.constants import QUESTIONS_PER_PAPER, PAPERS_PER_GENERATION


class PaperGenerationAgent:
    """
    Intelligent agent that orchestrates question paper generation
    across multiple LLM providers with automatic failover and retry logic.
    Now generates 100-question pools with duplicate detection.
    """
    
    def __init__(self):
        # Initialize all LLM services
        self.llm_services = {
            'groq': GroqLLMService(),
            'gemini': GeminiLLMService(),
            'huggingface': HuggingFaceLLMService()
        }
        
        # Initialize question pool service for duplicate detection
        self.pool_service = QuestionPoolService()
        
        # Priority order for LLM selection (fastest to slowest)
        self.llm_priority = ['groq', 'gemini', 'huggingface']
        
        # Configuration
        self.max_retries = 3
        self.timeout_seconds = 120
        self.papers_to_generate = PAPERS_PER_GENERATION  # Now 1 pool
        
        # Tracking
        self.generation_stats = {
            'total_attempts': 0,
            'successful_generations': 0,
            'failed_generations': 0,
            'duplicates_removed': 0,
            'llm_usage': {llm: 0 for llm in self.llm_priority}
        }
    
    def check_llm_availability(self) -> Dict[str, bool]:
        """Check which LLM services are available"""
        availability = {}
        
        for llm_name, service in self.llm_services.items():
            try:
                is_available = service.check_connection()
                availability[llm_name] = is_available
                print(f"  [{llm_name.upper()}] {'✓ Available' if is_available else '✗ Unavailable'}")
            except Exception as e:
                availability[llm_name] = False
                print(f"  [{llm_name.upper()}] ✗ Error: {str(e)[:50]}")
        
        return availability
    
    def select_best_llm(self, availability: Dict[str, bool]) -> Optional[str]:
        """Select the best available LLM based on priority"""
        for llm_name in self.llm_priority:
            if availability.get(llm_name, False):
                return llm_name
        return None
    
    def generate_single_paper_with_fallback(
        self, 
        grade: str, 
        subject: str, 
        topic: str, 
        paper_number: int,
        availability: Dict[str, bool]
    ) -> Optional[Dict]:
        """
        Generate a single paper with automatic fallback to other LLMs if one fails
        """
        print(f"\n📄 Generating Paper #{paper_number}...")
        
        # Check for custom prompt
        custom_prompt_text = None
        try:
            from services.db_prompt_service import DBPromptService
            prompt_service = DBPromptService()
            prompts = prompt_service.get_prompts(grade, subject, topic)
            if prompts:
                custom_prompt_text = prompts[0]['custom_prompt']
                print(f"  ✨ Using Custom Prompt: {prompts[0]['prompt_name']}")
        except Exception as e:
            print(f"  ⚠️ Error fetching custom prompt: {e}")
        
        # Try each available LLM in priority order
        for llm_name in self.llm_priority:
            if not availability.get(llm_name, False):
                continue
            
            # Try with retries
            for attempt in range(1, self.max_retries + 1):
                try:
                    self.generation_stats['total_attempts'] += 1
                    
                    service = self.llm_services[llm_name]
                    print(f"  Attempt {attempt}/{self.max_retries} using [{llm_name.upper()}]...", end=" ", flush=True)
                    
                    start_time = time.time()
                    
                    # Pass custom prompt if available
                    # Note: We updated Groq and Gemini to accept custom_prompt.
                    # HuggingFace might not support it yet, so we check signature or just pass it as kwargs if possible.
                    # But since we defined the method explicitly, we should call it correctly.
                    
                    if llm_name in ['groq', 'gemini']:
                        paper = service.generate_question_paper(grade, subject, topic, paper_number, custom_prompt=custom_prompt_text)
                    else:
                        # Fallback for services that don't support custom prompt yet
                        paper = service.generate_question_paper(grade, subject, topic, paper_number)
                    
                    elapsed = time.time() - start_time
                    
                    if paper and paper.get('questions'):
                        self.generation_stats['successful_generations'] += 1
                        self.generation_stats['llm_usage'][llm_name] += 1
                        print(f"✓ Success ({elapsed:.1f}s)")
                        return paper
                    else:
                        print(f"✗ Invalid response")
                        
                except Exception as e:
                    print(f"✗ Error: {str(e)[:50]}")
                    
                # Wait before retry
                if attempt < self.max_retries:
                    time.sleep(2)
            
            print(f"  [{llm_name.upper()}] Failed after {self.max_retries} attempts, trying next LLM...")
        
        # All LLMs failed
        self.generation_stats['failed_generations'] += 1
        print(f"  ✗ Paper #{paper_number} generation failed with all LLMs")
        return None
    
    def _validate_paper(self, paper_data: Dict) -> bool:
        """Validate that the generated paper has correct structure"""
        if not paper_data:
            return False
        
        required_fields = ['paper_number', 'grade', 'subject', 'topic', 'questions']
        if not all(field in paper_data for field in required_fields):
            return False
        
        questions = paper_data.get('questions', [])
        if len(questions) < QUESTIONS_PER_PAPER * 0.8:  # At least 80% of required questions
            return False
        
        # Validate each question
        for q in questions:
            required_q_fields = ['question_number', 'question_text', 'options', 'correct_answer']
            if not all(field in q for field in required_q_fields):
                return False
            
            # Check options
            options = q.get('options', {})
            if not all(opt in options for opt in ['A', 'B', 'C', 'D']):
                return False
        
        return True
    
    def generate_papers_parallel(
        self, 
        grade: str, 
        subject: str, 
        topic: str
    ) -> List[Dict]:
        """
        Generate multiple papers in parallel using thread pool
        """
        print(f"\n🤖 Paper Generation Agent Starting...")
        print(f"📚 Target: Grade {grade} | {subject} | {topic}")
        print(f"📊 Papers to generate: {self.papers_to_generate}")
        
        # Check LLM availability
        print(f"\n🔍 Checking LLM availability...")
        availability = self.check_llm_availability()
        
        available_llms = [llm for llm, avail in availability.items() if avail]
        if not available_llms:
            print("\n❌ No LLM services available! Please check your API keys and connections.")
            return []
        
        print(f"\n✓ {len(available_llms)} LLM(s) available: {', '.join([llm.upper() for llm in available_llms])}")
        
        # Generate papers in parallel
        papers = []
        print(f"\n🚀 Starting parallel generation...")
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all paper generation tasks
            future_to_paper = {
                executor.submit(
                    self.generate_single_paper_with_fallback,
                    grade, subject, topic, paper_num, availability
                ): paper_num
                for paper_num in range(1, self.papers_to_generate + 1)
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_paper):
                paper_num = future_to_paper[future]
                try:
                    paper = future.result(timeout=self.timeout_seconds)
                    if paper:
                        papers.append(paper)
                        self.generation_stats['successful_generations'] += 1
                    else:
                        print(f"  ❌ Paper #{paper_num} generation failed")
                        self.generation_stats['failed_generations'] += 1
                except Exception as e:
                    print(f"  ❌ Error generating paper #{paper_num}: {str(e)}")
                    self.generation_stats['failed_generations'] += 1
        
        # Post-processing: Duplicate detection and DB saving
        if papers:
            print(f"\n🔍 Processing generated questions...")
            
            # 1. Flatten all questions
            all_questions = []
            for paper in papers:
                all_questions.extend(paper.get('questions', []))
            
            total_before = len(all_questions)
            print(f"   Total questions generated: {total_before}")
            
            # 2. Check for duplicates (using existing logic)
            unique_questions, duplicates_count = self.pool_service.check_duplicate_questions(all_questions)
            self.generation_stats['duplicates_removed'] = duplicates_count
            
            if duplicates_count > 0:
                print(f"   ⚠️  Found {duplicates_count} duplicate/similar questions")
                print(f"   ✓ Removed duplicates, {len(unique_questions)} unique questions remaining")
            else:
                print(f"   ✓ No duplicates found - all questions are unique!")
            
            # 3. Save to Database
            print(f"\n💾 Saving to Database...")
            from services.db_question_service import DBQuestionService
            db_service = DBQuestionService()
            
            saved_count = 0
            for q in unique_questions:
                # Ensure all fields are present
                q['grade'] = grade
                q['subject'] = subject
                q['topic'] = topic
                if db_service.save_question(q) > 0:
                    saved_count += 1
            
            print(f"   ✓ Saved {saved_count} questions to database")
            
            # Update stats
            self.generation_stats['total_unique_questions'] = len(unique_questions)

        self.print_generation_summary()
        
        # Re-number questions sequentially
        for i, q in enumerate(unique_questions, 1):
            q['question_number'] = i
        
        # Update the first paper with all unique questions
        if papers:
            papers[0]['questions'] = unique_questions
            # Remove other papers since we now have one pool
            papers = [papers[0]]
        
        return papers
    
    def _remove_duplicates_from_papers(self, papers: List[Dict]) -> List[Dict]:
        """Remove duplicate questions from generated papers"""
        if not papers:
            return papers
        
        # Combine all questions from all papers
        all_questions = []
        for paper in papers:
            all_questions.extend(paper.get('questions', []))
        
        print(f"\n🔍 Checking for duplicate questions...")
        print(f"   Total questions before: {len(all_questions)}")
        
        # Use pool service to detect and remove duplicates
        unique_questions, duplicates_found = self.pool_service.check_duplicate_questions(all_questions)
        
        duplicates_count = len(all_questions) - len(unique_questions)
        self.generation_stats['duplicates_removed'] = duplicates_count
        
        if duplicates_count > 0:
            print(f"   ⚠️  Found {duplicates_count} duplicate/similar questions")
            print(f"   ✓ Removed duplicates, {len(unique_questions)} unique questions remaining")
        else:
            print(f"   ✓ No duplicates found - all questions are unique!")
        
        # Re-number questions sequentially
        for i, q in enumerate(unique_questions, 1):
            q['question_number'] = i
        
        # Update the first paper with all unique questions
        if papers:
            papers[0]['questions'] = unique_questions
            # Remove other papers since we now have one pool
            papers = [papers[0]]
        
        return papers
    
    def generate_papers_sequential(
        self, 
        grade: str, 
        subject: str, 
        topic: str
    ) -> List[Dict]:
        """
        Generate papers sequentially (fallback if parallel fails)
        """
        print(f"\n🤖 Paper Generation Agent Starting (Sequential Mode)...")
        print(f"📚 Target: Grade {grade} | {subject} | {topic}")
        
        # Check LLM availability
        print(f"\n🔍 Checking LLM availability...")
        availability = self.check_llm_availability()
        
        available_llms = [llm for llm, avail in availability.items() if avail]
        if not available_llms:
            print("\n❌ No LLM services available!")
            return []
        
        print(f"\n✓ {len(available_llms)} LLM(s) available")
        
        # Generate papers one by one
        papers = []
        for paper_num in range(1, self.papers_to_generate + 1):
            paper_data = self.generate_single_paper_with_fallback(
                grade, subject, topic, paper_num, availability
            )
            if paper_data:
                papers.append(paper_data)
        
        self._print_generation_summary(papers)
        return papers
    
    def print_generation_summary(self):
        """Print detailed summary of the generation process"""
        print("\n" + "="*60)
        print("📊 GENERATION SUMMARY")
        print("="*60)
        
        if self.generation_stats['successful_generations'] > 0:
            print(f"✓ Question Pool Generated")
            print(f"  Total Unique Questions: {self.generation_stats.get('total_unique_questions', 0)}")
            print(f"  Duplicates Removed: {self.generation_stats['duplicates_removed']}")
            print(f"  Total Attempts: {self.generation_stats['total_attempts']}")
            print(f"  Successful: {self.generation_stats['successful_generations']}")
            print(f"  Failed: {self.generation_stats['failed_generations']}")
            
            print("\n📈 LLM Usage:")
            for llm, count in self.generation_stats['llm_usage'].items():
                if count > 0:
                    print(f"  {llm.upper()}: {count} generation(s)")
        else:
            print("❌ Generation Failed")
            print(f"  Total Attempts: {self.generation_stats['total_attempts']}")
            
        print("="*60 + "\n")

    def reset_stats(self):
        """Reset statistics for new run"""
        self.generation_stats = {
            'total_attempts': 0,
            'successful_generations': 0,
            'failed_generations': 0,
            'duplicates_removed': 0,
            'total_unique_questions': 0,
            'llm_usage': {llm: 0 for llm in self.llm_priority}
        }
