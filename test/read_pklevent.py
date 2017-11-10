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
for ant in evtest.antennas:
    plt.plot(ant.time,ant.absE)
plt.show()

#print evtest
