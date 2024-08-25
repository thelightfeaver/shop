"""Widget para la gestión de categorías."""

from src.db.model import Categoria
from src.components.widget_table import TableModel

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableView,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)


class WidgetCategoria(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("Categorias")
        self.var_id = None
        self.__init_components()
        self.__load_data()

    def __modificar(self):
        if self.var_id and self.txt_categoria.text() != "":
            categoria = Categoria.get(id=self.var_id)
            categoria.nombre = self.txt_categoria.text()
            categoria.save()

            QMessageBox.information(self, "Aviso", "Categoria modificada")

            self.__load_data()
            self.__limpiar_valores()
        else:
            QMessageBox.critical(self, "Error", "Ingrese un nombre de marca")

    def __eliminar(self):
        selected_row = self.table.selectionModel().selectedRows()
        if selected_row:
            categoria = Categoria.get(id=self.var_id)
            categoria.eliminado = True
            categoria.save()

            QMessageBox.information(self, "Aviso", "Categoria eliminada")

            self.__load_data()
            self.__limpiar_valores()
        else:
            QMessageBox.critical(self, "Error", "Seleccione una marca para eliminar")

    def __agregar(self):
        if self.txt_categoria.text() != "":
            categoria = Categoria.create(nombre=self.txt_categoria.text())
            categoria.save()

            QMessageBox.information(self, "Aviso", "Categoria agregada")

            self.__load_data()
            self.__limpiar_valores()
        else:
            QMessageBox.critical(self, "Error", "Ingrese un nombre de marca")

    def __init_components(self):
        self.txt_categoria = QLineEdit()
        self.layout.addWidget(QLabel("Nombre"))
        self.layout.addWidget(self.txt_categoria)

        agregar_button = QPushButton("Agregar")
        agregar_button.clicked.connect(self.__agregar)
        self.layout.addWidget(agregar_button)

        eliminar_button = QPushButton("Eliminar")
        eliminar_button.clicked.connect(self.__eliminar)
        self.layout.addWidget(eliminar_button)

        modificar_button = QPushButton("Modificar")
        modificar_button.clicked.connect(self.__modificar)
        self.layout.addWidget(modificar_button)

        self.table = QTableView()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.clicked.connect(self.__on_table_clicked)
        self.layout.addWidget(self.table)

    def __load_data(self):
        marcas = Categoria.select().where(Categoria.eliminado == False)
        headers = ["ID", "Nombre"]
        values = ["id", "nombre"]
        model = TableModel(marcas, headers, values)
        self.table.setModel(model)
        self.table.clicked.connect(self.__on_table_clicked)

    def __on_table_clicked(self):
        selected_row = self.table.selectionModel().selectedRows()
        if selected_row:
            index = selected_row[0]
            self.var_id = index.sibling(index.row(), 0).data()
            self.var_marca.setText(index.sibling(index.row(), 1).data())

    def __on_table_clicked(self, index):
        self.txt_categoria.setText(index.siblingAtColumn(1).data())
        self.var_id = index.siblingAtColumn(0).data()

    def __limpiar_valores(self):
        self.txt_categoria.clear()
        self.var_id = None
