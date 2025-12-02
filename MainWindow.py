# -*- coding: utf-8 -*-                     # Indica que el archivo usa codificación UTF-8
from datetime import date, timedelta         # Importa clases para manejar fechas y diferencias entre ellas
import sys                                   # Permite acceder a funciones del intérprete de Python
import os                                    # Permite trabajar con archivos y rutas del sistema operativo
import serial                                # Librería para comunicarse por puertos seriales
import serial.tools.list_ports               # Permite listar los puertos seriales disponibles
import time                                  # Permite usar funciones de tiempo (sleep, etc.)
from PySide6.QtWidgets import QProgressDialog # Ventana de progreso visual
from PySide6.QtCore import Qt                # Constantes y funciones básicas de Qt
import json                                  # Para leer/escribir archivos JSON
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog, QMessageBox,
                              QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout)  
                                              # Importa widgets de Qt necesarios para las ventanas
# MODIFICADO: Añadido QDate
from PySide6.QtCore import Slot, QTime, QRect, QDate   # Importa señales, hora, rectángulos y fechas

# Importá tus archivos de interfaz generados con pyside6-uic
from ui_principal import Ui_MainWindow                # UI principal generada por pyside6-uic
from ui_inicia_sesion import Ui_Form as Ui_IniciarSesion  # UI ventana iniciar sesión
from ui_mostrar_horario import Ui_Form as Ui_MostrarHorario # UI ventana mostrar horario
from ui_editar_horario import Ui_Form as Ui_EditarHorario   # UI ventana editar horario
from ui_agendar_tarea import Ui_Form as Ui_AgendarTarea      # UI ventana agendar tarea
from ui_agendar_material import Ui_Form as Ui_AgendarMaterial # UI ventana agendar material
from ui_registrarse import Ui_Form as Ui_Registrarse          # UI ventana registrarse


# -----------------------------
# CLASES DE VENTANAS SECUNDARIAS
# -----------------------------
class VentanaRegistrarse(QDialog):       # Define una ventana secundaria que hereda de QDialog
    def __init__(self, parent=None):     # Constructor, parent es la ventana padre
        super().__init__(parent)         # Llama al constructor de QDialog
        self.ui = Ui_Registrarse()       # Crea la interfaz de la ventana
        self.ui.setupUi(self)            # Configura los widgets dentro del diálogo
        self.setWindowTitle("Registrarse")  # Título de la ventana

        self.archivo_usuarios = os.path.join(os.path.dirname(__file__), "usuarios.json")
                                          # Ruta completa al archivo usuarios.json

        # Cargar usuarios en el combo
        self.cargar_usuarios()            # Llama a la función que carga los nombres en el comboBox

        # La contraseña ingresada se oculta (en tu UI el campo se llama lineEdit)
        self.ui.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
                                          # Oculta los caracteres escritos como puntos

        # Botón registrar (en tu UI este botón se llama pushButton_2)
        self.ui.pushButton_2.clicked.connect(self.verificar_usuario)
                                           # Cuando se hace clic, se ejecuta verificar_usuario()

        # Variable que dirá si el usuario inició sesión
        self.usuario_actual = None        # Guardará los datos del usuario cuando inicie sesión

    def cargar_usuarios(self):            # Carga los usuarios desde usuarios.json
        try:
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                self.usuarios = json.load(f)   # Lee el listado de usuarios
        except:
            self.usuarios = []           # Si falla, crea una lista vacía

        # Limpiar usuarios vacíos o corruptos
        usuarios_validos = []            # Lista temporal
        for u in self.usuarios:          # Revisa cada usuario
            if isinstance(u, dict) and "nombre" in u:  # Solo acepta dict con clave nombre
                usuarios_validos.append(u)

        self.usuarios = usuarios_validos  # Guarda la lista validada

        # Llenar el combo solo con los que tengan usuario
        self.ui.comboBox.clear()          # Limpia el comboBox
        for u in self.usuarios:           # Agrega nombre por nombre
            self.ui.comboBox.addItem(u["nombre"])

    def verificar_usuario(self):          # Valida usuario y contraseña
        nombre = self.ui.comboBox.currentText().strip()
                                          # Obtiene el nombre actual del combo
        contrasena_ingresada = self.ui.lineEdit.text().strip()
                                          # Obtiene la contraseña ingresada

        if not contrasena_ingresada:      # Si no escribió nada
            QMessageBox.warning(self, "Error", "Ingrese la contraseña.")
            return

        # Cargar usuarios
        try:
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                usuarios = json.load(f)   # Relee el archivo usuarios.json
        except:
            usuarios = []                 # Si falla, lista vacía

        for u in usuarios:                # Recorre usuarios
            if u.get("nombre") == nombre: # Si coincide el nombre
                if u.get("contrasena") == contrasena_ingresada:
                                          # Contraseña correcta
                    self.usuario_actual = u  # Guarda el usuario logueado
                    QMessageBox.information(self, "Bienvenido", f"Sesión iniciada como {nombre}.")
                    self.accept()         # Cierra la ventana devolviendo "OK"
                    return
                else:
                    QMessageBox.warning(self, "Error", "Contraseña incorrecta.")
                    return

        QMessageBox.warning(self, "Error", "El usuario no existe.")  # Si no se encontró usuario


