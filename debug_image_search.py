#!/usr/bin/env python3
"""
Debug script for Image Search with specific queries
"""
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.image_search_service import ImageSearchService

def debug_search():
    print("Debugging Image Search...")
    service = ImageSearchService()
    
    queries = ["Heart", "Human Heart", "Volcano"]
    
    for query in queries:
        print(f"\n--- Searching for: {query} ---")
        results = service.search_images(query)
        
        if results:
            print(f"✅ Found {len(results)} images")
            for i, res in enumerate(results):
                print(f"  {i+1}. {res['title']}")
                print(f"     Thumb: {res['thumbnail_url'][:50]}...")
        else:
            print("❌ No images found")

if __name__ == "__main__":
    debug_search()
