# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'iniciar-sesionMJnaeF.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

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
        self.label_3.setGeometry(QRect(0, 50, 382, 43))
        font1 = QFont()
        font1.setPointSize(9)
        self.label_3.setFont(font1)
        self.label_3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(0, 90, 382, 43))
        self.label_4.setFont(font1)
        self.label_4.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(0, 130, 382, 43))
        self.label_5.setFont(font1)
        self.label_5.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(140, 210, 79, 24))
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(130, 60, 113, 21))
        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(130, 100, 113, 21))
        self.lineEdit_3 = QLineEdit(Form)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(130, 150, 113, 21))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Registrarse", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Nombre:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Gmail:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Contrase\u00f1a:", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Guardar", None))
    # retranslateUi

