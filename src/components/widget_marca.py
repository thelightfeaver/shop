"""Widget para gestionar marcas"""

from src.db.model import Marca 
from src.components.widget_table import TableModel

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableView, QLabel, QLineEdit, QPushButton, QMessageBox

class WidgetMarca(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setWindowTitle("Marcas")
        self.var_id = None
        self.__init_components()
        self.__load_data()

    def __modificar(self):
        if self.var_id  and self.txt_marca.text() != "":
            marca = Marca.get(id=self.var_id)
            marca.nombre = self.txt_marca.text()
            marca.save()

            QMessageBox.information(self, "Aviso", "Marca modificada")

            self.__load_data()
            self.__limpiar_valores()
        else:
            QMessageBox.critical(self, "Error", "Ingrese un nombre de marca")

    def __eliminar(self):
        selected_row = self.table.selectionModel().selectedRows()
        if selected_row:
            marca = Marca.get(id=self.var_id)
            marca.eliminado = True
            marca.save()

            QMessageBox.information(self, "Aviso", "Marca eliminada")

            self.__load_data()
            self.__limpiar_valores()
        else:
            QMessageBox.critical(
                self, "Error", "Seleccione una marca para eliminar"
            )

    def __agregar(self):
        if self.txt_marca.text() != "":
            marca = Marca.create(nombre=self.txt_marca.text())
            marca.save()

            QMessageBox.information(self, "Aviso", "Marca agregada")

            self.__load_data()
            self.__limpiar_valores()
        else:
            QMessageBox.critical(self, "Error", "Ingrese un nombre de marca")

    def __init_components(self):
        self.txt_marca = QLineEdit()
        self.layout.addWidget(QLabel("Nombre"))
        self.layout.addWidget(self.txt_marca)

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
        marcas = Marca.select().where(Marca.eliminado == False)
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
        self.txt_marca.setText(index.siblingAtColumn(1).data())
        self.var_id = index.siblingAtColumn(0).data()

    def __limpiar_valores(self):
        self.txt_marca.clear()
        self.var_id = None