class VentanaIniciarSesion(QDialog):    # Otra ventana secundaria
    def __init__(self, parent=None):
        super().__init__(parent)         # Llama al constructor padre
        self.ui = Ui_IniciarSesion()     # Carga la interfaz
        self.ui.setupUi(self)            # Configura widgets
        self.setWindowTitle("Iniciar Sesión")  # Título

        # Archivo donde se guardarán los usuarios
        self.archivo_usuarios = os.path.join(os.path.dirname(__file__), "usuarios.json")

        # Si no existe el archivo, lo creamos vacío
        if not os.path.exists(self.archivo_usuarios):
            with open(self.archivo_usuarios, "w", encoding="utf-8") as f:
                json.dump([], f)         # Crea un archivo JSON vacío

        # Ocultar la contraseña (según tu UI de iniciar sesión)
        try:
            self.ui.lineEdit_3.setEchoMode(QLineEdit.EchoMode.Password)
        except Exception:
            # En caso de nombres distintos en UI, ignoramos y dejamos continuar
            pass                         # Evita errores si el widget no existe

        # Conectar el botón "Guardar"
        self.ui.pushButton.clicked.connect(self.guardar_usuario)
                                        # Ejecuta guardar_usuario() al presionar el botón

    def guardar_usuario(self):          # Crea un nuevo usuario en usuarios.json
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
            return                      # No permitir datos vacíos

        # Leer usuarios existentes
        try:
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                usuarios = json.load(f) # Carga JSON existente
        except json.JSONDecodeError:
            usuarios = []               # JSON corrupto
        except FileNotFoundError:
            usuarios = []               # Archivo no encontrado

        # Verificar si ya existe el nombre o el gmail
        for usuario in usuarios:
            if usuario.get("nombre") == nombre:  # Nombre duplicado
                QMessageBox.warning(self, "Error", "Ya existe un usuario con ese nombre.")
                return
            if usuario.get("gmail") == gmail:    # Gmail duplicado
                QMessageBox.warning(self, "Error", "Ya existe un usuario con ese Gmail.")
                return

        # Agregar nuevo usuario con estructura completa
        nuevo_usuario = {
            "nombre": nombre,
            "gmail": gmail,
            "contrasena": contrasena,
            "tareas": [],               # Listas vacías para que no den error al usarlas
            "materiales": [],
            "horarios": []
        }
        usuarios.append(nuevo_usuario)  # Agrega el usuario a la lista

        # Guardar los usuarios en el archivo usuarios.json (ahora todo queda centralizado)
        try:
            with open(self.archivo_usuarios, "w", encoding="utf-8") as f:
                json.dump(usuarios, f, indent=4, ensure_ascii=False)
        except IOError as e:            # Si no se puede escribir
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
class VentanaMostrarHorario(QDialog):  # Clase que muestra el horario en una tabla
    def __init__(self, parent=None):  # Constructor de la ventana, recibe el MainWindow como parent
        super().__init__(parent)  # Llama al constructor de QDialog
        self.parent = parent  # Guarda el parent para acceder a los datos del usuario

        self.ui = Ui_MostrarHorario()  # Crea la interfaz generada por Qt Designer
        self.ui.setupUi(self)  # Configura todos los widgets
        self.setWindowTitle("Horario")  # Título de la ventana

        # cargar y mostrar el horario
        self.cargar_y_mostrar_horario()  # Llama a la función que lee y muestra el horario

    def cargar_y_mostrar_horario(self):  # Función que carga el horario desde el JSON y lo dibuja
        """Carga el horario desde usuarios.json (a través del parent) y lo muestra en la tabla."""
        if not self.parent or not getattr(self.parent, "usuario_actual", None):  # Verifica si existe usuario abierto
            QMessageBox.warning(self, "Error", "No hay usuario cargado.")  # Muestra error si no hay usuario
            return

        usuario = self.parent.cargar_datos_usuario()  # Carga datos del usuario desde JSON
        if usuario is None:  # Si no se pudo leer
            QMessageBox.warning(self, "Error", "No se pudieron cargar los datos del usuario.")  # Mensaje de error
            return

        horario = usuario.get("horarios", [])  # Obtiene la lista de horarios guardados del usuario

        # Filtrar entradas que NO tienen "dia" (evita KeyError)
        horario = [h for h in horario if isinstance(h, dict) and "dia" in h and "inicio" in h and "fin" in h]  # Filtra horarios inválidos

        dias_orden = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]  # Orden de días para ordenar después

        # Ordenar por día y hora
        try:
            horario_ordenado = sorted(  # Ordena la lista de clases
                horario,
                key=lambda x: (
                    dias_orden.index(x["dia"]) if x["dia"] in dias_orden else 999,  # Ordena por día
                    QTime.fromString(x["inicio"], "HH:mm")  # Luego por hora de inicio
                )
            )
        except Exception as e:  # Si falla el ordenamiento
            QMessageBox.warning(self, "Error", f"Ocurrió un problema al ordenar el horario:\n{e}")  # Mensaje error
            horario_ordenado = horario  # Deja el orden original

        # Configurar tabla (el UI ya trae tableWidget)
        self.ui.tableWidget.setColumnCount(4)  # La tabla tendrá 4 columnas
        self.ui.tableWidget.setHorizontalHeaderLabels(["Día", "Materia", "Inicio", "Fin"])  # Nombres de columnas
        self.ui.tableWidget.setRowCount(len(horario_ordenado))  # Cantidad de filas según cantidad de clases

        # Poblar la tabla
        for fila, entrada in enumerate(horario_ordenado):  # Recorre cada clase ordenada
            self.ui.tableWidget.setItem(fila, 0, QTableWidgetItem(entrada["dia"]))  # Día
            self.ui.tableWidget.setItem(fila, 1, QTableWidgetItem(entrada["materia"]))  # Materia
            self.ui.tableWidget.setItem(fila, 2, QTableWidgetItem(entrada["inicio"]))  # Hora inicio
            self.ui.tableWidget.setItem(fila, 3, QTableWidgetItem(entrada["fin"]))  # Hora fin

        self.ui.tableWidget.resizeColumnsToContents()  # Ajusta ancho de columnas al contenido


