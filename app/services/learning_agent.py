"""
Learning Agent - AI Teacher for Kids
Uses LLMs to explain topics in a fun, educational way.
Now integrated with ContentEnricher for Wikipedia + free API content!
"""

import os
from typing import Dict, Optional, Generator, List
from services.groq_llm_service import GroqLLMService
from services.gemini_llm_service import GeminiLLMService
from services.huggingface_llm_service import HuggingFaceLLMService
from services.llm_service import LLMService
from services.image_search_service import ImageSearchService
from services.content_enricher import ContentEnricher

class LearningAgent:
    """
    AI Teacher Agent that explains topics to kids.
    Now supercharged with Wikipedia, Wikimedia Commons, and Open Trivia DB!
    """

    def __init__(self):
        self.groq_service = GroqLLMService()
        self.ollama_service = LLMService()
        self.gemini_service = GeminiLLMService()
        self.hf_service = HuggingFaceLLMService()
        self.image_service = ImageSearchService()
        self.content_enricher = ContentEnricher()
        self._groq_available = None
        self._ollama_available = None

    def get_topic_images(self, topic: str) -> List[Dict]:
        """Get relevant images for the topic (from DuckDuckGo)"""
        return self.image_service.search_images(topic)

    def get_enriched_content(self, topic: str, grade: str, subject: str) -> Dict:
        """Get rich content from Wikipedia, Commons, and trivia APIs"""
        return self.content_enricher.enrich_topic(topic, grade, subject)

    def get_wiki_suggestions(self, query: str) -> List[str]:
        """Get topic suggestions from Wikipedia"""
        articles = self.content_enricher.wikipedia.search_wikipedia(query, max_results=5)
        return [a["title"] for a in articles]

    def _get_grade_level(self, grade: str) -> str:
        """Get grade-level description for age-appropriate teaching"""
        g = grade.strip()
        if g == "3":
            return "Grade 3 (ages 8-9)".upper()
        elif g == "4":
            return "Grade 4 (ages 9-10)".upper()
        elif g == "8":
            return "Grade 8 (ages 13-14)".upper()
        return f"Grade {g}".upper()

    def _get_grade_instructions(self, grade: str) -> str:
        """Get grade-specific teaching style instructions"""
        g = grade.strip()
        if g == "3":
            return """
            🎯 TEACHING STYLE FOR GRADE 3 (AGES 8-9):
            - Use VERY SIMPLE words and short sentences.
            - Explain concepts like you're talking to a curious 8-year-old.
            - Give 2-3 different real-world examples for every concept.
            - Use stories, analogies with toys, food, animals, and everyday objects.
            - Include simple step-by-step calculations.
            - Use emojis frequently to keep it fun 🎉.
            - Break everything into tiny digestible pieces.
            - End with a simple question or challenge for the student.
            """
        elif g == "4":
            return """
            🎯 TEACHING STYLE FOR GRADE 4 (AGES 9-10):
            - Use CLEAR, moderate vocabulary.
            - Explain like a friendly teacher in a classroom.
            - Give 2-3 different examples for every concept.
            - Use real-life scenarios (shopping, travel, cooking, games).
            - Include multi-step problem solving with clear steps.
            - Use diagrams described in text (no ASCII art).
            - Use emojis to make it engaging 😊.
            - Challenge students with "Try this!" questions.
            """
        elif g == "8":
            return """
            🎯 TEACHING STYLE FOR GRADE 8 (AGES 13-14):
            - Use age-appropriate academic vocabulary.
            - Explain like a knowledgeable high school teacher.
            - Give 2-3 diverse examples ranging from simple to challenging.
            - Include real-world applications and career connections.
            - Provide FORMULAS, THEOREMS, and their derivations.
            - Include multi-step problem solving with reasoning.
            - Connect concepts to higher-level thinking.
            - Challenge with "Think Deeper" questions.
            - Use proper terminology while explaining clearly.
            """
        else:
            return f"""
            🎯 TEACHING STYLE FOR GRADE {g}:
            - Use age-appropriate vocabulary and examples.
            - Give 2-3 different examples for each concept.
            - Make learning engaging and fun.
            - Break complex ideas into simple steps.
            """

    def _get_subject_instructions(self, subject: str) -> str:
        """Get subject-specific teaching instructions"""
        s = subject.lower()
        if "math" in s:
            return """
            📐 SUBJECT: MATHEMATICS
            - Focus on **Concepts**, **Formulas**, **Step-by-Step Problem Solving**.
            - Provide 2-3 worked examples with full solutions shown step-by-step.
            - Explain the 'Why' behind every formula — not just the 'How'.
            - Include common mistakes students make and how to avoid them.
            - Show multiple methods to solve the same problem.
            - End with a practice question (with answer hidden).
            """
        elif "science" in s or "physics" in s or "chemistry" in s or "biology" in s:
            return """
            🔬 SUBJECT: SCIENCE
            - Focus on **Observation**, **Hypothesis**, **Mechanism**, **Real-world Applications**.
            - Explain 'How it works' with 2-3 different examples from nature/daily life.
            - Use analogies to explain complex processes (e.g. "cell is like a factory").
            - Mention real-world applications and careers.
            - Include simple experiments students can try at home (with safety notes).
            - Connect to things students see every day.
            """
        elif "history" in s or "social" in s:
            return """
            🏛️ SUBJECT: HISTORY
            - Focus on **Storytelling**, **Timeline**, **Cause and Effect**.
            - Narrate like a story — make it dramatic and memorable.
            - Explain the 'Cause and Effect' chain of events.
            - Mention key figures, their motivations, and their impact.
            - Connect the past to the present — why it matters today.
            - Give different perspectives on the same event.
            """
        elif "english" in s or "language" in s:
            return """
            📖 SUBJECT: ENGLISH
            - Focus on **Rules**, **Usage**, **Examples**, and **Common Errors**.
            - Provide 3-4 sentence examples showing correct vs incorrect usage.
            - Explain the 'why' behind grammar rules.
            - Include practice exercises with answers.
            - Use fun sentences and stories as examples.
            - Mention nuances and context-dependent usage.
            """
        elif "geography" in s:
            return """
            🌍 SUBJECT: GEOGRAPHY
            - Focus on **Places**, **Processes**, **Interconnections**.
            - Use descriptive language to paint a picture of places.
            - Explain how natural processes shape our world.
            - Connect geography to climate, culture, and economy.
            - Use 2-3 real-world examples for each concept.
            - Include maps described in text (no ASCII art).
            """
        elif "computer" in s:
            return """
            💻 SUBJECT: COMPUTER SCIENCE
            - Focus on **Concepts**, **Logic**, **Real-world Applications**.
            - Explain how technology works in simple terms.
            - Give 2-3 examples of how concepts are used in real apps/websites.
            - Include simple code or pseudocode examples where appropriate.
            - Connect to things students use (games, apps, social media).
            - Mention exciting career paths in tech.
            """
        else:
            return """
            📚 SUBJECT: GENERAL
            - Focus on clear, logical explanation.
            - Break down complex ideas into simple terms.
            - Give 2-3 different examples for each concept.
            - Use stories and analogies to make it memorable.
            """

    def _build_teach_prompt(self, grade: str, subject: str, user_query: str, mode: str = "initial", previous_content: str = None) -> str:
        """Build a rich, grade-aware teaching prompt"""
        grade_desc = self._get_grade_level(grade)
        grade_style = self._get_grade_instructions(grade)
        subject_style = self._get_subject_instructions(subject)
        
        if mode == "initial":
            prompt = f"""
You are a WONDERFUL, PATIENT, and ENTHUSIASTIC teacher for {grade_desc}.

📚 TODAY'S LESSON: "{user_query}" ({subject})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{grade_style}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{subject_style}

CRITICAL STRUCTURE — Follow this EXACTLY:

1️⃣ INTRODUCTION (2-3 paragraphs)
   - Start with a fun hook or question that grabs attention
   - Explain WHY this topic matters in real life
   - Connect to things the student already knows

2️⃣ MAIN EXPLANATION (4-6 paragraphs)
   - Break the concept into small, logical steps
   - After each step, give A DIFFERENT REAL-WORLD EXAMPLE
   - Use analogies and comparisons
   - Include DIFFERENT examples — not the same one repeated

3️⃣ EXAMPLES & APPLICATIONS (3-5 examples)
   - Example 1: Simple, everyday situation
   - Example 2: More challenging scenario
   - Example 3: Fun/interesting application
   - Example 4: Cross-topic connection
   - Show step-by-step solutions where applicable

4️⃣ COMMON MISTAKES & TIPS (2-3 points)
   - What do students usually get wrong?
   - How to avoid those mistakes
   - Memory tricks or shortcuts

5️⃣ SUMMARY & PRACTICE
   - Quick recap of main points
   - A practice question for the student
   - Encouraging closing message

EXAMPLES OF DIFFERENT TEACHING APPROACHES (pick the best one):
- "Think of it like..." (analogy approach)
- "Let's look at an example..." (example-first approach)
- "Have you ever wondered why..." (curiosity approach)
- "Let's break this down step by step..." (procedural approach)

RULES:
- Use Markdown headers (##, ###) for organization
- Use emojis throughout to make it fun 🎉
- Give MULTIPLE DIFFERENT examples, never just one
- Show step-by-step solutions for problems
- Use bullet points and tables for clarity
- DO NOT generate ASCII art diagrams
- DO NOT use rigid templates like "Fun Fact" boxes
- Adapt vocabulary completely to {grade_desc} level
- Make every sentence clear and engaging
"""
        else:
            prompt = f"""
You are a WONDERFUL, PATIENT, and ENTHUSIASTIC teacher for {grade_desc}.

The student wants to learn MORE about "{user_query}" ({subject}).

Here's what we already covered:
"{previous_content[:500]}..."

Now go DEEPER:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{grade_style}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{subject_style}

NEW CONTENT REQUIREMENTS:
- Provide ADVANCED concepts not yet covered
- Go deeper into the topic
- Give 2-3 NEW examples not mentioned before
- Connect to real-world applications
- Challenge the student with deeper questions
- DO NOT repeat what was already said
"""
        return prompt.strip()

    def teach_topic_stream(self, grade: str, subject: str, topic: str, custom_query: str = None) -> Generator[str, None, None]:
        """
        Generates a detailed lesson for the given topic (Streaming).
        """
        user_query = custom_query if custom_query else topic
        prompt = self._build_teach_prompt(grade, subject, user_query, mode="initial")
        
        # Try Groq Stream first
        try:
            for chunk in self.groq_service.generate_stream(prompt):
                yield chunk
            return
        except Exception as e:
            print(f"Groq stream failed: {e}")

        # Fallback to Ollama (local, no API key needed, already running)
        try:
            print("Trying Ollama (local)...")
            for chunk in self.ollama_service.generate_stream(prompt):
                yield chunk
            return
        except Exception as e:
            print(f"Ollama fallback failed: {e}")

        # Fallback to Gemini if key is configured
        try:
            if os.getenv('GEMINI_API_KEY'):
                print("Attempting Gemini fallback...")
                full_text = self.gemini_service.generate_text(prompt)
                if full_text:
                    yield full_text
                    return
            else:
                print("Gemini: no API key configured, skipping.")
        except Exception as e:
            print(f"Gemini fallback failed: {e}")

        # Fallback to HuggingFace if key is configured
        try:
            if os.getenv('HUGGINGFACE_API_KEY'):
                print("Attempting HuggingFace fallback...")
                full_text = self.hf_service.generate_text(prompt)
                if full_text:
                    yield full_text
                    return
            else:
                print("HuggingFace: no API key configured, skipping.")
        except Exception as e:
            print(f"HuggingFace fallback failed: {e}")

        # All services failed
        yield "😔 Sorry, I couldn't generate the lesson at this time. Please make sure Ollama is running (`ollama serve`) and try again."

    def teach_more_stream(self, grade: str, subject: str, topic: str, previous_content: str) -> Generator[str, None, None]:
        """
        Generates MORE advanced details (Streaming).
        """
        prompt = self._build_teach_prompt(grade, subject, topic, mode="more", previous_content=previous_content)
        
        try:
            for chunk in self.groq_service.generate_stream(prompt):
                yield chunk
            return
        except Exception as e:
            print(f"Groq stream failed: {e}")

        # Fallback to Ollama (local)
        try:
            print("Trying Ollama (local)...")
            for chunk in self.ollama_service.generate_stream(prompt):
                yield chunk
            return
        except Exception as e:
            print(f"Ollama fallback failed: {e}")

        # Fallback to Gemini if key is configured
        try:
            if os.getenv('GEMINI_API_KEY'):
                full_text = self.gemini_service.generate_text(prompt)
                if full_text:
                    yield full_text
                    return
        except Exception as e:
            print(f"Gemini fallback failed: {e}")

        # All services failed
        yield "😔 Sorry, I couldn't generate more information. Please make sure Ollama is running (`ollama serve`) and try again."

    def teach_topic(self, grade: str, subject: str, topic: str, custom_query: str = None) -> str:
        """Legacy non-streaming method"""
        chunks = []
        for chunk in self.teach_topic_stream(grade, subject, topic, custom_query):
            chunks.append(chunk)
        return "".join(chunks)

    def teach_more(self, grade: str, subject: str, topic: str, previous_content: str) -> str:
        """Legacy non-streaming method"""
        chunks = []
        for chunk in self.teach_more_stream(grade, subject, topic, previous_content):
            chunks.append(chunk)
        return "".join(chunks)

    def _generate(self, prompt: str) -> str:
        """Helper to call LLMs (Deprecated internal use)"""
        return self.groq_service.generate_text(prompt)

    def generate_quiz(self, grade: str, subject: str, topic: str) -> List[Dict]:
        """Generate a mini-quiz for the topic"""
        prompt = f"""
        Create a mini-quiz for Grade {grade} students about "{topic}" ({subject}).
        Generate 3 multiple-choice questions.
        
        Return ONLY valid JSON in this format:
        [
            {{
                "question": "Question text here?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_index": 0,
                "explanation": "Why this is correct."
            }}
        ]
        """
        try:
            # We use the non-streaming method and parse JSON
            response = self.groq_service.generate_text(prompt)
            # Basic cleanup to ensure we get just the JSON list
            import json
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            return json.loads(response)
        except Exception as e:
            print(f"Quiz generation failed: {e}")
            return []

    def generate_flashcards(self, grade: str, subject: str, topic: str) -> List[Dict]:
        """Generate flashcards for the topic"""
        prompt = f"""
        Create 5 educational flashcards for Grade {grade} students about "{topic}" ({subject}).
        Each card should have a "front" (concept/question) and "back" (definition/answer).
        
        Return ONLY valid JSON in this format:
        [
            {{
                "front": "What is photosynthesis?",
                "back": "The process by which plants make food using sunlight."
            }}
        ]
        """
        try:
            response = self.groq_service.generate_text(prompt)
            import json
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            return json.loads(response)
        except Exception as e:
            print(f"Flashcard generation failed: {e}")
            return []
