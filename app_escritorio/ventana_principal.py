# ventana_principal.py
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from clientes_windows import ClientesWindow
from reservas_windows import ReservasWindow

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel del Administrador")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        btn_clientes = QPushButton("Clientes")
        btn_reservas = QPushButton("Reservas")

        btn_clientes.clicked.connect(self.abrir_clientes)
        btn_reservas.clicked.connect(self.abrir_reservas)

        layout.addWidget(btn_clientes)
        layout.addWidget(btn_reservas)

        self.setLayout(layout)

    def abrir_clientes(self):
        self.clientes_window = ClientesWindow()
        self.clientes_window.show()

    def abrir_reservas(self):
        self.reservas_window = ReservasWindow()
        self.reservas_window.show()
