# reservas_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import sqlite3

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

        layout.addWidget(QLabel("Nombre del Cliente:"))
        layout.addWidget(self.id_cliente)
        layout.addWidget(QLabel(" Mesa:"))
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
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Rubrica_reservas 
            (id_cliente, id_mesa, fecha, hora, numero_personas, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            self.id_cliente.text(),
            self.id_mesa.text(),
            self.fecha.text(),
            self.hora.text(),
            self.num_personas.text(),
            self.estado.text()
        ))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Éxito", "Reserva guardada correctamente.")
        self.close()