class VentanaEditarHorario(QDialog):  # Ventana para agregar o modificar el horario
    def __init__(self, parent=None):  # Constructor
        super().__init__(parent)  # Inicializa QDialog
        self.parent = parent  # Guarda el MainWindow para usar sus funciones
        self.ui = Ui_EditarHorario()  # Carga la UI
        self.ui.setupUi(self)  # Configura widgets
        self.setWindowTitle("Editar Horario")  # Título

        # --- Habilitar widgets ---
        self.ui.timeEdit.setEnabled(True)  # Activa selector de hora inicio
        self.ui.timeEdit_2.setEnabled(True)  # Activa selector de hora fin
        self.ui.comboBox.setEnabled(True)  # Combo de días

        if self.ui.comboBox.count() == 0:  # Si el combo de días está vacío
            self.ui.comboBox.addItems(["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"])  # Agrega días

        self.ui.comboBox_2.setEnabled(True)  # Combo de materias existentes

        # --- Datos en memoria ---
        self.materias = []  # Lista interna de materias del usuario
        self.horario = []  # Lista interna del horario

        # Cargar desde usuarios.json vía parent
        self.cargar_datos()  # Carga materias y horario desde el archivo

        # Editable combo materias
        self.ui.comboBox_2.setEditable(True)  # Permite escribir materias nuevas
        self.ui.comboBox_2.setInsertPolicy(self.ui.comboBox_2.InsertPolicy.NoInsert)  # Evita duplicados automáticos

        # Conectar botones
        self.ui.pushButton.clicked.connect(self.agregar_clase)  # Botón "Agregar"
        self.ui.pushButton_2.clicked.connect(self.guardar_y_cerrar)  # Botón "Guardar y cerrar"

    def agregar_clase(self):  # Función para agregar una nueva clase al horario
        dia = self.ui.comboBox.currentText()  # Obtiene el día seleccionado
        materia = self.ui.comboBox_2.currentText().strip()  # Materia escrita/seleccionada
        hora_inicio = self.ui.timeEdit.time().toString("HH:mm")  # Hora inicio en formato string
        hora_fin = self.ui.timeEdit_2.time().toString("HH:mm")  # Hora fin

        # Validaciones
        if not materia:  # Si no se escribió materia
            QMessageBox.warning(self, "Error", "Ingresá una materia.")  # Mensaje error
            return

        if hora_inicio == hora_fin:  # Evita horarios inválidos
            QMessageBox.warning(self, "Error", "El horario no puede tener la misma hora de inicio y fin.")
            return

        # Agregar materia si no existe
        if materia not in self.materias:  # Si es nueva
            self.materias.append(materia)  # La agrega internamente
            self.ui.comboBox_2.addItem(materia)  # La agrega al combo

        # Crear registro de clase
        clase = {
            "dia": dia,
            "materia": materia,
            "inicio": hora_inicio,
            "fin": hora_fin
        }

        # Agregar al horario en memoria
        self.horario.append(clase)  # Añade la clase a la lista

        QMessageBox.information(self, "OK", "Clase agregada correctamente.")  # Aviso

    def cargar_datos(self):  # Carga materias y horarios desde JSON
        """Carga materias y horarios desde usuarios.json usando el usuario actual (vía parent)."""
        if not self.parent or not getattr(self.parent, "usuario_actual", None):  # Verifica usuario cargado
            QMessageBox.warning(self, "Error", "No hay usuario cargado.")  # Mensaje si falta
            self.materias = []  # Limpia todo
            self.horario = []
            return

        usuario = self.parent.cargar_datos_usuario()  # Lee JSON
        if not usuario:  # Si falla
            QMessageBox.warning(self, "Error", "No se pudieron leer datos del usuario.")
            self.materias = []
            self.horario = []
            return

        # Cargar materias
        self.materias = usuario.get("materias", [])  # Lista de materias guardada

        # Cargar horario (filtrar basura como {})
        self.horario = [
            h for h in usuario.get("horarios", [])  # Recorrer clases
            if isinstance(h, dict) and "dia" in h and "materia" in h  # Solo válidas
        ]

        # Poblar materias en el combobox
        self.ui.comboBox_2.clear()  # Limpia el combo
        self.ui.comboBox_2.addItems(self.materias)  # Carga materias guardadas

    def guardar_y_cerrar(self):  # Guarda cambios y cierra la ventana
        self.guardar_datos_en_archivo()  # Llama a la función de guardar
        self.accept()  # Cierra la ventana

    def guardar_datos_en_archivo(self):  # Guarda horario y materias en usuarios.json
        if not self.parent or not getattr(self.parent, "usuario_actual", None):  # Sin usuario cargado
            QMessageBox.warning(self, "Error", "No hay usuario cargado para guardar.")  # Error
            return

        usuario = self.parent.cargar_datos_usuario()  # Carga usuario
        if usuario is None:  # Si falla
            QMessageBox.warning(self, "Error", "No existe usuario cargado.")
            return

        # Guardar horarios limpios
        usuario["horarios"] = [
            h for h in self.horario
            if isinstance(h, dict) and "dia" in h and "materia" in h
        ]

        # Guardar materias
        usuario["materias"] = self.materias  # Guarda materias

        # Guardar en usuarios.json a través del parent
        self.parent.guardar_datos_usuario(usuario)  # Escribe cambios en archivo
