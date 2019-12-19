import operator
from itertools import repeat, chain

class InvalidMapping(Exception):
	pass

timingMode = True

treeDepth = 0

treePins = {}
treeN = 0
treeEnabled = False


def setTreeVals(pins, n, depth = 0, enabled = True):
	global treePins
	global treeDepth
	global treeN
	global treeEnabled
	treePins = pins
	treeN = n
	treeDepth = depth
	treeEnabled = enabled

def genTree(gen):
	if timingMode:
		return gen
	def out(*args,**kwargs):
		if treeEnabled:
			global treeDepth
			treeDepth += 1
			sOut = str(args[0])
			print('|  ' * treeDepth + sOut + ' ' * ((3 * (treeN - len(treePins) + 2 - treeDepth)) + len(str(list(range(treeN)))) - len(sOut)), opCounter(args[0], treePins, treeN)[1:])
		for i in gen(*args,**kwargs): yield i
		if treeEnabled:
			treeDepth -= 1
	return out

def altGenTree(gen):
	if timingMode:
		return gen
	def out(*args, **kwargs):
		#if treeEnabled:
		global treeDepth
		for i in gen(*args, **kwargs):
			print('|  ' * treeDepth + str(i))
			treeDepth += 1
			yield i
			treeDepth -= 1
		#else:
		#	for i in gen(*args, **kwargs): yield i
	return out

def genRuntime(gen):
	def out(*args,**kwargs):
		t = -time()
		out = gen(*args,**kwargs)
		t += time()

def serialize(mapping): #create a number to represent the element
	ops = list(range(len(mapping)))
	nums = []
	for e in mapping:
		i = ops.index(e)
		del ops[i]
		nums.append(i)
	number = 0
	size = 0
	for i in nums[::-1]:
		size += 1
		number *= size
		number += i
	return (number, size)

#def serFixed(mapping, fP = set()): #create a number	to represent the element 

def deserialize(number, size):
	ops = list(range(size))
	mapping = []
	while size:
		(number, x) = divmod(number, size)
		mapping.append(ops.pop(x))
		size -= 1
	return mapping

def identity(n):
	return list(range(n))

def compose(m1, m2):
	size = len(m1)
	m3 = [0]*size
	if size != len(m2):
		raise ValueError('Attempt to compose permutations of different sets')
	for i in range(size):
		m3[i] = m1[m2[i]]
	return m3

def inverse(m1):
	size = len(m1)
	m2 = [0]*size
	for i in range(size):
		m2[m1[i]]=i
	return m2

def desc(pi):
	piI = iter(enumerate(pi))
	pI, pX = next(piI)
	descSet = set()
	for i, x in piI:
		if pX > x:
			descSet.add(pI)
		pX = x
		pI = i
	return descSet

def pP(m):
	peaks = set()
	pinnacles = set()
	for i in range(1, len(m)-1):
		if m[i-1] < m[i] and m[i+1] < m[i]:
			peaks.add(i)
			pinnacles.add(m[i])
	return (peaks,pinnacles)

def tTAdd(m, adj = False): #Tweaked to give vallies. -Add meaning it also counts the ends.  w1 w2 x w4 w5
	if not m: return (set(), set())
	peaks = set()
	pinnacles = set()
	n = len(m)
	m = m.copy()
	m.append(max(m) + 1)
	for i in range(0, n):
		if m[i-1] > m[i] and m[i+1] > m[i]:
			peaks.add(i)
			pinnacles.add(m[i])
			if adj:
				pinnacles[-1] = (pinnacles[-1],(m[i-1] == m[i]+1) or (m[i+1] == m[i]+1))
	return (peaks,pinnacles)

def consec(m): #Lists values which are immediately adjacent to their successor.
	consecs = set()
	n = len(m)
	m = m.copy()
	m.append(n+1)
	for i in range(0,n):
		val = m[i] + 1
		if m[i-1] == val or m[i+1] == val: consecs.add(m[i])
	return consecs

