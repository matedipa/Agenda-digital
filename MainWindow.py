# -*- coding: utf-8 -*-
import datetime
import sys
import os
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog, QMessageBox, 
                             QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout)
from PySide6.QtCore import Slot, QTime, QRect

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
            try:
                usuarios = json.load(f)
            except json.JSONDecodeError:
                usuarios = []

        # Verificar si ya existe el nombre o el gmail
        for usuario in usuarios:
            if usuario["nombre"] == nombre:
                QMessageBox.warning(self, "Error", "Ya existe un usuario con ese nombre.")
                return
            if usuario["gmail"] == gmail:
                QMessageBox.warning(self, "Error", "Ya existe un usuario con ese Gmail.")
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
        self.setMinimumSize(400, 300)

        # --- Lógica de la tabla ---
        # Como el UI no tiene una tabla, la creamos aquí
        # Asumimos que el Ui_MostrarHorario usa setGeometry
        self.tableWidget = QTableWidget(self)
        # Posicionamos la tabla debajo del título (label)
        self.tableWidget.setGeometry(QRect(10, 50, 380, 240)) 
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Día", "Materia", "Inicio", "Fin"])
        self.tableWidget.setSortingEnabled(True)

        self.archivo_horario = os.path.join(os.path.dirname(__file__), "horario.json")
        self.cargar_y_mostrar_horario()

    def cargar_y_mostrar_horario(self):
        horario = []
        if os.path.exists(self.archivo_horario):
            try:
                with open(self.archivo_horario, "r") as f:
                    data = json.load(f)
                    horario = data.get("horario", [])
            except json.JSONDecodeError:
                horario = []

        self.tableWidget.setRowCount(len(horario))
        
        # Ordenar por día y luego por hora de inicio
        dias_orden = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
        try:
            horario_ordenado = sorted(
                horario, 
                key=lambda x: (dias_orden.index(x["dia"]), QTime.fromString(x["inicio"], "HH:mm"))
            )
        except ValueError:
            horario_ordenado = horario # Fallback si hay un día no esperado
            
        for row, entrada in enumerate(horario_ordenado):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(entrada["dia"]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(entrada["materia"]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(entrada["inicio"]))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(entrada["fin"]))

        self.tableWidget.resizeColumnsToContents()


