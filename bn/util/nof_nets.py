#!/usr/bin/env python

comb = []
def calc_combs(n):
	for k in xrange(n+1):
		comb.append([1])
		for j in xrange(1,k):
			comb[k].append(comb[k-1][j-1] + comb[k-1][j])
		if k> 0: comb[k].append(1)

def b(N):
	B=[]
	B.append(1)
	for n in xrange(1,N+1):
		B.append(0)
		for k in xrange(1,n+1):
			B[-1]+=(-1)**(k+1)*comb[n][k]*2**(k*(n-k))*B[n-k]
	return B[-1]

import sys, math, coliche

def main(n):
    calc_combs(n)
    nof = b(n)
    print(nof, math.log(nof))

coliche.che(main,"n (int)")
