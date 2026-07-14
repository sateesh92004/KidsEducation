"""
🎨 KIDS EDUCATION - Cartoon Brutalist Theme
Bold, playful, and super fun for kids!
"""

class ModernStyles:
    # 🎨 Core Kids Palette - Super Bright & Fun
    PRIMARY_YELLOW = "#FFD93D"      # Sunny yellow
    PRIMARY_ORANGE = "#FF6B35"      # Bright orange
    SECONDARY_GREEN = "#6BCB77"     # Grass green
    ACCENT_BLUE = "#4D96FF"         # Sky blue
    ACCENT_PURPLE = "#9B59B6"       # Magic purple
    ACCENT_PINK = "#FF6B9D"         # Bubblegum pink
    ACCENT_RED = "#FF4757"         # Apple red
    ACCENT_TEAL = "#00D2D3"        # Ocean teal
    
    # Text colors
    TEXT_DARK = "#2D3436"           # Almost black
    TEXT_LIGHT = "#FFFFFF"          # White
    TEXT_GRAY = "#636E72"           # Friendly gray
    
    # Backgrounds
    BG_MAIN = "#FFF8E7"             # Warm cream
    CARD_BG = "#FFFFFF"             # White
    BG_BLUE_SOFT = "#E8F4FD"        # Soft sky
    BG_GREEN_SOFT = "#E8F8E8"       # Soft grass
    BG_YELLOW_SOFT = "#FFF3CD"      # Soft sunshine
    BG_PINK_SOFT = "#FDE8EF"        # Soft cotton candy
    BG_PURPLE_SOFT = "#F3E8FF"      # Soft lavender
    
    # Shadows (for QGraphicsDropShadowEffect in code)
    SHADOW_COLOR = "rgba(0, 0, 0, 0.15)"
    
    @staticmethod
    def get_main_window_style():
        return f"""
            QMainWindow {{
                background-color: {ModernStyles.BG_MAIN};
            }}
            QWidget {{
                font-family: 'Segoe UI', 'Comic Sans MS', 'Chalkboard SE', sans-serif;
                color: {ModernStyles.TEXT_DARK};
            }}
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                background-color: #F5E6D3;
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {ModernStyles.ACCENT_BLUE};
                border-radius: 6px;
                min-height: 30px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                background-color: #F5E6D3;
                height: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {ModernStyles.ACCENT_BLUE};
                border-radius: 6px;
                min-width: 30px;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """
    
    @staticmethod
    def get_card_style(color="#FFFFFF", border_color="#FFD93D"):
        return f"""
            QFrame {{
                background-color: {color};
                border-radius: 20px;
                border: 3px solid {border_color};
            }}
        """
    
    @staticmethod
    def get_big_button_style(base_color="#FFD93D", text_color="#2D3436"):
        """Super chunky fun button for kids"""
        hover_color = ModernStyles._lighten(base_color, 20)
        return f"""
            QPushButton {{
                background-color: {base_color};
                color: {text_color};
                border: 3px solid {ModernStyles.TEXT_DARK};
                border-radius: 20px;
                padding: 16px 32px;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border: 4px solid {ModernStyles.TEXT_DARK};
                margin-top: -2px;
            }}
            QPushButton:pressed {{
                background-color: {ModernStyles._darken(base_color, 15)};
                margin-top: 4px;
            }}
        """
    
    @staticmethod
    def _lighten(color, percent):
        """Lighten a hex color by percent"""
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        r = min(255, r + int((255 - r) * percent / 100))
        g = min(255, g + int((255 - g) * percent / 100))
        b = min(255, b + int((255 - b) * percent / 100))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def _darken(color, percent):
        """Darken a hex color by percent"""
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        r = max(0, r - int(r * percent / 100))
        g = max(0, g - int(g * percent / 100))
        b = max(0, b - int(b * percent / 100))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def get_button_style(color="blue"):
        """Button styles using the color scheme"""
        styles = {
            "blue": (ModernStyles.ACCENT_BLUE, "#FFFFFF"),
            "green": (ModernStyles.SECONDARY_GREEN, "#FFFFFF"),
            "orange": (ModernStyles.PRIMARY_ORANGE, "#FFFFFF"),
            "yellow": (ModernStyles.PRIMARY_YELLOW, ModernStyles.TEXT_DARK),
            "pink": (ModernStyles.ACCENT_PINK, "#FFFFFF"),
            "purple": (ModernStyles.ACCENT_PURPLE, "#FFFFFF"),
            "teal": (ModernStyles.ACCENT_TEAL, "#FFFFFF"),
            "red": (ModernStyles.ACCENT_RED, "#FFFFFF"),
        }
        bg, fg = styles.get(color, (ModernStyles.ACCENT_BLUE, "#FFFFFF"))
        hover = ModernStyles._lighten(bg, 15)
        return ModernStyles.get_big_button_style(bg, fg)
    
    @staticmethod
    def get_input_style():
        return f"""
            QLineEdit {{
                background-color: white;
                border: 3px solid {ModernStyles.ACCENT_BLUE};
                border-radius: 20px;
                padding: 14px 20px;
                font-size: 16px;
                font-weight: bold;
            }}
            QLineEdit:focus {{
                border: 4px solid {ModernStyles.ACCENT_BLUE};
                background-color: {ModernStyles.BG_BLUE_SOFT};
            }}
            QLineEdit::placeholder {{
                color: #B2BEC3;
                font-weight: normal;
            }}
        """
    
    @staticmethod
    def get_tab_style():
        return f"""
            QTabWidget::pane {{
                border: 3px solid {ModernStyles.PRIMARY_YELLOW};
                border-radius: 15px;
                background: white;
                top: -2px;
            }}
            QTabBar::tab {{
                background: {ModernStyles.BG_YELLOW_SOFT};
                border: 2px solid {ModernStyles.PRIMARY_YELLOW};
                padding: 10px 25px;
                margin-right: 5px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                color: {ModernStyles.TEXT_DARK};
                font-weight: bold;
                font-size: 14px;
            }}
            QTabBar::tab:selected {{
                background: white;
                border-bottom-color: white;
                color: {ModernStyles.ACCENT_BLUE};
                font-size: 15px;
            }}
            QTabBar::tab:hover {{
                background: white;
                color: {ModernStyles.ACCENT_BLUE};
            }}
        """
    
    @staticmethod
    def get_topic_chip_style():
        return f"""
            QPushButton {{
                background-color: {ModernStyles.BG_BLUE_SOFT};
                color: {ModernStyles.ACCENT_BLUE};
                border: 2px solid {ModernStyles.ACCENT_BLUE};
                border-radius: 18px;
                padding: 6px 16px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {ModernStyles.ACCENT_BLUE};
                color: white;
                border: 3px solid {ModernStyles.PRIMARY_YELLOW};
            }}
        """
    
    @staticmethod
    def get_fun_fact_box_style():
        return f"""
            QFrame {{
                background-color: {ModernStyles.BG_YELLOW_SOFT};
                border: 3px solid {ModernStyles.PRIMARY_YELLOW};
                border-radius: 18px;
            }}
        """
    
    @staticmethod
    def get_image_card_style():
        return f"""
            QFrame {{
                background-color: white;
                border: 3px solid {ModernStyles.ACCENT_TEAL};
                border-radius: 15px;
            }}
        """
    
    @staticmethod
    def get_quiz_card_style():
        return f"""
            QFrame {{
                background-color: {ModernStyles.BG_GREEN_SOFT};
                border: 3px solid {ModernStyles.SECONDARY_GREEN};
                border-radius: 18px;
            }}
        """
