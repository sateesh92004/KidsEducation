# 🗄️ Database Migration Plan - SQLite Implementation

## 🎯 Objective

Migrate from JSON files to SQLite database for:
- User management & authentication
- Question storage (by Grade, Subject, Topic)
- User-question tracking (answered questions)
- Test results storage
- Admin custom prompts

---

## 📊 Database Schema

### **1. Users Table**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,  -- 'student' or 'admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **2. Questions Table**
```sql
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade TEXT NOT NULL,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    question_text TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_answer TEXT NOT NULL,  -- 'A', 'B', 'C', or 'D'
    explanation TEXT,
    difficulty TEXT,  -- 'Easy', 'Medium', 'Hard'
    question_type TEXT,  -- 'word_problem', 'complex', 'conceptual', 'application'
    generated_by TEXT,  -- 'groq', 'gemini', 'huggingface'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(grade, subject, topic, question_text)  -- Prevent exact duplicates
);
```

### **3. User Answered Questions Table**
```sql
CREATE TABLE user_answered_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (question_id) REFERENCES questions(id),
    UNIQUE(user_id, question_id)  -- User can answer each question only once
);
```

### **4. Test Results Table**
```sql
CREATE TABLE test_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    grade TEXT NOT NULL,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    total_questions INTEGER NOT NULL,
    correct_answers INTEGER NOT NULL,
    wrong_answers INTEGER NOT NULL,
    score_percentage REAL NOT NULL,
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### **5. Test Answers Table** (Detailed answers for each test)
```sql
CREATE TABLE test_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_result_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    user_answer TEXT NOT NULL,  -- 'A', 'B', 'C', or 'D'
    is_correct BOOLEAN NOT NULL,
    FOREIGN KEY (test_result_id) REFERENCES test_results(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);
```

### **6. Custom Prompts Table** (Admin feature)
```sql
CREATE TABLE custom_prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER NOT NULL,
    grade TEXT NOT NULL,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    custom_prompt TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id)
);
```

---

## 🏗️ Implementation Steps

### **Phase 1: Database Setup**
1. Create `app/database/db_manager.py` - Database connection & initialization
2. Create `app/database/schema.sql` - SQL schema definitions
3. Create `app/database/models.py` - Python models for each table

### **Phase 2: Database Services**
1. Create `app/services/db_user_service.py` - User CRUD operations
2. Create `app/services/db_question_service.py` - Question CRUD operations
3. Create `app/services/db_test_service.py` - Test & results operations
4. Create `app/services/db_prompt_service.py` - Custom prompts management

### **Phase 3: Migration**
1. Migrate user authentication to database
2. Migrate question storage to database
3. Migrate test results to database
4. Update all UI components to use database services

### **Phase 4: New Features**
1. Admin custom prompt interface
2. Enhanced question retrieval (unused questions for user)
3. Comprehensive test history
4. Analytics dashboard

---

## 🔄 Workflow Changes

### **Current (JSON-based):**
```
Generate → Save to JSON files → Load from JSON → Track in separate JSON
```

### **New (Database):**
```
Generate → Save to SQLite → Query unused questions → Track in DB
```

---

## 📝 Files to Create

### **Database Layer:**
1. `app/database/__init__.py`
2. `app/database/db_manager.py` - Connection management
3. `app/database/schema.sql` - Database schema
4. `app/database/models.py` - Data models

### **Services:**
5. `app/services/db_user_service.py`
6. `app/services/db_question_service.py`
7. `app/services/db_test_service.py`
8. `app/services/db_prompt_service.py`

### **UI Updates:**
9. Update `app/ui/admin_panel.py` - Add custom prompt feature
10. Update `app/ui/test_screen.py` - Use database queries
11. Update `app/ui/login_screen.py` - Database authentication

---

## 🎯 Key Features

### **1. Question Management**
- ✅ Store all questions in database
- ✅ Organize by Grade, Subject, Topic
- ✅ Track question metadata (difficulty, type, source)
- ✅ Prevent duplicate questions

### **2. User Tracking**
- ✅ Flag answered questions per user
- ✅ Never show same question twice
- ✅ Track user progress

### **3. Admin Custom Prompts**
- ✅ Admin can specify custom prompt
- ✅ LLM uses custom prompt for generation
- ✅ Store prompts in database
- ✅ Reuse prompts for consistency

### **4. Test Results**
- ✅ Store all test results
- ✅ Detailed answer tracking
- ✅ Historical performance data
- ✅ Analytics and reporting

---

## 💡 Benefits

1. **Performance**: Faster queries than JSON files
2. **Scalability**: Can handle thousands of questions
3. **Integrity**: Foreign keys ensure data consistency
4. **Flexibility**: Complex queries for analytics
5. **Reliability**: ACID transactions
6. **No Server**: SQLite runs locally, no setup needed

---

## 🧪 Testing Plan

1. Create database and tables
2. Migrate existing users
3. Migrate existing questions
4. Test question retrieval
5. Test user tracking
6. Test custom prompts
7. Test results storage

---

## ⏱️ Estimated Implementation Time

- **Phase 1**: Database setup (30 min)
- **Phase 2**: Services (1 hour)
- **Phase 3**: Migration (1 hour)
- **Phase 4**: New features (30 min)

**Total**: ~3 hours of development

---

## 🚀 Next Steps

1. Create database schema
2. Implement database manager
3. Create service layer
4. Update UI components
5. Test thoroughly

---

**Ready to implement? This will be a significant improvement to the system!**
