import math
import drawSvg as draw
from constructions import *
from deltaNeigbourhood import *
from hyperbolic.poincare.shapes import *
from Triangle import *
import matplotlib.pyplot as plt
import numpy as np


#no ideals
i=0
DList = []
while i<100:
    PList=randomPoints(3)
    p1=PList[0]
    p2=PList[1]
    p3=PList[2]
    #p1=Ideal(PList[0].theta)
    #p2=Ideal(PList[1].theta)
    #p3=Ideal(PList[2].theta)
    PList=[p1,p2, p3]
    Tri=Triangle.fromVertices(PList)
    delta = Tri.approx()
    DList[i]=delta
    i=i+1
i=0
k=0
l=0
m=0.1
CList=[]
while k<10:
    while i<100:
        if DList[i]<m and DList[i]>l: 
            CList[k]=CList[k]+1
    l=l+0.1
    m=m+0.1       

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
interval = ['0.0-0.1','0.1-0.2','0.2-0.3','0.3-0.4','0.4-0.5','0.5-0.6','0.6-0.7','0.7-0.8','0.8-0.9','0.9-1.0' ]
ax.bar(interval,CList)
plt.show()

