#!/usr/bin/env python3
"""
Debug script to test Gemini LLM Service directly
"""
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.gemini_llm_service import GeminiLLMService
from dotenv import load_dotenv

def test_gemini():
    print("Testing Gemini LLM Service...")
    load_dotenv()
    
    key = os.getenv('GEMINI_API_KEY')
    if key:
        print(f"✅ Found GEMINI_API_KEY: {key[:5]}...{key[-5:]}")
    else:
        print("❌ GEMINI_API_KEY not found in environment!")

    service = GeminiLLMService()
    
    if not service.check_connection():
        print("❌ Connection Check Failed! Check API Key.")
        return

    print("✅ Connection Check Passed.")
    
    print("\nAttempting to generate text...")
    prompt = "Explain why the sky is blue in one sentence."
    
    result = service.generate_text(prompt)
    
    if result:
        print(f"✅ Success! Response:\n{result}")
    else:
        print("❌ Generation Failed (returned None)")

if __name__ == "__main__":
    test_gemini()
