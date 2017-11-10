import utils
import numpy as np

class Shower:
    def __init__(self, id = 0,type='',input=''):
        self.id = id        
        self.type = type
        self.time = []

        self.energy = 0
        self.theta = 0
        self.phi = 0
        self.part = ''
        self.vertdepth = 0
        self.slantdepth = 0
        self.HXmax = 0
        self.XmaxCoord = []
        self.antennas = []
        
        # #fill the antenna info and traces with the text file timefresnel-root.dat
#     def fillantennas(self,stid=None):
#         f = open(self.inputfolder + '/timefresnel-root.dat')
#         lines = f.readlines()
#         time = np.array([])
#         traces = []
#         first = True        
#         for i in range(self.antnr):
#             pos = self.antpos[i]
#             ant = antenna.Antenna(i,pos[0],pos[1],pos[2],'EA61','EW',self.inputfolder,stid)
#             self.antennas.append(ant)
#         newant = False
#         curant = 0
#         curshower = 0
#         for l in lines[20:]:
#             if '#' in l:
                
#             if l == lines[-1]:
#                 print 'last line............'
#                 self.antennas[curant-1].Ex = aEx
#                 self.antennas[curant-1].Ey = aEy
#                 self.antennas[curant-1].Ez = aEz
#                 self.antennas[curant-1].absE = aabsE
#                 self.antennas[curant-1].time = time

#             ls = l.split()
#             [showernr, antnr,x,y,z,t,absA,Ax,Ay,Az,absE,Ex,Ey,Ez] = [int(ls[0]),int(ls[1]),float(ls[2]),float(ls[3]),float(ls[4]),float(ls[5]),float(ls[6]),float(ls[7]),float(ls[8]),float(ls[9]),float(ls[10]),float(ls[11]),float(ls[12]),float(ls[13])] 
# #            print 'antnr == ' , antnr , ' curant = ', curant ,'  showernr = ',showernr ,' curshower =: ', curshower
#             if (antnr == curant)  and (showernr == curshower):
#                 newant = False                
#                 time = np.append(time,t)
#                 aEx = np.append(aEx,Ex)
#                 aEy = np.append(aEy,Ey)
#                 aEz = np.append(aEz,Ez)
#                 aabsE = np.append(aabsE,absE)
#             else:
#                 if (first==False):
#                     self.antennas[curant-1].Ex = aEx
#                     self.antennas[curant-1].Ey = aEy
#                     self.antennas[curant-1].Ez = aEz
#                     self.antennas[curant-1].absE = aabsE
#                     self.antennas[curant-1].time = time
#                     print time
#                 newant = True                
#                 curant = antnr 
#                 curshower = showernr                
#                 time = np.array([])
#                 time = np.append(time,t)
#                 aEx = np.array([])
#                 aEx = np.append(aEx,Ex)
#                 aEy = np.array([])
#                 aEy = np.append(aEy,Ey)
#                 aEz = np.array([])
#                 aEz = np.append(aEz,Ez)
#                 aabsE = np.array([])
#                 aabsE = np.append(aabsE,absE)
#                 first = False
# #        utils.geteventinfo(self.inputfile, self.antenna)
# #        utils.fillantenna(self.inputfile)
    
#         f.close()

        
