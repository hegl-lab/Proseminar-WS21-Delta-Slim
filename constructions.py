'''Constructionos for delta-slim triangles'''

import math
from hyperbolic import util
from hyperbolic.euclid import intersection
from hyperbolic.euclid.shapes import  Arc, Line as ELine
from hyperbolic.poincare.shapes import *

def shift(seq, shift=1):
    perm=shift%len(seq)
    return seq[-perm:] + seq[:-perm]

def deltaLines_of_Line(Line, offset):
    hc1=Hypercycle.fromHypercycleOffset(Line,offset)
    hc2=Hypercycle.fromHypercycleOffset(Line,-offset)
    return [hc1,hc2]

def isPointOnSegment(px,py, Line):
    ''' Assumes that the given point is on the line '''
    assert isinstance(Line.projShape, (Arc, ELine))    #check wheter Line has segment
    if isinstance(Line.projShape, ELine): 
        K1=(px-Line.projShape.x1)*(Line.projShape.x2-Line.projShape.x1)+(py-Line.projShape.y1)*(Line.projShape.y2-Line.projShape.y1)
        K2=(px-Line.projShape.x2)*(Line.projShape.x1-Line.projShape.x2)+(py-Line.projShape.y2)*(Line.projShape.y1-Line.projShape.y2)
        if K1>=0 and K2>=0:
            return True
        else:
            return False
    elif isinstance(Line.projShape,Arc):
        arc = Line.projShape
        startDeg, endDeg = arc.startDeg % 360, arc.endDeg % 360
        if arc.cw:
            startDeg, endDeg = endDeg, startDeg
        else:
            startDeg, endDeg = startDeg, endDeg
        px = px - arc.cx
        py = py - arc.cy
        pDeg = math.degrees(math.atan2(py, px)) % 360
        if util.nearZero(pDeg - startDeg) or util.nearZero(pDeg - endDeg):
            return True
        if startDeg<endDeg: 
            return startDeg<=pDeg<=endDeg
        else:
            return (endDeg<=pDeg) ^ (pDeg<=startDeg)
    else:
        return True