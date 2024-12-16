class DatabaseHandler:
    @staticmethod
    def extract_project_id(url):
        """Extract project ID from URL (not needed for test message)"""
        return None

    @staticmethod
    def get_injection_script(project_id=None):
        """Return a simple script that injects test message"""
        return """
        function injectDatabaseFunctionality() {
            // Create a div element
            const div = document.createElement('div');
            div.style.position = 'fixed';
            div.style.bottom = '20px';
            div.style.right = '20px';
            div.style.backgroundColor = '#4CAF50';
            div.style.color = 'white';
            div.style.padding = '10px';
            div.style.borderRadius = '5px';
            div.style.zIndex = '9999';
            div.style.fontFamily = 'Arial, sans-serif';
            div.textContent = 'test123 by @Trey6383';
            
            // Add div to the page
            document.body.appendChild(div);
            
            // Fade out after 3 seconds
            setTimeout(() => {
                div.style.transition = 'opacity 1s';
                div.style.opacity = '0';
                setTimeout(() => div.remove(), 1000);
            }, 3000);
        }
        """