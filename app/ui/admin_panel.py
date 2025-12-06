"""Admin Panel for generating question papers"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit,
    QPushButton, QMessageBox, QProgressDialog, QTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from services.question_service import QuestionService
from utils.constants import GRADES, SUBJECTS
from ui.base_window import BaseWindow


class PaperGenerationWorker(QThread):
    """Worker thread for paper generation"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, grade: str, subject: str, topic: str):
        super().__init__()
        self.grade = grade
        self.subject = subject
        self.topic = topic
        self.question_service = QuestionService()

    def run(self):
        """Run paper generation in background"""
        try:
            self.progress.emit("Starting paper generation...")
            result = self.question_service.generate_papers_for_topic(
                self.grade, self.subject, self.topic
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class AdminPanel(BaseWindow):
    """Admin Panel Screen"""

    logout_signal = pyqtSignal()

    def __init__(self):
        super().__init__("Kids Education - Admin Panel", 1100, 700)
        self.question_service = QuestionService()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("⚙️ Admin Panel - Question Paper Generator")
        title.setFont(self.get_title_font())
        header_layout.addWidget(title)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet(self.get_button_style())
        logout_btn.setMaximumWidth(120)
        logout_btn.clicked.connect(self.logout)
        header_layout.addStretch()
        header_layout.addWidget(logout_btn)
        main_layout.addLayout(header_layout)

        # Separator
        separator = QLabel()
        separator.setStyleSheet("border-bottom: 2px solid #CCCCCC;")
        main_layout.addWidget(separator)

        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Grade Selection
        grade_label = QLabel("Select Grade Level:")
        grade_label.setFont(self.get_subheader_font())
        grade_label.setStyleSheet("color: #333333; font-weight: bold;")
        form_layout.addWidget(grade_label)
        
        self.grade_combo = QComboBox()
        self.grade_combo.addItems(GRADES)
        self.grade_combo.setStyleSheet(self.get_input_style())
        self.grade_combo.setMinimumHeight(50)
        self.grade_combo.setFont(self.get_normal_font())
        form_layout.addWidget(self.grade_combo)

        # Subject Selection
        subject_label = QLabel("Select Subject:")
        subject_label.setFont(self.get_subheader_font())
        subject_label.setStyleSheet("color: #333333; font-weight: bold;")
        form_layout.addWidget(subject_label)
        
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(SUBJECTS)
        self.subject_combo.setStyleSheet(self.get_input_style())
        self.subject_combo.setMinimumHeight(50)
        self.subject_combo.setFont(self.get_normal_font())
        form_layout.addWidget(self.subject_combo)

        # Topic Input
        topic_label = QLabel("Enter Topic Name:")
        topic_label.setFont(self.get_subheader_font())
        topic_label.setStyleSheet("color: #333333; font-weight: bold;")
        form_layout.addWidget(topic_label)
        
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("e.g., Algebra, Photosynthesis, Forces and Motion")
        self.topic_input.setStyleSheet(self.get_input_style())
        self.topic_input.setMinimumHeight(50)
        self.topic_input.setFont(self.get_normal_font())
        form_layout.addWidget(self.topic_input)

        main_layout.addLayout(form_layout)

        # Generate Button
        generate_btn = QPushButton("🚀 Generate 10 Question Papers")
        generate_btn.setFont(self.get_header_font())
        generate_btn.setStyleSheet(self.get_button_style())
        generate_btn.setMinimumHeight(55)
        generate_btn.clicked.connect(self.generate_papers)
        main_layout.addWidget(generate_btn)

        # Status/Log area
        log_label = QLabel("Generation Log:")
        log_label.setFont(self.get_subheader_font())
        log_label.setStyleSheet("color: #333333; font-weight: bold;")
        main_layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #F5F5F5;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                color: #333333;
            }
        """)
        self.log_text.setMinimumHeight(220)
        main_layout.addWidget(self.log_text)

        main_layout.addStretch()

        central_widget.setLayout(main_layout)

    def generate_papers(self):
        """Generate question papers"""
        grade = self.grade_combo.currentText()
        subject = self.subject_combo.currentText()
        topic = self.topic_input.text().strip()

        if not topic:
            QMessageBox.warning(self, "Input Error", "Please enter a topic name.")
            return

        # Clear log
        self.log_text.clear()
        self.log_text.append(f"Generating question papers for:\nGrade: {grade}\nSubject: {subject}\nTopic: {topic}\n")
        self.log_text.append("="*50)
        self.log_text.append("Starting generation... This may take a few minutes.\n")

        # Create worker thread
        self.worker = PaperGenerationWorker(grade, subject, topic)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)
        self.worker.start()

    def on_progress(self, message: str):
        """Handle progress updates"""
        self.log_text.append(message)

    def on_generation_finished(self, result: dict):
        """Handle generation completion"""
        self.log_text.append("\n" + "="*50)
        
        if result["success"]:
            self.log_text.append(f"✅ {result['message']}\n")
            
            for paper in result["papers"]:
                self.log_text.append(f"  • Paper {paper['paper_number']}: Generated")
            
            QMessageBox.information(self, "Success", result["message"])
        else:
            self.log_text.append(f"❌ Error: {result['message']}\n")
            QMessageBox.warning(self, "Generation Failed", result["message"])

    def on_generation_error(self, error: str):
        """Handle generation errors"""
        self.log_text.append(f"\n❌ Error: {error}\n")
        QMessageBox.critical(self, "Error", f"Generation failed: {error}")

    def logout(self):
        """Logout from admin panel"""
        reply = QMessageBox.question(
            self, "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_signal.emit()
            self.close()