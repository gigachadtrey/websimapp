import sys
import os
from PyQt6.QtCore import QUrl, QStandardPaths
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QHBoxLayout, QInputDialog, QMessageBox,
                           QMenu, QDialog, QLabel, QCheckBox, QSpinBox)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import (QWebEngineScript, QWebEngineProfile, 
                                  QWebEnginePage, QWebEngineSettings,
                                  QWebEngineUrlRequestInterceptor)
from PyQt6.QtGui import QIcon, QAction

class ChromeRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, chrome_version):
        super().__init__()
        self.chrome_version = chrome_version
        
    def interceptRequest(self, info):
        # Add Chrome-specific headers
        info.setHttpHeader(
            b"sec-ch-ua",
            f'"Not_A Brand";v="8", "Chromium";v="{self.chrome_version}", "Google Chrome";v="{self.chrome_version}"'.encode()
        )
        info.setHttpHeader(b"sec-ch-ua-mobile", b"?0")
        info.setHttpHeader(b"sec-ch-ua-platform", b'"Windows"')

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 300, 200)
        
        layout = QVBoxLayout()
        
        # JavaScript toggle
        self.js_checkbox = QCheckBox("Enable JavaScript")
        self.js_checkbox.setChecked(True)
        layout.addWidget(self.js_checkbox)
        
        # Cache size setting
        cache_layout = QHBoxLayout()
        cache_layout.addWidget(QLabel("Cache Size (MB):"))
        self.cache_size = QSpinBox()
        self.cache_size.setRange(50, 1000)
        self.cache_size.setValue(100)
        cache_layout.addWidget(self.cache_size)
        layout.addLayout(cache_layout)
        
        # Clear data button
        clear_data_btn = QPushButton("Clear Browsing Data")
        clear_data_btn.clicked.connect(self.clear_data)
        layout.addWidget(clear_data_btn)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def clear_data(self):
        profile = self.parent().profile
        profile.clearHttpCache()
        profile.clearAllVisitedLinks()
        QMessageBox.information(self, "Success", "Browsing data cleared!")

class WebSimBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WebSim.ai Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Flag to track initial load
        self.initial_load = True

        # Setup persistent storage for cookies and cache
        self.setup_persistent_storage()

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create web view with persistent profile first
        self.web_view = QWebEngineView()
        
        # Create page with enhanced settings
        page = QWebEnginePage(self.profile, self.web_view)
        self.setup_page_settings(page)
        self.web_view.setPage(page)
        
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
        # Create Database button
        self.database_button = QPushButton("💾 Database")
        self.database_button.clicked.connect(self.inject_database_functionality)
        self.style_button(self.database_button, "#4CAF50")
        bottom_button_layout.addWidget(self.database_button)

        # Create Add Plugin button
        self.plugin_button = QPushButton("🔌 Plugins")
        self.plugin_button.clicked.connect(self.show_plugins_menu)
        self.style_button(self.plugin_button, "#9C27B0")
        bottom_button_layout.addWidget(self.plugin_button)
        
        # Add stretch to push buttons to the left
        bottom_button_layout.addStretch()
        
        # Add button layouts to main layout
        main_layout.addLayout(top_button_layout)
        main_layout.addLayout(bottom_button_layout)
        main_layout.addWidget(self.web_view)

        # Remove window frame margins
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Initialize the injection script
        self.setup_injection_script()

        # Create plugins menu
        self.plugins_menu = QMenu(self)
        self.setup_plugins_menu()

    def setup_plugins_menu(self):
        """Setup the plugins dropdown menu"""
        self.plugins_menu.clear()
        
        # Add preset plugins
        self.plugins_menu.addAction("@Trey6383/injectify", 
                                  lambda: self.apply_preset_plugin("@Trey6383/injectify"))
        self.plugins_menu.addAction("@hintbl0ck/edit5", 
                                  lambda: self.apply_preset_plugin("@hintbl0ck/edit5"))
        self.plugins_menu.addAction("@Trey6383/edit6-real", 
                                  lambda: self.apply_preset_plugin("@Trey6383/edit6-real"))
        self.plugins_menu.addSeparator()
        self.plugins_menu.addAction("New Plugin...", self.add_plugin)

    def show_plugins_menu(self):
        """Show the plugins dropdown menu"""
        # Show menu at the plugin button's position
        self.plugins_menu.exec(self.plugin_button.mapToGlobal(
            self.plugin_button.rect().bottomLeft()
        ))

    def show_settings(self):
        """Show the settings dialog"""
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Apply settings
            settings = self.profile.settings()
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled,
                               dialog.js_checkbox.isChecked())
            self.profile.setHttpCacheMaximumSize(dialog.cache_size.value() * 1024 * 1024)

    def clear_cache(self):
        """Clear browser cache and cookies"""
        reply = QMessageBox.question(self, "Clear Cache",
                                   "Are you sure you want to clear all browsing data?",
                                   QMessageBox.StandardButton.Yes | 
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.profile.clearHttpCache()
            self.profile.clearAllVisitedLinks()
            QMessageBox.information(self, "Success", "Cache cleared successfully!")

    def setup_page_settings(self, page):
        """Configure page settings for better compatibility"""
        settings = page.settings()
        
        # Security and privacy settings
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FocusOnNavigationEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowGeolocationOnInsecureOrigins, False)  # Require HTTPS for geolocation
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False)  # Require HTTPS
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, True)  # Security feature
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanPaste, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebRTCPublicInterfacesOnly, True)  # Privacy feature
        settings.setAttribute(QWebEngineSettings.WebAttribute.ErrorPageEnabled, True)
        
        # Set default fonts to match Chrome
        settings.setFontFamily(QWebEngineSettings.FontFamily.StandardFont, "Segoe UI")
        settings.setFontFamily(QWebEngineSettings.FontFamily.SansSerifFont, "Segoe UI")
        settings.setFontFamily(QWebEngineSettings.FontFamily.SerifFont, "Times New Roman")
        settings.setFontFamily(QWebEngineSettings.FontFamily.FixedFont, "Consolas")
        
        # Set font sizes
        settings.setFontSize(QWebEngineSettings.FontSize.DefaultFontSize, 16)
        settings.setFontSize(QWebEngineSettings.FontSize.DefaultFixedFontSize, 13)
        settings.setFontSize(QWebEngineSettings.FontSize.MinimumFontSize, 0)
        settings.setFontSize(QWebEngineSettings.FontSize.MinimumLogicalFontSize, 6)
        
        # Connect to loadFinished signal for auto-reload
        page.loadFinished.connect(self.on_load_finished)

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

    def add_plugin(self):
        """Handle adding a custom plugin"""
        # Get current URL
        current_url = self.web_view.url().toString()
        
        # Remove any existing plugin parameter
        if "?plugin=" in current_url:
            current_url = current_url.split("?plugin=")[0]
        
        # Get plugin creator username
        username, ok = QInputDialog.getText(self, 
            "Plugin Creator", 
            "Who made the plugin? Enter their websim username with the @:")
        if not ok or not username:
            return
        
        # Ensure username starts with @
        if not username.startswith("@"):
            username = "@" + username
        
        # Get plugin name
        plugin_name, ok = QInputDialog.getText(self, 
            "Plugin Name", 
            "What's the name of the plugin?")
        if not ok or not plugin_name:
            return
        
        # Construct plugin URL
        plugin_param = f"?plugin={username}/{plugin_name}"
        new_url = current_url + plugin_param
        
        # Navigate to the new URL
        self.web_view.setUrl(QUrl(new_url))
        
        # Show confirmation
        QMessageBox.information(self, 
            "Plugin Added", 
            f"Plugin {username}/{plugin_name} has been added to the current page.")

    def apply_preset_plugin(self, plugin_id):
        """Apply a preset plugin to the current page"""
        current_url = self.web_view.url().toString()
        
        # Remove any existing plugin parameter
        if "?plugin=" in current_url:
            current_url = current_url.split("?plugin=")[0]
        
        # Add the new plugin
        new_url = current_url + f"?plugin={plugin_id}"
        self.web_view.setUrl(QUrl(new_url))

    def setup_persistent_storage(self):
        # Create persistent profile in AppData Local with custom name
        storage_path = os.path.join(
            os.path.expandvars("%LOCALAPPDATA%"),
            'WebSimBrowser'
        )
        
        # Print storage path for debugging
        print(f"Storage path: {storage_path}")
        
        # Ensure the directory exists
        os.makedirs(storage_path, exist_ok=True)
        
        # Create persistent profile with enhanced settings
        self.profile = QWebEngineProfile('WebSimProfile', None)
        
        # Set storage paths
        self.profile.setPersistentStoragePath(storage_path)
        cookies_path = os.path.join(storage_path, 'cookies')
        os.makedirs(cookies_path, exist_ok=True)
        
        # Enable cache with specific paths
        cache_path = os.path.join(storage_path, 'cache')
        os.makedirs(cache_path, exist_ok=True)
        self.profile.setCachePath(cache_path)
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        self.profile.setHttpCacheMaximumSize(100 * 1024 * 1024)  # 100MB cache
        
        # Configure security settings
        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        
        # Set modern Chrome user agent with full security features
        chrome_version = "120.0.0.0"
        webkit_version = "537.36"
        self.profile.setHttpUserAgent(
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{webkit_version} "
            f"(KHTML, like Gecko) Chrome/{chrome_version} Safari/{webkit_version} "
            f"Chromium/{chrome_version}"
        )
        
        # Set language and encoding
        self.profile.setHttpAcceptLanguage("en-US,en;q=0.9")
        
        # Create and set the request interceptor
        interceptor = ChromeRequestInterceptor(chrome_version)
        self.profile.setUrlRequestInterceptor(interceptor)
        
        # Enhanced cookie settings for better persistence
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        
        # Don't clear existing data on startup
        # self.profile.clearHttpCache()
        # self.profile.clearAllVisitedLinks()

    def setup_injection_script(self):
        """Initialize the database injection script"""
        self.injection_script = QWebEngineScript()
        self.injection_script.setName("databaseFunctionality")
        self.injection_script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        self.web_view.page().scripts().insert(self.injection_script)

    def inject_database_functionality(self):
        """Inject database functionality that integrates with websim.ai"""
        current_url = self.web_view.url().toString()
        
        # Get the current project ID from the URL if available
        project_id = ""
        if "/project/" in current_url:
            project_id = current_url.split("/project/")[-1].split("/")[0]
        
        script_content = """
        function injectDatabaseFunctionality() {
            // Get the current project context
            let projectId = '%s';
            if (!projectId) {
                projectId = document.querySelector('[data-project-id]')?.dataset.projectId;
            }
            
            // Get the current websim origin
            let baseUrl = window.location.origin;
            
            // Create database window
            let dbWindow = window.open(
                baseUrl + '/database' + (projectId ? '?project=' + projectId : ''),
                'WebSimDatabase',
                'width=800,height=800,resizable=yes,scrollbars=yes,status=yes'
            );
            
            // Add window features
            if (dbWindow) {
                // Inject custom styles and functionality
                dbWindow.addEventListener('DOMContentLoaded', function() {
                    // Add custom styles
                    const style = dbWindow.document.createElement('style');
                    style.textContent = `
                        body { font-family: 'Segoe UI', sans-serif; }
                        .websim-db-header {
                            background: #4CAF50;
                            color: white;
                            padding: 10px;
                            position: sticky;
                            top: 0;
                            z-index: 1000;
                        }
                        .websim-db-content {
                            padding: 20px;
                        }
                        .websim-db-button {
                            background: #4CAF50;
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 4px;
                            cursor: pointer;
                            margin: 5px;
                        }
                        .websim-db-button:hover {
                            background: #45a049;
                        }
                    `;
                    dbWindow.document.head.appendChild(style);
                    
                    // Add header
                    const header = dbWindow.document.createElement('div');
                    header.className = 'websim-db-header';
                    header.innerHTML = `
                        <h2>WebSim Database</h2>
                        <div>Project ID: ${projectId || 'None'}</div>
                    `;
                    dbWindow.document.body.insertBefore(header, dbWindow.document.body.firstChild);
                    
                    // Add functionality to sync with main window
                    const syncButton = dbWindow.document.createElement('button');
                    syncButton.className = 'websim-db-button';
                    syncButton.textContent = 'Sync with Project';
                    syncButton.onclick = function() {
                        // Refresh the database content
                        dbWindow.location.reload();
                    };
                    header.appendChild(syncButton);
                });
            }
        }
        """ % project_id
        
        self.web_view.page().runJavaScript(script_content + "\ninjectDatabaseFunctionality();")

    def on_load_finished(self, ok):
        """Handle page load completion"""
        if ok and self.initial_load:
            # Only reload once on initial launch
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(1000, self.reload_once)

    def reload_once(self):
        """Perform one-time reload and reset the flag"""
        self.web_view.reload()
        self.initial_load = False

def main():
    app = QApplication(sys.argv)
    browser = WebSimBrowser()
    browser.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 