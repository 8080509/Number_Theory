import SymmetricGroups1 as s
from math import floor

import Utils as u

def nC2seq(a,b): #where sequences all integer a,b subject to 0 <= a < b
	return (b*b-b)//2 + a

def nC2deSeq(k): #recovers a and b from k
	b = floor((1+(1+8*k)**0.5)/2)
	a = k - (b*b-b)//2
	return a, b

def bindingBreakdown(m, tracker = None, pins = None):
	if tracker is None:
		tracker = u.housing()
	tracker.value = [None]*(max(m)+1)
	todo = [s.pVFactor(m, pins)]
	pinBinds = {None: set()} #The bindings reserved by the pinnacles
	ascBinds = dict() #The bindings of ascent values to valley collections
	remBinds = [None] #stores remaining values to be bound.
	while todo:
		v, *asc = todo.pop()
		p = remBinds.pop()
		if isinstance(v, list):
			x1, v, x2 = v
			todo.append(x1)
			todo.append(x2)
			pinBinds[v] = set()
			remBinds.append(v)
			remBinds.append(v)
		pinBinds[p].add(v)
		tracker.value[v] = p
		ascBinds[v] = set(asc)
		for a in asc:
			tracker.value[a] = v
	return pinBinds, ascBinds

def arrBind(pinBinds): #Gives back the PV-Factorization of the arrangement with that pinBinds set
	vCol = u.defFuncDict(lambda p, k: [k]) #dictionary of all valley collections under each pinnacle
	out, = pinBinds.pop(None)
	for k, v in pinBinds.items():
		l, r = v
		if l > r: l, r = r, l
		vCol[k].insert(0, vCol[l])
		vCol[k].append(vCol[r])
	return vCol[out]

#Binding Rules:
	#A pinnacle will have bound to it exactly two other items from
	#P u V.  Each is below the pinnacle in question, and each element
	#can only be bound to a single pinnacle.
	#
	#Each element of $ P \cup V $ also binds a number of the ascents,
	#subject to the condition that each ascent is bound exactly once,
	#and that it is between the element, and the pinnacle that element
	#is bound to.

def fullBind(pinBinds, ascBinds):
	vCol = u.defFuncDict(lambda p, k: [k]) #dictionary of all valley collections under each pinnacle
	out, = pinBinds.pop(None)
	for k, v in pinBinds.items():
		l, r = v
		if l > r: l, r = r, l
		vCol[k].insert(0, vCol[l])
		vCol[k].append(vCol[r])
	for k, v in ascBinds.items():
		vCol[k].extend(sorted(v))
	return vCol[out]

def bindSeq(m,  pins = None, vals = None): #Finds binding numbers for all elements.
	if pins is None:
		pins = s.pP(m)[1]
	if vals is None:
		vals = s.tTAdd(m)[1]
	pV = pins.union(vals)
	M = max(m) + 1
	fVals = list() #Valleys and pinnacles not yet bound.
	n_PV = 0 #n_PV function from notes.  Should always match len(fVals)
	bNos = list() # list of binding numbers.
	bPos = list() # list of number of possible binding numbers.
	tracker = u.housing()
	pB, aB = bindingBreakdown(m, tracker, pins.copy())
	for i in sorted(m):
		if i in vals:
			fVals.append(i)
			n_PV += 1
			val = 0
			pos = 1 #Valleys are trivially bound, since we don't consider a valley as bound to a pinnacle, but rather that a pinnacle can bind a valley.
		elif i in pins:
			fVals.append(i) #Technically, this should also have n_PV += 1, but the difference is accounted for.
			l, r = pB[i]
			if l > r: l, r = r, l
			a, b = u.seqInd(fVals, (l, r))
			val = nC2seq(a, b)
			pos = (n_PV*(n_PV-1))//2
			del fVals[a]
			del fVals[b-1]
			n_PV -= 1 #Should be -= 2, but as we never incremented, we only decrement once.
		else:
			val = fVals.index(tracker.value[i])
			pos = n_PV
		bNos.append(val)
		bPos.append(pos)
	return bNos, bPos

def bBRec(bNos, pins, vals, ops = None): #Recovers pB and aB from bNos, pins, vals, and ops (a sorted list or range).
	if ops == None:
		ops = range(max(pins) + 1)
	elif isinstance(ops, int):
		ops = range(ops)
	fVals = list()
	pB = {None: {max(pins)}}
	aB = dict()
	for p in pins:
		aB[p] = set()
	for v in vals:
		aB[v] = set()
	for val, bNo in zip(ops, bNos):
		if val in vals:
			fVals.append(val)
		elif val in pins:
			fVals.append(val)
			a, b = nC2deSeq(bNo)
			l = fVals.pop(a)
			r = fVals.pop(b-1)
			pB[val] = {l, r}
		else:
			aB[fVals[bNo]].add(val)
	return pB, aB

def action(m, acts): #acts is a dict or list containing the orders of the actions on each element.
	pins = s.pP(m)[1]
	vals = s.tTAdd(m)[1]
	bNos, bPos = bindSeq(m, pins, vals)
	if isinstance(acts, dict):
		iterable = acts.items()
	elif isinstance(acts, list):
		iterable = enumerate(acts)
	else:
		raise ValueError('acts argument of action must be a list or dictionary')
	for k, v in iterable:
		bNos[k] = (bNos[k] + v) % bPos[k] #Todo: optimize this.
	pB, aB = bBRec(bNos, pins, vals, sorted(m))
	return s.reFac(fullBind(pB, aB))

def newActRep(p, v, n = None):
	if n is None: n = max(p) if p else 0
	return s.reFac(fullBind(*bBRec(u.repIter(0), p, v, n)))




























