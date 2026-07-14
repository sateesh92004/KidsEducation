# Implementation Plan: Enhanced Question Generation & Tracking System

## Requirements

### 1. Fix Submit Test Button
- Ensure Submit button is always visible and functional
- Remove any visibility logic that might hide it

### 2. Generate 100 Questions (Instead of 3 sets of 20)
- Change from 3 papers × 20 questions = 60 total
- To: 1 large pool of 100 unique questions per topic

### 3. Duplicate Detection
- Agent checks for duplicate/repetitive questions
- Uses semantic similarity to detect near-duplicates
- Ensures all 100 questions are unique

### 4. User Question Tracking
- Track which questions each user has answered
- Mark questions as "used" for specific users
- Never show same question twice to same user

### 5. Question Selection Logic
- When user starts test: Select 20 random questions from unused pool
- If < 20 unused questions: Show error message
- Error: "Not enough questions available. Please ask admin to generate more questions."

## Implementation Steps

### Step 1: Fix Submit Button (Immediate)
- File: `app/ui/test_screen.py`
- Remove visibility logic for submit button
- Ensure it's always enabled

### Step 2: Update Constants
- File: `app/utils/constants.py`
- Change `QUESTIONS_PER_PAPER` to 100
- Change `PAPERS_PER_GENERATION` to 1

### Step 3: Create Question Pool System
- File: `app/services/question_pool_service.py` (NEW)
- Manages question pools per topic
- Tracks user-question relationships
- Selects unused questions for tests

### Step 4: Add Duplicate Detection to Agent
- File: `app/services/paper_generation_agent.py`
- Add duplicate detection after generation
- Use text similarity comparison
- Remove duplicates before saving

### Step 5: Create User Question Tracking
- File: `app/data/user_questions.json` (NEW)
- Structure:
  ```json
  {
    "username": {
      "grade_subject_topic": {
        "answered_questions": [1, 2, 3, ...],
        "last_test_date": "2025-12-06"
      }
    }
  }
  ```

### Step 6: Update Question Service
- File: `app/services/question_service.py`
- Integrate with question pool service
- Use new selection logic

### Step 7: Update Test Screen
- File: `app/ui/test_screen.py`
- Check available questions before starting
- Show appropriate error messages

## Files to Create
1. `app/services/question_pool_service.py`
2. `app/data/user_questions.json`

## Files to Modify
1. `app/ui/test_screen.py` - Fix submit button
2. `app/utils/constants.py` - Update question counts
3. `app/services/paper_generation_agent.py` - Add duplicate detection
4. `app/services/question_service.py` - Integrate pool service
5. `app/ui/student_dashboard.py` - Add question availability check

## Testing Plan
1. Test submit button works
2. Generate 100 questions
3. Verify no duplicates
4. Test user tracking
5. Test question selection
6. Test error message when < 20 questions available

---

**Priority**: Fix submit button first, then implement new system
