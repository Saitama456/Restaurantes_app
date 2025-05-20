# mesas_windows.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QListWidget
import requests

class MesasWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mesas")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        # Campos de entrada
        self.capacidad = QLineEdit()
        self.estado = QComboBox()
        self.estado.addItems(["disponible", "ocupada"])

        layout.addWidget(QLabel("Capacidad de la mesa:"))
        layout.addWidget(self.capacidad)
        layout.addWidget(QLabel("Estado:"))
        layout.addWidget(self.estado)

        # Botón para guardar nueva mesa
        btn_guardar = QPushButton("Guardar Mesa")
        btn_guardar.clicked.connect(self.guardar_mesa)
        layout.addWidget(btn_guardar)

        # Lista de mesas existentes
        layout.addWidget(QLabel("Mesas registradas:"))
        self.lista_mesas = QListWidget()
        layout.addWidget(self.lista_mesas)

        self.setLayout(layout)

        # Cargar mesas al abrir la ventana
        self.cargar_mesas()

    def guardar_mesa(self):
        datos = {
            "capacidad": int(self.capacidad.text()),
            "estado": self.estado.currentText()
        }

        try:
            response = requests.post("http://localhost:8000/api/mesas/", json=datos)
            if response.status_code == 201:
                QMessageBox.information(self, "Éxito", "Mesa registrada correctamente.")
                self.capacidad.clear()
                self.cargar_mesas()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo registrar la mesa.\n{response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error de conexión", str(e))

    def cargar_mesas(self):
        self.lista_mesas.clear()
        try:
            response = requests.get("http://localhost:8000/api/mesas/")
            if response.status_code == 200:
                mesas = response.json()
                for mesa in mesas:
                    texto = f"Mesa {mesa['id']} - Capacidad: {mesa['capacidad']} - Estado: {mesa['estado']}"
                    self.lista_mesas.addItem(texto)
            else:
                self.lista_mesas.addItem("Error al cargar las mesas.")
        except Exception as e:
            self.lista_mesas.addItem(f"Error de conexión: {e}")

