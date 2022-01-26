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
        '''gives the orientation of the euclidian triangle rigth now needs fixing
        x0, y0 = self.vertices[0].x, self.vertices[0].y
        x1, y1 = self.vertices[1].x, self.vertices[1].y
        x2, y2 = self.vertices[2].x, self.vertices[2].y
        x1, y1 = x1-x0, y1-y0                           #transform p0 to origin
        x2, y2 = x2-x0, y2-y0                           #transform p0 to origin
        Deg1 = math.degrees(math.atan2(y1, x1))         #get Deg of p1
        Deg2 = math.degrees(math.atan2(y2, x2))         #get Deg of p2
        ccw = (Deg2-Deg1)%360<=180'''
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
        return (self.vertices[0].isIdeal() and self.vertices[1].isIdeal() and self.vertices[2].isIdeal())
    def isEdgeIdeal(self, edgeNum):
        if (self.vertices[(edgeNum+1)%len(self.vertices)].isIdeal() 
            and self.vertices[edgeNum%len(self.vertices)].isIdeal()):
            return True
        else:
            return False
    def offsetEdge(self, edgeNum, offset, inner=True):
        if ((self.isCCW() and offset<=0) 
            or (not self.isCCW() and offset>=0)):
            offset = -offset
        if self.isEdgeIdeal(edgeNum=edgeNum):
            offset = -offset
        if inner:
            return Hypercycle.fromHypercycleOffset(self.edges[edgeNum%len(self.edges)], offset)
        else:
            return Hypercycle.fromHypercycleOffset(self.edges[edgeNum%len(self.edges)], -offset)
    def isCovered(self, delta):
        #if (self.isCCW() and delta<=0) or (not self.isCCW() and delta>=0):
        #    delta = -delta
        for i, edge in enumerate(self.edges):
            ip1 = edge.intersectionsWithHcycle(self.offsetEdge(i-1,delta))
            ip2 = edge.intersectionsWithHcycle(self.offsetEdge(i+1,delta))
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
        i=1
        k=0
        delta=1    
        while self.isCovered(delta)==False:
            delta=delta*2
            k=k+1
        while i-k<17:
            if self.isCovered(delta)==True:
                delta=delta-2**(k-i)
                i=i+1
            else:
                delta=delta+2**(k-i)
                i=i+1
        if self.isCovered(delta)==False:
            delta=delta+2**(k-i)
            i=i+1
        return delta
    @classmethod
    def fromVertices(cls, vertices):
        if len(vertices)!=3:
            raise ValueError('Triangle vertices need to be three Points')
        return cls(vertices=vertices)
    @classmethod
    def fromEdges(cls, edges, join=True):
        return cls(edges=edges, join=join)

