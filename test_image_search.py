#!/usr/bin/env python3
"""
Test script for Image Search
"""
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.image_search_service import ImageSearchService

def test_image_search():
    print("Testing Image Search...")
    service = ImageSearchService()
    
    query = "Human Skeleton"
    print(f"Searching for: {query}")
    
    results = service.search_images(query)
    
    if results:
        print(f"✅ Found {len(results)} images:")
        for i, res in enumerate(results):
            print(f"  {i+1}. {res['title']}")
            print(f"     URL: {res['image_url'][:50]}...")
            print(f"     Thumb: {res['thumbnail_url'][:50]}...")
    else:
        print("❌ No images found (or duckduckgo_search not installed/working)")

if __name__ == "__main__":
    test_image_search()
