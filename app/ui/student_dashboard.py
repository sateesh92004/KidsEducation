"""Student Dashboard Screen - Modern Design"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QMessageBox, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from services.question_service import QuestionService
from utils.constants import GRADES, SUBJECTS
from ui.base_window import BaseWindow
from ui.test_screen import TestScreen


class StudentDashboard(BaseWindow):
    """Student Dashboard Screen - Modern Design"""

    logout_signal = pyqtSignal()

    def __init__(self, username: str):
        super().__init__("Kids Education - Student Dashboard", 1300, 1000)
        self.username = username
        self.question_service = QuestionService()
        self.test_screen = None
        self.init_ui()
        self.load_statistics()

    def init_ui(self):
        """Initialize UI components"""
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #F5F7FA;")
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(20)

        # Header with welcome and logout
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: linear-gradient(135deg, #4472C4 0%, #5B8FD4 100%);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        header_frame.setMaximumHeight(100)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(25, 15, 25, 15)
        
        title = QLabel(f"🎆 Welcome, {self.username}!")
        title_font = QFont()
        title_font.setFamily('Segoe UI')
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet(self.get_button_style())
        logout_btn.setMaximumWidth(120)
        logout_btn.setMinimumHeight(45)
        logout_btn.clicked.connect(self.logout)
        header_layout.addWidget(logout_btn)
        main_layout.addWidget(header_frame)

        # Test Selection Section
        selection_frame = QFrame()
        selection_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
                padding: 20px;
            }
        """)
        selection_layout = QVBoxLayout(selection_frame)
        selection_layout.setSpacing(15)
        selection_layout.setContentsMargins(25, 20, 25, 20)

        # Selection label
        selections_label = QLabel("📚 Select Your Test")
        selections_font = QFont()
        selections_font.setFamily('Segoe UI')
        selections_font.setPointSize(16)
        selections_font.setBold(True)
        selections_label.setFont(selections_font)
        selections_label.setStyleSheet("color: #212F3D;")
        selection_layout.addWidget(selections_label)

        # Dropdowns in ONE row
        dropdowns_layout = QHBoxLayout()
        dropdowns_layout.setSpacing(20)
        dropdowns_layout.setContentsMargins(0, 15, 0, 15)

        # Grade
        grade_label = QLabel("📚 Grade:")
        grade_label.setFont(self.get_normal_font())
        grade_label.setStyleSheet("color: #4472C4; font-weight: bold; min-width: 70px;")
        dropdowns_layout.addWidget(grade_label)
        
        self.grade_combo = QComboBox()
        self.grade_combo.addItems(GRADES)
        self.grade_combo.setStyleSheet(self.get_dropdown_style())
        self.grade_combo.setMinimumHeight(40)
        self.grade_combo.setMinimumWidth(130)
        self.grade_combo.setMaximumWidth(180)
        self.grade_combo.setFont(self.get_normal_font())
        dropdowns_layout.addWidget(self.grade_combo)

        # Subject
        subject_label = QLabel("🔬 Subject:")
        subject_label.setFont(self.get_normal_font())
        subject_label.setStyleSheet("color: #4472C4; font-weight: bold; min-width: 70px;")
        dropdowns_layout.addWidget(subject_label)
        
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(SUBJECTS)
        self.subject_combo.setStyleSheet(self.get_dropdown_style())
        self.subject_combo.setMinimumHeight(40)
        self.subject_combo.setMinimumWidth(130)
        self.subject_combo.setMaximumWidth(180)
        self.subject_combo.setFont(self.get_normal_font())
        dropdowns_layout.addWidget(self.subject_combo)

        # Topic
        topic_label = QLabel("🎯 Topic:")
        topic_label.setFont(self.get_normal_font())
        topic_label.setStyleSheet("color: #4472C4; font-weight: bold; min-width: 70px;")
        dropdowns_layout.addWidget(topic_label)
        
        self.topic_combo = QComboBox()
        self.topic_combo.setStyleSheet(self.get_dropdown_style())
        self.topic_combo.setMinimumHeight(40)
        self.topic_combo.setMinimumWidth(150)
        self.topic_combo.setMaximumWidth(220)
        self.topic_combo.setFont(self.get_normal_font())
        self.populate_topics()
        self.grade_combo.currentTextChanged.connect(self.populate_topics)
        self.subject_combo.currentTextChanged.connect(self.populate_topics)
        dropdowns_layout.addWidget(self.topic_combo)

        dropdowns_layout.addStretch()
        
        start_btn = QPushButton("🚀 Start Test")
        start_btn.setFont(self.get_subheader_font())
        start_btn.setStyleSheet(self.get_button_style())
        start_btn.setMinimumHeight(40)
        start_btn.setMinimumWidth(140)
        start_btn.clicked.connect(self.start_test)
        dropdowns_layout.addWidget(start_btn)
        
        selection_layout.addLayout(dropdowns_layout)
        main_layout.addWidget(selection_frame)

        # Statistics Section Title
        stats_title = QLabel("📊 Your Test Statistics")
        stats_title_font = QFont()
        stats_title_font.setFamily('Segoe UI')
        stats_title_font.setPointSize(16)
        stats_title_font.setBold(True)
        stats_title.setFont(stats_title_font)
        stats_title.setStyleSheet("color: #212F3D; margin-top: 10px;")
        main_layout.addWidget(stats_title)

        # Statistics scroll area
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
        scroll_widget.setStyleSheet("background-color: transparent;")
        self.stats_layout = QVBoxLayout(scroll_widget)
        self.stats_layout.setSpacing(15)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll, 1)

        central_widget.setLayout(main_layout)

    def get_dropdown_style(self) -> str:
        """Get dropdown styling with highlighting"""
        return """
            QComboBox {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                color: #212F3D;
            }
            QComboBox:hover {
                border: 2px solid #4472C4;
                background-color: #F8FAFC;
            }
            QComboBox:focus {
                border: 2px solid #4472C4;
                background-color: #E8F4F8;
            }
            QComboBox:on {
                border: 2px solid #4472C4;
                background-color: #E8F4F8;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #4472C4;
                background-color: white;
                selection-background-color: #4472C4;
                selection-color: white;
                padding: 5px;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                border-radius: 4px;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #4472C4;
                color: white;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #E8F4F8;
                color: #4472C4;
            }
        """

    def load_statistics(self):
        """Load and display student statistics"""
        try:
            from utils.excel_handler import ExcelHandler
            
            results = ExcelHandler.get_student_results(self.username)
            
            # Clear previous layout
            while self.stats_layout.count():
                child = self.stats_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            if not results:
                no_tests_label = QLabel("📌 No tests taken yet. Start a test to see your statistics!")
                no_tests_label.setFont(self.get_normal_font())
                no_tests_label.setStyleSheet("color: #999999; font-style: italic; padding: 30px;")
                self.stats_layout.addWidget(no_tests_label)
                self.stats_layout.addStretch()
                return
            
            # Create statistics by grade+subject+topic
            stats_dict = {}
            for result in results:
                key = f"{result[1]}-{result[2]}-{result[3]}"  # grade-subject-topic
                if key not in stats_dict:
                    stats_dict[key] = {'tests': 0, 'total_score': 0, 'scores': []}
                
                stats_dict[key]['tests'] += 1
                score = float(result[8].replace('%', ''))
                stats_dict[key]['total_score'] += score
                stats_dict[key]['scores'].append(score)
            
            # Display statistics
            for key, stats in sorted(stats_dict.items()):
                grade, subject, topic = key.split('-')
                avg_score = stats['total_score'] / stats['tests']
                max_score = max(stats['scores'])
                min_score = min(stats['scores'])
                
                # Create card for each topic
                card = QFrame()
                
                # Color based on average score
                if avg_score >= 80:
                    border_color = "#70AD47"  # Green
                    bg_color = "#F1F8F0"
                elif avg_score >= 60:
                    border_color = "#FFA500"  # Orange
                    bg_color = "#FFF8F0"
                else:
                    border_color = "#E53935"  # Red
                    bg_color = "#FFF1F0"
                
                card.setStyleSheet(f"""
                    QFrame {{
                        background-color: {bg_color};
                        border-radius: 12px;
                        border-left: 5px solid {border_color};
                        padding: 0px;
                    }}
                """)
                card_layout = QVBoxLayout(card)
                card_layout.setSpacing(10)
                card_layout.setContentsMargins(20, 15, 20, 15)
                
                # Topic title
                topic_title = QLabel(f"📖 {grade}th Grade - {subject} - {topic}")
                topic_title_font = QFont()
                topic_title_font.setFamily('Segoe UI')
                topic_title_font.setPointSize(13)
                topic_title_font.setBold(True)
                topic_title.setFont(topic_title_font)
                topic_title.setStyleSheet(f"color: {border_color}; font-weight: bold;")
                card_layout.addWidget(topic_title)
                
                # Statistics row 1: Tests and scores
                stats_row1 = QHBoxLayout()
                
                tests_label = QLabel(f"📋 Tests: {stats['tests']}")
                tests_label.setFont(self.get_normal_font())
                tests_label.setStyleSheet("color: #333333; font-weight: bold;")
                stats_row1.addWidget(tests_label)
                
                stats_row1.addSpacing(30)
                
                avg_label = QLabel(f"📈 Avg: {avg_score:.1f}%")
                avg_label.setFont(self.get_normal_font())
                avg_label.setStyleSheet("color: #333333; font-weight: bold;")
                stats_row1.addWidget(avg_label)
                
                stats_row1.addSpacing(30)
                
                best_label = QLabel(f"🌟 Best: {max_score:.1f}%")
                best_label.setFont(self.get_normal_font())
                best_label.setStyleSheet("color: #333333; font-weight: bold;")
                stats_row1.addWidget(best_label)
                
                stats_row1.addStretch()
                card_layout.addLayout(stats_row1)
                
                # Progress bar representation
                progress_label = QLabel()
                progress_bar = self.create_progress_bar(avg_score)
                progress_label.setText(progress_bar)
                progress_font = QFont()
                progress_font.setFamily('Courier New')
                progress_font.setPointSize(11)
                progress_label.setFont(progress_font)
                progress_label.setStyleSheet(f"color: {border_color}; font-weight: bold;")
                card_layout.addWidget(progress_label)
                
                self.stats_layout.addWidget(card)
            
            self.stats_layout.addStretch()
            
        except Exception as e:
            error_label = QLabel(f"⚠ Could not load statistics: {str(e)[:50]}")
            error_label.setFont(self.get_normal_font())
            error_label.setStyleSheet("color: #E53935;")
            self.stats_layout.addWidget(error_label)
            self.stats_layout.addStretch()

    def create_progress_bar(self, percentage: float) -> str:
        """Create text-based progress bar"""
        filled = int(percentage / 5)
        empty = 20 - filled
        bar = "█" * filled + "░" * empty
        return f"Progress: [{bar}] {percentage:.1f}%"

    def populate_topics(self):
        """Populate available topics for selected grade and subject"""
        self.topic_combo.clear()
        
        grade = self.grade_combo.currentText()
        subject = self.subject_combo.currentText()
        
        if not grade or not subject:
            return
        
        # Get available topics from saved papers
        available_topics = self.question_service.get_available_topics(grade, subject)
        
        if available_topics:
            self.topic_combo.addItems(available_topics)
        else:
            self.topic_combo.addItem("No topics available")

    def start_test(self):
        """Start a test"""
        grade = self.grade_combo.currentText()
        subject = self.subject_combo.currentText()
        topic = self.topic_combo.currentText()

        if not grade or not subject or not topic or topic == "No topics available":
            QMessageBox.warning(self, "Selection Error", "Please select all options.")
            return

        # Check if papers are available
        available_papers = self.question_service.get_available_papers(grade, subject, topic)
        
        if not available_papers:
            QMessageBox.warning(
                self,
                "No Papers Available",
                f"No test papers available for {grade} grade, {subject}, {topic}.\n\n"
                f"Please contact your administrator to generate question papers."
            )
            return

        # Open test screen
        self.test_screen = TestScreen(
            self.username, grade, subject, topic, available_papers[0]
        )
        self.test_screen.test_completed.connect(self.on_test_completed)
        self.test_screen.back_signal.connect(self.on_test_back)
        self.test_screen.show()
        self.hide()

    def on_test_completed(self, result: dict):
        """Handle test completion"""
        self.show()
        if self.test_screen:
            self.test_screen.close()
        # Reload statistics
        self.load_statistics()

    def on_test_back(self):
        """Handle back from test"""
        self.show()
        if self.test_screen:
            self.test_screen.close()
        # Reload statistics
        self.load_statistics()

    def logout(self):
        """Logout from student dashboard"""
        reply = QMessageBox.question(
            self, "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_signal.emit()
            self.close()
