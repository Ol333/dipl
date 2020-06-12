# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'output.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_out(object):
    def setupUi(self, Form_out):
        Form_out.setObjectName("Form_out")
        Form_out.resize(710, 521)
        self.textEdit = QtWidgets.QTextEdit(Form_out)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 691, 501))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Form_out)
        QtCore.QMetaObject.connectSlotsByName(Form_out)

    def retranslateUi(self, Form_out):
        _translate = QtCore.QCoreApplication.translate
        Form_out.setWindowTitle(_translate("Form_out", "Output"))

