#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
QGridLayout, QInputDialog, QApplication, QMessageBox, QTextEdit,
QGroupBox, QScrollArea, QLabel, QHBoxLayout, QMainWindow)
import subprocess
from ui import Ui_Form
from param import Ui_Form_param
from PyQt5.QtCore import (QRect, QCoreApplication,pyqtSignal, QObject, Qt)
import os
import fileinput
import shutil
import glob

class Example(Ui_Form, QObject, Ui_Form_param, object):
    numb = 1
    lay = QGridLayout()
    gridElementOfInput = []
    base_addr = None
    curInd = None

    def __init__(self, form1, com, form2, ui):
        super().__init__()
        self.window_param = form2
        self.ui_param = ui
        self.comm = com
        self.setupUi(form1)
        self.connect_slots()
        self.form = form1
        self.base_addr = os.getcwd()

        self.gridElementOfInput.append([QLabel(str(self.numb)),QLineEdit(),
        QPushButton("Add parameters"),QTextEdit(),QLineEdit(),QLineEdit()])
        self.gridElementOfInput[0][2].clicked.connect(self.buttonClicked_adp)
        self.gridElementOfInput[0][2].setObjectName("adp0")
        self.gridElementOfInput[0][1].textChanged.connect(self.textLineEditChange)
        self.gridElementOfInput[0][2].setEnabled(False)
        self.gridElementOfInput[0][3].setEnabled(False)
        self.gridElementOfInput[0][4].setEnabled(False)
        self.gridElementOfInput[0][5].setEnabled(False)
        self.gridElementOfInput[0][1].setObjectName("prNam0")
        for i in range(5):
            self.lay.addWidget(self.gridElementOfInput[0][i],0,i,1,1)
        self.lay.addWidget(self.gridElementOfInput[0][5],0,5,1,2)
        self.scrollAreaWidgetContents.setLayout(self.lay)
        self.scrollArea.setAlignment(Qt.AlignBottom)
        self.numb += 1

    def connect_slots(self):
        self.pushButton.clicked.connect(self.execute)
        self.pushButton_2.clicked.connect(self.buttonClicked_addModule)
        self.comm.fillParam.connect(self.fillParamLineEdit)

    def execute(self):
        mes = QMessageBox()
        re = ""
        for i in range(len(self.gridElementOfInput)):
            if self.gridElementOfInput[i][2].isEnabled():
                module_name = self.gridElementOfInput[i][1].text()
                path = self.base_addr
                path = os.path.join(path,"programs",module_name)
                os.chdir(path)                                   # меняем директорию
                if os.path.exists('makefile'):
                    # изменить док
                    counter = 0
                    masChange = self.gridElementOfInput[i][3].toPlainText().split('\n')
                    for j in range(len(masChange)):
                        masChange[j] = masChange[j].split('>')

                    if os.path.exists('makefile.bak'):
                        path = os.path.join(path,"makefile.bak")
                        s = ""
                        f = open(path,"r")
                        for line in f:
                            s += line.replace(masChange[counter][0].strip(), masChange[counter][1].strip())
                            if counter+1 != len(masChange):
                                counter += 1
                        f.close()
                        f = open(path[:-4],"w")
                        f.write(s)
                        f.close()
                    else:
                        path = os.path.join(path,"makefile")
                        shutil.copyfile(path, path + '.bak')
                        s = ""
                        f = open(path,"r")
                        for line in f:
                            s += line.replace(masChange[counter][0].strip(), masChange[counter][1].strip())
                            if counter+1 != len(masChange):
                                counter += 1
                        f.close()
                        f = open(path,"w")
                        f.write(s)
                        f.close()

                    # запустить
                    re += "\n №" + str(i)
                    re += str(subprocess.run('make'))+"\n"
                    re += str(subprocess.run("./" + module_name))+"\n"
                else:
                    re += "\n №" + str(i)
                    ar = ['python3',self.gridElementOfInput[i][1].text()+'.py']
                    ar.extend(self.gridElementOfInput[i][3].toPlainText().split(' '))
                    re += str(subprocess.run(ar))+"\n"

        mes.setText(str(re))
        mes.exec_()
        # #удалять все .bak
        for file in glob.glob("*.bak"):
            print(file)
            src = file
            dst = file[:-4]
            shutil.copyfile(src, dst)
            os.remove(file)

    def buttonClicked_del(self):
        mb = QMessageBox()
        ind = int(str(self.form.sender().objectName())[3:])
        mb.setText("del "+str(ind))
        mb.exec()
        for i in range(len(self.gridElementOfInput[ind])):
            # print(self.lay.itemAtPosition(ind,i).widget())
            # self.lay.removeWidget(i)
            self.lay.itemAtPosition(ind,i).widget().hide()
            # i.deleteLater()
        # self.gridElementOfInput.remove(self.gridElementOfInput[ind])
        # self.numb -= 1
        # for i in range(len(self.gridElementOfInput)):
        #     self.gridElementOfInput[i][0] = i
        #     print(self.lay.itemAtPosition(i,0))
        #     self.lay.itemAtPosition(i,0).widget().setText(str(i+1))
        #     self.lay.itemAtPosition(i,2).widget().setObjectName("adp"+str(i))
        #     if i != 0:
        #         self.lay.itemAtPosition(i,6).widget().setObjectName("del"+str(i))


    def buttonClicked_adp(self):
        mb = QMessageBox()
        self.curInd = int(str(self.form.sender().objectName())[3:])
        module_name = self.gridElementOfInput[self.curInd][1].text()
        path = self.base_addr
        path = os.path.join(path,"programs",module_name)
        os.chdir(path)                                      # меняем директорию
        if os.path.exists('makefile'):
            if os.path.exists('makefile.bak'):
                path = os.path.join(path,"makefile.bak")
            else:
                path = os.path.join(path,"makefile")
            f = open(path)
            outText = []
            for line in f:
                if line.find("=") != -1:
                    line = line.split('=')
                    outText.append([line[0].strip(),line[1].strip()])
            self.window_param.show()
            self.ui_param.set_param(outText)
            f.close()
        else:
            mb.setText("(for lab_1: x1 x2 x3 epsilon)")
            mb.exec()

    def textLineEditChange(self):
        ind = int(str(self.form.sender().objectName())[5:])
        module_name = self.gridElementOfInput[ind][1].text()
        path = self.base_addr
        path = os.path.join(path,"programs",module_name)
        if os.path.exists(path):
            self.gridElementOfInput[ind][2].setEnabled(True)
            self.gridElementOfInput[ind][3].setEnabled(True)
        else:
            self.gridElementOfInput[ind][2].setEnabled(False)
            self.gridElementOfInput[ind][3].setEnabled(False)

    def fillParamLineEdit(self):
        self.gridElementOfInput[self.curInd][3].clear()
        mas = self.ui_param.return_outMas()
        for i in mas:
            self.gridElementOfInput[self.curInd][3].append(i[0] + ' > ' + i[1])

    def buttonClicked_addModule(self):
        self.gridElementOfInput.append([QLabel(str(self.numb)),QLineEdit(),
        QPushButton("Add parameters"),QTextEdit(),QLineEdit(),
        QLineEdit(),QPushButton("Delete")])
        self.gridElementOfInput[self.numb-1][2].clicked.connect(self.buttonClicked_adp)
        self.gridElementOfInput[self.numb-1][6].clicked.connect(self.buttonClicked_del)
        self.gridElementOfInput[self.numb-1][1].textChanged.connect(self.textLineEditChange)
        self.gridElementOfInput[self.numb-1][2].setObjectName("adp"+str(self.numb-1))
        self.gridElementOfInput[self.numb-1][6].setObjectName("btn"+str(self.numb-1))
        self.gridElementOfInput[self.numb-1][1].setObjectName("prNam"+str(self.numb-1))
        self.gridElementOfInput[self.numb-1][2].setEnabled(False)
        self.gridElementOfInput[self.numb-1][3].setEnabled(False)
        self.gridElementOfInput[self.numb-1][4].setEnabled(False)
        self.gridElementOfInput[self.numb-1][5].setEnabled(False)
        for i in range(7):
            self.lay.addWidget(self.gridElementOfInput[self.numb-1][i],self.numb-1,i,1,1)
        self.numb += 1

