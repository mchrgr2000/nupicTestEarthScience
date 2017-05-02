#!/usr/bin/python
### BY RUGGERO 2017, YCU
# FOR EXECUTING/PUSHING THE NUPIC MODEL 
# AFTER SWARMING
# run the model FOR EVER 
# 
import csv
import time as clk
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic_output import NuPICFileOutput, NuPICPlotOutput
## IMPORT THE RESULTS FROM SWARMING ###
# you have to "touch" __init.py__ in folder model_0
from model_0 import model_params as mp
from numpy import *
import pyqtgraph as pg
from PyQt4 import QtGui, QtCore
#import generate_data as gd
import random
from pyqtgraph.Qt import QtGui, QtCore
### for white background #####
pg.setConfigOption('background', 'w')  # first set background to white
pg.setConfigOption('foreground', 'k')
app = QtGui.QApplication([])
#FirstLoop=True
t0=clk.time() # reset clock
### SOME COLOR CODES ######
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
 #######################

PSTEPS = 1 # the prediction steps
model_params = mp.MODEL_PARAMS
input_file = "VerylargeSeismData.csv"

global Qlabel # if there is a Quake or not
global N;   N=200 # number of points to plot
global val; val=zeros((0))#[0.0]*N # value
global pre; pre=zeros((0))#[zeros((0))#zeros((0))#0.0]*N # predicted
global ano; ano=zeros((0))#[zeros((0))#0.0]*N # anomaly level
global aMe; aMe=zeros((0))# anomaly sensitivity (peak Anomaly/ peak acceleration)
global err; err=zeros((0))#[zeros((0))#0.0]*N # anomaly average
global mid; mid=zeros((0))#[0.0]*N # error average
global rmsX; rmsX=zeros((0))#[0.0]*N # error RMS
global anoX; anoX=zeros((0))# anomaly averaged

win= pg.GraphicsWindow(title="window") # make the window
p1=win.addPlot(title="acc value")
p2=win.addPlot(title="acc predicted");win.nextRow()
p3=win.addPlot(title="anomaly")
p4=win.addPlot(title="anomaly sensitivity");win.nextRow()
p5=win.addPlot(title="error average")
p6=win.addPlot(title="error RMS/%d points"%N);win.nextRow()
p7=win.addPlot(title="error")
p8=win.addPlot(title="anomaly/%d points"%N)

print(OKBLUE+"generating syntetic earthquakes"+ENDC)
print("using this model: ",model_params)
model = ModelFactory.create(model_params)
model.enableInference({"predictedField": "acc"})
print("created nupic model in :%f min"%((clk.time()-t0)/60.))

#blockSize=N
# generate a block of data, filename is irrilevant if no write on disk
#acc_block = gd.run(fname,blockSize)

#print("generated %d data "%len(acc_block))

# prepare graphs
curve1=p1.plot(symbolSize=2,symbol="x",Pen="k")
curve2=p2.plot(symbolSize=2,symbol="x",Pen="b")
curve3=p3.plot(symbolSize=2,symbol="x",Pen="k")
curve4=p4.plot(symbolSize=2,symbol="x",Pen="b")
curve5=p5.plot(symbolSize=2,symbol="x",Pen="k")
curve6=p6.plot(symbolSize=2,symbol="x",Pen="b")
curve7=p7.plot(symbolSize=2,symbol="x",Pen="y")
curve8=p8.plot(symbolSize=2,symbol="x",Pen="k")
JITTER_MAX=5 # maximum jitter amplitude
JITTER_PROBABILITY=1/200. # probability of jitter in 1/(time steps) 
ROWS = 1000
JITTER_DURATION = 25
def jitter(acc_data,phi0,duration,amplitude):
	NFrequencies = 10; f_min=0.01; f_max=0.1; f_coeff=(f_max-f_min)
	freqArray=zeros((NFrequencies))
	# normalize to the number of frequencies
	amplitude = 2*amplitude/NFrequencies 
	# generate array of N random frequencies  
	for f in range(NFrequencies):
		freqArray[f]=random.random()*f_coeff + f_min
		# use these frequencies to generate a random "seismic" impulse
	for t in range(duration):
		time = t # an arbitrary time
		#acc = amplitude*(random.standard_normal()) # between +/-amplitude
		acc=0
		for f in range(NFrequencies):
			acc= acc + amplitude*sin(2* pi * freqArray[f] * t + phi0)
			# add the noise
			acc = acc + random.uniform(-1,1) 
			acc_data = append(acc_data,acc)
	return acc_data

def plots(acc_value,prediction,anomaly):
		#global acc_value
		global val,pre,ano,anoX,aMe,err,mid,rmsX
		global pChange,Qlabel,N,block
		error=prediction-acc_value # the error
		val=append(val,acc_value) 
		pre=append(pre,prediction)
		ano=append(ano,anomaly)
		block=len(val);
		if block>N:block=N # the chunk of data to evaluate and plot
		#aMe=append(aMe,average(ano[-block:]))
		err=append(err,error) 
		mid=append(mid,average(err[-block:])) 
		curve1.setData(val[-block:]);curve2.setData(pre[-block:])
		curve3.setData(ano[-block:])#;curve4.setData(aMe[-block:])
		curve5.setData(mid[-block:])
		curve7.setData(err[-block:])
		if len(val)%N==0: # % means "reminer/modulus"
			anoX=append(anoX,average(ano[-block:]))
			curve8.setData(anoX) # update this only every N points
			rmsX=append(rmsX,sqrt(average(err[-block:]**2)))
			curve6.setData(rmsX) # update this only every N points
# the real data
Qlabel=False
pChange=0.0000
def Quake():
	global Qlabel
def run():
        global val,pre,ano,anoX,aMe,err,mid,rmsX
	global pChange,Qlabel,N,block
	if random.random()<pChange:Qlabel=not(Qlabel)
	if Qlabel:
		anomaly_array=zeros((0))
		print("earthquake state")
		pChange=0.1
		acc_value_array=jitter(val,random.uniform(-2*pi,2*pi),JITTER_DURATION,JITTER_MAX*random.random())
		jitter_array = acc_value_array[-JITTER_DURATION:] # the jiter array
		jitter_peak = max(abs(jitter_array)) # the peak
		for acc_value in jitter_array:
			result = model.run({"acc": acc_value})
			prediction=result.inferences['multiStepBestPredictions'][PSTEPS]
			anomaly=result.inferences['anomalyScore']
			plots(acc_value,prediction,anomaly)
			anomaly_array=append(anomaly_array,anomaly)
			Qlabel=False
		anomaly_peak=max(anomaly_array)
		aMe=append(aMe,anomaly_peak/jitter_peak)	
		print("aMe",anomaly_peak/jitter_peak)
		print(jitter_array,shape(jitter_array))
		print("ap",anomaly_peak,"jp",jitter_peak)
		curve4.setData(aMe)
	else:
		#print("quiet")
		pChange=0.0
		acc_value= random.uniform(-1,1)
		result = model.run({"acc": acc_value})
		prediction=result.inferences['multiStepBestPredictions'][PSTEPS]
		anomaly=result.inferences['anomalyScore']
		plots(acc_value,prediction,anomaly)
		# append the value and remove head
timer=QtCore.QTimer()
#timer2=QtCore.QTimer()
timer.timeout.connect(run) # connect to the function
timer.start(50)
#timer2.timeout.connect(Quake)
#timer2.start(50)

pg.QtGui.QApplication.exec_()
