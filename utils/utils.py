import scipy.signal as signal
import numpy as np
import constant
import math
#########
#time###

from datetime import date
import datetime
def gpstodate(gpssecond):
    return  date.fromtimestamp(gpssecond+315964800)
import datetime
def gpstodatetime(gpssecond):
#    return  datetime.datetime.fromtimestamp(gpssecond+315964800)
    return  datetime.datetime.fromtimestamp(gpssecond)

def tstamptodatetime(tstamp):
    return  datetime.datetime.utcfromtimestamp(tstamp)
def nptstamptodatetime(tstamp):
    date = np.array([])
    for t in tstamp:
        d = tstamptodatetime(t)
        date = np.append(date,d)
#        print t, ' ' , d
    return  date
 
def datettotimestamp(dt):
    if not isinstance(dt, datetime.date):
        print 'you should give a datetime.date or datetime.datetime instance in argument'
        return 
    elif not isinstance(dt, datetime.datetime):
        dt = datetime.datetime(dt.year,dt.month,dt.day) 
    timestamp = (dt - datetime.datetime(1970, 1, 1)).total_seconds()
    return timestamp
    
def datestringtodate(date):
#    print date[:4]
    y = int(date[:4])
    m = int(date[4:6])
    d = int(date[6:8])
    print 'y = ' ,y, ' m = ', m , ' d = ',d
    thedate = datetime.date(y,m,d)
    return thedate



def doytodate(year,doy,hour=None,minute=None):
    if hour == None and minute == None:
        date = datetime.datetime.strptime(str(year)+ ' '+str(doy), '%Y %j')
    elif minute == None:
        date = datetime.datetime.strptime(str(year)+ ' '+str(doy) + ' '+str(hour), '%Y %j %H')
    else:
        date = datetime.datetime.strptime(str(year)+ ' '+str(doy) + ' '+str(hour)+ ' ' +str(minute) , '%Y %j %H %M')
    return date
    
def datetodoy(date):
    year = date.year
    day = int(date.strftime('%j'))
    return (year,day)

def doytoUTC(year,doy,hour=None,minute=None):
    date = doytodate(year,doy,hour,minute)
    tstamp = datettotimestamp(date)
    return tstamp

def UTCtodoy(utc):
    date = tstamptodatetime(utc)
    return datetodoy(date)

def hhmmtosecond(hhmm):
    hh = hhmm/100
    mm = hhmm % 100
    sec = hh*3600 + mm*60
    return sec

def sectohhmm(sec):
    h = int(sec/3600)
    m = int(sec%3600)
    hhmm = h*100+m
    return hhmm

def hhmmtohour(hhmm):
    hh = hhmm/100
    mm = hhmm % 100
    sec = hh*3600 + mm*60
    h = hh + mm.astype(float)/60
    return h

def hourtohhmm(hours):
    hh = hours/100
    hh = hh.astype(int)
    mm = (hours-hh*100)*0.6
    hhmm = hh*100 + mm
    return hhmm

def timetohour(hour,min):
    return hour + float(min)/60.


def readmonittxtfile(filename,gps=None):
    f = open(filename,'r')
    a_val = np.array([])
    a_date = np.array([])
    for l in f:
        ls = l.split()
        a_val = np.append(a_val,float(ls[1]))
        if gps!=None:
            a_date = np.append(a_date,int(ls[0]))
        else:
            a_date = np.append(a_date,gpstodatetime(int(ls[0])))

    return [a_date, a_val]



###############################################
####              filtering               #####
###############################################

def lowpass(amp, sampling, order, fcut):
    Nyfreq = sampling/2
    ratiofcut = float(fcut)/Nyfreq
    b, a = signal.butter(order, ratiofcut, 'low')
    filtered = signal.filtfilt(b, a, amp)
    return filtered

