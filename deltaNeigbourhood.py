# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 12:53:04 2021

@author: Simon Heidrich
"""
from constructions import is_on_Linesegment, deltaLines_of_Line
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
                if is_on_Linesegment(*p, hcycle):
                    mpoints.append(p)
        assert len(points1)==1 and len(points2)==1 and len(mpoints)==1
        p1, p2, mp = points1[0], points2[0], mpoints[0]
        arc = Arc.fromPoints(*p1, *p2, *mp, excludeMid=True)
        return arc                  #we need Line(arc, segment=True) but this implementation is not yet in hyperbolic





