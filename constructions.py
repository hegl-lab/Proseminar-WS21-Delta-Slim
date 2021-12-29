'''constructionos for delta-slim triangles'''

import math
from hyperbolic.euclid import intersection
from hyperbolic.euclid.shapes import  Arc, Line as ELine
from hyperbolic.poincare.shapes import *

def deltaLines_of_Line(Line, offset):
    hc1=Hypercycle.fromHypercycleOffset(Line,offset)
    hc2=Hypercycle.fromHypercycleOffset(Line,-offset)
    return [hc1,hc2]

def is_on_Linesegment(px,py, Line):
    ''' Assumes that the given point is on the line '''
    assert Line.segment
    assert isinstance(Line.projShape, ( Arc, ELine))    #check wheter Line has segment
    if isinstance(Line.projShape, ELine): 
        K1=(Line.projShape.x1-px)*(Line.projShape.x1-Line.projShape.x2)+(Line.projShape.y1-py)*(Line.projShape.y1-Line.projShape.y2)
        K2=(Line.projShape.x2-px)*(Line.projShape.x2-Line.projShape.x1)+(Line.projShape.y2-py)*(Line.projShape.y2-Line.projShape.y1)
        if K1>=0 and K2>=0:     #do we need > ?
            return True
        else:
            return False
    elif isinstance(Line.projShape,Arc):
        px = px-Line.projShape.cx
        py = py-Line.projShape.cy
        pDeg = math.degrees(math.atan2(py, px))
        if not Line.projShape.cw:
            return Line.projShape.startDeg<=pDeg and pDeg<=Line.projShape.endDeg    #do we need < ?
        else:
            return Line.projShape.startDeg>=pDeg and pDeg>=Line.projShape.endDeg    #do we need > ?


def ips_with_deltaneigbourhood(sideLine,deltaLines,delta):
    PL=[]
    for l in deltaLines:
        for h in deltaLines_of_Line(l,delta):
            px1,py1,px2,py2=intersection.circleCircle(h.projShape,sideLine.projShape)
            if is_on_Linesegment(px1,py1,sideLine):
                PL.append(Point.fromEuclid(px1,py1))
            elif is_on_Linesegment(px2,py1,sideLine):
                PL.append(Point.fromEuclid(px2,py2))
    return PL