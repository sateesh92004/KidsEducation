# 🧠 Interactive Learning Update

I have added **Quizzes** and **Flashcards** to make learning active and fun!

## ✨ New Features

### 1. 📝 Flashcards
- **What**: After the AI teaches a topic, it automatically generates **5 interactive flashcards**.
- **How**: You see a card with a question/concept. Click it to **flip** and reveal the answer!
- **UI**: Beautiful blue/orange cards with smooth flipping animation (simulated).

### 2. 🧠 Mini-Quiz
- **What**: A quick **3-question multiple-choice quiz** to test understanding.
- **How**: Select an answer and click "Submit".
- **Feedback**: Instant feedback!
    - ✅ **Correct**: Green success message.
    - ❌ **Incorrect**: Red message with the **correct explanation**.

## 🛠️ Technical Details

- **New Widgets**: Created `FlashCardWidget` and `QuizWidget` in `ui/interactive_widgets.py`.
- **Parallel Loading**: The app fetches the lesson text, images, videos, flashcards, and quiz **simultaneously** so you don't have to wait.
- **Dynamic UI**: The interactive section appears automatically below the lesson when the content is ready.

## 🚀 How to Test

1. **Restart the App**:
   ```bash
   ./START_APP.command
   ```
2. **Go to Learning Mode**:
   - Login -> Learning Tab.
3. **Ask a Topic**:
   - Type: **"Solar System"**.
4. **Scroll Down**:
   - Below the lesson and videos, you will see:
     - **Flashcards**: Click "Next" to cycle through them. Click the card to flip!
     - **Quick Quiz**: Try to answer the questions!

Enjoy the interactive learning! 🎓
