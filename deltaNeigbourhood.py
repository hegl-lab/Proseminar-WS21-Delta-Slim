"""
Created on Mon Dec 27 12:53:04 2021

@author: Simon Heidrich
"""
from Triangle import *
from constructions import *
from hyperbolic.poincare.shapes import *
from hyperbolic.euclid.shapes import Arc

class deltaNBH:
    def __init__(self, subShape):
        assert isinstance(subShape, (Triangle))
        subShape = self.subShape

def capIntersections(cap1, hcycle2):
    if not isinstance(cap1, Hypercycle) or not isinstance(hcycle2, Hypercycle):
        return []
    else:
        return cap1.segmentIntersectionsWithHcycle(hcycle2)

def deltaNbh(triangle, delta, edgeNum=0):
    k=edgeNum
    sCap = triangle.endCap(k, k-1, delta)
    v2 = triangle.offsetVertice(k, k-1, delta, inner=False)
    v3 = triangle.offsetVertice(k-1, k-1, delta, inner=False)  
    sOutLine = triangle.offsetEdge(k-1, delta, inner=False).trimmed(*v3, *v2).reversed()
    mCap = triangle.midCap(k-1, delta)
    v4 = triangle.offsetVertice(k-1, k+1, delta, inner=False)
    v5 = triangle.offsetVertice(k+1, k+1, delta, inner=False)
    eOutLine = triangle.offsetEdge(k+1, delta, inner=False).trimmed(*v5, *v4).reversed()
    eCap = triangle.endCap(k+1, k+1, delta)
    if isinstance(eCap, Hypercycle):
        eCap=eCap.reversed()
    v1 = triangle.offsetVertice(k, k-1, delta, inner=True)
    v6 = triangle.offsetVertice(k+1, k+1, delta, inner=True)
    temp7 = triangle.offsetVertice(k-1, k+1, delta, inner=True)
    temp8 = triangle.offsetVertice(k-1, k-1, delta, inner= True) 
    sInLine = triangle.offsetEdge(k-1, delta, inner=True).trimmed(*temp8, *v1)
    eInLine = triangle.offsetEdge(k+1, delta, inner=True).trimmed(*v6, *temp7)
    if len(capIntersections(sCap, eCap))==1:
        v1 = capIntersections(sCap, eCap)[0]
        sCap = Hypercycle(Arc.fromPoints(*v1, *v2, *triangle.offsetVertice(k, k-1, delta, onEdge=True), excludeMid=True), segment=True)
        eCap = Hypercycle(Arc.fromPoints(*v5, *v1, *triangle.offsetVertice(k+1, k+1, delta, onEdge=True), excludeMid=True), segment=True)
        vertices , edges = [v1, v2, v3, v4, v5], [sCap, sOutLine, mCap, eOutLine, eCap]
    elif len(capIntersections(sCap, eInLine))==1:
        v1 = capIntersections(sCap, eInLine)[0]
        eInLine = eInLine.trimmed(*v6, *v1)
        sCap = Hypercycle(Arc.fromPoints(*v1, *v2, *triangle.offsetVertice(k, k-1, delta, onEdge=True), excludeMid=True), segment=True)
        vertices, edges = [v1, v2, v3, v4, v5, v6], [sCap, sOutLine, mCap, eOutLine, eCap, eInLine]
    elif len(capIntersections(eCap, sInLine))==1:
        v6 = capIntersections(eCap, sInLine)[0]
        sInLine = sInLine.trimmed(*v6, *v1)
        eCap = Hypercycle(Arc.fromPoints(*v5, *v6, *triangle.offsetVertice(k+1, k+1, delta, onEdge=True), excludeMid=True), segment=True)
        vertices, edges = [v1, v2, v3, v4, v5, v6], [sCap, sOutLine, mCap, eOutLine, eCap, sInLine]
    else:
        v7 = triangle.offsetEdgeIntersectionPoint(k, delta)
        sInLine = sInLine.trimmed(*v7, *v1)
        eInLine = eInLine.trimmed(*v6, *v7)
        vertices, edges = [v1, v2, v3, v4, v5, v6, v7], [sCap, sOutLine, mCap, eOutLine, eCap, eInLine, sInLine]
    vertices = [v for v,e in zip(vertices, edges) if isinstance(e, Hypercycle)]
    edges = [e for e in edges if isinstance(e,Hypercycle)]
    return Polygon(edges, join=False, vertices=vertices)






