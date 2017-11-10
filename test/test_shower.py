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
parser.add_argument("inpfile", type=str, nargs='?',default='/Users/gaior/aires/example/e_18.5/e_18_5.inp', help="full input file name")
parser.add_argument("type", type=str, nargs='?',default='test', help="type of simulated shower, test or real")
args = parser.parse_args()
evname = args.inpfile
type = args.type

#folder = constant.simfolder + 'inp'
folder = evname[:evname.rfind('/')+1] 
file = evname[evname.rfind('/')+1:]
evtest = event.Event(id=1,type=type,inputfolder=folder, inputfile=file)
evtest.fillevent()
if type == 'real':
    stid = file[file.rfind('st_')+3:file.rfind('.inp')]
    try:
        val = int(stid)
    except ValueError:
        stid = file[file.rfind('st_')+3:file.rfind('_')]
        print("That's not an int!")
    print 'stid = ' , stid
else:
    stid = 0
evtest.fillantennas(stid=int(stid))
evtest.fillsryinfo()

#######################################                                                                                                               
## save in pkl format the event data ##                                                                                                               
#######################################                                                                                                               
#outfolder = constant.eventfolder 
# outfilename = outfolder + str(file[:-4] ) + '.pkl'
# out = open(outfilename,'wb')
# pickle.dump(evtest,out)
# out.close()

evtest.printevent()
for shower in evtest.showers:
    print shower.id
    fig = plt.figure()
    for ant in shower.antennas:
        ant.getXmax_angle(evtest.XmaxCoord)
        ant.setantenna()
        gain = ant.getgainatXmax()
        ant.filtertrace()
        ant.setvtrace()
#    plt.plot(ant.time,ant.vtrace,label='final trace')
#    plt.plot(ant.time,ant.Ex,label='Ex')
#    plt.plot(ant.time,ant.Ey,label='Ey')
#    plt.plot(ant.time,ant.Ez,label='Ez')
        plt.plot(ant.time,ant.vtrace**2/50,label='P')
        print 'AF = ' , ant.AF
plt.legend()
plt.show()

#print evtest