def aTrans(e,n):
	return trans(e, e+1, n)

def trans(a,b,n):
	m = list(range(n))
	m[a] = b
	m[b] = a
	return m

def xFactor(m,x):
	j = m.index(x)
	i = j-1
	while i >= 0 and m[i] < x: i -= 1
	i+=1
	w1 = m[:i]
	w2 = m[i:j]
	j += 1
	i = j
	n = len(m)
	while i < n and m[i] < x: i += 1
	w4 = m[j:i]
	w5 = m[i:]
	return (w1,w2,w4,w5)

def fSActionX(m,x):
	(w1,w2,w4,w5) = xFactor(m,x)
	return [*w1,*w4,x,*w2,*w5]

def fSTActionX(m,x):
	(w1,w2,w4,w5) = xFactor(m,x)
	return [*w1,*w4[::-1],x,*w2[::-1],*w5]

def fSActionS(m,s):
	for x in s:
		m = fSActionX(m,x)
	return m

def fSTActionS(m,s):
	for x in s:
		m = fSTActionX(m,x)
	return m

def powIter(collection):
	collection = collection.copy()
	if not collection:
		yield []
		return
	x = collection.pop()
	for i in powIter(collection):
		yield [x, *i]
		yield i

def subsetIter(coll, k): #Iterates through the k-element subsets of a collection.
	if k == 0: yield []; return
	tCol = coll.copy()
	for _ in range(k-1, len(tCol)):  # we want to select items from tCol, so long as what remains has at least k-1 entries.  This just makes it run the loop that many times.
		x = tCol.pop()
		for i in subsetIter(tCol, k-1): i.append(x); yield i #Iterates through subsets with one fewer element from the collection of items not yet used in this level.

def subsetIterComp(coll, k): #Iterates through the k-element subsets of a collection.
	if k == 0:
		yield [], coll
		return
	tCol = coll.copy()
	pCol = []
	for _ in range(k-1, len(tCol)):  # we want to select items from tCol, so long as what remains has at least k-1 entries.  This just makes it run the loop that many times.
		x = tCol.pop()
		for i, comp in subsetIterComp(tCol, k-1): #Iterates through subsets with one fewer element from the collection of items not yet used in this level.
			i.append(x)
			yield i, pCol + comp
		pCol.append(x)

def admValIter(pins):
	if not pins:
		yield {1}
		return
	coll = [i for i in range(1, max(pins)) if i not in pins]
	for i in subsetIter(coll, len(pins)):
		i.append(0)
		i = set(i)
		if admiscible(pins, i): yield i
	return

def fSOrbitIter(m):
	S = set(range(len(m)))
	S.difference_update(tTAdd(m)[1])
	for s in powIter(S):
		yield fSActionS(m,s)

def fSTOrbitIter(m):
	S = set(range(len(m)))
	for s in powIter(S):
		yield fSTActionS(m,s)

def fSOrbitList(m):
	return list(fSOrbitIter(m))

def fSOrbit(m):
	l = []
	for i in fSOrbitIter(m):
		if i not in l: l.append(i)
	return l

def fSTOrbit(m):
	l = []
	for i in fSTOrbitIter(m):
		if i not in l: l.append(i)
	return l

def cycleFac(m): #Factors a permutation as the product of cycles
	s = list(range(len(m)))
	f = []
	while s:
		c = []
		x = s[0]
		while True:
			if x in c: break
			c.append(x)
			s.remove(x)
			x = m[x]
		if c: f.append(c)
	return (f, len(m))

def cycleRec(f, n):
	f = f[::-1]
	m = [None] * n
	for i in range(n):
		x = i
		for c in f:
			try:
				k = c.index(x)
			except ValueError: pass
			except: raise
			else: x = c[k + 1 - len(c)]
		m[i] = x
	return m

def pinFactor(m):
	i = 0
	words = []
	for j in pP(m)[0]:
		words.append(m[i:j])
		words.append([m[j]])
		i = j+1
	words.append(m[i:])
	return words

