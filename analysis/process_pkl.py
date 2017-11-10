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
file  = evname
print 'typw =  ', evtest.type
if evtest.type == 'real':
    stid = file[file.rfind('st_')+3:file.rfind('.pkl')]
    print 'stid = ' , stid
else:
    stid = 0

for ant in evtest.antennas:
    ant.stid = int(stid)
    ant.getXmax_angle(evtest.XmaxCoord)
    ant.setantenna()
    gain = ant.getgainatXmax()
    ant.filtertrace()
    ant.setvtrace()
outfolder = constant.eventfolder 
outfilename = outfolder + str(evname[:-4] ) + '_p.pkl'
out = open(outfilename,'wb')
pickle.dump(evtest,out)
out.close()