def lowpasshard(amp, sampling, fcut):
    fft = np.fft.rfft(amp)
    freq = np.fft.rfftfreq(len(fft),float(1./sampling))
    Nyfreq = sampling/2
    #    print 'Nyfreq = ' , Nyfreq, 'fcut = ', fcut
    min = np.min(np.absolute(fft))
    ratiofcut = float(fcut)/float(Nyfreq)
    size = len(fft)
    newpass = fft[:int(ratiofcut*size)]
    sizeofzeros = size - len(newpass)
    newcut = np.zeros(sizeofzeros)
    newfft = np.append(newpass,newcut)
    out = np.fft.irfft(newfft)
    return out.real

def highpass(amp, sampling, order, fcut):
    Nyfreq = sampling/2
    ratiofcut = float(fcut)/Nyfreq
    b, a = signal.butter(order, ratiofcut, 'high')
    filtered = signal.filtfilt(b, a, amp)
    return filtered

def highpasshard(amp, sampling, fcut):
    fft = np.fft.rfft(amp)
    freq = np.fft.rfftfreq(len(fft),float(1./sampling))
    Nyfreq = sampling/2
    min = np.min(np.absolute(fft))
    ratiofcut = float(fcut)/Nyfreq
    size = len(fft)
    newpass = fft[int(ratiofcut*size):]
    sizeofzeros = size - len(newpass)
    newcut = np.zeros(sizeofzeros)
    newfft = np.append(newpass,newcut)
    out = np.fft.irfft(newfft)
    return out.real


def slidingwindow(y,bins,option=None):
    window = np.ones(bins)/bins
    if option is not None:
        if option.lower() not in ['full','same','valid']:
            print 'invalid option, check your sliding window'
    if option == None:
        return np.convolve(y,window,'same')
    else:
        return np.convolve(y,window,option)

def matchedfilter(y,sig,option=None):
    filtered = signal.correlate(y,sig, mode='full')
#    filtered = signal.correlate(y,sig, mode='valid')
    return filtered

def vertdepthtoH(vertdepth):
    h0 = 8.4e3
    X0 = 1034
    H = -h0*np.log(vertdepth/X0)
    return H


def gaussian(x, a, b, c):
    return a * np.exp( -(x-b)**2/(2*c**2))


def getpol(id):
    fname = constant.sharedinfofolder + '/polarisation.txt'
    f = open(fname,'r')
    pol= 'EW'
    foundid = False
    for l in f:
        if str(id) == l.split()[0]:
            pol = l.split()[1]
            foundid = True
    if foundid == False:
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        print '!! Id ', id, '  wasn t found, will set the polarisation to EW  !!!!!!!!!!!'
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    return pol



#################################
### simulation function   #######
#################################
def produceresponse(time,amp,gain,tau):
    tend = 500e-9
    period = time[1] - time[0]
    x = np.arange(0,tend,period)
    convfunc = period*np.exp(-x/tau)/( -(math.exp(-tend/tau) - 1)*tau)
    power = gain*(amp**2)/50
    signal = 10*np.log10(power) + 30
    resp = np.convolve(signal,convfunc,'valid')
    newtime = np.linspace(time[0], time[0]+ float(len(resp))*period, len(resp))
    newamp = resp
    return [newtime,newamp]

def produceresponse2(time,amp,gain,tau):
    tend = time[-1] - time[0]
    period = time[1] - time[0]
    x = np.arange(0,tend+period,period)
    convfunc = period*np.exp(-x/tau)/( -(math.exp(-tend/tau) - 1)*tau)
    fft = np.fft.rfft(convfunc)
    power = gain*(amp**2)/50
    signal = 10*np.log10(power) + 30
    fftsig = np.fft.rfft(signal)
    if (len(fft) - len(fftsig) == -1):
        fftsig = fftsig[:-1]
#        fft = np.append(fft,0)
    if (len(fft) - len(fftsig) == 1):
#        fftsig = np.append(fftsig,0)
        fft = fft[:-1]
    out = fft*fftsig
    out = np.fft.irfft(out)
    return [time,out]

