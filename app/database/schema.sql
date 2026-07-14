-- Kids Education App Database Schema
-- SQLite Database for managing users, questions, tests, and results

-- ============================================================
-- USERS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student', 'admin')),
    full_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- ============================================================
-- QUESTIONS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade TEXT NOT NULL,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    question_text TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_answer TEXT NOT NULL CHECK(correct_answer IN ('A', 'B', 'C', 'D')),
    explanation TEXT,
    difficulty TEXT CHECK(difficulty IN ('Easy', 'Medium', 'Hard')),
    question_type TEXT CHECK(question_type IN ('word_problem', 'complex', 'conceptual', 'application')),
    generated_by TEXT,
    custom_prompt_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (custom_prompt_id) REFERENCES custom_prompts(id)
);

-- Indexes for fast question retrieval
CREATE INDEX IF NOT EXISTS idx_questions_grade_subject_topic ON questions(grade, subject, topic);
CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions(difficulty);
CREATE INDEX IF NOT EXISTS idx_questions_type ON questions(question_type);
CREATE INDEX IF NOT EXISTS idx_questions_created ON questions(created_at);

-- ============================================================
-- USER ANSWERED QUESTIONS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS user_answered_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    UNIQUE(user_id, question_id)
);

CREATE INDEX IF NOT EXISTS idx_user_answered_user ON user_answered_questions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_answered_question ON user_answered_questions(question_id);

-- ============================================================
-- TEST RESULTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS test_results (
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
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_test_results_user ON test_results(user_id);
CREATE INDEX IF NOT EXISTS idx_test_results_date ON test_results(test_date);
CREATE INDEX IF NOT EXISTS idx_test_results_topic ON test_results(grade, subject, topic);

-- ============================================================
-- TEST ANSWERS TABLE (Detailed answers for each test)
-- ============================================================
CREATE TABLE IF NOT EXISTS test_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_result_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    user_answer TEXT NOT NULL CHECK(user_answer IN ('A', 'B', 'C', 'D')),
    is_correct BOOLEAN NOT NULL,
    FOREIGN KEY (test_result_id) REFERENCES test_results(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_test_answers_result ON test_answers(test_result_id);
CREATE INDEX IF NOT EXISTS idx_test_answers_question ON test_answers(question_id);

-- ============================================================
-- CUSTOM PROMPTS TABLE (Admin feature)
-- ============================================================
CREATE TABLE IF NOT EXISTS custom_prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER NOT NULL,
    grade TEXT NOT NULL,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    prompt_name TEXT NOT NULL,
    custom_prompt TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_custom_prompts_admin ON custom_prompts(admin_id);
CREATE INDEX IF NOT EXISTS idx_custom_prompts_topic ON custom_prompts(grade, subject, topic);
CREATE INDEX IF NOT EXISTS idx_custom_prompts_active ON custom_prompts(is_active);

-- ============================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================

-- View: User Statistics
CREATE VIEW IF NOT EXISTS user_statistics AS
SELECT 
    u.id,
    u.username,
    u.role,
    COUNT(DISTINCT uaq.question_id) as questions_answered,
    COUNT(DISTINCT tr.id) as tests_taken,
    AVG(tr.score_percentage) as average_score
FROM users u
LEFT JOIN user_answered_questions uaq ON u.id = uaq.user_id
LEFT JOIN test_results tr ON u.id = tr.user_id
GROUP BY u.id, u.username, u.role;

-- View: Question Statistics
CREATE VIEW IF NOT EXISTS question_statistics AS
SELECT 
    q.id,
    q.grade,
    q.subject,
    q.topic,
    q.difficulty,
    q.question_type,
    COUNT(DISTINCT uaq.user_id) as times_answered,
    COUNT(DISTINCT ta.id) as times_used_in_tests
FROM questions q
LEFT JOIN user_answered_questions uaq ON q.id = uaq.question_id
LEFT JOIN test_answers ta ON q.id = ta.question_id
GROUP BY q.id;

-- ============================================================
-- INITIAL DATA
-- ============================================================

-- Create default admin user (password: admin123 - should be changed!)
-- Password hash for 'admin123' using simple hash (will be replaced with proper hashing)
INSERT OR IGNORE INTO users (username, password_hash, role, full_name)
VALUES ('admin', 'admin123', 'admin', 'System Administrator');