class Param(Ui_Form_param, QObject):
    def __init__(self, form, com):
        super().__init__()
        self.window = form
        self.comm = com
        self.setupUi(form)
        self.connect_slots()
        self.lay = QGridLayout()
        self.scrollAreaWidgetContents.setLayout(self.lay)

    def connect_slots(self):
        self.buttonBox.accepted.connect(self.buttonClicked_accept)
        self.buttonBox.rejected.connect(self.buttonClicked_reject)

    def buttonClicked_accept(self):
        for i in range(len(self.mas)):
            self.outMas[i].append(self.mas[i][0].text() + ' = ' + self.mas[i][1].text())
        self.window.hide()
        self.comm.fillParam.emit()

    def return_outMas(self):
        return self.outMas

    def buttonClicked_reject(self):
        self.window.hide()

    def set_param(self, list_param):
        self.mas = []

        for i in range(self.lay.count()):
            self.lay.itemAt(i).widget().close()

        for i in range(len(list_param)):
            self.mas.append([QLabel(list_param[i][0]),QLineEdit()])
            self.lay.addWidget(self.mas[i][0],i,0,1,1)
            self.lay.addWidget(self.mas[i][1],i,1,1,1)
            self.mas[i][1].setText(list_param[i][1])
        self.outMas = list(map(lambda x: [x[0] + ' = ' + x[1]], list_param))

class Communicate(QObject):
    fillParam = pyqtSignal()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    com = Communicate()

    window = QWidget()
    window_param = QWidget()
    ui_param = Param(window_param, com)
    ui = Example(window, com, window_param, ui_param)
    window.show()


    sys.exit(app.exec_())
