#!/usr/bin/env python3
"""
Test script for Video Search
"""
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.image_search_service import ImageSearchService

def test_video_search():
    print("Testing Video Search...")
    service = ImageSearchService()
    
    query = "Human Skeleton"
    print(f"Searching for: {query}")
    
    results = service.search_videos(query)
    
    if results:
        print(f"✅ Found {len(results)} videos:")
        for i, res in enumerate(results):
            print(f"  {i+1}. {res['title']}")
            print(f"     URL: {res['video_url'][:50]}...")
            print(f"     Duration: {res['duration']}")
    else:
        print("❌ No videos found (or duckduckgo_search not installed/working)")

if __name__ == "__main__":
    test_video_search()
