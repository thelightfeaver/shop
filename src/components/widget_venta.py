from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QTableWidget,
    QComboBox,
)

from src.db.service_inventario import get_all_ropa, get_ropa_by_id, update_canitdad_ropa
from src.db.model import Venta
from src.components.widget_table import TableModel
from src.components.custom_dialog import CustomDialog


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
        self.index = None
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setWindowTitle("Ventas")
        self.setGeometry(100, 100, 800, 600)
        self._init_components()
        self._cargar_datos()

    def _init_components(self):
        # Label Total
        self.lbl_total = QLabel(f"Total: ${self.precio_total}")
        self.lbl_total.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.lbl_total)

        # label ropas
        lbl_ventas = QLabel("Ropas:")
        self.layout.addWidget(lbl_ventas)

        # Combo Ropas
        self.combo_ropas = QComboBox()
        self.combo_ropas.currentIndexChanged.connect(self._on_combo_change)

        # Cargar ropas
        ropas = get_all_ropa()
        for ropa in ropas:
            self.combo_ropas.addItem(
                f"{ropa.id} - {ropa.categoria.nombre} - {ropa.marca.nombre} - {ropa.size.nombre}"
            )

        # buscar precio y mostrarlo
        id = self.combo_ropas.currentText().split(" - ")[0].strip()
        ropa = get_ropa_by_id(id)[0]

        # Label Precio
        self.q_precio = QLabel(f"Precio: ${ropa.precio}")
        self.price_layout = QHBoxLayout()
        self.price_layout.addWidget(self.combo_ropas)
        self.price_layout.addWidget(self.q_precio)
        self.layout.addLayout(self.price_layout)

        # Label Cantidad
        lbl_cantidad = QLabel("Cantidad:")
        self.layout.addWidget(lbl_cantidad)

        # Q cantidad
        self.q_cantidad = QLineEdit()
        self.layout.addWidget(self.q_cantidad)

        # Button Agregar
        self.btn_agregar = QPushButton("Agregar")
        self.btn_agregar.clicked.connect(self._agregar_articulo)
        self.layout.addWidget(self.btn_agregar)

        # Button Facturar
        self.btn_facturar = QPushButton("Facturar")
        self.btn_facturar.clicked.connect(self._facturar_compra)
        self.layout.addWidget(self.btn_facturar)

        # Table ventas
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.clicked.connect(self._on_table_click)
        self.layout.addWidget(self.table)

        # button borrar
        self.btn_borrar = QPushButton("Borrar")
        self.btn_borrar.setStyleSheet("background-color: red; color: white;")
        self.btn_borrar.clicked.connect(self._delete_data)
        self.layout.addWidget(self.btn_borrar)
        self.btn_borrar.hide()

    def _on_combo_change(self):
        id = self.combo_ropas.currentText().split(" - ")[0].strip()
        ropa = get_ropa_by_id(id)[0]

        if self.q_precio:
            self.q_precio.setText(f"Precio: ${ropa.precio}")

    def _agregar_articulo(self):
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
        else:
            self.precio_total = 0
            self.lbl_total.setText(f"Total: ${self.precio_total}")

    def _facturar_compra(self):

        dls = CustomDialog("Facturar", "¿Desea facturar la compra?")
        if dls.exec() == QMessageBox.Accepted:
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

                update_canitdad_ropa(producto.id, producto.cantidad)

            self._limpiar_datos()
            self._cargar_datos()
            self._actualizar_total()
            self.data = []

    def _cargar_datos(self):
        headers = ["Id", "Nombre", "Precio", "Cantidad"]
        values = ["id", "nombre", "precio", "cantidad"]
        model = TableModel(data=self.data, headers=headers, values=values)
        self.table.setModel(model)

    def _on_table_click(self):
        selected_row = self.table.selectionModel().selectedRows()
        if selected_row:
            self.index = selected_row[0]
            self.btn_borrar.show()

    def _delete_data(self):

        cfm = CustomDialog("Eliminar", "¿Desea eliminar el producto?")
        if cfm.exec() == QMessageBox.Accepted:

            selected_row = self.table.selectionModel().selectedRows()
            if selected_row:

                for data in self.data:
                    if (
                        data.id
                        == selected_row[0].sibling(selected_row[0].row(), 0).data()
                    ):
                        self.data.remove(data)
                        break

                self.btn_borrar.hide()
                self._actualizar_total()
                self._cargar_datos()
        else:
            self.btn_borrar.hide()
