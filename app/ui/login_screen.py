"""Login and Registration Screen"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from services.auth_service import AuthService
from ui.base_window import BaseWindow


class LoginScreen(BaseWindow):
    """Login and Registration Screen"""

    # Signals
    student_login_success = pyqtSignal(str)  # username
    admin_login_success = pyqtSignal()

    def __init__(self):
        super().__init__("Kids Education - Login")
        self.auth_service = AuthService()
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("🎓 Kids Education Platform")
        title.setFont(self.get_title_font())
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Learn with AI-Generated Questions")
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(20)

        # Tab widget for Student/Admin
        tabs = QTabWidget()
        tabs.addTab(self.create_student_tab(), "Student")
        tabs.addTab(self.create_admin_tab(), "Admin")
        main_layout.addWidget(tabs)

        central_widget.setLayout(main_layout)

    def create_student_tab(self) -> QWidget:
        """Create student login/registration tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Sub-tabs for Login/Register
        sub_tabs = QTabWidget()
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
        layout.setContentsMargins(20, 20, 20, 20)

        # Username
        username_label = QLabel("Username:")
        username_label.setStyleSheet(self.get_label_style())
        layout.addWidget(username_label)
        self.student_login_username = QLineEdit()
        self.student_login_username.setPlaceholderText("Enter your username")
        self.student_login_username.setStyleSheet(self.get_input_style())
        layout.addWidget(self.student_login_username)

        # Password
        password_label = QLabel("Password:")
        password_label.setStyleSheet(self.get_label_style())
        layout.addWidget(password_label)
        self.student_login_password = QLineEdit()
        self.student_login_password.setPlaceholderText("Enter your password")
        self.student_login_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.student_login_password.setStyleSheet(self.get_input_style())
        layout.addWidget(self.student_login_password)

        # Login Button
        login_btn = QPushButton("Login")
        login_btn.setStyleSheet(self.get_button_style())
        login_btn.clicked.connect(self.student_login)
        layout.addWidget(login_btn)

        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def create_student_register_form(self) -> QWidget:
        """Create student registration form"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Info
        info = QLabel("Create a new account to get started!")
        info.setFont(self.get_normal_font())
        layout.addWidget(info)

        # Username
        username_label = QLabel("Username:")
        username_label.setStyleSheet(self.get_label_style())
        layout.addWidget(username_label)
        self.student_reg_username = QLineEdit()
        self.student_reg_username.setPlaceholderText("Choose a username (3-20 characters)")
        self.student_reg_username.setStyleSheet(self.get_input_style())
        layout.addWidget(self.student_reg_username)

        # Password
        password_label = QLabel("Password:")
        password_label.setStyleSheet(self.get_label_style())
        layout.addWidget(password_label)
        self.student_reg_password = QLineEdit()
        self.student_reg_password.setPlaceholderText("Choose a password (min 4 characters)")
        self.student_reg_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.student_reg_password.setStyleSheet(self.get_input_style())
        layout.addWidget(self.student_reg_password)

        # Confirm Password
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setStyleSheet(self.get_label_style())
        layout.addWidget(confirm_label)
        self.student_reg_confirm = QLineEdit()
        self.student_reg_confirm.setPlaceholderText("Confirm your password")
        self.student_reg_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.student_reg_confirm.setStyleSheet(self.get_input_style())
        layout.addWidget(self.student_reg_confirm)

        # Register Button
        register_btn = QPushButton("Register")
        register_btn.setStyleSheet(self.get_button_style())
        register_btn.clicked.connect(self.student_register)
        layout.addWidget(register_btn)

        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def create_admin_tab(self) -> QWidget:
        """Create admin login tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Info
        info = QLabel("⚙️ Admin Panel - Generate Question Papers")
        info.setFont(self.get_header_font())
        layout.addWidget(info)

        # Username
        username_label = QLabel("Admin Username:")
        username_label.setStyleSheet(self.get_label_style())
        layout.addWidget(username_label)
        self.admin_username = QLineEdit()
        self.admin_username.setPlaceholderText("Enter admin username")
        self.admin_username.setStyleSheet(self.get_input_style())
        layout.addWidget(self.admin_username)

        # Password
        password_label = QLabel("Admin Password:")
        password_label.setStyleSheet(self.get_label_style())
        layout.addWidget(password_label)
        self.admin_password = QLineEdit()
        self.admin_password.setPlaceholderText("Enter admin password")
        self.admin_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.admin_password.setStyleSheet(self.get_input_style())
        layout.addWidget(self.admin_password)

        # Login Button
        login_btn = QPushButton("Admin Login")
        login_btn.setStyleSheet(self.get_button_style())
        login_btn.clicked.connect(self.admin_login)
        layout.addWidget(login_btn)

        layout.addStretch()

        tab.setLayout(layout)
        return tab

    def student_login(self):
        """Handle student login"""
        username = self.student_login_username.text().strip()
        password = self.student_login_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        success, message = self.auth_service.login_student(username, password)

        if success:
            QMessageBox.information(self, "Success", message)
            self.student_login_success.emit(username)
            self.student_login_username.clear()
            self.student_login_password.clear()
        else:
            QMessageBox.warning(self, "Login Failed", message)

    def student_register(self):
        """Handle student registration"""
        username = self.student_reg_username.text().strip()
        password = self.student_reg_password.text()
        confirm = self.student_reg_confirm.text()

        if not username or not password or not confirm:
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return

        if password != confirm:
            QMessageBox.warning(self, "Password Mismatch", "Passwords do not match. Please try again.")
            return

        success, message = self.auth_service.register_student(username, password)

        if success:
            QMessageBox.information(self, "Success", message)
            self.student_reg_username.clear()
            self.student_reg_password.clear()
            self.student_reg_confirm.clear()
        else:
            QMessageBox.warning(self, "Registration Failed", message)

    def admin_login(self):
        """Handle admin login"""
        username = self.admin_username.text().strip()
        password = self.admin_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        success, message = self.auth_service.login_admin(username, password)

        if success:
            QMessageBox.information(self, "Success", message)
            self.admin_login_success.emit()
            self.admin_username.clear()
            self.admin_password.clear()
        else:
            QMessageBox.warning(self, "Login Failed", message)