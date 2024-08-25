"""Este modulo contiene la clase principal de la aplicacion Shop."""

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
    """
    A class representing the main window of the Shop application.
    Methods:
    - __init__: Initializes the main window.
    - __eliminar: Deletes a category from the database.
    - __agregar: Adds a new category to the database.
    - __modificar: Modifies an existing category in the database.
    - __load_data: Loads data from the database and populates the table.
    - __init_components: Initializes the components of the main window.
    - __on_table_clicked: Handles the event when a row in the table is clicked.
    - __limpiar_valores: Clears the values of the input fields.
    - start: Shows the main window.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shop")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.__init_components()

        # Widgets
        self.container = None

    def __init_components(self):
        q = QLabel("Menu Principal")
        self.layout.addWidget(q)

        button = QPushButton("Categorias")
        button.clicked.connect(self.__show_categorias)
        self.layout.addWidget(button)

        button = QPushButton("Marcas")
        button.clicked.connect(self.__show_marcas)
        self.layout.addWidget(button)

        button = QPushButton("Sizes")
        button.clicked.connect(self.__show_sizes)
        self.layout.addWidget(button)

        button = QPushButton("Ventas")
        # button.clicked.connect(self.__show_ventas)
        self.layout.addWidget(button)

        button = QPushButton("Inventario")
        button.clicked.connect(self.__show_productos)
        self.layout.addWidget(button)

    def __show_productos(self):

        self.__show_widget(WidgetInventario)

    def __show_categorias(self):

        self.__show_widget(WidgetCategoria)

    def __show_marcas(self):

        self.__show_widget(WidgetMarca)

    def __show_sizes(self):

        self.__show_widget(WidgetSize)

    def __show_widget(self,  widget):
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
