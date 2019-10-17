import os
import math
import matplotlib.pyplot as plt
import numpy as np
import numexpr as ne

def save(name='', folder='', fmt='png'):
    pwd = os.getcwd()
    iPath = './pictures/{}/{}'.format(fmt,folder)
    if not os.path.exists(iPath):
        os.mkdir(iPath)
    os.chdir(iPath)
    plt.savefig('{}.{}'.format(name, fmt), fmt='png')
    os.chdir(pwd)
    #plt.close()

array=[] #считываем параметры
with  open('parametres.txt', 'r') as f:
    array = [row.strip().split('"')[1] for row in f]
array = list(map(float,array))

x = [array[0],array[1],array[2]]
y = list(map(lambda a: a**(-a)+a*a-3,x))
li = list()
diaL = array[0]
diaR = array[2]
lag = 0.1
xx = np.arange(float(diaL), float(diaR), lag)

k = 0
while abs(x[1]**(-x[1])+x[1]*x[1]-3)>array[3]:
    k += 1
    a = (y[2]-y[0]-((y[1]-y[0])*(x[2]-x[0])/(x[1]-x[0])))/(x[2]*x[2]-x[0]*x[0]+((x[0]*x[0]-x[1]*x[1])*(x[2]-x[0])/(x[1]-x[0])))
    b = (y[1]-a*x[1]*x[1]+a*x[0]*x[0]-y[0])/(x[1]-x[0])
    c = y[0]-a*x[0]*x[0]-b*x[0]    

    d = b*b-4*a*c
    if (d<0):
        print('нет корней', x,y)
        break
    elif (d==0):
        x.append((-1)*b / (2*a)) 
        x.remove(x[0])
    else:
        x1 = ((-1)*b + math.sqrt(d)) / (2*a)
        x2 = ((-1)*b - math.sqrt(d)) / (2*a)
        if abs(x[0]-x1)<abs(x[0]-x2):
            x.append(x1)
        else:
            x.append(x2)
        x.remove(x[0])

    y = list(map(lambda a: a**(-a)+a*a-3,x))

    f = 'a*x*x+b*x+c'
    aa = {'x':xx} 
    yy = ne.evaluate(f,local_dict=aa)
    fig = plt.figure()
    li.append((xx,yy))
    for i in range(len(li)):
        plt.plot(li[i][0], li[i][1])
    grid1 = plt.grid(True)
    plt.scatter(x[2],y[2])
    save(name='{}_{}_{}_{}_{}'.format(*array,k), folder = '{}_{}_{}_{}'.format(*array))
##    plt.show()

output = open('./text/{}_{}_{}_{}.txt'.format(*array), 'w')
output.write('x = '+str(x[1])+'\nsteps = '+str(k)+'\ny = '+str(y[1])+'\naccuracy = '+str(array[3]))
output.close()
