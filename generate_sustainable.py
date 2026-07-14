"""
Sustainable Question Generation Script
Generates 20-50 questions per topic with long delays to respect API rate limits
Designed to be run daily or on a schedule
"""

import sys
import os
import time
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.paper_generation_agent import PaperGenerationAgent
from services.db_question_service import DBQuestionService
from database.db_manager import db

# Configuration
QUESTIONS_PER_TOPIC = 20  # Generate 20 questions per topic per run
MAX_TOPICS_PER_RUN = 3   # Process max 3 topics per run
DELAY_BETWEEN_TOPICS = 300  # 5 minutes between topics
DELAY_BETWEEN_BATCHES = 60  # 1 minute between batches

# All Algebra topics
ALGEBRA_TOPICS = [
    # Chapter 2
    "2-1 Relations and Functions",
    "2-2 Direct Variation",
    "2-3 Linear Functions and Slope-Intercept Form",
    "2-4 More About Linear Equations",
    "2-5 Using Linear Models",
    "2-6 Families of Functions",
    "2-7 Absolute Value Functions and Graphs",
    "2-8 Two-Variable Inequalities",
    "Concept Byte: Piecewise Functions",
    # Chapter 3
    "3-1 Solving Systems Using Tables and Graphs",
    "3-2 Solving Systems Algebraically",
    "3-3 Systems of Inequalities",
    "3-4 Linear Programming",
    "3-5 Systems With Three Variables",
    "3-6 Solving Systems Using Matrices",
    "Concept Byte TECHNOLOGY: Linear Programming",
    "Concept Byte ACTIVITY: Graphs in Three Dimensions",
    # Chapter 4
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
    "Algebra Review: Square Roots and Radicals",
    # Chapter 5
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
    "Concept Byte ACTIVITY: Graphing Polynomials Using Zeros",
    # Chapter 6
    "6-1 Roots and Radical Expressions",
    "6-2 Multiplying and Dividing Radical Expressions",
    "6-3 Binomial Radical Expressions",
    "6-4 Rational Exponents",
    "6-5 Solving Square Root and Other Radical Equations",
    "6-6 Function Operations",
    "6-7 Inverse Relations and Functions",
    "6-8 Graphing Radical Functions",
    "Concept Byte REVIEW: Properties of Exponents",
    "Concept Byte TECHNOLOGY: Graphing Inverses",
    # Chapter 7
    "7-1 Exploring Exponential Models",
    "7-2 Properties of Exponential Functions",
    "7-3 Logarithmic Functions as Inverses",
    "7-4 Properties of Logarithms",
    "7-5 Exponential and Logarithmic Equations",
    "7-6 Natural Logarithms",
    "7-7 Transforming Exponential and Logarithmic Functions",
    "7-8 Curve Fitting with Exponential and Logarithmic Models",
    # Chapter 8
    "8-1 Inverse Variation",
    "8-2 The Reciprocal Function Family",
    "8-3 Rational Functions and Their Graphs",
    "8-4 Rational Expressions",
    "8-5 Adding and Subtracting Rational Expressions",
    "8-6 Solving Rational Equations",
    "8-7 Probability Models",
    "Concept Byte TECHNOLOGY: Rational Functions",
    # Chapter 9
    "9-1 Mathematical Patterns",
    "9-2 Arithmetic Sequences",
    "9-3 Geometric Sequences",
    "9-4 Arithmetic Series",
    "9-5 Geometric Series",
    "Concept Byte EXTENSION: The Fibonacci Sequence",
    "Concept Byte Geometry and Infinite Series",
]

def check_existing_questions(grade: str, subject: str, topic: str) -> int:
    """Check how many questions already exist for a topic"""
    result = db.execute_query(
        "SELECT COUNT(*) as count FROM questions WHERE grade = ? AND subject = ? AND topic = ?",
        (grade, subject, topic)
    )
    return result[0]['count'] if result else 0

def get_topics_needing_questions(grade: str, subject: str, target: int = 100) -> list:
    """Get list of topics that need more questions"""
    topics_needing = []
    for topic in ALGEBRA_TOPICS:
        count = check_existing_questions(grade, subject, topic)
        if count < target:
            topics_needing.append((topic, count))
    # Sort by count (lowest first)
    topics_needing.sort(key=lambda x: x[1])
    return topics_needing

