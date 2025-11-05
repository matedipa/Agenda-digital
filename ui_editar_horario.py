# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edicion_horariomsmWpI.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QPushButton,
    QSizePolicy, QTimeEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(397, 300)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 382, 43))
        font = QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.comboBox = QComboBox(Form)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(130, 50, 80, 24))
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 80, 382, 43))
        font1 = QFont()
        font1.setPointSize(9)
        self.label_2.setFont(font1)
        self.label_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 40, 382, 43))
        self.label_3.setFont(font1)
        self.label_3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.timeEdit = QTimeEdit(Form)
        self.timeEdit.setObjectName(u"timeEdit")
        self.timeEdit.setGeometry(QRect(120, 130, 118, 23))
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(0, 120, 382, 43))
        self.label_4.setFont(font1)
        self.label_4.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.timeEdit_2 = QTimeEdit(Form)
        self.timeEdit_2.setObjectName(u"timeEdit_2")
        self.timeEdit_2.setGeometry(QRect(120, 170, 118, 23))
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(0, 160, 382, 43))
        self.label_5.setFont(font1)
        self.label_5.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(140, 220, 79, 24))
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(140, 260, 79, 24))
        self.comboBox_2 = QComboBox(Form)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(120, 90, 111, 24))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Edicion Horario", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"Lunes", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Form", u"Martes", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Form", u"Miercoles", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Form", u"Jueves", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Form", u"Viernes", None))

        self.label_2.setText(QCoreApplication.translate("Form", u"Ingresar Materia:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Seleccionar D\u00eda:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Ingresar Hora Inicio:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Ingresar Hora Fin:", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Agregar", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Guardar", None))
    # retranslateUi