class VentanaEditarHorario(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_EditarHorario()
        self.ui.setupUi(self)
        self.setWindowTitle("Editar Horario")

        # --- NUEVO: Forzar la habilitación y población de los widgets ---
        # Garantizamos que los campos de día y hora sean seleccionables
        # independientemente de la configuración del archivo .ui
        
        # Habilitar los selectores de tiempo
        self.ui.timeEdit.setEnabled(True)
        self.ui.timeEdit_2.setEnabled(True)
        
        # Habilitar y poblar el selector de días (comboBox)
        self.ui.comboBox.setEnabled(True)
        # Limpiamos por si el .ui tenía algo mal o estaba vacío
        if self.ui.comboBox.count() == 0:
            self.ui.comboBox.addItems(["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"])
        
        # Habilitar el selector de materia (se puebla en cargar_datos)
        self.ui.comboBox_2.setEnabled(True)
        # --- FIN DE LA ADICIÓN ---


        # --- Configuración de la lógica ---
        self.archivo_horario = os.path.join(os.path.dirname(__file__), "horario.json")
        
        # Datos en memoria
        self.materias = []
        self.horario = []

        self.cargar_datos()

        # Hacer el ComboBox de materias editable
        self.ui.comboBox_2.setEditable(True)
        # Opcional: Configurar para que el texto ingresado se añada (si no existe)
        self.ui.comboBox_2.setInsertPolicy(self.ui.comboBox_2.InsertPolicy.NoInsert)


        # Conectar botones
        self.ui.pushButton.clicked.connect(self.agregar_clase)
        self.ui.pushButton_2.clicked.connect(self.guardar_y_cerrar)

    def cargar_datos(self):
        """Carga materias y horario desde el archivo JSON a la memoria."""
        if not os.path.exists(self.archivo_horario):
            # Si no existe, lo creamos con estructura vacía
            self.guardar_datos_en_archivo()
            return

        try:
            with open(self.archivo_horario, "r") as f:
                data = json.load(f)
                self.materias = data.get("materias", [])
                self.horario = data.get("horario", [])
        except json.JSONDecodeError:
            self.materias = []
            self.horario = []
            QMessageBox.warning(self, "Error de Carga", "No se pudo leer el archivo horario.json. Se creará uno nuevo.")
            self.guardar_datos_en_archivo() # Crea uno nuevo si está corrupto

        # Poblar el combobox de materias
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItems(self.materias)

    def guardar_datos_en_archivo(self):
        """Escribe los datos en memoria (materias y horario) al archivo JSON."""
        data = {
            "materias": sorted(list(set(self.materias))), # Ordena y elimina duplicados
            "horario": self.horario
        }
        try:
            with open(self.archivo_horario, "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            QMessageBox.critical(self, "Error al Guardar", f"No se pudo escribir en el archivo horario.json:\n{e}")

    def guardar_y_cerrar(self):
        """Guarda los cambios pendientes en el archivo y cierra la ventana."""
        self.guardar_datos_en_archivo()
        QMessageBox.information(self, "Guardado", "Horario guardado correctamente.")
        self.accept() # Cierra el QDialog

    def check_overlap(self, inicio1, fin1, inicio2, fin2):
        """Comprueba si dos rangos de QTime se superponen."""
        # Logica: (Inicio1 < Fin2) y (Fin1 > Inicio2)
        return inicio1 < fin2 and fin1 > inicio2

    def agregar_clase(self):
        """Añade la clase configurada a la lista de horario en memoria."""
        
        # 1. Obtener datos de la UI
        dia = self.ui.comboBox.currentText()
        materia = self.ui.comboBox_2.currentText().strip()
        
        # Validar materia
        if not materia:
            QMessageBox.warning(self, "Datos incompletos", "Debe ingresar o seleccionar una materia.")
            return

        inicio_qtime = self.ui.timeEdit.time()
        fin_qtime = self.ui.timeEdit_2.time()

        # Validar horas
        if fin_qtime <= inicio_qtime:
            QMessageBox.warning(self, "Error de Horas", "La hora de fin debe ser posterior a la hora de inicio.")
            return

        # 2. Detección de conflictos
        indices_a_borrar = []
        for i, entrada in enumerate(self.horario):
            # Solo revisar conflictos en el mismo día
            if entrada["dia"] != dia:
                continue

            # Convertir horas guardadas (string) a QTime para comparar
            e_inicio = QTime.fromString(entrada["inicio"], "HH:mm")
            e_fin = QTime.fromString(entrada["fin"], "HH:mm")

            if self.check_overlap(inicio_qtime, fin_qtime, e_inicio, e_fin):
                # ¡Conflicto encontrado!
                respuesta = QMessageBox.question(self, "Conflicto de Horario",
                    f"El horario ingresado ({inicio_qtime.toString('HH:mm')} - {fin_qtime.toString('HH:mm')}) "
                    f"se superpone con:\n\n"
                    f"Materia: {entrada['materia']}\n"
                    f"Horario: {entrada['inicio']} - {entrada['fin']}\n\n"
                    f"¿Desea sobreescribir la entrada existente?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if respuesta == QMessageBox.StandardButton.Yes:
                    indices_a_borrar.append(i)
                else:
                    # El usuario no quiso sobreescribir, cancelamos "Agregar"
                    QMessageBox.information(self, "Cancelado", "Operación cancelada. No se agregó la clase.")
                    return

        # 3. Borrar entradas marcadas (en orden inverso para no alterar índices)
        if indices_a_borrar:
            for i in sorted(indices_a_borrar, reverse=True):
                del self.horario[i]

        # 4. Agregar la nueva materia (si es nueva)
        if materia not in self.materias:
            self.materias.append(materia)
            # Actualizamos el ComboBox en vivo
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItems(self.materias)
            self.ui.comboBox_2.setCurrentText(materia)

        # 5. Agregar la nueva entrada de horario (en memoria)
        nueva_entrada = {
            "dia": dia,
            "materia": materia,
            "inicio": inicio_qtime.toString("HH:mm"),
            "fin": fin_qtime.toString("HH:mm")
        }
        self.horario.append(nueva_entrada)

        QMessageBox.information(self, "Agregado", 
                                f"Clase '{materia}' agregada para el {dia}.\n\n"
                                "Presione 'Guardar' para aplicar todos los cambios permanentemente.")



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
        # Usamos exec() para que la ventana sea modal y espere a que se cierre
        # (al presionar "Guardar") antes de continuar.
        ventana.exec()
        
        # Opcional: Si quisieras que la tabla se actualice automáticamente
        # después de cerrar "Editar", tendrías que rehacer la ventana "Mostrar"
        # o enviarle una señal. Por ahora, se actualizará la próxima vez
        # que se abra "Mostrar Horario".


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