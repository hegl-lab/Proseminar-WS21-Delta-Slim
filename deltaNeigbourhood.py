# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 12:53:04 2021

@author: Simon Heidrich
"""
from Triangle import *
from constructions import *
from hyperbolic.poincare.shapes import *
from hyperbolic.euclid.shapes import Arc


def makeEndCap(triangle, vertNum, edgeNum, delta):
    '''only tested a bit yet'''
    k_v = vertNum%len(triangle.vertices)
    k_e = edgeNum%len(triangle.edges)
    assert k_e!=(k_v+1)%len(triangle.vertices) #edge and vertice don't lie opposide of each other
    point=triangle.vertices[k_v]
    hcycle=triangle.edges[k_e]
    if point.isIdeal():
        return point
    else:
        perp = hcycle.makePerpendicular(*point)
        points1 = perp.intersectionsWithHcycle(hcycle.makeOffset(delta))
        points2 = perp.intersectionsWithHcycle(hcycle.makeOffset(-delta))
        mpoints = []
        for h in deltaLines_of_Line(perp, delta):
            for p in hcycle.intersectionsWithHcycle(h):
                if isPointOnSegment(hcycle, *p):
                    mpoints.append(p)
        assert len(points1)==1 and len(points2)==1 and len(mpoints)==1
        p1, p2, mp = points1[0], points2[0], mpoints[0]
        arc = Arc.fromPoints(*p1, *p2, *mp, excludeMid=True)
        return arc

def iP(triangle, vertNum, edgeNum, delta):
    '''intersection point of inner offsetEdge and perpendicular line of edge edgeNum at vertice vertNum'''
    iv = vertNum%len(triangle.vertices)
    ie = edgeNum%len(triangle.edges)
    hcycle = triangle.offsetEdge(ie, delta, inner=True)
    vert = triangle.vertices[iv]
    if vert.isIdeal():
        return vert
    perp = triangle.edges[ie].makePerpendicular(*vert)
    pts= hcycle.intersectionsWithHcycle(perp)
    assert len(pts)==1
    return pts[0]

def oP(triangle, vertNum, edgeNum, delta):
    '''intersection point of outer offsetEdge and perpendicular line of edge edgeNum at vertice vertNum'''
    iv = vertNum%len(triangle.vertices)
    ie = edgeNum%len(triangle.edges)
    hcycle = triangle.offsetEdge(ie, delta, inner=False)
    vert = triangle.vertices[iv]
    if vert.isIdeal():
        return vert
    perp = triangle.edges[ie].makePerpendicular(*vert)
    pts= hcycle.intersectionsWithHcycle(perp)
    assert len(pts)==1
    return pts[0]

def innerInterPoint(triangle, vertNum, delta):
    '''only tested a bit yet'''
    ips=triangle.offsetEdge(vertNum-1,delta).intersectionsWithHcycle(triangle.offsetEdge(vertNum,delta))
    pts=[p for p in ips if not p.isIdeal()]
    assert len(pts)==1
    return pts[0]
    #TODO determine valid ip out of ips

def makeMidCap(triangle, vertNum, delta):
    '''Only tested a bit'''
    point=triangle.vertices[vertNum%len(triangle.vertices)]
    side1, side2 =triangle.edges[(vertNum-1)%len(triangle.vertices)], triangle.edges[vertNum%len(triangle.vertices)]
    if point.isIdeal():
        return point
    perp1, perp2 = side1.makePerpendicular(*point), side2.makePerpendicular(*point)
    p1=perp1.intersectionsWithHcycle(triangle.offsetEdge(vertNum-1, offset=delta, inner=False))
    p2=perp2.intersectionsWithHcycle(triangle.offsetEdge(vertNum, offset=delta, inner=False))
    circ=Circle.fromCenterRadius(point, delta)
    cp=Point.fromEuclid(circ.projShape.cx, circ.projShape.cy)
    cr=circ.projShape.r
    arc=Arc.fromPointsWithCenter(*p1[0],*p2[0], *cp, r=cr)
    if triangle.isCCW():
        return arc
    else:
        return Arc(arc.cx, arc.cy, arc.r, arc.startDeg, arc.endDeg, not arc.cw)


lineStyle1 = dict(fill='red', fill_opacity=1)

def deltaNbh(triangle, drawing, delta, edgeNum=0, **kwargs):
    '''old needs change with def from above'''
    k=edgeNum
    Cap1=makeEndCap(triangle, k, k-1, delta)
    inLine1 = triangle.offsetEdge(k-1, delta, inner=True)     #needs to be trimmed
    inLine1 = inLine1.trimmed(*innerInterPoint(triangle, k-1, delta),*iP(triangle, k, k-1, delta))
    inLine2 = triangle.offsetEdge(k+1, delta, inner=True)
    inLine2 = inLine2.trimmed(*iP(triangle, k+1, k+1, delta),*innerInterPoint(triangle, k-1, delta))
    Cap2=makeEndCap(triangle, k+1, k+1, delta)
    outLine2=triangle.offsetEdge(k+1,delta, inner=False)
    outLine2 = outLine2.trimmed(*oP(triangle, k+1, k+1, delta),*oP(triangle, k-1, k+1, delta))
    Cap3=makeMidCap(triangle,k-1,delta)
    outLine1=triangle.offsetEdge(k-1,delta, inner=False)
    outLine1 = outLine1.trimmed(*oP(triangle, k-1, k-1, delta), *oP(triangle, k, k-1, delta))

    Lines=[Cap1,inLine1,inLine2,Cap2,outLine2,Cap3,outLine1]
    for l in Lines:
        drawing.draw(l, hwidth=0.03, fill='red')

        #stroke_width=0.01, stroke='red', fill='red'

lineStyle1 = dict(fill='red', fill_opacity=1)

def deltaNeigbourhood(triangle, drawing, delta, edgeNumber=0):
    for i,l in enumerate(triangle.edges):
        if not triangle.vertices[i].isIdeal():
            drawing.draw(Circle.fromCenterRadius(triangle.vertices[i], delta),**lineStyle1)
        if i==edgeNumber:
            continue
        else:
            drawing.draw(l, hwidth=2*delta, **lineStyle1)
    

class deltaNBH:
    def __init__(self, subShape):
        assert isinstance(subShape, (Triangle))
        subShape = self.subShape





