from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                           QPushButton, QLabel, QCheckBox, QSpinBox,
                           QMessageBox)

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