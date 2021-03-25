
import itertools as it

"""

We are going to count the number of permutations with a given pinnacle set according to our count.

As a reminder, the count follows:

count = 2^{n - |P| - 1} sum_{V in VV(P)} prod_{p in P} binom{N_{PV}(p)}2 prod_{k in [n] \ (P cup V)} N_{PV}

VV(P) being the set of admissible vale sets

"""

# Pinnacle Set Format [p1, p2, p3,..., p_ell]

def dualBoundWeakCompGenSub(ub, lb, acc, rem, storage, ind):
	if not rem:
		for i in range(ind, len(storage)): storage[i] = 0
		yield storage
		return True
	u = min(ub[ind], rem)
	l = max(lb[ind] - acc, 0) - 1
	nInd = ind + 1
	for i in range(u, l, -1):
		storage[ind] = i
		if not (yield from dualBoundWeakCompGenSub(ub, lb, acc + i, rem - i, storage, nInd)):
			return i != u
	return u != l

def primaryWeakCompGen(bounds, ell, storage):
	return dualBoundWeakCompGenSub(bounds, range(1, ell + 1), 0, ell, storage, 0)

def gapCards(P, v):
	
	ell = len(P)
	g = [None] * ell
	
	prev = v
	for i in range(ell):
		p = P[i]
		g[i] = p - prev - 1
		prev = p
	
	return g

def gapSets(P, v):
	ell = len(P)
	G = [None] * ell
	g = [None] * ell
	prev = v
	for i in range(ell):
		p = P[i]
		G[i] = range(prev + 1, p)
		g[i] = p - prev - 1
		prev = p
	return G, g

# def NPVPGen(P, t):
	# N = 2
	# for p, ti in zip(P, t):
		# N += ti - 1
		# yield N

factorialMemo = [1]
def factorialMemoBuild(N):
	k = len(factorialMemo)
	prev = factorialMemo[k - 1]
	while k <= N:
		prev *= k
		factorialMemo.append(prev) #fM[k] = prev = fM[k-1] * k
		k += 1
	return prev

def factorial(n):
	if n < len(factorialMemo): return factorialMemo[n]
	return factorialMemoBuild(n)

def binom(n, k): return factorial(n) // (factorial(k) * factorial(n - k))
def binom2(n): return (n * (n - 1)) >> 1

def intPow(b, e):
	out = 1
	while e:
		if e & 1: out *= b
		b *= b
		e >>= 1
	return out

def neg1Pow(e):
	return 1 - ((e & 1) << 1)

def compCount(ell, g, t):
	N = 1
	prod = 1
	for i in range(ell):
		ti = t[i]
		acc = 0
		for k in range(ti+1):
			acc += binom(ti, k) * neg1Pow(k) * intPow(N, g[i])
			N += 1
		# N' = N + ti + 1
		N -= 1
		acc //= factorial(ti)
		prod *= binom2(N) * neg1Pow(ti) * acc
		N -= 1
	return prod

def fullCount(n, P, v):
	ell = len(P)
	g = gapCards(P, v)
	t = [0] * ell
	acc = 0
	for _ in primaryWeakCompGen(g, ell, t):
		acc += compCount(ell, g, t)
	return acc << (n - ell - 1)

def valeSetGen(P, v):
	"Generates vale sets following the method described in the paper."
	ell = len(P)
	G, g = gapSets(P, v)
	t = [0] * ell
	base = {v}
	return it.chain.from_iterable(
		map(
			lambda i: it.starmap(
				base.union,
				it.product(*map(it.combinations, G, i))
			),
			primaryWeakCompGen(g, ell, t)
		)
	)

def pvCount(P, V, v):
	"Counts the number of permutations which may be generated from a given pinnacle set P, vale set V, and minimum vale v."
	prod = 1
	N = 1
	prev = v
	for p in P:
		for k in range(prev + 1, p):
			if k in V: N += 1; continue
			prod *= N
		prod *= N
		N -= 1
		prod *= N
		prod >>= 1
		prev = p
	return prod

def origFCount(n, P, v):
	acc = 0
	for V in valeSetGen(P, v):
		acc += pvCount(P, V, v)
	return acc << (n - len(P) - 1)
			














































