# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'param.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_param(object):
    def setupUi(self, Form_param):
        Form_param.setObjectName("Form_param")
        Form_param.resize(429, 408)
        Form_param.setAutoFillBackground(True)
        Form_param.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.scrollArea = QtWidgets.QScrollArea(Form_param)
        self.scrollArea.setGeometry(QtCore.QRect(10, 50, 411, 221))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 409, 219))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label = QtWidgets.QLabel(Form_param)
        self.label.setGeometry(QtCore.QRect(10, 20, 81, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form_param)
        self.label_2.setGeometry(QtCore.QRect(170, 20, 64, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form_param)
        self.label_3.setGeometry(QtCore.QRect(10, 270, 411, 101))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_7 = QtWidgets.QLabel(Form_param)
        self.label_7.setGeometry(QtCore.QRect(270, 10, 71, 41))
        self.label_7.setObjectName("label_7")
        self.label_4 = QtWidgets.QLabel(Form_param)
        self.label_4.setGeometry(QtCore.QRect(340, 10, 81, 41))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(Form_param)
        self.pushButton.setGeometry(QtCore.QRect(240, 370, 83, 25))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(252, 175, 62))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 175, 62))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 175, 62))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.pushButton.setPalette(palette)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form_param)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 370, 83, 25))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(252, 175, 62))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 175, 62))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 175, 62))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.pushButton_2.setPalette(palette)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Form_param)
        QtCore.QMetaObject.connectSlotsByName(Form_param)

    def retranslateUi(self, Form_param):
        _translate = QtCore.QCoreApplication.translate
        Form_param.setWindowTitle(_translate("Form_param", "Parameters"))
        self.label.setText(_translate("Form_param", "Parameter"))
        self.label_2.setText(_translate("Form_param", "Value"))
        self.label_3.setText(_translate("Form_param", "if the parameter you need is not displayed please contact the author\n"
"check \'group\' field for parameter\'s value combination\n"
"check \'one by one\' field for searching parameter\'s value one by one"))
        self.label_7.setText(_translate("Form_param", "Group"))
        self.label_4.setText(_translate("Form_param", "One \n"
"by\n"
" one"))
        self.pushButton.setText(_translate("Form_param", "Cancel"))
        self.pushButton_2.setText(_translate("Form_param", "OK"))

