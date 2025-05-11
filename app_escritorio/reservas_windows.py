from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QListWidget, QListWidgetItem, QHBoxLayout
import requests

class ReservasWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reservas")
        self.setGeometry(100, 100, 400, 500)

        layout = QVBoxLayout()

        # Campos
        self.id_cliente = QLineEdit()
        self.id_mesa = QLineEdit()
        self.fecha = QLineEdit()
        self.hora = QLineEdit()
        self.numero_personas = QLineEdit()
        self.estado = QLineEdit()

        layout.addWidget(QLabel("ID Cliente:"))
        layout.addWidget(self.id_cliente)
        layout.addWidget(QLabel("ID Mesa:"))
        layout.addWidget(self.id_mesa)
        layout.addWidget(QLabel("Fecha (YYYY-MM-DD):"))
        layout.addWidget(self.fecha)
        layout.addWidget(QLabel("Hora (HH:MM):"))
        layout.addWidget(self.hora)
        layout.addWidget(QLabel("Número de personas:"))
        layout.addWidget(self.numero_personas)
        layout.addWidget(QLabel("Estado (confirmada/cancelada):"))
        layout.addWidget(self.estado)

        btn_guardar = QPushButton("Registrar reserva")
        btn_guardar.clicked.connect(self.guardar_reserva)
        layout.addWidget(btn_guardar)

        layout.addWidget(QLabel("Historial de reservas:"))
        self.lista_reservas = QListWidget()
        self.lista_reservas.itemClicked.connect(self.seleccionar_reserva)
        layout.addWidget(self.lista_reservas)

        btns = QHBoxLayout()
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_editar.clicked.connect(self.editar_reserva)
        self.btn_eliminar.clicked.connect(self.eliminar_reserva)
        btns.addWidget(self.btn_editar)
        btns.addWidget(self.btn_eliminar)
        layout.addLayout(btns)

        self.setLayout(layout)
        self.id_reserva_actual = None
        self.cargar_reservas()

    def cargar_reservas(self):
        self.lista_reservas.clear()
        try:
            response = requests.get("http://localhost:8000/api/reservas/")
            if response.status_code == 200:
                reservas = response.json()
                for r in reservas:
                    texto = f"ID {r['id']} - Cliente {r['cliente']} - Mesa {r['mesa']} - {r['fecha']} {r['hora']} ({r['estado']})"
                    item = QListWidgetItem(texto)
                    item.setData(1000, r)
                    self.lista_reservas.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar reservas.\n{e}")

    def seleccionar_reserva(self, item):
        reserva = item.data(1000)
        self.id_reserva_actual = reserva['id']
        self.id_cliente.setText(str(reserva['cliente']))
        self.id_mesa.setText(str(reserva['mesa']))
        self.fecha.setText(reserva['fecha'])
        self.hora.setText(reserva['hora'])
        self.numero_personas.setText(str(reserva['numero_personas']))
        self.estado.setText(reserva['estado'])

    def guardar_reserva(self):
        datos = {
            "cliente": int(self.id_cliente.text()),
            "mesa": int(self.id_mesa.text()),
            "fecha": self.fecha.text(),
            "hora": self.hora.text(),
            "numero_personas": int(self.numero_personas.text()),
            "estado": self.estado.text().lower()
        }
        try:
            response = requests.post("http://localhost:8000/api/reservas/", json=datos)
            if response.status_code == 201:
                QMessageBox.information(self, "Éxito", "Reserva registrada.")
                self.limpiar_campos()
                self.cargar_reservas()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo registrar.\n{response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def editar_reserva(self):
        if not self.id_reserva_actual:
            QMessageBox.warning(self, "Advertencia", "Selecciona una reserva.")
            return
        datos = {
            "cliente": int(self.id_cliente.text()),
            "mesa": int(self.id_mesa.text()),
            "fecha": self.fecha.text(),
            "hora": self.hora.text(),
            "numero_personas": int(self.numero_personas.text()),
            "estado": self.estado.text().lower()
        }
        try:
            response = requests.put(f"http://localhost:8000/api/reservas/{self.id_reserva_actual}/", json=datos)
            if response.status_code == 200:
                QMessageBox.information(self, "Actualizado", "Reserva editada correctamente.")
                self.limpiar_campos()
                self.cargar_reservas()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo editar.\n{response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def eliminar_reserva(self):
        if not self.id_reserva_actual:
            QMessageBox.warning(self, "Advertencia", "Selecciona una reserva.")
            return
        confirm = QMessageBox.question(self, "Confirmar", "¿Eliminar esta reserva?")
        if confirm == QMessageBox.Yes:
            try:
                response = requests.delete(f"http://localhost:8000/api/reservas/{self.id_reserva_actual}/")
                if response.status_code == 204:
                    QMessageBox.information(self, "Eliminada", "Reserva eliminada.")
                    self.limpiar_campos()
                    self.cargar_reservas()
                else:
                    QMessageBox.warning(self, "Error", f"No se pudo eliminar.\n{response.text}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def limpiar_campos(self):
        self.id_cliente.clear()
        self.id_mesa.clear()
        self.fecha.clear()
        self.hora.clear()
        self.numero_personas.clear()
        self.estado.clear()
        self.id_reserva_actual = None
