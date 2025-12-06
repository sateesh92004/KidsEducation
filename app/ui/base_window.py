"""Base Window for the Application"""

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette


class BaseWindow(QMainWindow):
    """Base window class with common styling"""

    def __init__(self, title: str = "Kids Education", width: int = 1000, height: int = 700):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, width, height)
        self.init_styles()

    def init_styles(self):
        """Initialize application styling"""
        # Set modern color scheme
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(245, 248, 252))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(33, 47, 61))
        self.setPalette(palette)

    def get_button_style(self) -> str:
        """Get modern button styling with better appearance"""
        return """
            QPushButton {
                background-color: #4472C4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #2E5DA6;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15);
            }
            QPushButton:pressed {
                background-color: #1F3A72;
                padding: 13px 23px;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
        """

    def get_success_button_style(self) -> str:
        """Get success button styling (green)"""
        return """
            QPushButton {
                background-color: #70AD47;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #548235;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15);
            }
            QPushButton:pressed {
                background-color: #375623;
                padding: 13px 23px;
            }
        """

    def get_input_style(self) -> str:
        """Get modern input field styling"""
        return """
            QLineEdit, QComboBox, QTextEdit {
                background-color: white;
                border: 2px solid #E8EEF5;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #212F3D;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 2px solid #4472C4;
                background-color: #F8FAFC;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
        """

    def get_label_style(self) -> str:
        """Get modern label styling"""
        return """
            QLabel {
                color: #333333;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """

    def get_title_font(self) -> QFont:
        """Get title font - larger and bolder"""
        font = QFont()
        font.setFamily('Segoe UI')
        font.setPointSize(22)  # Increased from 18
        font.setBold(True)
        return font

    def get_header_font(self) -> QFont:
        """Get header font - larger"""
        font = QFont()
        font.setFamily('Segoe UI')
        font.setPointSize(16)  # Increased from 14
        font.setBold(True)
        return font

    def get_subheader_font(self) -> QFont:
        """Get sub-header font"""
        font = QFont()
        font.setFamily('Segoe UI')
        font.setPointSize(14)
        font.setBold(True)
        return font

    def get_normal_font(self) -> QFont:
        """Get normal font - larger"""
        font = QFont()
        font.setFamily('Segoe UI')
        font.setPointSize(13)  # Increased from 11
        return font

    def get_large_font(self) -> QFont:
        """Get large font for important text"""
        font = QFont()
        font.setFamily('Segoe UI')
        font.setPointSize(15)
        font.setBold(True)
        return font
