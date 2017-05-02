#!/usr/bin/env python
import pyqtgraph as pg
from numpy import *


#import pandas as pd
#h=pd.read_csv("sine_output.csv",sep=",",header=1 )
fname=raw_input("file name ? ")
M=loadtxt(fname+'.csv',skiprows=3,delimiter=",")
print("array shape: ",shape(M))
dimensions=shape(M)[1]
print(dimensions)
t=M[:,0]
acc=M[:,1]
if dimensions>2: pred=M[:,2]
if dimensions>3: an=M[:,3]
print(shape(t),shape(acc))
# plotting 
win= pg.GraphicsWindow(title="subplot window") # make the window
p=win.addPlot(title="fig 1");
p.plot(t,acc)
if dimensions>2: p.plot(t,pred,pen='b')
if dimensions>3: 
	p.plot(t,an,pen='c')
	win.nextRow()
	p=win.addPlot(title="fig 2")
	p.plot(t,an,pen='c')

pg.QtGui.QApplication.exec_()

