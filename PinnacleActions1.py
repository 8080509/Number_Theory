from itertools import chain
from SymmetricGroups1 import compose, inverse, subDescGen, desc

# def shiftFac(n, k):
	# return [*range(k-1), *range(k+1, n), k-1, k]

def getPV(x):
	edge = float('inf')
	x = x.copy()
	x.append(edge)
	P = set()
	V = set()
	preV = edge
	preD = True
	for j in x:
		newD = prev > j
		if (not preD) and newD:
			P.add(prev)
		elif preD and (not newD):
			V.add(prev)
	return P, V

def shiftFac(n, k):
	return [k-1, k, *range(k-1), *range(k+1, n)]

def shiftFacInv(n, k):
	return [*range(2, k+1), 0, 1, *range(k+1, n)]

def uLFac(pi, x):
	U = [[]]
	L = []
	piIter = iter(pi)
	val = next(piIter)
	try:
		while True:
			while val >= x:
				U[-1].append(val)
				val = next(piIter)
			U.append([])
			L.append([])
			while val < x:
				L[-1].append(val)
				val = next(piIter)
	except StopIteration:
		pass
	except: raise
	return U, L

def ascShift(pi, x, n):
	U, L = uLFac(pi, x + 1)
	(k, Lk), = filter(lambda i: i[1][0] == x or i[1][-1] == x, enumerate(L))
	s = Lk[0] == x
	if s:
		Lk.pop(0)
	else:
		Lk.pop(-1)
	k = (k + n) % len(L)
	if s:
		L[k].insert(0, x)
	else:
		L[k].append(x)
	L.append([])
	return sum(chain.from_iterable(zip(U, L)), [])

def fMax(ops):
	return lambda i: max(filter(ops.__contains__, i))

#0 <= a < b <= ell - 2 = len(L) - 2
def valShift(pi, x, a, b):
	P, V = getPV(x)
	assert 0 <= a
	assert a <  b
	U, L0 = uLFac(pi, x)
	ell = len(L0)
	k = U.index([x])
	L1 = [*map(tuple, L0)]
	assert b < ell
	tau = shiftFac(ell, k)
	L2 = compose(L1, tau)
	sigma = [0] * len(L1)
	origPos = {val: i for i, val in enumerate(L2)}
	lL = L2[:2]
	rL = L2[2:]
	lL.sort(key = max)
	rL.sort(key = max)
	L3 = lL + rL
	sigma = [origPos[val] for val in L3] # L3 = compose(L2, sigma)
	Lk = L3.pop(a)
	LK = L3.pop(b-1)
	L3.sort(key = max)
	L4 = sorted([Lk, LK], key = fMax(P.union(V))) + L3
	L5 = compose(compose(L4, inverse(sigma)), inverse(tau))
	L5.append([])
	return sum(chain.from_iterable(zip(U, map(list, L5))), [])

def uLPlotDataI(x, k):
	edge = max(x) + 2
	pts = []
	alt = []
	prev = (0, edge)
	k += 1
	for i, j in enumerate((j + 1 for j in x), 1):
		pt = (i, j)
		if prev[1] < k and k < j:
			alt.append(((k - prev[1])*(i - prev[0])/(j - prev[1])+prev[0], k))
		elif k == j:
			alt.append(pt)
		pts.append(pt)
		prev = pt
	return pts, alt, edge

def uLPlotDataD(x, k):
	edge = max(x) + 2
	pts = []
	alt = []
	prev = (0, edge)
	k += 1
	for i, j in enumerate((j + 1 for j in x), 1):
		pt = (i, j)
		if prev[1] > k and k > j:
			alt.append(((k - prev[1])*(i - prev[0])/(j - prev[1])+prev[0], k))
		elif k == j:
			alt.append(pt)
		pts.append(pt)
		prev = pt
	return pts, alt, edge

def uLPlotData(x, k):
	edge = max(x) + 2
	pts = []
	alt = []
	prev = (0, edge)
	k += 1
	for i, j in enumerate((j + 1 for j in x), 1):
		pt = (i, j)
		if (prev[1] < k and k < j) or (prev[1] > k and k > j):
			alt.append(((k - prev[1])*(i - prev[0])/(j - prev[1])+prev[0], k))
		elif k == j:
			alt.append(pt)
		pts.append(pt)
		prev = pt
	return pts, alt, edge

def mainGraphPlot(pts, mark = 'square', color = 'blue', mSize = None):
	out = '\\addplot[color=' + color + ',mark=' + mark
	if mSize is not None:
		out += ',mark size=' + str(mSize) + 'pt'
	out += ']coordinates{'
	out += ''.join(map(str, pts))
	out += '};\n'
	return out

def plotEdges(pts, xMax, xLen, color = 'blue'):
	edge = xMax + 2
	out  = mainGraphPlot(((0, edge), pts[0]), 'none', color)
	out += mainGraphPlot((pts[-1], (xLen + 1, edge)), 'none', color)
	return out

def stdTitle(x):
	out = '$_=('
	out += ', '.join(map(str, (i + 1 for i in x)))
	out += ')$'
	return out

def plotWrapper(plot, xMax, xLen, title = '_'):
	out = '\\begin{tikzpicture}\n\\begin{axis}[\n    height=\\axisdefaultheight*0.8,\n    width=\\textwidth*0.55,\n    title={'
	out += title
	out += '},\n    xtick={'
	out += ', '.join(map(str, range(1, xLen + 1)))
	out += '},\n    ytick={'
	out += ', '.join(map(str, range(1, xMax + 2)))
	out += '},\n    ymajorgrids=true,\n    grid style=dashed,\n    xmin = 0,\n    xmax = ' + str(xLen+1) + ',\n    ymin = 0,\n    ymax = ' + str(xMax + 2) + '\n]\n'
	out += plot
	out += '\\end{axis}\n\\end{tikzpicture}'
	return out

def ascShiftPlot(x, k):
	pts, alt, edge = uLPlotDataI(x, k)
	xMax = max(x)
	xLen = len(x)
	plot = mainGraphPlot(pts)
	plot += plotEdges(pts, xMax, xLen)
	for pt in alt:
		plot += mainGraphPlot((pt,), 'x', 'black', 3)
	plot += '\\addplot[color=black, domain=0:' + str(xLen + 1) + ']{' + str(k+1) + '};\n'
	return plotWrapper(plot, xMax, xLen, stdTitle(x))

def descShiftPlot(x, k):
	pts, alt, edge = uLPlotDataD(x, k)
	xMax = max(x)
	xLen = len(x)
	plot = mainGraphPlot(pts)
	plot += plotEdges(pts, xMax, xLen)
	for pt in alt:
		plot += mainGraphPlot((pt,), 'x', 'black', 3)
	plot += '\\addplot[color=black, domain=0:' + str(xLen + 1) + ']{' + str(k+1) + '};\n'
	return plotWrapper(plot, xMax, xLen, stdTitle(x))

def valShiftPlot(x, p):
	pts, alt, edge = uLPlotData(x, p)
	xMax = max(x)
	xLen = len(x)
	plot = mainGraphPlot(pts)
	for pt in alt:
		if pt[0] < 1 or pt[0] > xLen:
			continue
		plot += mainGraphPlot(((pt[0], 0), (pt[0], edge)), 'none', 'black')
	return plotWrapper(plot, xMax, xLen, stdTitle(x))





































