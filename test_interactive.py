#!/usr/bin/env python3
"""
Test script for Interactive Content (Quiz & Flashcards)
"""
import sys
import os
import json

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.learning_agent import LearningAgent

def test_interactive_content():
    print("Testing Interactive Content Generation...")
    agent = LearningAgent()
    
    grade = "5"
    subject = "Science"
    topic = "Solar System"
    
    print(f"\nTopic: {topic}")
    
    # 1. Test Flashcards
    print("\n1. Generating Flashcards...")
    cards = agent.generate_flashcards(grade, subject, topic)
    if cards:
        print(f"✅ Generated {len(cards)} flashcards:")
        print(json.dumps(cards, indent=2))
    else:
        print("❌ Failed to generate flashcards")
        
    # 2. Test Quiz
    print("\n2. Generating Quiz...")
    quiz = agent.generate_quiz(grade, subject, topic)
    if quiz:
        print(f"✅ Generated {len(quiz)} quiz questions:")
        print(json.dumps(quiz, indent=2))
    else:
        print("❌ Failed to generate quiz")

if __name__ == "__main__":
    test_interactive_content()