def factorial(n):
	acc = 1
	for i in range(1, n+1):
		acc *= i
	return acc

def badPinGen(pins, n):
	for i in range(factorial(n)):
		x = deserialize(i,n)
		if pP(x)[1] == pins: yield x

#def basePinGen(pins, n):
#	pins = set(pins)
#	ops = set(range(n))
#	ops.difference_update(pins)
#	resOps = ops.copy()
#	res
#	while pins:
#		P = max(pins)
#		pins.remove(P)
#		Q = P
#		while Q >= P:
#			Q = max(resOps)
#			resOps.remove(Q)
#		res[Q] = P
#	m = []
#	while ops:
#		i = min(ops)
#		ops.remove(i)
#		if i in res:
#			m.append(res[i])
#		m.append(i)
#	return m

def pVFactor(m, pins = None, p = None):
	if pins is None:
		pins = pP(m)[1]
	if not pins:
		return sorted(m)
	if p is None:
		p = max(pins)
	pins.remove(p)
	x = xFactor(m,p)
	lS = {*x[1]}
	lP = set()
	rP = set()
	for i in pins:
		if i in lS: lP.add(i)
		else: rP.add(i)
	lp = max(lP) if lP else min(x[1])
	rp = max(rP) if rP else min(x[2])
	x1 = pVFactor(x[1], lP, lp)
	x2 = pVFactor(x[2], rP, rp)
	if lp > rp: (x1,x2) = (x2,x1)
	return [[x1,p,x2],*sorted([*x[0],*x[3]])]

def reFac(f):
	m = []
	for i in f:
		if isinstance(i,list): m.extend(reFac(i))
		else: m.append(i)
	return m

def cRep(m):
	return reFac(pVFactor(m))

def fSRootGen(elems): #Generates one item from every foata-strehl orbit, given a set of elements
	pins = set(elems)
	if len(pins) < 2:
		yield list(pins)
		return
	P = max(pins)
	pins.remove(P)
	p = max(pins)
	pins.remove(p)
	for s in powIter(pins):
		c = pins.difference(s)
		c.add(p)
		if not s:
			for i in fSRootGen(c):
				yield [*i, P]
		else:
			for i in fSRootGen(s):
				for j in fSRootGen(c):
					yield [*i, P, *j]

def admiscible(P,V):
	if 0 not in V: return False
	if len(V) != len(P) + 1: return False
	n = 0
	for i in sorted((*P, *V)):
		if i in V: n += 1; continue
		if n < 2: return False
		n -= 1
	return True

@genTree
def arrGen(P,V):  #Let P and V be sorted lists
	if len(P) == 0: yield V; return
	if len(P) == 1: [v1,v2] = V; yield [v1,*P,v2]; return #This is for optimization.
	P = P.copy()
	p = P.pop(0)#P is now P', stored under the same variable for efficiency
	V1 = list(filter(lambda i: i < p, V)) #this is Vp from the notes
	V2 = V.copy() #this is just for optimization
	V2.insert(V.index(max(V1)) + 1, p)
	for [v1,v2] in subsetIter(V1, 2):
		V3 = V2.copy() #this will be V' from the notes
		V3.remove(v1)
		V3.remove(v2)
		for a in arrGen(P,V3): #here a' is selected
			j = a.index(p)
			a.insert(j+1,v2) #this line, and the following produce a, corresponding to a'.
			a.insert(j,v1)
			yield a

#TODO:  Reverse iteration order?

def fSRC(i = None, j = None, n = None):
	if j is None:
		j = n - (2 * i) + 1
	if i == 0: return 0
	if j < 0: return 0
	if i == 1 and j == 0: return 1
	return (j + 1) * fSRC(i - 1, j + 1) + i * fSRC(i, j - 1)

