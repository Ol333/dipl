#!/usr/bin/env python3
import os
from datetime import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt

class AllTime():
    timeResult = {}

    def add_module(self,module_name):
        self.timeResult[module_name] = {'worstWorstTime':None,
                                        'worstAverageTime':None,
                                        'bestAverageTime':None,
                                        'bestBestTime':None,
                                        'wwtModule':0, 'watModule':0,
                                        'batModule':0, 'bbtModule':0,
                                        'diagram_names':[], 'diagram_values':[]}

    def const_rand_flags_test(self,mas_line,module_name):
        if mas_line.split(' ')[0]=="CONSTFLAGS":
            temp = mas_line.split('=',1)[1]
            self.timeResult[module_name]['diagram_names'].append(temp)
        elif mas_line.split(' ')[0]=="RANDFLAGS":
            self.timeResult[module_name]['diagram_names'][-1] += '\n' + mas_line

    def module_name_exist(self,module_name):
        if not self.timeResult.get(module_name):
            self.add_module(module_name)

    def add_time_of_module(self,module_name,time):
        self.timeResult[module_name]['diagram_values'].append(time)

    def test_time_values(self,module_name,worstTime,aver_time,bestTime,mod_num):
        if (self.timeResult[module_name]['worstWorstTime'] == None or
                self.timeResult[module_name]['worstWorstTime'] < worstTime):
            self.timeResult[module_name]['worstWorstTime'] = worstTime
            self.timeResult[module_name]['wwtModule'] = mod_num
        if (self.timeResult[module_name]['worstAverageTime'] == None or
                self.timeResult[module_name]['worstAverageTime'] < aver_time):
            self.timeResult[module_name]['worstAverageTime'] = aver_time
            self.timeResult[module_name]['watModule'] = mod_num
        if (self.timeResult[module_name]['bestAverageTime'] == None or
                self.timeResult[module_name]['bestAverageTime'] > aver_time):
            self.timeResult[module_name]['bestAverageTime'] = aver_time
            self.timeResult[module_name]['batModule'] = mod_num
        if (self.timeResult[module_name]['bestBestTime'] == None or
                self.timeResult[module_name]['bestBestTime'] > bestTime):
            self.timeResult[module_name]['bestBestTime'] = bestTime
            self.timeResult[module_name]['bbtModule'] = mod_num

    def result(self,module_name):
        res = ""
        res += (str(self.timeResult[module_name]['worstWorstTime'])+
                ' - worst worst Time\n')
        res += ('worst worst Time module №:  '+
                str(self.timeResult[module_name]['wwtModule'])+'\n')
        res += (str(self.timeResult[module_name]['worstAverageTime'])+
                ' - worst average Time\n')
        res += ('worst average Time module №:  '+
                str(self.timeResult[module_name]['watModule'])+'\n')
        res += (str(self.timeResult[module_name]['bestAverageTime'])+
                ' - best average Time\n')
        res += ('best average Time module №:  '+
                str(self.timeResult[module_name]['batModule'])+'\n')
        res += (str(self.timeResult[module_name]['bestBestTime'])+
                ' - best best Time\n')
        res += ('best best Time module №:  '+
                str(self.timeResult[module_name]['bbtModule'])+'\n')
        return res

    def list_flags_name(self,module_name,numb_of_combinats):
        res = self.timeResult[module_name]['diagram_names'][:numb_of_combinats]
        return res

    def col_vo_const_fl(self,module_name,numb_of_combinats):
        res = int(len(self.timeResult[module_name]['diagram_names'])/
                numb_of_combinats)
        return res

    def take_list_cut(self,module_name,numb_of_combinats,ind):
        temp_list = self.timeResult[module_name]['diagram_values']
        res = temp_list[numb_of_combinats*ind:numb_of_combinats*(ind+1)]
        return res

    def list_for_label(self,module_name,numb_of_combinats,ind):
        index = numb_of_combinats * ind
        temp = self.timeResult[module_name]['diagram_names'][index].split('\n')
        res = ""
        if temp[0] != '':
            res = temp[0]
        else:
            res = '-'
        return res

    def modules_res(self):
        res = ""
        for mod in self.timeResult.keys():
            res += '#######\n'
            res += mod + '\n'
            res += self.result(mod)
        res += '#######\n'
        return res

