from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QApplication
from clientes_windows import ClientesWindow
from reservas_windows import ReservasWindow
from mesas_windows import MesasWindow

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Reservas - Administración")
        self.setGeometry(100, 100, 600, 600)

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Crear pestañas usando los formularios que ya tienes
        self.tabs.addTab(ClientesWindow(), "Clientes")
        self.tabs.addTab(ReservasWindow(), "Reservas")
        self.tabs.addTab(MesasWindow(), "Mesas")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

# Solo si ejecutas este archivo directamente
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())