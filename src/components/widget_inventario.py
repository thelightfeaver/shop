from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QHBoxLayout,
    QLineEdit,
    QTableView,
    QTableWidget
)

from src.db.service_inventario import get_all_ropa
from src.db.model import Marca, Ropa
from src.db.model import Size
from src.db.model import Categoria
from src.components.widget_table import TableModel

class WidgetInventario(QWidget):
    def __init__(self, ) -> None:
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setWindowTitle("Inventario")
        self.setGeometry(100, 100, 800, 600)
        self.__init_components()
        self.__load_data()

    def __init_components(self):
        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.setAlignment(Qt.AlignTop)
       
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

        precio = QLabel("Precio")
        self.q_precio = QLineEdit()
        self.layout.addWidget(self.q_precio)
        self.layout.addWidget(precio)

        cantidad = QLabel("Cantidad")
        self.q_cantidad = QLineEdit()
        self.layout.addWidget(self.q_cantidad)
        self.layout.addWidget(cantidad)


        button = QPushButton("Agregar", clicked=self.__agregar)
        self.layout_buttons.addWidget(button)
        button = QPushButton("Eliminar")
        self.layout_buttons.addWidget(button)
        button = QPushButton("Modificar")
        self.layout_buttons.addWidget(button)
    
        self.layout.addLayout(self.layout_buttons)

        self.table = QTableView()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.layout.addWidget(self.table)

    def __agregar(self):
        marca = Marca.get(Marca.nombre == self.combo.currentText())
        categoria = Categoria.get(Categoria.nombre == self.combo_categoria.currentText())
        size = Size.get(Size.nombre == self.combo_size.currentText())
        cantidad = int(self.q_cantidad.text())
        precio = float(self.q_precio.text())
        ropa = Ropa.create(precio=precio, categoria=categoria.id, size=size.id, marca=marca.id, cantidad=cantidad)
        ropa.save()
        self.__load_data()
    def __load_data(self):

        ropas = get_all_ropa()
        print(ropas)
        headers = ["ID", "Precio", "Categoria", "Size", "Marca", "Cantidad"]
        values = ["id", "precio", "categoria", "size", "marca", "cantidad"]
        tablemodel = TableModel(ropas, headers, values)
        self.table.setModel(tablemodel)