#!/usr/bin/env python3
import math
import typer
app = typer.Typer()

comb = []
def calc_combs(n):
	for k in range(n+1):
		comb.append([1])
		for j in range(1,k):
			comb[k].append(comb[k-1][j-1] + comb[k-1][j])
		if k > 0: 
			comb[k].append(1)

def b(N):
	B=[]
	B.append(1)
	for n in range(1,N+1):
		B.append(0)
		for k in range(1,n+1):
			B[-1]+=(-1)**(k+1)*comb[n][k]*2**(k*(n-k))*B[n-k]
	return B[-1]

@app.command()
def nof_nets(nof_vars: int, use_log: bool = False):
	calc_combs(nof_vars)
	nof = b(nof_vars)
	if use_log:
		print(f'{math.log(nof):.3f}')
	else:
	    print(f'{nof}')

if __name__ == "__main__":
    app()
