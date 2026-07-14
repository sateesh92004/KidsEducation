#!/usr/bin/env python3
"""
Debug script to test Image Downloading and Rendering in PyQt6
"""
import sys
import os
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtGui import QPixmap

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.image_search_service import ImageSearchService

class ImageDebugWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Debugger")
        self.resize(600, 400)
        self.layout = QVBoxLayout(self)
        self.status_label = QLabel("Initializing...")
        self.layout.addWidget(self.status_label)
        
        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self.on_download_finished)
        
        # Start search
        QTimer.singleShot(100, self.start_search)
        
    def start_search(self):
        self.status_label.setText("Searching for 'Human Heart'...")
        service = ImageSearchService()
        results = service.search_images("Human Heart")
        
        if not results:
            self.status_label.setText("❌ No search results found!")
            return
            
        self.status_label.setText(f"✅ Found {len(results)} images. Downloading first one...")
        
        first_image = results[0]
        url = first_image.get('thumbnail_url') or first_image.get('image_url')
        print(f"Downloading URL: {url}")
        
        # Test with requests first
        import requests
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
            print(f"Requests Lib Status: {r.status_code}, Size: {len(r.content)}")
        except Exception as e:
            print(f"Requests Lib Error: {e}")

        req = QNetworkRequest(QUrl(url))
        req.setRawHeader(b"User-Agent", b"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36")
        req.setAttribute(QNetworkRequest.Attribute.FollowRedirectsAttribute, True)
        
        self.current_reply = self.nam.get(req)
        self.current_reply.sslErrors.connect(self.on_ssl_errors)
        
    def on_ssl_errors(self, errors):
        print(f"⚠️ SSL Errors: {[e.errorString() for e in errors]}")
        self.sender().ignoreSslErrors()
        
    def on_download_finished(self, reply):
        url = reply.request().url().toString()
        if reply.error():
            err = reply.errorString()
            print(f"❌ Download Error: {err}")
            self.status_label.setText(f"❌ Download Error: {err}")
            reply.deleteLater()
            return
            
        data = reply.readAll()
        print(f"✅ Downloaded {len(data)} bytes")
        
        pixmap = QPixmap()
        if pixmap.loadFromData(data):
            self.status_label.setText(f"✅ Success! Image loaded ({pixmap.width()}x{pixmap.height()})")
            lbl = QLabel()
            lbl.setPixmap(pixmap)
            self.layout.addWidget(lbl)
        else:
            print("❌ Failed to load pixmap from data")
            self.status_label.setText("❌ Failed to load pixmap (invalid data?)")
            
        reply.deleteLater()
        QTimer.singleShot(1000, QApplication.quit)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageDebugWindow()
    # window.show() # Don't need to show in headless
    QTimer.singleShot(5000, QApplication.quit) # Safety timeout
    sys.exit(app.exec())
