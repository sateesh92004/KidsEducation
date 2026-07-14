"""
Generate 100 questions for each topic/subtopic in 8th Grade Algebra
Based on the Algebra textbook syllabus provided
"""

import sys
import os
from typing import List, Dict

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.paper_generation_agent import PaperGenerationAgent
from services.db_question_service import DBQuestionService
from database.db_manager import db

# 8th Grade Algebra Syllabus - All Topics and Subtopics
ALGEBRA_SYLLABUS = {
    "Chapter 2: Functions, Equations, and Graphs": {
        "grade": "8",
        "subject": "Mathematics",
        "subtopics": [
            "2-1 Relations and Functions",
            "2-2 Direct Variation",
            "2-3 Linear Functions and Slope-Intercept Form",
            "2-4 More About Linear Equations",
            "2-5 Using Linear Models",
            "2-6 Families of Functions",
            "2-7 Absolute Value Functions and Graphs",
            "2-8 Two-Variable Inequalities",
            "Concept Byte: Piecewise Functions"
        ]
    },
    "Chapter 3: Linear Systems": {
        "grade": "8",
        "subject": "Mathematics",
        "subtopics": [
            "3-1 Solving Systems Using Tables and Graphs",
            "3-2 Solving Systems Algebraically",
            "3-3 Systems of Inequalities",
            "3-4 Linear Programming",
            "3-5 Systems With Three Variables",
            "3-6 Solving Systems Using Matrices",
            "Concept Byte TECHNOLOGY: Linear Programming",
            "Concept Byte ACTIVITY: Graphs in Three Dimensions"
        ]
    },
    "Chapter 4: Quadratic Functions and Equations": {
        "grade": "8",
        "subject": "Mathematics",
        "subtopics": [
            "4-1 Quadratic Functions and Transformations",
            "4-2 Standard Form of a Quadratic Function",
            "4-3 Modeling With Quadratic Functions",
            "4-4 Factoring Quadratic Expressions",
            "4-5 Quadratic Equations",
            "4-6 Completing the Square",
            "4-7 The Quadratic Formula",
            "4-8 Complex Numbers",
            "4-9 Quadratic Systems",
            "Concept Byte: Identifying Quadratic Data",
            "Concept Byte: Writing Equations From Roots",
            "Concept Byte: Quadratic Inequalities",
            "Concept Byte EXTENSION: Powers of Complex Numbers",
            "Algebra Review: Square Roots and Radicals"
        ]
    },
    "Chapter 5: Polynomials and Polynomial Functions": {
        "grade": "8",
        "subject": "Mathematics",
        "subtopics": [
            "5-1 Polynomial Functions",
            "5-2 Polynomials, Linear Factors, and Zeros",
            "5-3 Solving Polynomial Equations",
            "5-4 Dividing Polynomials",
            "5-5 Theorems About Roots of Polynomial Equations",
            "5-6 The Fundamental Theorem of Algebra",
            "5-7 The Binomial Theorem",
            "5-8 Polynomial Models in the Real World",
            "5-9 Transforming Polynomial Functions",
            "Concept Byte EXTENSION: Using Polynomial Identities",
            "Concept Byte ACTIVITY: Graphing Polynomials Using Zeros"
        ]
    },
    "Chapter 6: Radical Functions and Rational Exponents": {
        "grade": "8",
        "subject": "Mathematics",
        "subtopics": [
            "6-1 Roots and Radical Expressions",
            "6-2 Multiplying and Dividing Radical Expressions",
            "6-3 Binomial Radical Expressions",
            "6-4 Rational Exponents",
            "6-5 Solving Square Root and Other Radical Equations",
            "6-6 Function Operations",
            "6-7 Inverse Relations and Functions",
            "6-8 Graphing Radical Functions",
            "Concept Byte REVIEW: Properties of Exponents",
            "Concept Byte TECHNOLOGY: Graphing Inverses"
        ]
    },
    "Chapter 7: Exponential and Logarithmic Functions": {
        "grade": "8",
        "subject": "Mathematics",
        "subtopics": [
            "7-1 Exploring Exponential Models",
            "7-2 Properties of Exponential Functions",
            "7-3 Logarithmic Functions as Inverses",
            "7-4 Properties of Logarithms",
            "7-5 Exponential and Logarithmic Equations",
            "7-6 Natural Logarithms",
            "7-7 Transforming Exponential and Logarithmic Functions",
            "7-8 Curve Fitting with Exponential and Logarithmic Models"
        ]
    },
    "Chapter 8: Rational Functions": {
        "grade": "8",
        "subject": "Mathematics",
        "subtopics": [
            "8-1 Inverse Variation",
            "8-2 The Reciprocal Function Family",
            "8-3 Rational Functions and Their Graphs",
            "8-4 Rational Expressions",
            "8-5 Adding and Subtracting Rational Expressions",
            "8-6 Solving Rational Equations",
            "8-7 Probability Models",
            "Concept Byte TECHNOLOGY: Rational Functions"
        ]
    },
    "Chapter 9: Sequences and Series": {
        "grade": "8",
        "subject": "Mathematics",
        "subtopics": [
            "9-1 Mathematical Patterns",
            "9-2 Arithmetic Sequences",
            "9-3 Geometric Sequences",
            "9-4 Arithmetic Series",
            "9-5 Geometric Series",
            "Concept Byte EXTENSION: The Fibonacci Sequence",
            "Concept Byte Geometry and Infinite Series"
        ]
    }
}

def check_existing_questions(grade: str, subject: str, topic: str) -> int:
    """Check how many questions already exist for a topic"""
    result = db.execute_query(
        "SELECT COUNT(*) as count FROM questions WHERE grade = ? AND subject = ? AND topic = ?",
        (grade, subject, topic)
    )
    return result[0]['count'] if result else 0

