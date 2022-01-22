'''Constructionos for delta-slim triangles'''

import math
import numpy as np
from hyperbolic import util
from hyperbolic.euclid.shapes import  Arc, Line as ELine
from hyperbolic.poincare.shapes import *

def shift(seq, shift=1):
    perm=shift%len(seq)
    return seq[-perm:] + seq[:-perm]

def deltaLines_of_Line(Line, offset):
    hc1=Hypercycle.fromHypercycleOffset(Line,offset)
    hc2=Hypercycle.fromHypercycleOffset(Line,-offset)
    return [hc1,hc2]

def randomPoints(number):
    rvals = np.random.rand(number)**0.5
    tvals = 2*math.pi*np.random.rand(number)
    pts = [Point.fromPolarEuclid(r,rad=t) for r,t in zip(rvals,tvals)]
    return pts

def isPointOnSegment(Line, x, y):
    ''' Assumes that the given point is on the line '''
    if isinstance(Line, ELine):
        ''' Assumes that the given point is on the line '''
        eline = Line.projShape
        #dot product of vectors startPoint->(x,y) and startpoint->endPoint
        K1 = (x - eline.x1) * (eline.x2 - eline.x1) + (y - eline.y1) * (eline.y2 - eline.y1)
        #dot product of vectors endPoint->(x,y) and endpoint->startPoint
        K2 = (x - eline.x2) * (eline.x1 - eline.x2) + (y - eline.y2) * (eline.y1 - eline.y2)      
        return K1 >= 0 and K2 >= 0
    elif isinstance(Line, Arc):
        arc = Line
        ''' Assumes that the given point is on the circle and returns True if on this arc '''
        startDeg, endDeg = arc.startDeg % 360, arc.endDeg % 360
        if arc.cw:
            startDeg, endDeg = endDeg, startDeg
        else:
            startDeg, endDeg = startDeg, endDeg
        px = x - arc.cx
        py = y - arc.cy
        pDeg = math.degrees(math.atan2(py, px)) % 360
        if util.nearZero(pDeg-startDeg) or util.nearZero(pDeg-endDeg):
            return True
        if startDeg<endDeg:
            return startDeg<=pDeg<=endDeg
        else:
            return (endDeg<=pDeg) ^ (pDeg<=startDeg)        
    elif isinstance(Line.projShape, ELine):
        ''' Assumes that the given point is on the line '''
        eline = Line.projShape
        #dot product of vectors startPoint->(x,y) and startpoint->endPoint
        K1 = (x - eline.x1) * (eline.x2 - eline.x1) + (y - eline.y1) * (eline.y2 - eline.y1)
        #dot product of vectors endPoint->(x,y) and endpoint->startPoint
        K2 = (x - eline.x2) * (eline.x1 - eline.x2) + (y - eline.y2) * (eline.y1 - eline.y2)      
        return K1 >= 0 and K2 >= 0
    elif isinstance(Line.projShape,Arc):
        arc = Line.projShape
        ''' Assumes that the given point is on the circle and returns True if on this arc '''
        startDeg, endDeg = arc.startDeg % 360, arc.endDeg % 360
        if arc.cw:
            startDeg, endDeg = endDeg, startDeg
        else:
            startDeg, endDeg = startDeg, endDeg
        px = x - arc.cx
        py = y - arc.cy
        pDeg = math.degrees(math.atan2(py, px)) % 360
        if util.nearZero(pDeg-startDeg) or util.nearZero(pDeg-endDeg):
            return True
        if startDeg<endDeg:
            return startDeg<=pDeg<=endDeg
        else:
            return (endDeg<=pDeg) ^ (pDeg<=startDeg)
    else:
        raise TypeError('Type is not supported')