class VentanaAgendarTarea(QDialog):  # Ventana para crear y guardar tareas
    def __init__(self, parent=None):  # Constructor
        super().__init__(parent)  # Inicializa QDialog
        self.parent_window = parent  # Guarda el MainWindow para acceder a JSON
        self.ui = Ui_AgendarTarea()  # Carga la interfaz .ui
        self.ui.setupUi(self)  # Configura widgets
        self.setWindowTitle("Agendar Tarea")  # Título ventana

        self.materias = []  # Lista de materias, se carga del usuario
        self.tareas_pendientes = []  # Lista de tareas aún no guardadas

        # Cargar datos
        self.cargar_materias()  # Obtiene materias del horario
        self.cargar_tareas()  # Carga tareas existentes del usuario

        # Configurar widgets
        self.ui.comboBox_2.setEditable(True)  # Permite escribir materias nuevas
        self.ui.dateEdit.setDate(QDate.currentDate())  # Fecha por defecto = hoy
        self.ui.dateEdit.setCalendarPopup(True)  # Muestra el calendario desplegable

        # Conectar botones
        self.ui.pushButton_3.clicked.connect(self.agregar_tarea)  # Botón "Agregar"
        self.ui.pushButton_2.clicked.connect(self.guardar_y_cerrar)  # Botón "Guardar"

    def cargar_materias(self):  # Carga materias del horario del usuario
        if not self.parent_window or not getattr(self.parent_window, "usuario_actual", None):
            # nada que cargar si no hay usuario
            return
        usuario = self.parent_window.cargar_datos_usuario()  # Carga JSON
        if usuario:
            # materias se sacan del horario del usuario
            self.materias = [h.get("materia") for h in usuario.get("horarios", []) if "materia" in h]

        self.ui.comboBox_2.clear()  # Limpia el combo
        self.ui.comboBox_2.addItems(sorted(list(set(self.materias))))  # Agrega materias sin duplicados

    def cargar_tareas(self):  # Carga tareas desde el JSON
        if not self.parent_window or not getattr(self.parent_window, "usuario_actual", None):
            return
        usuario = self.parent_window.cargar_datos_usuario()  # Leer JSON
        if usuario:
            self.tareas_pendientes = usuario.get("tareas", [])  # Lista de tareas guardadas

    def agregar_tarea(self):  # Crea una nueva tarea
        materia = self.ui.comboBox_2.currentText().strip()  # Materia escrita/seleccionada
        descripcion = self.ui.textEdit.toPlainText().strip()  # Texto de descripción
        fecha_entrega_qdate = self.ui.dateEdit.date()  # Fecha desde UI
        fecha_entrega_str = fecha_entrega_qdate.toString("yyyy-MM-dd")  # Formato para guardar

        if not materia or not descripcion:  # Validación mínima
            QMessageBox.warning(self, "Datos incompletos", "Debe ingresar una materia y una descripción.")
            return

        nueva_tarea = {  # Tarea a guardar en memoria
            "materia": materia,
            "descripcion": descripcion,
            "fecha_entrega": fecha_entrega_str,
            "completada": False  # Siempre empieza sin completar
        }

        self.tareas_pendientes.append(nueva_tarea)  # Se agrega a la lista

        QMessageBox.information(self, "Agregado", "Tarea agregada. Presione 'Guardar' para confirmar.")  # Aviso

        self.ui.textEdit.clear()  # Limpia campos
        self.ui.dateEdit.setDate(QDate.currentDate())  # Restablece fecha a hoy
        self.ui.comboBox_2.setFocus()  # Vuelve a enfocar materia

    def guardar_y_cerrar(self):  # Guarda en JSON y cierra
        if not self.parent_window or not getattr(self.parent_window, "usuario_actual", None):
            return
        usuario = self.parent_window.cargar_datos_usuario()  # Cargar JSON
        if usuario is not None:
            usuario["tareas"] = self.tareas_pendientes  # Sobrescribe lista tareas
            self.parent_window.guardar_datos_usuario(usuario)  # Guardar

        QMessageBox.information(self, "Guardado", "Tareas guardadas correctamente.")  # Aviso
        self.accept()  # Cerrar ventana


