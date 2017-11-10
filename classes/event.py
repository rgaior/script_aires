import utils
import constant
import numpy as np
import antenna
import shower
pi = np.pi
class Event:
    def __init__(self, id = 0, type='',inputfolder='', inputfile=''):
        self.id = id
        self.type = type
        self.inputfolder = inputfolder
        self.inputfile = inputfile
        self.antnr = 0
        self.showernr = 0
        self.antennas = []
        self.showers = []
        self.antpos = []

        self.energy = 0
        self.theta = 0
        self.phi = 0
        self.part = ''
        self.vertdepth = 0
        self.slantdepth = 0
        self.HXmax = 0
        self.XmaxCoord = []
        
#fill the event with info with the input text file 
    def fillevent(self):
        antcount = 0
        f = open(self.inputfolder + self.inputfile)
        for l in f:
            if 'PrimaryParticle' in l:
                part = l.split()[1]
            if 'PrimaryEnergy' in l:
                energy = float(l.split()[1])
                eunit = l.split()[2]
                self.energy = energy*constant.econv[eunit]
            if 'PrimaryZenAngle' in l:
                self.theta = float(l.split()[1]) # deg
            if 'PrimaryAzimAngle' in l:
                self.phi = float(l.split()[1]) # deg
            if 'TotalShowers' in l:
                self.showernr = int(l.split()[1]) # deg
            if 'AddAntenna' in l:
                antcount+=1
                [x,y,z] = [float(l.split()[1]),float(l.split()[2]),float(l.split()[3])]
                # set the z to a.s.l. instead of malargue reference
                self.antpos.append([x,y,z + constant.zmalargue])
        self.antnr = antcount
        f.close()
#fill the antenna info and traces with the text file timefresnel-root.dat
    def fillantennas(self,stid=None):
        f = open(self.inputfolder + '/timefresnel-root.dat')
        lines = f.readlines()
        time = np.array([])
        traces = []
        first = True        
        for j in range(self.showernr):
            sh = shower.Shower(id=j)
            for i in range(self.antnr):
                pos = self.antpos[i]
                ant = antenna.Antenna(i,pos[0],pos[1],pos[2],'EA61','EW',self.inputfolder,stid)
                sh.antennas.append(ant)
            self.showers.append(sh)
        newant = False
        curant = 0
        curshower = 0
        for l in lines[10:]:
            if 'new shower' in l:
                print ' l ', l
                showernr = int(l.split()[3])
                print 'showernr = ' , showernr
                curshow = self.showers[showernr-1]
                continue
            elif '#' in l:
                continue
            ls = l.split()
            [showernr, antnr,x,y,z,t,absA,Ax,Ay,Az,absE,Ex,Ey,Ez] = [int(ls[0]),int(ls[1]),float(ls[2]),float(ls[3]),float(ls[4]),float(ls[5]),float(ls[6]),float(ls[7]),float(ls[8]),float(ls[9]),float(ls[10]),float(ls[11]),float(ls[12]),float(ls[13])] 
#            if (antnr == curant)  and (showernr == curshower):
#                newant = False                
#                time = np.append(time,t)
            curshow.time = time
            curshow.antennas[antnr-1].time = np.append(curshow.antennas[antnr-1].time,t)
            curshow.antennas[antnr-1].Ex = np.append(curshow.antennas[antnr-1].Ex,Ex)
            curshow.antennas[antnr-1].Ey = np.append(curshow.antennas[antnr-1].Ey,Ey)
            curshow.antennas[antnr-1].Ez = np.append(curshow.antennas[antnr-1].Ez,Ez)
            curshow.antennas[antnr-1].absE = np.append(curshow.antennas[antnr-1].absE,absE)
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
    
        f.close()

    def fillsryinfo(self):
        sryfile = self.inputfolder + self.inputfile[:-4] + '.sry'
        f = open(sryfile,'r')
        for l in f:
            if 'Vt. depth of max. (g/cm2):' in l:
                vertdepth = float(l.split()[5])
                print 'vertdepth = ',vertdepth
            if 'Sl. depth of max. (g/cm2):' in l:
                sldepth = float(l.split()[5])
                print 'sldepth = ',sldepth
        self.vertdepth = vertdepth
        self.slantdepth = sldepth
        self.HXmax = utils.vertdepthtoH(self.vertdepth)
        
        rho = self.HXmax/np.cos(self.theta*pi/180)
        XmaxCoord = rho*np.array([np.sin(self.theta*pi/180)*np.cos(self.phi*pi/180) , np.sin(self.theta*pi/180)*np.sin(self.phi*pi/180) , np.cos(self.theta*pi/180)])
        self.XmaxCoord = XmaxCoord

    def printevent(self):
        print '############## PRINT EVENT ##################'
        print '###### event nr: ', self.id , ' of type : ', self.type , '#####'
        print '###### E = ', self.energy, ' theta = ' , self.theta, ' phi = ', self.phi , '#####'
        print '###### number of antennas: ', self.antnr, ' ######'
        print '###### antennas pos: ', self.antpos, ' ######'
        print '#############################################'


