from PySide6.QtWidgets import QWidget, QVBoxLayout




class WidgetGraph(QWidget):
     

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setWindowTitle("Gráfico")
        self.setGeometry(100, 100, 800, 600)
        self._init_components()

    def _init_components(self):
        pass
       