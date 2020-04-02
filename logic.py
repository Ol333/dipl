#!/usr/bin/env python3

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
