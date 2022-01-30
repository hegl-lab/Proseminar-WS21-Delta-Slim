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

def randomPoints(total, numIdeal=0):
    if total<numIdeal:
        raise ValueError('The total number of points must be greater than number of ideal points')
    rvals = np.random.rand(total-numIdeal)**0.5
    tvals = 2*np.pi*np.random.rand(total)
    pts = [Point.fromPolarEuclid(rvals[k],rad=t) if k<total-numIdeal else Ideal(t) for k, t in enumerate(tvals)]
    np.random.shuffle(pts)
    return pts

def removeIdealPoints(list):
    valid = [p for p in list if not p.isIdeal()]
    return valid
