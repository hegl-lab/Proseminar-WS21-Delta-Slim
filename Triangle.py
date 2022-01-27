import math
from hyperbolic.poincare import Transform
from hyperbolic.poincare.shapes import *
from constructions import *

class Triangle(Polygon):
    def __init__(self, edges=None, join=False, vertices=None):
        if not edges==None:
            assert len(edges)==3
        elif not vertices==None:
            assert len(vertices)==3
        super().__init__(edges=edges, join=join, vertices=vertices)
    def isCCW(self):
        '''returns True for a counter-clock-wise self'''
        if self.isIdeal():
            Deg0 = math.degrees(self.vertices[0].theta)
            Deg1 = math.degrees(self.vertices[1].theta)
            Deg2 = math.degrees(self.vertices[2].theta)
            ccw = (Deg2-Deg0)%360 >= (Deg1-Deg0)%360
        else:
            vertNumOfPoints = [i for i,p in enumerate(self.vertices) if not p.isIdeal()]
            k=vertNumOfPoints[0]
            newOriginandnewX = Transform.shiftOrigin(self.vertices[k], self.vertices[(k+1)%len(self.vertices)])
            p2 = Transform.applyToPoint(newOriginandnewX, self.vertices[(k-1)%len(self.vertices)])
            ccw=math.degrees(p2.theta)%360<=180
        return ccw
    def isIdeal(self):
        '''returns True when all vertices are ideal points'''
        return (self.vertices[0].isIdeal() and self.vertices[1].isIdeal() and self.vertices[2].isIdeal())
    def isEdgeIdeal(self, edgeNum):
        '''returns True when both vertices of the edge are ideal points'''
        return (self.vertices[edgeNum%len(self.vertices)].isIdeal() and self.vertices[(edgeNum+1)%len(self.vertices)].isIdeal())
    def offsetEdge(self, edgeNum, offset, inner=True):
        '''returns the offset hypercycle of the edge closer to the inside of the self when inner is True'''
        if ((self.isCCW() and offset<=0) or (not self.isCCW() and offset>=0)) ^ self.isEdgeIdeal(edgeNum):
            offset = -offset
        if inner:
            return Hypercycle.fromHypercycleOffset(self.edges[edgeNum%len(self.edges)], offset)
        else:
            return Hypercycle.fromHypercycleOffset(self.edges[edgeNum%len(self.edges)], -offset)
    def isCovered(self, delta):
        '''returns True when the delta-neigbourhood of any two sides of the self already cover the last one'''
        for i, edge in enumerate(self.edges):
            ip1 = edge.intersectionsWithHcycle(self.offsetEdge(i-1, delta))
            ip2 = edge.intersectionsWithHcycle(self.offsetEdge(i+1, delta))
            p1 = [p for p in ip1 if (isPointOnSegment(edge, *p) and not p.isIdeal())]   #tiny delta for ideal triangles will remove all points
            p2 = [p for p in ip2 if (isPointOnSegment(edge, *p) and not p.isIdeal())]   #tiny delta for ideal triangles will remove all points
            if len(p1) <= 0 or len(p2) <= 0:            #deltaNbh of one side is sourrounding the whole edge or problem above
                continue
            elif len(p1) > 1 or len(p2) > 1:
                raise ValueError('Intersection with edge %s is ambiguous'%i)
            else:
                ps1, ps2 = p1[0], p2[0]
                s1 = self.vertices[i]
                if isPointOnSegment(Line.fromPoints(*s1, *ps1, segment=True), *ps2):
                    continue
                else:
                    return False
        return True
    def approx(self):
        '''returns the smallest delta for which self is delta-slim'''
        i=1
        k=0
        delta=1    
        while self.isCovered(delta)==False:
            delta=delta*2
            k=k+1
        while i-k<19:
            if self.isCovered(delta)==True:
                delta=delta-2**(k-i)
                i=i+1
            else:
                delta=delta+2**(k-i)
                i=i+1
        if self.isCovered(delta)==False:
            delta=delta+2**(k-i+1)      #some triangles are still not covered
            i=i+1
        return delta
    def offsetVertice(self, vertNum, edgeNum, offset, inner=False, onEdge=False):
        '''returns intersection point of the (outer) offsetEdge and the edge's perpendicular line at the vertice
        or returns intersection point of the offset edge's perpendicular line at the vertice and the edge itself'''
        assert edgeNum!=(vertNum+1)%len(self.vertices)          #edge and vertice can't lie opposide of each other
        vert = self.vertices[vertNum%len(self.vertices)]
        if vert.isIdeal():
            return vert        
        edge = self.edges[edgeNum%len(self.edges)]
        offsetEdge = self.offsetEdge(edgeNum, offset, inner)
        perp = edge.makePerpendicular(*vert)
        if onEdge:
            pts = [edge.intersectionsWithHcycle(h)[0] 
                    for h in deltaLines_of_Line(perp, offset) 
                    if isPointOnSegment(edge, *edge.intersectionsWithHcycle(h)[0])]
            assert len(pts)==1
        else:
            pts = offsetEdge.intersectionsWithHcycle(perp)
            assert len(pts)==1
        return pts[0]
    def offsetEdgeIntersectionPoint(self, edgeNum, offset):
        hc1 = self.offsetEdge(edgeNum+1, offset)
        hc2 = self.offsetEdge(edgeNum-1, offset)
        pts = [p for p in hc1.intersectionsWithHcycle(hc2) if not p.isIdeal()]
        assert len(pts)==1      #fails for bad geometry
        return pts[0]
    def endCap(self, vertNum, edgeNum, offset):
        sp = self.offsetVertice(vertNum, edgeNum, offset, inner=True)
        mp = self.offsetVertice(vertNum, edgeNum, offset, onEdge=True)
        ep = self.offsetVertice(vertNum, edgeNum, offset, inner=False)
        if sp.isIdeal() or mp.isIdeal() or ep.isIdeal():
            idealpts=[p for p in [sp,mp,ep] if p.isIdeal()]
            return idealpts[0]
        else:
            return Arc.fromPoints(*sp, *ep, *mp, excludeMid=True)
    def midCap(self, vertNum, offset):
        vert = self.vertices[vertNum%len(self.vertices)]
        if vert.isIdeal():
            return vert
        sp = self.offsetVertice(vertNum, vertNum-1, offset, inner=False)
        ep = self.offsetVertice(vertNum, vertNum, offset, inner=False)
        circ = Circle.fromCenterRadius(self.vertices[vertNum%len(self.vertices)], offset)
        cp = Point.fromEuclid(circ.projShape.cx, circ.projShape.cy)
        if sp.isIdeal() or cp.isIdeal() or ep.isIdeal():
            idealpts=[p for p in [sp,cp,ep] if p.isIdeal()]
            return idealpts[0]
        else:
            return Arc.fromPointsWithCenter(*sp,*ep, *cp, r=circ.projShape.r, cw= not self.isCCW())
    @classmethod
    def fromVertices(cls, vertices):
        if len(vertices)!=3:
            raise ValueError('Triangle vertices need to be three Points')
        return cls(vertices=vertices)
    @classmethod
    def fromEdges(cls, edges, join=True):
        return cls(edges=edges, join=join)

