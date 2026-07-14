"""
🎮 Kids Learning Screen - Complete Redesign
Cartoon Brutalist style with LLM + DuckDuckGo + OpenTriviaDB content
"""

import requests
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextBrowser, QProgressBar,
    QScrollArea, QFrame, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QPixmap
from ui.styles import ModernStyles
from services.learning_agent import LearningAgent
from utils.grade_topics import GRADE_TOPICS
from services.content_enricher import ContentEnricher
import markdown
import random


class ContentWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, agent, grade, subject, topic, custom_query, mode="initial", previous_content=None):
        super().__init__()
        self.agent = agent
        self.grade = grade
        self.subject = subject
        self.topic = topic
        self.custom_query = custom_query
        self.mode = mode
        self.previous_content = previous_content

    def run(self):
        if self.mode == "initial":
            stream = self.agent.teach_topic_stream(self.grade, self.subject, self.topic, self.custom_query)
        else:
            stream = self.agent.teach_more_stream(self.grade, self.subject, self.topic, self.previous_content)
        for chunk in stream:
            self.progress.emit(chunk)
        self.finished.emit()


class ImageDownloader(QThread):
    image_downloaded = pyqtSignal(dict)

    def __init__(self, images):
        super().__init__()
        self.images = images

    def run(self):
        for img in self.images:
            url = img.get("thumbnail_url") or img.get("url")
            if not url:
                continue
            try:
                r = requests.get(url, headers={"User-Agent": "KidsEducationApp/1.0"}, timeout=8)
                if r.status_code == 200:
                    self.image_downloaded.emit({"data": r.content, "title": img.get("title", "")})
            except:
                pass


class FunFactCard(QFrame):
    def __init__(self, fact_text, emoji="🌟"):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{ background-color: {ModernStyles.BG_YELLOW_SOFT}; border: 3px solid {ModernStyles.PRIMARY_YELLOW}; border-radius: 18px; }}
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        e = QLabel(emoji)
        e.setStyleSheet("font-size: 28px; border: none; background: transparent;")
        layout.addWidget(e)
        f = QLabel(fact_text)
        f.setWordWrap(True)
        f.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {ModernStyles.TEXT_DARK}; border: none; background: transparent;")
        layout.addWidget(f, 1)
        s = QGraphicsDropShadowEffect(); s.setBlurRadius(12); s.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(s)


class QuizCard(QFrame):
    def __init__(self, quiz_data, index):
        super().__init__()
        self.quiz_data = quiz_data
        self.answered = False
        self.setStyleSheet(f"""
            QFrame {{ background-color: {ModernStyles.BG_GREEN_SOFT}; border: 3px solid {ModernStyles.SECONDARY_GREEN}; border-radius: 18px; }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18); layout.setSpacing(10)
        h = QHBoxLayout()
        n = QLabel(f"🎯 Q{index+1}")
        n.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {ModernStyles.SECONDARY_GREEN}; border: none;")
        h.addWidget(n); h.addStretch(); layout.addLayout(h)
        q = QLabel(quiz_data.get("question", ""))
        q.setWordWrap(True)
        q.setStyleSheet(f"font-size: 15px; font-weight: bold; color: {ModernStyles.TEXT_DARK}; border: none; padding: 5px 0;")
        layout.addWidget(q)
        self.btns = []
        for i, opt in enumerate(quiz_data.get("options", [])):
            btn = QPushButton(f"  {chr(65+i)}. {opt}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{ background-color: white; border: 2px solid {ModernStyles.SECONDARY_GREEN}; border-radius: 12px;
                    padding: 10px 15px; text-align: left; font-size: 13px; font-weight: bold; }}
                QPushButton:hover {{ background-color: {ModernStyles.BG_GREEN_SOFT}; border: 3px solid {ModernStyles.SECONDARY_GREEN}; }}
            """)
            btn.clicked.connect(lambda checked, idx=i: self.check(idx))
            layout.addWidget(btn); self.btns.append(btn)
        self.feedback = QLabel()
        self.feedback.setWordWrap(True); self.feedback.hide()
        self.feedback.setStyleSheet("font-size: 13px; font-weight: bold; padding: 10px; border-radius: 10px; border: none; background: transparent;")
        layout.addWidget(self.feedback)
        s = QGraphicsDropShadowEffect(); s.setBlurRadius(12); s.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(s)

    def check(self, idx):
        if self.answered: return
        self.answered = True
        correct = self.quiz_data.get("correct_answer", "")
        selected = self.quiz_data.get("options", [])[idx]
        for i, btn in enumerate(self.btns):
            opt = self.quiz_data.get("options", [])[i]
            if opt == correct:
                btn.setStyleSheet(f"QPushButton {{ background-color: {ModernStyles.SECONDARY_GREEN}; color: white; border: 3px solid #2ECC71; border-radius: 12px; padding: 10px 15px; text-align: left; font-size: 13px; font-weight: bold; }}")
            elif i == idx:
                btn.setStyleSheet(f"QPushButton {{ background-color: {ModernStyles.ACCENT_RED}; color: white; border: 3px solid {ModernStyles.ACCENT_RED}; border-radius: 12px; padding: 10px 15px; text-align: left; font-size: 13px; font-weight: bold; }}")
            else:
                btn.setStyleSheet("QPushButton { background-color: #F0F0F0; border: 2px solid #DDD; border-radius: 12px; padding: 10px 15px; text-align: left; font-size: 13px; font-weight: bold; color: #999; }")
            btn.setEnabled(False)
        if selected == correct:
            self.feedback.setText("✅ Correct! Great job! 🌟")
            self.feedback.setStyleSheet("font-size: 14px; font-weight: bold; color: #27AE60; padding: 10px; background-color: #D5F5E3; border-radius: 10px;")
        else:
            self.feedback.setText(f"❌ The answer was: {correct}")
            self.feedback.setStyleSheet("font-size: 14px; font-weight: bold; color: #E74C3C; padding: 10px; background-color: #FADBD8; border-radius: 10px;")
        self.feedback.show()


