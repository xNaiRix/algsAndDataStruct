# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerRcHPsc.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(539, 408)
        self.sumButton = QPushButton(Dialog)
        self.sumButton.setObjectName(u"sumButton")
        self.sumButton.setGeometry(QRect(370, 130, 91, 31))
        self.multyButton = QPushButton(Dialog)
        self.multyButton.setObjectName(u"multyButton")
        self.multyButton.setGeometry(QRect(370, 190, 91, 31))
        self.FirstNumber = QLineEdit(Dialog)
        self.FirstNumber.setObjectName(u"FirstNumber")
        self.FirstNumber.setGeometry(QRect(100, 130, 61, 21))
        self.SecondNumber = QLineEdit(Dialog)
        self.SecondNumber.setObjectName(u"SecondNumber")
        self.SecondNumber.setGeometry(QRect(230, 130, 61, 21))
        self.instructLabel = QLineEdit(Dialog)
        self.instructLabel.setObjectName(u"instructLabel")
        self.instructLabel.setGeometry(QRect(120, 80, 113, 21))
        self.instructLabel.setReadOnly(True)
        self.result = QLineEdit(Dialog)
        self.result.setObjectName(u"result")
        self.result.setGeometry(QRect(160, 180, 131, 21))
        self.result.setReadOnly(True)
        self.differenceButton = QPushButton(Dialog)
        self.differenceButton.setObjectName(u"differenceButton")
        self.differenceButton.setGeometry(QRect(370, 160, 91, 31))
        self.divButton = QPushButton(Dialog)
        self.divButton.setObjectName(u"divButton")
        self.divButton.setGeometry(QRect(370, 220, 91, 31))
        self.intDivButton = QPushButton(Dialog)
        self.intDivButton.setObjectName(u"intDivButton")
        self.intDivButton.setGeometry(QRect(340, 250, 161, 51))
        self.remButton = QPushButton(Dialog)
        self.remButton.setObjectName(u"remButton")
        self.remButton.setGeometry(QRect(370, 300, 91, 31))
        self.answerLabel = QLineEdit(Dialog)
        self.answerLabel.setObjectName(u"answerLabel")
        self.answerLabel.setGeometry(QRect(100, 180, 51, 21))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.sumButton.setText(QCoreApplication.translate("Dialog", u"\u0421\u043b\u043e\u0436\u0435\u043d\u0438\u0442\u044c", None))
        self.multyButton.setText(QCoreApplication.translate("Dialog", u"\u0423\u043c\u043d\u043e\u0436\u0438\u0442\u044c", None))
        self.instructLabel.setText(QCoreApplication.translate("Dialog", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 2 \u0447\u0438\u0441\u043b\u0430", None))
        self.differenceButton.setText(QCoreApplication.translate("Dialog", u"\u0412\u044b\u0447\u0435\u0441\u0442\u044c", None))
        self.divButton.setText(QCoreApplication.translate("Dialog", u"\u041f\u043e\u0434\u0435\u043b\u0438\u0442\u044c", None))
        self.intDivButton.setText(QCoreApplication.translate("Dialog", u"\u0426\u0435\u043b\u043e\u0447\u0438\u0441\u043b\u0435\u043d\u043d\u043e \u043f\u043e\u0434\u0435\u043b\u0438\u0442\u044c", None))
        self.remButton.setText(QCoreApplication.translate("Dialog", u"\u041e\u0441\u0442\u0430\u0442\u043e\u043a", None))
        self.answerLabel.setText(QCoreApplication.translate("Dialog", u"\u041e\u0442\u0432\u0435\u0442", None))
    # retranslateUi

