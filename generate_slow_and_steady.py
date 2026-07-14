"""
Slow and steady question generation - handles rate limits better
Generates questions one topic at a time with long delays
"""

import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.paper_generation_agent import PaperGenerationAgent
from services.db_question_service import DBQuestionService
from database.db_manager import db

# Just generate for ONE topic first to test
TEST_TOPIC = {
    "grade": "8",
    "subject": "Mathematics",
    "topic": "2-1 Relations and Functions"
}

def check_existing_questions(grade: str, subject: str, topic: str) -> int:
    """Check how many questions already exist"""
    result = db.execute_query(
        "SELECT COUNT(*) as count FROM questions WHERE grade = ? AND subject = ? AND topic = ?",
        (grade, subject, topic)
    )
    return result[0]['count'] if result else 0

def generate_one_topic_slowly(agent, grade: str, subject: str, topic: str, target: int = 20):
    """Generate questions for one topic with very slow, careful approach"""
    print(f"\n{'='*70}")
    print(f"📚 Generating: {topic}")
    print(f"{'='*70}")
    
    existing = check_existing_questions(grade, subject, topic)
    print(f"📊 Existing: {existing} questions")
    
    if existing >= target:
        print(f"✅ Already have {existing} questions. Skipping.")
        return existing
    
    needed = target - existing
    print(f"🎯 Need: {needed} more questions")
    print(f"⏱️  This will take approximately {needed * 2} minutes due to rate limits")
    print(f"💡 Tip: You can stop with Ctrl+C and resume later\n")
    
    # Temporarily set to generate fewer questions
    import app.utils.constants as constants
    original = constants.QUESTIONS_PER_PAPER
    constants.QUESTIONS_PER_PAPER = needed
    
    try:
        print("🚀 Starting generation (this will be slow but steady)...\n")
        papers = agent.generate_papers_parallel(grade, subject, topic)
        
        if papers and papers[0].get('questions'):
            count = len(papers[0]['questions'])
            final = check_existing_questions(grade, subject, topic)
            print(f"\n✅ Generated {count} questions")
            print(f"📊 Total in database: {final} questions")
            return final
        else:
            print("\n⚠️  No questions generated")
            return check_existing_questions(grade, subject, topic)
    finally:
        constants.QUESTIONS_PER_PAPER = original

def main():
    """Generate questions slowly for one topic"""
    print("="*70)
    print("🐢 SLOW & STEADY Question Generator")
    print("="*70)
    print("\nThis script generates questions VERY slowly to avoid rate limits.")
    print("It's designed to work with Groq's free tier limitations.\n")
    
    agent = PaperGenerationAgent()
    
    # Check availability
    availability = agent.check_llm_availability()
    available = [llm for llm, avail in availability.items() if avail]
    
    if not available:
        print("❌ No LLM services available!")
        return
    
    print(f"✅ Using: {', '.join([llm.upper() for llm in available])}\n")
    
    # Generate for test topic
    count = generate_one_topic_slowly(
        agent,
        TEST_TOPIC["grade"],
        TEST_TOPIC["subject"],
        TEST_TOPIC["topic"],
        target=20  # Just 20 for testing
    )
    
    # Check available topics
    db_service = DBQuestionService()
    topics = db_service.get_available_topics(TEST_TOPIC["grade"], TEST_TOPIC["subject"])
    
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    print(f"✅ Questions generated: {count}")
    print(f"📚 Available topics: {len(topics)}")
    if topics:
        print("\nTopics now available:")
        for t in topics:
            stats = db_service.get_topic_stats(TEST_TOPIC["grade"], TEST_TOPIC["subject"], t)
            print(f"   - {t}: {stats['total_questions']} questions")
    print("="*70)
    print("\n💡 You can now test the UI - the topic should appear!")
    print("💡 To generate more topics, run this script again with different topics")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation stopped by user")
        print("💡 Questions generated so far have been saved to the database")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

