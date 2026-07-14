# Testing Guide for KidsEducation App Fixes

## Test Environment Setup

Make sure you have:
- ✅ Ollama running: `brew services start ollama`
- ✅ Mistral model installed: `ollama pull mistral`
- ✅ Python dependencies installed
- ✅ App ready to run: `python app/main.py`

---

## Test Case 1: Percentage Display Fix

### Steps:
1. Start the app: `python app/main.py`
2. Login as admin (username: `sateesh92004`)
3. Generate 10 question papers for any grade/subject/topic
4. Logout and login as a student (or create new account)
5. Select a test and complete at least 5 questions
6. Submit the test

### Expected Results:
- ✅ Score percentage is clearly visible at the top
- ✅ Percentage uses golden/yellow color (#FFD700)
- ✅ Font size is large and readable (56pt)
- ✅ Score card is properly sized (150-200px height)
- ✅ All stats are aligned properly

### Example Screenshot Check:
- Score should show like: **75.0%** (large, yellow text)
- Correct answers below: **15/20**
- Grade/Subject/Topic visible on the right

---

## Test Case 2: One-by-One Question Review

### Steps:
1. Complete the test from Test Case 1
2. After submission, view the test results
3. In the "Answer Review" section, observe the navigation

### Expected Results:
- ✅ Only ONE question card is visible at a time
- ✅ Question counter shows: "Question X of 30"
- ✅ "← Previous Question" button is visible
- ✅ "Next Question →" button is visible
- ✅ Previous button is disabled on first question
- ✅ Next button is disabled on last question
- ✅ Can navigate forward and backward through all questions
- ✅ Each question shows:
  - Question number and status (✅ Correct / ❌ Incorrect)
  - Question text
  - Your answer (highlighted in green if correct, red if wrong)
  - Correct answer (if you were wrong)
  - Explanation

### Expected Navigation:
```
Question 1 of 30: [← Previous disabled] [Question 1 of 30] [Next Question →]
↓ (click Next)
Question 2 of 30: [← Previous Question] [Question 2 of 30] [Next Question →]
↓ (click Next repeatedly to reach last)
Question 30 of 30: [← Previous Question] [Question 30 of 30] [Next disabled]
```

---

## Test Case 3: Paper Randomization

### Scenario A: Different Papers on Multiple Tests

#### Setup:
1. Login as admin
2. Generate exactly **10 question papers** for:
   - Grade: 9
   - Subject: Science
   - Topic: Photosynthesis
3. Logout

#### Test Steps:
1. Login as student (or create new account)
2. Select Grade 9, Science, Photosynthesis → Start Test
3. **Note down the first 3 questions**
4. Logout (without completing)
5. Login as student again
6. Select same test → Start Test
7. **Check if different questions appear**
8. Repeat steps 4-7 two more times

#### Expected Results:
- ✅ Test 1 shows different questions than Test 2
- ✅ Test 2 shows different questions than Test 3
- ✅ Test 3 shows different questions than Test 1
- ✅ All tests cover the same topic (Photosynthesis)
- ✅ No duplicate question sets appear

### Scenario B: Generated Papers Have Variety

#### Setup:
1. Generate 3 papers for a topic
2. Review the generated JSON files in `app/data/`

#### Check Files:
```bash
# Look at generated files
ls app/data/paper_*.json
cat app/data/paper_9_Science_Photosynthesis_p1.json
cat app/data/paper_9_Science_Photosynthesis_p2.json
cat app/data/paper_9_Science_Photosynthesis_p3.json
```

#### Expected Results:
- ✅ Each paper has 30 unique questions
- ✅ Paper 1, 2, and 3 have completely different questions
- ✅ Question topics vary (definitions, applications, examples, etc.)
- ✅ Difficulty levels are mixed within each paper
- ✅ Questions are well-formatted JSON with proper structure

### Scenario C: Verify Admin Can See Papers

#### Steps:
1. Login as admin
2. Navigate to view generated papers
3. Check that multiple papers are listed

#### Expected Results:
- ✅ Admin can see all generated papers
- ✅ Papers are indexed 1, 2, 3, etc.
- ✅ Each paper is independent and can be viewed

---

## Quick Verification Checklist

Use this checklist after applying fixes:

### Percentage Display ✅
- [ ] Percentage is visible in results screen
- [ ] Font size is appropriate (56pt)
- [ ] Color is golden/yellow (#FFD700)
- [ ] Positioned at top of score card
- [ ] No overlapping with other elements

### Question Review Navigation ✅
- [ ] Only one question shows per screen
- [ ] Question counter is visible ("Question X of 30")
- [ ] Previous/Next buttons work correctly
- [ ] Buttons are properly enabled/disabled
- [ ] All question details visible (question, answers, explanation)
- [ ] Navigation is smooth (no lag)

### Paper Randomization ✅
- [ ] Different papers selected on each test
- [ ] Multiple papers exist for topics
- [ ] Questions vary between papers
- [ ] No visible repetition of question sets
- [ ] Random selection is working

---

## Troubleshooting

### Problem: Percentage not showing
- **Solution**: Check if PyQt6 is properly installed: `pip install PyQt6`
- **Check font availability**: Try using "Arial" or "System" fonts

### Problem: Previous/Next buttons not working
- **Solution**: Ensure `display_current_question_review()` method is called
- **Check**: Button signals are connected properly in code

### Problem: Same papers appearing multiple times
- **Solution**: Verify `random.choice()` is used in `start_test()`
- **Check**: Multiple papers actually exist in `app/data/`
- **Generate more papers**: Use admin panel to generate 10+ papers

### Problem: Questions look identical in different papers
- **Solution**: Increase temperature in llm_service.py (already done to 0.9)
- **Check**: Ollama is running with good resources
- **Generate fresh**: Delete old papers and regenerate

---

## Performance Notes

- ⚡ Results review should load instantly
- ⚡ Navigation between questions should be smooth
- ⚡ Paper selection should be immediate
- ⚡ No noticeable lag when switching between questions

---

## Success Criteria

All three issues are fixed when:

1. ✅ **Percentage Display**: Users clearly see their score percentage in gold/yellow, prominent and readable
2. ✅ **Question Review**: After a test, users navigate one question at a time, not all at once
3. ✅ **Paper Variety**: Students taking multiple tests get different papers and different questions

