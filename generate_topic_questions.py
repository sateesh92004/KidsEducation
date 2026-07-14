"""
Ad-hoc Question Generation - 50 questions per main topic
Groups all subtopics under main chapter topics
"""

import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.paper_generation_agent import PaperGenerationAgent
from services.db_question_service import DBQuestionService
from database.db_manager import db

# Main Topics (Chapters) - All subtopics grouped together
MAIN_TOPICS = {
    "Topic 1: Functions, Equations, and Graphs": {
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
    "Topic 2: Linear Systems": {
        "grade": "8",
        "subject": "Mathematics",
        "subtopics": [
            "3-1 Solving Systems Using Tables and Graphs",
            "3-2 Solving Systems Algebraically",
            "3-3 Systems of Inequalities",
            "3-4 Linear Programming",
            "3-5 Systems With Three Variables",
            "3-6 Solving Systems Using Matrices"
        ]
    },
    "Topic 3: Quadratic Functions and Equations": {
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
            "4-9 Quadratic Systems"
        ]
    },
    "Topic 4: Polynomials and Polynomial Functions": {
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
            "5-9 Transforming Polynomial Functions"
        ]
    },
    "Topic 5: Radical Functions and Rational Exponents": {
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
            "6-8 Graphing Radical Functions"
        ]
    },
    "Topic 6: Exponential and Logarithmic Functions": {
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
    "Topic 7: Rational Functions": {
        "grade": "8",
        "subject": "Mathematics",
        "subtopics": [
            "8-1 Inverse Variation",
            "8-2 The Reciprocal Function Family",
            "8-3 Rational Functions and Their Graphs",
            "8-4 Rational Expressions",
            "8-5 Adding and Subtracting Rational Expressions",
            "8-6 Solving Rational Equations",
            "8-7 Probability Models"
        ]
    },
    "Topic 8: Sequences and Series": {
        "grade": "8",
        "subject": "Mathematics",
        "subtopics": [
            "9-1 Mathematical Patterns",
            "9-2 Arithmetic Sequences",
            "9-3 Geometric Sequences",
            "9-4 Arithmetic Series",
            "9-5 Geometric Series"
        ]
    }
}

def check_existing_questions(grade: str, subject: str, topic: str) -> int:
    """Check how many questions exist for a topic"""
    result = db.execute_query(
        "SELECT COUNT(*) as count FROM questions WHERE grade = ? AND subject = ? AND topic = ?",
        (grade, subject, topic)
    )
    return result[0]['count'] if result else 0

def generate_for_topic(agent, grade: str, subject: str, topic_name: str, topic_data: dict, target: int = 50):
    """Generate 50 questions for a main topic"""
    print(f"\n{'='*70}")
    print(f"📚 {topic_name}")
    print(f"{'='*70}")
    
    # Check existing
    existing = check_existing_questions(grade, subject, topic_name)
    print(f"📊 Existing questions: {existing}")
    
    if existing >= target:
        print(f"✅ Already have {existing} questions (target: {target}). Skipping.")
        return existing, "already_complete"
    
    needed = target - existing
    print(f"🎯 Need to generate: {needed} more questions")
    
    # Create a comprehensive description including all subtopics
    subtopics_list = ", ".join(topic_data['subtopics'])
    enhanced_topic = f"{topic_name}. This topic covers: {subtopics_list}. Generate diverse, real-world, complex problems that require multi-step thinking and application of concepts."
    
    # Temporarily modify constants
    import app.utils.constants as constants
    original = constants.QUESTIONS_PER_PAPER
    constants.QUESTIONS_PER_PAPER = needed
    
    try:
        print(f"\n🚀 Generating {needed} questions...")
        print(f"⏱️  This will take approximately {needed * 2} minutes due to rate limits")
        print(f"💡 Generating real-world, complex, non-repetitive problems...\n")
        
        papers = agent.generate_papers_parallel(grade, subject, enhanced_topic)
        
        if papers and papers[0].get('questions'):
            generated = len(papers[0]['questions'])
            final = check_existing_questions(grade, subject, topic_name)
            print(f"\n✅ Generated {generated} questions")
            print(f"📊 Total in database: {final} questions")
            return final, "success"
        else:
            final = check_existing_questions(grade, subject, topic_name)
            print(f"\n⚠️  Generated {final - existing} questions (some may have failed)")
            return final, "partial"
    except Exception as e:
        print(f"\n❌ Error: {str(e)[:100]}")
        final = check_existing_questions(grade, subject, topic_name)
        return final, "error"
    finally:
        constants.QUESTIONS_PER_PAPER = original

def main():
    """Generate questions for specified topic(s)"""
    print("="*70)
    print("🎯 AD-HOC QUESTION GENERATION")
    print("="*70)
    print("\nGenerates 50 questions per main topic")
    print("All questions are real-world, complex, non-repetitive, multiple choice")
    print("="*70)
    
    # Initialize
    agent = PaperGenerationAgent()
    db_service = DBQuestionService()
    
    # Check LLM availability
    print("\n🔍 Checking LLM availability...")
    availability = agent.check_llm_availability()
    available = [llm for llm, avail in availability.items() if avail]
    
    if not available:
        print("❌ No LLM services available!")
        return
    
    print(f"✅ Using: {', '.join([llm.upper() for llm in available])}\n")
    
    # Generate for Topic 1
    topic_name = "Topic 1: Functions, Equations, and Graphs"
    topic_data = MAIN_TOPICS[topic_name]
    
    print(f"🎯 Generating for: {topic_name}")
    print(f"📋 Covers {len(topic_data['subtopics'])} subtopics")
    
    final_count, status = generate_for_topic(
        agent,
        topic_data['grade'],
        topic_data['subject'],
        topic_name,
        topic_data,
        target=50
    )
    
    # Summary
    print("\n" + "="*70)
    print("📊 GENERATION SUMMARY")
    print("="*70)
    print(f"Topic: {topic_name}")
    print(f"Status: {status}")
    print(f"Total Questions: {final_count}/50")
    
    # Check if topic appears in database
    topics = db_service.get_available_topics(topic_data['grade'], topic_data['subject'])
    print(f"\n📚 Available topics in database: {len(topics)}")
    if topic_name in topics:
        print(f"✅ Topic '{topic_name}' is now available in the Test screen!")
    else:
        print(f"⚠️  Topic not found - checking database...")
        # Check with exact match
        result = db.execute_query(
            "SELECT COUNT(*) as count FROM questions WHERE grade = ? AND subject = ? AND topic = ?",
            (topic_data['grade'], topic_data['subject'], topic_name)
        )
        if result and result[0]['count'] > 0:
            print(f"✅ Found {result[0]['count']} questions in database")
    
    print("="*70)
    print("\n💡 You can now test the UI - select Grade 8, Mathematics, and 'Take Test'")
    print("💡 The topic should appear in the list!")

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

