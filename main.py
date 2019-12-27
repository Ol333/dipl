#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
QGridLayout, QInputDialog, QApplication, QMessageBox,
QGroupBox, QScrollArea, QLabel, QHBoxLayout, QMainWindow)
import subprocess
from ui import Ui_Form
from param import Ui_Form_param
from PyQt5.QtCore import (QRect, QCoreApplication,pyqtSignal, QObject)
import os

class Example(Ui_Form, QObject, Ui_Form_param, object):
    numb = 1
    lay = QGridLayout()
    # labellist = QGridLayout()
    grid = []
    f = None
    base_addr = None
    curInd = None

    def __init__(self, form1, com, form2, ui):
        super().__init__()
        self.window_param = form2
        self.ui_param = ui
        self.comm = com
        self.setupUi(form1)
        self.connect_slots()
        self.f = form1
        self.base_addr = os.getcwd()
        # self.labellist.addWidget(QLabel("№"),0,0,1,1)
        # self.labellist.addWidget(QLabel("Parameters \n(for lab_1:\n x1 x2 x3 \nepsilon)"),0,1,1,1)
        # self.labellist.addWidget(QLabel(""),0,2,1,1)
        # self.labellist.addWidget(QLabel("prog's or \nfolder's name"),0,3,1,1)
        # self.labellist.addWidget(QLabel("number \nof launchs"),0,4,1,1)
        # self.labellist.addWidget(QLabel("names of \nresalts for \nfuture \nmodules"),0,5,1,1)
        # self.labellist.addWidget(QLabel(""),0,6,1,1)
        # self.scrollArea_2.setLayout(self.labellist)


        self.grid.append([QLabel(str(self.numb)),QLineEdit(),
        QPushButton("Add parameters"),QLineEdit(),QLineEdit(),QLineEdit()])
        self.grid[0][2].clicked.connect(self.buttonClicked_adp)
        self.grid[0][2].setObjectName("adp0")
        self.grid[0][1].textChanged.connect(self.tChang)
        self.grid[0][2].hide()
        self.grid[0][1].setObjectName("prNam0")
        for i in range(5):
            self.lay.addWidget(self.grid[0][i],0,i,1,1)
        self.lay.addWidget(self.grid[0][5],0,5,1,2)
        self.scrollAreaWidgetContents.setLayout(self.lay)
        self.numb += 1

    def connect_slots(self):
        self.pushButton.clicked.connect(self.execute)
        self.pushButton_2.clicked.connect(self.buttonClicked_2)
        self.comm.fillParam.connect(self.fillParamLineEdit)

    def execute(self):
        mes = QMessageBox()
        re = ""
        for i in range(len(self.grid)):
            proj_name = self.grid[i][1].text()
            path = self.base_addr
            path = os.path.join(path,"programs")
            path = os.path.join(path,proj_name)
            os.chdir(path)        # меняем директорию
            if os.path.exists('makefile'):
                re += "\n №" + str(i)
                re += str(subprocess.run('make'))+"\n"
                re += str(subprocess.run("./" + proj_name))+"\n"
            else:
                re += "\n №" + str(i)
                ar = ['python3',self.grid[i][1].text()+'.py']
                ar.extend(self.grid[i][3].text().split(' '))
                print(ar)
                re += str(subprocess.run(ar))+"\n"

        mes.setText(str(re))
        mes.exec_()

    def buttonClicked_del(self):
        mb = QMessageBox()
        ind = int(str(self.f.sender().objectName())[3:])
        mb.setText("del "+str(ind))
        mb.exec()
        for i in range(len(self.grid[ind])):
            # print(self.lay.itemAtPosition(ind,i).widget())
            # self.lay.removeWidget(i)
            self.lay.itemAtPosition(ind,i).widget().hide()
            # i.deleteLater()
        # self.grid.remove(self.grid[ind])
        # self.numb -= 1
        # for i in range(len(self.grid)):
        #     self.grid[i][0] = i
        #     print(self.lay.itemAtPosition(i,0))
        #     self.lay.itemAtPosition(i,0).widget().setText(str(i+1))
        #     self.lay.itemAtPosition(i,2).widget().setObjectName("adp"+str(i))
        #     if i != 0:
        #         self.lay.itemAtPosition(i,6).widget().setObjectName("del"+str(i))


    def buttonClicked_adp(self):
        mb = QMessageBox()
        ind = int(str(self.f.sender().objectName())[3:])
        self.curInd = ind
        proj_name = self.grid[ind][1].text()
        path = self.base_addr
        path = os.path.join(path,"programs")
        path = os.path.join(path,proj_name)
        os.chdir(path)                                      # меняем директорию
        if os.path.exists('makefile'):
            path = os.path.join(path,"makefile")
            f = open(path)
            outText = []
            for line in f:
                if line.find("=") != -1:
                    line = line.split(' ')
                    outText.append(line[0])
                else:
                    break
            self.window_param.show()
            self.ui_param.set_param(outText)
        else:
            mb.setText("Можете ввести вручную в блоке правее, вы же их и так наверное знаете :)")
            mb.exec()

    def tChang(self):
        ind = int(str(self.f.sender().objectName())[5:])
        proj_name = self.grid[ind][1].text()
        path = self.base_addr
        path = os.path.join(path,"programs")
        path = os.path.join(path,proj_name)
        if os.path.exists(path):
            self.grid[ind][2].show()
        else:
            self.grid[ind][2].hide()

    def fillParamLineEdit(self):
        self.grid[self.curInd][3].setText(' '.join(self.ui_param.return_outMas()))

    def buttonClicked_2(self):
        self.grid.append([QLabel(str(self.numb)),QLineEdit(),
        QPushButton("Add parameters"),QLineEdit(),QLineEdit(),
        QLineEdit(),QPushButton("Delete")])
        self.grid[self.numb-1][2].clicked.connect(self.buttonClicked_adp)
        self.grid[self.numb-1][6].clicked.connect(self.buttonClicked_del)
        self.grid[self.numb-1][1].textChanged.connect(self.tChang)
        self.grid[self.numb-1][2].setObjectName("adp"+str(self.numb-1))
        self.grid[self.numb-1][6].setObjectName("btn"+str(self.numb-1))
        self.grid[self.numb-1][1].setObjectName("prNam"+str(self.numb-1))
        self.grid[self.numb-1][2].hide()
        for i in range(7):
            self.lay.addWidget(self.grid[self.numb-1][i],self.numb-1,i,1,1)

        self.numb += 1
        self.scrollAreaWidgetContents.setLayout(self.lay)

class Param(Ui_Form_param, QObject):
    def __init__(self, form, com):
        super().__init__()
        self.window = form
        self.comm = com
        self.setupUi(form)
        self.connect_slots()

    def connect_slots(self):
        self.buttonBox.accepted.connect(self.buttonClicked_accept)
        self.buttonBox.rejected.connect(self.buttonClicked_reject)

    def buttonClicked_accept(self):
        self.outMas = []
        for i in range(len(self.mas)):
            self.outMas.append(self.mas[i][1].text())
        self.window.hide()
        self.comm.fillParam.emit()

    def return_outMas(self):
        return self.outMas

    def buttonClicked_reject(self):
        self.window.hide()

    def set_param(self, list_param):
        self.mas = []
        lay = QGridLayout()
        for i in range(len(list_param)):
            self.mas.append([QLabel(list_param[i]),QLineEdit()])
            lay.addWidget(self.mas[i][0],i,0,1,1)
            lay.addWidget(self.mas[i][1],i,1,1,1)
        self.scrollAreaWidgetContents.setLayout(lay)

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