def deconv(time,amp,gain,tau):
    tend = time[-1] - time[0]
    period = time[1] - time[0]
    x = np.arange(0,tend+period,period)
    convfunc = period*np.exp(-x/tau)/( -(math.exp(-tend/tau) - 1)*tau)
    fftconv = np.fft.rfft(convfunc)
    fftsig = np.fft.rfft(amp)
    out = fftsig/fftconv
    out = np.fft.irfft(out)
    return [time[:-1],out]

def powerdetfunc2(x,a, k, j):
    return a*np.exp(-(k*x)) + j

def m2_powerdetectorsim(time,amp,gain,capaornot):
    logamp = watttodbm(gain*amp*amp/50) 
    freq = np.fft.rfftfreq(len(time),time[1]-time[0])
    fft = np.fft.rfft(logamp)
    # no capa
    if capaornot == 1: 
        file = constant.c2_file
        phase = np.load(file)['phase']
        freqori = np.load(file)['freq']
        interpphase = np.interp(freq,freqori,phase)
        prefact = constant.c2_prefact
        k = constant.c2_k
        j = constant.c2_j
        spec = powerdetfunc2(freq[1:],prefact,k,j)
        dcval = np.absolute(constant.c2_slope + constant.c2_offset/np.mean(logamp))
        spec = np.insert(spec,0,dcval)
        response = spec*np.exp(1j*interpphase)
        outfft = fft*response
        out = np.fft.irfft(outfft)
    if capaornot == 0: 
        file = constant.nc2_file
        phase = np.load(file)['phase']
        freqori = np.load(file)['freq']
        interpphase = np.interp(freq,freqori,phase)
        prefact = constant.nc2_prefact
        k = constant.nc2_k
        j = constant.nc2_j
        spec = powerdetfunc2(freq[1:],prefact,k,j)
        dcval = np.absolute(constant.nc2_slope + constant.nc2_offset/np.mean(logamp))
        spec = np.insert(spec,0,dcval)
        response = spec*np.exp(1j*interpphase)
        outfft = fft*response
        out = np.fft.irfft(outfft)
    return out

def m3_powerdetectorsim(time,amp,gain,tau,slope,offset):
    size = len(time)
    conv = produceresponse2(time,amp,gain,tau)
    sim = conv[1] 
    polyconv_pd = np.poly1d([slope,offset])
    simpd = polyconv_pd(sim)
    return [conv[0],simpd]

def findparam_3(wfRF,wfPD,t):
    size = len(wfRF[1])
    conv = produceresponse(wfRF[0],wfRF[1],t)
    real = wfPD[1] -  getbaseline(wfPD[1],1)
    sim = conv[1] - getbaseline(conv[1],1)
    #resize the two waveforms to the same size (because of the convolution)                                                                 
    [real,sim] = resize(real,sim)
    time = gettime(wfPD[0],conv[0])
    delay = finddelay2(real,sim)
    simshifted =  np.roll(sim,delay)
    #fit the conv vs power:                                                                                                                 
    fitconv_pd = np.polyfit(simshifted,real,1)
    #polyconv_pd = np.poly1d(fitconv_pd)
    polyconv_pd = np.poly1d([-0.0252,0])
    simpd = polyconv_pd(simshifted)
    return [[time,simpd],[time,real]]


def boardspecfunc(freq,prefact,mu,sigma,k):
    return  prefact*np.exp(-(freq/1e6 - mu)**2/(2*sigma**2)) + k
def boardphasefunc(freq,a,b,c):
    pgainphase  = np.poly1d([a,b,c])
    phase = pgainphase(freq/1e6)
    return phase
    

