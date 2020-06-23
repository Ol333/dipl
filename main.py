#!/usr/bin/env python3
import sys
import os
import subprocess
from datetime import datetime, timedelta
import matplotlib as mpl
import matplotlib.pyplot as plt
import webbrowser
import asyncio
import threading

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QCheckBox,
QGridLayout, QInputDialog, QApplication, QMessageBox, QTextEdit, QRadioButton,
QGroupBox, QScrollArea, QLabel, QHBoxLayout, QMainWindow, QProgressBar,
QAction, QFileDialog, QDialog)
from PyQt5.QtCore import (QRect, QCoreApplication, pyqtSignal, QObject, Qt,
QTranslator, QLocale)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem)

from ui import Ui_MainWindow
from param import Ui_Form_param
import rab_with_db
import logic as lgc
from genetic import Genetic
import bot

class Example(Ui_MainWindow, QObject, Ui_Form_param, object):
    numb = 0
    lay = QGridLayout()
    mas_progress = []
    gridElementOfInput = []
    moduleInfo = lgc.ModuleTime()
    timeResult = lgc.AllTime()
    base_addr = None
    curInd = None
    url_report = None
    ga = None
    cur_mod = ""
    cur_er_count = 0
    time_of_begin = datetime.now()
    bot_com = pyqtSignal()
    exec_mode = 0
    stop_fl = False
    sum_good = 0
    sum_good_i = 0
    sum_er_i = []

    def __init__(self, form1, com, form2, ui, transl, app):
        super().__init__()
        self.window_param = form2
        self.ui_param = ui
        self.comm = com
        self.form = form1
        self.base_addr = os.getcwd()
        self.transl = transl
        self.app = app
        self.setupUi(form1)
        self.window_main = form1
        self.treeView.setModel(QStandardItemModel())
        self.connect_slots()

        self.buttonClicked_addModule()
        self.scrollAreaWidgetContents.setLayout(self.lay)
        self.scrollArea.setAlignment(Qt.AlignBottom)
        self.rwd = rab_with_db.DbWork()

        self.dateTimeEdit_2.setDateTime(datetime.now())
        with open('configure', 'r') as f:
            ar = [row.strip() for row in f]
            if ar[0].split(' ')[1]=='en':
                self.translate()
            if ar[1].split(' ')[2]=='Time':
                print('time')
        self.pushButton_8.setEnabled(False)

    def showDialog_createProject(self):
        qwe1 = QWidget()
        t = QInputDialog()
        t.setOkButtonText(self.tr("OK")) # не работает
        t.setCancelButtonText(self.tr("Cancel")) # не работает
        text1, ok1 = t.getText(qwe1, self.tr('New project'),
            self.tr('Enter new project name:'))
        if ok1:
            if (self.rwd.select_proj_by_name(text1) != None):
                mb = QMessageBox()
                mb.setWindowTitle(self.tr("New project"))
                mb.setText(self.tr("Project already exists."))
                mb.exec()
                self.showDialog_createProject()
            else:
                path = QFileDialog.getExistingDirectory(self.form,
                    self.tr('Choose directory of project (press Enter)'), self.base_addr)
                if path:
                    self.label_5.setText(text1)
                    # for somethinf in path add modules

    def delete_and_create_db_tables(self): # only for development
        self.rwd.delete_db_tables()
        self.rwd.create_db_tables()
        self.fill_tree()

    def translate(self):
        if self.actionTranslate.text() == "Перевести на английский":
            self.transl.load('language_en.qm')
            f = open('configure', 'r')
            lines = f.readlines()
            lines[0] = 'Language en' + '\n'
            f.close()
            save_changes = open('configure', 'w')
            save_changes.writelines(lines)
            save_changes.close()
        else:
            # по какой-то причине, после добавления модуля перестает работать
            self.transl.load('language_ru.qm')
            f = open('configure', 'r')
            lines = f.readlines()
            lines[0] = 'Language ru' + '\n'
            f.close()
            save_changes = open('configure', 'w')
            save_changes.writelines(lines)
            save_changes.close()
        self.app.installTranslator(self.transl)
        self.retranslateUi(self.window_main)
        self.ui_param.retranslateUi(self.window_param)
        for i in self.gridElementOfInput:
            i[2].setText(self.tr("Change \nparameters"))
            i[5].setText(self.tr("Delete"))

    def del_proj(self):
        if self.treeView.selectedIndexes() == []:
            mb = QMessageBox()
            mb.setWindowTitle(self.tr("Delete project"))
            mb.setText(self.tr("None selected."))
            mb.exec()
        elif (str(self.treeView.selectionModel().model().data(self.treeView.selectedIndexes()[0])) != "Project:"
            and str(self.treeView.selectionModel().model().data(self.treeView.selectedIndexes()[0])) != "Проект:"):
            mb = QMessageBox()
            mb.setWindowTitle(self.tr("Delete project"))
            mb.setText(self.tr("Please, selecte project."))
            mb.exec()
        else:
            d = QMessageBox.question(self.form, self.tr("Delete project"),
                                    self.tr("Are you sure?"),
                                    QMessageBox.Yes|QMessageBox.No,
                                    QMessageBox.No)
            if d == QMessageBox.Yes:
                temp = self.treeView.selectionModel().model()
                proj_name = str(temp.data(self.treeView.selectedIndexes()[1]))
                lgc.delete_proj(self.rwd.select_proj_by_name(proj_name)[0],self.rwd)

    def open_proj(self):
        if self.treeView.selectedIndexes() == []:
            mb = QMessageBox()
            mb.setWindowTitle(self.tr("Open project"))
            mb.setText(self.tr("None selected."))
            mb.exec()
        elif str(self.treeView.selectionModel().model().data(self.treeView.selectedIndexes()[0])) != self.tr("Project:"):
            mb = QMessageBox()
            mb.setWindowTitle(self.tr("Open project"))
            mb.setText(self.tr("Please, select project."))
            mb.exec()
        else:
            self.tabWidget.setCurrentIndex(1)
            temp = self.treeView.selectionModel().model()
            proj_name = str(temp.data(self.treeView.selectedIndexes()[1]))
            out = lgc.get_safe_proj(self.rwd.select_proj_by_name(proj_name)[0],self.rwd)
            self.label_5.setText(proj_name)
            for i in range(len(out)):
                if i>=len(self.gridElementOfInput):
                    self.buttonClicked_addModule()
                self.gridElementOfInput[i][0].setText(str(out[i][0]))
                self.gridElementOfInput[i][1].setText(out[i][1])
                self.gridElementOfInput[i][3].clear()
                for s in out[i][2]:
                    self.gridElementOfInput[i][3].append(s)
                self.gridElementOfInput[i][4].setText(str(out[i][3]))
                for j in range(len(self.gridElementOfInput[i])):
                    self.gridElementOfInput[i][j].setEnabled(True)
                    self.lay.itemAtPosition(i,j).widget().show()
            for i in range(len(self.gridElementOfInput)-len(out)):
                self.gridElementOfInput[len(out)+i][5].click()

    def open_mod_res(self):
        if self.treeView.selectedIndexes() == []:
            mb = QMessageBox()
            mb.setWindowTitle(self.tr("Open result"))
            mb.setText(self.tr("None selected."))
            mb.exec()
        elif str(self.treeView.selectionModel().model().data(self.treeView.selectedIndexes()[0])) == self.tr("Module:"):
            temp = self.treeView.selectionModel().model()
            mod_path = str(temp.data(self.treeView.selectedIndexes()[2]))
            self.treeView.setColumnHidden(6,False)
            bind_path = str(temp.data(self.treeView.selectedIndexes()[5]))
            self.treeView.setColumnHidden(6,True)
            path = os.path.join(mod_path,bind_path[2:-2])
            # subprocess.run(["thunar",path])
            subprocess.run(["thunar",os.path.dirname(path)])
        elif str(self.treeView.selectionModel().model().data(self.treeView.selectedIndexes()[0])) == self.tr("Project:"):
            temp = self.treeView.selectionModel().model()
            proj_path = str(temp.data(self.treeView.selectedIndexes()[2]))
            path = os.path.join(proj_path,"result")
            subprocess.run(["thunar",path])
        elif str(self.treeView.selectionModel().model().data(self.treeView.selectedIndexes()[0])) == self.tr("Result:"):
            temp = self.treeView.selectionModel().model()
            res_path = str(temp.data(self.treeView.selectedIndexes()[2]))
            subprocess.run(["thunar",os.path.dirname(res_path)])
        else:
            mb = QMessageBox()
            mb.setWindowTitle(self.tr("Open result"))
            mb.setText(self.tr("Please, selecte module, project or result."))
            mb.exec()

    def about_program(self):
        mb = QMessageBox()
        mb.setWindowTitle(self.tr("About"))
        mb.setText(self.tr("It's program.\nAuthor is O.P.Bobrovskaya."))
        mb.exec()

    def open_diagram(self):
        new = 2
        webbrowser.open(self.url_report,new=new)

    def set_exhaustive_search(self):
        self.actionExhaustive_search.setText(self.tr("Exhaustive search +"))
        self.actionGenetic.setText(self.tr("Genetic"))

    def set_genetic(self):
        self.actionExhaustive_search.setText(self.tr("Exhaustive search"))
        self.actionGenetic.setText(self.tr("Genetic +"))

    def error_ignore_mode(self):
        self.actionError_ignore_mode.setText(self.tr("Error ignore +"))
        self.actionFirst_error_stop.setText(self.tr("First error stop"))
        self.actionModule_skipping_on_first_error.setText(self.tr("Module skipping on first error"))
        self.exec_mode = 0

    def first_error_stop(self):
        self.actionError_ignore_mode.setText(self.tr("Error ignore"))
        self.actionFirst_error_stop.setText(self.tr("First error stop +"))
        self.actionModule_skipping_on_first_error.setText(self.tr("Module skipping on first error"))
        self.exec_mode = 1

    def module_skipping_on_first_error(self):
        self.actionError_ignore_mode.setText(self.tr("Error ignore"))
        self.actionFirst_error_stop.setText(self.tr("First error stop"))
        self.actionModule_skipping_on_first_error.setText(self.tr("Module skipping on first error +"))
        self.exec_mode = 2

    def connect_slots(self):
        self.pushButton.clicked.connect(self.execute)
        self.pushButton_2.clicked.connect(self.buttonClicked_addModule)
        self.comm.fillParam.connect(self.fillParamLineEdit)
        self.actionNew_project.triggered.connect(self.showDialog_createProject)
        self.pushButton_5.clicked.connect(self.showDialog_createProject)
        self.actionDelete_db_and_create_new.triggered.connect(self.delete_and_create_db_tables)
        self.pushButton_4.clicked.connect(self.fill_tree)
        self.actionTranslate.triggered.connect(self.translate)
        self.actionAbout.triggered.connect(self.about_program)
        self.pushButton_3.clicked.connect(self.del_proj)
        self.pushButton_6.clicked.connect(self.open_proj)
        self.pushButton_7.clicked.connect(self.open_mod_res)
        self.pushButton_8.clicked.connect(self.open_diagram)
        self.actionExhaustive_search.triggered.connect(self.set_exhaustive_search)
        self.actionGenetic.triggered.connect(self.set_genetic)
        # self.bot_com.connect(self.send_mes_to_bot)
        self.actionError_ignore_mode.triggered.connect(self.error_ignore_mode)
        self.actionFirst_error_stop.triggered.connect(self.first_error_stop)
        self.actionModule_skipping_on_first_error.triggered.connect(self.module_skipping_on_first_error)
        self.pushButton_10.clicked.connect(self.stop_project)

    def set_and_safe_one_modul_params(self,i,file_name,path):
        # изменить док
        counter = -1
        masChange = self.gridElementOfInput[i][3].toPlainText().split('\n')
        masChange = list(map(lambda x: x.strip(),masChange))

        f = open(os.path.join(path,file_name),"r")
        s = ""
        out_path = ""
        for line in f:
            if counter+1 != len(masChange):
                counter += 1
            self.timeResult.const_rand_flags_test(masChange[counter],
                                                  os.path.split(path)[-1])
            test_s_mas = masChange[counter].split(' ')[0].split('_')
            if test_s_mas[0]+test_s_mas[-1] == "VOUT":
                out_path  = masChange[counter].split(' ')[-1]
            s += line.replace(self.moduleInfo.string_for_replace(i,counter),
                              masChange[counter])
        f.close()
        f_new = open(os.path.join(path,"temporary_new_file"),"w")
        f_new.write(s)
        f_new.close()
        return masChange,out_path

    def execute_one_module(self,i,path,module_name,t):
        if os.path.exists('makefile'):
            return(self.execute_with_makefile(i,path,module_name,t))
        elif os.path.exists("parameters"):
            return(self.execute_with_parameters(i,path,module_name,t))
        else:
            return(self.execute_with_python(i,path,module_name,t))

    def execute_with_makefile(self,i,path,module_name,sum_t):
        res_list = []
        mas, out_path = (self.set_and_safe_one_modul_params(i,"makefile",path))
        res_list.extend(mas)
        # запустить
        re = "\n"+ "### " + self.tr("Module") +" №"+ str(i)
        temp_txt = self.gridElementOfInput[i][3].toPlainText().split('\n')
        temp_txt = list(map(lambda x: "> "+x+'  \n',temp_txt))
        re += '\n' + ''.join(temp_txt) + '\n'
        for j in range(int(self.gridElementOfInput[i][4].text())):
            if not self.stop_fl:
                try:
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
                    temp_mas = loc_re.split('\n')
                    for k in range(len(temp_mas)):
                        temp_mas[k] = ' ' + ("\\" if temp_mas[k].startswith("#") else "") + temp_mas[k]+"  "
                    re += "\n"+ "   " +self.tr("Launch") +" №"+  str(j)+"  \n"+'\n'.join(temp_mas)+ '\n'
                    temp_s = ('№'+str(j)+self.tr(' launch completed successfully. ')
                              + self.tr('Program execution time: ') + str(t))
                    self.textEdit.append(temp_s)
                    sum_t += t
                    self.sum_good_i += 1
                except Exception as e:
                    self.textEdit.append('№'+str(j)+self.tr(' launch. Error: ')+str(e))
                    self.sum_er_i.append('№'+str(j)+self.tr(' launch. Error: ')+str(e))
                    if self.exec_mode == 1:
                        d = QMessageBox.question(self.form, self.tr("Error"),
                                                self.tr("Do you want continue project?"),
                                                QMessageBox.Yes|QMessageBox.No,
                                                QMessageBox.No)
                        if d == QMessageBox.No:
                            self.stop_project()
                    elif self.exec_mode == 2:
                        break
        os.remove('temporary_new_file')
        return (res_list,re,sum_t,out_path)

    def execute_with_parameters(self,i,path,module_name,sum_t):
        res_list = []
        mas, out_path = (self.set_and_safe_one_modul_params(i,"parameters",path))
        res_list.extend(mas)
        re = "\n"+ "### " + self.tr("Module") +" №"+ str(i)
        temp_txt = self.gridElementOfInput[i][3].toPlainText().split('\n')
        temp_txt = list(map(lambda x: "> "+x+'  \n',temp_txt))
        re += '\n' + ''.join(temp_txt) + '\n'
        for j in range(int(self.gridElementOfInput[i][4].text())):
            if not self.stop_fl:
                try:
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
                    temp_mas = loc_re.split('\n')
                    for k in range(len(temp_mas)):
                        temp_mas[k] = ' ' + ("\\" if temp_mas[k].startswith("#") else "") + temp_mas[k]+"  "
                    re += "\n"+ "   " +self.tr("Launch") +" №"+  str(j)+"  \n"+'\n'.join(temp_mas)+ '\n'
                    temp_s = ('№'+str(j) + self.tr(' launch completed successfully. ')
                              + self.tr('Program execution time: ') + str(t))
                    self.textEdit.append(temp_s)
                    sum_t += t
                    self.sum_good_i += 1
                except Exception as e:
                    self.textEdit.append('№'+str(j)+self.tr(' launch. Error: ')+str(e))
                    self.sum_er_i.append('№'+str(j)+self.tr(' launch. Error: ')+str(e))
                    if self.exec_mode == 1:
                        d = QMessageBox.question(self.form, self.tr("Error"),
                                                self.tr("Do you want continue project?"),
                                                QMessageBox.Yes|QMessageBox.No,
                                                QMessageBox.No)
                        if d == QMessageBox.No:
                            self.stop_project()
                    elif self.exec_mode == 2:
                        break
        os.remove('temporary_new_file')
        return (res_list,re,sum_t,out_path)

    def execute_with_python(self,i,path,module_name,sum_t):
        res_list = []
        re = ''
        re = "\n"+ "### " + self.tr("Module") +" №"+ str(i)
        temp_txt = self.gridElementOfInput[i][3].toPlainText().split('\n')
        temp_txt = list(map(lambda x: "> "+x+'  \n',temp_txt))
        re += '\n' + ''.join(temp_txt) + '\n'
        for j in range(int(self.gridElementOfInput[i][4].text())):
            if not self.stop_fl:
                try:
                    loc_re = ""
                    ar = ['python3',self.gridElementOfInput[i][1].text()+'.py']
                    start_time = datetime.now()
                    loc_re += str(subprocess.run(ar))
                    t = datetime.now()-start_time
                    self.moduleInfo.test_time_values(i,j,t)
                    ar.extend(self.gridElementOfInput[i][3].toPlainText().split(' '))
                    temp_mas = loc_re.split('\n')
                    for k in range(len(temp_mas)):
                        temp_mas[k] = ' ' + ("\\" if temp_mas[k].startswith("#") else "") + temp_mas[k]+"  "
                    re += "\n"+ "   " +self.tr("Launch") +" №"+  str(j)+"  \n"+'\n'.join(temp_mas)+ '\n'
                    temp_s = ('№'+str(j)+self.tr(' launch completed successfully. ')
                              + self.tr('Program execution time: ') + str(t))
                    self.textEdit.append(temp_s)
                    sum_t += t
                    self.sum_good_i += 1
                except Exception as e:
                    self.textEdit.append('№'+str(j)+self.tr(' launch. Error: ')+str(e))
                    self.sum_er_i.append('№'+str(j)+self.tr(' launch. Error: ')+str(e))
                    if self.exec_mode == 1:
                        d = QMessageBox.question(self.form, self.tr("Error"),
                                                self.tr("Do you want continue project?"),
                                                QMessageBox.Yes|QMessageBox.No,
                                                QMessageBox.No)
                        if d == QMessageBox.No:
                            self.stop_project()
                    elif self.exec_mode == 2:
                        break
        return (res_list,re,sum_t,"")

    def module_run_inter(self,i,set_of_modules,modules_paramValueRes,re,er_fl,sum_er,sum_t,count_of_execs):
        sum_t_i = timedelta()
        self.sum_er_i.clear()
        self.sum_good_i = 0
        module_name = self.gridElementOfInput[i][1].text().split('/')[-1]
        self.cur_mod = module_name + ' №' + str(i)
        set_of_modules.add(module_name)
        self.textEdit.append('<i>'+self.tr('Module ')+str(i)+'.'
                            +module_name+self.tr(' is begin ')
                            +datetime.now().strftime("%H:%M:%S")+'</i>')
        self.timeResult.module_name_exist(module_name)

        path = self.base_addr
        path = os.path.join(path,"programs",module_name)
        modules_paramValueRes.append([module_name,path,[]])
        os.chdir(path)                              # меняем директорию

        res_list,res,sum_t_i,out_path = self.execute_one_module(i,path,module_name,sum_t_i)
        modules_paramValueRes[-1][-1].extend(res_list)
        modules_paramValueRes[-1].append(out_path)#path
        modules_paramValueRes[-1].append(self.gridElementOfInput[i][0].text())#numb
        modules_paramValueRes[-1].append(self.gridElementOfInput[i][4].text())#count
        re += res
        aver_time = self.moduleInfo.aver_time(i,
                            int(self.gridElementOfInput[i][4].text()))

        re += self.moduleInfo.module_time(i,aver_time)
        self.timeResult.add_time_of_module(module_name,aver_time.total_seconds())
        self.timeResult.test_time_values(module_name,
                                    self.moduleInfo.get_worst_time(i),
                                    aver_time,
                                    self.moduleInfo.get_best_time(i),
                                    i)
        self.textEdit.append('<i>'+self.tr('Module ')+str(i)+'.'
                            +module_name+self.tr(' is finished ')
                            +datetime.now().strftime("%H:%M:%S")+'</i>')

        temp_txt = self.textEdit.toPlainText().split('\n')
        temp_txt = list(map(lambda x: x.strip(),temp_txt))
        self.textEdit.append('<i>'+self.tr('Total module lead time : ')
                            +str(sum_t_i)
                            +self.tr('. Successfully completed launchs: ')
                            +'<b>'+str(self.sum_good_i)
                            +'/'+self.gridElementOfInput[i][4].text()
                            +'</b></i>')
        self.progressBar.setValue(((self.progressBar.value()
                                    /100*count_of_execs
                    + int(self.gridElementOfInput[i][4].text()))
                                                   /count_of_execs)*100)
        sum_t += sum_t_i
        if self.sum_good_i == int(self.gridElementOfInput[i][4].text()):
            self.sum_good += 1
        sum_er.append(list(map(lambda x:'№'+str(i)+self.tr(' module ')+x,self.sum_er_i)))
        self.cur_er_count += len(self.sum_er_i)
        # self.bot_com.emit()
        return set_of_modules,modules_paramValueRes,re,er_fl,sum_er,sum_t,count_of_execs,module_name

    def execute(self):
        while self.label_5.text() == "...---...":
            self.showDialog_createProject()
        self.textEdit.clear()
        self.cur_er_count = 0

        self.thread = bot.BotThread(self)
        self.thread.start()
        # thread.join()

        self.time_of_begin = datetime.now()
        proj_name = self.label_5.text()
        self.tabWidget.setCurrentIndex(0) #выполняет спустя итерацию
        modules_paramValueRes = []
        re = '## <center>' + self.tr("Project ") + proj_name + '</center>'
        count_of_modules = 0
        count_of_execs = 0
        sum_t = timedelta()
        sum_er = []
        set_of_modules = set()
        er_fl = False
        for i in range(len(self.gridElementOfInput)):
            if self.gridElementOfInput[i][2].isEnabled():
                count_of_modules += 1
                count_of_execs += int(self.gridElementOfInput[i][4].text())
        self.textEdit.append('<b>'+self.tr("Project ")+proj_name
              +self.tr(" is begin ")+datetime.now().strftime("%H:%M:%S")+'</b>')

        if self.actionGenetic.text() == self.tr("Genetic +"):
            if not (er_fl and exec_mode == 1):
                mod_numb_launch = int(self.gridElementOfInput[self.curInd][4].text())
                for i in range(len(self.gridElementOfInput[self.curInd])):
                    self.gridElementOfInput[self.curInd][i].setEnabled(False)
                    self.lay.itemAtPosition(self.curInd,i).widget().hide()

                count_of_modules = 16
                all_launch = count_of_modules * mod_numb_launch
                set_of_modules,modules_paramValueRes,re,er_fl,sum_er,sum_t,count_of_execs,module_name = self.ga.run_algorithm([0,set_of_modules,modules_paramValueRes,re,er_fl,sum_er,sum_t,all_launch])
        else:
            for i in range(len(self.gridElementOfInput)):
                if not (er_fl and self.exec_mode == 1):
                    if self.gridElementOfInput[i][2].isEnabled():
                        set_of_modules,modules_paramValueRes,re,er_fl,sum_er,sum_t,count_of_execs,module_name = self.module_run_inter(i,set_of_modules,modules_paramValueRes,re,er_fl,sum_er,sum_t,count_of_execs)
        re += self.timeResult.modules_res()
        list_of_flags = self.timeResult.list_flags_name(module_name, None)
        # list_of_flags = self.timeResult.list_flags_name(module_name, 32)
        for i in range(len(list_of_flags)):
            list_of_flags[i] = str(i)+'. '+list_of_flags[i]
        re += '  \n'.join(list_of_flags)+"  \n"
        self.textEdit.append('<b>'+self.tr("Project ")+proj_name
                            +self.tr(" is finished ")
                            +datetime.now().strftime("%H:%M:%S")+'</b>')
        self.textEdit.append(self.tr('Total project lead time : ')+str(sum_t)
                            +self.tr('. Successfully completed modules: ')+'<b>'
                            +str(self.sum_good)+'/'
                            +str(count_of_modules)+'</b>')
        if er_fl:
            self.textEdit.append(self.tr('Errors: '))
            for er in sum_er:
                for err in er:
                    self.textEdit.append(err)

        mas_fig = []
        for m in set_of_modules:
            mas_fig.append(lgc.diagram(count_of_modules,self.timeResult,m))
        self.progressBar.setValue(100)

        if not (os.path.isdir(os.path.join(self.base_addr,"result"))):
            os.makedirs(os.path.join(self.base_addr,"result"))
        mas_im_adr = []
        for i in range(len(mas_fig)):
            # save pyplot
            pyplot_res_name = os.path.join(self.base_addr,"result","res_"
                                           + proj_name + '_'
                                           + datetime.now().strftime("%H_%M")
                                           + '_' + str(i) + '.png')
            mas_fig[i].savefig(pyplot_res_name)
            mas_im_adr.append(pyplot_res_name)
        for i in range(len(mas_im_adr)):
            re += """![Diagram {}]({})  \n""".format(i,mas_im_adr[i])
        rep_short_nam = "res_"+proj_name+'_'+ datetime.now().strftime("%H_%M")
        report_name = os.path.join(self.base_addr,"result",rep_short_nam)
        os.chdir(os.path.join(self.base_addr,"result"))
        f = open(report_name+'.md', 'w+')
        f.write(re+'\n'+self.tr('### Progress')+'\n'
            +'\n'.join(list(map(lambda x: x+'  ',self.textEdit.toPlainText().split('\n')))))
        f.close()
        subprocess.run(['grip',rep_short_nam+".md",'--export',rep_short_nam+".html","--quiet"])#--title=<title>
        self.url_report = report_name+".html"
        self.pushButton_8.setEnabled(True)
        self.pushButton_10.setEnabled(False)
        temp_proj_list = [proj_name,self.base_addr,report_name+".html"]
        temp_proj_list.extend(mas_im_adr)
        # db project modules parametres values results(-)
        lgc.add_(temp_proj_list,modules_paramValueRes,self.rwd)

    def buttonClicked_del(self):  # hide row
        mb = QMessageBox()
        ind = int(str(self.form.sender().objectName())[3:])
        mb.setWindowTitle(self.tr("Delete module"))
        mb.setText(self.tr("del ")+str(ind))
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

    def fillParamLineEdit_ExhaustiveSearch(self, mas):
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

    def fillParamLineEdit_Genetic(self, mas):
        mas_param_for_change = [[],[]]
        strings = self.gridElementOfInput[self.curInd][3].toPlainText().split('\n')
        for numb in mas[0][1]:
            if not numb in mas_param_for_change[1]:
                mas_param_for_change[0].append(strings[numb])
                mas_param_for_change[1].append(numb)
        self.ga = Genetic(mas_param_for_change, self)

    def fillParamLineEdit(self):
        self.gridElementOfInput[self.curInd][3].clear()
        mas = self.ui_param.return_outMas()
        for i in mas[2]:
            self.gridElementOfInput[self.curInd][3].append(i)

        if mas[0][0] == 'someone want a combination':
            if self.actionExhaustive_search.text() == self.tr("Exhaustive search +"):
                self.fillParamLineEdit_ExhaustiveSearch(mas)
            else:
                self.fillParamLineEdit_Genetic(mas)

    def genetic_exec(self, new_str, ind_str,mst):
        self.buttonClicked_addModule()
        self.gridElementOfInput[self.numb-1][1].setText(self.gridElementOfInput[self.curInd][1].text())
        self.gridElementOfInput[self.numb-1][4].setText(self.gridElementOfInput[self.curInd][4].text())
        strings = self.gridElementOfInput[self.curInd][3].toPlainText().split('\n')
        strings[ind_str] = strings[ind_str].split('=',1)[0]+' = '+new_str
        self.gridElementOfInput[self.numb-1][3].clear()
        for i in strings:
            self.gridElementOfInput[self.numb-1][3].append(i.strip())
        another_mas = self.module_run_inter(self.numb-1,mst[1],mst[2],mst[3],mst[4],mst[5],mst[6],mst[7])
        return self.numb-1,another_mas

    def buttonClicked_addModule(self):
        self.gridElementOfInput.append([QLabel(str(self.numb)), QLineEdit(),
                                        QPushButton(self.tr("Change \nparameters")),
                                        QTextEdit(), QLineEdit(),
                                        QPushButton(self.tr("Delete"))])
        self.moduleInfo.add_module()
        self.gridElementOfInput[self.numb][2].clicked.connect(self.buttonClicked_adp)
        self.gridElementOfInput[self.numb][5].clicked.connect(self.buttonClicked_del)
        self.gridElementOfInput[self.numb][1].textChanged.connect(self.textLineEditChange)
        self.gridElementOfInput[self.numb][2].setObjectName("adp"+str(self.numb))
        self.gridElementOfInput[self.numb][5].setObjectName("btn"+str(self.numb))
        self.gridElementOfInput[self.numb][1].setObjectName("prNam"+str(self.numb))
        self.gridElementOfInput[self.numb][4].setText("1")
        self.gridElementOfInput[self.numb][2].setEnabled(False)
        self.gridElementOfInput[self.numb][3].setEnabled(False)
        self.gridElementOfInput[self.numb][4].setEnabled(False)
        self.gridElementOfInput[self.numb][3].setReadOnly(True)
        for i in range(6):
            self.lay.addWidget(self.gridElementOfInput[self.numb][i],self.numb,i,1,1)
        self.numb += 1

    def fill_tree(self):
        model = QStandardItemModel(0, 7, None)
        model.setHeaderData(0, Qt.Horizontal, self.tr(""))
        model.setHeaderData(1, Qt.Horizontal, self.tr("id"))
        model.setHeaderData(2, Qt.Horizontal, self.tr("name"))
        model.setHeaderData(3, Qt.Horizontal, self.tr("path/value"))
        model.setHeaderData(4, Qt.Horizontal, self.tr("date"))
        model.setHeaderData(5, Qt.Horizontal, self.tr("time"))
        model.setHeaderData(6, Qt.Horizontal, self.tr("path"))

        self.treeView.setModel(model)
        self.treeView.setColumnHidden(1,True)
        self.treeView.setColumnWidth(0,200)
        self.treeView.setColumnHidden(6,True)

        found = lgc.find_(self.lineEdit.text(),self.lineEdit_2.text(),
                          self.dateTimeEdit.dateTime().toPyDateTime(),
                          self.dateTimeEdit_2.dateTime().toPyDateTime(),
                          self.rwd)

        root = model.invisibleRootItem()
        parent = root
        for pr in found:
            old_parent_pr = parent
            parent.appendRow([QStandardItem(self.tr("Project:")),
                              QStandardItem(str(pr[0][0])),
                              QStandardItem(str(pr[0][1])),
                              QStandardItem(str(pr[0][2])),
                              QStandardItem(),QStandardItem(),QStandardItem()])
            parent = parent.child(parent.rowCount() - 1)
            for r in pr[1]:
                parent.appendRow([QStandardItem(self.tr("Result:")),
                                  QStandardItem(),QStandardItem(),
                                  QStandardItem(str(r[1])),
                                  QStandardItem(str(r[4])),
                                  QStandardItem(str(r[5])),QStandardItem()])
            for b in pr[2:]:
                old_parent_mod = parent
                parent.appendRow([QStandardItem(self.tr("Module:")),
                                  QStandardItem(str(b[1][0])),
                                  QStandardItem(str(b[1][1])),
                                  QStandardItem(str(b[1][2])),QStandardItem(),
                                  QStandardItem(),QStandardItem(b[0][3])])
                parent = parent.child(parent.rowCount() - 1)
                for pv in b[2:]:
                    parent.appendRow([QStandardItem(self.tr("Parameter,Value:")),
                                      QStandardItem(str(pv[0][0])),
                                      QStandardItem(str(pv[0][2])),
                                      QStandardItem(str(pv[1][2])),
                                      QStandardItem(), QStandardItem(),QStandardItem()])
                parent = old_parent_mod
            parent = old_parent_pr

    def get_bot_info(self):
        mas = []
        if self.textEdit.toPlainText() == "" or self.pushButton_8.isEnabled():
            mas.append(None)
            mas.append(timedelta())
        else:
            mas.append(datetime.now() - self.time_of_begin)
            mas.append(self.label_5.text())
        mas.append(self.cur_mod)
        mas.append(self.cur_er_count)
        return mas

    def send_mes_to_bot(self):
        # self.thread.periodic(self.cur_mod)
        pass

    def stop_project(self):
        self.stop_fl = True

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
        self.pushButton_2.clicked.connect(self.buttonClicked_accept)
        self.pushButton.clicked.connect(self.buttonClicked_reject)

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
                    combination.append({'number':i, 'param':j})
                    combinationIndex.append(i)
        if len(combination) > 0 or len(search_one_by_one) > 0:
            self.outMas.append(['someone want a combination', combinationIndex])
            self.outMas.append([combination, search_one_by_one])
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

class Communicate(QObject):
    fillParam = pyqtSignal()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    com = Communicate()

    translator = QTranslator(app)
    translator.load('language_ru.qm')
    app.installTranslator(translator)

    window = QMainWindow()
    window_param = QWidget()
    ui_param = Param(window_param, com)
    ui = Example(window, com, window_param, ui_param, translator, app)
    window.show()

    sys.exit(app.exec_())
