import sys
import os
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineScript
from PyQt6.QtGui import QIcon, QImage, QPixmap
import urllib.request

from src.settings_dialog import SettingsDialog
from src.plugin_manager import PluginManager
from src.browser_settings import BrowserSettings
from src.api_manager import ApiManager

def download_websim_logo():
    """Download the websim.ai logo if it doesn't exist"""
    logo_path = os.path.join("assets", "websim_logo.png")
    
    # If logo already exists, return it
    if os.path.exists(logo_path):
        return logo_path
        
    try:
        # Create assets directory if it doesn't exist
        os.makedirs("assets", exist_ok=True)
        
        # Try multiple potential logo URLs
        logo_urls = [
            "https://websim.ai/favicon.ico",
            "https://websim.ai/favicon.png",
            "https://websim.ai/logo.png"
        ]
        
        for url in logo_urls:
            try:
                urllib.request.urlretrieve(url, logo_path)
                if os.path.exists(logo_path) and os.path.getsize(logo_path) > 0:
                    return logo_path
            except:
                continue
                
        # If no logo could be downloaded, use a default icon
        return None
    except Exception as e:
        print(f"Could not set up logo: {str(e)}")
        return None

class WebSimBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WebSim.ai Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Show initial alert
        QMessageBox.information(self, "Welcome", 
            "Welcome to WebSim Browser!\n\n"
            "This application is still in development.\n"
            "Some features may not work as expected.")

        # Set application icon
        logo_path = download_websim_logo()
        if logo_path is not None and os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))

        # Flag to track initial load
        self.initial_load = True

        # Setup persistent storage for cookies and cache
        BrowserSettings.setup_persistent_storage(self)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create web view with persistent profile first
        self.web_view = QWebEngineView()
        
        # Create page with enhanced settings
        page = QWebEnginePage(self.profile, self.web_view)
        BrowserSettings.setup_page_settings(page)
        self.web_view.setPage(page)
        
        # Connect to loadFinished signal for auto-reload
        page.loadFinished.connect(self.on_load_finished)
        
        self.web_view.setUrl(QUrl("https://websim.ai"))

        # Create button layouts
        top_button_layout = QHBoxLayout()
        bottom_button_layout = QHBoxLayout()
        
        # First row of buttons
        # Create Home button
        self.home_button = QPushButton("🏠 Home")
        self.home_button.clicked.connect(self.go_home)
        self.style_button(self.home_button, "#2196F3")
        top_button_layout.addWidget(self.home_button)

        # Create Reload button
        self.reload_button = QPushButton("🔄 Reload")
        self.reload_button.clicked.connect(self.web_view.reload)
        self.style_button(self.reload_button, "#607D8B")
        top_button_layout.addWidget(self.reload_button)

        # Create Settings button
        self.settings_button = QPushButton("⚙️ Settings")
        self.settings_button.clicked.connect(self.show_settings)
        self.style_button(self.settings_button, "#795548")
        top_button_layout.addWidget(self.settings_button)

        # Create Clear Cache button
        self.clear_button = QPushButton("🧹 Clear Cache")
        self.clear_button.clicked.connect(self.clear_cache)
        self.style_button(self.clear_button, "#9E9E9E")
        top_button_layout.addWidget(self.clear_button)

        # Add stretch to separate button groups
        top_button_layout.addStretch()

        # Second row of buttons
        # Create Plugin button
        self.plugin_button = QPushButton("🔌 Plugins")
        self.plugin_button.clicked.connect(self.show_plugins_menu)
        self.style_button(self.plugin_button, "#9C27B0")
        bottom_button_layout.addWidget(self.plugin_button)

        # Create API Features button
        self.api_button = QPushButton("🛠️ API Features")
        self.api_button.clicked.connect(self.show_api_menu)
        self.style_button(self.api_button, "#FF5722")
        bottom_button_layout.addWidget(self.api_button)
        
        # Add stretch to push buttons to the left
        bottom_button_layout.addStretch()
        
        # Add button layouts to main layout
        main_layout.addLayout(top_button_layout)
        main_layout.addLayout(bottom_button_layout)
        main_layout.addWidget(self.web_view)

        # Remove window frame margins
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Initialize managers
        self.plugin_manager = PluginManager(self)
        self.api_manager = ApiManager(self)

    def style_button(self, button, color):
        """Apply consistent styling to buttons"""
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {color}DD;
            }}
        """)

    def go_home(self):
        """Navigate to WebSim home page"""
        self.web_view.setUrl(QUrl("https://websim.ai"))

    def show_settings(self):
        """Show the settings dialog"""
        dialog = SettingsDialog(self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            # Apply settings
            settings = self.profile.settings()
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled,
                               dialog.js_checkbox.isChecked())
            self.profile.setHttpCacheMaximumSize(dialog.cache_size.value() * 1024 * 1024)

    def clear_cache(self):
        """Clear browser cache and cookies"""
        reply = self.question("Clear Cache",
                            "Are you sure you want to clear all browsing data?")
        if reply:
            self.profile.clearHttpCache()
            self.profile.clearAllVisitedLinks()
            self.information("Success", "Cache cleared successfully!")

    def show_plugins_menu(self):
        """Show the plugins dropdown menu"""
        self.plugin_manager.menu.exec(self.plugin_button.mapToGlobal(
            self.plugin_button.rect().bottomLeft()
        ))

    def show_api_menu(self):
        """Show the API features menu"""
        self.api_manager.menu.exec(self.api_button.mapToGlobal(
            self.api_button.rect().bottomLeft()
        ))

    def on_load_finished(self, ok):
        """Handle page load completion"""
        if ok:
            # Check for plugin in URL
            current_url = self.web_view.url().toString()
            if "plugin=@Trey6383/test123" in current_url:
                script = """
                function injectPlugin() {
                    // Create a div element
                    const div = document.createElement('div');
                    div.style.position = 'fixed';
                    div.style.bottom = '20px';
                    div.style.right = '20px';
                    div.style.backgroundColor = '#9C27B0';
                    div.style.color = 'white';
                    div.style.padding = '10px';
                    div.style.borderRadius = '5px';
                    div.style.zIndex = '9999';
                    div.style.fontFamily = 'Arial, sans-serif';
                    div.textContent = 'Plugin: test123 by @Trey6383';
                    
                    // Add div to the page
                    document.body.appendChild(div);
                    
                    // Fade out after 3 seconds
                    setTimeout(() => {
                        div.style.transition = 'opacity 1s';
                        div.style.opacity = '0';
                        setTimeout(() => div.remove(), 1000);
                    }, 3000);
                }
                injectPlugin();
                """
                self.web_view.page().runJavaScript(script)
            
            # Handle initial load
            if self.initial_load:
                QTimer.singleShot(1000, self.reload_once)

    def reload_once(self):
        """Perform one-time reload and reset the flag"""
        self.web_view.reload()
        self.initial_load = False

    def question(self, title, message):
        """Show a question dialog"""
        from PyQt6.QtWidgets import QMessageBox
        return QMessageBox.question(self, title, message,
                                  QMessageBox.StandardButton.Yes | 
                                  QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes

    def information(self, title, message):
        """Show an information dialog"""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, title, message)

def main():
    app = QApplication(sys.argv)
    
    # Set application-wide icon if logo is available
    logo_path = download_websim_logo()
    if logo_path is not None and os.path.exists(logo_path):
        app.setWindowIcon(QIcon(logo_path))
    
    browser = WebSimBrowser()
    browser.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 