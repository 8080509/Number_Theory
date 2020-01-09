
from timeit import timeit

import SymmetricGroups2 as sg2
import PinnacleActions1 as pa1

def bpgTTest(n, P, count = 1):
	"""Tests average runtime of sg2.badPinGen over 'count' (default 1) trials.
	Note that 'P' must be a set."""
	return timeit('[*badPinGen(%s, %s)]' % (repr(P), repr(n)), 'from SymmetricGroups2 import badPinGen', number = count) / count

def gpgTTest(n, P, count = 1):
	"""Tests average runtime of sg2.goodPinGen over 'count' (default 1) trials."""
	return timeit('[*goodPinGen(%s, %s)]' % (repr(P), repr(n)), 'from SymmetricGroups2 import goodPinGen', number = count) / count

def mpgTTest(n, P, count = 1):
	"""Tests average runtime of sg2.magicPinGenFull over 'count' (default 1) trials.
	Note that 'P' must be a set."""
	return timeit('[*magicPinGenFull(%s, %s)]' % (repr(n), repr(P)), 'from SymmetricGroups2 import magicPinGenFull', number = count) / count

def abgTTest(n, P, count = 1):
	"""Tests average runtime of pa1.ActionBasedGen over 'count' (default 1) trials."""
	return timeit('ActionBasedGen(%s, %s)' % (repr(n), repr(P)), 'from PinnacleActions1 import ActionBasedGen', number = count) / count

def convToTupleSet(iterable):
	return {*map(tuple, iterable)}

def slowAdmPinGen(n):
	return filter(sg2.admPinTest, sg2.powIter([*range(n)][::-1]))

def apgVTest(n):
	return convToTupleSet(slowAdmPinGen(n)) == convToTupleSet(sg2.admPinGen(n))

def tableGen(n, count = 1):
	for P in sorted(sg2.admPinGen(n), key = lambda i: (len(i), i)):
		pSet = {*P}
		print('\\{%s\\} & %d & %.2f ms & %.2f ms & %.2f ms & %.2f ms \\\\\\cline{2-7}' % (
			', '.join(map(lambda i: str(i + 1), P)),
			len({*sg2.magicPinGenFull(n, pSet)}),
			bpgTTest(n, pSet, count) * 1000,
			gpgTTest(n, pSet, 10 * count) * 1000,
			abgTTest(n, pSet, 10 * count) * 1000,
			mpgTTest(n, pSet, 10 * count) * 1000,
		))

def altTableGen(n, count = 1):
	for P in sorted(sg2.admPinGen(n), key = lambda i: (len(i), i)):
		pSet = {*P}
		print('\\{%s\\} & %d & %.2f ms & %.2f ms & %.2f ms \\\\\\cline{2-7}' % (
			', '.join(map(lambda i: str(i + 1), P)),
			len({*sg2.magicPinGenFull(n, pSet)}),
			gpgTTest(n, pSet, count) * 1000,
			abgTTest(n, pSet, count) * 1000,
			mpgTTest(n, pSet, count) * 1000,
		))

def megaTest(n):
	for P in sorted(sg2.admPinGen(n), key = lambda i: (len(i), i)):
		pSet = {*P}
		print(P, convToTupleSet(sg2.goodPinGen(pSet, n)) == convToTupleSet(sg2.magicPinGenFull(n, pSet)))

# def compGen(g1, g2



















