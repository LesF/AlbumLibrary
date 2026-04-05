from qt.core import QWidget, QVBoxLayout, QLabel

class ConfigWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.label = QLabel('Album Library Configuration')
        self.layout.addWidget(self.label)

    def save_settings(self):
        # We'll implement settings persistence later
        pass
