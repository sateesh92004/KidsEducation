"""
Image Search Service
Finds educational diagrams and images for topics.
"""

from typing import List, Dict, Optional
try:
    from duckduckgo_search import DDGS
    DDG_AVAILABLE = True
except ImportError:
    DDG_AVAILABLE = False
    print("Warning: duckduckgo_search not installed.")

class ImageSearchService:
    """Service to find images/diagrams for topics"""
    
    def __init__(self):
        self.max_results = 3

    def search_images(self, query: str, context: str = "educational diagram") -> List[Dict]:
        """
        Search for images related to the query.
        Returns a list of dicts with 'title', 'image', 'thumbnail', 'url'.
        """
        if not DDG_AVAILABLE:
            return []
            
        # Try multiple search terms if first fails
        search_terms = [
            f"{query} diagram",
            f"{query} labeled diagram",
            f"{query} educational image"
        ]
        
        results = []
        
        for term in search_terms:
            if results: break
            
            try:
                with DDGS() as ddgs:
                    ddg_results = ddgs.images(
                        term,
                        region="wt-wt",
                        safesearch="on",
                        max_results=self.max_results
                    )
                    
                    for r in ddg_results:
                        results.append({
                            "title": r.get("title", ""),
                            "image_url": r.get("image", ""),
                            "thumbnail_url": r.get("thumbnail", ""),
                            "source": r.get("url", "")
                        })
            except Exception as e:
                print(f"Image search error for '{term}': {e}")
            
        return results
            
    def search_videos(self, query: str, context: str = "educational video for kids") -> List[Dict]:
        """
        Search for videos related to the query.
        """
        if not DDG_AVAILABLE:
            return []
            
        search_term = f"{query} {context}"
        results = []
        
        try:
            with DDGS() as ddgs:
                ddg_results = ddgs.videos(
                    search_term,
                    region="wt-wt",
                    safesearch="on",
                    max_results=self.max_results
                )
                
                for r in ddg_results:
                    # DuckDuckGo video results usually have 'content' (url), 'title', 'images' (thumbnail)
                    # We need to be careful with the structure
                    results.append({
                        "title": r.get("title", ""),
                        "video_url": r.get("content", ""),
                        "thumbnail_url": r.get("images", {}).get("medium", "") if isinstance(r.get("images"), dict) else "",
                        "duration": r.get("duration", "")
                    })
                    
        except Exception as e:
            print(f"Video search error: {e}")
            
        return results
