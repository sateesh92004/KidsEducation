"""
Content Enricher - Fetches rich educational content from free public APIs
Combines Wikipedia, Wikimedia Commons, and Open Trivia DB for rich kid-friendly content
"""

import requests
import json
import random
from typing import Dict, List, Optional, Generator
from datetime import datetime
import re
import html

try:
    import wikipediaapi
    # Test that it actually works (Python 3.9 doesn't support X|Y syntax used in newer versions)
    test = wikipediaapi.__version__
    WIKI_AVAILABLE = True
except Exception:
    # wikipediaapi may fail on Python 3.9 due to X|Y union syntax
    WIKI_AVAILABLE = False


class WikipediaEnricher:
    """Fetches and structures content from Wikipedia API"""

    def __init__(self):
        self.user_agent = "KidsEducationApp/1.0 (educational app for kids)"
        self.wiki = None
        if WIKI_AVAILABLE:
            self.wiki = wikipediaapi.Wikipedia(
                language='en',
                user_agent=self.user_agent
            )

    def search_wikipedia(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search Wikipedia for relevant articles"""
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "srlimit": max_results,
                "srprop": "snippet|titlesnippet"
            }
            headers = {"User-Agent": self.user_agent}
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            data = resp.json()

            results = []
            for item in data.get("query", {}).get("search", []):
                snippet = item.get("snippet", "")
                # Clean HTML tags from snippet
                snippet = re.sub(r'<[^>]+>', '', snippet)
                snippet = html.unescape(snippet)

                results.append({
                    "title": item.get("title", ""),
                    "snippet": snippet,
                    "page_id": item.get("pageid", 0),
                    "relevance": item.get("relevance", 0)
                })
            return results
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return []

    def get_article_extract(self, title: str, sentences: int = 15) -> Optional[Dict]:
        """Get full article extract from Wikipedia"""
        try:
            if self.wiki:
                page = self.wiki.page(title)
                if page.exists():
                    return {
                        "title": page.title,
                        "summary": page.summary[:2000],
                        "full_text": page.text[:5000],
                        "url": page.fullurl,
                        "categories": [cat for cat in page.categories.keys()][:10]
                    }

            # Fallback to REST API
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(title)}"
            headers = {"User-Agent": self.user_agent}
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "title": data.get("title", title),
                    "summary": data.get("extract", ""),
                    "full_text": data.get("extract", ""),
                    "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                    "categories": []
                }
            return None
        except Exception as e:
            print(f"Wikipedia extract error for '{title}': {e}")
            return None

    def get_did_you_know(self, topic: str) -> List[str]:
        """Get fun facts from Wikipedia 'Did you know' section"""
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "search",
                "srsearch": f'"{topic}" "did you know"',
                "format": "json",
                "srlimit": 5,
                "srprop": "snippet"
            }
            headers = {"User-Agent": self.user_agent}
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            data = resp.json()

            facts = []
            for item in data.get("query", {}).get("search", []):
                snippet = item.get("snippet", "")
                snippet = re.sub(r'<[^>]+>', '', snippet)
                snippet = html.unescape(snippet)
                if snippet.strip():
                    facts.append(snippet[:200])
            return facts[:3]
        except Exception as e:
            print(f"Did you know error: {e}")
            return []

    def structure_for_kids(self, topic: str, article: Dict) -> Dict:
        """Structure Wikipedia content into kid-friendly sections"""
        if not article:
            return {}

        text = article.get("full_text", article.get("summary", ""))
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

        # Simple section extraction
        sections = {"introduction": [], "main_content": [], "fun_facts": [], "examples": []}

        current_section = "introduction"
        for para in paragraphs[:30]:  # Limit to first 30 paragraphs
            para_lower = para.lower()

            if any(word in para_lower for word in ["history", "background", "origin"]):
                current_section = "main_content"
            elif any(word in para_lower for word in ["example", "example:", "for example", "for instance"]):
                current_section = "examples"
            elif any(word in para_lower for word in ["fun fact", "interesting", "did you know"]):
                current_section = "fun_facts"

            if current_section in sections:
                if len(para) > 30:  # Skip very short lines
                    sections[current_section].append(para)

        return {
            "topic": topic,
            "title": article.get("title", topic),
            "summary": article.get("summary", ""),
            "introduction": sections["introduction"][:3],
            "main_content": sections["main_content"][:8],
            "examples": sections["examples"][:5],
            "fun_facts": sections["fun_facts"][:3],
            "url": article.get("url", ""),
            "source": "Wikipedia",
            "fetched_at": datetime.now().isoformat()
        }


class WikimediaCommons:
    """Fetches educational images from Wikimedia Commons"""

    def __init__(self):
        self.user_agent = "KidsEducationApp/1.0"

    def search_commons(self, query: str, max_results:  int = 8) -> List[Dict]:
        """Search Wikimedia Commons for educational images"""
        try:
            url = "https://commons.wikimedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "srlimit": max_results,
                "srnamespace": "6",  # File namespace
                "srprop": "snippet|size|wordcount"
            }
            headers = {"User-Agent": self.user_agent}
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            data = resp.json()

            results = []
            for item in data.get("query", {}).get("search", []):
                title = item.get("title", "").replace("File:", "")
                results.append({
                    "title": title,
                    "description": item.get("snippet", ""),
                    "page_id": item.get("pageid", 0),
                })
            return results
        except Exception as e:
            print(f"Wikimedia Commons search error: {e}")
            return []

    def get_image_url(self, filename: str) -> Optional[str]:
        """Get the actual image URL from a Commons filename"""
        try:
            url = "https://commons.wikimedia.org/w/api.php"
            params = {
                "action": "query",
                "titles": f"File:{filename}",
                "prop": "imageinfo",
                "iiprop": "url|size|mime",
                "format": "json",
                "iiurlwidth": 400,
            }
            headers = {"User-Agent": self.user_agent}
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            data = resp.json()

            pages = data.get("query", {}).get("pages", {})
            for page_id, page_data in pages.items():
                if page_id != "-1":
                    image_info = page_data.get("imageinfo", [])
                    if image_info:
                        return {
                            "url": image_info[0].get("url", ""),
                            "thumb_url": image_info[0].get("thumburl", ""),
                            "description_url": image_info[0].get("descriptionurl", ""),
                            "mime": image_info[0].get("mime", ""),
                        }
            return None
        except Exception as e:
            print(f"Commons image URL error for '{filename}': {e}")
            return None


class OpenTriviaDB:
    """Fetches quiz questions from Open Trivia DB (free, no API key needed)"""

    CATEGORY_MAP = {
        "general": 9,
        "science": 17,
        "math": 19,
        "history": 23,
        "geography": 22,
        "computers": 18,
        "animals": 27,
        "nature": 17,
    }

    def __init__(self):
        self.base_url = "https://opentdb.com/api.php"

    def get_questions(self, category: str = "general", amount: int = 3, difficulty: str = "easy") -> List[Dict]:
        """Fetch trivia questions from Open Trivia DB"""
        try:
            cat_id = self.CATEGORY_MAP.get(category.lower(), 9)
            params = {
                "amount": amount,
                "category": cat_id,
                "difficulty": difficulty,
                "type": "multiple"
            }
            resp = requests.get(self.base_url, params=params, timeout=10)
            data = resp.json()

            if data.get("response_code") == 0:
                questions = []
                for item in data.get("results", []):
                    # Decode HTML entities
                    question_text = html.unescape(item.get("question", ""))
                    correct = html.unescape(item.get("correct_answer", ""))
                    incorrect = [html.unescape(i) for i in item.get("incorrect_answers", [])]

                    # Shuffle options
                    options = incorrect + [correct]
                    random.shuffle(options)

                    questions.append({
                        "question": question_text,
                        "options": options,
                        "correct_answer": correct,
                        "difficulty": item.get("difficulty", "easy"),
                        "category": item.get("category", ""),
                    })
                return questions
            return []
        except Exception as e:
            print(f"OpenTriviaDB error: {e}")
            return []


class ContentEnricher:
    """
    Master enricher that combines Wikipedia, Wikimedia Commons, Open Trivia DB,
    and the existing LLM agent for rich kid-friendly content
    """

    def __init__(self):
        self.wikipedia = WikipediaEnricher()
        self.commons = WikimediaCommons()
        self.trivia = OpenTriviaDB()
        self._cache = {}

    def enrich_topic(self, topic: str, grade: str, subject: str) -> Dict:
        """
        Get enriched content for a topic from multiple sources.
        Returns structured content with Wikipedia article, images, fun facts, quiz
        """
        # Check cache first
        cache_key = f"{topic}:{grade}:{subject}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        result = {
            "topic": topic,
            "grade": grade,
            "subject": subject,
            "wikipedia": None,
            "images": [],
            "fun_facts": [],
            "quiz": [],
            "related_topics": [],
            "source_summary": "",
            "has_rich_content": False,
        }

        # 1. Wikipedia content
        articles = self.wikipedia.search_wikipedia(topic)
        if articles:
            best = articles[0]
            article = self.wikipedia.get_article_extract(best["title"])
            if article:
                kid_struct = self.wikipedia.structure_for_kids(topic, article)
                result["wikipedia"] = kid_struct
                result["source_summary"] = article.get("summary", "")[:500]
                result["has_rich_content"] = True

                # Fun facts from Wikipedia
                dyk = self.wikipedia.get_did_you_know(topic)
                if dyk:
                    result["fun_facts"].extend(dyk)

        # 2. Wikimedia Commons images
        commons_images = self.commons.search_commons(f"{topic} educational diagram")
        for img in commons_images[:4]:
            img_url = self.commons.get_image_url(img["title"])
            if img_url:
                result["images"].append({
                    "title": img["title"],
                    "url": img_url.get("url", ""),
                    "thumb_url": img_url.get("thumb_url", ""),
                    "source": "Wikimedia Commons",
                })

        # 3. Generate some fun facts from the topic itself
        if not result["fun_facts"]:
            # Create fun engaging facts based on subject
            subject_facts = self._generate_subject_facts(topic, subject)
            result["fun_facts"].extend(subject_facts)

        # 4. Related topics
        if articles:
            result["related_topics"] = [
                a["title"] for a in articles[1:4]
            ]

        # Cache
        self._cache[cache_key] = result
        return result

    def _generate_subject_facts(self, topic: str, subject: str) -> List[str]:
        """Generate subject-specific fun facts"""
        facts_map = {
            "mathematics": [
                f"Did you know? {topic} helps us solve real-world problems every day!",
                f"Ancient mathematicians were the first to explore {topic}!",
                f"{topic} is used by architects to build amazing structures!",
            ],
            "science": [
                f"Scientists use {topic} to understand how the world works!",
                f"Every day, new discoveries are made about {topic}!",
                f"Nature is full of amazing examples of {topic}!",
            ],
            "english": [
                f"Words are powerful tools — and {topic} helps you use them better!",
                f"Did you know English has words from over 100 languages?",
                f"Writing about {topic} can transport readers to new worlds!",
            ],
            "history": [
                f"The story of {topic} shaped the world we live in today!",
                f"Archaeologists are still discovering new things about {topic}!",
                f"Different cultures experienced {topic} in unique ways!",
            ],
            "geography": [
                f"Our amazing planet has countless examples of {topic}!",
                f"Satellites help us study {topic} from space!",
                f"Every continent has unique {topic} features!",
            ],
        }

        subj_lower = subject.lower()
        for key, facts in facts_map.items():
            if key in subj_lower:
                return facts

        return [
            f"Let's explore the amazing world of {topic}!",
            f"{topic} is more fascinating than you might think!",
            f"Learning about {topic} opens up new ways of seeing the world!",
        ]

    def get_kids_quiz(self, topic: str, subject: str) -> List[Dict]:
        """Get kid-friendly quiz questions from Open Trivia DB"""
        # Map subject to trivia category
        category_map = {
            "math": "math",
            "science": "science",
            "history": "history",
            "geography": "geography",
            "computer": "computers",
        }

        category = "general"
        for key, val in category_map.items():
            if key in subject.lower():
                category = val
                break

        return self.trivia.get_questions(category=category, amount=3, difficulty="easy")
