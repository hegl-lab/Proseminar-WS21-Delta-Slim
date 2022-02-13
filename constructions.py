'''Constructionos for delta-slim triangles'''

import numpy as np
from hyperbolic.poincare.shapes import Hypercycle, Point, Ideal
from Triangle import Triangle

def deltaLines_of_Line(Line, offset):
    hc1=Hypercycle.fromHypercycleOffset(Line,offset)
    hc2=Hypercycle.fromHypercycleOffset(Line,-offset)
    return [hc1,hc2]

def randomPoints(total, numIdeal=0):
    '''returns a list of hyperbolic points of which numIdeal are ideal points'''
    if total<numIdeal:
        raise ValueError('The total number of points must be greater than number of ideal points')
    rvals = np.random.rand(total-numIdeal)**0.5
    tvals = 2*np.pi*np.random.rand(total)
    pts = [Point.fromPolarEuclid(rvals[k],rad=t) if k<total-numIdeal else Ideal(t) for k, t in enumerate(tvals)]
    np.random.shuffle(pts)
    return pts

def sample(n=1000, precision=16, numIdeal=0):    
    i=0
    DList = []
    while i<n:
        PList=randomPoints(3,numIdeal)
        try:
            Tri=Triangle.fromVertices(PList)
            delta = Tri.approx(precision)
        except:
            continue
        DList.append(delta)
        i=i+1
    return DList

def Data(n, precision, i=0):
    return [sample(n, precision, k) for k in range(i+1)]


