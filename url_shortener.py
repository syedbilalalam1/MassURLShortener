import sys
import os
import json
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QComboBox, QTextEdit, QFileDialog, QMessageBox,
                            QDialog, QFormLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
from dotenv import load_dotenv, set_key

class APISettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("API Settings")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Add help text at the top
        help_text = QLabel(
            "Enter your API keys below. Click the Help button to learn how to obtain them."
        )
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(help_text)
        
        form_layout = QFormLayout()
        
        # API Key inputs with help buttons
        self.cuty_key = QLineEdit(self)
        self.ouo_key = QLineEdit(self)
        self.shrinkme_key = QLineEdit(self)
        
        # Create help buttons for each service
        cuty_help = QPushButton("?")
        cuty_help.setFixedSize(25, 25)
        cuty_help.clicked.connect(lambda: self.show_help("cuty.io"))
        
        ouo_help = QPushButton("?")
        ouo_help.setFixedSize(25, 25)
        ouo_help.clicked.connect(lambda: self.show_help("ouo.io"))
        
        shrinkme_help = QPushButton("?")
        shrinkme_help.setFixedSize(25, 25)
        shrinkme_help.clicked.connect(lambda: self.show_help("shrinkme.io"))
        
        # Load existing values
        self.cuty_key.setText(os.getenv('CUTY_API_KEY', ''))
        self.ouo_key.setText(os.getenv('OUO_API_KEY', ''))
        self.shrinkme_key.setText(os.getenv('SHRINKME_API_KEY', ''))
        
        # Create horizontal layouts for each input with help button
        cuty_layout = QHBoxLayout()
        cuty_layout.addWidget(self.cuty_key)
        cuty_layout.addWidget(cuty_help)
        
        ouo_layout = QHBoxLayout()
        ouo_layout.addWidget(self.ouo_key)
        ouo_layout.addWidget(ouo_help)
        
        shrinkme_layout = QHBoxLayout()
        shrinkme_layout.addWidget(self.shrinkme_key)
        shrinkme_layout.addWidget(shrinkme_help)
        
        form_layout.addRow("Cuty.io API Key:", cuty_layout)
        form_layout.addRow("Ouo.io API Key:", ouo_layout)
        form_layout.addRow("Shrinkme.io API Key:", shrinkme_layout)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
    
    def show_help(self, service):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle(f"How to get {service} API Key")
        help_dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(help_dialog)
        
        help_text = QLabel()
        help_text.setWordWrap(True)
        help_text.setOpenExternalLinks(True)
        
        if service == "cuty.io":
            help_text.setText(
                "To get your Cuty.io API key:\n\n"
                "1. Go to <a href='https://cuty.io/'>https://cuty.io/</a>\n"
                "2. Sign up for an account if you haven't already\n"
                "3. Log in to your account\n"
                "4. Go to your dashboard\n"
                "5. Look for the 'API' or 'Developer' section\n"
                "6. Copy your API key"
            )
        elif service == "ouo.io":
            help_text.setText(
                "To get your Ouo.io API key:\n\n"
                "1. Go to <a href='https://ouo.io/'>https://ouo.io/</a>\n"
                "2. Create an account if you haven't already\n"
                "3. Log in to your account\n"
                "4. Navigate to your dashboard\n"
                "5. Find the 'API Token' section\n"
                "6. Copy your API token"
            )
        elif service == "shrinkme.io":
            help_text.setText(
                "To get your Shrinkme.io API key:\n\n"
                "1. Go to <a href='https://shrinkme.io/'>https://shrinkme.io/</a>\n"
                "2. Register for an account if you don't have one\n"
                "3. Log in to your account\n"
                "4. Go to your dashboard\n"
                "5. Look for the 'API' or 'Developer' section\n"
                "6. Copy your API token"
            )
        
        layout.addWidget(help_text)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(help_dialog.accept)
        layout.addWidget(close_btn)
        
        help_dialog.exec()
    
    def save_settings(self):
        # Get the .env file path
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
        
        # Create .env file and directory if they don't exist
        os.makedirs(os.path.dirname(env_path), exist_ok=True)
        if not os.path.exists(env_path):
            with open(env_path, 'w') as f:
                f.write("# URL Shortener API Keys\n")
        
        try:
            # Update .env file
            set_key(env_path, 'CUTY_API_KEY', self.cuty_key.text())
            set_key(env_path, 'OUO_API_KEY', self.ouo_key.text())
            set_key(env_path, 'SHRINKME_API_KEY', self.shrinkme_key.text())
            
            # Reload environment variables
            load_dotenv(override=True)
            
            self.accept()
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Failed to save API keys: {str(e)}\nPlease check file permissions."
            )

class URLShortenerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("URL Shortener")
        self.setMinimumSize(700, 500)
        
        # Load environment variables
        load_dotenv()
        
        # Set the window background color
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QLabel {
                color: #1a1a1a;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """)
        
        self.init_ui()
        
        # Check if API keys are set
        if not all([os.getenv('CUTY_API_KEY'), os.getenv('OUO_API_KEY'), os.getenv('SHRINKME_API_KEY')]):
            QMessageBox.information(self, "API Keys Required", 
                                  "Please set up your API keys in the Settings dialog.")
            self.show_settings_dialog()
    
    def init_ui(self):
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add credit at the top
        credit_label = QLabel("Made by syedbilalalam")
        credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credit_font = QFont()
        credit_font.setPointSize(12)
        credit_font.setBold(True)
        credit_label.setFont(credit_font)
        credit_label.setStyleSheet("color: #4a90e2; margin-bottom: 10px;")
        layout.addWidget(credit_label)
        
        # Settings button at top right
        settings_layout = QHBoxLayout()
        settings_layout.addStretch()
        settings_btn = QPushButton("Settings")
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.clicked.connect(self.show_settings_dialog)
        settings_layout.addWidget(settings_btn)
        layout.addLayout(settings_layout)
        
        # Service selection
        service_layout = QHBoxLayout()
        service_label = QLabel("Select Service:")
        service_label.setFixedWidth(100)
        self.service_combo = QComboBox()
        self.service_combo.addItems(["cuty.io", "ouo.io", "shrinkme.io"])
        service_layout.addWidget(service_label)
        service_layout.addWidget(self.service_combo)
        layout.addLayout(service_layout)
        
        # URL input
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL to shorten")
        shorten_btn = QPushButton("Shorten")
        shorten_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        shorten_btn.clicked.connect(self.shorten_url)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(shorten_btn)
        layout.addLayout(url_layout)
        
        # File handling
        file_layout = QHBoxLayout()
        self.file_btn = QPushButton("Upload URLs File")
        self.file_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.file_btn.clicked.connect(self.upload_file)
        file_layout.addWidget(self.file_btn)
        file_layout.addStretch()
        layout.addLayout(file_layout)
        
        # Results area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setPlaceholderText("Shortened URLs will appear here...")
        self.results_text.setMinimumHeight(200)
        layout.addWidget(self.results_text)
        
        # Buttons layout at bottom
        buttons_layout = QHBoxLayout()
        
        # Copy results button
        self.copy_btn = QPushButton("Copy Results")
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.clicked.connect(self.copy_results)
        
        # Download button
        self.download_btn = QPushButton("Download Shortened URLs")
        self.download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_btn.clicked.connect(self.download_results)
        
        buttons_layout.addWidget(self.copy_btn)
        buttons_layout.addWidget(self.download_btn)
        layout.addLayout(buttons_layout)
    
    def show_settings_dialog(self):
        dialog = APISettingsDialog(self)
        if dialog.exec():
            QMessageBox.information(self, "Success", "API settings saved successfully!")
    
    def check_api_key(self, service):
        key_map = {
            "cuty.io": "CUTY_API_KEY",
            "ouo.io": "OUO_API_KEY",
            "shrinkme.io": "SHRINKME_API_KEY"
        }
        
        api_key = os.getenv(key_map[service])
        if not api_key:
            QMessageBox.warning(self, "API Key Required", 
                              f"Please set up your {service} API key in Settings first.")
            self.show_settings_dialog()
            return None
        return api_key
    
    def shorten_url(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL")
            return
            
        service = self.service_combo.currentText()
        api_key = self.check_api_key(service)
        if not api_key:
            return
            
        shortened = None
        if service == "cuty.io":
            shortened = self.shorten_cuty(url, api_key)
        elif service == "ouo.io":
            shortened = self.shorten_ouo(url, api_key)
        elif service == "shrinkme.io":
            shortened = self.shorten_shrinkme(url, api_key)
            
        if shortened:
            self.results_text.append(f"Original: {url}\nShortened: {shortened}\n")
            self.url_input.clear()
    
    def shorten_cuty(self, url, api_key):
        api_url = f"https://cuty.io/api"
        params = {
            "api": api_key,
            "url": url
        }
        
        try:
            response = requests.get(api_url, params=params)
            data = response.json()
            
            if data["status"] == "success":
                return data["shortenedUrl"]
            else:
                QMessageBox.warning(self, "Error", data["message"])
                return None
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to shorten URL: {str(e)}")
            return None
            
    def shorten_ouo(self, url, api_key):
        api_url = f"http://ouo.io/api/{api_key}={url}"
        
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.text.strip()
            else:
                QMessageBox.warning(self, "Error", f"Failed to shorten URL. Status code: {response.status_code}")
                return None
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to shorten URL: {str(e)}")
            return None
            
    def shorten_shrinkme(self, url, api_key):
        api_url = "https://shrinkme.io/api"
        params = {
            "api": api_key,
            "url": url
        }
        
        try:
            response = requests.get(api_url, params=params)
            data = response.json()
            
            if data["status"] == "success":
                return data["shortenedUrl"]
            else:
                QMessageBox.warning(self, "Error", data.get("message", "Unknown error occurred"))
                return None
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to shorten URL: {str(e)}")
            return None
    
    def upload_file(self):
        if not any([os.getenv('CUTY_API_KEY'), os.getenv('OUO_API_KEY'), os.getenv('SHRINKME_API_KEY')]):
            QMessageBox.warning(self, "API Key Required", "Please set up your API keys in Settings first.")
            self.show_settings_dialog()
            return
            
        file_name, _ = QFileDialog.getOpenFileName(self, "Open URLs File", "", "Text Files (*.txt)")
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    urls = file.readlines()
                    service = self.service_combo.currentText()
                    api_key = self.check_api_key(service)
                    if not api_key:
                        return
                    
                    for url in urls:
                        url = url.strip()
                        if url:
                            shortened = None
                            if service == "cuty.io":
                                shortened = self.shorten_cuty(url, api_key)
                            elif service == "ouo.io":
                                shortened = self.shorten_ouo(url, api_key)
                            elif service == "shrinkme.io":
                                shortened = self.shorten_shrinkme(url, api_key)
                                
                            if shortened:
                                self.results_text.append(f"Original: {url}\nShortened: {shortened}\n")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to process file: {str(e)}")
    
    def copy_results(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.results_text.toPlainText())
        QMessageBox.information(self, "Success", "Results copied to clipboard!")
        
    def download_results(self):
        if not self.results_text.toPlainText():
            QMessageBox.warning(self, "Error", "No results to download!")
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Shortened URLs",
            "shortened_urls.txt",
            "Text Files (*.txt)"
        )
        
        if file_name:
            try:
                # Extract only shortened URLs from the results
                content = self.results_text.toPlainText()
                shortened_urls = []
                for line in content.split('\n'):
                    if line.startswith('Shortened:'):
                        # Extract just the URL part after "Shortened: "
                        shortened_urls.append(line.replace('Shortened:', '').strip())
                
                # Write only the shortened URLs to file
                with open(file_name, 'w') as file:
                    file.write('\n'.join(shortened_urls))
                QMessageBox.information(self, "Success", "Shortened URLs saved successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save results: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = URLShortenerApp()
    window.show()
    sys.exit(app.exec()) 