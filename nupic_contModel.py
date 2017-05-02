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

def run(fname="verylargeseism_out"):
  print(OKBLUE+"generating syntetic earthquakes"+ENDC)
  print("using this model: ",model_params)
  model = ModelFactory.create(model_params)
  model.enableInference({"predictedField": "acc"})
  print("created nupic model in :%f min"%((clk.time()-t0)/60.))
  print("will output predictions and anomalies in this file: %s"%fname)  

  #output = NuPICFileOutput(fname, show_anomaly_score=True)
  with open(input_file, "rb") as data_input:
    csv_reader = csv.reader(data_input)

  # skip header rows
    csv_reader.next()
    csv_reader.next()
    csv_reader.next()
  # prepare graphs
    win= pg.GraphicsWindow(title="window") # make the window#w1 = pg.plot()
    p1=win.addPlot(title="acc value");win.nextRow()
    p2=win.addPlot(title="acc predicted");win.nextRow()
    p3=win.addPlot(title="anomaly")
    N=100 # number of points
    val=zeros((N)) # value
    pre=zeros((N)) # predicted
    ano=zeros((N)) # anomaly
    # the real data
    for row in csv_reader:
      time = float(row[0])
      acc_value= float(row[1])
      result = model.run({"acc": acc_value})
      #output.write(time, acc_value, result, prediction_step=PSTEPS)
      print(OKBLUE+BOLD+"prediction, anomaly:"+ENDC)

      prediction=result.inferences['multiStepBestPredictions'][PSTEPS]
      anomaly=result.inferences['anomalyScore']
       
      # append the value and remove head
      val=delete(val,0);val=append(val,acc_value) 
      pre=delete(pre,0);pre=append(pre,prediction)
      ano=delete(ano,0);ano=append(ano,anomaly) 
      
      p1.plot(val,clear=True,symbolSize=2,symbol="x",symbolPen="w")
      p2.plot(pre,clear=True,symbolSize=2,symbol="x",symbolPen="b")
      p3.plot(ano,clear=True,symbolSize=2,symbol="x",symbolPen="r")
      pg.QtGui.QApplication.processEvents()
      print(prediction,anomaly)
      #raw_input(OKGREEN+"?"+ENDC)
  output.close()
  pg.QtGui.QApplication.exec_()
  print("time is :%f min"%((clk.time()-t0)/60.))


if __name__ == "__main__":
  t0=clk.time() # reset clock
  run()
