import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from PySide6.QtCore import Slot

# Importá tus archivos de interfaz generados con pyside6-uic
from ui_principal import Ui_MainWindow  # Tu archivo principal real
from ui_inicia_sesion import Ui_Form as Ui_IniciarSesion
from ui_mostrar_horario import Ui_Form as Ui_MostrarHorario
from ui_editar_horario import Ui_Form as Ui_EditarHorario
from ui_agendar_tarea import Ui_Form as Ui_AgendarTarea
from ui_agendar_material import Ui_Form as Ui_AgendarMaterial


# -----------------------------
# CLASES DE VENTANAS SECUNDARIAS
# -----------------------------

class VentanaIniciarSesion(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_IniciarSesion()
        self.ui.setupUi(self)
        self.setWindowTitle("Iniciar Sesión")


class VentanaMostrarHorario(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MostrarHorario()
        self.ui.setupUi(self)
        self.setWindowTitle("Mostrar Horario")


class VentanaEditarHorario(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_EditarHorario()
        self.ui.setupUi(self)
        self.setWindowTitle("Editar Horario")


class VentanaAgendarTarea(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AgendarTarea()
        self.ui.setupUi(self)
        self.setWindowTitle("Agendar Tarea")


class VentanaAgendarLibros(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AgendarMaterial()
        self.ui.setupUi(self)
        self.setWindowTitle("Agendar Libros")


# -----------------------------
# CLASE PRINCIPAL
# -----------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Agenda Digital")

        # Conectar botones a funciones (ajustá los nombres a los de tu interfaz)
        self.ui.pushButton_7.clicked.connect(self.abrir_iniciar_sesion)
        self.ui.pushButton_6.clicked.connect(self.abrir_mostrar_horario)
        self.ui.pushButton_4.clicked.connect(self.abrir_editar_horario)
        self.ui.pushButton_3.clicked.connect(self.abrir_agendar_tareas)
        self.ui.pushButton_5.clicked.connect(self.abrir_agendar_libros)

    # -------------------------
    # FUNCIONES DE APERTURA
    # -------------------------
    @Slot()
    def abrir_iniciar_sesion(self):
        ventana = VentanaIniciarSesion()
        ventana.exec()

    @Slot()
    def abrir_mostrar_horario(self):
        ventana = VentanaMostrarHorario()
        ventana.exec()

    @Slot()
    def abrir_editar_horario(self):
        ventana = VentanaEditarHorario()
        ventana.exec()

    @Slot()
    def abrir_agendar_tareas(self):
        ventana = VentanaAgendarTarea()
        ventana.exec()

    @Slot()
    def abrir_agendar_libros(self):
        ventana = VentanaAgendarLibros()
        ventana.exec()


# -----------------------------
# PROGRAMA PRINCIPAL
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
