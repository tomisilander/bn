#!/usr/bin/python

import math, cgamma

def lgamma(x):
    """
    Natural log of the gamma function (x > 0)
    Derived from "Numerical Receipes in C"
    """

    cof = (76.18009172947146,    -86.50532032941677,
           24.01409824083091,    -1.231739572450155,
           0.1208650973866179e-2,-0.5395239384953e-5)
    tmp = x + 5.5 - (x + 0.5) * math.log(x + 5.5);
    ser = 1.000000000190015 + sum([ c / (x + i + 1)
                                    for (i,c) in enumerate(cof)])
    return math.log(2.5066282746310005 * ser / x) - tmp

#def gammaln(double x):
#    cdef double tmp, ser
#    cdef int i
#    tmp = x + 5.5
#    tmp = tmp - (x + 0.5) * log(tmp)
#    ser = 1.000000000190015
#    for i from 0 <= i <= 5:
#        ser += cof[i] / (x + i + 1)
#def vamma(x):)
#    return x

#gammaln = cgamma.gammaln
for t in xrange(500000):
    g = cgamma.gammaln(6.34)
    # g = lgamma(6.34)
