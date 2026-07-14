"""Login and Registration Screen"""

import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QMessageBox, QCheckBox, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QLinearGradient, QPalette, QBrush
from services.auth_service import AuthService
from ui.base_window import BaseWindow
from ui.styles import ModernStyles

class LoginScreen(QMainWindow):
    """Login and Registration Screen"""

    # Signals
    student_login_success = pyqtSignal(str)  # username
    admin_login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kids Education - Login")
        self.resize(1000, 700)
        self.auth_service = AuthService()
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        # Set main background
        self.setStyleSheet(ModernStyles.get_main_window_style())
        
        # Central Widget with Gradient Background
        central_widget = QWidget()
        central_widget.setStyleSheet(f"""
            QWidget#CentralWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 {ModernStyles.ACCENT_BLUE}, 
                                          stop:1 {ModernStyles.ACCENT_PURPLE});
            }}
        """)
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        # Main Layout (Centering the card)
        main_layout = QVBoxLayout(central_widget)
        
        # Add stretch to push card to middle
        main_layout.addStretch()

        # Login Card
        card = QFrame()
        card.setFixedWidth(360)  # Smaller width as requested
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 20px;
            }}
        """)
        
        # Shadow for the card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 50))
        card.setGraphicsEffect(shadow)

        # Card Layout
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 30, 25, 30)
        card_layout.setSpacing(15)

        # Logo/Title
        title = QLabel("🚀 My Learning Portal") # Changed Name
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {ModernStyles.ACCENT_BLUE}; font-family: 'Segoe UI';")
        card_layout.addWidget(title)
        
        subtitle = QLabel("Your Learning Adventure Starts Here!")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 12px; color: #757575; margin-bottom: 5px;")
        card_layout.addWidget(subtitle)

        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet(ModernStyles.get_tab_style())
        tabs.addTab(self.create_student_tab(), "Student")
        tabs.addTab(self.create_admin_tab(), "Admin")
        card_layout.addWidget(tabs)

        main_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add stretch to push card to middle
        main_layout.addStretch()


    def create_student_tab(self) -> QWidget:
        """Create student login/registration tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Align top to avoid stretching

        # Sub-tabs for Login/Register
        sub_tabs = QTabWidget()
        sub_tabs.setStyleSheet(ModernStyles.get_tab_style())
        sub_tabs.addTab(self.create_student_login_form(), "Login")
        sub_tabs.addTab(self.create_student_register_form(), "Register")

        layout.addWidget(sub_tabs)
        tab.setLayout(layout)
        return tab

    def create_student_login_form(self) -> QWidget:
        """Create student login form"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(5, 15, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Align top

        self.student_login_username = QLineEdit()
        self.student_login_username.setPlaceholderText("👤 Username")
        self.student_login_username.setStyleSheet(ModernStyles.get_input_style())
        layout.addWidget(self.student_login_username)

        self.student_login_password = QLineEdit()
        self.student_login_password.setPlaceholderText("🔒 Password")
        self.student_login_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.student_login_password.setStyleSheet(ModernStyles.get_input_style())
        layout.addWidget(self.student_login_password)

        login_btn = QPushButton("Let's Go! 🚀")
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.setStyleSheet(ModernStyles.get_button_style("orange"))
        login_btn.clicked.connect(self.student_login)
        layout.addWidget(login_btn)

        widget.setLayout(layout)
        return widget

    def create_student_register_form(self) -> QWidget:
        """Create student registration form"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(5, 15, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Align top

        self.student_reg_username = QLineEdit()
        self.student_reg_username.setPlaceholderText("👤 Choose Username")
        self.student_reg_username.setStyleSheet(ModernStyles.get_input_style())
        layout.addWidget(self.student_reg_username)

        self.student_reg_password = QLineEdit()
        self.student_reg_password.setPlaceholderText("🔒 Choose Password")
        self.student_reg_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.student_reg_password.setStyleSheet(ModernStyles.get_input_style())
        layout.addWidget(self.student_reg_password)

        self.student_reg_confirm = QLineEdit()
        self.student_reg_confirm.setPlaceholderText("🔒 Confirm Password")
        self.student_reg_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.student_reg_confirm.setStyleSheet(ModernStyles.get_input_style())
        layout.addWidget(self.student_reg_confirm)

        register_btn = QPushButton("Create Account ✨")
        register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        register_btn.setStyleSheet(ModernStyles.get_button_style("green"))
        register_btn.clicked.connect(self.student_register)
        layout.addWidget(register_btn)

        widget.setLayout(layout)
        return widget

    def create_admin_tab(self) -> QWidget:
        """Create admin login tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(5, 15, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Align top

        self.admin_username = QLineEdit()
        self.admin_username.setPlaceholderText("🛡️ Admin Username")
        self.admin_username.setStyleSheet(ModernStyles.get_input_style())
        layout.addWidget(self.admin_username)

        self.admin_password = QLineEdit()
        self.admin_password.setPlaceholderText("🔑 Admin Password")
        self.admin_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.admin_password.setStyleSheet(ModernStyles.get_input_style())
        layout.addWidget(self.admin_password)

        login_btn = QPushButton("Admin Access")
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.setStyleSheet(ModernStyles.get_button_style("blue"))
        login_btn.clicked.connect(self.admin_login)
        layout.addWidget(login_btn)

        tab.setLayout(layout)
        return tab

    def student_login(self):
        """Handle student login"""
        username = self.student_login_username.text().strip()
        password = self.student_login_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        result = self.auth_service.login(username, password)

        if result["success"]:
            if result["user"]["role"] == "student":
                self.student_login_success.emit(username)
                self.student_login_username.clear()
                self.student_login_password.clear()
            else:
                QMessageBox.warning(self, "Login Failed", "This account is not a student account.")
        else:
            QMessageBox.warning(self, "Login Failed", result["message"])

    def student_register(self):
        """Handle student registration"""
        username = self.student_reg_username.text().strip()
        password = self.student_reg_password.text()
        confirm = self.student_reg_confirm.text()

        if not username or not password or not confirm:
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return

        if password != confirm:
            QMessageBox.warning(self, "Password Mismatch", "Passwords do not match.")
            return

        result = self.auth_service.register_student(username, password)

        if result["success"]:
            QMessageBox.information(self, "Success", "Account created! Please login.")
            self.student_reg_username.clear()
            self.student_reg_password.clear()
            self.student_reg_confirm.clear()
        else:
            QMessageBox.warning(self, "Registration Failed", result["message"])

    def admin_login(self):
        """Handle admin login"""
        username = self.admin_username.text().strip()
        password = self.admin_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        result = self.auth_service.login(username, password)

        if result["success"]:
            if result["user"]["role"] == "admin":
                self.admin_login_success.emit()
                self.admin_username.clear()
                self.admin_password.clear()
            else:
                QMessageBox.warning(self, "Login Failed", "Access denied. Admin privileges required.")
        else:
            QMessageBox.warning(self, "Login Failed", result["message"])