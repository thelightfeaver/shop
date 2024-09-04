from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableView,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QInputDialog,
    QComboBox,
)

from src.db.service_inventario import get_all_ropa, get_ropa_by_id
from src.components.widget_table import TableModel
from src.db.model import Venta


class Producto:
    def __init__(self, id, nombre, precio, cantidad):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def __str__(self):
        return f"{self.id} - {self.nombre} - ${self.precio} - {self.cantidad}"


class WidgetVenta(QWidget):

    def __init__(self):
        super().__init__()
        self.precio_total = 0
        self.data = []
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setWindowTitle("Ventas")
        self.setGeometry(100, 100, 800, 600)
        self._init_components()
        self._cargar_datos()

    def _init_components(self):
        self.lbl_total = QLabel(f"Total: ${self.precio_total}")
        self.lbl_total.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.lbl_total)
        lbl_ventas = QLabel("Ropas:")
        self.layout.addWidget(lbl_ventas)

        self.combo_ropas = QComboBox()
        self.layout.addWidget(self.combo_ropas)
        ropas = get_all_ropa()
        for ropa in ropas:
            self.combo_ropas.addItem(
                f"{ropa.id} - {ropa.categoria.nombre} - {ropa.marca.nombre} - {ropa.size.nombre}"
            )

        lbl_cantidad = QLabel("Cantidad:")
        self.layout.addWidget(lbl_cantidad)
        self.q_cantidad = QLineEdit()
        self.layout.addWidget(self.q_cantidad)

        self.btn_agregar = QPushButton("Agregar")
        self.btn_agregar.clicked.connect(self.agregar_articulo)
        self.layout.addWidget(self.btn_agregar)

        self.btn_facturar = QPushButton("Facturar")
        self.btn_facturar.clicked.connect(self.facturar_compra)
        self.layout.addWidget(self.btn_facturar)

        self.table = QTableView()
        self.layout.addWidget(self.table)

    def agregar_articulo(self):
        try:
            id = self.combo_ropas.currentText().split(" - ")[0].strip()
            cantidad = int(self.q_cantidad.text())
            ropa = get_ropa_by_id(id)[0]
            precio = ropa.precio
            nombre = (
                f"{ropa.categoria.nombre} - {ropa.marca.nombre} - {ropa.size.nombre}"
            )

            if cantidad:
                self.data.append(Producto(id, nombre, precio, cantidad))
                self._cargar_datos()
                self._actualizar_total()
                self._limpiar_datos()

        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Error", "Error al agregar articulo")

    def _limpiar_datos(self):
        self.q_cantidad.setText("")
        self.combo_ropas.setCurrentIndex(0)

    def _actualizar_total(self):

        total = sum([producto.precio * producto.cantidad for producto in self.data])
        if total:

            self.precio_total = total
            self.lbl_total.setText(f"Total: ${self.precio_total}")

    def facturar_compra(self):
        for producto in self.data:
            Venta.create(
                ropa=producto.id,
                fecha=datetime.now(),
                cantidad=producto.cantidad,
                precio=producto.precio,
                descuento=0,
                precio_final=producto.precio * producto.cantidad,
                dinero_pagado=self.precio_total,
            )
        self._limpiar_datos()

    def _cargar_datos(self):
        headers = ["Id", "Nombre", "Precio", "Cantidad"]
        values = ["id", "nombre", "precio", "cantidad"]
        self.data = []
        model = TableModel(data=self.data, headers=headers, values=values)
        self.table.setModel(model)

    def _on_table_click(self):
        selected_row = self.table.selectionModel().selectedRows()
        if selected_row:
            index = selected_row[0]
