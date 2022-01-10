from hyperbolic.poincare.shapes import *
from constructions import deltaLines_of_Line, isPointOnSegment

class Triangle(Polygon):
    def __init__(self, edges=None, join=False, vertices=None):
        super().__init__(edges=edges, join=join, vertices=vertices)
    def isCovered(self, delta):
        for i, edge in enumerate(self.edges):
            side1, side2 = self.edges[(i-1)%len(self.edges)], self.edges[(i+1)%len(self.edges)]
            vert = edge.intersectionsWithHcycle(side1)
            p1, p2 = [], []
            for h1 in deltaLines_of_Line(side1, delta):
                ip1 = edge.intersectionsWithHcycle(h1)
                for p in ip1:
                    if isPointOnSegment(*p,edge):
                        p1.append(p)
            for h2 in deltaLines_of_Line(side2, delta):
                ip2 = edge.intersectionsWithHcycle(h2)
                for p in ip2:
                    if isPointOnSegment(*p,edge):
                        p2.append(p)
            if len(p1) <= 0 or len(p2) <= 0:        #one side delta is sourrounding the whole edge
                continue
            elif len(p1) > 1 or len(p2) > 1:
                raise Exception('Intersection with edge %s is ambiguous'%i)
            else:
                ps1, ps2 = p1[0], p2[0]
                s1=vert[0]
                if isPointOnSegment(*ps2, Line.fromPoints(*s1, *ps1, segment=True)):
                    continue
                else:
                    return False
        return True
    def isCw(self):
        #TODO: return True if triangle is clockwise, 'cause only inner hypercycle is needed for isCovered
        # can be decided by CW or CCW 
        pass
    def makeRandom(self):
        #TODO: returns random triangle
        pass
    @classmethod
    def fromVertices(cls, vertices):
        if len(vertices)!=3:
            raise ValueError('Triangle vertices need to be three Points')
        return cls(vertices=vertices)