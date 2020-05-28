#!/usr/bin/env python3
import sys
import os
import subprocess
import fileinput
from datetime import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QCheckBox,
QGridLayout, QInputDialog, QApplication, QMessageBox, QTextEdit, QRadioButton,
QGroupBox, QScrollArea, QLabel, QHBoxLayout, QMainWindow,
QAction, QFileDialog)
from PyQt5.QtCore import (QRect, QCoreApplication,pyqtSignal, QObject, Qt)
from PyQt5.QtGui import QStandardItemModel,QStandardItem

from ui import Ui_MainWindow
from param import Ui_Form_param
from output import Ui_Form_out
import rab_with_db
import logic as lgc

class Example(Ui_MainWindow, QObject, Ui_Form_param, Ui_Form_out, object):
    numb = 0
    lay = QGridLayout()
    gridElementOfInput = []
    moduleInfo = lgc.ModuleTime()
    timeResult = lgc.AllTime()
    base_addr = None
    curInd = None

    def __init__(self, form1, com, form2, ui, form3, ui3):
        super().__init__()
        self.window_param = form2
        self.ui_param = ui
        self.comm = com
        self.form = form1
        self.window_output = form3
        self.ui_output = ui3
        self.base_addr = os.getcwd()
        self.setupUi(form1)
        self.connect_slots()

        self.buttonClicked_addModule()
        self.scrollAreaWidgetContents.setLayout(self.lay)
        self.scrollArea.setAlignment(Qt.AlignBottom)
        self.rwd = rab_with_db.DbWork()

    def showDialog_createProject(self):
        qwe1 = QWidget()
        text1, ok1 = QInputDialog.getText(qwe1, 'new project',
            'enter new project name:')
        if ok1:
            path = QFileDialog.getExistingDirectory(self.form,
                'Choose directory of project (press Enter)', self.base_addr)
            if path:
                self.label_6.setText(f"project name: {text1}")
                # for somethinf in path add modules

    def delete_and_create_db_tables(self): # only for development
        self.rwd.delete_db_tables()
        self.rwd.create_db_tables()
        self.fill_tree()

    def connect_slots(self):
        self.pushButton.clicked.connect(self.execute)
        self.pushButton_2.clicked.connect(self.buttonClicked_addModule)
        self.comm.fillParam.connect(self.fillParamLineEdit)
        self.actionNew_project.triggered.connect(self.showDialog_createProject)
        self.actionDelete_db_and_create_new.triggered.connect(self.delete_and_create_db_tables)
        self.pushButton_4.clicked.connect(self.fill_tree)

    def set_and_safe_one_modul_params(self,i,file_name,path):
        # изменить док
        counter = 0
        masChange = self.gridElementOfInput[i][3].toPlainText().split('\n')
        masChange = list(map(lambda x: x.strip(),masChange))

        f = open(os.path.join(path,file_name),"r")
        s = ""
        mas_paramValue = []
        for line in f:
            self.timeResult.const_rand_flags_test(masChange[counter],
                                                  os.path.split(path)[-1])
            s += line.replace(self.moduleInfo.string_for_replace(i,counter),
                              masChange[counter])
            if counter+1 != len(masChange):
                mas_paramValue.append(masChange[counter].strip())
                counter += 1
        f.close()
        f_new = open(os.path.join(path,"temporary_new_file"),"w")
        f_new.write(s)
        f_new.close()
        return mas_paramValue

    def execute_one_module(self,i,path,module_name):
        if os.path.exists('makefile'):
            return(self.execute_with_makefile(i,path,module_name))
        elif os.path.exists("parameters"):
            return(self.execute_with_parameters(i,path,module_name))
        else:
            return(self.execute_with_python(i,path,module_name))

    def execute_with_makefile(self,i,path,module_name):
        res_list = []
        res_list.extend(self.set_and_safe_one_modul_params(i,"makefile",path))
        # запустить
        re = ''
        re += "\n №" + str(i)
        for j in range(int(self.gridElementOfInput[i][4].text())):
            loc_re = ""
            some_str = subprocess.check_output(['make','-f','temporary_new_file'],
                                                stderr=subprocess.STDOUT)
            some_str = some_str.decode()
            loc_re += some_str
            start_time = datetime.now()
            some_str = subprocess.check_output("./" + module_name,
                                                stderr=subprocess.STDOUT)
            t = datetime.now()-start_time
            self.moduleInfo.test_time_values(i,j,t)
            some_str = some_str.decode()
            loc_re += some_str
            re += "\n №№" + str(j)+' '+loc_re
        os.remove('temporary_new_file')
        return (res_list,re)

    def execute_with_parameters(self,i,path,module_name):
        res_list = []
        res_list.extend(self.set_and_safe_one_modul_params(i,"parameters",path))
        re = ''
        re += "\n №" + str(i)
        for j in range(int(self.gridElementOfInput[i][4].text())):
            loc_re = ""
            ar = ['python3',self.gridElementOfInput[i][1].text()+'.py']
            start_time = datetime.now()
            loc_re += str(subprocess.run(ar))
            t = datetime.now()-start_time
            self.moduleInfo.test_time_values(i,j,t)
            # some_str = subprocess.check_output(ar,stderr=subprocess.STDOUT)
            # some_str = some_str.decode()
            # print(some_str,"@@@@@")
            # loc_re += some_str+"\n"
            re += "\n №№" + str(j)+' '+loc_re
        os.remove('temporary_new_file')
        return (res_list,re)

    def execute_with_python(self,i,path,module_name):
        res_list = []
        re = ''
        re += "\n №" + str(i)
        for j in range(int(self.gridElementOfInput[i][4].text())):
            loc_re = ""
            ar = ['python3',self.gridElementOfInput[i][1].text()+'.py']
            start_time = datetime.now()
            loc_re += str(subprocess.run(ar))
            t = datetime.now()-start_time
            self.moduleInfo.test_time_values(i,j,t)
            ar.extend(self.gridElementOfInput[i][3].toPlainText().split(' '))
            re += "\n №№" + str(j)+' '+loc_re
        return (res_list,re)

    def execute(self):
        if self.label_6.text() == "project name: ...---...":
            self.showDialog_createProject()
        modules_paramValueRes = []
        re = ""
        for i in range(len(self.gridElementOfInput)):
            if self.gridElementOfInput[i][2].isEnabled():
                module_name = self.gridElementOfInput[i][1].text()
                self.timeResult.module_name_exist(module_name)

                path = self.base_addr
                path = os.path.join(path,"programs",module_name)
                modules_paramValueRes.append([module_name,path,[]])
                os.chdir(path)                              # меняем директорию

                res_list,res = self.execute_one_module(i,path,module_name)
                modules_paramValueRes[-1][-1].extend(res_list)
                modules_paramValueRes[-1].append(self.gridElementOfInput[i][0].text())#numb
                modules_paramValueRes[-1].append(self.gridElementOfInput[i][4].text())#count
                re += res
                aver_time = self.moduleInfo.aver_time(i,
                    int(self.gridElementOfInput[i][4].text()))

                re += self.moduleInfo.module_time(i,aver_time)
                self.timeResult.add_time_of_module(module_name,
                                                  (aver_time).total_seconds())
                self.timeResult.test_time_values(module_name,
                                            self.moduleInfo.get_worst_time(i),
                                            aver_time,
                                            self.moduleInfo.get_best_time(i),
                                            i)
        # re += self.timeResult.modules_res()
        # list_of_flags = self.timeResult.list_flags_name(module_name,32)
        # temp_list = list(map(lambda x:str(list_of_flags.index(x)+1)+' '+
        #                                   str(x.split('\n')[1]),
        #                      list_of_flags))
        # re += '\n'.join(temp_list)
        self.ui_output.setText(str(re))
        self.window_output.show()
        #
        #
        # fig = plt.figure()
        # mpl.rcParams.update({'font.size': 10})
        # plt.title('Среднее время выполнения программы')
        #
        # ax = plt.axes()
        # ax.xaxis.grid(True, zorder = 1)
        #
        # tempN = 32
        # col_vo_const_fl = self.timeResult.col_vo_const_fl(module_name,tempN)
        #
        # xs = range(tempN)
        # for i in range(col_vo_const_fl):
        #     plt.barh([x + 0.05 + (0.9 / col_vo_const_fl)*i for x in xs],
        #             self.timeResult.take_list_cut(module_name,tempN,i),
        #             height=(0.9 / col_vo_const_fl),
        #             color=[(0.12*(i%3))/1,(0.12*(i%3+1))/1,(0.12*(i%3+2))/1],
        #             label=self.timeResult.list_for_label(module_name,tempN,i),
        #             zorder=2)
        # plt.yticks(xs,range(1,tempN+1))
        # plt.legend(loc='upper right')
        # plt.show()
        #
        #
        # # save pyplot
        # fig.savefig("res_"+self.label_6.text().split(":")[1].strip()+'.png')
        # save txt
        f_new = open(os.path.join(self.base_addr,"res_"+self.label_6.text().split(":")[1].strip()+'.txt'),"w")
        f_new.write(re)
        f_new.close()
        # db project modules parametres values results(-)
        lgc.add_([self.label_6.text().split(":")[1].strip(),self.base_addr,'png','txt'],modules_paramValueRes,self.rwd)

    def buttonClicked_del(self):  # hide row
        mb = QMessageBox()
        ind = int(str(self.form.sender().objectName())[3:])
        mb.setText("del "+str(ind))
        mb.exec()
        for i in range(len(self.gridElementOfInput[ind])):
            self.gridElementOfInput[ind][i].setEnabled(False)
            self.lay.itemAtPosition(ind,i).widget().hide()

    def take_params_from_file_comment_symbol(self,path,file_name,com_symb):
        path = os.path.join(path,file_name)
        f = open(path)
        outText = []
        for line in f:
            if line.find("=") != -1:
                line = line.split('=',1)
                if line[0].lstrip()[0] != com_symb:
                    outText.append([line[0].strip(),line[1].strip()])
        f.close()
        return outText

    def take_params_from_file(self,index):
        module_name = self.gridElementOfInput[index][1].text()
        path = self.base_addr
        path = os.path.join(path,"programs",module_name)
        os.chdir(path)                                      # меняем директорию
        if os.path.exists('makefile'):
            return self.take_params_from_file_comment_symbol(path,'makefile','#')
        elif os.path.exists('parameters'):
            return self.take_params_from_file_comment_symbol(path,'parameters','#')
        else:
            return "¯\_(&)_/¯"

    def buttonClicked_adp(self):
        self.curInd = int(str(self.form.sender().objectName())[3:])
        outText = self.gridElementOfInput[self.curInd][3].toPlainText().split('\n')
        for j in range(len(outText)):
            outText[j] = outText[j].split('=',1)
            # if len(outText[j] > 2):
            #     outText[j][1] = '='.join(outText[j][1:])
        self.window_param.show()
        self.ui_param.set_param(outText)

    def textLineEditChange(self):
        ind = int(str(self.form.sender().objectName())[5:])
        module_name = self.gridElementOfInput[ind][1].text()
        path = self.base_addr
        path = os.path.join(path,"programs",module_name)
        if os.path.exists(path) and module_name != "":
            self.gridElementOfInput[ind][2].setEnabled(True)
            self.gridElementOfInput[ind][3].setEnabled(True)
            self.gridElementOfInput[ind][4].setEnabled(True)
            textParam = self.take_params_from_file(ind)
            self.moduleInfo.set_orig_param(ind,textParam)
            self.gridElementOfInput[ind][3].clear()
            for i in textParam:
                self.gridElementOfInput[ind][3].append(i[0]+' = '+i[1])
            self.gridElementOfInput[ind][3].setReadOnly(True)
        else:
            self.gridElementOfInput[ind][2].setEnabled(False)
            self.gridElementOfInput[ind][3].setEnabled(False)
            self.gridElementOfInput[ind][4].setEnabled(False)

    def fillParamLineEdit(self):
        self.gridElementOfInput[self.curInd][3].clear()
        mas = self.ui_param.return_outMas()
        for i in mas[2]:
            self.gridElementOfInput[self.curInd][3].append(i)

        if mas[0][0] == 'someone want a combination':
            for k in range(1 if len(mas[1][1])==0 else len(mas[1][1][0]['param'])+1): #перебор по одному
                numbFl = len(mas[1][0])
                for i in range(2**numbFl): #перебор всех возможных комбинаций
                    self.buttonClicked_addModule()
                    self.gridElementOfInput[self.numb-1][1].setText(self.gridElementOfInput[self.curInd][1].text())
                    self.gridElementOfInput[self.numb-1][4].setText(self.gridElementOfInput[self.curInd][4].text())
                    strings = self.gridElementOfInput[self.curInd][3].toPlainText().split('\n')
                    for numb in mas[0][1]:
                        temp = strings[numb].split('=',1)
                        temp[1] = ''
                        strings[numb] = '='.join(temp)
                    if len(mas[1][1]) != 0:
                        temp = strings[mas[1][1][0]['number']].split('=',2)
                        if k<len(mas[1][1][0]['param']):
                            temp[2] = mas[1][1][0]['param'][k]
                            strings[mas[1][1][0]['number']] = '='.join(temp)
                        else:
                            strings[mas[1][1][0]['number']] = temp[0] + '='
                    for j in range(numbFl):
                        if i&(0b1 << j):
                            temp = strings[mas[1][0][j]['number']].split('=',1)
                            temp[1] += mas[1][0][j]['param'] + ' '
                            strings[mas[1][0][j]['number']] = '='.join(temp)
                    self.gridElementOfInput[self.numb-1][3].clear()
                    for i in strings:
                        self.gridElementOfInput[self.numb-1][3].append(i.strip())
            for i in range(len(self.gridElementOfInput[self.curInd])):
                self.gridElementOfInput[self.curInd][i].setEnabled(False)
                self.lay.itemAtPosition(self.curInd,i).widget().hide()

    def buttonClicked_addModule(self):
        self.gridElementOfInput.append([QLabel(str(self.numb)), QLineEdit(),
                                        QPushButton("Change \nparameters"),
                                        QTextEdit(), QLineEdit(), QLineEdit(),
                                        QPushButton("Delete")])
        self.moduleInfo.add_module()
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
        self.gridElementOfInput[self.numb][3].setReadOnly(True)
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

        # proj = self.rwd.get_table("project")
        # for pr in proj:
        #     old_parent_pr = parent
        #     parent.appendRow([QStandardItem("project:"),QStandardItem(str(pr[0])),QStandardItem(str(pr[1])),
        #                     QStandardItem(str(pr[2])),QStandardItem(), QStandardItem()])
        #     parent = parent.child(parent.rowCount() - 1)
        #
        #     res = self.rwd.get_table_by_id("result","Project_id",pr[0])
        #     for r in res:
        #         old_parent_res = parent
        #         parent.appendRow([QStandardItem("result:"),QStandardItem(str(r[0])),QStandardItem(), QStandardItem(str(r[1])),
        #                         QStandardItem(str(r[4])),QStandardItem(str(r[5]))])
        #         # r[0]
        #         parent = parent.child(parent.rowCount() - 1)
        #         mod = self.rwd.get_table_by_id("module","Project_id",pr[0])
        #         for m in mod:
        #             old_parent_mod = parent
        #             appRow_wait = [QStandardItem("module:"),QStandardItem(str(m[0])),QStandardItem(str(m[1])),
        #                             QStandardItem(str(m[2])),QStandardItem(), QStandardItem()]
        #             # parent.appendRow([QStandardItem("module:"),QStandardItem(str(m[0])),QStandardItem(str(m[1])),
        #             #                 QStandardItem(str(m[2])),QStandardItem(), QStandardItem()])
        #             param = self.rwd.get_table_by_id("parameter","Module_id",m[0])
        #             # parent = parent.child(parent.rowCount() - 1)
        #             for p in param:
        #                 val = self.rwd.get_value(p[0],r[0])
        #                 if val != None:
        #                     if appRow_wait:
        #                         parent.appendRow(appRow_wait)
        #                         appRow_wait = None
        #                         parent = parent.child(parent.rowCount() - 1)
        #                     parent.appendRow([QStandardItem("parameter value:"),QStandardItem(str(p[0])),QStandardItem(str(p[2])),
        #                                     QStandardItem(str(val[2])),QStandardItem(), QStandardItem()])
        #                     # p[1]
        #
        #             parent = old_parent_mod
        #         parent = old_parent_res
        #     parent = old_parent_pr

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
        combination = []
        combinationIndex = []
        search_one_by_one = []
        for i in range(len(self.mas)):
            if self.mas[i][3].isChecked():
                tempL = list(self.mas[i][1].text().strip().split('='))
                search_one_by_one.append({'number':i,
                                          'param':tempL[1][1:-1].split(';')})
            if self.mas[i][2].isChecked():
                tempL = list(self.mas[i][1].text().strip().split(' '))
                k = 0
                while k < len(tempL):
                    if tempL[k][0] != '-' and tempL[k][0] != '$':
                        tempL[k-1] += ' ' + tempL[k]
                        tempL.remove(tempL[k])
                    else:
                        k += 1
                for j in tempL:
                    combination.append({'number':i,'param':j})
                    combinationIndex.append(i)
        if len(combination) > 0 or len(search_one_by_one) > 0:
            self.outMas.append(['someone want a combination',combinationIndex])
            self.outMas.append([combination,search_one_by_one])
        else:
            self.outMas.append(['',])
            self.outMas.append(list())
        self.outMas.append(list())

        for i in range(len(self.mas)):
            self.outMas[2].append(self.mas[i][0].text().strip()+' = '+
                                  self.mas[i][1].text().strip())
        self.window.hide()
        self.comm.fillParam.emit() #вызов функции из главного окна

    def return_outMas(self):
        return self.outMas

    def buttonClicked_reject(self):
        self.window.hide()

    def set_param(self, list_param):
        self.mas = []

        for i in range(self.lay.count()):
            self.lay.itemAt(i).widget().close()

        for i in range(len(list_param)):
            self.mas.append([QLabel(list_param[i][0]),QLineEdit(),
                                    QCheckBox(),QRadioButton()])
            self.lay.addWidget(self.mas[i][0],i,0,1,1)
            self.lay.addWidget(self.mas[i][1],i,1,1,1)
            self.lay.addWidget(self.mas[i][2],i,2,1,1)
            self.lay.addWidget(self.mas[i][3],i,3,1,1)
            self.mas[i][1].setText(list_param[i][1])

        self.outMas = list()

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
