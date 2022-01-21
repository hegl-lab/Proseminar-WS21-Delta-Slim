# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 12:53:04 2021

@author: Simon Heidrich
"""
from Triangle import Triangle
from constructions import isPointOnSegment, deltaLines_of_Line
from hyperbolic.poincare.shapes import *
from hyperbolic.euclid.shapes import Arc


def makeRoundCap(hcycle, point, delta):
    '''Assumes Point is startPoint or endPoint of hypercycle'''
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
        return arc                  #we need Line(arc, segment=True) but this implementation is not yet in hyperbolic

def makeEndCap(triangle, vertNum, edgeNum, delta):
    '''only tested a bit yet'''
    assert edgeNum%len(triangle.vertices)!=(vertNum+1)%len(triangle.vertices) #edge and vertice don't lie opposide of each other
    point=triangle.vertices[vertNum%len(triangle.vertices)]
    hcycle=triangle.edges[edgeNum%len(triangle.edges)]
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

def innerInterPoint(triangle, vertNum, delta):
    '''only tested a bit yet'''
    ips=triangle.offsetEdge(vertNum-1,delta).intersectionsWithHcycle(triangle.offsetEdge(vertNum,delta))
    pts=[p for p in ips if not p.isIdeal()]
    assert len(pts)==1
    return pts
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
    arc=Arc.fromPointsWithCenter(*p1[0],*p2[0], circ.projShape.cx, circ.projShape.cy, r=cr)
    if triangle.isCCW():
        return arc
    else:
        return Arc(arc.cx, arc.cy, arc.r, arc.startDeg, arc.endDeg, not arc.cw)


lineStyle1 = dict(fill='red', fill_opacity=1)

def deltaNbh(triangle, drawing, delta, edgeNum=0, **kwargs):
    '''old needs change with def from above'''
    k=edgeNum
    Cap1=makeEndCap(triangle, k, k-1, delta)
    inLine1=triangle.offsetEdge(k-1, delta, inner=True)     #needs to be trimmed to innerInterPoint(triangle, k-1, delta)
    inLine2=triangle.offsetEdge(k+1, delta, inner=True)
    Cap2=makeEndCap(triangle, k+1, k+1, delta)
    outLine2=triangle.offsetEdge(k+1,delta, inner=False)
    Cap3=makeMidCap(triangle,k+1,delta)
    outLine1=triangle.offsetEdge(k-1,delta, inner=False)
    #string everything together
