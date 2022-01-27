# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 12:53:04 2021

@author: Simon Heidrich
"""
from Triangle import *
from constructions import *
from hyperbolic.poincare.shapes import *
from hyperbolic.euclid.shapes import Arc
from hyperbolic.euclid import intersection
from hyperbolic.euclid.intersection import InfiniteIntersections, SingleIntersection, \
                                  NoIntersection

class deltaNBH:
    def __init__(self, subShape):
        assert isinstance(subShape, (Triangle))
        subShape = self.subShape

def innerInterPoint(triangle, vertNum, delta):
    '''only tested a bit yet'''
    ips=triangle.offsetEdge(vertNum-1,delta).intersectionsWithHcycle(triangle.offsetEdge(vertNum,delta))
    pts=[p for p in ips if not p.isIdeal()]
    assert len(pts)==1
    return pts[0]
    #TODO determine valid ip out of ips

def offsetEdgeIntersectionPoint(triangle, edgeNum, delta):
    hc1 = triangle.offsetEdge(edgeNum+1, delta)
    hc2 = triangle.offsetEdge(edgeNum-1, delta)
    pts=[p for p in hc1.intersectionsWithHcycle(hc2) if not p.isIdeal()]
    assert len(pts)==1      #fails for bad geometry
    return pts[0]


def deltaNbh(triangle, drawing, delta, edgeNum=0, **kwargs):
    '''needs change'''
    k=edgeNum
    sCap = triangle.endCap(k, k-1, delta)
    v2 = triangle.offsetVertice(k, k-1, delta, inner=False)
    v3 = triangle.offsetVertice(k-1, k-1, delta, inner=False)
    sOutLine = triangle.offsetEdge(k-1, delta, inner=False).trimmed(*v2, *v3)
    mCap = triangle.midCap(k-1, delta)
    v4 = triangle.offsetVertice(k-1, k+1, delta, inner=False)
    v5 = triangle.offsetVertice(k+1, k+1, delta, inner=False)
    eOutLine = triangle.offsetEdge(k+1, delta, inner=False).trimmed(*v4, *v5)
    eCap = triangle.endCap(k+1, k+1, delta)
    sInLine = triangle.offsetEdge(k-1, delta, inner=True)     #needs to be trimmed
    eInLine = triangle.offsetEdge(k+1, delta, inner=True)
    #TODO: get correct intersections between sCap, sInLine, eInLine and eCap \
    # implement this into class and write toDrawables and toPath       

lineStyle1 = dict(fill='red', fill_opacity=1)

def deltaNeigbourhood(triangle, drawing, delta, edgeNumber=0):
    for i,l in enumerate(triangle.edges):
        if not triangle.vertices[i].isIdeal():
            drawing.draw(Circle.fromCenterRadius(triangle.vertices[i], delta),**lineStyle1)
        if i==edgeNumber:
            continue
        else:
            drawing.draw(l, hwidth=2*delta, **lineStyle1)






