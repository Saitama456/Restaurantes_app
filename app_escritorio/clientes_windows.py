from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QListWidget, QListWidgetItem, QHBoxLayout
import requests

class ClientesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clientes")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        # Formulario
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

        layout.addWidget(QLabel("Clientes registrados:"))
        self.lista_clientes = QListWidget()
        self.lista_clientes.itemClicked.connect(self.seleccionar_cliente)
        layout.addWidget(self.lista_clientes)

        # Botones de acción
        btn_layout = QHBoxLayout()
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_editar.clicked.connect(self.editar_cliente)
        self.btn_eliminar.clicked.connect(self.eliminar_cliente)
        btn_layout.addWidget(self.btn_editar)
        btn_layout.addWidget(self.btn_eliminar)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.id_cliente_actual = None
        self.cargar_clientes()

    def cargar_clientes(self):
        self.lista_clientes.clear()
        try:
            response = requests.get("http://localhost:8000/api/clientes/")
            if response.status_code == 200:
                clientes = response.json()
                for cliente in clientes:
                    item = QListWidgetItem(f"{cliente['id']}: {cliente['nombre']} - {cliente['correo']}")
                    item.setData(1000, cliente)  # guardamos el cliente completo
                    self.lista_clientes.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar clientes.\n{e}")

    def seleccionar_cliente(self, item):
        cliente = item.data(1000)
        self.id_cliente_actual = cliente['id']
        self.nombre.setText(cliente['nombre'])
        self.email.setText(cliente['correo'])
        self.telefono.setText(cliente['telefono'])

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
                self.nombre.clear()
                self.email.clear()
                self.telefono.clear()
                self.cargar_clientes()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo registrar cliente.\n{response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def editar_cliente(self):
        if not self.id_cliente_actual:
            QMessageBox.warning(self, "Advertencia", "Selecciona un cliente para editar.")
            return

        datos = {
            "nombre": self.nombre.text(),
            "correo": self.email.text(),
            "telefono": self.telefono.text()
        }
        try:
            response = requests.put(f"http://localhost:8000/api/clientes/{self.id_cliente_actual}/", json=datos)
            if response.status_code == 200:
                QMessageBox.information(self, "Éxito", "Cliente editado correctamente.")
                self.nombre.clear()
                self.email.clear()
                self.telefono.clear()
                self.id_cliente_actual = None
                self.cargar_clientes()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo editar cliente.\n{response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def eliminar_cliente(self):
        if not self.id_cliente_actual:
            QMessageBox.warning(self, "Advertencia", "Selecciona un cliente para eliminar.")
            return

        confirm = QMessageBox.question(self, "Confirmar", "¿Seguro que deseas eliminar este cliente?")
        if confirm == QMessageBox.Yes:
            try:
                response = requests.delete(f"http://localhost:8000/api/clientes/{self.id_cliente_actual}/")
                if response.status_code == 204:
                    QMessageBox.information(self, "Éxito", "Cliente eliminado correctamente.")
                    self.nombre.clear()
                    self.email.clear()
                    self.telefono.clear()
                    self.id_cliente_actual = None
                    self.cargar_clientes()
                else:
                    QMessageBox.warning(self, "Error", f"No se pudo eliminar cliente.\n{response.text}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
