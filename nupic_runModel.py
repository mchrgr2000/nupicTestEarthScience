#!/usr/bin/python
### BY RUGGERO 2017, YCU
# FOR EXECUTING/PUSHING THE NUPIC MODEL 
# AFTER SWARMING
import csv
import time as clk
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic_output import NuPICFileOutput, NuPICPlotOutput
## IMPORT THE RESULTS FROM SWARMING ###
# you have to "touch" __init.py__ in folder model_0
from model_0 import model_params as mp

PSTEPS = 1 # the prediction steps
model_params = mp.MODEL_PARAMS
input_file = "VerylargeSeismData.csv"

def run(fname="verylargeseism_out"):
  print("reading %s"%input_file)
  print("using this model: ",model_params)
  model = ModelFactory.create(model_params)
  model.enableInference({"predictedField": "acc"})
  print("created nupic model in :%f min"%((clk.time()-t0)/60.))
  print("will output predictions and anomalies \n in this file: %s"%fname)  

  output = NuPICFileOutput(fname, show_anomaly_score=True)
  with open(input_file, "rb") as data_input:
    csv_reader = csv.reader(data_input)

    # skip header rows
    csv_reader.next()
    csv_reader.next()
    csv_reader.next()

    # the real data
    for row in csv_reader:
      time = float(row[0])
      acc_value= float(row[1])
      result = model.run({"acc": acc_value})
      output.write(time, acc_value, result, prediction_step=PSTEPS)

  output.close()
  print("time is :%f min"%((clk.time()-t0)/60.))








if __name__ == "__main__":
  t0=clk.time() # reset clock
  run()
