#!/usr/bin/env python3
"""
Test script for Learning Agent (AI Teacher)
Tests LLM connectivity and lesson generation
"""

import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from services.learning_agent import LearningAgent

def test_teaching_lesson():
    """Test generating a lesson"""
    print("=" * 60)
    print("🎓 Testing Learning Agent (AI Teacher)")
    print("=" * 60)
    
    agent = LearningAgent()
    
    # Test parameters
    grade = "5"
    subject = "Science"
    topic = "Photosynthesis"
    
    print(f"\nRequest: Teach Grade {grade} {subject} about '{topic}'")
    print("Generating lesson (Streaming)...")
    
    # Test streaming
    full_lesson = ""
    print("-" * 40)
    for chunk in agent.teach_topic_stream(grade, subject, topic):
        print(chunk, end="", flush=True)
        full_lesson += chunk
    print("\n" + "-" * 40)
    
    if full_lesson and len(full_lesson) > 100:
        print("\n✅ Lesson generated successfully!")
        return True
    else:
        print("\n❌ Failed to generate lesson")
        return False

def test_teach_more():
    """Test generating more details"""
    print("\n" + "=" * 60)
    print("🚀 Testing 'Tell Me More' Feature")
    print("=" * 60)
    
    agent = LearningAgent()
    
    grade = "5"
    subject = "Science"
    topic = "Photosynthesis"
    previous = "Photosynthesis is how plants make food using sunlight."
    
    print(f"\nRequest: Tell me more about '{topic}'")
    print("Generating advanced details...\n")
    
    more_info = agent.teach_more(grade, subject, topic, previous)
    
    if more_info and len(more_info) > 100:
        print("\n✅ Advanced details generated successfully!")
        print("-" * 40)
        print(more_info[:500] + "...\n(truncated)")
        print("-" * 40)
        return True
    else:
        print("\n❌ Failed to generate more info")
        return False

def main():
    """Run tests"""
    print("\n🤖 Learning Agent - Test Suite")
    
    success_lesson = test_teaching_lesson()
    if success_lesson:
        test_teach_more()
    
    print("\n" + "=" * 60)
    print("✅ Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
