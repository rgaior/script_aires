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
import detector
import simulation
import waveform
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
parser.add_argument("-factor", type=int, nargs='?',default=1, help="signal factor")
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
    stid = file[file.rfind('st_')+3:file.rfind('.inp')]
    evid = file[file.rfind('ev_')+3:file.rfind('st_')]
    print 'stid = ' , stid
else:
    stid = 0

for ant in evtest.antennas:
    ant.getXmax_angle(evtest.XmaxCoord)
    ant.setantenna()
    gain = ant.getgainatXmax()
    ant.filtertrace()
    ant.setvtrace()
    
ant = evtest.antennas[0]

parser.add_argument("-det", type=str, nargs='?',default='dmx', help="type of detector: gi, dmx, norsat, helix")
args = parser.parse_args()
dettype = args.det
if dettype == 'dmx':
    detname = 'EASIER'
if dettype == 'norsat':
    detname = 'GDC'
if dettype == 'helix':
    detname = 'GDL'
    
method = 3
tsys = constant.meantempdict[detname]
det = detector.Detector(temp = tsys, type=dettype)
det.loadspectrum()
print 'tsys = ' , tsys
print 'delta B = ', det.deltaB


sig = waveform.Waveform(ant.time*1e-9,ant.vtrace,'vtrace')
#sig = waveform.Waveform(ant.time*1e-9,ant.othervtrace,'vtrace')
print 'sig smampling = ' , sig.sampling
print 'sig lenght = ' , sig.length

#time = ant.maketimearray()
sim = simulation.Simulation(det=det, sampling = sig.sampling)
sim.producetime()
sim.producenoise(True)
#sim.time = time
factor = args.factor
sim.setsignalwitharrays(sig.time,factor*sig.amp)

# sim.setpowerenvelopewitharray([time,ant.power])
# sim.producesignal()
print 'len(noise) = ' , len(sim.noise),'len(nsig) = ' , len(sim.signal),'len(time) = ' , len(sim.time)
simwf = waveform.Waveform(sim.time,sim.noise+sim.signal, type='hf')
wf = det.producesimwaveform(simwf,'adc',method)
# ant.trace = wf.amp
pnoise = np.mean(sim.noise**2/50)
print 'Pnoise = ' , pnoise
print 'calc tsys = ' , pnoise/(constant.kb*det.deltaB)
#plt.plot(sim.time, sim.signal)
#plt.plot(simwf.time,simwf.amp)
plotfolder = constant.airesanalysisfolder + '/plots/'
figsim = plt.figure(figsize=(8,5))
plt.plot(wf.amp-np.mean(wf.amp))
plt.xlabel('time bin [25ns]')
plt.ylabel('radio power [ADCu]')

figsim.savefig(plotfolder + 'simev_'+evid+'_fac_'+str(factor) + '.png')
figstep, ar = plt.subplots(4, figsize=(8,10))
print 'ant.time = ',ant.Ex
ar[0].plot(ant.time, ant.Ex)
ar[1].plot(ant.time, ant.vtrace)
ar[2].plot(sim.time, sim.noise+sim.signal)
ar[3].plot((wf.amp-np.mean(wf.amp)))
plt.tight_layout()
figstep.savefig(plotfolder+ 'step.png')
#plt.plot(wf.time,wf.amp)

#####################
# data
#####################
figdata = plt.figure(figsize=(8,5))
datafolder = '/Users/gaior/EASIER/data_analysis/production/script/'
dataevid = constant.eventdictpath[int(evid)]
txtfile = datafolder + dataevid
df1 = utils.txtfilereader(txtfile)
t1 =  df1.trace[0]
plt.plot(-t1 -np.mean(-t1))
plt.xlabel('time bin [25ns]')
plt.ylabel('radio power [ADCu]')
figdata.savefig(plotfolder + 'dataev_'+evid+'_fac_'+str(factor) + '.png')
plt.show()