def generate_questions_for_topic(agent: PaperGenerationAgent, grade: str, subject: str, topic: str, target_count: int = 100):
    """Generate questions for a specific topic"""
    print(f"\n{'='*80}")
    print(f"📚 Generating questions for: {topic}")
    print(f"{'='*80}")
    
    # Check existing questions
    existing = check_existing_questions(grade, subject, topic)
    print(f"📊 Existing questions: {existing}")
    
    if existing >= target_count:
        print(f"✅ Already have {existing} questions (target: {target_count}). Skipping...")
        return existing
    
    needed = target_count - existing
    print(f"🎯 Need to generate: {needed} more questions")
    
    # Generate questions using the agent
    # The agent generates 100 questions per call, so we may need multiple calls
    generated = 0
    attempts = 0
    max_attempts = 5  # Try up to 5 times to get enough questions
    
    while generated < needed and attempts < max_attempts:
        attempts += 1
        print(f"\n🔄 Attempt {attempts}/{max_attempts}...")
        
        try:
            # Reset agent stats for new generation
            agent.reset_stats()
            
            # Add delay between topics to respect rate limits
            if attempts > 1:
                import time
                wait_time = 30 * attempts  # Exponential backoff: 30s, 60s, 90s...
                print(f"⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            
            papers = agent.generate_papers_parallel(grade, subject, topic)
            
            if papers and papers[0].get('questions'):
                new_count = len(papers[0]['questions'])
                generated += new_count
                print(f"✅ Generated {new_count} questions in this attempt")
                
                # Check current count in database
                current_total = check_existing_questions(grade, subject, topic)
                print(f"📈 Total in database: {current_total} questions")
                
                if current_total >= target_count:
                    print(f"✅ Target reached! Total questions: {current_total}")
                    return current_total
            else:
                print(f"⚠️  No questions generated in this attempt")
                
        except Exception as e:
            print(f"❌ Error in attempt {attempts}: {str(e)[:100]}")
            import time
            time.sleep(5)  # Wait before retry
    
    final_count = check_existing_questions(grade, subject, topic)
    print(f"\n📊 Final count for '{topic}': {final_count} questions")
    
    if final_count < target_count:
        print(f"⚠️  Warning: Only {final_count}/{target_count} questions generated")
    
    return final_count

def main():
    """Main function to generate all questions"""
    print("="*80)
    print("🚀 8th Grade Algebra Question Generator")
    print("="*80)
    print("\nThis script will generate 100 questions for each subtopic in 8th Grade Algebra.")
    print("This may take a while depending on your LLM API limits...\n")
    
    # Check LLM availability first
    agent = PaperGenerationAgent()
    availability = agent.check_llm_availability()
    available_llms = [llm for llm, avail in availability.items() if avail]
    
    if not available_llms:
        print("\n❌ No LLM services available! Please check your API keys.")
        print("   Required: GROQ_API_KEY, GEMINI_API_KEY, or HUGGINGFACE_API_KEY")
        return
    
    print(f"\n✅ {len(available_llms)} LLM service(s) available: {', '.join([llm.upper() for llm in available_llms])}")
    
    # Ask for confirmation (skip if running non-interactively)
    try:
        response = input("\nProceed with question generation? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Generation cancelled.")
            return
    except EOFError:
        # Running non-interactively, auto-confirm
        print("\n⚠️  Running in non-interactive mode. Auto-confirming...")
        print("Proceeding with question generation...\n")
    
    # Statistics
    total_topics = 0
    total_questions = 0
    successful_topics = 0
    failed_topics = []
    skipped_topics = []
    
    # Process each chapter
    for chapter_name, chapter_data in ALGEBRA_SYLLABUS.items():
        print(f"\n{'#'*80}")
        print(f"📖 {chapter_name}")
        print(f"{'#'*80}")
        
        grade = str(chapter_data['grade'])
        subject = chapter_data['subject']
        
        # Process each subtopic
        for idx, subtopic in enumerate(chapter_data['subtopics'], 1):
            total_topics += 1
            try:
                # Add delay between topics to respect API rate limits
                if idx > 1:
                    import time
                    print(f"\n⏳ Waiting 5 seconds before next topic (rate limit protection)...")
                    time.sleep(5)
                
                count = generate_questions_for_topic(agent, grade, subject, subtopic, target_count=100)
                if count >= 100:
                    successful_topics += 1
                    total_questions += count
                elif count > 0:
                    failed_topics.append((subtopic, count))
                else:
                    skipped_topics.append(subtopic)
            except KeyboardInterrupt:
                print("\n\n⚠️  Generation interrupted by user")
                break
            except Exception as e:
                print(f"❌ Error generating questions for '{subtopic}': {e}")
                failed_topics.append((subtopic, 0))
    
    # Print summary
    print("\n" + "="*80)
    print("📊 GENERATION SUMMARY")
    print("="*80)
    print(f"Total Topics Processed: {total_topics}")
    print(f"Successfully Generated (≥100 questions): {successful_topics}")
    print(f"Total Questions Generated: {total_questions}")
    print(f"Incomplete Topics (<100 questions): {len(failed_topics)}")
    print(f"Skipped Topics (0 questions): {len(skipped_topics)}")
    
    if failed_topics:
        print("\n⚠️  Topics that need more questions:")
        for topic, count in failed_topics:
            print(f"   - {topic}: {count} questions (target: 100)")
    
    if skipped_topics:
        print("\n⚠️  Topics that were skipped:")
        for topic in skipped_topics:
            print(f"   - {topic}")
    
    print("\n✅ Generation complete!")
    print("="*80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

