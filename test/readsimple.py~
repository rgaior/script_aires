import numpy as np
import matplotlib.pyplot as plt
import sys
import os
cwd = os.getcwd()
#classpath = cwd + '/../classes/'
utilspath = cwd + '/../utils/'
sys.path.append(utilspath)
#sys.path.append(classpath)
import datetime
import constant
import utils
import pandas as pd

#file = '/Users/gaior/aires/example/refshower/timefresnel-root.dat'
file = '/Users/gaior/aires/example/1e19/timefresnel-root.dat'

f = open(file,'r')

lines = f.readlines()
a_ant = np.array([])
a_E = np.array([])
a_t = np.array([])
count = 0
first = True
for l in lines[15:]:
#    if '# new run started' in l:
#        break
    if '# new shower' in l:
        first = False

    if first == False:
#        print l
        if count < 3:
            count+=1
            continue
        else:
            count+=1
            ls = l.split()
            a_t = np.append(a_t,float(ls[5]))
            a_ant = np.append(a_ant,int(ls[1]))
            a_E = np.append(a_E,float(ls[10]))
            
binning = 0.1e-9
fsampling = 1./binning
amp = a_E[(a_ant==1)]
lpcut = 4.2e9
hpcut = 3.4e9
lpfiltered = utils.lowpass(amp,fsampling,3,lpcut)
hpfiltered = utils.lowpass(lpfiltered,fsampling,3,hpcut)
plt.plot(a_t[(a_ant==1)], a_E[(a_ant==1)])
plt.plot(a_t[(a_ant==1)], a_E[(a_ant==1)])
#plt.plot(a_t[(a_ant==2)], a_E[(a_ant==2)])
#plt.plot(a_t[(a_ant==3)], a_E[(a_ant==3)])
#plt.plot(a_t[(a_ant==4)], a_E[(a_ant==4)])

fft = np.fft.rfft( a_E[(a_ant==1)])
freq = np.fft.rfftfreq(len( a_E[(a_ant==1)] ) , binning )
#plt.semilogy(freq,np.abs(fft))
#plt.plot(freq,np.arctan(fft.imag/fft.real))
plt.show()