def pinCount(n, k):
	if k == 0: return 1
	if n == 1: return 0
	if n <= 2 * k: return 0
	return (n - 2 * k) * pinCount(n - 1, k - 1) + (k + 1) * pinCount(n - 1, k)

@genTree
def pinPopulate(l, pins, n, i = 0):
	if i == n:
		yield l
		return
	j = i + 1
	if i in pins:
		k = l.index(i)
		if (k == 0) or (k == len(l) - 1) or (l[k - 1] > i) or (l[k + 1] > i): return
		for r in pinPopulate(l, pins.difference({i}), n, j): yield r
		return
	ln = len(l)
	for k in range(ln+1):
		if ((k != ln) and (l[k] not in pins)) or ((k != 0) and (l[k - 1] in pins) and ((k - 1 == 0) or l[k - 2] > l[k - 1])): continue
		m = l.copy()
		m.insert(k, i)
		for r in pinPopulate(m, pins, n, j): yield r

def vPinPopulate(l, n):
	k = l.copy()
	ops = list(range(n))
	for i in l: ops.remove(i)
	for i in pP(l)[1]: k.remove(i)
	for i in tTAdd(l)[1]: k.append(i)
	k.sort()
	for i in vPPSub(l, ops, k): yield i

@genTree	
def vPPSub(l, ops, k, res = 0):
	if len(k) == 1 and 0 not in l: #this clause is just for optimization.
		if not res: yield l + [0]
		return
	if not k:
		yield l
		return
	p = k[0]
	j = l.index(p)
	k = k[1:]
	nRes = 0
	rep = bool(k and (p == k[0]))
	j += not rep
	for i in range(res, len(ops)):
		nOps = ops.copy()
		q = nOps.pop(i)
		if q > p: return
		if rep: nRes = i
		m = l.copy()
		m.insert(j, q)
		for n in vPPSub(m, nOps, k, nRes): yield n

@genTree
def newPinPopulate(l, tPins, ops):
	if isinstance(ops, int):
		ops = list(range(ops))
		if not l: yield ops; return
		for i in l: ops.remove(i)
	else:
		ops = ops.copy()
	if not ops:
		yield l
		return
	i = ops.pop(0)
	pins = tPins.copy()
	for j in tPins:
		if i > j: pins.remove(j)
	ln = len(l)
	for k in range(1, ln+1):
		if (((k != ln) and (l[k] not in pins))) or (l[k-1] > i): continue
		m = l.copy()
		m.insert(k, i)
		for r in newPinPopulate(m, pins, ops): yield r

def fSPRootGen(pins, n):
	for r in fSRootGen(pins):
		for s in vPinPopulate(r, n):
			for t in newPinPopulate(s, pins, n): yield t

def altFSPRootGen(pins,n):
	for a in fullArrGen(pins):
		for pi in newPinPopulate(a, pins, n): yield pi

def oldArrGen(pins):
	n = max(pins) + 1
	for r in fSRootGen(pins):
		for s in vPinPopulate(r, n):
			if 0 in s: yield s

def fullArrGen(pins):
	vOps = sorted(i for i in range(max(pins) + 1) if i not in pins)
	pins = sorted(pins)
	for vals in subsetIter(vOps, len(pins)+1):
		if not admiscible(pins, vals): continue
		for a in arrGen(pins, vals): yield a

def oldfSPRootGen(pins, n):
	for s in fSRootGen(pins):
		for r in pinPopulate(s, pins, n): yield r

def goodPinGen(pins, n):
	for r in fSPRootGen(pins, n):
		for s in fSOrbitIter(r): yield s

def altPinGen(pins, n):
	for r in altFSPRootGen(pins,n):
		for s in fSOrbitIter(r): yield s

def newFullArrGen(pins):
	return chain.from_iterable(map(arrGen, repeat(pins), valeSetGenF(pins)))

