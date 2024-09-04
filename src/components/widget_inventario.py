from datetime import datetime as dt

from src.db.service_inventario import get_all_ropa
from src.db.model import Marca, Ropa
from src.db.model import Size
from src.db.model import Categoria
from src.components.widget_table import TableModel

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
    QTableWidget,
    QMessageBox,
)


class WidgetInventario(QWidget):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.var_id = None
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
        self.combo_marca = QComboBox()

        marcas = Marca.select().where(Marca.eliminado == False)
        self.combo_marca.addItems([marca.nombre for marca in marcas])
        select = QLabel("Seleccionar Marca:")
        self.layout.addWidget(select)
        self.layout.addWidget(self.combo_marca)

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
        select = QLabel("Size:")
        self.layout.addWidget(select)
        self.layout.addWidget(self.combo_size)

        # Qlabel precio
        label_precio = QLabel("Precio:")
        self.q_precio = QLineEdit()
        self.layout.addWidget(label_precio)
        self.layout.addWidget(self.q_precio)

        # Qlabel cantidad
        label_cantidad = QLabel("Cantidad:")
        self.q_cantidad = QLineEdit()
        self.layout.addWidget(label_cantidad)
        self.layout.addWidget(self.q_cantidad)

        # Qpushbutton agregar
        button = QPushButton("Agregar", clicked=self.__agregar)
        self.layout_buttons.addWidget(button)

        # Qpushbutton eliminar
        button = QPushButton("Eliminar", clicked=self.__eliminar)
        self.layout_buttons.addWidget(button)

        # Qpushbutton Modificar
        button = QPushButton("Modificar", clicked=self.__modificar)
        self.layout_buttons.addWidget(button)
        self.layout.addLayout(self.layout_buttons)

        # qtableview inventario
        self.table = QTableView()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.clicked.connect(self.__on_table_clicked)
        self.layout.addWidget(self.table)

    def __agregar(self):
        marca = Marca.get(Marca.nombre == self.combo_marca.currentText())
        categoria = Categoria.get(
            Categoria.nombre == self.combo_categoria.currentText()
        )
        size = Size.get(Size.nombre == self.combo_size.currentText())
        cantidad = int(self.q_cantidad.text())
        precio = float(self.q_precio.text())
        ropa = Ropa.create(
            precio=precio,
            categoria=categoria.id,
            size=size.id,
            marca=marca.id,
            cantidad=cantidad,
            fecha=dt.now(),
        )
        ropa.save()
        self.__load_data()
        self.__limpiar_valores()

        QMessageBox.information(self, "Aviso", "Inventario agregado!")

    def __load_data(self):

        ropas = get_all_ropa()
        headers = ["ID", "Marca", "Categoria", "Size", "Precio", "Cantidad", "Fecha"]
        values = [
            "id",
            ["marca", "nombre"],
            ["categoria", "nombre"],
            ["size", "nombre"],
            "precio",
            "cantidad",
            "fecha",
        ]
        model = TableModel(ropas, headers=headers, values=values)
        self.table.setModel(model)

    def __eliminar(self):
        selected_row = self.table.selectionModel().selectedRows()

        if selected_row:
            ropa = Ropa.get(id=self.var_id)
            ropa.eliminado = True
            ropa.save()

            self.__load_data()
            self.__limpiar_valores()

            QMessageBox.information(self, "Aviso", "Inventario eliminado!")
        else:
            QMessageBox.critical(self, "Error", "Seleccione una marca para eliminar")

    def __modificar(self):
        selected_row = self.table.selectionModel().selectedRows()
        if selected_row:
            ropa = Ropa.get(id=self.var_id)
            marca = Marca.get(Marca.nombre == self.combo_marca.currentText())
            categoria = Categoria.get(
                Categoria.nombre == self.combo_categoria.currentText()
            )
            size = Size.get(Size.nombre == self.combo_size.currentText())
            cantidad = int(self.q_cantidad.text())
            precio = float(self.q_precio.text())

            ropa.marca = marca.id
            ropa.categoria = categoria.id
            ropa.size = size.id
            ropa.cantidad = cantidad
            ropa.precio = precio
            ropa.save()

            self.__load_data()
            self.__limpiar_valores()

            QMessageBox.information(self, "Aviso", "Inventario modificado")
        else:
            QMessageBox.critical(self, "Error", "Seleccione una marca para modificar")

    def __on_table_clicked(self):
        selected_row = self.table.selectionModel().selectedRows()
        if selected_row:
            index = selected_row[0]
            self.var_id = index.sibling(index.row(), 0).data()
            self.combo_marca.setCurrentText(index.sibling(index.row(), 1).data())
            self.combo_categoria.setCurrentText(index.sibling(index.row(), 2).data())
            self.combo_size.setCurrentText(index.sibling(index.row(), 3).data())
            self.q_precio.setText(str(index.sibling(index.row(), 4).data()))
            self.q_cantidad.setText(str(index.sibling(index.row(), 5).data()))

    def __limpiar_valores(self):
        self.var_id = None
        self.q_cantidad.clear()
        self.q_precio.clear()
        self.combo_marca.setCurrentIndex(0)
        self.combo_categoria.setCurrentIndex(0)
        self.combo_size.setCurrentIndex(0)
