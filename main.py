"""Este modulo contiene la clase principal de la aplicacion Shop."""

from src.components.widget_venta import WidgetVenta
from src.components.widget_marca import WidgetMarca
from src.components.widget_size import WidgetSize
from src.components.widget_inventario import WidgetInventario

from src.components.widget_categoria import WidgetCategoria
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)


class Windows(QMainWindow):
    """Clase principal de la aplicacion"""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shop")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self._init_components()

        # Widgets
        self.container = None

    def _init_components(self):
        q = QLabel("Menu Principal")
        self.layout.addWidget(q)

        button = QPushButton("Categorias")
        button.clicked.connect(self._show_categorias)
        self.layout.addWidget(button)

        button = QPushButton("Marcas")
        button.clicked.connect(self._show_marcas)
        self.layout.addWidget(button)

        button = QPushButton("Sizes")
        button.clicked.connect(self._show_sizes)
        self.layout.addWidget(button)

        button = QPushButton("Ventas")
        button.clicked.connect(self._show_ventas)
        self.layout.addWidget(button)

        button = QPushButton("Inventario")
        button.clicked.connect(self._show_productos)
        self.layout.addWidget(button)

    def _show_ventas(self):
            
        self._show_widget(WidgetVenta)
                               
    def _show_productos(self):

        self._show_widget(WidgetInventario)

    def _show_categorias(self):

        self._show_widget(WidgetCategoria)

    def _show_marcas(self):

        self._show_widget(WidgetMarca)

    def _show_sizes(self):

        self._show_widget(WidgetSize)

    def _show_widget(self,  widget):
        try:
           
            if self.container is None or not self.container.isVisible():
                self.container = widget()
                self.container.show()
            else:
                self.container.close()
                self.container = None

        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication([])
    w = Windows()
    w.show()
    app.exec()
