import math
from hyperbolic.poincare.shapes import *
from constructions import deltaLines_of_Line, isPointOnSegment

class Triangle(Polygon):
    def __init__(self, edges=None, join=False, vertices=None):
        if not edges==None:
            assert len(edges)==3
        elif not vertices==None:
            assert len(vertices)==3
        super().__init__(edges=edges, join=join, vertices=vertices)
    def isCCW(self):
        x0, y0 = self.vertices[0].x, self.vertices[0].y
        x1, y1 = self.vertices[1].x, self.vertices[1].y
        x2, y2 = self.vertices[2].x, self.vertices[2].y
        Deg1 = math.degrees(math.atan2(y0, x0))
        Deg2 = math.degrees(math.atan2(y1, x1))
        Deg3 = math.degrees(math.atan2(y2, x2))
        cw = (Deg2-Deg1)%360 > (Deg3-Deg1)%360
        return not cw
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
        if (self.isCCW() and delta<=0) or (not self.isCCW() and delta>=0):
            delta = -delta
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
    def offsetTriangle(self, offset, reverseOrder=False):
        ''' If self is a CCW triangle, returns a CCW triangle that is smaller by
            offset. '''
        edges = self.edges
        if reverseOrder:
            edges = reversed(edges)
        offEdges = [  # Maybe outer, maybe inner
            edge.makeOffset(offset)
            for edge in edges
            if not isinstance(edge, Point) or edge.isIdeal()
        ]
        return Triangle.fromEdges(offEdges, join=True)
    def makeRandom(self):
        #TODO: returns random triangle
        pass
    @classmethod
    def fromVertices(cls, vertices):
        if len(vertices)!=3:
            raise ValueError('Triangle vertices need to be three Points')
        return cls(vertices=vertices)
    @classmethod
    def fromEdges(cls, edges, join=True):
        return cls(edges=edges, join=join)