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
        title = QLabel("⚙️ Admin Panel")
        title.setFont(self.get_title_font())
        header_layout.addWidget(title)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet(self.get_button_style())
        logout_btn.setMaximumWidth(120)
        logout_btn.clicked.connect(self.logout)
        header_layout.addStretch()
        header_layout.addWidget(logout_btn)
        main_layout.addLayout(header_layout)

        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_generation_tab(), "Generate Questions")
        tabs.addTab(self.create_prompts_tab(), "Custom Prompts")
        main_layout.addWidget(tabs)

        central_widget.setLayout(main_layout)

    def create_generation_tab(self) -> QWidget:
        """Create the question generation tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Grade Selection
        grade_label = QLabel("Select Grade Level:")
        grade_label.setFont(self.get_subheader_font())
        layout.addWidget(grade_label)
        
        self.grade_combo = QComboBox()
        self.grade_combo.addItems(GRADES)
        self.grade_combo.setStyleSheet(self.get_input_style())
        layout.addWidget(self.grade_combo)

        # Subject Selection
        subject_label = QLabel("Select Subject:")
        subject_label.setFont(self.get_subheader_font())
        layout.addWidget(subject_label)
        
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(SUBJECTS)
        self.subject_combo.setStyleSheet(self.get_input_style())
        layout.addWidget(self.subject_combo)

        # Topic Input
        topic_label = QLabel("Enter Topic Name:")
        topic_label.setFont(self.get_subheader_font())
        layout.addWidget(topic_label)
        
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("e.g., Algebra, Photosynthesis")
        self.topic_input.setStyleSheet(self.get_input_style())
        layout.addWidget(self.topic_input)

        layout.addSpacing(20)

        # Generate Button
        generate_btn = QPushButton("🚀 Generate Question Pool")
        generate_btn.setFont(self.get_header_font())
        generate_btn.setStyleSheet(self.get_button_style())
        generate_btn.setMinimumHeight(55)
        generate_btn.clicked.connect(self.generate_papers)
        layout.addWidget(generate_btn)

        # Log
        log_label = QLabel("Generation Log:")
        log_label.setFont(self.get_subheader_font())
        layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #F5F5F5; border: 1px solid #CCC; padding: 10px;")
        layout.addWidget(self.log_text)

        tab.setLayout(layout)
        return tab

    def create_prompts_tab(self) -> QWidget:
        """Create the custom prompts tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        info = QLabel("Define custom prompts for specific topics to guide the AI generation.")
        info.setFont(self.get_normal_font())
        layout.addWidget(info)
        
        # Inputs for prompt
        self.prompt_grade = QComboBox()
        self.prompt_grade.addItems(GRADES)
        layout.addWidget(QLabel("Grade:"))
        layout.addWidget(self.prompt_grade)
        
        self.prompt_subject = QComboBox()
        self.prompt_subject.addItems(SUBJECTS)
        layout.addWidget(QLabel("Subject:"))
        layout.addWidget(self.prompt_subject)
        
        self.prompt_topic = QLineEdit()
        self.prompt_topic.setPlaceholderText("Topic Name")
        layout.addWidget(QLabel("Topic:"))
        layout.addWidget(self.prompt_topic)
        
        self.prompt_name = QLineEdit()
        self.prompt_name.setPlaceholderText("Prompt Name (e.g., 'Hard Algebra Problems')")
        layout.addWidget(QLabel("Prompt Name:"))
        layout.addWidget(self.prompt_name)
        
        layout.addWidget(QLabel("Custom Prompt Instructions:"))
        self.prompt_text = QTextEdit()
        self.prompt_text.setPlaceholderText("Enter detailed instructions for the AI...")
        layout.addWidget(self.prompt_text)
        
        save_btn = QPushButton("Save Custom Prompt")
        save_btn.setStyleSheet(self.get_button_style())
        save_btn.clicked.connect(self.save_custom_prompt)
        layout.addWidget(save_btn)
        
        tab.setLayout(layout)
        return tab

    def save_custom_prompt(self):
        """Save the custom prompt to DB"""
        grade = self.prompt_grade.currentText()
        subject = self.prompt_subject.currentText()
        topic = self.prompt_topic.text().strip()
        name = self.prompt_name.text().strip()
        prompt = self.prompt_text.toPlainText().strip()
        
        if not topic or not name or not prompt:
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
            
        from services.db_prompt_service import DBPromptService
        prompt_service = DBPromptService()
        
        # Admin ID is hardcoded to 1 for now (since we auto-created admin)
        # In real app, get from auth service
        admin_id = 1 
        
        try:
            prompt_service.save_prompt(admin_id, grade, subject, topic, name, prompt)
            QMessageBox.information(self, "Success", "Custom prompt saved successfully!")
            self.prompt_topic.clear()
            self.prompt_name.clear()
            self.prompt_text.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save prompt: {e}")

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
        
        if result: # Result is list of papers or True/False depending on implementation
             self.log_text.append(f"✅ Generation Complete!\n")
             QMessageBox.information(self, "Success", "Questions generated and saved to database!")
        else:
             self.log_text.append(f"❌ Generation Failed\n")
             QMessageBox.warning(self, "Generation Failed", "Failed to generate questions.")

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