#Uses the generation sequence to build all the representatives.
@altGenTree
def genSeqAlg(pins, vals, k, oLen = 1):
	#assert oLen == cLessS(vals, k) - cLessS(pins, k)
	if not oLen:
		yield []
		return
	if k in vals:
		oLen -= 1
		for out in genSeqAlg(pins, vals, k - 1, oLen):
			out.append((k,))
			yield out
		return
	if k in pins:
		oLen += 1
		for out in genSeqAlg(pins, vals, k - 1, oLen):
			for i in range(oLen):
				tOut0 = out.copy()
				l = tOut0.pop(i)
				for j in range(i, oLen - 1):
					tOut1 = tOut0.copy()
					w = l + (k,) + tOut1.pop(j)
					tOut1.append(w)
					yield tOut1
		return
	for out in genSeqAlg(pins, vals, k - 1, oLen):
		for i in range(oLen):
			temp = out[i]
			out[i] += (k,)
			yield out
			out[i] = temp
		# for w in out: #Be very careful with this.  Note to self:  If something strange happens, troubleshoot here.  We are modifying a component of 
			# w.append(k)
			# yield out
			# w.pop()

#collGen is an iterator for elements of the collection.  k is the size of the subset.  d(= 0) is the depth of the recursive generator, and indicates how many elements may be added to $l$ by higher operations, as it counts the number of higher operations.
def altSubsetIter(collGen, k, d = 0):
	mLL = k - d #minimum len(l) for output
	try: val = next(collGen)
	except StopIteration:
		if mLL <= 0: #only if we could add enough to fill $l$ do we allow the process to begin.
			yield [], [], 0
		return
	except: raise
	for l, r, lL in altSubsetIter(collGen, k, d + 1):
		if lL < k: #only extend $l$ when there is a deficit.
			yield [val, *l], r, lL + 1
		if mLL <= lL: #only let $l$ persist when it'd be possible to sufficiently extend it.
			yield l, [val, *r], lL

def subDescGen(n, S): #generates all permutations where desc(pi) is a subset of S.  S dicates where the descents can be, but they need not be there.
	return descGenSub(map(operator.add, sorted(S), repeat(1)), iter(range(n)), 0)

def descGenSub(sIter, coll, lS):  #sIter admitting the descents in increasing order (actually, d + 1 for d in desc)
	try: i = next(sIter)
	except StopIteration:
		yield [*coll]
		return
	except: raise
	assert lS < i
	for l, r, _ in altSubsetIter(coll, i - lS):
		for val in descGenSub(sIter, iter(r), i): yield l + val

def opCounter(m, pins, n):
	fixed = set(m).difference(pins)
	unset = set(range(n)).difference(set(m))
	pins = {*pins, n}
	ops = dict()
	m = [*m, n]
	nm = len(m)
	acc = set()
	stable = True
	pOps = dict((p, 0) for p in range(n) if p not in pins)
	pVals = tTAdd(list(filter(lambda i: i in pins, m)))[1]
	p = -1
	pmax = -1
	for i in range(nm):
		prev = p
		p = m[i]
		if p not in pins: acc.add(p); continue
		ops[p] = {*filter(lambda j: j < p and j > prev and j > pmax, unset), *acc}
		if not acc: stable = False
		if p in pVals: pmax = prev
		else: pmax = -1
		acc = set()
		p = -1
	lOps = dict()
	for i in pins:
		lOps[i] = len(ops[i])
		for j in ops[i]: pOps[j] += 1
	return ops, lOps, pOps, stable

def C3(p,v):
	if not p:
		return 1
	acc = 1
	ops = 0
	for i in range(max(p)+1):
		if i in v: ops += 1
		elif i in p: ops -= 1
		else: acc *= ops
	return acc

def C2(p,v): # assuming p,v are sorted lists
	acc = 1
	j = 0
	jMax = len(v)
	for i in range(len(p)):
		pin = p[i]
		while j < jMax and v[j] < pin: j += 1
		acc *= (j - i)*(j - i - 1)//2
	return acc

