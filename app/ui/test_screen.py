"""Test Taking Screen"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QButtonGroup,
    QPushButton, QMessageBox, QProgressBar, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from services.question_service import QuestionService
from services.score_service import ScoreService
from ui.base_window import BaseWindow


class TestScreen(BaseWindow):
    """Test Taking Screen"""

    test_completed = pyqtSignal(dict)  # Result data
    back_signal = pyqtSignal()

    def __init__(self, username: str, grade: str, subject: str, topic: str, paper_num: int):
        super().__init__(f"Test - {grade}th Grade {subject}", 1100, 850)
        self.username = username
        self.grade = grade
        self.subject = subject
        self.topic = topic
        self.paper_num = paper_num
        
        self.question_service = QuestionService()
        self.score_service = ScoreService()
        
        self.current_question_index = 0
        self.user_answers = {}
        self.questions = []
        
        self.init_ui()
        self.load_questions()

    def init_ui(self):
        """Initialize UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel(f"📝 {self.grade}th Grade {self.subject} Test")
        title.setFont(self.get_title_font())
        title.setStyleSheet("color: #4472C4; font-weight: bold;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        back_btn = QPushButton("← Back")
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.setMaximumWidth(120)
        back_btn.setMinimumHeight(45)
        back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(back_btn)
        main_layout.addLayout(header_layout)

        # Progress bar with label
        progress_frame = QFrame()
        progress_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #E8EEF5;
                padding: 12px;
            }
        """)
        progress_layout = QVBoxLayout(progress_frame)
        progress_layout.setContentsMargins(10, 10, 10, 10)
        
        progress_label = QLabel("Progress:")
        progress_label.setFont(self.get_subheader_font())
        progress_label.setStyleSheet("color: #212F3D;")
        progress_layout.addWidget(progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(25)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                font-size: 12px;
                color: white;
                background-color: #F5F5F5;
            }
            QProgressBar::chunk {
                background-color: #4472C4;
                border-radius: 6px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)
        main_layout.addWidget(progress_frame)

        # Question area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #F5F5F5;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background-color: #4472C4;
                border-radius: 6px;
            }
        """)
        
        scroll_widget = QWidget()
        self.question_layout = QVBoxLayout(scroll_widget)
        self.question_layout.setSpacing(20)
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll, 1)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(15)
        
        self.prev_btn = QPushButton("← Previous")
        self.prev_btn.setStyleSheet(self.get_button_style())
        self.prev_btn.setMinimumHeight(45)
        self.prev_btn.setMinimumWidth(140)
        self.prev_btn.clicked.connect(self.previous_question)
        nav_layout.addWidget(self.prev_btn)
        
        self.question_label = QLabel("")
        self.question_label.setFont(self.get_subheader_font())
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setStyleSheet("color: #4472C4;")
        nav_layout.addWidget(self.question_label)
        
        self.next_btn = QPushButton("Next →")
        self.next_btn.setStyleSheet(self.get_button_style())
        self.next_btn.setMinimumHeight(45)
        self.next_btn.setMinimumWidth(140)
        self.next_btn.clicked.connect(self.next_question)
        nav_layout.addWidget(self.next_btn)
        
        nav_layout.addSpacing(30)
        
        self.submit_btn = QPushButton("✅ Submit Test")
        self.submit_btn.setStyleSheet(self.get_success_button_style())
        self.submit_btn.setMinimumHeight(45)
        self.submit_btn.setMinimumWidth(160)
        self.submit_btn.clicked.connect(self.submit_test)
        nav_layout.addWidget(self.submit_btn)
        
        main_layout.addLayout(nav_layout)

        central_widget.setLayout(main_layout)

    def load_questions(self):
        """Load questions from question service (user-specific unused questions)"""
        # Use new method that selects unused questions for this user
        result = self.question_service.get_test_questions_for_user(
            self.username, self.grade, self.subject, self.topic
        )
        
        if "error" in result:
            QMessageBox.critical(self, "Not Enough Questions", result["error"])
            self.go_back()
            return
            
        self.questions = result.get("questions", [])
        self.paper_num = result.get("paper_number", 1)
        
        if not self.questions:
            QMessageBox.critical(self, "Error", "Failed to load questions.")
            self.go_back()
            return
        
        self.update_question_display()

    def update_question_display(self):
        """Update the current question display"""
        # Clear previous layout
        while self.question_layout.count():
            child = self.question_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not self.questions:
            return
        
        q = self.questions[self.current_question_index]
        
        # Question number and text
        q_label = QLabel(f"Question {q['question_number']} of {len(self.questions)}")
        q_label.setFont(self.get_header_font())
        q_label.setStyleSheet("color: #4472C4; padding: 5px;")
        self.question_layout.addWidget(q_label)
        
        question_text = QLabel(q['question_text'])
        question_text.setFont(self.get_large_font())
        question_text.setWordWrap(True)
        question_text.setStyleSheet("""
            QLabel {
                padding: 15px;
                background-color: white;
                border: 2px solid #4472C4;
                border-radius: 8px;
                color: #212F3D;
            }
        """)
        question_text.setMinimumHeight(80)
        self.question_layout.addWidget(question_text)
        
        self.question_layout.addSpacing(10)
        
        # Options
        options_label = QLabel("Select your answer:")
        options_label.setFont(self.get_subheader_font())
        options_label.setStyleSheet("color: #333333; padding: 5px;")
        self.question_layout.addWidget(options_label)
        
        self.button_group = QButtonGroup()
        
        options = q.get('options', {})
        option_keys = ['A', 'B', 'C', 'D']
        
        for i, key in enumerate(option_keys):
            option_text = options.get(key, "")
            if option_text:
                radio_btn = QRadioButton(f"{key}) {option_text}")
                radio_btn.setFont(self.get_normal_font())
                radio_btn.setMinimumHeight(50)
                radio_btn.setStyleSheet("""
                    QRadioButton {
                        padding: 12px 15px;
                        background-color: white;
                        border: 2px solid #E8EEF5;
                        border-radius: 8px;
                        margin: 8px 0px;
                        color: #212F3D;
                    }
                    QRadioButton:hover {
                        background-color: #F0F8FF;
                        border: 2px solid #4472C4;
                    }
                    QRadioButton:checked {
                        background-color: #E8F4F8;
                        border: 2px solid #4472C4;
                        color: #4472C4;
                        font-weight: bold;
                    }
                    QRadioButton::indicator {
                        width: 20px;
                        height: 20px;
                    }
                """)
                
                self.button_group.addButton(radio_btn, i)
                self.question_layout.addWidget(radio_btn)
                
                # Check if we have a saved answer for this question
                if question['question_number'] in self.user_answers:
                    if self.user_answers[question['question_number']] == key:
                        radio_btn.setChecked(True)
        
        self.question_layout.addStretch()
        
        # Update progress bar
        progress = ((self.current_question_index + 1) / len(self.questions)) * 100
        self.progress_bar.setValue(int(progress))
        
        # Update button states
        self.prev_btn.setEnabled(self.current_question_index > 0)
        self.next_btn.setEnabled(self.current_question_index < len(self.questions) - 1)
        # Always show submit button
        self.submit_btn.setVisible(True)
        self.submit_btn.setEnabled(True)

    def save_current_answer(self):
        """Save the current selected answer"""
        if self.questions:
            q = self.questions[self.current_question_index]
            checked_btn = self.button_group.checkedButton()
            if checked_btn:
                # Get the option letter from button text
                btn_text = checked_btn.text()
                option = btn_text.split(")")[0].strip()
                self.user_answers[q['question_number']] = option

    def next_question(self):
        """Go to next question"""
        self.save_current_answer()
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.update_question_display()

    def previous_question(self):
        """Go to previous question"""
        self.save_current_answer()
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.update_question_display()

    def submit_test(self):
        """Submit the test"""
        self.save_current_answer()
        
        # Check if all questions are answered
        if len(self.user_answers) < len(self.questions):
            reply = QMessageBox.question(
                self,
                "Incomplete Test",
                f"You have only answered {len(self.user_answers)} out of {len(self.questions)} questions.\n"
                f"Do you want to submit anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        # Process and save test
        # Pass self.questions instead of paper_num
        result = self.score_service.process_and_save_test(
            self.username,
            self.grade,
            self.subject,
            self.topic,
            self.questions,
            self.user_answers
        )
        
        if result["success"]:
            # Mark these questions as answered by this user
            # We need question IDs now
            question_ids = [q.get('id') for q in self.questions if q.get('id')]
            if question_ids:
                self.question_service.mark_questions_answered(
                    self.username, self.grade, self.subject, self.topic, question_ids
                )
            
            # Show detailed results screen instead of just a message
            self.show_detailed_results(result)
        else:
            QMessageBox.warning(self, "Error", result["message"])

    def show_detailed_results(self, result: dict):
        """Show detailed test results"""
        # Create a new window for detailed results
        from ui.results_screen import ResultsScreen
        
        self.results_screen = ResultsScreen(
            self.username,
            self.grade,
            self.subject,
            self.topic,
            self.questions,
            self.user_answers,
            result
        )
        self.results_screen.back_signal.connect(self.on_results_back)
        self.results_screen.show()
        self.hide()

    def on_results_back(self):
        """Handle back from results"""
        self.test_completed.emit({})

    def go_back(self):
        """Go back to dashboard"""
        reply = QMessageBox.question(
            self,
            "Exit Test",
            "Are you sure you want to exit the test? Your progress will not be saved.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.back_signal.emit()