# -----------------------------------------------------------------
# --- CLASE MODIFICADA: VentanaAgendarLibros ---
# -----------------------------------------------------------------
class VentanaAgendarLibros(QDialog):  # Ventana para agregar materiales/libros
    def __init__(self, parent=None):  # Constructor
        super().__init__(parent)
        self.parent = parent  # MainWindow
        self.ui = Ui_AgendarMaterial()  # Interfaz .ui correspondiente
        self.ui.setupUi(self)
        # El título lo toma del .ui ("Agregar Material")
        self.setWindowTitle("Agendar Material")

        self.materias = []  # Lista de materias para seleccionar
        self.lista_materiales = []  # Lista interna de materiales a guardar

        # Cargar datos desde el usuario actual (si existe)
        self.cargar_materias()  # Materias del usuario
        self.cargar_materiales()  # Materiales ya guardados

        # Configurar widgets
        self.ui.comboBox_2.setEditable(True)  # Permite escribir materias nuevas

        # Conectar botones (según el .ui)
        self.ui.pushButton.clicked.connect(self.agregar_material)  # Botón “Agregar”
        self.ui.pushButton_2.clicked.connect(self.guardar_y_cerrar)  # Botón “Guardar”

    def cargar_materias(self):  # Trae materias desde usuario.json
        """Carga la lista de materias desde el usuario actual (usuarios.json vía parent)."""
        if not self.parent or not getattr(self.parent, "usuario_actual", None):
            self.materias = []
        else:
            usuario = self.parent.cargar_datos_usuario()  # Leer JSON
            if usuario:
                self.materias = usuario.get("materias", [])  # Lista de materias
            else:
                self.materias = []

        # Poblar el combobox
        self.ui.comboBox_2.clear()  # Limpia combo
        self.ui.comboBox_2.addItems(self.materias)  # Agrega materias

    def cargar_materiales(self):  # Lee materiales que ya existan
        if not self.parent or not getattr(self.parent, "usuario_actual", None):
            self.lista_materiales = []
        else:
            usuario = self.parent.cargar_datos_usuario()  # Read JSON
            self.lista_materiales = usuario.get("materiales", [])  # Lista de dicts de materiales

        # Poblar ComboBox con materias que ya están en lista_materiales (si corresponde)
        self.ui.comboBox_2.clear()

        # Si no hay materias cargadas en usuario, mantenemos las del archivo
        if self.materias:
            self.ui.comboBox_2.addItems(self.materias)  # Usa materias normales
        else:
            # Si no hay materias en usuario, intenta usarlas del material guardado
            self.ui.comboBox_2.addItems([m.get("materia") for m in self.lista_materiales if "materia" in m])

    def agregar_material(self):  # Añade un material nuevo
        """Añade el material a la lista en memoria (self.lista_materiales)"""

        # 1. Obtener datos de la UI
        materia = self.ui.comboBox_2.currentText().strip()  # Materia
        material_desc = self.ui.lineEdit.text().strip()  # Descripción material

        # 2. Validar
        if not materia or not material_desc:
            QMessageBox.warning(self, "Datos incompletos", "Debe ingresar una materia y el material necesario.")
            return

        # 3. Crear el diccionario del material
        nuevo_material = {
            "materia": materia,
            "material": material_desc,
            "conseguido": False  # Estado por defecto
        }

        # 4. Añadir a la lista en memoria
        self.lista_materiales.append(nuevo_material)

        # 5. Notificar y limpiar campos
        QMessageBox.information(
            self, "Agregado",
            f"Material '{material_desc}' agregado para '{materia}'.\n\n"
            "Presione 'Guardar' para aplicar todos los cambios."
        )

        self.ui.lineEdit.clear()  # Limpia input
        self.ui.comboBox_2.setFocus()  # Foco

    def guardar_y_cerrar(self):  # Guarda en JSON y cierra ventana
        if not self.parent or not getattr(self.parent, "usuario_actual", None):  # Verifica usuario
            QMessageBox.warning(self, "Error", "No hay usuario cargado para guardar materiales.")
            return

        usuario = self.parent.cargar_datos_usuario()  # Cargar JSON
        if usuario is None:
            QMessageBox.warning(self, "Error", "No existe usuario cargado.")
            return

        usuario["materiales"] = self.lista_materiales  # Guarda lista final
        self.parent.guardar_datos_usuario(usuario)  # Escribe JSON
        QMessageBox.information(self, "Guardado", "Materiales guardados correctamente.")  # Aviso
        self.accept()  # Cerrar


