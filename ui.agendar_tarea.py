# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'agendar_tareavxlJKQ.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QLabel,
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 382, 43))
        font = QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.comboBox_2 = QComboBox(Form)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(130, 60, 111, 24))
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 50, 382, 43))
        font1 = QFont()
        font1.setPointSize(9)
        self.label_2.setFont(font1)
        self.label_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.textEdit = QTextEdit(Form)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(130, 90, 111, 64))
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 80, 382, 43))
        self.label_3.setFont(font1)
        self.label_3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.dateEdit = QDateEdit(Form)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setGeometry(QRect(130, 160, 116, 23))
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(0, 150, 382, 43))
        self.label_4.setFont(font1)
        self.label_4.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(140, 200, 79, 24))
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(140, 240, 79, 24))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Agendar Tareas", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Ingresar Materia:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Descripcion Trabajo:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Ingrese Fecha Entrega:", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"Agregar", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Guardar", None))
    # retranslateUi

