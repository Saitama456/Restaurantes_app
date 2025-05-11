# login_app.py
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sys
from ventana_principal import VentanaPrincipal  

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login de Administrador")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.usuario_input = QLineEdit()
        self.contrasena_input = QLineEdit()
        self.contrasena_input.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Iniciar sesión")
        self.btn_login.clicked.connect(self.verificar_login)

        layout.addWidget(QLabel("Usuario:"))
        layout.addWidget(self.usuario_input)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.contrasena_input)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def verificar_login(self):
        usuario = self.usuario_input.text()
        contrasena = self.contrasena_input.text()

        if usuario == "admin" and contrasena == "admin123":
            self.abrir_ventana_admin()
        else:
            QMessageBox.warning(self, "Error", "Credenciales incorrectas")

    def abrir_ventana_admin(self):
        self.ventana_admin = VentanaPrincipal()
        self.ventana_admin.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
