"""
Interactive Widgets for Learning Mode
Includes Flashcards and Mini-Quizzes
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QStackedWidget, QFrame, QButtonGroup, QRadioButton
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QRect
from PyQt6.QtGui import QFont, QColor, QCursor
from ui.styles import ModernStyles

class FlashCardWidget(QWidget):
    """A flippable flashcard widget"""
    
    def __init__(self, front_text, back_text):
        super().__init__()
        self.front_text = front_text
        self.back_text = back_text
        self.is_flipped = False
        
        self.init_ui()
        
    def init_ui(self):
        self.setFixedSize(300, 200)
        
        # Card Container
        self.card = QPushButton(self)
        self.card.setFixedSize(300, 200)
        self.card.setCursor(Qt.CursorShape.PointingHandCursor)
        self.card.clicked.connect(self.flip)
        
        self.update_style()
        self.card.setText(self.front_text)
        
    def update_style(self):
        color = "#E3F2FD" if not self.is_flipped else "#FFF3E0"
        border = "#2196F3" if not self.is_flipped else "#FF9800"
        text_color = "#1565C0" if not self.is_flipped else "#E65100"
        
        self.card.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: 2px solid {border};
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
                color: {text_color};
                padding: 20px;
                text-align: center;
            }}
        """)
        
    def flip(self):
        self.is_flipped = not self.is_flipped
        self.update_style()
        self.card.setText(self.back_text if self.is_flipped else self.front_text)

class FlashCardDeck(QWidget):
    """Container for multiple flashcards"""
    
    def __init__(self, cards_data):
        super().__init__()
        self.cards_data = cards_data
        self.current_index = 0
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("📝 Flashcards")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Card Area
        self.card_stack = QStackedWidget()
        self.card_stack.setFixedSize(320, 220)
        
        for data in self.cards_data:
            card = FlashCardWidget(data['front'], data['back'])
            container = QWidget()
            l = QVBoxLayout(container)
            l.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
            self.card_stack.addWidget(container)
            
        layout.addWidget(self.card_stack, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Controls
        controls = QHBoxLayout()
        
        prev_btn = QPushButton("◀ Prev")
        prev_btn.clicked.connect(self.prev_card)
        prev_btn.setStyleSheet(ModernStyles.get_button_style("blue"))
        prev_btn.setFixedSize(100, 40)
        
        next_btn = QPushButton("Next ▶")
        next_btn.clicked.connect(self.next_card)
        next_btn.setStyleSheet(ModernStyles.get_button_style("blue"))
        next_btn.setFixedSize(100, 40)
        
        controls.addWidget(prev_btn)
        self.lbl_counter = QLabel(f"1/{len(self.cards_data)}")
        controls.addWidget(self.lbl_counter, alignment=Qt.AlignmentFlag.AlignCenter)
        controls.addWidget(next_btn)
        
        layout.addLayout(controls)
        
    def next_card(self):
        if self.current_index < self.card_stack.count() - 1:
            self.current_index += 1
            self.card_stack.setCurrentIndex(self.current_index)
            self.update_counter()
            
    def prev_card(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.card_stack.setCurrentIndex(self.current_index)
            self.update_counter()
            
    def update_counter(self):
        self.lbl_counter.setText(f"{self.current_index + 1}/{self.card_stack.count()}")

class QuizWidget(QWidget):
    """Mini Quiz Widget"""
    
    def __init__(self, quiz_data):
        super().__init__()
        self.quiz_data = quiz_data
        self.score = 0
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        title = QLabel("🧠 Quick Quiz")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2E7D32;")
        layout.addWidget(title)
        
        self.question_widgets = []
        
        for i, q in enumerate(self.quiz_data):
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background-color: #F1F8E9;
                    border: 1px solid #C5E1A5;
                    border-radius: 10px;
                    padding: 10px;
                }
            """)
            q_layout = QVBoxLayout(frame)
            
            # Question Text
            lbl_q = QLabel(f"{i+1}. {q['question']}")
            lbl_q.setWordWrap(True)
            lbl_q.setStyleSheet("font-weight: bold; font-size: 14px;")
            q_layout.addWidget(lbl_q)
            
            # Options
            btn_group = QButtonGroup(frame)
            options_layout = QVBoxLayout()
            
            for j, opt in enumerate(q['options']):
                rb = QRadioButton(opt)
                rb.setStyleSheet("font-size: 13px; padding: 5px;")
                btn_group.addButton(rb, j)
                options_layout.addWidget(rb)
                
            q_layout.addLayout(options_layout)
            
            # Feedback Label (Hidden initially)
            lbl_feedback = QLabel("")
            lbl_feedback.setWordWrap(True)
            lbl_feedback.hide()
            q_layout.addWidget(lbl_feedback)
            
            self.question_widgets.append({
                "group": btn_group,
                "feedback": lbl_feedback,
                "correct": q['correct_index'],
                "explanation": q.get('explanation', '')
            })
            
            layout.addWidget(frame)
            
        # Submit Button
        self.btn_submit = QPushButton("Submit Answers")
        self.btn_submit.setStyleSheet(ModernStyles.get_button_style("green"))
        self.btn_submit.clicked.connect(self.check_answers)
        layout.addWidget(self.btn_submit, alignment=Qt.AlignmentFlag.AlignCenter)
        
    def check_answers(self):
        score = 0
        total = len(self.question_widgets)
        
        for qw in self.question_widgets:
            group = qw['group']
            feedback = qw['feedback']
            correct_idx = qw['correct']
            explanation = qw['explanation']
            
            selected_id = group.checkedId()
            
            if selected_id == -1:
                feedback.setText("❌ Please select an answer.")
                feedback.setStyleSheet("color: orange;")
                feedback.show()
                continue
                
            if selected_id == correct_idx:
                score += 1
                feedback.setText("✅ Correct!")
                feedback.setStyleSheet("color: green; font-weight: bold;")
            else:
                feedback.setText(f"❌ Incorrect. {explanation}")
                feedback.setStyleSheet("color: red;")
                
            feedback.show()
            
            # Disable radio buttons
            for btn in group.buttons():
                btn.setEnabled(False)
                
        self.btn_submit.setEnabled(False)
        self.btn_submit.setText(f"Score: {score}/{total}")
