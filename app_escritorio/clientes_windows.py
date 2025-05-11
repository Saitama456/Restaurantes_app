# clientes_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import sqlite3

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
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Rubrica_clientes (nombre, correo_electronico, telefono) VALUES (?, ?, ?)",
                       (self.nombre.text(), self.email.text(), self.telefono.text()))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Éxito", "Cliente guardado correctamente.")
        self.close()
