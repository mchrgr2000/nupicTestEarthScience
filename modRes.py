#!/usr/bin/python
### BY RUGGERO 2017, YCU
# FOR EXECUTING/PUSHING THE NUPIC MODEL 
# AFTER SWARMING
# run the model FOR EVER 
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
import generate_data as gd

#FirstLoop=True
win= pg.GraphicsWindow(title="window") # make the window
p1=win.addPlot(title="acc value");win.nextRow()
p2=win.addPlot(title="acc predicted");win.nextRow()
p3=win.addPlot(title="anomaly")
t0=clk.time() # reset clock
#pg.QtGui.QApplication.exec_()
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

global N;   N=1000 # number of points to plot
global val; val=zeros((N+1)) # value
global pre; pre=zeros((N+1)) # predicted
global ano; ano=zeros((N+1)) # anomaly

print(OKBLUE+"generating syntetic earthquakes"+ENDC)
print("using this model: ",model_params)
model = ModelFactory.create(model_params)
model.enableInference({"predictedField": "acc"})
print("created nupic model in :%f min"%((clk.time()-t0)/60.))

def run(WinHandle=0,fname="verylargeseism_out"):
	global N, val, pre, ano
        p1=WinHandle[0]
        p2=WinHandle[1]
        p3=WinHandle[2]
        blockSize=N
	# generate a block of data, filename is irrilevant if no write on disk
	acc_block = gd.run(fname,blockSize)
	print("generated %d data "%len(acc_block))

	#output = NuPICFileOutput(fname, show_anomaly_score=True)
	#  with open(input_file, "rb") as data_input:
	#    csv_reader = csv.reader(data_input)

	# skip header rows
	#    csv_reader.next()
	#    csv_reader.next()
	#    csv_reader.next()
	# prepare graphs
	# the real data
	for t, acc in enumerate(acc_block):
		time = float(t)
		acc_value= float(acc_block[t])
		result = model.run({"acc": acc_value})
		print(result)
		#output.write(time, acc_value, result, prediction_step=PSTEPS)
		#print(OKBLUE+BOLD+"prediction, anomaly:"+ENDC)

		prediction=result.inferences['multiStepBestPredictions'][PSTEPS]
		anomaly=result.inferences['anomalyScore']

		# append the value and remove head
		val[t]=acc_value 
		pre[t]=prediction
		ano[t]=anomaly 

		#print(prediction,anomaly)
		#raw_input(OKGREEN+"?"+ENDC)
		#output.close()
		pg.QtGui.QApplication.processEvents()
	p1.plot(val,clear=True,symbolSize=2,symbol="x",symbolPen="w")
	p2.plot(pre,clear=True,symbolSize=2,symbol="x",symbolPen="b")
	p3.plot(ano,clear=True,symbolSize=2,symbol="x",symbolPen="r")
	tt=OKBLUE+"time is :%f min"+ENDC
	print(tt%((clk.time()-t0)/60.))


if __name__ == "__main__":
        while True: run(WinHandle=[p1,p2,p3])