def generate_for_topic(agent, grade: str, subject: str, topic: str, target: int):
    """Generate questions for one topic"""
    existing = check_existing_questions(grade, subject, topic)
    
    if existing >= target:
        return existing, "already_complete"
    
    needed = min(target - existing, QUESTIONS_PER_TOPIC)
    
    print(f"\n📚 Topic: {topic}")
    print(f"   Current: {existing} questions")
    print(f"   Generating: {needed} more questions")
    print(f"   Target: {target} questions")
    
    # Temporarily modify constants
    import app.utils.constants as constants
    original = constants.QUESTIONS_PER_PAPER
    constants.QUESTIONS_PER_PAPER = needed
    
    try:
        papers = agent.generate_papers_parallel(grade, subject, topic)
        
        if papers and papers[0].get('questions'):
            generated = len(papers[0]['questions'])
            final = check_existing_questions(grade, subject, topic)
            return final, "success"
        else:
            final = check_existing_questions(grade, subject, topic)
            return final, "failed"
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        final = check_existing_questions(grade, subject, topic)
        return final, "error"
    finally:
        constants.QUESTIONS_PER_PAPER = original

def main():
    """Main generation function"""
    print("="*70)
    print("🌱 SUSTAINABLE QUESTION GENERATION")
    print("="*70)
    print(f"\n📅 Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⚙️  Configuration:")
    print(f"   - Questions per topic per run: {QUESTIONS_PER_TOPIC}")
    print(f"   - Max topics per run: {MAX_TOPICS_PER_RUN}")
    print(f"   - Delay between topics: {DELAY_BETWEEN_TOPICS // 60} minutes")
    print(f"   - Delay between batches: {DELAY_BETWEEN_BATCHES} seconds")
    
    grade = "8"
    subject = "Mathematics"
    
    # Initialize services
    agent = PaperGenerationAgent()
    db_service = DBQuestionService()
    
    # Check LLM availability
    print("\n🔍 Checking LLM availability...")
    availability = agent.check_llm_availability()
    available = [llm for llm, avail in availability.items() if avail]
    
    if not available:
        print("❌ No LLM services available!")
        return
    
    print(f"✅ Using: {', '.join([llm.upper() for llm in available])}")
    
    # Get topics that need questions
    print("\n📊 Analyzing topics...")
    topics_needing = get_topics_needing_questions(grade, subject, target=100)
    
    total_topics = len(ALGEBRA_TOPICS)
    completed_topics = total_topics - len(topics_needing)
    
    print(f"\n📈 Progress Summary:")
    print(f"   Total topics: {total_topics}")
    print(f"   Completed (≥100 questions): {completed_topics}")
    print(f"   Needing questions: {len(topics_needing)}")
    
    if not topics_needing:
        print("\n🎉 All topics have 100+ questions! Generation complete!")
        return
    
    # Process up to MAX_TOPICS_PER_RUN
    topics_to_process = topics_needing[:MAX_TOPICS_PER_RUN]
    
    print(f"\n🎯 Processing {len(topics_to_process)} topic(s) in this run...")
    print(f"⏱️  Estimated time: ~{len(topics_to_process) * (QUESTIONS_PER_TOPIC * DELAY_BETWEEN_BATCHES + DELAY_BETWEEN_TOPICS) // 60} minutes")
    
    results = []
    for idx, (topic, current_count) in enumerate(topics_to_process, 1):
        print(f"\n{'='*70}")
        print(f"Topic {idx}/{len(topics_to_process)}")
        print(f"{'='*70}")
        
        final_count, status = generate_for_topic(agent, grade, subject, topic, target=100)
        
        results.append({
            'topic': topic,
            'before': current_count,
            'after': final_count,
            'status': status
        })
        
        # Wait between topics (except for the last one)
        if idx < len(topics_to_process):
            print(f"\n⏳ Waiting {DELAY_BETWEEN_TOPICS // 60} minutes before next topic...")
            time.sleep(DELAY_BETWEEN_TOPICS)
    
    # Summary
    print("\n" + "="*70)
    print("📊 RUN SUMMARY")
    print("="*70)
    
    for result in results:
        status_icon = "✅" if result['status'] == "success" else "⚠️" if result['status'] == "already_complete" else "❌"
        print(f"{status_icon} {result['topic']}")
        print(f"   Before: {result['before']} → After: {result['after']} questions")
    
    # Overall progress
    topics_needing_after = get_topics_needing_questions(grade, subject, target=100)
    completed_after = total_topics - len(topics_needing_after)
    
    print(f"\n📈 Overall Progress:")
    print(f"   Completed topics: {completed_after}/{total_topics}")
    print(f"   Remaining: {len(topics_needing_after)} topics")
    
    if completed_after < total_topics:
        print(f"\n💡 Run this script daily to gradually complete all topics")
        print(f"💡 Each run processes {MAX_TOPICS_PER_RUN} topics with {QUESTIONS_PER_TOPIC} questions each")
        estimated_days = (total_topics - completed_after) / MAX_TOPICS_PER_RUN
        print(f"💡 Estimated days to complete: ~{estimated_days:.0f} days")
    
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation stopped by user")
        print("💡 Questions generated so far have been saved")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

