#!/usr/bin/python

# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
import csv
import time as clk
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic_output import NuPICFileOutput, NuPICPlotOutput
from nupic.swarming import permutations_runner

import generate_data

# Change this to switch from a matplotlib plot to file output.

PSTEPS = 1 # prediction steps
PLOT = False
SWARM_CONFIG = {
  "includedFields": [
    {
      "fieldName": "acc",
      "fieldType": "float",
      "maxValue": 15.0,
      "minValue": -15.0
    }
  ],
  "streamDef": {
    "info": "acc",
    "version": 1,
    "streams": [
      {
        "info": "eQnoise.csv",
        "source": "file://eQnoise.csv",
        "columns": [
          "*"
        ]
      }
    ]
  },
  "inferenceType": "TemporalAnomaly",
  "inferenceArgs": {
    "predictionSteps": [
      PSTEPS
    ],
    "predictedField": "acc"
  },
  "swarmSize": "large"
}



def swarm_over_data():
  return permutations_runner.runWithConfig(SWARM_CONFIG,
    {'maxWorkers': 4, 'overwrite': True})



def run_seism_experiment():
  input_file = "eQnoise.csv"
  generate_data.run(input_file)
  print("time is :%f secs"%((clk.time()-t0)/60.))
  model_params = swarm_over_data()
  print("time is :%f secs"%((clk.time()-t0)/60.))
  print(model_params)
  if PLOT: 
    pass
    #output = NuPICPlotOutput("sine3_output", show_anomaly_score=True)
  else:
    output = NuPICFileOutput("eQnoise_output", show_anomaly_score=True)
  print("time is :%f min"%((clk.time()-t0)/60.))
  model = ModelFactory.create(model_params)
  model.enableInference({"predictedField": "acc"})

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
  run_seism_experiment()
