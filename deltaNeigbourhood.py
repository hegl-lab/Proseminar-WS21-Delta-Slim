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

def intersectionsCap(cap, line):
    x1, y1 = 1, 1  # Default, invalid
    x2, y2 = 1, 1  # Default, invalid
    try:
        if isinstance(cap, (Arc,Circle)):
            if isinstance(line, (Arc,Circle)):
                x1, y1, x2, y2 = intersection.circleCircle(cap, line)
            elif isinstance(line, Hypercycle):
                if isinstance(line.projShape, (Arc,Circle)):
                    x1, y1, x2, y2 = intersection.circleCircle(cap, line.projShape)
                elif isinstance(line.projShape, ELine):
                    x1, y1, x2, y2 = intersection.circleLine(cap, line.projShape)
    except InfiniteIntersections as e:
        raise e from None
    except SingleIntersection as e:
        x1, y1 = e.args
    except NoIntersection:
        x1, y1 = 1, 1  # Invalid
    pts = []
    try:
        pts.append(Point.fromEuclid(x1, y1))
    except ValueError: pass
    try:
        pts.append(Point.fromEuclid(x2, y2))
    except ValueError: pass
    valid = [p for p in pts if (isPointOnSegment(cap, *p) and isPointOnSegment(line, *p))]
    return valid


def deltaNbh(triangle, delta, edgeNum=0):
    k=edgeNum
    sCap = triangle.endCap(k, k-1, delta)
    v2 = triangle.offsetVertice(k, k-1, delta, inner=False)
    v3 = triangle.offsetVertice(k-1, k-1, delta, inner=False)
    sOutLine = triangle.offsetEdge(k-1, delta, inner=False).trimmed(*v2, *v3, chooseShorter=True)
    mCap = triangle.midCap(k-1, delta)
    v4 = triangle.offsetVertice(k-1, k+1, delta, inner=False)
    v5 = triangle.offsetVertice(k+1, k+1, delta, inner=False)
    eOutLine = triangle.offsetEdge(k+1, delta, inner=False).trimmed(*v4, *v5, chooseShorter=True)
    eCap = triangle.endCap(k+1, k+1, delta)
    v1 = triangle.offsetVertice(k, k-1, delta, inner=True)
    v6 = triangle.offsetVertice(k+1, k+1, delta, inner=True)
    temp7 = triangle.offsetVertice(k-1, k+1, delta, inner=True)
    temp8 = triangle.offsetVertice(k-1, k-1, delta, inner= True)
    sInLine = triangle.offsetEdge(k-1, delta, inner=True).trimmed(*temp8, *v1, chooseShorter=True)
    eInLine = triangle.offsetEdge(k+1, delta, inner=True).trimmed(*v6, *temp7, chooseShorter=True)
    if len(intersectionsCap(sCap, eCap))==1:
        v1 = intersectionsCap(sCap, eCap)[0]
        sCap = sCap.trimmed(*v1, *v2, chooseShorter=True)
        eCap = eCap.trimmed(*v5, *v1, chooseShorter=True)
        vertices , edges = [v1, v2, v3, v4, v5], [sCap, sOutLine, mCap, eOutLine, eCap]
    elif len(intersectionsCap(sCap, eInLine))==1:
        v6 = triangle.offsetVertice(k+1, k+1, delta, inner=True)
        v1 = intersectionsCap(sCap, eInLine)[0]
        eInLine = eInLine.trimmed(*v6, *v1, chooseShorter=True)
        sCap = sCap.trimmed(*v1, *v2, chooseShorter=True)
        vertices, edges = [v1, v2, v3, v4, v5, v6], [sCap, sOutLine, mCap, eOutLine, eCap, eInLine]
    elif len(intersectionsCap(eCap, sInLine))==1:
        v6 = intersectionsCap(eCap, sInLine)[0]
        v1 = triangle.offsetVertice(k, k-1, delta, inner=True)
        sInLine = sInLine.trimmed(*v6, *v1, chooseShorter=True)
        eCap = eCap.trimmed(*v5, *v6, chooseShorter=True)
        vertices, edges = [v1, v2, v3, v4, v5, v6], [sCap, sOutLine, mCap, eOutLine, eCap, sInLine]
    else:
        v6 = triangle.offsetVertice(k+1, k+1, delta, inner=True)
        v7 = triangle.offsetEdgeIntersectionPoint(k, delta)
        v1 = triangle.offsetVertice(k, k-1, delta, inner=True)
        sInLine = sInLine.trimmed(*v7, *v1, chooseShorter=True)
        eInLine = eInLine.trimmed(*v6, *v7, chooseShorter=True)
        vertices, edges = [v1, v2, v3, v4, v5, v6, v7], [sCap, sOutLine, mCap, eOutLine, eCap, eInLine, sInLine]
    return Polygon(edges, join=False, vertices=vertices)
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






