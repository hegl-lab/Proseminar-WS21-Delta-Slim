'''Constructionos for delta-slim triangles'''

import math
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

def is_on_Linesegment(px,py, Line):
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
        px = px-Line.projShape.cx
        py = py-Line.projShape.cy
        pDeg = math.degrees(math.atan2(py, px))
        if not Line.projShape.cw:
            return Line.projShape.startDeg<=pDeg and pDeg<=Line.projShape.endDeg
        else:
            return Line.projShape.startDeg>=pDeg and pDeg>=Line.projShape.endDeg
    else:
        return True

def triangleIsCovered(triangle, delta):             #use subclass Triangle instead
    assert isinstance(triangle,Polygon)
    edges=triangle.edges
    for i, edge in enumerate(edges):
        side1, side2 = edges[(i-1)%len(edges)], edges[(i+1)%len(edges)]
        vert = edge.intersectionsWithHcycle(side1)
        p1, p2 = [], []
        for h1 in deltaLines_of_Line(side1, delta):
            ip1 = edge.intersectionsWithHcycle(h1)
            for p in ip1:
                if is_on_Linesegment(*p,edge):
                    p1.append(p)
        for h2 in deltaLines_of_Line(side2, delta):
            ip2 = edge.intersectionsWithHcycle(h2)
            for p in ip2:
                if is_on_Linesegment(*p,edge):
                    p2.append(p)
        if len(p1) <= 0 or len(p2) <= 0:        #one side delta is sourrounding the whole edge
            continue
        elif len(p1) > 1 or len(p2) > 1:
            raise Exception('Intersection with edge %s is ambiguous'%i)
        else:
            ps1, ps2 = p1[0], p2[0]
            s1=vert[0]
            if is_on_Linesegment(*ps2, Line.fromPoints(*s1, *ps1, segment=True)):
                continue
            else:
                return False
    return True