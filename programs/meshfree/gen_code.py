#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Параметры скрипта например такие
# n = 5
# u0 = 0.6
# strFun = 'u^2-u'
# fileName = 'recalcD'

from __future__ import print_function
from sys import argv, stdout, exit
if len(argv) < 5:
    print('Empty parameter(s)!\nUsage: {0} <nmax> <u0> <function> <file_name_without_extension> [LaTeX_flag]\nExample: {0} 10 0.5 u^2 recalcD'.format(argv[0]))
    exit()
n = int(argv[1])
u0 = float(argv[2])
strFun = argv[3]
fileName = argv[4]
print('Running {} for {}, n = {}, u0 = {}. Please wait'.format(argv[0], strFun, n, u0))
# Список для хранения производных в нетронутом виде
listD = []
# Внутренние константы
strX = 'x'
strU = 'u'
from sympy import Symbol, Function, sympify, diff, simplify
x = Symbol(strX)
u = Function(strU)(x)
f = sympify(strFun)
f = f.subs(Symbol(strU), u)
print('Getting substitution list... ', end='')
listSubs = ['Derivative(u(x), x)']
i = 2
while i < n:
    listSubs.append('Derivative(u(x), (x, {}))'.format(i))
    i += 1
# print(listSubs)
print('Done\nCalculating derivatives... ', end='')
stdout.flush()
listD.append(f)
# Список для хранения производных с подстановками
listN = [u0]
symU0 = Symbol('u0')
listFunPair = []
i = 0
while i < n - 1:
    listD.append(diff(listD[i], x))
    d = listD[i]
    j = i
    while j > 0:
        d = d.subs(sympify(listSubs[j - 1]), listN[j])
        j -= 1
    listN.append(d)
    # listFunPair.append(('f{}'.format(i + 1), d.subs(u, symU0) ))
    listFunPair.append(('f{}'.format(i + 1), simplify(d.subs(u, symU0)) ))
    i += 1
print('Done\nPreparing data for code generation... ', end='')
# print(listD)
# print(listN)
strFuns = ""
i = 1;
while i < n:
    strFuns += "Function('f{}')(u0), ".format(i)
    i += 1
strFuns = strFuns[: len(strFuns) - 2]
listFun = [symU0]
listFun.extend(sympify(strFuns))
from sympy import Matrix, MatrixSymbol, Eq
Ui = MatrixSymbol('Ui', n, 1)
mat = Matrix(listFun)
resFunc = Eq(Ui, mat)
listFunFull = []
listFunFull.extend(listFunPair)
listFunFull.append(('recalcD', resFunc))
from sympy.utilities.codegen import codegen
print('Done\nGenerating code... ', end='')
# [(c_name, c_code), (h_name, h_code)] = codegen(listFunFull, 'C', argv[4], header=False, empty=False) # global_vars=(symU0,), to_files=True
[(c_name, c_code), (h_name, h_code)] = codegen(listFunFull, 'C', fileName, header=False, empty=False) # global_vars=(symU0,), to_files=True
print('Done\nPolishing generated code... ', end='')
def depow(code, n):
    i = 2
    while i <= n:
        code = code.replace("pow(u0, {})".format(i), " * ".join(list('a'*i)).replace('a', 'u0'))
        i += 1
    return code

c_code = depow(c_code, 9)
# эту сроку нужно будет удалить при наличии функций из math.h
# c_code = c_code.replace('#include <math.h>', '')
c_code = c_code.replace("}\ndouble f", "}\ninline double f").replace("double f1(double u0)", "inline double f1(double u0)")
print('Done\nWrite to files... ', end='')

# inline
# c_code = c_code.replace("pow(u0, 2)", "u0 * u0").replace("#include <math.h>", "").replace("}\ndouble f", "}\ninline double f").replace("double f1(double u0)", "inline double f1(double u0)")
# no inline
# print(c_code.replace("pow(u0, 2)", "u0 * u0").replace("#include <math.h>", ""))

def writeToFile(fName, content):
    with open(fName, 'w') as out_file:
        out_file.writelines(content)

def getLatexD():
    from sympy import latex
    with open('derivatives.tex', 'w') as out_file:
        out_file.write('\\documentclass[eqno]{extarticle}\n\\usepackage[margin=2cm,landscape,a4paper]{geometry}\n\\usepackage{amsmath}\n\\begin{document}\n\\tiny')
        out_file.writelines(['$$%s$$\n' % latex(item)  for item in listD])
        out_file.write('\\end{document}')

writeToFile(c_name, c_code)
writeToFile(h_name, h_code)
print('All done!\nYour code in {} and {}'.format(c_name, h_name))
if len(argv) == 6:
    print('Generating LaTeX file... ', end='')
    getLatexD()
    print('Done: derivatives.tex')
