"""
Quick script to check progress of question generation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from database.db_manager import db

def check_progress():
    """Check how many questions have been generated for 8th grade Algebra"""
    print("="*80)
    print("📊 Question Generation Progress - 8th Grade Algebra")
    print("="*80)
    
    # Get total questions
    total_result = db.execute_query(
        "SELECT COUNT(*) as count FROM questions WHERE grade = '8' AND subject = 'Mathematics'"
    )
    total = total_result[0]['count'] if total_result else 0
    
    print(f"\n📈 Total Questions Generated: {total}")
    
    # Get questions by topic
    topics_result = db.execute_query(
        """SELECT topic, COUNT(*) as count 
           FROM questions 
           WHERE grade = '8' AND subject = 'Mathematics'
           GROUP BY topic
           ORDER BY topic"""
    )
    
    if topics_result:
        print(f"\n📚 Questions by Topic:")
        print("-" * 80)
        for row in topics_result:
            topic = row['topic']
            count = row['count']
            status = "✅" if count >= 100 else "⚠️ " if count > 0 else "❌"
            print(f"{status} {topic}: {count} questions")
    
    # Count topics with 100+ questions
    complete_topics = db.execute_query(
        """SELECT COUNT(DISTINCT topic) as count
           FROM questions 
           WHERE grade = '8' AND subject = 'Mathematics'
           GROUP BY topic
           HAVING COUNT(*) >= 100"""
    )
    
    complete_count = len(complete_topics) if complete_topics else 0
    
    print(f"\n✅ Topics with 100+ questions: {complete_count}")
    print(f"📊 Estimated completion: {complete_count}/75 topics")
    print("="*80)

if __name__ == "__main__":
    try:
        check_progress()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

