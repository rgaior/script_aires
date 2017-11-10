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
cols = colors.values()[:12]
a_distx = np.array([])
a_disty = np.array([])
ax_Ex = np.array([])
ax_Ey = np.array([])
ax_Ez = np.array([])
ax_E = np.array([])

ay_Ex = np.array([])
ay_Ey = np.array([])
ay_Ez = np.array([])
ay_E = np.array([])
for ant,c in zip(evtest.antennas,cols):
    if ant.X != 0:
        a_distx = np.append(a_distx,ant.X)
        ax_Ex = np.append(ax_Ex,np.max(np.abs(ant.Ex)))
        ax_Ey = np.append(ax_Ey,np.max(np.abs(ant.Ey)))
        ax_Ez = np.append(ax_Ez,np.max(np.abs(ant.Ez)))
        ax_E = np.append(ax_E,np.max(np.abs(ant.absE)))
    if ant.Y != 0:
        a_disty = np.append(a_disty,ant.Y)
        ay_Ex = np.append(ay_Ex,np.max(np.abs(ant.Ex)))
        ay_Ey = np.append(ay_Ey,np.max(np.abs(ant.Ey)))
        ay_Ez = np.append(ay_Ez,np.max(np.abs(ant.Ez)))
        ay_E = np.append(ay_E,np.max(np.abs(ant.absE)))
plotfolder = constant.basefolder + '/plots/'
basename = evname[:-4]
figx = plt.figure()
figx.suptitle('X axis event: '+evtest.inputfile + ' E: ' +str(evtest.energy)+ ' theta: '+ str(evtest.theta) + ' phi: '+str(evtest.phi), fontsize=12)
plt.plot(a_distx, ax_Ex*1e3,c='b',label='Ex')
plt.plot(a_distx, ax_Ey*1e3,c='r',label='Ey')
plt.plot(a_distx, ax_Ez*1e3,c='g',label='Ez')
plt.plot(a_distx, ax_E*1e3,lw=2,c='k',label='|E"')
plt.legend()
plt.xlabel('distance [m]')
plt.ylabel('E field [mV/m]')
figx.savefig(plotfolder + basename +'_dist_Xaxis.png')

figy = plt.figure()
figy.suptitle('Y axis event: '+evtest.inputfile + ' E: ' +str(evtest.energy)+ ' theta: '+ str(evtest.theta) + ' phi: '+str(evtest.phi), fontsize=12)
plt.plot(a_disty, ay_Ex*1e3,c='b',label='Ex')
plt.plot(a_disty, ay_Ey*1e3,c='r',label='Ey')
plt.plot(a_disty, ay_Ez*1e3,c='g',label='Ez')
plt.plot(a_disty, ay_E*1e3,lw=2,c='k',label='|E|')
plt.legend()
plt.xlabel('distance [m]')
plt.ylabel('E field [mV/m]')
figy.savefig(plotfolder + basename +'_dist_Yaxis.png')
plt.show()

#print evtest
#     axEx.plot(ant.time,ant.Ex*1e3,color=c,label = 'ant: '+str(ant.id) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')
#     axEy.plot(ant.time,ant.Ey*1e3,color=c,label = 'ant: '+str(ant.id) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')
#     axEz.plot(ant.time,ant.Ez*1e3,color=c,label = 'ant: '+str(ant.id) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')
#     axE.plot(ant.time,ant.absE*1e3,color=c,label = 'ant: '+str(ant.id) + ' ('+str(int(ant.X)) +', '+str(int(ant.Y))+')')
#     axE.set_xlabel('time[ns]')
#     axE.set_ylabel('E field [mV/m]')
#     axEx.set_xlabel('time[ns]')
#     axEx.set_ylabel('E field [mV/m]')
#     axEy.set_xlabel('time[ns]')
#     axEy.set_ylabel('E field [mV/m]')
#     axEz.set_xlabel('time[ns]')
#     axEz.set_ylabel('E field [mV/m]')
#     axEx.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#                ncol=3, mode="expand", borderaxespad=0.)
#     axEy.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#                ncol=3, mode="expand", borderaxespad=0.)
#     axEz.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#                ncol=3, mode="expand", borderaxespad=0.)
#     axE.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#                ncol=3, mode="expand", borderaxespad=0.)
#     figEx.subplots_adjust(bottom=0.12, top=0.75, left=0.18, right=0.95)
#     figEy.subplots_adjust(bottom=0.12, top=0.75, left=0.18, right=0.95)
#     figEz.subplots_adjust(bottom=0.12, top=0.75, left=0.18, right=0.95)
#     figE.subplots_adjust(bottom=0.12, top=0.75, left=0.18, right=0.95)

# #plt.legend()
# plotfolder = constant.basefolder + '/plots/'
# basename = evname[:-4]
# figEx.savefig(plotfolder + basename +'_Ex.png')
# axEx.set_xlim(0,1000)
# figEx.savefig(plotfolder + basename +'_Ex_zoom.png')
# figEy.savefig(plotfolder + basename +'_Ey.png')
# axEy.set_xlim(0,1000)
# figEy.savefig(plotfolder + basename +'_Ey_zoom.png')
# figEz.savefig(plotfolder + basename +'_Ez.png')
# axEz.set_xlim(0,1000)
# figEz.savefig(plotfolder + basename +'_Ez_zoom.png')
# figE.savefig(plotfolder + basename +'_E.png')
# axE.set_xlim(0,1000)
# figE.savefig(plotfolder + basename +'_E_zoom.png')
# #plt.savefig(figEx,plotfolder + inpfile+'_Ex.png')
