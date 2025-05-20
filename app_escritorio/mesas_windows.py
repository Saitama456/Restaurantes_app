from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QListWidget, QListWidgetItem, QHBoxLayout
import requests

class MesasWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Mesas")
        self.setGeometry(100, 100, 400, 500)

        layout = QVBoxLayout()

        self.numero = QLineEdit()
        self.capacidad = QLineEdit()
        self.estado = QLineEdit()

        layout.addWidget(QLabel("Número de Mesa:"))
        layout.addWidget(self.numero)
        layout.addWidget(QLabel("Capacidad:"))
        layout.addWidget(self.capacidad)
        layout.addWidget(QLabel("Estado (disponible/ocupada):"))
        layout.addWidget(self.estado)

        btn_guardar = QPushButton("Guardar Mesa")
        btn_guardar.clicked.connect(self.guardar_mesa)
        layout.addWidget(btn_guardar)

        layout.addWidget(QLabel("Mesas registradas:"))
        self.lista_mesas = QListWidget()
        self.lista_mesas.itemClicked.connect(self.seleccionar_mesa)
        layout.addWidget(self.lista_mesas)

        botones = QHBoxLayout()
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_editar.clicked.connect(self.editar_mesa)
        self.btn_eliminar.clicked.connect(self.eliminar_mesa)
        botones.addWidget(self.btn_editar)
        botones.addWidget(self.btn_eliminar)
        layout.addLayout(botones)

        self.setLayout(layout)
        self.id_mesa_actual = None
        self.cargar_mesas()

    def cargar_mesas(self):
        self.lista_mesas.clear()
        try:
            response = requests.get("http://localhost:8000/api/mesas/")
            if response.status_code == 200:
                mesas = response.json()
                for mesa in mesas:
                    texto = f"Mesa {mesa['numero']} - Capacidad: {mesa['capacidad']} - Estado: {mesa['estado']}"
                    item = QListWidgetItem(texto)
                    item.setData(1000, mesa)
                    self.lista_mesas.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las mesas.\n{e}")

    def seleccionar_mesa(self, item):
        mesa = item.data(1000)
        self.id_mesa_actual = mesa['id']
        self.numero.setText(str(mesa['numero']))
        self.capacidad.setText(str(mesa['capacidad']))
        self.estado.setText(mesa['estado'])

    def guardar_mesa(self):
        datos = {
            "numero": self.numero.text(),
            "capacidad": int(self.capacidad.text()),
            "estado": self.estado.text().lower()
        }
        try:
            response = requests.post("http://localhost:8000/api/mesas/", json=datos)
            if response.status_code == 201:
                QMessageBox.information(self, "Éxito", "Mesa registrada correctamente.")
                self.limpiar_campos()
                self.cargar_mesas()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo registrar la mesa.\n{response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def editar_mesa(self):
        if not self.id_mesa_actual:
            QMessageBox.warning(self, "Advertencia", "Selecciona una mesa para editar.")
            return
        datos = {
            "numero": self.numero.text(),
            "capacidad": int(self.capacidad.text()),
            "estado": self.estado.text().lower()
        }
        try:
            response = requests.put(f"http://localhost:8000/api/mesas/{self.id_mesa_actual}/", json=datos)
            if response.status_code == 200:
                QMessageBox.information(self, "Éxito", "Mesa editada correctamente.")
                self.limpiar_campos()
                self.cargar_mesas()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo editar la mesa.\n{response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def eliminar_mesa(self):
        if not self.id_mesa_actual:
            QMessageBox.warning(self, "Advertencia", "Selecciona una mesa para eliminar.")
            return
        confirmar = QMessageBox.question(self, "Confirmar", "¿Estás seguro de eliminar esta mesa?")
        if confirmar == QMessageBox.Yes:
            try:
                response = requests.delete(f"http://localhost:8000/api/mesas/{self.id_mesa_actual}/")
                if response.status_code == 204:
                    QMessageBox.information(self, "Éxito", "Mesa eliminada correctamente.")
                    self.limpiar_campos()
                    self.cargar_mesas()
                else:
                    QMessageBox.warning(self, "Error", f"No se pudo eliminar.\n{response.text}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def limpiar_campos(self):
        self.numero.clear()
        self.capacidad.clear()
        self.estado.clear()
        self.id_mesa_actual = None
