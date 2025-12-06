"""Main Application Entry Point"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ui.login_screen import LoginScreen
from ui.student_dashboard import StudentDashboard
from ui.admin_panel import AdminPanel
from utils.excel_handler import ExcelHandler


class KidsEducationApp:
    """Main Application Class"""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_screen = None
        self.student_dashboard = None
        self.admin_panel = None
        self.current_user = None
        
        # Initialize data
        self.init_data()
        
        # Show login screen
        self.show_login_screen()

    def init_data(self):
        """Initialize data files and folders"""
        # Ensure all necessary Excel files and folders exist
        ExcelHandler.ensure_data_folder()
        ExcelHandler.init_users_excel()
        ExcelHandler.init_test_results_excel()
        print("✅ Data initialization complete")

    def show_login_screen(self):
        """Show login screen"""
        self.login_screen = LoginScreen()
        self.login_screen.student_login_success.connect(self.on_student_login)
        self.login_screen.admin_login_success.connect(self.on_admin_login)
        self.login_screen.show()

    def on_student_login(self, username: str):
        """Handle student login"""
        self.current_user = username
        self.login_screen.hide()
        
        # Show student dashboard
        self.student_dashboard = StudentDashboard(username)
        self.student_dashboard.logout_signal.connect(self.on_student_logout)
        self.student_dashboard.show()

    def on_student_logout(self):
        """Handle student logout"""
        self.current_user = None
        if self.student_dashboard:
            self.student_dashboard.close()
        self.show_login_screen()

    def on_admin_login(self):
        """Handle admin login"""
        self.login_screen.hide()
        
        # Show admin panel
        self.admin_panel = AdminPanel()
        self.admin_panel.logout_signal.connect(self.on_admin_logout)
        self.admin_panel.show()

    def on_admin_logout(self):
        """Handle admin logout"""
        if self.admin_panel:
            self.admin_panel.close()
        self.show_login_screen()

    def run(self):
        """Run the application"""
        sys.exit(self.app.exec())


def main():
    """Main entry point"""
    app = KidsEducationApp()
    app.run()


if __name__ == "__main__":
    main()