class ImageGalleryCard(QFrame):
    def __init__(self, pixmap, title=""):
        super().__init__()
        self.setStyleSheet(f"QFrame {{ background-color: white; border: 3px solid {ModernStyles.ACCENT_TEAL}; border-radius: 15px; }}")
        layout = QVBoxLayout(self); layout.setContentsMargins(8, 8, 8, 8); layout.setSpacing(5)
        img = QLabel()
        scaled = pixmap.scaled(220, 160, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        img.setPixmap(scaled); img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img.setStyleSheet("border: none; border-radius: 10px;")
        layout.addWidget(img)
        if title:
            t = QLabel(title[:40]); t.setWordWrap(True)
            t.setStyleSheet("font-size: 10px; color: #888; border: none; text-align: center;")
            t.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(t)
        s = QGraphicsDropShadowEffect(); s.setBlurRadius(10); s.setColor(QColor(0, 0, 0, 25))
        self.setGraphicsEffect(s)


class LearningScreen(QMainWindow):
    back_signal = pyqtSignal()

    def __init__(self, username, grade, subject, available_topics):
        super().__init__()
        self.username = username; self.grade = grade; self.subject = subject
        self.available_topics = available_topics
        self.agent = LearningAgent(); self.enricher = ContentEnricher()
        self.current_content = ""
        self.setWindowTitle(f"🎮 Learning: {subject}")
        self.resize(1300, 950); self.setMinimumSize(1000, 700)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(ModernStyles.get_main_window_style())
        cw = QWidget(); self.setCentralWidget(cw)
        ml = QVBoxLayout(cw); ml.setContentsMargins(0, 0, 0, 0); ml.setSpacing(0)

        # HEADER
        hdr = QFrame()
        hdr.setStyleSheet(f"""
            QFrame {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {ModernStyles.ACCENT_BLUE}, stop:0.5 {ModernStyles.ACCENT_PURPLE}, stop:1 {ModernStyles.ACCENT_PINK});
                border-bottom: 4px solid {ModernStyles.PRIMARY_YELLOW}; }}
        """)
        hdr.setFixedHeight(80)
        hl = QHBoxLayout(hdr); hl.setContentsMargins(25, 10, 25, 10)
        back_btn = QPushButton("⬅️")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor); back_btn.setFixedSize(50, 50)
        back_btn.setStyleSheet("QPushButton { background-color: rgba(255,255,255,0.3); border: 2px solid white; border-radius: 25px; font-size: 24px; } QPushButton:hover { background-color: rgba(255,255,255,0.5); border: 3px solid white; }")
        back_btn.clicked.connect(self.on_back); hl.addWidget(back_btn)
        title = QLabel(f"📚 {self.subject} Explorer")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: white; border: none;")
        hl.addWidget(title)
        mascot = QLabel(random.choice(["🦉", "🤖", "🐱", "🦊", "🐼", "🐨", "🦁", "🐯"]))
        mascot.setStyleSheet("font-size: 36px; border: none;"); hl.addStretch(); hl.addWidget(mascot)
        badge = QLabel(f"Grade {self.grade}")
        badge.setStyleSheet(f"background-color: {ModernStyles.PRIMARY_YELLOW}; color: {ModernStyles.TEXT_DARK}; border: 2px solid {ModernStyles.TEXT_DARK}; border-radius: 15px; padding: 6px 18px; font-size: 14px; font-weight: bold;")
        hl.addWidget(badge)
        ml.addWidget(hdr)

        # SCROLL AREA
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        content_widget = QWidget()
        content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.cl = QVBoxLayout(content_widget)
        self.cl.setContentsMargins(8, 8, 8, 8); self.cl.setSpacing(12)
        scroll.setWidget(content_widget); ml.addWidget(scroll, 1)

        # SEARCH
        self.search_frame = QFrame()
        self.search_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.search_frame.setStyleSheet(f"QFrame {{ background-color: white; border: 3px solid {ModernStyles.PRIMARY_YELLOW}; border-radius: 24px; }}")
        sl = QVBoxLayout(self.search_frame); sl.setContentsMargins(25, 20, 25, 20); sl.setSpacing(12)
        pl = QLabel("🔍 What do you want to explore today?")
        pl.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {ModernStyles.TEXT_DARK}; border: none;")
        sl.addWidget(pl)
        sr = QHBoxLayout()
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Type anything — Photosynthesis, Fractions, Ancient Egypt...")
        self.topic_input.setStyleSheet(ModernStyles.get_input_style())
        self.topic_input.returnPressed.connect(self.start_learning); sr.addWidget(self.topic_input)
        go_btn = QPushButton("🚀 Explore!")
        go_btn.setCursor(Qt.CursorShape.PointingHandCursor); go_btn.setMinimumWidth(150)
        go_btn.setStyleSheet(ModernStyles.get_button_style("orange"))
        go_btn.clicked.connect(self.start_learning); sr.addWidget(go_btn)
        sl.addLayout(sr)

        topics = self.available_topics
        if not topics:
            gt = GRADE_TOPICS.get(self.grade, {})
            topics = gt.get(self.subject, [])
        if topics:
            clbl = QLabel("⚡ Quick pick:")
            clbl.setStyleSheet("font-size: 13px; color: #999; border: none;"); sl.addWidget(clbl)
            cs = QScrollArea(); cs.setWidgetResizable(True); cs.setFixedHeight(50)
            cs.setStyleSheet("border: none; background: transparent;")
            cw2 = QWidget(); cl2 = QHBoxLayout(cw2); cl2.setContentsMargins(0,0,0,0); cl2.setSpacing(8)
            for t in random.sample(topics, min(12, len(topics))):
                b = QPushButton(t); b.setCursor(Qt.CursorShape.PointingHandCursor)
                b.setStyleSheet(ModernStyles.get_topic_chip_style())
                b.clicked.connect(lambda checked, tt=t: self.set_topic(tt))
                cl2.addWidget(b)
            cl2.addStretch(); cs.setWidget(cw2); sl.addWidget(cs)
        self.cl.addWidget(self.search_frame)

        # LOADING
        self.loading_frame = QFrame()
        self.loading_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.loading_frame.hide()
        self.loading_frame.setStyleSheet(f"QFrame {{ background-color: white; border: 3px solid {ModernStyles.ACCENT_BLUE}; border-radius: 24px; }}")
        ll = QVBoxLayout(self.loading_frame); ll.setContentsMargins(30, 25, 30, 25); ll.setAlignment(Qt.AlignmentFlag.AlignCenter)
        le = QLabel("🔍"); le.setStyleSheet("font-size: 48px; border: none;"); le.setAlignment(Qt.AlignmentFlag.AlignCenter); ll.addWidget(le)
        self.loading_text = QLabel("🤖 AI Teacher is preparing your lesson...")
        self.loading_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_text.setStyleSheet("font-size: 18px; font-weight: bold; color: #888; border: none; margin: 10px 0;")
        ll.addWidget(self.loading_text)
        self.loading_bar = QProgressBar(); self.loading_bar.setRange(0, 0); self.loading_bar.setFixedHeight(12)
        self.loading_bar.setStyleSheet(f"""
            QProgressBar {{ border: 2px solid {ModernStyles.ACCENT_BLUE}; border-radius: 6px; text-align: center; background-color: {ModernStyles.BG_BLUE_SOFT}; }}
            QProgressBar::chunk {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {ModernStyles.ACCENT_BLUE}, stop:1 {ModernStyles.ACCENT_PURPLE}); border-radius: 4px; }}
        """)
        ll.addWidget(self.loading_bar)
        self.cl.addWidget(self.loading_frame)

        # RESULT AREA
        self.result_frame = QFrame()
        self.result_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.result_frame.hide()
        self.result_frame.setStyleSheet(f"QFrame {{ background-color: white; border: 3px solid {ModernStyles.ACCENT_TEAL}; border-radius: 24px; }}")
        rl = QVBoxLayout(self.result_frame); rl.setContentsMargins(0, 0, 0, 0); rl.setSpacing(0)
        rs = QScrollArea(); rs.setWidgetResizable(True)
        rs.setStyleSheet("QScrollArea { border: none; background: transparent; border-radius: 24px; }")
        ri = QWidget(); self.ril = QVBoxLayout(ri)
        self.ril.setContentsMargins(8, 8, 8, 8); self.ril.setSpacing(12)
        rs.setWidget(ri); rl.addWidget(rs)
        self.cl.addWidget(self.result_frame)

        # EMPTY STATE
        self.empty_frame = QFrame()
        self.empty_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.empty_frame.setStyleSheet("QFrame { background-color: white; border: 3px dashed #DDD; border-radius: 24px; }")
        el = QVBoxLayout(self.empty_frame); el.setContentsMargins(40, 50, 40, 50); el.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ee = QLabel("🤖"); ee.setStyleSheet("font-size: 72px; border: none;"); ee.setAlignment(Qt.AlignmentFlag.AlignCenter); el.addWidget(ee)
        et = QLabel("Ready to Learn Something Awesome?")
        et.setAlignment(Qt.AlignmentFlag.AlignCenter)
        et.setStyleSheet("font-size: 24px; font-weight: bold; color: #666; border: none; margin-top: 15px;")
        el.addWidget(et)
        es = QLabel("Type a topic above and hit 🚀 Explore!\nI'll find images, and teach you everything with fun facts and quizzes!")
        es.setAlignment(Qt.AlignmentFlag.AlignCenter); es.setWordWrap(True)
        es.setStyleSheet("font-size: 15px; color: #999; border: none; line-height: 1.6;")
        el.addWidget(es)
        self.cl.addWidget(self.empty_frame)
        self.cl.addStretch()

    def set_topic(self, topic):
        self.topic_input.setText(topic); self.start_learning()

    def start_learning(self):
        q = self.topic_input.text().strip()
        if not q: return
        self.current_content = ""; self._downloaded_pixmaps = []
        self.empty_frame.hide(); self.result_frame.hide(); self.search_frame.hide()
        self.loading_frame.show(); self.loading_text.setText("🤖 AI Teacher is preparing your lesson...")
        self.topic_input.setEnabled(False)

        # Get images from DuckDuckGo
        self.loading_text.setText("🔍 Finding cool images...")
        imgs = self.agent.get_topic_images(q)
        if imgs:
            self.downloader = ImageDownloader(imgs)
            self.downloader.image_downloaded.connect(self.on_img)
            self.downloader.start()

        # Start LLM streaming
        self.worker = ContentWorker(self.agent, self.grade, self.subject, q, q, mode="initial")
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_img(self, data):
        if not hasattr(self, '_downloaded_pixmaps'): self._downloaded_pixmaps = []
        d = data.get("data"); px = QPixmap(); px.loadFromData(d)
        if not px.isNull(): self._downloaded_pixmaps.append({"pixmap": px, "title": data.get("title", "")})

    def on_progress(self, chunk):
        self.current_content += chunk
        if not self.result_frame.isVisible():
            self.loading_frame.hide(); self.result_frame.show(); self.build_content()
        self.update_llm()

    def build_content(self):
        self._clear(self.ril)
        topic = self.topic_input.text().strip()

        # TOPIC HEADER
        th = QFrame()
        th.setStyleSheet(f"QFrame {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {ModernStyles.ACCENT_BLUE}, stop:1 {ModernStyles.ACCENT_PURPLE}); border-radius: 18px; }}")
        thl = QHBoxLayout(th); thl.setContentsMargins(20, 15, 20, 15)
        emoji = "📚"
        for k, e in {"math": "📐", "science": "🔬", "history": "🏛️", "geography": "🌍", "english": "📖", "computer": "💻"}.items():
            if k in self.subject.lower(): emoji = e; break
        tt = QLabel(f"{emoji} {topic}")
        tt.setStyleSheet("font-size: 26px; font-weight: bold; color: white; border: none;")
        thl.addWidget(tt)
        self.ril.addWidget(th)

        # FUN FACTS
        facts = [
            f"Learning about {topic} makes your brain stronger! 💪",
            f"Did you know? {topic} is used in everyday life more than you think! 🌟",
            f"Exploring {topic} opens up a whole new world of knowledge! 🌍"
        ]
        ff = QFrame()
        ff.setStyleSheet(f"QFrame {{ background-color: {ModernStyles.BG_YELLOW_SOFT}; border: 3px solid {ModernStyles.PRIMARY_YELLOW}; border-radius: 18px; }}")
        fl = QVBoxLayout(ff); fl.setContentsMargins(18, 15, 18, 15)
        ft = QLabel("🌟 Fun Facts!")
        ft.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {ModernStyles.TEXT_DARK}; border: none;")
        fl.addWidget(ft)
        for i, f in enumerate(facts):
            fl.addWidget(FunFactCard(f, emoji=["✨", "🌟", "💡"][i % 3]))
        self.ril.addWidget(ff)

        # IMAGE GALLERY
        self.gf = QFrame()
        self.gf.setStyleSheet(f"QFrame {{ background-color: white; border: 3px solid {ModernStyles.ACCENT_TEAL}; border-radius: 18px; }}")
        gl = QVBoxLayout(self.gf); gl.setContentsMargins(18, 15, 18, 15)
        gt = QLabel("🖼️ Visual Explorer")
        gt.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {ModernStyles.ACCENT_TEAL}; border: none;")
        gl.addWidget(gt)
        self.gs = QScrollArea(); self.gs.setWidgetResizable(True); self.gs.setFixedHeight(200)
        self.gs.setStyleSheet("border: none; background: transparent;")
        self.gi = QWidget(); self.gil = QHBoxLayout(self.gi); self.gil.setSpacing(12)
        self.gil.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.gil.addWidget(QLabel("🔍 Loading images..."))
        self.gs.setWidget(self.gi); gl.addWidget(self.gs)
        self.ril.addWidget(self.gf)

        # LLM CONTENT
        lc = QFrame()
        lc.setStyleSheet(f"QFrame {{ background-color: white; border: 3px solid {ModernStyles.ACCENT_PURPLE}; border-radius: 18px; }}")
        ll = QVBoxLayout(lc); ll.setContentsMargins(18, 15, 18, 15)
        lt = QLabel("🤖 AI Teacher Explains")
        lt.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {ModernStyles.ACCENT_PURPLE}; border: none;")
        ll.addWidget(lt)
        self.ca = QTextBrowser(); self.ca.setOpenExternalLinks(True)
        self.ca.setStyleSheet("QTextBrowser { background-color: transparent; border: none; font-size: 16px; line-height: 1.7; padding: 5px; }")
        self.ca.setMinimumHeight(400); ll.addWidget(self.ca)
        self.ril.addWidget(lc)

        # KNOW MORE
        self.mb = QPushButton("🧠 Know More / Go Deeper 🚀")
        self.mb.setCursor(Qt.CursorShape.PointingHandCursor); self.mb.setMinimumHeight(60)
        self.mb.setStyleSheet(ModernStyles.get_button_style("purple"))
        self.mb.clicked.connect(self.load_more); self.mb.hide()
        self.ril.addWidget(self.mb)

        # QUIZ
        self.qf = QFrame(); self.qf.hide()
        self.qf.setStyleSheet(f"QFrame {{ background-color: {ModernStyles.BG_GREEN_SOFT}; border: 3px solid {ModernStyles.SECONDARY_GREEN}; border-radius: 18px; }}")
        ql = QVBoxLayout(self.qf); ql.setContentsMargins(18, 15, 18, 15)
        qt = QLabel("🎯 Quick Quiz!")
        qt.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {ModernStyles.SECONDARY_GREEN}; border: none;")
        ql.addWidget(qt)
        self.qc = QVBoxLayout(); ql.addLayout(self.qc)
        self.ril.addWidget(self.qf)

    def update_llm(self):
        if hasattr(self, 'ca') and self.current_content:
            html = self.render_md(self.current_content)
            self.ca.setHtml(html)
            sb = self.ca.verticalScrollBar(); sb.setValue(sb.maximum())

    def on_finished(self):
        self.loading_frame.hide(); self.topic_input.setEnabled(True)
        if hasattr(self, 'mb'): self.mb.show()
        self.update_gallery(); self.fetch_quiz()

    def update_gallery(self):
        self._clear(self.gil)
        if hasattr(self, '_downloaded_pixmaps') and self._downloaded_pixmaps:
            for d in self._downloaded_pixmaps[:6]:
                self.gil.addWidget(ImageGalleryCard(d["pixmap"], d["title"]))
        else:
            l = QLabel("📷 No images found"); l.setStyleSheet("font-size: 13px; color: #AAA;")
            self.gil.addWidget(l)
        self.gil.addStretch()

    def fetch_quiz(self):
        try:
            qs = self.enricher.get_kids_quiz(self.topic_input.text().strip(), self.subject)
            if qs:
                self.qf.show(); self._clear(self.qc)
                for i, q in enumerate(qs[:3]):
                    self.qc.addWidget(QuizCard(q, i))
        except Exception as e:
            print(f"Quiz error: {e}")

    def load_more(self):
        q = self.topic_input.text().strip()
        self.loading_frame.show(); self.loading_text.setText("🤔 Thinking deeper...")
        self.mb.setEnabled(False); self.mb.setText("⏳ Thinking...")
        self.current_content += "\n\n---\n\n"
        self.worker = ContentWorker(self.agent, self.grade, self.subject, q, q, mode="more", previous_content=self.current_content)
        self.worker.progress.connect(self.on_progress); self.worker.finished.connect(self.on_more)
        self.worker.start()

    def on_more(self):
        self.loading_frame.hide(); self.mb.setEnabled(True); self.mb.setText("🧠 Know More / Go Deeper 🚀")

    def render_md(self, text):
        try:
            html = markdown.markdown(text, extensions=['fenced_code', 'tables'])
            style = f"""
            <style>
                body {{ font-family: 'Segoe UI', 'Comic Sans MS', sans-serif; color: {ModernStyles.TEXT_DARK}; font-size: 16px; line-height: 1.8; padding: 10px; }}
                h1 {{ color: {ModernStyles.ACCENT_BLUE}; border-bottom: 4px solid {ModernStyles.PRIMARY_YELLOW}; padding-bottom: 12px; font-size: 28px; }}
                h2 {{ color: {ModernStyles.ACCENT_PURPLE}; background-color: {ModernStyles.BG_PURPLE_SOFT}; padding: 12px 18px; border-radius: 14px; font-size: 22px; }}
                h3 {{ color: {ModernStyles.ACCENT_TEAL}; font-size: 18px; }}
                p {{ margin-bottom: 14px; line-height: 1.8; }}
                ul, ol {{ margin-bottom: 14px; padding-left: 25px; }}
                li {{ margin-bottom: 8px; }}
                code {{ background-color: {ModernStyles.BG_YELLOW_SOFT}; padding: 3px 10px; border-radius: 8px; color: {ModernStyles.ACCENT_PINK}; font-family: monospace; font-weight: bold; border: 1px solid {ModernStyles.PRIMARY_YELLOW}; }}
                pre {{ background-color: #2D3436; color: #F5F5F5; padding: 18px; border-radius: 14px; border: 3px solid {ModernStyles.PRIMARY_YELLOW}; }}
                blockquote {{ border-left: 6px solid {ModernStyles.PRIMARY_ORANGE}; background-color: {ModernStyles.BG_YELLOW_SOFT}; padding: 14px 22px; margin: 20px 0; border-radius: 0 14px 14px 0; font-style: italic; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 2px solid {ModernStyles.PRIMARY_YELLOW}; padding: 12px 16px; }}
                th {{ background-color: {ModernStyles.ACCENT_BLUE}; color: white; }}
                tr:nth-child(even) {{ background-color: {ModernStyles.BG_BLUE_SOFT}; }}
                a {{ color: {ModernStyles.ACCENT_BLUE}; font-weight: bold; }}
                hr {{ border: 2px dashed {ModernStyles.PRIMARY_YELLOW}; margin: 25px 0; }}
                strong {{ color: {ModernStyles.ACCENT_PINK}; }}
            </style>"""
            return style + html
        except:
            return text.replace("\n", "<br>")

    def _clear(self, layout):
        while layout.count():
            c = layout.takeAt(0)
            if c.widget(): c.widget().deleteLater()
            elif c.layout(): self._clear(c.layout())

    def on_back(self):
        self.back_signal.emit(); self.close()
