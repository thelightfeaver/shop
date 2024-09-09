from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox


class CustomDialog(QDialog):
    def __init__(self, title: str, message: str):
        super().__init__()

        self.setWindowTitle(title)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel(f"{message}")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
