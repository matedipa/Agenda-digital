# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'registrarseWavzad.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

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
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 50, 111, 43))
        font1 = QFont()
        font1.setPointSize(9)
        self.label_3.setFont(font1)
        self.label_3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.comboBox = QComboBox(Form)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(160, 60, 80, 24))
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(0, 120, 111, 43))
        self.label_4.setFont(font1)
        self.label_4.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(140, 130, 113, 21))
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(160, 200, 79, 24))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Iniciar Sesion", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Seleccionar Usuario:", None))
        self.comboBox.setItemText(0, "")
        self.comboBox.setItemText(1, "")
        self.comboBox.setItemText(2, "")
        self.comboBox.setItemText(3, "")
        self.comboBox.setItemText(4, "")

        self.label_4.setText(QCoreApplication.translate("Form", u"Contrase\u00f1a:", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Continuar", None))
    # retranslateUi

