from pprint import pprint

from src.db.service_ventas import get_sell_by_month, get_sell_total, get_count_sell_by_ropa

import matplotlib.pyplot as plt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class WidgetGraph(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setWindowTitle("Gráfico")
        self.setGeometry(100, 100, 800, 600)
        self._init_components()

    def _init_components(self):

        # Total de ventas
        total = get_sell_total()
        self.label_total = QLabel("Total Vendido: ")
        self.layout.addWidget(self.label_total)
        self.total_ventas = QLabel(f"${total:,.2f}")
        self.total_ventas.setStyleSheet("font-size: 24px")
        self.layout.addWidget(self.total_ventas)

        # Grafica ventas por mes
        ventas = get_sell_by_month()
        # Crear la figura de matplotlib
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        # Datos 
        meses = [venta["mes"] for venta in ventas]
        cantidades = [venta["cantidad"] for venta in ventas]
        # Crear el gráfico de barras
        self.ax.bar(meses, cantidades)
        self.ax.set_title("Ventas por Mes")
        self.ax.set_xlabel("Mes")
        self.ax.set_ylabel("Cantidad")
        # Actualizar el canvas
        self.canvas.draw()

        # Grafica ventas por ropa
        ventas_ropa = get_count_sell_by_ropa()

        # Crear la figura de matplotlib
        self.figure_ropa, self.ax_ropa = plt.subplots()
        self.canvas_ropa = FigureCanvas(self.figure_ropa)

        self.layout.addWidget(self.canvas_ropa)

        # Datos
        nombres = [venta["nombre"] for venta in ventas_ropa]
        cantidades = [venta["cantidad"] for venta in ventas_ropa]

        # Crear el gráfico de barras
        self.ax_ropa.bar(nombres, cantidades)
        self.ax_ropa.set_title("Ventas por Ropa")
        self.ax_ropa.set_xlabel("Ropa")
        self.ax_ropa.set_ylabel("Cantidad")
        # Actualizar el canvas
        self.canvas_ropa.draw()
