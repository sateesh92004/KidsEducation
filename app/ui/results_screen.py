"""Detailed Test Results Screen - Modern Design"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from ui.base_window import BaseWindow


class ResultsScreen(BaseWindow):
    """Detailed Test Results Screen"""

    back_signal = pyqtSignal()

    def __init__(self, username: str, grade: str, subject: str, topic: str,
                 questions: list, user_answers: dict, result: dict):
        super().__init__(f"Test Results - {grade}th Grade {subject}", 1200, 1000)
        self.username = username
        self.grade = grade
        self.subject = subject
        self.topic = topic
        self.questions = questions
        self.user_answers = user_answers
        self.result = result
        
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #F5F7FA;")
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Top bar with back button and title
        top_layout = QHBoxLayout()
        title = QLabel(f"📋 Test Results")
        title.setFont(self.get_title_font())
        title.setStyleSheet("color: #212F3D;")
        top_layout.addWidget(title)
        top_layout.addStretch()
        
        back_btn = QPushButton("← Back")
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.setMaximumWidth(120)
        back_btn.setMinimumHeight(40)
        back_btn.clicked.connect(self.go_back)
        top_layout.addWidget(back_btn)
        main_layout.addLayout(top_layout)

        # Score card (compact, not huge)
        score_frame = QFrame()
        score_frame.setStyleSheet("""
            QFrame {
                background: linear-gradient(135deg, #4472C4 0%, #5B8FD4 100%);
                border-radius: 12px;
                padding: 20px;
                border: none;
            }
        """)
        score_frame.setMaximumHeight(180)  # Reasonable height, not half screen!
        score_layout = QHBoxLayout(score_frame)
        score_layout.setContentsMargins(30, 20, 30, 20)
        score_layout.setSpacing(40)

        # Left side: Score circle
        score_circle_layout = QVBoxLayout()
        score_circle_layout.setSpacing(10)
        score_circle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Score percentage (large but reasonable)
        score_text = QLabel(f"{self.result['score_percentage']:.1f}%")
        score_font = QFont()
        score_font.setFamily('Segoe UI')
        score_font.setPointSize(48)  # Reduced from 72pt to 48pt
        score_font.setBold(True)
        score_text.setFont(score_font)
        score_text.setStyleSheet("color: #FFD700; margin: 0px;")
        score_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_circle_layout.addWidget(score_text)
        
        score_label = QLabel("Your Score")
        score_label_font = QFont()
        score_label_font.setFamily('Segoe UI')
        score_label_font.setPointSize(14)
        score_label.setFont(score_label_font)
        score_label.setStyleSheet("color: #FFFFFF;")
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_circle_layout.addWidget(score_label)
        
        score_layout.addLayout(score_circle_layout)
        
        # Right side: Details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(15)
        details_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        # Correct answers
        correct_label = QLabel(f"Correct Answers")
        correct_label_font = QFont()
        correct_label_font.setFamily('Segoe UI')
        correct_label_font.setPointSize(12)
        correct_label.setFont(correct_label_font)
        correct_label.setStyleSheet("color: #E8F4F8;")
        details_layout.addWidget(correct_label)
        
        correct_value = QLabel(f"{self.result['correct_answers']}/{self.result['total_questions']}")
        correct_font = QFont()
        correct_font.setFamily('Segoe UI')
        correct_font.setPointSize(32)
        correct_font.setBold(True)
        correct_value.setFont(correct_font)
        correct_value.setStyleSheet("color: #FFFFFF;")
        details_layout.addWidget(correct_value)
        
        # Additional stats
        stats_text = QLabel(
            f"Grade: {self.grade} | Subject: {self.subject}\nTopic: {self.topic}"
        )
        stats_font = QFont()
        stats_font.setFamily('Segoe UI')
        stats_font.setPointSize(11)
        stats_text.setFont(stats_font)
        stats_text.setStyleSheet("color: #FFFFFF;")
        details_layout.addWidget(stats_text)
        
        details_layout.addStretch()
        score_layout.addLayout(details_layout)
        score_layout.addStretch()
        
        main_layout.addWidget(score_frame)

        # Answer Review Section
        review_label = QLabel("📝 Answer Review")
        review_label.setFont(self.get_subheader_font())
        review_label.setStyleSheet("color: #212F3D; margin-top: 10px;")
        main_layout.addWidget(review_label)

        # Scroll area for question reviews
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #E8EEF5;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4472C4;
                border-radius: 6px;
            }
        """)
        
        scroll_widget = QWidget()
        self.results_layout = QVBoxLayout(scroll_widget)
        self.results_layout.setSpacing(12)
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add each question review
        self.display_question_reviews()
        
        self.results_layout.addStretch()
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll, 1)

        central_widget.setLayout(main_layout)

    def display_question_reviews(self):
        """Display detailed review for each question"""
        for detail in self.result.get('details', []):
            q_num = detail.get('question_number')
            user_ans = detail.get('user_answer')
            correct_ans = detail.get('correct_answer')
            is_correct = detail.get('is_correct')
            explanation = detail.get('explanation', '')
            
            # Find the question to get its text
            question = None
            for q in self.questions:
                if q.get('question_number') == q_num:
                    question = q
                    break
            
            if not question:
                continue
            
            # Create question card frame
            card_frame = QFrame()
            
            # Set background color based on correctness
            if is_correct:
                card_style = """
                    QFrame {
                        background-color: #E8F5E9;
                        border: 2px solid #70AD47;
                        border-radius: 10px;
                        padding: 15px;
                    }
                """
            else:
                card_style = """
                    QFrame {
                        background-color: #FFEBEE;
                        border: 2px solid #E53935;
                        border-radius: 10px;
                        padding: 15px;
                    }
                """
            
            card_frame.setStyleSheet(card_style)
            card_layout = QVBoxLayout(card_frame)
            card_layout.setSpacing(10)
            card_layout.setContentsMargins(15, 12, 15, 12)

            # Question number and status
            header_layout = QHBoxLayout()
            
            q_header = QLabel(f"Question {q_num}")
            q_header.setFont(self.get_subheader_font())
            q_header.setStyleSheet("color: #333333;")
            header_layout.addWidget(q_header)
            
            header_layout.addStretch()
            
            if is_correct:
                status = QLabel("✅ Correct")
                status.setStyleSheet("color: #70AD47; font-weight: bold; font-size: 13px;")
            else:
                status = QLabel("❌ Incorrect")
                status.setStyleSheet("color: #E53935; font-weight: bold; font-size: 13px;")
            
            header_layout.addWidget(status)
            card_layout.addLayout(header_layout)

            # Question text
            q_text = QLabel(question.get('question_text', ''))
            q_text.setFont(self.get_normal_font())
            q_text.setWordWrap(True)
            q_text.setStyleSheet("font-weight: bold; color: #212F3D; margin: 5px 0px;")
            card_layout.addWidget(q_text)

            # Separator
            sep = QLabel()
            sep.setStyleSheet("border-bottom: 1px solid #CCCCCC; margin: 5px 0px;")
            sep.setMinimumHeight(1)
            card_layout.addWidget(sep)

            # User's answer
            user_ans_label = QLabel("Your Answer:")
            user_ans_label.setFont(self.get_normal_font())
            user_ans_label.setStyleSheet("color: #333333; font-weight: bold;")
            card_layout.addWidget(user_ans_label)
            
            if user_ans:
                options = question.get('options', {})
                user_ans_text = options.get(user_ans, "Not answered")
                user_ans_display = QLabel(f"{user_ans}) {user_ans_text}")
                user_ans_display.setFont(self.get_normal_font())
                user_ans_display.setWordWrap(True)
                if is_correct:
                    user_ans_display.setStyleSheet("color: #70AD47; font-weight: bold; padding: 8px; background-color: white; border-radius: 5px; margin-left: 10px;")
                else:
                    user_ans_display.setStyleSheet("color: #E53935; font-weight: bold; padding: 8px; background-color: white; border-radius: 5px; margin-left: 10px;")
                card_layout.addWidget(user_ans_display)
            else:
                not_answered = QLabel("Not answered")
                not_answered.setFont(self.get_normal_font())
                not_answered.setStyleSheet("color: #999999; font-style: italic; padding: 8px; margin-left: 10px;")
                card_layout.addWidget(not_answered)

            # Correct answer (if user got it wrong)
            if not is_correct:
                correct_label = QLabel("Correct Answer:")
                correct_label.setFont(self.get_normal_font())
                correct_label.setStyleSheet("color: #70AD47; font-weight: bold; margin-top: 10px;")
                card_layout.addWidget(correct_label)
                
                options = question.get('options', {})
                correct_ans_text = options.get(correct_ans, "Unknown")
                correct_ans_display = QLabel(f"{correct_ans}) {correct_ans_text}")
                correct_ans_display.setFont(self.get_normal_font())
                correct_ans_display.setWordWrap(True)
                correct_ans_display.setStyleSheet("color: #70AD47; font-weight: bold; padding: 8px; background-color: white; border-radius: 5px; margin-left: 10px;")
                card_layout.addWidget(correct_ans_display)

            # Explanation
            if explanation:
                exp_label = QLabel("Explanation:")
                exp_label.setFont(self.get_normal_font())
                exp_label.setStyleSheet("color: #333333; font-weight: bold; margin-top: 10px;")
                card_layout.addWidget(exp_label)
                
                exp_text = QLabel(explanation)
                exp_text.setFont(self.get_normal_font())
                exp_text.setWordWrap(True)
                exp_text.setStyleSheet("color: #555555; padding: 8px; background-color: white; border-radius: 5px; margin-left: 10px;")
                card_layout.addWidget(exp_text)

            self.results_layout.addWidget(card_frame)

    def go_back(self):
        """Go back to dashboard"""
        self.back_signal.emit()
        self.close()
