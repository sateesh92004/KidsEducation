"""
Quick script to generate 20 questions for one topic for testing
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.paper_generation_agent import PaperGenerationAgent
from services.db_question_service import DBQuestionService
from database.db_manager import db

def generate_test_questions():
    """Generate a small set of questions for testing"""
    print("="*60)
    print("Generating Test Questions for UI Testing")
    print("="*60)
    
    grade = "8"
    subject = "Mathematics"
    topic = "2-1 Relations and Functions"
    
    print(f"\n📚 Generating questions for:")
    print(f"   Grade: {grade}")
    print(f"   Subject: {subject}")
    print(f"   Topic: {topic}")
    print(f"   Target: 20 questions (for testing)")
    
    # Initialize services
    agent = PaperGenerationAgent()
    db_service = DBQuestionService()
    
    # Check LLM availability
    print("\n🔍 Checking LLM availability...")
    availability = agent.check_llm_availability()
    
    available_llms = [llm for llm, avail in availability.items() if avail]
    if not available_llms:
        print("\n❌ No LLM services available!")
        return
    
    print(f"\n✅ Using: {', '.join([llm.upper() for llm in available_llms])}")
    
    # Temporarily modify to generate fewer questions
    from utils.constants import QUESTIONS_PER_PAPER
    import app.utils.constants as constants
    
    # Save original value
    original_count = constants.QUESTIONS_PER_PAPER
    # Set to 20 for testing
    constants.QUESTIONS_PER_PAPER = 20
    
    try:
        print("\n🚀 Generating questions...")
        papers = agent.generate_papers_parallel(grade, subject, topic)
        
        if papers and papers[0].get('questions'):
            count = len(papers[0]['questions'])
            print(f"\n✅ Successfully generated {count} questions!")
            
            # Verify in database
            db_count = db.execute_query(
                "SELECT COUNT(*) as count FROM questions WHERE grade = ? AND subject = ? AND topic = ?",
                (grade, subject, topic)
            )
            saved_count = db_count[0]['count'] if db_count else 0
            print(f"📊 Saved to database: {saved_count} questions")
            
            # Check available topics
            topics = db_service.get_available_topics(grade, subject)
            print(f"\n📚 Available topics now: {len(topics)}")
            for t in topics:
                print(f"   - {t}")
        else:
            print("\n❌ Failed to generate questions")
    finally:
        # Restore original value
        constants.QUESTIONS_PER_PAPER = original_count

if __name__ == "__main__":
    try:
        generate_test_questions()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

