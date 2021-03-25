
import PinnacleCounts as pc
import SymmetricGroups3 as sg3
from timeit import timeit



def numIterable(n, v): return range(v, n + v)
def bitGen(n):
	while n:
		yield n & 1
		n >>= 1

def powGen(iterSrc):
	return map(
		lambda x: map(
			lambda i: i[1],
			filter(
				lambda i: i[0],
				zip(
					bitGen(x),
					iterSrc
				)
			)
		),
		range(1 << len(iterSrc))
	)

def pinSetCandGen(n, v):
	return map(list, powGen(numIterable(n, v)))

def admPinFilt(P, v):
	for i, p in enumerate(P, 1):
		if p - v < 2 * i: return False
	return True

def admPinGen(n, v):
	return filter(lambda i: admPinFilt(i, v), pinSetCandGen(n, v))

def pcCount(n, P, v):
	return pc.fullCount(n, P, v)

def sg3fCountAltVSG(p, n = None):
	acc = 0
	for v in pc.valeSetGen(p, 0):
		acc += sg3.pvCount(p, v)
	if n is not None:
		acc *= 2**(n - len(p) - 1)
	return acc

def pcSg3fcavsg(n, P, v):
	P = [p - v for p in P]
	return sg3fCountAltVSG(P, n)

def pcOrigFCount(n, P, v):
	return pc.origFCount(n, P, v)

def sg3fCount(n, P, v):
	P = [p - v for p in P]
	return sg3.fCount(P, n)

def sg3newPinGenCount(n, P, v):
	P = [p - v for p in P]
	count = 0
	for pi in sg3.newPinGen(P, n): count += 1
	return count

def checkSg3fcBySg3npgcSingle(n, P, v):
	return sg3fCount(n, P, v) == sg3newPinGenCount(n, P, v)

def checkSg3fcBySg3npgcPoly(n, v):
	return all(map(lambda i: checkSg3fcBySg3npgcSingle(n, i, v), admPinGen(n, v)))

def checkSg3fcBySg3npgcPoly_getFail(n, v):	
	for P in admPinGen(n, v):
		if checkSg3fcBySg3npgcSingle(n, P, v): continue
		return (n, P, v)
	return None

def checkPccBySg3fcSingle(n, P, v):
	return pcCount(n, P, v) == sg3fCount(n, P, v)

def checkPccBySg3fcPoly(n, v):
	return all(map(lambda i: checkPccBySg3fcSingle(n, [*i], v), admPinGen(n, v)))

def checkPccBySg3fcPoly_getFail(n, v):	
	for P in admPinGen(n, v):
		if checkPccBySg3fcSingle(n, P, v): continue
		return (n, P, v)
	return None

def checkPcSg3fcavsgBySg3fcSingle(n, P, v):
	return pcSg3fcavsg(n, P, v) == sg3fCount(n, P, v)

def checkPcSg3fcavsgBySg3fcPoly(n, v):
	return all(map(lambda i: checkPcSg3fcavsgBySg3fcSingle(n, [*i], v), admPinGen(n, v)))

def checkPcSg3fcavsgBySg3fcPoly_getFail(n, v):	
	for P in admPinGen(n, v):
		if checkPcSg3fcavsgBySg3fcSingle(n, P, v): continue
		return (n, P, v)
	return None

def checkOfcBySg3fcSingle(n, P, v):
	return pcOrigFCount(n, P, v) == sg3fCount(n, P, v)

def checkOfcBySg3fcPoly(n, v):
	return all(map(lambda i: checkOfcBySg3fcSingle(n, [*i], v), admPinGen(n, v)))

def checkOfcBySg3fcPoly_getFail(n, v):	
	for P in admPinGen(n, v):
		if checkOfcBySg3fcSingle(n, P, v): continue
		return (n, P, v)
	return None

def timeOfc(n, P, v, count = 1):
	return timeit(lambda: pc.origFCount(n, P, v), number = count) / count

def timePcCount(n, P, v, count = 1):
	return timeit(lambda: pc.fullCount(n, P, v), number = count) / count


































