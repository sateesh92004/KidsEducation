"""
Quick script to check if Topic 1 is complete
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from database.db_manager import db

def check_topic1():
    """Check Topic 1 status"""
    topic_name = "Topic 1: Functions, Equations, and Graphs"
    
    result = db.execute_query(
        "SELECT COUNT(*) as count FROM questions WHERE grade = '8' AND subject = 'Mathematics' AND topic = ?",
        (topic_name,)
    )
    
    count = result[0]['count'] if result else 0
    
    print("="*70)
    print("📊 TOPIC 1 STATUS CHECK")
    print("="*70)
    print(f"\nTopic: {topic_name}")
    print(f"Questions Generated: {count}/50")
    
    if count >= 50:
        print("\n" + "🎉" * 35)
        print("✅ TOPIC 1 IS COMPLETE! 🎉")
        print("🎉" * 35)
        print("\n💡 You can now:")
        print("   1. Open the app")
        print("   2. Login as student")
        print("   3. Select Grade 8 → Mathematics → Take Test")
        print("   4. You should see 'Topic 1: Functions, Equations, and Graphs'")
        print("="*70)
        return True
    else:
        remaining = 50 - count
        print(f"\n⏳ Still generating...")
        print(f"   Remaining: {remaining} questions")
        print(f"   Progress: {(count/50)*100:.1f}%")
        print("="*70)
        return False

if __name__ == "__main__":
    check_topic1()