def pvCount(p, v, n = None):
	oCount = C2(sorted(p), sorted(v)) * C3(p, v)
	if n is not None:
		oCount *= 2**(n - len(v))
	return oCount

def fCount(p, n = None):
	acc = 0
	for v in admValIter(p):
		acc += pvCount(p, v)
	if n is not None:
		acc *= 2**(n - len(p) - 1)
	return acc

def valid(mapping):
	ops = list(range(len(mapping)))
	try:
		for e in mapping:
			ops.remove(e)
	except ValueError:
		return False
	except:
		raise
	else:
		return True

#let elems be a sorted list
# def newPVGen(elems, P, V):
	# k = elems.pop(0)
	# lOps = newPVGen(elems, P, V)
	# for op in lOps:
		
#P be a sorted list
def valeSetGenF(P, pSet = None):
	if pSet is None:
		pSet = {*P}
	pm = P.pop(0)
	if not P:
		for v in filter(lambda i : i not in pSet, range(1, pm)):
			yield [0, v]
		return
	for V in valeSetGenF(P, pSet):
		for v in filter(lambda i : i not in pSet, range(1, min(pm, V[1]))):
			nV = V.copy()
			nV.insert(1, v)
			yield nV

#Again, P is a sorted list
def valeSetGenD(P, vM):
	if vM == 0:
		return
	if vM in P:
		return
	P = P.copy()
	pM = P.pop()
	if vM > pM:
		return
	if not P:
		if vM < pM:
			yield [0, vM]
		return
	for nVM in range(1, vM):
		for V in valeSetGenD(P, nVM):
			V = V.copy()
			V.append(vM)
			yield V

# class BadValeCount(Exception):
	
	# @property
	# def high(self):
		# return self.args[0]
	
	# @property
	# def low(self):
		# return not self.args[0]

# def magicPinGenFull(n, P, k = 0, given = [], addVales = 1):
	# if k == n:
		# if len(given) > 1:
			# raise BadValeCount(True)
		# yield given[0]
		# return
	# if k in P:
		# if len(given) < 2:
			# raise BadValeCount(False)
		# for sub, comp in subsetIterComp(given):
			# yield comp + [sub[0] + (k,) + sub[1]]
			# yield comp + [sub[1] + (k,) + sub[0]]
		# return
	# if addVales:
		# try:
			# for res in magicPinGenFull(n, P, k + 1, given + [(k,)]):
				# pass

def magicPinGenFixedValeCR(n, P, V, k = 0, given = [[]]):
	if k == n:
		return [val[0] for val in given]
	if k in V:
		res = [val + [(k,)] for val in given]
	elif k in P:
		res = [comp + [sub[0] + (k,) + sub[1]] for val in given for sub, comp in subsetIterComp(val, 2)]
	else:
		res = [comp + [sub[0] + (k,)] for val in given for sub, comp in subsetIterComp(val, 1)]
	return magicPinGenFixedValeCR(n, P, V, k + 1, res)

# def valeSetGenU(P, vm, ops = None):
	# if not P:
		# yield [0, vm]
		# return
	# if ops is None:
		# ops = [x for x in range(max(P)) if x not in P]
	# pm = P.pop(0)
	

#counts the number of items in a sorted list less than $x$.\\
def cLessS(sList, x):
	out = 0
	for i in sList:
		if i >= x: break
		out += 1
	return out

def pVPlot(x):
  out = ''
  out += '\\addplot[color=blue,mark=square]coordinates{'
  i = 1
  for j in x: out += '(' + str(i) + ',' + str(j + 1) + ')'; i += 1
  out += '};'
  T = tTAdd(x)[0]
  P = pP(x)[0]
  cov = dict()
  prev = 0
  pend = []
  for k in sorted([*T, *P]):
    if k in T: cov[x[k]] = [True, prev]; prev = k; continue
    cov[x[prev]].append(k)
    prev = k
    pin = x[k]
    while pend:
      p, pPin = pend[-1]
      if pPin > pin: break
      cov[pPin].append(k)
      del(pend[-1])
    if not pend: p = 0
    cov[pin] = [False, p]
    pend.append([k,pin])
  k = len(x)-1
  cov[x[prev]].append(k)
  for _, pin in pend: cov[pin].append(k)
  for val, [green, start, end] in cov.items():
    out += '\n\\addplot[color=' + ('green' if green else 'red') + ',domain=' + str(start+1) + ':' + str(end + 1) + ']{' + str(val + 1) + '};'
  print(out)

