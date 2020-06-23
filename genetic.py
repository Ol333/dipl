#!/usr/bin/env python3
from pyeasyga.pyeasyga import GeneticAlgorithm
import random
import PyQt5
from datetime import datetime, timedelta

class Genetic():
    ga = None
    exec = None
    mas_some_things = None
    another_mas = None

    def __init__(self, mas_param_and_ind,exec):
        self.exec = exec
        mas_param_with_names, mas_ind = mas_param_and_ind
        self.ind = mas_ind[0]
        tempL = ''.join(list(map(lambda x:x.split('=',1)[1],mas_param_with_names)))
        mas_param = list(tempL.strip().split(' '))
        k = 0
        while k < len(mas_param):
            if mas_param[k][0] != '-' and mas_param[k][0] != '$':
                mas_param[k-1] += ' ' + mas_param[k]
                mas_param.remove(mas_param[k])
            else:
                k += 1
        self.ga = GeneticAlgorithm(mas_param, population_size=4, generations=4,
                           crossover_probability=1.0, mutation_probability=0.4,
                           elitism=True, maximise_fitness=True)
        self.ga.create_individual = self.create_individual
        self.ga.crossover_function = self.crossover
        self.ga.mutate_function = self.mutate
        self.ga.selection_function = self.selection
        self.ga.fitness_function = self.fitness

    def create_individual(self, data):
        return [random.randint(0, 1) for _ in range(len(data))]

    def crossover(self, parent_1, parent_2):
        crossover_index = random.randrange(1, len(parent_1))
        child_1 = parent_1[:crossover_index] + parent_2[crossover_index:]
        child_2 = parent_2[:crossover_index] + parent_1[crossover_index:]
        return child_1, child_2

    def mutate(self, individual):
        mutate_index = random.randrange(len(individual))
        if individual[mutate_index] == 0:
            individual[mutate_index] = 1
        else:
            individual[mutate_index] = 0

    def selection(self, population):
        return random.choice(population)

    def fitness (self, individual, data):
        mas_param_for_launch = []
        for (selected, flag) in zip(individual, data):
            if selected:
                mas_param_for_launch.append(flag)

        print(mas_param_for_launch)
        print(individual)
        print("#####")
        mod_ind,self.another_mas = self.exec.genetic_exec(' '.join(mas_param_for_launch),self.ind,self.mas_some_things)
        self.mas_some_things[0] = mod_ind
        for i in range(len(self.mas_some_things)-1):
            self.mas_some_things[i+1] = self.another_mas[i]

        module_index = self.mas_some_things[0]
        aver_time = self.exec.moduleInfo.aver_time(module_index,
            int(self.exec.gridElementOfInput[module_index][4].text()))
        fitness = -aver_time.total_seconds() # среднее время исполнения модуля
        return fitness

    def run_algorithm(self,mas_some_things):
        self.mas_some_things = mas_some_things
        self.ga.run()
        for individual in self.ga.last_generation():
            print (individual)
        return self.another_mas