def resize(amp1,amp2):
    difflen = len(amp1) - len(amp2)
    if difflen == 0:
        return [amp1,amp2]
    elif difflen == 1:
        amp1 = amp1[1:]
    elif difflen == -1:
        amp2 = amp2[:-1]
    elif difflen %2 == 0  and difflen > 0:
        amp1 = amp1[difflen/2:-difflen/2]
    elif difflen %2 == 0  and difflen < 0:
        diff = difflen/2
        amp2 = amp2[diff:-diff]
    elif difflen %2 != 0  and difflen < 0:
        diff = int(np.absolute(float(difflen)/2))
        amp2 = amp2[diff+1:-diff]
    elif difflen %2 != 0  and difflen > 0:
        diff = int(np.absolute(difflen/2))
        amp1 = amp1[diff+1:-diff]
    return [amp1,amp2]


def gettime(time1,time2):
    difflen = len(time1) - len(time2)
    if difflen==1:
        return [time1[:-1],time2]
    elif difflen==-1:
        return [time1,time2[:-1]]
    elif len(time1) > len(time2):
        time1 = time1[difflen/2:-difflen/2]
    elif len(time1) < len(time2):
        time2 = time1[-difflen/2:difflen/2]
    return [time1,time2]

def finddelay2(amp1,amp2):
    fftamp1 = np.fft.fft(amp1)
    fftamp2 = np.fft.fft(amp2)
    cfftamp1 = -fftamp1.conjugate()
    cfftamp2 = -fftamp2.conjugate()
    return np.argmax(np.abs(np.fft.ifft(fftamp1*cfftamp2)))

def alignwaveform(amp1,amp2,pos):
    if pos == True:
        delay = np.argmax(amp1) - np.argmax(amp2)
    else:
        delay = np.argmin(amp1) - np.argmin(amp2)
#    print delay
    amp2 = np.roll(amp2,delay)
    return [amp1,amp2]

def alignwaveform2(amp1,amp2):
    [amp1,amp2] = resize(amp1,amp2)
    delay = finddelay2(amp1,amp2)
    amp2 = np.roll(amp2,delay)
    return [amp1,amp2]

def resample(time, amp, newsampling):
    newtime = np.arange(time[0],time[-1],1/newsampling)
    newamp = np.interp(newtime,time,amp)
    return [newtime,newamp]

def getbaseline(amp, portion):
    size= len(amp)
    return np.mean(amp[:int(size*portion)] )


def linearize(amp):
    amp = adctov_board(amp)
    amp_pd = (amp - constant.boardoffset)/(constant.boardslope)
    power_dbm = (amp_pd - constant.c3_powerdetoffset)/(constant.c3_powerdetslope)
    power_watt = dbmtowatt(power_dbm) 
    return power_watt

def normalize(amp):
    return (amp - np.mean(amp))/np.std(amp)


import pandas as pd
def txtfilereader(filename,pm=None):
    f = open(filename,"r")
    lines = f.readlines()
    ids = lines[0].split()    
    id = int(ids[0])
    stid = int(ids[1])

    es = lines[1].split()
    energy = float(es[0])
    denergy = float(es[1])

    angles = lines[2].split()
    theta = float(angles[0])
    dtheta = float(angles[1])
    phi = float(angles[2])
    dphi = float(angles[3])
    
    dist = lines[3].split()
    x = float(dist[0])
    dx = float(dist[1])
    y = float(dist[2])
    dy = float(dist[3])
    r =  float(dist[4])
    trace = lines[4].split()
    trace = np.asarray(trace, dtype=int)
    if pm==1:
        tracepm = lines[5].split()
        tracepm = np.asarray(tracepm, dtype=int)
        df = pd.DataFrame([[id, stid, energy, denergy, theta, dtheta, phi, dphi, x, dx, y, dy, r, trace, tracepm]], columns=['evid','stid','E','dE','theta','dtheta','phi','dphi','X','dX','Y','dY','R','trace','tracepm'])
    else:
        df = pd.DataFrame([[id, stid, energy, denergy, theta, dtheta, phi, dphi, x, dx, y, dy, r, trace]], columns=['evid','stid','E','dE','theta','dtheta','phi','dphi','X','dX','Y','dY','R','trace'])

    return df