def classPlot(x):
	points = dict()
	for i, val in enumerate(x):
		points[val] = (i + 1, val + 1)
	pointType = dict()
	pRes = False
	m = x + [max(x) + 1]
	pVal = m.pop(0)
	for val in m:
		res = pVal < val
		if pRes:
			if res:
				pointType[pVal] = '\\addplot[color=purple,mark=triangle,mark size=4pt]coordinates{'
			else:
				pointType[pVal] = '\\addplot[color=green,mark=o,mark size=4pt]coordinates{'
		else:
			if res:
				pointType[pVal] = '\\addplot[color=red,mark=x,mark size=4pt]coordinates{'
			else:
				pointType[pVal] = '\\addplot[color=black,mark=square,mark size=4pt]coordinates{'
		pRes = res
		pVal = val
	out = '\\begin{tikzpicture}\n\\begin{axis}[\n    height=\\axisdefaultheight*0.8,\n    width=\\textwidth*0.55,\n    title={$_=('
	out += ', '.join(map(lambda i: str(i+1), x))
	out += ')$},\n    xtick={'
	out += ', '.join(map(str, range(1, len(x) + 1)))
	out += '},\n    ytick={'
	out += ', '.join(map(str, range(1, max(x) + 2)))
	out += '},\n    ymajorgrids=true,\n    grid style=dashed,\n    xmin = 0,\n    xmax = ' + str(len(x)+1) + ',\n    ymin = 0,\n    ymax = ' + str(max(x)+2) + '\n]\n'
	out += '\\addplot[color=blue,mark=none]coordinates{'
	for i in x:
		out += str(points[i])
	out += '};\n'
	for i in x:
		out += pointType[i] + str(points[i]) + '};\n'
	out += '\\end{axis}\n\\end{tikzpicture}'
	print(out)

def oldGraphPlot(x, shift = True):
	x = [i + shift for i in x]
	m = max(x)
	pos = [set()] #List of sets, where all elements of a set have an x-position based on the index of that set in pos.
	maxs = [None] #List of maximum elements.
	maxer = {m: None} #Dictionary pointing each element to its maximum element.
	pinExt = list()
	for i in sorted(x, reverse = True):
		loc = maxs.index(maxer[i])
		pos[loc].add(i)
		w1,w2,w4,w5 = xFactor(x,i)
		t1 = w2 == []
		t2 = w4 == []
		below = t1+t2
		if below == 1:
			k = max(w2+w4)
			maxer[k] = maxer[i]
		elif below == 0:
			l = max(w2)
			r = max(w4)
			if l > r: l,r = r,l
			maxer[l] = l
			maxer[r] = r
			pinExt.append((l, i, r))
			maxs.insert(loc, l)
			pos.insert(loc, set())
			maxs.insert(loc + 2, r)
			pos.insert(loc + 2, set())
	out = '\\begin{tikzpicture}\n\\begin{axis}[\n    height=\\axisdefaultheight*0.8,\n    width=\\textwidth*0.55,\n    title={$_=('
	out += ', '.join(map(str, x))
	out += ')$},\n    xtick={'
	out += ', '.join(map(str, range(1, len(pos) + 1)))
	out += '},\n    ytick={'
	out += ', '.join(map(str, range(1, m + 1)))
	out += '},\n    ymajorgrids=true,\n    grid style=dashed,\n    xmin = 0,\n    xmax = ' + str(len(pos)+1) + ',\n    ymin = 0,\n    ymax = ' + str(m + 1) + '\n]\n'
	for x, Y in enumerate(pos, 1):
		out += '\\addplot[color=blue,mark=square]coordinates{'
		out += ''.join(map(str, ((x, y) for y in sorted(Y))))
		out += '};\n'
	for l, i, r in pinExt:
		out += '\\addplot[color=blue,mark=none]coordinates{'
		out += ''.join(map(str, ((maxs.index(l)+1, l), (maxs.index(maxer[i])+1, i), (maxs.index(r)+1, r))))
		out += '};\n'
	out += '\\end{axis}\n\\end{tikzpicture}'
	print(out)

