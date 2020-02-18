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
        Form_param.resize(401, 310)
        self.scrollArea = QtWidgets.QScrollArea(Form_param)
        self.scrollArea.setGeometry(QtCore.QRect(10, 30, 381, 201))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 379, 199))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label = QtWidgets.QLabel(Form_param)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form_param)
        self.label_2.setGeometry(QtCore.QRect(220, 10, 64, 17))
        self.label_2.setObjectName("label_2")
        self.buttonBox = QtWidgets.QDialogButtonBox(Form_param)
        self.buttonBox.setGeometry(QtCore.QRect(120, 280, 166, 25))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_3 = QtWidgets.QLabel(Form_param)
        self.label_3.setGeometry(QtCore.QRect(10, 230, 381, 41))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_7 = QtWidgets.QLabel(Form_param)
        self.label_7.setGeometry(QtCore.QRect(340, 10, 41, 17))
        self.label_7.setObjectName("label_7")

        self.retranslateUi(Form_param)
        QtCore.QMetaObject.connectSlotsByName(Form_param)

    def retranslateUi(self, Form_param):
        _translate = QtCore.QCoreApplication.translate
        Form_param.setWindowTitle(_translate("Form_param", "Parameters"))
        self.label.setText(_translate("Form_param", "Parameter"))
        self.label_2.setText(_translate("Form_param", "value"))
        self.label_3.setText(_translate("Form_param", "if the parameter you need is not displayed \n"
"please contact the author\n"
"check group field for parameter\'s value combination"))
        self.label_7.setText(_translate("Form_param", "group"))