# -----------------------------
# CLASE PRINCIPAL
# -----------------------------
class MainWindow(QMainWindow):  # Definimos la ventana principal heredando de QMainWindow
    def __init__(self):  # Constructor de la clase
        super().__init__()  # Llama al constructor de QMainWindow
        self.ui = Ui_MainWindow()  # Crea el objeto de la interfaz generada por Qt Designer
        self.ui.setupUi(self)  # Carga la interfaz dentro de esta ventana
        self.setWindowTitle("Agenda Digital")  # Cambia el título de la ventana
        self.usuario_actual = None  # Variable para guardar el usuario logueado
        self.habilitar_funciones(False)  # Deshabilita botones protegidos hasta iniciar sesión

        # --- CONEXIÓN ARDUINO ---
        self.arduino = None  # Variable donde guardaremos el objeto serial si se conecta
        self.conectar_arduino()  # Intento automático de conexión al Arduino
        # ------------------------

        # Conectar botones a funciones (pasamos self como parent donde corresponda)
        self.ui.pushButton_8.clicked.connect(self.abrir_registrarse)  # Botón Registrarse
        self.ui.pushButton_7.clicked.connect(self.abrir_iniciar_sesion)  # Botón Iniciar sesión
        
        # MODIFICADO: Ahora conectan a las funciones PROTEGIDAS
        self.ui.pushButton_6.clicked.connect(self.abrir_mostrar_horario)  # Mostrar horario (requiere login)
        self.ui.pushButton_4.clicked.connect(lambda: self.abrir_ventana_protegida(self.abrir_editar_horario))  # Editar horario protegido
        self.ui.pushButton_3.clicked.connect(lambda: self.abrir_ventana_protegida(self.abrir_agendar_tareas))  # Agendar tareas protegido
        self.ui.pushButton_5.clicked.connect(lambda: self.abrir_ventana_protegida(self.abrir_agendar_libros))  # Agendar materiales protegido

    def conectar_arduino(self):  # Intenta detectar y conectar el Arduino por puerto serie
        """Intenta conectar automáticamente con el Arduino"""
        try:
            # Busca puertos disponibles
            puertos = serial.tools.list_ports.comports()  # Lista todos los puertos COM disponibles
            for puerto in puertos:  # Recorre cada puerto encontrado
                # Ajusta esto si tu Arduino tiene otro nombre, pero suele detectar USB
                if "Arduino" in puerto.description or "CH340" in puerto.description or "USB" in puerto.description:
                    self.arduino = serial.Serial(puerto.device, 9600, timeout=0.1)  # Abre conexión serial
                    time.sleep(2) # Esperar a que resetee el Arduino al conectarse
                    print(f"Conectado a {puerto.device}")  # Mensaje de éxito
                    break  # Sale del bucle si ya conectó
            
            if not self.arduino:  # Si no se conectó ningún Arduino
                print("No se encontró Arduino. Funcionará en modo simulación (o fallará si es estricto).")
        except Exception as e:  # Captura cualquier error de conexión
            print(f"Error al conectar Arduino: {e}")

    def abrir_ventana_protegida(self, funcion_abrir_ventana):  # Función para bloquear acceso hasta OK del Arduino
        """
        Esta función bloquea el acceso hasta que Arduino da el OK.
        """
        # 1. Verificar si hay usuario (lógica original)
        if not self.usuario_actual:  # Si no hay usuario logueado
            QMessageBox.warning(self, "Error", "Debes iniciar sesión primero para cargar tus datos.")
            return  # Cancela la acción

        # 2. Si no hay arduino conectado, avisamos (o dejamos pasar si es test)
        if not self.arduino:  # Si no existe conexión con Arduino
            QMessageBox.warning(self, "Error de Hardware", "Arduino no detectado. Revisa la conexión USB.")
            return

        # 3. Enviar señal de BLOQUEO al Arduino (para que muestre 'No tienes acceso')
        try:
            self.arduino.write(b'B') # 'B' de Bloqueado — Arduino lo usa para mostrar mensaje
        except:
            pass  # Si falla, lo ignoramos

        # 4. Crear un diálogo modal que dice "Esperando acceso..."
        dialogo = QProgressDialog("Esperando acceso del Arduino...\nPresiona el botón físico.", "Cancelar", 0, 0, self)
        dialogo.setWindowTitle("Acceso Bloqueado")  # Título del cuadro
        dialogo.setWindowModality(Qt.WindowModal)  # Bloquea toda la ventana
        dialogo.setCancelButton(None) # Oculta botón cancelar — obliga a usar el botón físico
        dialogo.show()  # Muestra el cuadro

        acceso_concedido = False  # Bandera que indica si Arduino permite el acceso

        # 5. Bucle de espera (Polling)
        while dialogo.isVisible():  # Mientras siga abierto
            QApplication.processEvents() # Mantiene viva la interfaz mientras esperamos
            
            try:
                if self.arduino.in_waiting > 0:  # Si Arduino envió datos
                    linea = self.arduino.readline().decode().strip()  # Lee la línea enviada
                    if linea == "1":  # "1" = acceso permitido
                        acceso_concedido = True
                        dialogo.close()  # Cierra el cuadro
                        break  # Sale del bucle
            except Exception as e:
                print(f"Error leyendo Arduino: {e}")
                break  # Sale si hay error
        
        # 6. Si se concedió acceso, abrimos la ventana
        if acceso_concedido:
            # Ejecutamos la función original (ej: abrir_mostrar_horario)
            funcion_abrir_ventana()  # Llama a la función que se quería ejecutar
            
            # AL CERRAR LA VENTANA (cuando funcion_abrir_ventana termine su .exec())
            # Enviamos señal para volver a poner "No tienes acceso" en el LCD
            try:
                self.arduino.write(b'L') # 'L' para resetear mensaje a bloqueado
            except:
                pass
        else:
            # Si cerraron el diálogo o falló
            try:
                self.arduino.write(b'L')  # Asegura que el LCD vuelva al mensaje bloqueado
            except:
                pass

    # -------------------------
    # FUNCIONES DE APERTURA
    # -------------------------
    @Slot()  # Marca este método como una "slot" de Qt
    def abrir_editar_horario(self):
        ventana = VentanaEditarHorario(self)  # Crea la ventana hija
        ventana.exec()  # Abre la ventana en modo modal
    # al cerrar, se bloquea automáticamente porque Arduino no vuelve a mandar "1"

    @Slot()
    def abrir_mostrar_horario(self):
        ventana = VentanaMostrarHorario(self)  # Ventana para ver horario
        ventana.exec()

    @Slot()
    def abrir_agendar_tareas(self):
        ventana = VentanaAgendarTarea(self)  # Ventana para añadir tareas
        ventana.exec()

    @Slot()
    def abrir_agendar_libros(self):
        ventana = VentanaAgendarLibros(self)  # Ventana para materiales/libros
        ventana.exec()

    def cargar_datos_usuario(self):
        """Carga los datos completos del usuario actual desde usuarios.json"""
        archivo = os.path.join(os.path.dirname(__file__), "usuarios.json")  # Ruta al archivo JSON
        if not os.path.exists(archivo):  # Si no existe, no hay nada que cargar
            return None

        try:
            with open(archivo, "r", encoding="utf-8") as f:  # Abre el archivo en modo lectura
                usuarios = json.load(f)  # Carga todos los usuarios
        except json.JSONDecodeError:  # Si el archivo está dañado o vacío
            usuarios = []

        for u in usuarios:  # Recorre cada usuario guardado
            if u.get("nombre") == (self.usuario_actual and self.usuario_actual.get("nombre")):
                # Aseguramos que existan las claves importantes aunque estén vacías
                u.setdefault("tareas", [])
                u.setdefault("materiales", [])
                u.setdefault("horarios", [])
                u.setdefault("materias", [])
                return u  # Devuelve el usuario encontrado

        return None  # Si no encuentra usuario, devuelve None

    def guardar_datos_usuario(self, datos_actualizados):
        """Guarda los cambios del usuario actual dentro de usuarios.json"""
        archivo = os.path.join(os.path.dirname(__file__), "usuarios.json")  # Ruta del archivo
        if os.path.exists(archivo):
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    usuarios = json.load(f)  # Carga usuarios existentes
            except json.JSONDecodeError:
                usuarios = []  # Archivo inválido → lista vacía
        else:
            usuarios = []  # Si no existe, empezamos de cero

        # Reemplazar usuario actual por nombre (si existe) o agregar
        reemplazado = False  # Indica si ya reemplazamos al usuario
        for i, u in enumerate(usuarios):
            if u.get("nombre") == (self.usuario_actual and self.usuario_actual.get("nombre")):
                usuarios[i] = datos_actualizados  # Sobrescribe usuario
                reemplazado = True
                break

        if not reemplazado:  # Si no lo encontró, lo agrega
            usuarios.append(datos_actualizados)

        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(usuarios, f, indent=4, ensure_ascii=False)  # Guarda todo en JSON formateado
        except IOError as e:
            QMessageBox.critical(self, "Error al Guardar", f"No se pudo escribir en usuarios.json:\n{e}")
    @Slot()  # Decorador para indicar que este método es un slot de Qt
    def mostrar_comunicado_recordatorios(self):
        if not self.usuario_actual:  # Si no hay usuario logueado, no se muestra nada
            return  # Salimos directamente

        # Cargar datos del usuario actual desde usuarios.json
        datos_usuario = self.cargar_datos_usuario()  # Llama a la función que devuelve los datos del usuario
        if not datos_usuario:  # Si no hay datos
            QMessageBox.information(self, "Recordatorio", "No hay datos para mostrar.")  # Aviso
            return

        tareas = datos_usuario.get("tareas", [])  # Obtiene la lista de tareas guardadas
        materiales = datos_usuario.get("materiales", [])  # Obtiene los materiales guardados

        texto = "📘 Recordatorio personal\n\n"  # Empieza a armar el texto del mensaje

        # Tareas
        mañana = date.today() + timedelta(days=1)  # Calcula la fecha de mañana
        mañana_str = mañana.strftime("%Y-%m-%d")  # Convierte mañana a formato YYYY-MM-DD

        tareas_manana = [t for t in tareas if t.get('fecha_entrega') == mañana_str]  
        # Filtra solo las tareas cuya fecha de entrega coincide con mañana

        if tareas_manana:  # Si hay tareas para mañana
            texto += "📚 Tareas para mañana:\n"
            for t in tareas_manana:  # Las recorre y las agrega al texto
                texto += f"- {t['materia']}: {t['descripcion']} — entrega: {t['fecha_entrega']}\n"
        else:
            texto += "No tenés tareas para mañana.\n"

        mañana = date.today() + timedelta(days=1)  # Vuelve a calcular mañana (innecesario pero válido)
        dia_semana = mañana.strftime("%A")  # Obtiene el nombre del día en inglés

        traduc = {  # Diccionario para traducir días al español
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miercoles",
            "Thursday": "Jueves",
            "Friday": "Viernes"
        }

        dia_manana = traduc.get(dia_semana, None)  # Traduce el día a español

        # Materiales pendientes
        # Materias que tenés mañana
        materias_manana = [
            h["materia"]
            for h in datos_usuario.get("horarios", [])  # Recorre los horarios del usuario
            if h.get("dia") == dia_manana  # Solo las materias del día siguiente
        ]

        # Materiales para mañana
        materiales_manana = [
            m for m in materiales
            if not m.get("conseguido") and m.get("materia") in materias_manana
            # Filtra materiales no conseguidos y que correspondan a materias del día siguiente
        ]

        texto += "\n📆 Material necesario para mañana:\n"
        if materiales_manana:  # Si hay materiales que llevar
            for m in materiales_manana:
                texto += f"- Llevar {m['material']} para {m['materia']}\n"
        else:
            texto += "No necesitás llevar nada mañana.\n"

        # Mostrar mensaje final
        msg = QMessageBox()  # Crea un mensaje emergente
        msg.setWindowTitle("Recordatorio")  # Título
        msg.setText(texto)  # Texto completo
        msg.exec()  # Lo muestra

    def habilitar_funciones(self, estado):
        self.ui.pushButton_6.setEnabled(estado)  # Habilita o deshabilita botón Mostrar horario
        self.ui.pushButton_4.setEnabled(estado)  # Habilita o deshabilita Editar horario
        self.ui.pushButton_3.setEnabled(estado)  # Habilita o deshabilita Agendar tarea/examen
        self.ui.pushButton_5.setEnabled(estado)  # Habilita o deshabilita Agendar material

    @Slot()
    def abrir_registrarse(self):
        ventana = VentanaRegistrarse(self)  # Abre la ventana de registro
        if ventana.exec():  # Si el registro/inicio se realizó correctamente
            # ventana.usuario_actual viene del diálogo; asignamos como usuario actual
            self.usuario_actual = ventana.usuario_actual  # Guarda el usuario que inició sesión
            self.habilitar_funciones(True)  # Activa los botones del menú
            # Mostrar recordatorio inmediatamente después de iniciar sesión
            self.mostrar_comunicado_recordatorios()
        else:
            self.habilitar_funciones(False)  # Si se canceló, deshabilita todo

    @Slot()
    def abrir_iniciar_sesion(self):
        ventana = VentanaIniciarSesion(self)  # Crea ventana de iniciar sesión
        ventana.exec()  # Ejecuta de forma modal

if __name__ == "__main__":  # Punto de entrada del programa
    app = QApplication(sys.argv)  # Crea la aplicación Qt
    window = MainWindow()  # Crea la ventana principal
    window.show()  # La muestra en pantalla
    sys.exit(app.exec())  # Ejecuta el loop principal de eventos de Qt
