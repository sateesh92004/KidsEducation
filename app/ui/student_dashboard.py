"""Student Dashboard Screen - Modern Design"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QMessageBox, QFrame, QScrollArea, QGridLayout, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QIcon, QCursor
from services.question_service import QuestionService
from utils.constants import GRADES, SUBJECTS
from ui.base_window import BaseWindow
from ui.test_screen import TestScreen
from ui.styles import ModernStyles
from ui.learning_screen import LearningScreen
import random

class ClickableCard(QFrame):
    """A clickable card widget for subjects/topics"""
    clicked = pyqtSignal(str)

    def __init__(self, title, color, icon_text="📚"):
        super().__init__()
        self.title = title
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 15px;
                border: 2px solid {color};
            }}
            QFrame:hover {{
                background-color: {color}10; /* 10% opacity */
                border: 3px solid {color};
                margin-top: -5px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icon/Emoji
        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet("font-size: 40px; border: none; background: transparent;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {ModernStyles.TEXT_DARK}; border: none; background: transparent;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)

    def mousePressEvent(self, event):
        self.clicked.emit(self.title)


class StudentDashboard(BaseWindow):
    """Student Dashboard Screen - Modern Design"""

    logout_signal = pyqtSignal()

    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.question_service = QuestionService()
        self.test_screen = None
        
        # State
        self.selected_grade = "5" # Default
        self.selected_subject = None
        
        self.setWindowTitle("Kids Education - Student Dashboard")
        self.resize(1200, 900)
        self.init_ui()
        self.load_statistics()

    def init_ui(self):
        """Initialize UI components"""
        self.setStyleSheet(ModernStyles.get_main_window_style())
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # --- Header Section ---
        header = QHBoxLayout()
        
        # Welcome Text
        welcome_layout = QVBoxLayout()
        welcome_title = QLabel(f"👋 Hi, {self.username}!")
        welcome_title.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {ModernStyles.TEXT_DARK};")
        welcome_subtitle = QLabel("Ready to learn something new today?")
        welcome_subtitle.setStyleSheet("font-size: 16px; color: #757575;")
        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_subtitle)
        header.addLayout(welcome_layout)
        
        header.addStretch()
        
        # Grade Selector (Top Right)
        grade_layout = QHBoxLayout()
        grade_label = QLabel("I am in Grade:")
        grade_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.grade_combo = QComboBox()
        self.grade_combo.addItems(GRADES)
        self.grade_combo.setCurrentText(self.selected_grade)
        self.grade_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 8px 15px;
                border-radius: 20px;
                border: 2px solid {ModernStyles.ACCENT_BLUE};
                min-width: 80px;
                font-weight: bold;
            }}
        """)
        self.grade_combo.currentTextChanged.connect(self.on_grade_changed)
        grade_layout.addWidget(grade_label)
        grade_layout.addWidget(self.grade_combo)
        header.addLayout(grade_layout)
        
        header.addSpacing(20)
        
        # Logout Button
        logout_btn = QPushButton("Logout")
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFEBEE;
                color: #D32F2F;
                border: none;
                border-radius: 15px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFCDD2;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        header.addWidget(logout_btn)
        
        main_layout.addLayout(header)

        # --- Content Area (Stacked) ---
        # We use a QStackedLayout logic manually by clearing/rebuilding the content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 20, 0, 0)
        main_layout.addWidget(self.content_area, stretch=2)
        
        # Initial View: Subject Selection
        self.show_subject_selection()

        # --- Statistics Section (Bottom) ---
        stats_title = QLabel("🏆 My Achievements")
        stats_title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {ModernStyles.TEXT_DARK}; margin-top: 20px;")
        main_layout.addWidget(stats_title)

        # Scroll Area for Stats
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll.setFixedHeight(250) # Fixed height for stats area
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background: transparent;")
        self.stats_layout = QHBoxLayout(scroll_widget) # Horizontal scrolling for stats cards
        self.stats_layout.setSpacing(15)
        self.stats_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

    def on_grade_changed(self, grade):
        self.selected_grade = grade
        # Reset to subject selection when grade changes
        self.show_subject_selection()

    def show_subject_selection(self):
        """Show the grid of subjects"""
        self.clear_content_area()
        self.selected_subject = None
        
        # Title
        title = QLabel("Choose a Subject")
        title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {ModernStyles.ACCENT_BLUE};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(title)
        
        # Grid
        grid = QGridLayout()
        grid.setSpacing(20)
        
        subjects_data = [
            ("Mathematics", ModernStyles.ACCENT_BLUE, "📐"),
            ("Science", ModernStyles.SECONDARY_GREEN, "🔬"),
            ("English", ModernStyles.PRIMARY_ORANGE, "📖"),
            ("History", "#795548", "🏛️"),
            ("Geography", "#009688", "🌍"),
            ("Computer Science", "#673AB7", "💻")
        ]
        
        row, col = 0, 0
        for name, color, icon in subjects_data:
            if name in SUBJECTS: # Only show supported subjects
                card = ClickableCard(name, color, icon)
                card.clicked.connect(self.on_subject_clicked)
                card.setFixedSize(200, 150)
                grid.addWidget(card, row, col)
                
                col += 1
                if col > 2: # 3 columns
                    col = 0
                    row += 1
        
        grid_widget = QWidget()
        grid_widget.setLayout(grid)
        self.content_layout.addWidget(grid_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addStretch()

    def on_subject_clicked(self, subject):
        """Handle subject selection"""
        self.selected_subject = subject
        self.show_mode_selection()

    def show_mode_selection(self):
        """Show Learning vs Test mode selection"""
        self.clear_content_area()
        self.selected_mode = None
        
        # Header with Back Button
        header = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet(f"color: {ModernStyles.ACCENT_BLUE}; border: none; font-weight: bold; font-size: 16px;")
        back_btn.clicked.connect(self.show_subject_selection)
        header.addWidget(back_btn)
        
        title = QLabel(f"{self.selected_subject}")
        title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {ModernStyles.TEXT_DARK};")
        header.addWidget(title)
        header.addStretch()
        
        self.content_layout.addLayout(header)
        
        # Title
        mode_title = QLabel("What would you like to do?")
        mode_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mode_title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {ModernStyles.TEXT_DARK}; margin-top: 20px;")
        self.content_layout.addWidget(mode_title)
        
        # Modes Layout
        modes_layout = QHBoxLayout()
        modes_layout.setSpacing(40)
        modes_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Learning Mode Card
        learn_card = ClickableCard("Start Learning", ModernStyles.ACCENT_BLUE, "📖")
        learn_card.setFixedSize(250, 200)
        learn_card.clicked.connect(lambda: self.on_mode_clicked("learning"))
        modes_layout.addWidget(learn_card)
        
        # Test Mode Card
        test_card = ClickableCard("Take Test", ModernStyles.SECONDARY_GREEN, "📝")
        test_card.setFixedSize(250, 200)
        test_card.clicked.connect(lambda: self.on_mode_clicked("test"))
        modes_layout.addWidget(test_card)
        
        self.content_layout.addLayout(modes_layout)
        self.content_layout.addStretch()

    def on_mode_clicked(self, mode):
        """Handle mode selection"""
        self.selected_mode = mode
        
        if mode == "learning":
            # For Learning Mode, we don't need to block if there are no DB topics.
            # We just fetch them for suggestions, but allow the user to type anything.
            all_topics = self.question_service.get_available_topics(self.selected_grade, self.selected_subject)
            
            # Open Learning Screen directly
            self.learning_screen = LearningScreen(
                self.username, self.selected_grade, self.selected_subject, all_topics
            )
            self.learning_screen.back_signal.connect(self.on_learning_back)
            self.learning_screen.show()
            self.hide()
        else:
            # For Test Mode, we need existing topics
            self.show_topic_selection()

    def show_topic_selection(self):
        """Show topics for the selected subject"""
        self.clear_content_area()
        
        # Header with Back Button
        header = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet(f"color: {ModernStyles.ACCENT_BLUE}; border: none; font-weight: bold; font-size: 16px;")
        back_btn.clicked.connect(self.show_mode_selection)
        header.addWidget(back_btn)
        
        mode_text = "Learning" if self.selected_mode == "learning" else "Test"
        title = QLabel(f"{self.selected_subject} - {mode_text} Topics")
        title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {ModernStyles.TEXT_DARK};")
        header.addWidget(title)
        header.addStretch()
        
        self.content_layout.addLayout(header)
        
        # Get Topics from database
        topics = self.question_service.get_available_topics(self.selected_grade, self.selected_subject)
        
        if not topics:
            no_topics = QLabel(
                f"😕 No topics available for Grade {self.selected_grade} {self.selected_subject}.\n\n"
                f"Topics will appear here once questions are generated.\n"
                f"Ask your teacher (admin) to generate questions for this subject!"
            )
            no_topics.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_topics.setStyleSheet("font-size: 16px; color: #757575; margin-top: 50px; padding: 20px;")
            self.content_layout.addWidget(no_topics)
            self.content_layout.addStretch()
            return

        # Show count of available topics
        count_label = QLabel(f"📚 {len(topics)} topic(s) available")
        count_label.setStyleSheet(f"font-size: 14px; color: {ModernStyles.TEXT_DARK}; margin-bottom: 10px;")
        self.content_layout.addWidget(count_label)

        # Topics Grid
        grid = QGridLayout()
        grid.setSpacing(15)
        
        row, col = 0, 0
        for topic in topics:
            # Get question count for this topic
            stats = self.question_service.db_service.get_topic_stats(
                self.selected_grade, self.selected_subject, topic
            )
            question_count = stats.get('total_questions', 0)
            
            # Random color for variety
            color = random.choice([ModernStyles.ACCENT_BLUE, ModernStyles.SECONDARY_GREEN, ModernStyles.PRIMARY_ORANGE, ModernStyles.ACCENT_PURPLE])
            
            # Create enhanced card with question count
            card = self.create_topic_card(topic, color, question_count)
            card.clicked.connect(self.on_topic_clicked)
            card.setFixedSize(200, 140)
            grid.addWidget(card, row, col)
            
            col += 1
            if col > 3: # 4 columns
                col = 0
                row += 1
                
        grid_widget = QWidget()
        grid_widget.setLayout(grid)
        
        scroll = QScrollArea()
        scroll.setWidget(grid_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        self.content_layout.addWidget(scroll)

    def create_topic_card(self, topic: str, color: str, question_count: int) -> ClickableCard:
        """Create a topic card with question count"""
        # Use ClickableCard but customize it
        card = ClickableCard(topic, color, "🎯")
        
        # Get the layout to add question count
        layout = card.layout()
        
        # Add question count label after title
        count_label = QLabel(f"{question_count} questions")
        count_label.setStyleSheet(f"font-size: 11px; color: {color}; font-weight: bold; border: none; background: transparent;")
        count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.insertWidget(2, count_label)  # Insert after icon and title
        
        return card

    def on_topic_clicked(self, topic):
        """Start test or learning for topic"""
        # Check if papers/questions exist (double check)
        available = self.question_service.get_available_papers(self.selected_grade, self.selected_subject, topic)
        
        # Note: For learning mode, we might not strictly need existing papers if we use the Agent to generate content on the fly.
        # But if the user clicked a specific topic card, it implies they want that topic.
        
        if self.selected_mode == "test":
            if not available:
                QMessageBox.warning(self, "Oops!", "No questions available for this topic yet.")
                return

            # Start Test
            self.test_screen = TestScreen(
                self.username, self.selected_grade, self.selected_subject, topic, 1
            )
            self.test_screen.test_completed.connect(self.on_test_completed)
            self.test_screen.back_signal.connect(self.on_test_back)
            self.test_screen.show()
            self.hide()
        else:
            # Start Learning
            # Get all available topics for suggestions
            all_topics = self.question_service.get_available_topics(self.selected_grade, self.selected_subject)
            
            self.learning_screen = LearningScreen(
                self.username, self.selected_grade, self.selected_subject, all_topics
            )
            self.learning_screen.back_signal.connect(self.on_learning_back)
            # Pre-select the topic if they clicked one
            self.learning_screen.set_topic(topic)
            self.learning_screen.show()
            self.hide()

    def on_learning_back(self):
        """Handle back from learning screen"""
        self.show()
        if hasattr(self, 'learning_screen'):
            self.learning_screen.close()

    def clear_content_area(self):
        """Clear the content area"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                # Recursively delete layout items
                self._clear_layout(child.layout())

    def _clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self._clear_layout(child.layout())

    def load_statistics(self):
        """Load and display student statistics"""
        try:
            from services.db_test_service import DBTestService
            from services.db_user_service import DBUserService
            
            user_service = DBUserService()
            test_service = DBTestService()
            
            user = user_service.get_user_by_username(self.username)
            if not user:
                return
                
            results = test_service.get_user_test_history(user['id'])
            
            # Clear previous stats
            while self.stats_layout.count():
                child = self.stats_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            if not results:
                no_tests = QLabel("No tests yet. Start learning! 🚀")
                no_tests.setStyleSheet("color: #999; font-style: italic;")
                self.stats_layout.addWidget(no_tests)
                return
            
            # Group stats
            stats_dict = {}
            for result in results:
                key = f"{result['subject']}\n{result['topic']}"
                if key not in stats_dict:
                    stats_dict[key] = []
                stats_dict[key].append(result['score_percentage'])
            
            # Create Stats Cards
            for key, scores in stats_dict.items():
                avg_score = sum(scores) / len(scores)
                best_score = max(scores)
                
                card = QFrame()
                card.setFixedSize(160, 140)
                
                # Color based on score
                color = ModernStyles.SECONDARY_GREEN if avg_score >= 80 else (ModernStyles.PRIMARY_ORANGE if avg_score >= 60 else "#E53935")
                
                card.setStyleSheet(f"""
                    QFrame {{
                        background-color: white;
                        border-radius: 15px;
                        border-bottom: 4px solid {color};
                    }}
                """)
                
                layout = QVBoxLayout(card)
                
                title = QLabel(key)
                title.setAlignment(Qt.AlignmentFlag.AlignCenter)
                title.setWordWrap(True)
                title.setStyleSheet("font-weight: bold; font-size: 12px;")
                layout.addWidget(title)
                
                score_lbl = QLabel(f"{avg_score:.0f}%")
                score_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                score_lbl.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {color};")
                layout.addWidget(score_lbl)
                
                sub_lbl = QLabel(f"Best: {best_score:.0f}%")
                sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                sub_lbl.setStyleSheet("color: #757575; font-size: 11px;")
                layout.addWidget(sub_lbl)
                
                # Shadow
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(10)
                shadow.setColor(QColor(0,0,0,20))
                card.setGraphicsEffect(shadow)
                
                self.stats_layout.addWidget(card)
                
            self.stats_layout.addStretch()

        except Exception as e:
            print(f"Stats Error: {e}")

    def on_test_completed(self, result: dict):
        self.show()
        if self.test_screen:
            self.test_screen.close()
        self.load_statistics()

    def on_test_back(self):
        self.show()
        if self.test_screen:
            self.test_screen.close()
        self.load_statistics()

    def logout(self):
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_signal.emit()
            self.close()
