#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
QGridLayout, QInputDialog, QApplication, QMessageBox, QTextEdit,
QGroupBox, QScrollArea, QLabel, QHBoxLayout, QMainWindow,
QAction, QFileDialog)
import subprocess
from ui import Ui_MainWindow
from param import Ui_Form_param
from output import Ui_Form_out
from PyQt5.QtCore import (QRect, QCoreApplication,pyqtSignal, QObject, Qt)
from PyQt5.QtGui import QStandardItemModel,QStandardItem
import os
import fileinput
import shutil
import glob
import rab_with_db as rwd


class Example(Ui_MainWindow, QObject, Ui_Form_param, Ui_Form_out, object):
    numb = 0
    lay = QGridLayout()
    gridElementOfInput = []
    base_addr = None
    curInd = None

    def __init__(self, form1, com, form2, ui, form3, ui3):
        super().__init__()
        self.window_param = form2
        self.ui_param = ui
        self.comm = com
        self.setupUi(form1)
        self.connect_slots()
        self.form = form1
        self.window_output = form3
        self.ui_output = ui3
        self.base_addr = os.getcwd()

        self.buttonClicked_addModule()
        self.scrollAreaWidgetContents.setLayout(self.lay)
        self.scrollArea.setAlignment(Qt.AlignBottom)

        self.fill_tree()

    def showDialog_createProject(self):
        qwe1 = QWidget()
        text1, ok1 = QInputDialog.getText(qwe1, 'new project',
            'enter new project name:')
        if ok1:
            path = QFileDialog.getExistingDirectory(self.form, 'Choose directory of project (press Enter)', self.base_addr)
            if path:
                self.label_6.setText(f"project name: {text1}")
                # for somethinf in path add modules

    def delete_and_create_db_tables(self):
        rwd.delete_db_tables()
        rwd.create_db_tables()
        self.fill_tree()

    def connect_slots(self):
        self.pushButton.clicked.connect(self.execute)
        self.pushButton_2.clicked.connect(self.buttonClicked_addModule)
        self.comm.fillParam.connect(self.fillParamLineEdit)
        self.actionNew_project.triggered.connect(self.showDialog_createProject)
        self.actionDelete_db_and_create_new.triggered.connect(self.delete_and_create_db_tables)

    def set_and_safe_one_modul_params(self,i,file_name,path):
        # изменить док
        counter = 0
        masChange = self.gridElementOfInput[i][3].toPlainText().split('\n')
        for j in range(len(masChange)):
            masChange[j] = masChange[j].split('>')

        path = os.path.join(path,file_name)
        shutil.copyfile(path, path + '.bak')
        f = open(path,"r")
        s = ""
        mas_paramValue = []
        for line in f:
            s += line.replace(masChange[counter][0].strip(), masChange[counter][1].strip())
            if counter+1 != len(masChange):
                mas_paramValue.append(masChange[counter][1].strip())
                counter += 1
        f.close()
        f = open(path,"w")
        f.write(s)
        f.close()
        return mas_paramValue

    def execute(self):
        if self.label_6.text() == "project name: ...---...":
            self.showDialog_createProject()
        modules_paramValueRes = []

        re = ""
        list_modules = []
        for i in range(len(self.gridElementOfInput)):
            if self.gridElementOfInput[i][2].isEnabled():
                module_name = self.gridElementOfInput[i][1].text()
                path = self.base_addr
                path = os.path.join(path,"programs",module_name)
                modules_paramValueRes.append([module_name,path,[]])
                os.chdir(path)                                   # меняем директорию
                list_modules.append(path)
                if os.path.exists('makefile'):
                    modules_paramValueRes[-1][-1].extend(self.set_and_safe_one_modul_params(i,"makefile",path))
                    # запустить
                    re += "\n №" + str(i)
                    for j in range(int(self.gridElementOfInput[i][4].text())):
                        loc_re = ""
                        some_str = subprocess.check_output('make',stderr=subprocess.STDOUT)
                        some_str = some_str.decode()
                        loc_re += some_str
                        some_str = subprocess.check_output("./" + module_name,stderr=subprocess.STDOUT)
                        some_str = some_str.decode()
                        loc_re += some_str
                        modules_paramValueRes[-1].append(loc_re)
                        re += "\n №№" + str(j)+' '+loc_re
                    self.del_bak_file()
                elif os.path.exists("parameters"):
                    modules_paramValueRes[-1][-1].extend(self.set_and_safe_one_modul_params(i,"parameters",path))
                    re += "\n №" + str(i)
                    for j in range(int(self.gridElementOfInput[i][4].text())):
                        loc_re = ""
                        ar = ['python3',self.gridElementOfInput[i][1].text()+'.py']
                        loc_re += str(subprocess.run(ar))
                        # some_str = subprocess.check_output(ar,stderr=subprocess.STDOUT)
                        # some_str = some_str.decode()
                        # print(some_str,"@@@@@")
                        # loc_re += some_str+"\n"
                        modules_paramValueRes[-1].append(loc_re)
                        re += "\n №№" + str(j)+' '+loc_re
                    self.del_bak_file()
                else:
                    re += "\n №" + str(i)
                    for j in range(int(self.gridElementOfInput[i][4].text())):
                        loc_re = ""
                        ar = ['python3',self.gridElementOfInput[i][1].text()+'.py']
                        ar.extend(self.gridElementOfInput[i][3].toPlainText().split(' '))
                        loc_re += str(subprocess.run(ar))
                        modules_paramValueRes[-1].append(loc_re)
                        re += "\n №№" + str(j)+' '+loc_re

        self.ui_output.setText(str(re))
        self.window_output.show()

        # db project modules parametres values results
        rwd.add_([self.label_6.text().split(":")[1].strip(),self.base_addr],modules_paramValueRes)

        self.fill_tree()

    def del_bak_file(self):
        for file in glob.glob("*.bak"):
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
            path = os.path.join(path,"makefile")
            f = open(path)
            outText = []
            for line in f:
                if line.find("=") != -1:
                    line = line.split('=')
                    # if line[0][:2]=="V_":
                    outText.append([line[0].strip(),line[1].strip()])
            self.window_param.show()
            self.ui_param.set_param(outText)
            f.close()
        else:
            if os.path.exists('parameters'):
                path = os.path.join(path,"parameters")
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
                mb.setText("¯\_(&)_/¯")
                mb.exec()

    def textLineEditChange(self):
        ind = int(str(self.form.sender().objectName())[5:])
        module_name = self.gridElementOfInput[ind][1].text()
        path = self.base_addr
        path = os.path.join(path,"programs",module_name)
        if os.path.exists(path) and module_name != "":
            self.gridElementOfInput[ind][2].setEnabled(True)
            self.gridElementOfInput[ind][3].setEnabled(True)
            self.gridElementOfInput[ind][4].setEnabled(True)
        else:
            self.gridElementOfInput[ind][2].setEnabled(False)
            self.gridElementOfInput[ind][3].setEnabled(False)
            self.gridElementOfInput[ind][4].setEnabled(False)

    def fillParamLineEdit(self):
        self.gridElementOfInput[self.curInd][3].clear()
        mas = self.ui_param.return_outMas()
        for i in mas:
            self.gridElementOfInput[self.curInd][3].append(i[0] + ' > ' + i[1])
        self.gridElementOfInput[self.curInd][3].setReadOnly(True)

    def buttonClicked_addModule(self):
        self.gridElementOfInput.append([QLabel(str(self.numb + 1)),QLineEdit(),
                                        QPushButton("Add parameters"),QTextEdit(),QLineEdit(),
                                        QLineEdit(),QPushButton("Delete")])
        self.gridElementOfInput[self.numb][2].clicked.connect(self.buttonClicked_adp)
        self.gridElementOfInput[self.numb][6].clicked.connect(self.buttonClicked_del)
        self.gridElementOfInput[self.numb][1].textChanged.connect(self.textLineEditChange)
        self.gridElementOfInput[self.numb][2].setObjectName("adp"+str(self.numb))
        self.gridElementOfInput[self.numb][6].setObjectName("btn"+str(self.numb))
        self.gridElementOfInput[self.numb][1].setObjectName("prNam"+str(self.numb))
        self.gridElementOfInput[self.numb][4].setText("1")
        self.gridElementOfInput[self.numb][2].setEnabled(False)
        self.gridElementOfInput[self.numb][3].setEnabled(False)
        self.gridElementOfInput[self.numb][4].setEnabled(False)
        self.gridElementOfInput[self.numb][5].setEnabled(False)
        for i in range(7):
            self.lay.addWidget(self.gridElementOfInput[self.numb][i],self.numb,i,1,1)
        self.numb += 1

    def fill_tree(self):
        model = QStandardItemModel(0, 6, None)
        # model.setHorizontalHeaderLabels(['','id', 'name','path/value','date','time'])
        model.setHeaderData(0, Qt.Horizontal, "")
        model.setHeaderData(1, Qt.Horizontal, "id")
        model.setHeaderData(2, Qt.Horizontal, "name")
        model.setHeaderData(3, Qt.Horizontal, "path/value")
        model.setHeaderData(4, Qt.Horizontal, "date")
        model.setHeaderData(5, Qt.Horizontal, "time")

        self.treeView.setModel(model)
        self.treeView.setColumnHidden(1,True)
        self.treeView.setColumnWidth(0,200)


        root = model.invisibleRootItem()

        parent = root

        proj = rwd.get_table("project")
        for pr in proj:
            old_parent_pr = parent
            parent.appendRow([QStandardItem("project:"),QStandardItem(str(pr[0])),QStandardItem(str(pr[1])),
                            QStandardItem(str(pr[2])),QStandardItem(), QStandardItem()])
            parent = parent.child(parent.rowCount() - 1)

            res = rwd.get_table_by_id("result","Project_id",pr[0])
            for r in res:
                old_parent_res = parent
                parent.appendRow([QStandardItem("result:"),QStandardItem(str(r[0])),QStandardItem(), QStandardItem(str(r[1])),
                                QStandardItem(str(r[4])),QStandardItem(str(r[5]))])
                # r[0]
                parent = parent.child(parent.rowCount() - 1)
                mod = rwd.get_table_by_id("module","Project_id",pr[0])
                for m in mod:
                    old_parent_mod = parent
                    appRow_wait = [QStandardItem("module:"),QStandardItem(str(m[0])),QStandardItem(str(m[1])),
                                    QStandardItem(str(m[2])),QStandardItem(), QStandardItem()]
                    # parent.appendRow([QStandardItem("module:"),QStandardItem(str(m[0])),QStandardItem(str(m[1])),
                    #                 QStandardItem(str(m[2])),QStandardItem(), QStandardItem()])
                    param = rwd.get_table_by_id("parameter","Module_id",m[0])
                    # parent = parent.child(parent.rowCount() - 1)
                    for p in param:
                        val = rwd.get_value(p[0],r[0])
                        if val != None:
                            if appRow_wait:
                                parent.appendRow(appRow_wait)
                                appRow_wait = None
                                parent = parent.child(parent.rowCount() - 1)
                            parent.appendRow([QStandardItem("parameter value:"),QStandardItem(str(p[0])),QStandardItem(str(p[2])),
                                            QStandardItem(str(val[2])),QStandardItem(), QStandardItem()])
                            # p[1]

                    parent = old_parent_mod
                parent = old_parent_res
            parent = old_parent_pr

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

class Output(Ui_Form_out):
    def __init__(self, form):
        super().__init__()
        self.window = form
        self.setupUi(form)

    def setText(self,text):
        self.textEdit.clear()
        self.textEdit.append(text)

class Communicate(QObject):
    fillParam = pyqtSignal()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    com = Communicate()

    window = QMainWindow()
    window_param = QWidget()
    window_output = QWidget()
    ui_output = Output(window_output)
    ui_param = Param(window_param, com)
    ui = Example(window, com, window_param, ui_param, window_output, ui_output)
    window.show()

    sys.exit(app.exec_())
