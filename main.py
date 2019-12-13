#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
QGridLayout, QInputDialog, QApplication, QMessageBox,
QGroupBox, QScrollArea, QLabel, QHBoxLayout,QMainWindow)
import subprocess
from ui1 import Ui_Form
from PyQt5.QtCore import (QRect, QCoreApplication)
import os

class Example(Ui_Form):
    numb = 1
    lay = QGridLayout()
    labellist = []
    combolist = []
    grid = []

    def __init__(self, form):
        super().__init__()
        self.setupUi(form)
        self.connect_slots()

        self.grid.append((QLabel("№ "+str(self.numb)),QLineEdit(),
        QPushButton("Add parameters"),QLineEdit(),QLineEdit(),QLineEdit()))
        self.grid[0][2].clicked.connect(self.buttonClicked_adp)
        for i in range(5):
            self.lay.addWidget(self.grid[0][i],0,i,1,1)
        self.lay.addWidget(self.grid[0][5],0,5,1,2)
        self.scrollAreaWidgetContents.setLayout(self.lay)
        self.numb += 1

    def connect_slots(self):
        self.pushButton.clicked.connect(self.buttonClicked)
        self.pushButton_2.clicked.connect(self.buttonClicked_2)

    def buttonClicked(self):
        base_addr = os.getcwd()
        mes = QMessageBox()
        re = ""
        for i in range(len(self.grid)):
            proj_name = self.grid[i][3].text()
            path = base_addr
            path = os.path.join(path,"programs")
            path = os.path.join(path,proj_name)
            os.chdir(path)        # меняем директорию
            if os.path.exists('makefile'):
                re += "\n №" + str(i)
                re += str(subprocess.run('make'))+"\n"
                re += str(subprocess.run("./" + proj_name))+"\n"
            else:
                re += "\n №" + str(i)
                ar = ['python3', self.grid[i][3].text()+'.py']
                ar.extend(self.grid[i][1].text().split(' '))
                re += str(subprocess.run(ar))+"\n"

        mes.setText(str(re))
        mes.exec_()

    def buttonClicked_del(self):
        mb = QMessageBox()
        mb.setText("del")#+str(self.sender()))
        mb.exec()

    def buttonClicked_adp(self):
        mb = QMessageBox()
        mb.setText("adp")
        mb.exec()

    def buttonClicked_2(self):
        self.grid.append((QLabel("№ "+str(self.numb)),QLineEdit(),
        QPushButton("Add parameters"),QLineEdit(),QLineEdit(),
        QLineEdit(),QPushButton("Delete")))
        self.grid[self.numb-1][2].clicked.connect(self.buttonClicked_adp)
        self.grid[self.numb-1][6].clicked.connect(self.buttonClicked_del)
        for i in range(7):
            self.lay.addWidget(self.grid[self.numb-1][i],self.numb-1,i,1,1)

        self.numb += 1
        self.scrollAreaWidgetContents.setLayout(self.lay)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    ui = Example(window)
    window.show()
    # ex = Example()
    sys.exit(app.exec_())
