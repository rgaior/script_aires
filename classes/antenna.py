import utils
import constant
import numpy as np

class Antenna:
    def __init__(self, id = 0, x = 0,y = 0, z=0, type='', pol='',input='',stid=0):
        self.id = id        
        self.stid = stid        
        self.X = x
        self.Y = y
        self.Z = z
        self.type = type #'EA61' / 'GDC' / 'GDL'
        self.pol = pol #EW or NS
        self.Ex = np.array([])
        self.Ey = np.array([])
        self.Ez = np.array([])
        self.absE = np.array([])
        self.Exf = np.array([])
        self.Eyf = np.array([])
        self.Ezf = np.array([])
        self.absEf = np.array([])
        self.vtrace = np.array([])
        self.othervtrace = np.array([])
        self.time = np.array([])
        self.theta_xmax = 0
        self.gainmax = 0
        self.sigma = 0
        self.AF = 0
        
    def setantenna(self):
        if self.type == 'EA61' or self.type == None:            
            self.gainmax = np.power(10,constant.gainwsi_db/10)
            self.sigma = constant.sigmawsi 
            self.pol = utils.getpol(self.stid)
            self.AF = self.getAF()
    def getXmax_angle(self, xmaxcoord):
        rho = np.sqrt( (self.X-xmaxcoord[0])**2 + (self.Y-xmaxcoord[1])**2 + (self.Z-xmaxcoord[2])**2)
        theta_xmax = np.arccos( np.abs((self.Z-xmaxcoord[2]))/rho)
        self.theta_xmax = theta_xmax
        
    def getgainatXmax(self,f=None):
        theta = self.theta_xmax*180/np.pi
        gain = utils.gaussian(theta,self.gainmax, 0 , self.sigma)
        return gain
    def getAF(self):
        f= 3.8e9
        c=3e8
        wl = c/f
        gain = self.getgainatXmax()
        AF = 9.73/(wl*gain)
        self.AF = AF
        return AF

    def filtertrace(self):
        binning = 0.1e-9
        fsampling = 1./binning
        if self.type == 'EA61' or self.type == None:            
            f1 = 3.4e9
            f2 = 4.2e9
            order = 2
            Exf = utils.highpass(self.Ex,fsampling,order,f1)
            self.Exf = utils.lowpass(Exf,fsampling,order,f2)
            Eyf = utils.highpass(self.Ey,fsampling,order,f1)
            self.Eyf = utils.lowpass(Eyf,fsampling,order,f2)
            Ezf = utils.highpass(self.Ez,fsampling,order,f1)
            self.Ezf = utils.lowpass(Ezf,fsampling,order,f2)
            absEf = utils.highpass(self.absE,fsampling,order,f1)
            self.absEf = utils.lowpass(absEf,fsampling,order,f2)
            
    # set the final trace of voltage induced by the shower.
    # include the Antenna factor, the polarisation and the filtering
    def setvtrace(self):
        if self.pol == 'NS':
            self.vtrace = self.Exf/self.AF
            self.othervtrace = self.Eyf/self.AF
        else:
            self.vtrace = self.Eyf/self.AF
            self.othervtrace = self.Exf/self.AF

