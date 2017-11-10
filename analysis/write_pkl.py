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
if type == 'real':
    stid = file[file.rfind('st_')+3:file.rfind('.inp')]
    print 'stid = ' , stid
else:
    stid = 0
evtest = event.Event(id=1,type=type,inputfolder=folder, inputfile=file)
evtest.fillevent()
evtest.fillantennas()
evtest.fillsryinfo()


#######################################
## save in pkl format the event data ##
#######################################

outfolder = constant.eventfolder 
outfilename = outfolder + str(file[:-4] ) + '.pkl'
out = open(outfilename,'wb')
pickle.dump(evtest,out)
out.close()
