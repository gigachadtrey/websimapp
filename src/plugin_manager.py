from PyQt6.QtWidgets import QMenu, QInputDialog, QMessageBox
from PyQt6.QtCore import QUrl

class PluginManager:
    def __init__(self, browser):
        self.browser = browser
        self.menu = QMenu(browser)
        self.setup_menu()

    def setup_menu(self):
        """Setup the plugins dropdown menu"""
        self.menu.clear()
        
        # Add preset plugins
        self.menu.addAction("@Trey6383/test123", 
                          lambda: self.apply_preset_plugin("@Trey6383/test123"))
        self.menu.addAction("@Trey6383/injectify", 
                          lambda: self.apply_preset_plugin("@Trey6383/injectify"))
        self.menu.addAction("@hintbl0ck/edit5", 
                          lambda: self.apply_preset_plugin("@hintbl0ck/edit5"))
        self.menu.addAction("@Trey6383/edit6-real", 
                          lambda: self.apply_preset_plugin("@Trey6383/edit6-real"))
        self.menu.addSeparator()
        self.menu.addAction("New Plugin...", self.add_plugin)

    def add_plugin(self):
        """Handle adding a custom plugin"""
        # Get current URL
        current_url = self.browser.web_view.url().toString()
        
        # Remove any existing plugin parameter
        if "?plugin=" in current_url:
            current_url = current_url.split("?plugin=")[0]
        
        # Get plugin creator username
        username, ok = QInputDialog.getText(self.browser, 
            "Plugin Creator", 
            "Who made the plugin? Enter their websim username with the @:")
        if not ok or not username:
            return
        
        # Ensure username starts with @
        if not username.startswith("@"):
            username = "@" + username
        
        # Get plugin name
        plugin_name, ok = QInputDialog.getText(self.browser, 
            "Plugin Name", 
            "What's the name of the plugin?")
        if not ok or not plugin_name:
            return
        
        # Construct plugin URL
        plugin_param = f"?plugin={username}/{plugin_name}"
        new_url = current_url + plugin_param
        
        # Navigate to the new URL
        self.browser.web_view.setUrl(QUrl(new_url))
        
        # Show confirmation
        QMessageBox.information(self.browser, 
            "Plugin Added", 
            f"Plugin {username}/{plugin_name} has been added to the current page.")

    def apply_preset_plugin(self, plugin_id):
        """Apply a preset plugin to the current page"""
        current_url = self.browser.web_view.url().toString()
        
        # Remove any existing plugin parameter
        if "?plugin=" in current_url:
            current_url = current_url.split("?plugin=")[0]
        
        # Add the new plugin
        new_url = current_url + f"?plugin={plugin_id}"
        self.browser.web_view.setUrl(QUrl(new_url)) 