class ModuleTime():
    moduleInfo = []

    def add_module(self):
        self.moduleInfo.append({'originParam':None,'worstTime':None,
                                'bestTime':None,'sumTime':0})

    def set_orig_param(self,ind,text):
        self.moduleInfo[ind]['originParam']=text

    def string_for_replace(self,ind,counter):
        res = (self.moduleInfo[ind]['originParam'][counter][0]+' = '+
              self.moduleInfo[ind]['originParam'][counter][1])
        return res

    def test_time_values(self,ind,numb_of_repeat,time):
        if numb_of_repeat==0 or self.moduleInfo[ind]['worstTime'] < time:
            self.moduleInfo[ind]['worstTime'] = time
        if numb_of_repeat==0 or self.moduleInfo[ind]['bestTime'] > time:
            self.moduleInfo[ind]['bestTime'] = time
        if numb_of_repeat==0:
            self.moduleInfo[ind]['sumTime'] = time
        else:
            self.moduleInfo[ind]['sumTime'] += time

    def aver_time(self,ind,count_of_repeat):
        res = self.moduleInfo[ind]['sumTime'] / count_of_repeat
        return res

    def module_time(self,ind,aver_time):
        res = ""
        res += '****'+'\n'
        res += str(self.moduleInfo[ind]['worstTime'])+' - worst Time'+'\n'
        res += str(aver_time)+' - average Time' + '\n'
        res += str(self.moduleInfo[ind]['bestTime'])+' - best Time'+'\n'
        res += '****'+'\n'
        return res

    def get_worst_time(self,ind):
        return self.moduleInfo[ind]['worstTime']

    def get_best_time(self,ind):
        return self.moduleInfo[ind]['bestTime']

def add_(proj,modules_ParamValueRes,rwd):
    mas_of_mod_and_its_val = []
    for mod in modules_ParamValueRes:
        fl_mod = True
        mas_module = rwd.select_module(mod[0],mod[1])
        if mas_module:
            # модуль уже есть (и не один мб)
            mod_ind = 0
            while fl_mod and mod_ind < len(mas_module):
                fl_param = True
                pv_ind = 0
                mas_param_id = []
                while fl_param and pv_ind < len(mod[2]):
                    param,value = mod[2][pv_ind].split('=',1)
                    id_param = rwd.select_param(mas_module[mod_ind],param.strip(),"string") #эээээ стринг?
                    if id_param == None:
                        fl_param = False
                    else:
                        mas_param_id.append(id_param)
                    pv_ind += 1
                if fl_param:
                    pv_ind = 0
                    mas_of_mod_and_its_val.append([mas_module[mod_ind],[],mod[-2],mod[-1]])
                    while pv_ind < len(mod[2]):
                        param,value = mod[2][pv_ind].split('=',1)
                        mas_of_mod_and_its_val[-1][1].append([mas_param_id[pv_ind],value.strip().strip("'")])
                        pv_ind += 1
                    fl_mod = False
                mod_ind += 1
        # модуля нет или ни один не совпадает
        if fl_mod:
            id_mod = rwd.insert_module(mod[0],mod[1])
            mas_of_mod_and_its_val.append([id_mod,[],mod[-2],mod[-1]])
            for PV in mod[2]:
                param,value = PV.split('=',1)
                id_param = rwd.insert_param(id_mod,param.strip(),"string")
                mas_of_mod_and_its_val[-1][1].append([id_param,value.strip().strip("'")])
    # перебрали все модули
    id_proj = rwd.select_proj(proj[0],proj[1])
    if id_proj != None:
        # проверить привязки
        mas_safe_module = rwd.select_binding(id_proj)
        if (len(mas_safe_module) == len(mas_of_mod_and_its_val)):
            for m in mas_of_mod_and_its_val:
                if m[0] in mas_safe_module:
                    mas_safe_module.remove(m[0])
            if len(mas_safe_module) != 0:
                id_proj = rwd.insert_proj(proj[0],proj[1])
    else:
        id_proj = rwd.insert_proj(proj[0],proj[1])
    # создать результат и привязки
    for m in mas_of_mod_and_its_val:
        id_binding = rwd.insert_binding(m[2],m[3],"",id_proj,m[0])
        mas_of_values = []
        for pv in m[1]:
            mas_of_values.append([pv[0],pv[1],id_binding])
        rwd.insert_few_value(mas_of_values)
    rwd.insert_res(proj[2],proj[2].split('.')[1],id_proj)
    rwd.insert_res(proj[3],proj[3].split('.')[1],id_proj)
    rwd.connection.commit()

