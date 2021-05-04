
import itertools as it

__doc__ = """

Counts the number of permutations with a given pinnacle set.

See fullCount.

"""

def dualBoundWeakCompGenSub(ub, lb, rem, storage, acc = 0, ind = 0):
	if not rem:
		for i in range(ind, len(storage)): storage[i] = 0
		yield storage
		return True
	u = min(ub[ind], rem)
	l = max(lb[ind] - acc, 0) - 1
	nInd = ind + 1
	for i in range(u, l, -1):
		storage[ind] = i
		if not (yield from dualBoundWeakCompGenSub(ub, lb, rem - i, storage, acc + i, nInd)):
			return i != u
	return u != l

def primaryWeakCompGen(bounds, ell, storage):
	return dualBoundWeakCompGenSub(bounds, range(1, ell + 1), ell, storage)

def gapCards(P, v):
	ell = len(P)
	g = [None] * ell
	prev = v
	for i in range(ell):
		p = P[i]
		g[i] = p - prev - 1
		prev = p
	return g

factorialMemo = [1]
def factorialMemoBuild(N):
	k = len(factorialMemo)
	prev = factorialMemo[k - 1]
	while k <= N:
		prev *= k
		factorialMemo.append(prev)
		k += 1
	return prev

def factorial(n):
	if n < len(factorialMemo): return factorialMemo[n]
	return factorialMemoBuild(n)

def binom(n, k): return factorial(n) // (factorial(k) * factorial(n - k))
def binom2(n): return (n * (n - 1)) >> 1

def neg1Pow(e):
	return 1 - ((e & 1) << 1)

def compCount(ell, g, t):
	N = 1
	prod = 1
	for i in range(ell):
		ti = t[i]
		acc = 0
		for k in range(ti+1):
			acc += binom(ti, k) * neg1Pow(k) * (N ** g[i])
			N += 1
		N -= 1
		acc //= factorial(ti)
		prod *= binom2(N) * neg1Pow(ti) * acc
		N -= 1
	return prod

def fullCount(n, P, v):
	"""
	Counts the number of permutations in Sn with pinnacle set P.
	
	n - n
	P - pinnacle set, as a list sorted in increasing order
	v - minimum value
		Will generally be either 0 or 1, depending on convention.
	
	Requirements:
		P should be a strictly increasing list or range
		v < P[0]
		P[-1] < n + v
	"""
	ell = len(P)
	g = gapCards(P, v)
	t = [0] * ell
	acc = 0
	for _ in primaryWeakCompGen(g, ell, t):
		acc += compCount(ell, g, t)
	return acc << (n - ell - 1)
