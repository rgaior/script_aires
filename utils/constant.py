econv = {'keV':1e3,'MeV':1e6,'GeV':1e9,'TeV':1e12,'PeV':1e15,'EeV':1e18}

airesanalysisfolder ='/Users/gaior/EASIER/aires_analyse/data/'
eventfolder = airesanalysisfolder + '/eventpkl/'
sharedinfofolder = '/Users/gaior/EASIER/data/shared/'

zmalargue = 1400
gainwsi_db = 8.5 # dB
sigmawsi = 30 # deg


###########################################
## from detector sim and simulations/    ##
###########################################

kb = 1.38e-23
impedance = 50 # ohm


#############################
#### detector constants #####
#############################

## SD front end filter frequency cut ##
fefcut = 20e6 #Hz
## SD front end sampling rate ##
fesampling = 40e6 #S/s

########################
## constant for powerdetector with capacitor ##
##1rst method
c_powerdetoffset = 0.816
c_powerdetslope = -0.0217
c_powerdettau = 34.8e-9


## 3rd method
c3_powerdetoffset = 0.684
c3_powerdetslope = -0.0252
c3_powerdettau = 41.5e-9


##2nd method
##spec param:
c2_slope = -0.0252
c2_offset = 0.684
c2_prefact = 0.02408611
c2_k = 7.6977e-08
c2_j = 0.00138642
c2_dc = 0.04282547
#c2_file = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/test/capameanspec.npz'
c2_file = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/method2/capa/meanspec.npz'

## constant for power detector **without** capacitor ##
nc_powerdetoffset = 0.88
nc_powerdetslope = -0.0192
nc_powerdettau = 4.7e-9
##2nd method
##spec param:
nc2_slope = -0.0252
nc2_offset = 0.684
nc2_prefact = 0.02463391
nc2_k = 1.0523e-08
nc2_j = 0.00148898
nc2_dc = 0.04282547
#nc2_file = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/test/nocapameanspec.npz'
nc2_file = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/method2/nocapa/meanspec.npz'

## 3rd method
nc3_powerdetoffset = 0.684
nc3_powerdetslope = -0.0252
nc3_powerdettau = 6.3e-9
#nc3_powerdettau = 100e-9

#########################
## board carac:
## 1rst method
boardoffset = 5.923
boardslope = -4.19
## 2nd method:
## spectrum paramaters:
boardspecprefact = 3.86
boardspecmu = -40
boardspecsigma = 75.1
boardspeck = 1
## phase param:
boardphasea = 4.8e-5
boardphaseb = -1.1e-3
boardphasec = 2.97


##############
# detector dependant parameter:
meantempdict = {'EASIER':106,'GDC':58,'GDL':115} # average system temperature over the detector calibrated in K


eventdictpath = {111805504700:'/2011/bugfix/EA7_11180550470_342.txt',122492304500:'/2012/bugfix/EA61_12249230450_441.txt',130028056800:'//2013/bugfix/EA61_13002805680_429.txt',131547409900:'/2013/bugfix/EA61_13154740990_125.txt',131965595200:'/2013/bugfix/EA61_13196559520_196.txt',132692307400:'/2013/bugfix/EA61_13269230740_308.txt',150343910801:'/2015/bugfix/EA61_15034391080_405.txt'}

##############################
###    folder path    ########
##############################
basefolder = '/Users/gaior/EASIER/detectorsim/'
spectrafolder = basefolder + 'data/spectra/'
resultfolder = basefolder + 'results/'
calibdatafolder = basefolder + 'data/'
