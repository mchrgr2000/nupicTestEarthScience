#!/usr/bin/env python
# ----------------------------------------------------------------------
# generate a random noise similar to seismic signals with jitters
# by R. Micheletto
# 2017 YCU
# ----------------------------------------------------------------------

"""A simple script to generate a CSV with sine data."""

import csv
import math
from numpy import *

JITTER_MAX=5 # maximum jitter amplitude
JITTER_PROBABILITY=1/200. # probability of jitter in 1/(time steps) 
ROWS = 1000
JITTER_DURATION = 25

def jitter(t0,duration,wr,amplitude):
  NFrequencies = 10; f_min=0.01; f_max=0.1; f_coeff=(f_max-f_min)
  freqArray=zeros((NFrequencies))
  amplitude=amplitude/NFrequencies
  # generate array of N random frequencies  
  for f in range(NFrequencies):
     freqArray[f]=random.random()*f_coeff + f_min
  # use these frequencies to generate a random "seismic" impulse
  for t in range(t0,t0+duration):
    time = t # an arbitrary time
    #acc = amplitude*(random.standard_normal()) # between +/-amplitude
    acc=0
    for f in range(NFrequencies):
     acc= acc + amplitude*sin(2* pi * freqArray[f] * t)
    # add the noise
    acc = acc + random.uniform(-1,1) 
    wr.writerow([time, acc])


def run(filename="eQnoise.csv",length=ROWS):
  print "Generating no-earthquake data into %s" % filename
  fileHandle = open(filename,"w")
  writer = csv.writer(fileHandle)
  writer.writerow(["time","acc"])
  writer.writerow(["float","float"])
  writer.writerow(["",""])
  time=0 # arbitrary time
  for k in range(length):
    time=time+1 # update time 
    if random.random()<JITTER_PROBABILITY:
       jitter(t0=time,duration=JITTER_DURATION,wr=writer,amplitude=JITTER_MAX*random.random())
       time=time+JITTER_DURATION # update time
    acc = random.uniform(-1,1)
    writer.writerow([time, acc])

  fileHandle.close()
  print "Generated %i rows of output data into %s" % (length, filename)



if __name__ == "__main__":
  run()
