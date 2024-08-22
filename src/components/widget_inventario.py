from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QTableWidget,
)

from src.db.service_inventario import get_all_ropa
from src.db.model import Marca
from src.db.model import Size
from src.db.model import Categoria
from src.components.widget_table import TableModel

class WidgetInventario(QWidget):
    def __init__(self, ) -> None:
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setWindowTitle("Inventario")
        self.__init_components()
        self.__load_data()


    def __init_components(self):
        label = QLabel("Inventario")
        self.layout.addWidget(label)

        # Combobox of Marca
        self.combo = QComboBox()

        marcas = Marca.select().where(Marca.eliminado == False)
        self.combo.addItems([marca.nombre for marca in marcas])
        select = QLabel("Seleccionar Marca:")
        self.layout.addWidget(select)
        self.layout.addWidget(self.combo)

        # Combobox of Categoria
        self.combo_categoria = QComboBox()
        categorias = Categoria.select().where(Categoria.eliminado == False)

        self.combo_categoria.addItems([categoria.nombre for categoria in categorias])
        select = QLabel("Seleccionar Categoria:")
        self.layout.addWidget(select)
        self.layout.addWidget(self.combo_categoria)

        # Combobox of Ropa
        self.combo_size = QComboBox()
        sizes = Size.select().where(Size.eliminado == False)
        self.combo_size.addItems([size.nombre for size in sizes])
        select = QLabel("Seleccionar ropa:")
        self.layout.addWidget(select)
        self.layout.addWidget(self.combo_size)

        button = QPushButton("Realizar venta")
        self.layout.addWidget(button)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

    def __load_data(self):

        ropas = get_all_ropa()
        headers = ["ID", "Nombre"]
        values = ["id", "nombre"]
        # tablemodel = TableModel(ropas, headers, values)
        # self.table.setModel(tablemodel)