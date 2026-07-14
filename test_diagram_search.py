#!/usr/bin/env python3
"""
Test script for Diagram Search
"""
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.image_search_service import ImageSearchService

def test_diagram_search():
    print("Testing Diagram Search...")
    service = ImageSearchService()
    
    query = "Human Skeleton"
    print(f"Searching for: {query}")
    
    results = service.search_images(query)
    
    if results:
        print(f"✅ Found {len(results)} diagrams:")
        for i, res in enumerate(results):
            print(f"  {i+1}. {res['title']}")
            print(f"     URL: {res['image_url'][:50]}...")
    else:
        print("❌ No diagrams found")

if __name__ == "__main__":
    test_diagram_search()