def find_(s_proj,s_mod,dt1,dt2,rwd):
    result = []
    proj = rwd.select_proj_with_condition(s_proj)
    for pr in proj:
        result.append([pr])
        res = rwd.get_table_by_id("result","Project_id",pr[0])
        result[-1].append([])
        dt_fl = False
        for r in res:
            result[-1][-1].append(r)
            dt_res = datetime.combine(r[4], r[5])
            if dt1 < dt_res and dt_res < dt2:
                dt_fl = True
        if not dt_fl:
            result.pop()
            break
        bind = rwd.select_binding_with_condition(pr[0])
        mod_fl = False
        for b in bind:
            result[-1].append([])
            mod = rwd.get_line_by_id("module","Id",b[5])
            if (mod[1].find(s_mod) != -1):
                mod_fl = True
            result[-1][-1].append(b)
            result[-1][-1].append(mod)
            param = rwd.get_table_by_id("parameter","Module_id",mod[0])
            for p in param:
                val = rwd.get_value(p[0],b[0])
                result[-1][-1].append([p,val])
        if not mod_fl:
            result.pop()
    return result

def delete_proj(proj_id,rwd):
    mas_bind_id = rwd.select_binding(proj_id)
    mas_res_path = rwd.del_and_return_mas('result','Project_id',proj_id,'Path')
    for p in mas_res_path:
        os.remove(p[0])
    mods = set()
    for b in mas_bind_id:
        mas_modu_id = rwd.del_and_return_mas('value','Binding_id',b[0],'')
        mods.add(b[1])
    rwd.del_and_return_mas('binding','Project_id',proj_id,'')
    rwd.del_by_id('project',proj_id)
    for m in mods:
        mas_bind = rwd.get_table_by_id('binding','Module_id',m)
        if len(mas_bind)==0:
            rwd.del_and_return_mas('parameter','Module_id',m,'')
            rwd.del_by_id('module',m)
    rwd.connection.commit()

def diagram(count_of_modules,timeResult,module_name):
    fig = plt.figure()
    mpl.rcParams.update({'font.size': 10})
    plt.title('Average program execution time')
    ax = plt.axes()
    ax.xaxis.grid(True, zorder = 1)
    tempN = count_of_modules
    col_vo_const_fl = timeResult.col_vo_const_fl(module_name,tempN)
    xs = range(tempN)
    for i in range(col_vo_const_fl):
        plt.barh([x + 0.05 + (0.9 / col_vo_const_fl)*i for x in xs],
                timeResult.take_list_cut(module_name,tempN,i),
                height=(0.9 / col_vo_const_fl),
                color=[(0.12*(i%3))/1,(0.12*(i%3+1))/1,(0.12*(i%3+2))/1],
                label=timeResult.list_for_label(module_name,tempN,i),
                zorder=2)
    plt.yticks(xs,range(0,tempN))
    plt.legend(loc='upper right')
    # plt.show()
    return fig
