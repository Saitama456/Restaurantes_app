# clientes_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import requests  

class ClientesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Cliente")
        self.setGeometry(100, 100, 300, 250)

        layout = QVBoxLayout()
        self.nombre = QLineEdit()
        self.email = QLineEdit()
        self.telefono = QLineEdit()

        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.nombre)
        layout.addWidget(QLabel("Correo Electrónico:"))
        layout.addWidget(self.email)
        layout.addWidget(QLabel("Teléfono:"))
        layout.addWidget(self.telefono)

        btn_guardar = QPushButton("Guardar Cliente")
        btn_guardar.clicked.connect(self.guardar_cliente)
        layout.addWidget(btn_guardar)

        self.setLayout(layout)

    def guardar_cliente(self):  
        datos = {
            "nombre": self.nombre.text(),
            "correo": self.email.text(),
            "telefono": self.telefono.text()
        }

        try:
            response = requests.post("http://localhost:8000/api/clientes/", json=datos)
            if response.status_code == 201:
                QMessageBox.information(self, "Éxito", "Cliente registrado correctamente.")
            else:
                QMessageBox.warning(self, "Error", f"No se pudo registrar el cliente.\n{response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error de conexión", str(e))
