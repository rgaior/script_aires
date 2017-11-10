import numpy as np
import matplotlib.pyplot as plt
import sys
import os
cwd = os.getcwd()
classpath = cwd + '/../classes/'
utilspath = cwd + '/../utils/'
sys.path.append(utilspath)
sys.path.append(classpath)
import event
import constant
import utils
import argparse
import pickle


inpfiles = ['e_17_0.pkl','e_17_5.pkl','e_18_0.pkl','e_18_5.pkl','e_19_0.pkl','e_19_5.pkl']
a_E50 = np.array([])
a_E100 = np.array([])
a_E200 = np.array([])
a_E500 = np.array([])
a_E1000 = np.array([])
a_En = np.array([])
for f in inpfiles:
#######################################                                                                                                               
## open in pkl format the event data ##                                                                                                               
#######################################                                                                                                               
    eventfolder = constant.eventfolder 
    filename = eventfolder + f
    if os.path.isfile(filename):
        eventfile = open(filename,'rb')
    else:
        exit
    evtest = pickle.load(eventfile)
    ant = evtest.antennas
    a_En = np.append(a_En, evtest.energy)
    a_E50 = np.append(a_E50, np.max(ant[1].absE))
    a_E100 = np.append(a_E100, np.max(ant[3].absE))
    a_E200 = np.append(a_E200, np.max(ant[5].absE))
    a_E500 = np.append(a_E500, np.max(ant[7].absE))
    a_E1000 = np.append(a_E1000, np.max(ant[9].absE))

plt.loglog(a_En, a_E50*1e3, label='Y = 50m')
plt.loglog(a_En, a_E100*1e3, label='Y = 100m')
plt.loglog(a_En, a_E200*1e3, label='Y = 200m')
plt.loglog(a_En, a_E500*1e3, label='Y = 500m')
plt.loglog(a_En, a_E1000*1e3, label='Y = 1000m')
plt.legend()
plt.xlabel('energy [eV]')
plt.ylabel('field [mV/m]')
plotfolder = constant.basefolder + '/plots/'
plt.savefig(plotfolder + 'energy_Yaxis.png')

plt.show()