def graphPlot(x, shift = True):
	x = [i + shift for i in x]
	m = max(x)
	pins = pP(x)[1]
	vals = tTAdd(x)[1]
	pV = set.union(pins, vals)
	#P = max(pV)
	#pos = [set()] #List of sets, where all elements of a set have an x-position based on the index of that set in pos.
	#maxs = [P] #List of maximum pinnacles (or single valley).
	#maxer = {P: P} #Dictionary pointing each element to its maximum pinnacle (or single valley).
	pinExt = list()
	open = set() #pinnacles or valleys currently open.
	vCol = dict() #vCol about each pinnacle or valley, as a subword of pos.
	unbound = set(x)
	for i in sorted(pV):
		unbound.remove(i)
		if i in vals:
			open.add(i)
			vCol[i] = ([i],[{i}])
			continue
		w1, w2, w4, w5 = xFactor(x, i) #i is a pinnacle now.
		found = 0
		for i in open:
			if i in w2:
				l = i
				found += 1
			elif i in w4:
				r = i
				found += 1
			if found == 2: break
		if l > r: l, r = r, l; w2, w4 = w4, w2
		pinExt.append((l, i, r))
		lPins, lPoss = vCol[l]
		rPos = rPoss[rPins.index(l)]
		for j in w2:
			if j in unbound:
				unbound.remove(j)
				# maxer[j] = l
				lPos.add(j)
		rPins, rPoss = vCol[r]
		rPos = rPoss[rPins.index(r)]
		for j in w4:
			if j in unbound:
				unbound.remove(j)
				# maxer[j] = r
				rPos.add(j)
		vCol[i] = (lPins + [i] + rPins, lPoss + [{i}] + rPoss)
		open.add(i)
		open.remove(l)
		open.remove(r)
	pPins, pPoss = vCol[i] #i == P
	pPos = pPoss[pPins.index(i)]
	for j in w1+w5:
		unbound.remove(j)
		# maxer[j] = i
		pPos.add(j)
	assert not unbound
	assert open == {i}
	pos = pPoss
	maxs = pPins
	out = '\\begin{tikzpicture}\n\\begin{axis}[\n    height=\\axisdefaultheight*0.8,\n    width=\\textwidth*0.55,\n    title={$_=('
	out += ', '.join(map(str, x))
	out += ')$},\n    xtick={'
	out += ', '.join(map(str, range(1, len(pos) + 1)))
	out += '},\n    ytick={'
	out += ', '.join(map(str, range(1, m + 1)))
	out += '},\n    ymajorgrids=true,\n    grid style=dashed,\n    xmin = 0,\n    xmax = ' + str(len(pos)+1) + ',\n    ymin = 0,\n    ymax = ' + str(m + 1) + '\n]\n'
	for x, Y in enumerate(pos, 1):
		out += '\\addplot[color=blue,mark=square]coordinates{'
		out += ''.join(map(str, ((x, y) for y in sorted(Y))))
		out += '};\n'
	for l, i, r in pinExt:
		out += '\\addplot[color=blue,mark=none]coordinates{'
		out += ''.join(map(str, ((maxs.index(l)+1, l), (maxs.index(i)+1, i), (maxs.index(r)+1, r))))
		out += '};\n'
	out += '\\end{axis}\n\\end{tikzpicture}'
	print(out)