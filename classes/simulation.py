import utils
import math
import numpy as np
import constant
#import waveform

class Simulation:
    def __init__(self, snr = 0,
                 siglength = 0,
                 sampling= None,
                 det = None):
        
        self.snr = snr
        self.det = det
        self.siglength = siglength
        
        self.powerenvelope = np.array([])
 
        self.time = np.array([])
        self.noise = np.array([])
        self.signal = np.array([])
        self.envelope = np.array([])
        self.wf = np.array([])
        
        #hardcoded
        self.tracelength = 20e-6 #s
        if sampling ==None:
            self.sampling = 8e9 #Hz
        else:
            self.sampling = sampling
#        self.sampling = 5e9 #Hz
#        self.sigtime = self.tracelength/4
        self.sigtime = 0.31*self.tracelength


    def producetime(self):
        self.time = np.arange(0,self.tracelength,1./self.sampling)
        
    #produce the noise samples (according gauss dist)
#    def producenoise(self):
#        Pnoise = constant.kb*self.det.temp*(self.det.f2 - self.det.f1)
#         Pnoise = constant.kb*self.det.temp*self.det.bw 
#         Vnoise = np.sqrt(constant.impedance*Pnoise)
#         self.noise = utils.wf_normal(0,Vnoise,len(self.time))

    def producenoise(self,realistic=None):
        if realistic == None:
            self.noise = self.producenoisewf()
        elif realistic == True:
            self.noise = self.producenoisewfreal()

    def producenoisewf(self):
        self.det.setpnoise()
        #first produce the right spectrum:
        # we produce an fft with a flat spectrum and random phase:
        nyfreq = 0.5*self.sampling
        freqsamp = 1./self.tracelength
        freq = np.arange(0,nyfreq,freqsamp)
        spec = np.zeros(len(freq))
        phase = np.zeros(len(freq))
        size = len(freq[(freq > self.det.f1) & (freq < self.det.f2)])
        spec[(freq > self.det.f1) & (freq < self.det.f2)] = np.ones(size)
        phase[(freq > self.det.f1) & (freq < self.det.f2)] = np.random.uniform(-math.pi, math.pi, size)
        fft = spec*np.exp(1j*phase)
        #norm fft:
        sumsquare = np.sum(np.absolute(fft)**2)
        fft = fft/np.sqrt(sumsquare)
        Pnoise = self.det.pnoise
        fft = fft*np.sqrt(2*len(freq)*len(freq)*Pnoise*50)
        timewf = np.fft.irfft(fft)
        return timewf

    def producenoisewfreal(self):
        #first produce the right spectrum:
        # we produce an fft with the detector spectrum and random phase:
        nyfreq = 0.5*self.sampling
        freqsamp = 1./self.tracelength
        print 'nyfreq = ', int(nyfreq)
        print 'freqsamp = ', freqsamp
        freq = np.arange(0,nyfreq,freqsamp)
        spec = np.zeros(len(freq))
        phase = np.zeros(len(freq))
        print ' len(freq) = ' ,  len(freq) 
        noisespec = self.det.noisespectrum
        freqspec = noisespec[0]
        specspec = noisespec[1]
        insidefreq = freq[ (freq > freqspec[0]) & (freq < freqspec[-1]) ]
        size = len(insidefreq)
        insidespec = np.interp(insidefreq,freqspec,specspec)
        spec[ (freq > freqspec[0]) & ( freq < freqspec[-1]) ] = np.sqrt(insidespec)
        phase[(freq > freqspec[0]) & (freq < freqspec[-1])] = np.random.uniform(-math.pi, math.pi, size)
        fft = spec*np.exp(1j*phase)
        #norm fft:
        sumsquare = np.sum(np.absolute(fft)**2)
        fft = fft/np.sqrt(sumsquare)
        Pnoise = self.det.pnoise
        #        Pnoise = constant.kb*self.det.temp*(self.det.f2 - self.det.f1)
        fft = fft*np.sqrt(2*len(freq)*len(freq)*Pnoise*50)
        timewf = np.fft.irfft(fft)
        print 'len(timewf) = ' ,len(timewf)
        if len(timewf) - len(self.time) == -1:
            timewf = np.append(timewf, timewf[len(timewf)/2]) 
        if len(timewf) - len(self.time) == -2:
            timewf = np.append(timewf, timewf[len(timewf)/2]) 
            timewf = np.append(timewf, timewf[len(timewf)/3]) 
        return timewf

    # in case we want a simple fake signal
    # a gaussian is implemented as example
    def setpowerenvelope(self, type):
        if type == 'gauss':
            Psig = self.snr*self.det.pnoise
            powerenvelope =  Psig*utils.func_normedgauss(self.time,self.sigtime,self.siglength)
        self.powerenvelope = powerenvelope

    # method to import a power profile from a file
    def setpowerenvelopewithfile(self, file):
        # get the envelope (time vs power [W]) from a file
        timepower = utils.readsimfile(file)
        # first shift the signal i.e. add or remove some time shift w.r.t. maximum
        # to set the max at the set value
        timeofmax = timepower[0][np.argmax(timepower[1])]
        timepower[0] = timepower[0] - timeofmax + self.sigtime
        # then resample
        # when the original array is smaller than the interpolated, the default interpolation done with numpy 
        # sets the outside points to the last value.
        # we want to be sure that the power outside the limit of the given signal is low (but not zero because of the future log10)
        maxfactor = 1e-10
        max = np.max(timepower[1])
        newamp = np.interp(self.time,timepower[0],timepower[1],left = maxfactor*max,right = maxfactor*max)
        powerenvelope = newamp
        self.powerenvelope = powerenvelope


    # method to import a voltage profile from an array
    # this function suits the time and sampling and lenght of the trace
    def setsignalwitharrays(self,time,amp):
        # first shift the signal i.e. add or remove some time shift w.r.t. maximum
        # to set the max at the set value
        timeofmax = time[np.argmax(amp)]
        time = time - timeofmax + self.sigtime
        # then resample
        # when the original array is smaller than the interpolated, the default interpolation done with numpy 
        # sets the outside points to the last value.
        # we want to be sure that the power outside the limit of the given signal is low (but not zero because of the future log10)
        maxfactor = 1e-10
        max = np.max(amp)
        newamp = np.interp(self.time,time,amp,left = maxfactor*max,right = maxfactor*max)
        if np.abs(len(newamp) - len(self.time)) > 2:
            print 'priblem in the lenght of the interpolated amplitude see setsignalwitharrays() '
        if len(newamp) - len(self.time) == 1:
            newamp = newamp[:-1]
        self.signal = newamp

     #produce the signal in time vs amplitude [V]
    def producesignal(self):
        #        signal = utils.wf_normal(0,1,len(self.time)
        if self.det.type=='':
            noisewf = self.producenoisewf()
        else:
            noisewf = self.producenoisewfreal()
        noisewf = noisewf/(np.sqrt(np.mean(noisewf**2)))
        self.signal = np.sqrt(self.powerenvelope*constant.impedance)*noisewf
