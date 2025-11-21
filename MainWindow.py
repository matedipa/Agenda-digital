# -*- coding: utf-8 -*-
from datetime import date, timedelta
import sys
import os
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog, QMessageBox,
                              QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout)
# MODIFICADO: Añadido QDate
from PySide6.QtCore import Slot, QTime, QRect, QDate

# Importá tus archivos de interfaz generados con pyside6-uic
from ui_principal import Ui_MainWindow  # Tu archivo principal real
from ui_inicia_sesion import Ui_Form as Ui_IniciarSesion
from ui_mostrar_horario import Ui_Form as Ui_MostrarHorario
from ui_editar_horario import Ui_Form as Ui_EditarHorario
from ui_agendar_tarea import Ui_Form as Ui_AgendarTarea
from ui_agendar_material import Ui_Form as Ui_AgendarMaterial
from ui_registrarse import Ui_Form as Ui_Registrarse


# -----------------------------
# CLASES DE VENTANAS SECUNDARIAS
# -----------------------------
class VentanaRegistrarse(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Registrarse()
        self.ui.setupUi(self)
        self.setWindowTitle("Registrarse")

        self.archivo_usuarios = os.path.join(os.path.dirname(__file__), "usuarios.json")

        # Cargar usuarios en el combo
        self.cargar_usuarios()

        # La contraseña ingresada se oculta (en tu UI el campo se llama lineEdit)
        self.ui.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        # Botón registrar (en tu UI este botón se llama pushButton_2)
        self.ui.pushButton_2.clicked.connect(self.verificar_usuario)
        # Variable que dirá si el usuario inició sesión
        self.usuario_actual = None

    def cargar_usuarios(self):
        try:
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                self.usuarios = json.load(f)
        except:
            self.usuarios = []

        # Limpiar usuarios vacíos o corruptos
        usuarios_validos = []
        for u in self.usuarios:
            if isinstance(u, dict) and "nombre" in u:
                usuarios_validos.append(u)

        self.usuarios = usuarios_validos

        # Llenar el combo solo con los que tengan usuario
        self.ui.comboBox.clear()
        for u in self.usuarios:
            self.ui.comboBox.addItem(u["nombre"])

    def verificar_usuario(self):
        nombre = self.ui.comboBox.currentText().strip()
        contrasena_ingresada = self.ui.lineEdit.text().strip()

        if not contrasena_ingresada:
            QMessageBox.warning(self, "Error", "Ingrese la contraseña.")
            return

        # Cargar usuarios
        try:
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                usuarios = json.load(f)
        except:
            usuarios = []

        for u in usuarios:
            if u.get("nombre") == nombre:
                if u.get("contrasena") == contrasena_ingresada:
                    self.usuario_actual = u  # Guardamos los datos del usuario
                    QMessageBox.information(self, "Bienvenido", f"Sesión iniciada como {nombre}.")
                    self.accept()
                    return
                else:
                    QMessageBox.warning(self, "Error", "Contraseña incorrecta.")
                    return

        QMessageBox.warning(self, "Error", "El usuario no existe.")


class VentanaIniciarSesion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_IniciarSesion()
        self.ui.setupUi(self)
        self.setWindowTitle("Iniciar Sesión")

        # Archivo donde se guardarán los usuarios
        self.archivo_usuarios = os.path.join(os.path.dirname(__file__), "usuarios.json")

        # Si no existe el archivo, lo creamos vacío
        if not os.path.exists(self.archivo_usuarios):
            with open(self.archivo_usuarios, "w", encoding="utf-8") as f:
                json.dump([], f)

        # Ocultar la contraseña (según tu UI de iniciar sesión)
        try:
            self.ui.lineEdit_3.setEchoMode(QLineEdit.EchoMode.Password)
        except Exception:
            # En caso de nombres distintos en UI, ignoramos y dejamos continuar
            pass

        # Conectar el botón "Guardar"
        self.ui.pushButton.clicked.connect(self.guardar_usuario)

    def guardar_usuario(self):
        # Usamos los nombres tal como están en tu UI (si están intercambiados, mantené eso)
        try:
            nombre = self.ui.lineEdit.text().strip()
            gmail = self.ui.lineEdit_2.text().strip()
            contrasena = self.ui.lineEdit_3.text().strip()
        except Exception:
            # Fallback si tu UI tiene otros nombres de widgets
            nombre = getattr(self.ui, "lineEdit", None) and self.ui.lineEdit.text().strip() or ""
            gmail = getattr(self.ui, "lineEdit_2", None) and self.ui.lineEdit_2.text().strip() or ""
            contrasena = getattr(self.ui, "lineEdit_3", None) and self.ui.lineEdit_3.text().strip() or ""

        if not nombre or not gmail or not contrasena:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Leer usuarios existentes
        try:
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                usuarios = json.load(f)
        except json.JSONDecodeError:
            usuarios = []
        except FileNotFoundError:
            usuarios = []

        # Verificar si ya existe el nombre o el gmail
        for usuario in usuarios:
            if usuario.get("nombre") == nombre:
                QMessageBox.warning(self, "Error", "Ya existe un usuario con ese nombre.")
                return
            if usuario.get("gmail") == gmail:
                QMessageBox.warning(self, "Error", "Ya existe un usuario con ese Gmail.")
                return

        # Agregar nuevo usuario con estructura completa
        nuevo_usuario = {
            "nombre": nombre,
            "gmail": gmail,
            "contrasena": contrasena,
            "tareas": [],
            "materiales": [],
            "horarios": []
        }
        usuarios.append(nuevo_usuario)

        # Guardar los usuarios en el archivo usuarios.json (ahora todo queda centralizado)
        try:
            with open(self.archivo_usuarios, "w", encoding="utf-8") as f:
                json.dump(usuarios, f, indent=4, ensure_ascii=False)
        except IOError as e:
            QMessageBox.critical(self, "Error al Guardar", f"No se pudo escribir en usuarios.json:\n{e}")
            return

        QMessageBox.information(self, "Éxito", f"Usuario guardado correctamente.\nRuta: {os.path.abspath(self.archivo_usuarios)}")

        # Limpiar campos (si existen)
        if hasattr(self.ui, "lineEdit"):
            self.ui.lineEdit.clear()
        if hasattr(self.ui, "lineEdit_2"):
            self.ui.lineEdit_2.clear()
        if hasattr(self.ui, "lineEdit_3"):
            self.ui.lineEdit_3.clear()


class VentanaMostrarHorario(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.ui = Ui_MostrarHorario()
        self.ui.setupUi(self)
        self.setWindowTitle("Horario")

        # cargar y mostrar el horario
        self.cargar_y_mostrar_horario()

    def cargar_y_mostrar_horario(self):
        """Carga el horario desde usuarios.json (a través del parent) y lo muestra en la tabla."""
        if not self.parent or not getattr(self.parent, "usuario_actual", None):
            QMessageBox.warning(self, "Error", "No hay usuario cargado.")
            return

        usuario = self.parent.cargar_datos_usuario()
        if usuario is None:
            QMessageBox.warning(self, "Error", "No se pudieron cargar los datos del usuario.")
            return

        horario = usuario.get("horarios", [])

        # Filtrar entradas que NO tienen "dia" (evita KeyError)
        horario = [h for h in horario if isinstance(h, dict) and "dia" in h and "inicio" in h and "fin" in h]

        dias_orden = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]

        # Ordenar por día y hora
        try:
            horario_ordenado = sorted(
                horario,
                key=lambda x: (
                    dias_orden.index(x["dia"]) if x["dia"] in dias_orden else 999,
                    QTime.fromString(x["inicio"], "HH:mm")
                )
            )
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Ocurrió un problema al ordenar el horario:\n{e}")
            horario_ordenado = horario

        # Configurar tabla (el UI ya trae tableWidget)
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Día", "Materia", "Inicio", "Fin"])
        self.ui.tableWidget.setRowCount(len(horario_ordenado))

        # Poblar la tabla
        for fila, entrada in enumerate(horario_ordenado):
            self.ui.tableWidget.setItem(fila, 0, QTableWidgetItem(entrada["dia"]))
            self.ui.tableWidget.setItem(fila, 1, QTableWidgetItem(entrada["materia"]))
            self.ui.tableWidget.setItem(fila, 2, QTableWidgetItem(entrada["inicio"]))
            self.ui.tableWidget.setItem(fila, 3, QTableWidgetItem(entrada["fin"]))

        self.ui.tableWidget.resizeColumnsToContents()


class VentanaEditarHorario(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_EditarHorario()
        self.ui.setupUi(self)
        self.setWindowTitle("Editar Horario")

        # --- Habilitar widgets ---
        self.ui.timeEdit.setEnabled(True)
        self.ui.timeEdit_2.setEnabled(True)
        self.ui.comboBox.setEnabled(True)

        if self.ui.comboBox.count() == 0:
            self.ui.comboBox.addItems(["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"])

        self.ui.comboBox_2.setEnabled(True)

        # --- Datos en memoria ---
        self.materias = []
        self.horario = []

        # Cargar desde usuarios.json vía parent
        self.cargar_datos()

        # Editable combo materias
        self.ui.comboBox_2.setEditable(True)
        self.ui.comboBox_2.setInsertPolicy(self.ui.comboBox_2.InsertPolicy.NoInsert)

        # Conectar botones
        self.ui.pushButton.clicked.connect(self.agregar_clase)
        self.ui.pushButton_2.clicked.connect(self.guardar_y_cerrar)

    def agregar_clase(self):
        dia = self.ui.comboBox.currentText()
        materia = self.ui.comboBox_2.currentText().strip()
        hora_inicio = self.ui.timeEdit.time().toString("HH:mm")
        hora_fin = self.ui.timeEdit_2.time().toString("HH:mm")

        # Validaciones
        if not materia:
            QMessageBox.warning(self, "Error", "Ingresá una materia.")
            return

        if hora_inicio == hora_fin:
            QMessageBox.warning(self, "Error", "El horario no puede tener la misma hora de inicio y fin.")
            return

        # Agregar materia si no existe
        if materia not in self.materias:
            self.materias.append(materia)
            self.ui.comboBox_2.addItem(materia)

        # Crear registro de clase
        clase = {
            "dia": dia,
            "materia": materia,
            "inicio": hora_inicio,
            "fin": hora_fin
        }

        # Agregar al horario en memoria
        self.horario.append(clase)

        QMessageBox.information(self, "OK", "Clase agregada correctamente.")

    def cargar_datos(self):
        """Carga materias y horarios desde usuarios.json usando el usuario actual (vía parent)."""
        if not self.parent or not getattr(self.parent, "usuario_actual", None):
            QMessageBox.warning(self, "Error", "No hay usuario cargado.")
            self.materias = []
            self.horario = []
            return

        usuario = self.parent.cargar_datos_usuario()
        if not usuario:
            QMessageBox.warning(self, "Error", "No se pudieron leer datos del usuario.")
            self.materias = []
            self.horario = []
            return

        # Cargar materias
        self.materias = usuario.get("materias", [])

        # Cargar horario (filtrar basura como {})
        self.horario = [
            h for h in usuario.get("horarios", [])
            if isinstance(h, dict) and "dia" in h and "materia" in h
        ]

        # Poblar materias en el combobox
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItems(self.materias)

    def guardar_y_cerrar(self):
        self.guardar_datos_en_archivo()
        self.accept()

    def guardar_datos_en_archivo(self):
        if not self.parent or not getattr(self.parent, "usuario_actual", None):
            QMessageBox.warning(self, "Error", "No hay usuario cargado para guardar.")
            return

        usuario = self.parent.cargar_datos_usuario()
        if usuario is None:
            QMessageBox.warning(self, "Error", "No existe usuario cargado.")
            return

        # Guardar horarios limpios
        usuario["horarios"] = [
            h for h in self.horario
            if isinstance(h, dict) and "dia" in h and "materia" in h
        ]

        # Guardar materias
        usuario["materias"] = self.materias

        # Guardar en usuarios.json a través del parent
        self.parent.guardar_datos_usuario(usuario)


class VentanaAgendarTarea(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.ui = Ui_AgendarTarea()
        self.ui.setupUi(self)
        self.setWindowTitle("Agendar Tarea")

        self.materias = []
        self.tareas_pendientes = []

        # Cargar datos
        self.cargar_materias()
        self.cargar_tareas()

        # Configurar widgets
        self.ui.comboBox_2.setEditable(True)
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.dateEdit.setCalendarPopup(True)

        # Conectar botones
        self.ui.pushButton_3.clicked.connect(self.agregar_tarea)
        self.ui.pushButton_2.clicked.connect(self.guardar_y_cerrar)

    def cargar_materias(self):
        if not self.parent_window or not getattr(self.parent_window, "usuario_actual", None):
            # nada que cargar
            return
        usuario = self.parent_window.cargar_datos_usuario()
        if usuario:
            # materias se sacan del horario del usuario
            self.materias = [h.get("materia") for h in usuario.get("horarios", []) if "materia" in h]

        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItems(sorted(list(set(self.materias))))

    def cargar_tareas(self):
        if not self.parent_window or not getattr(self.parent_window, "usuario_actual", None):
            return
        usuario = self.parent_window.cargar_datos_usuario()
        if usuario:
            self.tareas_pendientes = usuario.get("tareas", [])

    def agregar_tarea(self):
        materia = self.ui.comboBox_2.currentText().strip()
        descripcion = self.ui.textEdit.toPlainText().strip()
        fecha_entrega_qdate = self.ui.dateEdit.date()
        fecha_entrega_str = fecha_entrega_qdate.toString("yyyy-MM-dd")

        if not materia or not descripcion:
            QMessageBox.warning(self, "Datos incompletos", "Debe ingresar una materia y una descripción.")
            return

        nueva_tarea = {
            "materia": materia,
            "descripcion": descripcion,
            "fecha_entrega": fecha_entrega_str,
            "completada": False
        }

        self.tareas_pendientes.append(nueva_tarea)
        QMessageBox.information(self, "Agregado", "Tarea agregada. Presione 'Guardar' para confirmar.")
        self.ui.textEdit.clear()
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.comboBox_2.setFocus()

    def guardar_y_cerrar(self):
        if not self.parent_window or not getattr(self.parent_window, "usuario_actual", None):
            return
        usuario = self.parent_window.cargar_datos_usuario()
        if usuario is not None:
            usuario["tareas"] = self.tareas_pendientes
            self.parent_window.guardar_datos_usuario(usuario)

        QMessageBox.information(self, "Guardado", "Tareas guardadas correctamente.")
        self.accept()


# -----------------------------------------------------------------
# --- CLASE MODIFICADA: VentanaAgendarLibros ---
# -----------------------------------------------------------------
class VentanaAgendarLibros(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_AgendarMaterial()
        self.ui.setupUi(self)
        # El título lo toma del .ui ("Agregar Material")
        self.setWindowTitle("Agendar Material")

        self.materias = []
        self.lista_materiales = []  # Lista en memoria

        # Cargar datos desde el usuario actual (si existe)
        self.cargar_materias()
        self.cargar_materiales()

        # Configurar widgets
        self.ui.comboBox_2.setEditable(True)

        # Conectar botones (según el .ui)
        self.ui.pushButton.clicked.connect(self.agregar_material)  # "Agregar"
        self.ui.pushButton_2.clicked.connect(self.guardar_y_cerrar)  # "Guardar"

    def cargar_materias(self):
        """Carga la lista de materias desde el usuario actual (usuarios.json vía parent)."""
        if not self.parent or not getattr(self.parent, "usuario_actual", None):
            self.materias = []
        else:
            usuario = self.parent.cargar_datos_usuario()
            if usuario:
                self.materias = usuario.get("materias", [])
            else:
                self.materias = []

        # Poblar el combobox
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItems(self.materias)

    def cargar_materiales(self):
        if not self.parent or not getattr(self.parent, "usuario_actual", None):
            self.lista_materiales = []
        else:
            usuario = self.parent.cargar_datos_usuario()
            self.lista_materiales = usuario.get("materiales", [])

        # Poblar ComboBox con materias que ya están en lista_materiales (si corresponde)
        self.ui.comboBox_2.clear()
        # Si no hay materias cargadas en usuario, mantenemos las materias (cargar_materias ya las cargó)
        if self.materias:
            self.ui.comboBox_2.addItems(self.materias)
        else:
            self.ui.comboBox_2.addItems([m.get("materia") for m in self.lista_materiales if "materia" in m])

    def agregar_material(self):
        """Añade el material a la lista en memoria (self.lista_materiales)"""

        # 1. Obtener datos de la UI
        materia = self.ui.comboBox_2.currentText().strip()
        material_desc = self.ui.lineEdit.text().strip()

        # 2. Validar
        if not materia or not material_desc:
            QMessageBox.warning(self, "Datos incompletos", "Debe ingresar una materia y el material necesario.")
            return

        # 3. Crear el diccionario del material
        nuevo_material = {
            "materia": materia,
            "material": material_desc,
            "conseguido": False  # Añadimos un estado por defecto
        }

        # 4. Añadir a la lista en memoria
        self.lista_materiales.append(nuevo_material)

        # 5. Notificar y limpiar campos
        QMessageBox.information(self, "Agregado",
                                f"Material '{material_desc}' agregado para '{materia}'.\n\n"
                                "Presione 'Guardar' para aplicar todos los cambios.")

        self.ui.lineEdit.clear()
        self.ui.comboBox_2.setFocus()

    def guardar_y_cerrar(self):
        if not self.parent or not getattr(self.parent, "usuario_actual", None):
            QMessageBox.warning(self, "Error", "No hay usuario cargado para guardar materiales.")
            return

        usuario = self.parent.cargar_datos_usuario()
        if usuario is None:
            QMessageBox.warning(self, "Error", "No existe usuario cargado.")
            return

        usuario["materiales"] = self.lista_materiales
        self.parent.guardar_datos_usuario(usuario)
        QMessageBox.information(self, "Guardado", "Materiales guardados correctamente.")
        self.accept()


# -----------------------------
# CLASE PRINCIPAL
# -----------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Agenda Digital")
        self.usuario_actual = None
        self.habilitar_funciones(False)

        # Conectar botones a funciones (pasamos self como parent donde corresponda)
        self.ui.pushButton_8.clicked.connect(self.abrir_registrarse)
        self.ui.pushButton_7.clicked.connect(self.abrir_iniciar_sesion)
        self.ui.pushButton_6.clicked.connect(self.abrir_mostrar_horario)
        self.ui.pushButton_4.clicked.connect(self.abrir_editar_horario)
        self.ui.pushButton_3.clicked.connect(self.abrir_agendar_tareas)
        self.ui.pushButton_5.clicked.connect(self.abrir_agendar_libros)

    # -------------------------
    # FUNCIONES DE APERTURA
    # -------------------------
    @Slot()
    def abrir_editar_horario(self):
        ventana = VentanaEditarHorario(self)
        ventana.exec()

    @Slot()
    def abrir_mostrar_horario(self):
        ventana = VentanaMostrarHorario(self)
        ventana.exec()

    @Slot()
    def abrir_agendar_tareas(self):
        ventana = VentanaAgendarTarea(self)
        ventana.exec()

    @Slot()
    def abrir_agendar_libros(self):
        ventana = VentanaAgendarLibros(self)
        ventana.exec()

    def cargar_datos_usuario(self):
        """Carga los datos completos del usuario actual desde usuarios.json"""
        archivo = os.path.join(os.path.dirname(__file__), "usuarios.json")
        if not os.path.exists(archivo):
            return None

        try:
            with open(archivo, "r", encoding="utf-8") as f:
                usuarios = json.load(f)
        except json.JSONDecodeError:
            usuarios = []

        for u in usuarios:
            if u.get("nombre") == (self.usuario_actual and self.usuario_actual.get("nombre")):
                # Aseguramos que existan las claves
                u.setdefault("tareas", [])
                u.setdefault("materiales", [])
                u.setdefault("horarios", [])
                u.setdefault("materias", [])
                return u

        return None

    def guardar_datos_usuario(self, datos_actualizados):
        """Guarda los cambios del usuario actual dentro de usuarios.json"""
        archivo = os.path.join(os.path.dirname(__file__), "usuarios.json")
        if os.path.exists(archivo):
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    usuarios = json.load(f)
            except json.JSONDecodeError:
                usuarios = []
        else:
            usuarios = []

        # Reemplazar usuario actual por nombre (si existe) o agregar
        reemplazado = False
        for i, u in enumerate(usuarios):
            if u.get("nombre") == (self.usuario_actual and self.usuario_actual.get("nombre")):
                usuarios[i] = datos_actualizados
                reemplazado = True
                break

        if not reemplazado:
            usuarios.append(datos_actualizados)

        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(usuarios, f, indent=4, ensure_ascii=False)
        except IOError as e:
            QMessageBox.critical(self, "Error al Guardar", f"No se pudo escribir en usuarios.json:\n{e}")

    @Slot()
    def mostrar_comunicado_recordatorios(self):
        if not self.usuario_actual:
            return  # No hay usuario logueado

        # Cargar datos del usuario actual desde usuarios.json
        datos_usuario = self.cargar_datos_usuario()
        if not datos_usuario:
            QMessageBox.information(self, "Recordatorio", "No hay datos para mostrar.")
            return

        tareas = datos_usuario.get("tareas", [])
        materiales = datos_usuario.get("materiales", [])

        texto = "📘 Recordatorio personal\n\n"

        # Tareas
        if tareas:
            texto += "📚 Tareas y exámenes pendientes:\n"
            for t in tareas:
                estado = "✔ completada" if t.get("completada") else "❗ pendiente"
                texto += f"- {t.get('materia')}: {t.get('descripcion')} — entrega: {t.get('fecha_entrega')} ({estado})\n"
        else:
            texto += "No hay tareas cargadas.\n"

        texto += "\n"

        # Materiales
        if materiales:
            texto += "🎒 Materiales cargados:\n"
            for m in materiales:
                estado = "✔ conseguido" if m.get("conseguido") else "❗ pendiente"
                texto += f"- {m.get('materia')}: {m.get('material')} ({estado})\n"
        else:
            texto += "No hay materiales cargados.\n"

        texto += "\n📆 Material necesario para mañana:\n"

        # Materiales pendientes
        materiales_manana = [m for m in materiales if not m.get("conseguido")]
        if materiales_manana:
            for m in materiales_manana:
                texto += f"- Llevar {m.get('material')} para {m.get('materia')}\n"
        else:
            texto += "No necesitás llevar nada extra mañana.\n"

        # Mostrar mensaje
        msg = QMessageBox()
        msg.setWindowTitle("Recordatorio")
        msg.setText(texto)
        msg.exec()

    def habilitar_funciones(self, estado):
        self.ui.pushButton_6.setEnabled(estado)  # Mostrar horario
        self.ui.pushButton_4.setEnabled(estado)  # Editar horario
        self.ui.pushButton_3.setEnabled(estado)  # Agendar tarea/examen
        self.ui.pushButton_5.setEnabled(estado)  # Agendar material

    @Slot()
    def abrir_registrarse(self):
        ventana = VentanaRegistrarse(self)
        if ventana.exec():  # si inicia sesión correctamente
            # ventana.usuario_actual viene del diálogo; asignamos como usuario actual
            self.usuario_actual = ventana.usuario_actual
            self.habilitar_funciones(True)
            # Mostrar recordatorio inmediatamente
            self.mostrar_comunicado_recordatorios()
        else:
            self.habilitar_funciones(False)

    @Slot()
    def abrir_iniciar_sesion(self):
        ventana = VentanaIniciarSesion(self)
        ventana.exec()


# -----------------------------
# PROGRAMA PRINCIPAL
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
