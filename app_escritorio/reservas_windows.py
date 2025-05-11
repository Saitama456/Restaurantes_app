# reservas_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import requests

class ReservasWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Reserva")
        self.setGeometry(100, 100, 300, 300)

        layout = QVBoxLayout()
        self.id_cliente = QLineEdit()
        self.id_mesa = QLineEdit()
        self.fecha = QLineEdit()
        self.hora = QLineEdit()
        self.num_personas = QLineEdit()
        self.estado = QLineEdit()

        layout.addWidget(QLabel("ID del Cliente:"))
        layout.addWidget(self.id_cliente)
        layout.addWidget(QLabel("ID de Mesa:"))
        layout.addWidget(self.id_mesa)
        layout.addWidget(QLabel("Fecha (YYYY-MM-DD):"))
        layout.addWidget(self.fecha)
        layout.addWidget(QLabel("Hora (HH:MM):"))
        layout.addWidget(self.hora)
        layout.addWidget(QLabel("Número de Personas:"))
        layout.addWidget(self.num_personas)
        layout.addWidget(QLabel("Estado (confirmada/cancelada):"))
        layout.addWidget(self.estado)

        btn_guardar = QPushButton("Guardar Reserva")
        btn_guardar.clicked.connect(self.guardar_reserva)
        layout.addWidget(btn_guardar)

        self.setLayout(layout)

    def guardar_reserva(self):
        datos = {
            "cliente": int(self.id_cliente.text()),
            "mesa": int(self.id_mesa.text()),
            "fecha": self.fecha.text(),
            "hora": self.hora.text(),
            "numero_personas": int(self.num_personas.text()),
            "estado": self.estado.text().lower()
        }

        try:
            response = requests.post("http://localhost:8000/api/reservas/", json=datos)
            if response.status_code == 201:
                QMessageBox.information(self, "Éxito", "Reserva guardada correctamente.")
                self.close()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo guardar la reserva.\n{response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error de conexión", str(e))
 
