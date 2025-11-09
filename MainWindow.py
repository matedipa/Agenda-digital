# -*- coding: utf-8 -*-
import sys
import os
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QLineEdit
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

        # Archivo donde se guardarán los usuarios
        self.archivo_usuarios = os.path.join(os.path.dirname(__file__), "usuarios.json")
        # Si no existe el archivo, lo creamos vacío
        if not os.path.exists(self.archivo_usuarios):
            with open(self.archivo_usuarios, "w") as f:
                json.dump([], f)

        # Ocultar la contraseña
        self.ui.lineEdit_3.setEchoMode(QLineEdit.EchoMode.Password)

        # Conectar el botón "Guardar"
        self.ui.pushButton.clicked.connect(self.guardar_usuario)

    def guardar_usuario(self):
        nombre = self.ui.lineEdit.text().strip()
        gmail = self.ui.lineEdit_2.text().strip()
        contrasena = self.ui.lineEdit_3.text().strip()

        if not nombre or not gmail or not contrasena:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Leer usuarios existentes
        with open(self.archivo_usuarios, "r") as f:
            usuarios = json.load(f)

        # Verificar si ya existe el nombre o la contraseña
        for usuario in usuarios:
            if usuario["nombre"] == nombre:
                QMessageBox.warning(self, "Error", "Ya existe un usuario con ese nombre.")
                return
            if usuario["contrasena"] == contrasena:
                QMessageBox.warning(self, "Error", "Esa contraseña ya está en uso.")
                return

        # Agregar nuevo usuario
        nuevo_usuario = {
            "nombre": nombre,
            "gmail": gmail,
            "contrasena": contrasena
        }
        usuarios.append(nuevo_usuario)

        # Guardar los usuarios en el archivo
        with open(self.archivo_usuarios, "w") as f:
            json.dump(usuarios, f, indent=4)

        QMessageBox.information(self, "Éxito", f"Usuario guardado correctamente.\nRuta: {os.path.abspath(self.archivo_usuarios)}")


        # Limpiar campos
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()


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

        # Conectar botones a funciones
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
