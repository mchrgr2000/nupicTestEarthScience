#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'sun'

from numpy import *
import pyqtgraph as pg
from PyQt4 import QtGui, QtCore

import MySQLdb, sys

db = MySQLdb.connect("localhost","root","","csn" )
cursor = db.cursor()
win= pg.GraphicsWindow(title="subplot window") # make the window#w1 = pg.plot()

def getData():
	cursor.execute("SELECT * FROM Event order by id desc limit "+str(N))
	results = cursor.fetchall()
	rs=asarray(results)
	x=rs[:,4];y=rs[:,5];z=rs[:,6]
	r=sqrt(x*x+y*y+z*z);
	return x,y,z,r
########## CREATE GRAPH ################
px=win.addPlot();prx=win.addPlot();win.nextRow()
py=win.addPlot();pry=win.addPlot();win.nextRow()
pz=win.addPlot();prz=win.addPlot();win.nextRow()
#pr=win.addPlot();win.nextRow()
N=3000 # number of points
std=zeros((N));stdx=zeros((N));stdy=zeros((N));stdz=zeros((N))
x,y,z,r=getData()
std[:]=r.std();stdx[:]=x.std();stdy[:]=y.std();stdz[:]=z.std();
while True:
	x,y,z,r=getData()
	d=x.std();stdx=delete(stdx,0);stdx=append(stdx,d); # append the std value and remove head
	d=y.std();stdy=delete(stdy,0);stdy=append(stdy,d); # append the std value and remove head
	d=z.std();stdz=delete(stdz,0);stdz=append(stdz,d); # append the std value and remove head
	#print(shape(x),x)
	px.plot(x-average(x),clear=True,symbolSize=2,symbol="x",symbolPen="b")
	py.plot(y-average(y),clear=True,symbolSize=2,symbol="x",symbolPen="b")
	pz.plot(z-average(z),clear=True,symbolSize=2,symbol="x",symbolPen="b")
#	pr.plot(std,clear=False,symbolSize=2,symbol="o",symbolPen="r")
	prx.plot(stdx,clear=True,symbolSize=2,symbol="o",symbolPen="w")
	pry.plot(stdy,clear=True,symbolSize=2,symbol="o",symbolPen="y")
	prz.plot(stdz,clear=True,symbolSize=2,symbol="o",symbolPen="b")
        pg.QtGui.QApplication.processEvents()
pg.QtGui.QApplication.exec_()



#pg.QtGui.QApplication.processEvents()
#while True:
#	pass



