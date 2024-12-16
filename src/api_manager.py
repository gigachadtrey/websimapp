from PyQt6.QtWidgets import QMenu, QPushButton, QHBoxLayout, QMessageBox, QInputDialog
from PyQt6.QtCore import QUrl
import os

class ApiManager:
    def __init__(self, browser):
        self.browser = browser
        self.menu = QMenu(browser)
        self.setup_menu()

    def setup_menu(self):
        """Setup the API features menu"""
        self.menu.clear()
        
        # Project Management
        self.menu.addAction("📂 My Projects", self.open_my_projects)
        self.menu.addAction("🔍 Search Projects", self.search_projects)
        self.menu.addSeparator()
        
        # Project Features
        project_menu = self.menu.addMenu("📊 Project Features")
        project_menu.addAction("Analytics", self.open_analytics)
        project_menu.addAction("Settings", self.open_settings)
        project_menu.addAction("Database", lambda: self.toggle_project_feature("enableDatabase"))
        project_menu.addAction("API Access", lambda: self.toggle_project_feature("enableApi"))
        project_menu.addAction("Multiplayer", lambda: self.toggle_project_feature("enableMultiplayer"))
        project_menu.addAction("LLM Features", lambda: self.toggle_project_feature("enableLLM"))
        
        # User Settings
        self.menu.addSeparator()
        settings_menu = self.menu.addMenu("⚙️ Settings")
        settings_menu.addAction("Editor Settings", self.open_editor_settings)
        settings_menu.addAction("Security Settings", self.open_security)
        settings_menu.addAction("Team Management", self.open_team)
        
        # Documentation
        self.menu.addSeparator()
        self.menu.addAction("📚 API Documentation", self.open_api_docs)

    def open_my_projects(self):
        """Open user's projects"""
        self.browser.web_view.setUrl(QUrl("https://websim.ai/projects/me"))

    def search_projects(self):
        """Open projects search"""
        self.browser.web_view.setUrl(QUrl("https://websim.ai/projects"))

    def open_analytics(self):
        """Open project analytics"""
        current_url = self.browser.web_view.url().toString()
        if "/project/" in current_url:
            project_id = current_url.split("/project/")[1].split("/")[0]
            self.browser.web_view.setUrl(QUrl(f"https://websim.ai/project/{project_id}/analytics"))
        else:
            QMessageBox.information(self.browser, "Info", "Please open a project first to view analytics.")

    def open_settings(self):
        """Open project settings"""
        current_url = self.browser.web_view.url().toString()
        if "/project/" in current_url:
            project_id = current_url.split("/project/")[1].split("/")[0]
            self.browser.web_view.setUrl(QUrl(f"https://websim.ai/project/{project_id}/settings"))
        else:
            QMessageBox.information(self.browser, "Info", "Please open a project first to view settings.")

    def toggle_project_feature(self, feature):
        """Toggle project features like database, API, multiplayer"""
        current_url = self.browser.web_view.url().toString()
        if "/project/" in current_url:
            project_id = current_url.split("/project/")[1].split("/")[0]
            # Execute JavaScript to toggle the feature
            script = f"""
            async function toggleFeature() {{
                const project = await window.websim.getProject('{project_id}');
                if (project && project.lore) {{
                    project.lore['{feature}'] = !project.lore['{feature}'];
                    await window.websim.updateProject(project);
                    return true;
                }}
                return false;
            }}
            toggleFeature();
            """
            self.browser.web_view.page().runJavaScript(script, lambda result: 
                QMessageBox.information(self.browser, "Success", f"Feature {'enabled' if result else 'disabled'}.")
                if result is not None else
                QMessageBox.warning(self.browser, "Error", "Could not toggle feature. Please try again.")
            )
        else:
            QMessageBox.information(self.browser, "Info", "Please open a project first to modify features.")

    def open_editor_settings(self):
        """Open editor settings"""
        self.browser.web_view.setUrl(QUrl("https://websim.ai/settings/editor"))

    def open_team(self):
        """Open team management"""
        self.browser.web_view.setUrl(QUrl("https://websim.ai/team"))

    def open_security(self):
        """Open security settings"""
        self.browser.web_view.setUrl(QUrl("https://websim.ai/settings/security"))

    def open_api_docs(self):
        """Open API documentation"""
        # Try to open local documentation first
        local_docs = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'apidocumentation.html')
        if os.path.exists(local_docs):
            self.browser.web_view.setUrl(QUrl.fromLocalFile(local_docs))
        else:
            # Fallback to online documentation
            self.browser.web_view.setUrl(QUrl("https://websim.ai/docs/api")) 