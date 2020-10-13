from SymmetricGroups3 import *

# extracts the pinnacle and vale set permutation
def pvPerm(pi):
	pPerm = []
	vPerm = []
	piIter = iter(pi)
	pVal = next(piIter)
	pDir = False
	for i in piIter:
		nDir = pVal < i
		if pDir and not nDir: pPerm.append(pVal)
		if not pDir and nDir: vPerm.append(pVal)
		pVal = i
		pDir = nDir
	if not pDir: vPerm.append(pVal)
	return tuple(pPerm), tuple(vPerm)

# computes the minimum vale set for the given pinnacle set
def minValeSet(P):
	V = set()
	count = len(P) + 1
	i = 0
	while count:
		if i not in P: V.add(i); count -= 1
		i += 1
	return V

# creates a dictionary mapping admissible all admissible pinnacle permutations to their admissible vale permutations.
def pvPermDict(P):
	out = dict()
	for pi in magicPinGenFixedValeFull(max(P) + 1, P, minValeSet(P)):
		pPerm, vPerm = pvPerm(pi)
		out.setdefault(pPerm, set())
		out[pPerm].add(vPerm)
	return out

def vPermCount(permDict):
	return {k: len(v) for k, v in permDict.items()}

def test(pd):
	return len(set(len(v) for v in pd.values())) == 1

def fullTest(P):
	return test(pvPermDict(P))