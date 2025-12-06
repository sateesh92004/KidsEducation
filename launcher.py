#!/usr/bin/env python3
"""
Kids Education App Launcher
Double-click to launch the application with a beautiful UI
"""

import sys
import os
import subprocess
import time
from pathlib import Path

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QProgressBar, QTextEdit, QTabWidget, QMessageBox
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
    from PyQt6.QtGui import QFont, QPixmap, QIcon, QColor
    from PyQt6.QtCore import QSize
except ImportError:
    print("PyQt6 not installed. Please run: pip install -r requirements.txt")
    sys.exit(1)


class AppLauncher(QThread):
    """Thread to launch the main app without blocking UI"""
    status_changed = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    progress_updated = pyqtSignal(int)

    def __init__(self, app_dir):
        super().__init__()
        self.app_dir = app_dir

    def run(self):
        try:
            # Step 1: Check virtual environment
            self.status_changed.emit("🔍 Checking virtual environment...")
            self.progress_updated.emit(20)
            venv_path = Path(self.app_dir) / "venv"
            if not venv_path.exists():
                self.status_changed.emit("📦 Creating virtual environment...")
                subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
            self.status_changed.emit("✅ Virtual environment ready!")
            self.progress_updated.emit(40)

            # Step 2: Check dependencies
            self.status_changed.emit("📚 Checking dependencies...")
            self.progress_updated.emit(60)
            venv_python = venv_path / "bin" / "python3" if os.name != 'nt' else venv_path / "Scripts" / "python.exe"
            
            # Try importing required packages
            try:
                result = subprocess.run(
                    [str(venv_python), "-c", "import PyQt6; import openpyxl"],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode != 0:
                    self.status_changed.emit("📥 Installing dependencies (may take a minute)...")
                    subprocess.run(
                        [str(venv_python), "-m", "pip", "install", "-r", 
                         str(Path(self.app_dir) / "requirements.txt")],
                        capture_output=True,
                        check=True
                    )
            except Exception:
                self.status_changed.emit("📥 Installing dependencies...")
                subprocess.run(
                    [str(venv_python), "-m", "pip", "install", "-r",
                     str(Path(self.app_dir) / "requirements.txt")],
                    capture_output=True
                )
            self.status_changed.emit("✅ Dependencies ready!")
            self.progress_updated.emit(80)

            # Step 3: Check Ollama
            self.status_changed.emit("🤖 Checking Ollama service...")
            try:
                import requests
                requests.get("http://localhost:11434/api/tags", timeout=2)
                self.status_changed.emit("✅ Ollama is running!")
            except Exception:
                self.status_changed.emit("⚠️  Ollama not detected (optional, but needed for question generation)")

            self.progress_updated.emit(90)

            # Step 4: Launch the app
            self.status_changed.emit("🚀 Launching Kids Education App...")
            time.sleep(1)
            self.progress_updated.emit(100)

            # Run the main app
            subprocess.Popen(
                [str(venv_python), str(Path(self.app_dir) / "app" / "main.py")],
                cwd=str(self.app_dir)
            )

            self.finished.emit(True, "App launched successfully!")
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")


class LauncherWindow(QMainWindow):
    """Beautiful launcher UI"""

    def __init__(self):
        super().__init__()
        self.app_dir = str(Path(__file__).parent)
        self.launcher_thread = None
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🎓 Kids Education App - Launcher")
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton#launchBtn {
                background-color: #667eea;
                color: white;
            }
            QPushButton#launchBtn:hover {
                background-color: #764ba2;
            }
            QPushButton#launchBtn:pressed {
                background-color: #5568d3;
            }
        """)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header = QLabel("🎓 Kids Education App")
        header_font = QFont()
        header_font.setPointSize(24)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        subtitle = QLabel("AI-Powered Question Generator")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666; font-size: 14px;")
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        # Status display
        status_label = QLabel("Ready to launch")
        status_label.setStyleSheet("color: #667eea; font-weight: bold; font-size: 12px;")
        layout.addWidget(status_label)
        self.status_label = status_label

        # Progress bar
        progress = QProgressBar()
        progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 8px;
                text-align: center;
                background-color: #f5f5f5;
            }
            QProgressBar::chunk {
                background-color: #667eea;
                border-radius: 6px;
            }
        """)
        progress.setValue(0)
        layout.addWidget(progress)
        self.progress_bar = progress

        layout.addSpacing(20)

        # Buttons
        button_layout = QHBoxLayout()
        
        launch_btn = QPushButton("🚀 Launch App")
        launch_btn.setObjectName("launchBtn")
        launch_btn.setMinimumHeight(50)
        launch_btn.clicked.connect(self.launch_app)
        button_layout.addWidget(launch_btn)
        self.launch_btn = launch_btn

        close_btn = QPushButton("✕ Close")
        close_btn.setObjectName("closeBtn")
        close_btn.setMinimumHeight(50)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #333;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        layout.addSpacing(20)

        # Info box
        info = QLabel(
            "💡 Tip: Make sure Ollama is running before starting the app.\n"
            "Open Applications → Ollama to start it."
        )
        info.setStyleSheet(
            "background-color: #f0f4ff; "
            "color: #333; "
            "padding: 12px; "
            "border-radius: 8px; "
            "border-left: 4px solid #667eea;"
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        layout.addStretch()

    def launch_app(self):
        """Launch the application"""
        self.launch_btn.setEnabled(False)
        self.status_label.setText("🔄 Preparing to launch...")
        self.progress_bar.setValue(0)

        # Create and start launcher thread
        self.launcher_thread = AppLauncher(self.app_dir)
        self.launcher_thread.status_changed.connect(self.on_status_changed)
        self.launcher_thread.progress_updated.connect(self.progress_bar.setValue)
        self.launcher_thread.finished.connect(self.on_launch_finished)
        self.launcher_thread.start()

    def on_status_changed(self, status):
        """Update status label"""
        self.status_label.setText(status)

    def on_launch_finished(self, success, message):
        """Handle launch completion"""
        self.launch_btn.setEnabled(True)
        if success:
            self.status_label.setText("✅ " + message)
            # Close launcher after 2 seconds
            QTimer.singleShot(2000, self.close)
        else:
            self.status_label.setText("❌ " + message)
            QMessageBox.critical(self, "Error", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LauncherWindow()
    window.show()
    sys.exit(app.exec())
