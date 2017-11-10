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

print 'typw =  ', evtest.type
file = evname
if evtest.type == 'real':
    stid = file[file.rfind('st_')+3:file.rfind('_p')]
    print 'stid = ' , stid
else:
    stid = 0

evtest.printevent()
figE, axE = plt.subplots(2,figsize=(8,8))
figE.suptitle('Abs(E) event: '+evtest.inputfile + ' E: ' +str(evtest.energy)+ ' theta: '+ str(evtest.theta) + ' phi: '+str(evtest.phi), fontsize=12)
figEx, axEx = plt.subplots(2,figsize=(8,8))
figEx.suptitle('Ex event: '+evtest.inputfile + ' E: ' +str(evtest.energy)+ ' theta: '+ str(evtest.theta) + ' phi: '+str(evtest.phi), fontsize=12)
figEy, axEy = plt.subplots(2,figsize=(8,8))
figEy.suptitle('Ey event: '+evtest.inputfile + ' E: ' +str(evtest.energy)+ ' theta: '+ str(evtest.theta) + ' phi: '+str(evtest.phi), fontsize=12)
figEz, axEz = plt.subplots(2,figsize=(8,8))
figEz.suptitle('Ez event: '+evtest.inputfile + ' E: ' +str(evtest.energy)+ ' theta: '+ str(evtest.theta) + ' phi: '+str(evtest.phi), fontsize=12)
#from random import randint
#colors = []
#for i in range(12):
#    colors.append('#%06X' % randint(0, 0xFFFFFF))
#    print colors
cols = colors.values()[:12]
for ant,c in zip(evtest.antennas,cols):
    print ant.stid
    c = 'blue'
    #    plt.plot(ant.time,ant.absE,label = 'ant nr: '+str(ant.id) + ' X:'+str(ant.X) + ' Y:'+str(ant.Y))
#    plt.plot(ant.time,ant.absE,label = 'ant nr: '+str(ant.id) + ' X:'+str(ant.X) + ' Y:'+str(ant.Y))
 #   plt.plot(ant.time,ant.absE,label = 'ant nr: '+str(ant.id) + ' X:'+str(ant.X) + ' Y:'+str(ant.Y))
    axEx[0].plot(ant.time,ant.Ex*1e3,color=c,label = 'ant: '+str(ant.stid) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')
    axEy[0].plot(ant.time,ant.Ey*1e3,color=c,label = 'ant: '+str(ant.stid) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')
    axEz[0].plot(ant.time,ant.Ez*1e3,color=c,label = 'ant: '+str(ant.stid) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')
    axE[0].plot(ant.time,ant.absE*1e3,color=c,label = 'ant: '+str(ant.stid) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')

    freq = np.fft.rfftfreq(len(ant.time),0.1e-9)
    specEx = np.fft.rfft(ant.Ex)
    specEy = np.fft.rfft(ant.Ey)
    specEz = np.fft.rfft(ant.Ez)
    specE = np.fft.rfft(ant.absE)
    axEx[1].semilogy(freq/1e9,np.abs(specEx),color=c,label = 'ant: '+str(ant.stid) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')
    axEy[1].semilogy(freq/1e9,np.abs(specEy),color=c,label = 'ant: '+str(ant.stid) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')
    axEz[1].semilogy(freq/1e9,np.abs(specEz),color=c,label = 'ant: '+str(ant.stid) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')
    axE[1].semilogy(freq/1e9,np.abs(specE),color=c,label = 'ant: '+str(ant.stid) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')

    axE[0].set_xlabel('time [ns]')
    axE[0].set_ylabel('E field [mV/m]')
    axEx[0].set_xlabel('time [ns]')
    axEx[0].set_ylabel('E field [mV/m]')
    axEy[0].set_xlabel('time [ns]')
    axEy[0].set_ylabel('E field [mV/m]')
    axEz[0].set_xlabel('time [ns]')
    axEz[0].set_ylabel('E field [mV/m]')

    axE[1].set_xlabel('frequency [GHz]')
    axE[1].set_ylabel('spectrum [a.u.]')
    axEx[1].set_xlabel('frequency [GHz]')
    axEx[1].set_ylabel('spectrum [a.u.]')
    axEy[1].set_xlabel('frequency [GHz]')
    axEy[1].set_ylabel('spectrum [a.u.]')
    axEz[1].set_xlabel('frequency [GHz]')
    axEz[1].set_ylabel('spectrum [a.u.]')

    axEx[0].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=3, mode="expand", borderaxespad=0.)
    axEy[0].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=3, mode="expand", borderaxespad=0.)
    axEz[0].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=3, mode="expand", borderaxespad=0.)
    axE[0].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=3, mode="expand", borderaxespad=0.)
    figEx.subplots_adjust(bottom=0.12, top=0.85, left=0.18, right=0.95,hspace=0.4)
    figEy.subplots_adjust(bottom=0.12, top=0.85, left=0.18, right=0.95,hspace=0.4)
    figEz.subplots_adjust(bottom=0.12, top=0.85, left=0.18, right=0.95,hspace=0.4)
    figE.subplots_adjust(bottom=0.12, top=0.85, left=0.18, right=0.95,hspace=0.4)

#plt.legend()
plotfolder = constant.airesanalysisfolder + '/plots/'
basename = evname[:-4]
figEx.savefig(plotfolder + basename +'_Ex.png')
axEx[0].set_xlim(ant.time[np.argmax(ant.Ex)]-100,  ant.time[np.argmax(ant.Ex)]+100)
print plotfolder + basename +'_Ex.png'
#ant.time,ant.Ex*1e3
figEx.savefig(plotfolder + basename +'_Ex_zoom.png')
figEy.savefig(plotfolder + basename +'_Ey.png')
axEy[0].set_xlim(ant.time[np.argmax(ant.Ey)]-100,  ant.time[np.argmax(ant.Ey)]+100)
figEy.savefig(plotfolder + basename +'_Ey_zoom.png')
figEz.savefig(plotfolder + basename +'_Ez.png')
axEz[0].set_xlim(ant.time[np.argmax(ant.Ez)]-100,  ant.time[np.argmax(ant.Ez)]+100)
figEz.savefig(plotfolder + basename +'_Ez_zoom.png')
figE.savefig(plotfolder + basename +'_E.png')
axE[0].set_xlim(ant.time[np.argmax(ant.absE)]-100,  ant.time[np.argmax(ant.absE)]+100)
figE.savefig(plotfolder + basename +'_E_zoom.png')
plt.show()

#print evtest
