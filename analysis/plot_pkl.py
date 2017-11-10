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
from matplotlib import colors as mcolors
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

############################
##  argument parser       ##
############################
parser = argparse.ArgumentParser()
parser.add_argument("inpfile", type=str, nargs='?',default='e_18_5.pkl', help="full input file name")
args = parser.parse_args()
evname = args.inpfile

#######################################                                                                                                               
## open in pkl format the event data ##                                                                                                               
#######################################                                                                                                               
eventfolder = constant.eventfolder 
filename = eventfolder + evname
if os.path.isfile(filename):
    eventfile = open(filename,'rb')
else:
    exit
evtest = pickle.load(eventfile)
evtest.printevent()
figE, axE = plt.subplots(figsize=(10,8))
figE.suptitle('Abs(E) event: '+evtest.inputfile + ' E: ' +str(evtest.energy)+ ' theta: '+ str(evtest.theta) + ' phi: '+str(evtest.phi), fontsize=12)
figEx, axEx = plt.subplots(figsize=(10,8))
figEx.suptitle('Ex event: '+evtest.inputfile + ' E: ' +str(evtest.energy)+ ' theta: '+ str(evtest.theta) + ' phi: '+str(evtest.phi), fontsize=12)
figEy, axEy = plt.subplots(figsize=(10,8))
figEy.suptitle('Ey event: '+evtest.inputfile + ' E: ' +str(evtest.energy)+ ' theta: '+ str(evtest.theta) + ' phi: '+str(evtest.phi), fontsize=12)
figEz, axEz = plt.subplots(figsize=(10,8))
figEz.suptitle('Ez event: '+evtest.inputfile + ' E: ' +str(evtest.energy)+ ' theta: '+ str(evtest.theta) + ' phi: '+str(evtest.phi), fontsize=12)
#from random import randint
#colors = []
#for i in range(12):
#    colors.append('#%06X' % randint(0, 0xFFFFFF))
#    print colors
cols = colors.values()[:12]
for ant,c in zip(evtest.antennas,cols):
    #    plt.plot(ant.time,ant.absE,label = 'ant nr: '+str(ant.id) + ' X:'+str(ant.X) + ' Y:'+str(ant.Y))
#    plt.plot(ant.time,ant.absE,label = 'ant nr: '+str(ant.id) + ' X:'+str(ant.X) + ' Y:'+str(ant.Y))
 #   plt.plot(ant.time,ant.absE,label = 'ant nr: '+str(ant.id) + ' X:'+str(ant.X) + ' Y:'+str(ant.Y))
    axEx.plot(ant.time,ant.Ex*1e3,color=c,label = 'ant: '+str(ant.id) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')
    axEy.plot(ant.time,ant.Ey*1e3,color=c,label = 'ant: '+str(ant.id) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')
    axEz.plot(ant.time,ant.Ez*1e3,color=c,label = 'ant: '+str(ant.id) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')
    axE.plot(ant.time,ant.absE*1e3,color=c,label = 'ant: '+str(ant.id) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')
    axE.set_xlabel('time[ns]')
    axE.set_ylabel('E field [mV/m]')
    axEx.set_xlabel('time[ns]')
    axEx.set_ylabel('E field [mV/m]')
    axEy.set_xlabel('time[ns]')
    axEy.set_ylabel('E field [mV/m]')
    axEz.set_xlabel('time[ns]')
    axEz.set_ylabel('E field [mV/m]')
    axEx.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=3, mode="expand", borderaxespad=0.)
    axEy.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=3, mode="expand", borderaxespad=0.)
    axEz.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=3, mode="expand", borderaxespad=0.)
    axE.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=3, mode="expand", borderaxespad=0.)
    figEx.subplots_adjust(bottom=0.12, top=0.75, left=0.18, right=0.95)
    figEy.subplots_adjust(bottom=0.12, top=0.75, left=0.18, right=0.95)
    figEz.subplots_adjust(bottom=0.12, top=0.75, left=0.18, right=0.95)
    figE.subplots_adjust(bottom=0.12, top=0.75, left=0.18, right=0.95)

#plt.legend()
plotfolder = constant.airesanalysisfolder + '/plots/'
basename = evname[:-4]
figEx.savefig(plotfolder + basename +'_Ex.png')
print plotfolder + basename +'_Ex.png'
#ant.time,ant.Ex*1e3
axEx.set_xlim(ant.time[np.argmax(ant.Ex)]-100,  ant.time[np.argmax(ant.Ex)]+100)
figEx.savefig(plotfolder + basename +'_Ex_zoom.png')
figEy.savefig(plotfolder + basename +'_Ey.png')
axEy.set_xlim(ant.time[np.argmax(ant.Ex)]-100,  ant.time[np.argmax(ant.Ex)]+100)
figEy.savefig(plotfolder + basename +'_Ey_zoom.png')
figEz.savefig(plotfolder + basename +'_Ez.png')
axEz.set_xlim(ant.time[np.argmax(ant.Ex)]-100,  ant.time[np.argmax(ant.Ex)]+100)
figEz.savefig(plotfolder + basename +'_Ez_zoom.png')
figE.savefig(plotfolder + basename +'_E.png')
axE.set_xlim(ant.time[np.argmax(ant.Ex)]-100,  ant.time[np.argmax(ant.Ex)]+100)
figE.savefig(plotfolder + basename +'_E_zoom.png')
plt.show()

#print evtest
