# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 12:53:04 2021

@author: Simon Heidrich
"""
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
    '''Not tested yet'''
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
    '''Not tested yet'''
    ips=triangle.offsetEdge(vertNum-1).intersectionsWithHcycle(triangle.offsetEdge(vertNum))
    #TODO determine valid ip out of ips
    pass

def makeMidCap(triangle, vertNum, delta):
    '''Not tested yet'''
    point=triangle.vertices[vertNum%len(triangle.vertices)]
    side1, side2 =triangle.edges[(vertNum-1)%len(triangle.vertices)], triangle.edges[vertNum%len(triangle.vertices)]
    perp1, perp2 = side1.makePerpendicular(*point), side2.makePerpendicular(*point)
    p1=perp1.intersectionsWithHcycle(triangle.offsetEdge(vertNum-1, offset=delta, inner=False))
    p2=perp2.intersectionsWithHcycle(triangle.offsetEdge(vertNum, ofset=delta, inner=False))
    circ=Circle.fromCenterRadius(point, delta)
    arc=Arc.fromPointsWithCenter(*p1,*p2,circ.projShape.cx, circ.projShape.y, r=circ.projShape.r)
    #arc.reverse() if wrong part of the arc
    return arc


lineStyle1 = dict(fill='red', fill_opacity=1)

def deltaNbh(triangle, drawing, delta, edgeNum=0):
    '''old needs change with def from above'''
    for i,l in enumerate(triangle.edges):
        if i==edgeNum:
            continue
        else:
            drawing.draw(makeRoundCap(l, triangle.vertices[i], delta), **lineStyle1)
            drawing.draw(makeRoundCap(l, triangle.vertices[(i+1)%len(triangle.vertices)], delta), **lineStyle1)
            drawing.draw(l, hwidth=2*delta, **lineStyle1)


