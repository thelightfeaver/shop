

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableView,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QComboBox
)

from src.db.service_inventario import get_all_ropa



class WidgetVenta(QWidget):

    def __init__(self) :
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setWindowTitle("Ventas")
        self.setGeometry(100, 100, 800, 600)
        self.__init_components()
        
    


    def __init_components(self):
        lbl_ventas = QLabel("Ropas:")
        self.layout.addWidget(lbl_ventas)

        self.combo_ropas = QComboBox()
        self.layout.addWidget(self.combo_ropas)
        ropas = get_all_ropa()
        for ropa in ropas:
            self.combo_ropas.addItem(f"{ropa.id} - {ropa.categoria.nombre} - {ropa.marca.nombre} - {ropa.size.nombre}")

        # lbl_cantidad = QLabel("Cantidad:")
        # self.layout.addWidget(lbl_cantidad)
        

        # self.btn_vender = QPushButton("Vender")
        # self.layout.addWidget(self.btn_vender)

        # self.table = QTableView()
        # self.layout.addWidget(self.table)
