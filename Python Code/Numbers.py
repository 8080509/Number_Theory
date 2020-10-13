cache = [[],[]]

from fractions import Fraction

import collections

numberClasses = (int, Fraction)

indVar = 0

def ioDebug(func):
	def temp(*args, **kwargs):
		global indVar
		print(('|' * indVar) + 'Calculating:  ', func.__name__, args, kwargs)
		indVar += 1
		val = func(*args, **kwargs)
		indVar -= 1
		print(('|' * indVar) + 'Result:  ', func.__name__, args, kwargs, '  :  ', val)
		return val
	return temp

class primeClass:
	
	def __init__(self):
		self.data = [2]
	
	def old_extendOne(self):
		searching = True
		p = self.data[-1] + 1
		while searching:
			testing = True
			q = self.data.__iter__()
			try:
				while testing:
					if divs(q.__next__(), p):
						testing = False
			except StopIteration:
				searching = False
			else:
				p += 1
		self.data.append(p)
		return p
	
	def nextPrime(self, n):
		p = n + 1
		while True:
			if p in self:
				break
			p += 1
		return p
	
	def extendOne(self):
		self.data.append(self.nextPrime(self.data[-1]))
	
	def __getitem__(self, i):
		while i >= len(self.data):
			self.extendOne()
		return self.data[i]
	
	#def __contains__(self, elem):
	#	while elem > self.data[-1]:
	#		self.extendOne()
	#	return elem in self.data
	
	def __contains__(self, elem):
		if elem < 2:
			return False
		if elem in self.data:
			return True
		else:
			max = floorSqRt(elem)
			good = True
			for p in self:
				if p > max:
					break
				if divs(p, elem):
					good = False
					break
			return good
	
	def __iter__(self):
		i = 0
		while True:
			yield self[i]
			i += 1
		return temp

primes = primeClass()

class linComb(collections.MutableMapping):
	
	def __clean__(self):
		marked = set()
		for key in self:
			if self[key] == 0:
				marked.add(key)
		for key in marked:
			del(self[key])
	
	def __str__(self):
		msg = str()
		for key in self:
			msg += str(self[key]) + key + ' + '
		return msg[:-3]
	
	__repr__ = __str__
	
	def __init__(self, input = None):
		self.coeffs = dict()
		if isinstance(input, (linComb, dict)):
			self.coeffs = dict(input)
		elif isinstance(input, numberClasses):
				self[''] = input
		elif input != None:
			raise TypeError()
		self.__clean__()
	
	def __mul__(self, scal):
		assert isinstance(scal, numberClasses)
		output = linComb()
		for key in self:
			output[key] = scal * self[key]
		return output
	
	__rmul__ = __mul__
	
	def __add__(self, other):
		out = linComb(self)
		if isinstance(other, linComb):
			for key in other:
				out[key] += other[key]
		elif isinstance(other, numberClasses):
			out[''] += other
		else:
			raise TypeError('Linear Combinations can only add integers or other linear combinations.')
		return out
	
	__radd__ = __add__
	
	def __neg__(self):
		out = linComb()
		for key in self:
			out[key] = -self[key]
		return out
	
	def __sub__(self, other):
		return self + (-other)
	
	def __rsub__(self, other):
		return other + (-self)
	
	def __div__(self, other):
		if not isinstance(other, numberClasses):
			raise TypeError()
		out  = linComb()
		for key in self:
			out[key] = Fraction(self[key], other)
		return out
	
	def __floordiv__(self, other):
		if not isinstance(other, numberClasses):
			raise TypeError()
		out  = linComb()
		for key in self:
			out[key] = self[key] // other
		return out
	
	def __mod__(self, other):
		if not isinstance(other, numberClasses):
			raise TypeError()
		out = linComb()
		for key in self:
			out[key] = self[key] % other
		return out
	
	def __iter__(self):
		for key in self.coeffs:
			yield key
	
	def __len__(self):
		return len(self.coeffs)
	
	def __setitem__(self, key, item):
		self.coeffs[key] = item
	
	def __getitem__(self, key):
		if key in self.coeffs:
			return self.coeffs[key]
		else:
			return 0
	
	def __delitem__(self, key):
		if key in self.coeffs:
			del(self.coeffs[key])
	
	def assume(self, **kwargs):
		out = linComb(self)
		acc = linComb()
		for key in kwargs:
			acc += (out.pop(key) * kwargs[key])
		return out + acc
	
	def solveFor(self, key, equates = 0):
		temp = linComb(self)
		denom = temp.pop(key)
		return ((equates - temp)/denom)
	
	def __eq__(self, other):
		if isinstance(other, (linComb, int, Fraction)):
			temp = self - other
			return len(linComb(temp)) == 0
		else:
			return False
	
	def __int__(self):
		temp = linComb(self)
		out = temp.pop('')
		if len(temp) == 0:
			return int(out)
		else:
			raise ValueError('linComb objects can only be integers if they have no variables.')

def lIndex(L, index):
	if isinstance(L, list) or isinstance(L, dict):
		return L[index]
	else:
		return L

#def cacheBuilder(function):
#	def temp(*args,**kwargs):
#		if function in cache[0]:
#			funLoc = cache[0].index(function)
#		else:
#			funLoc = -1
#			cache[0].append(function)
#			cache[1].append([])

def cacheBuilder_unused(function, flag):
	def temp(*args,**kwargs):
		if flag not in cache:
			cache[flag] = [[],[]]
		if [args, kwargs] in cache[flag][0]:
			loc = cache[flag][0].index([args, kwargs])
		else:
			loc = -1
			cache[flag][0].append([args,kwargs])
			cache[flag][1].append(function(*args,**kwargs))
		return cache[flag][1][loc]
	return temp

#class VarShell:
#	@property
#	def value(self):
#		if self._v == None:
#			return self
#		else:
#			return self._v
#	
#	@value.setter
#	def value(self, val):
#		if self.valReq == None:
#			if not self.valReq(val):
#				raise ValueError('The input value, ' + str(val) + ', did not meet the assignment condidtion.')
#		self._v = val
#	
#	@value.deleter
#	def value(self):
#		self._v = None

def gcdList(tA, tB, show = False):
	a = tA
	b = tB
	pairList = []
	quoList = []
	while b > 0:
		pairList.append([b, a % b])
		quoList.append(a//b)
		if show:
			print(str(a) + ' = ' + str(quoList[-1]) + ' * ' + str(pairList[-1][0]) + ' + ' + str(pairList[-1][1]))
		a, b = pairList[-1]
	return a, quoList, pairList

def gcd(a, b):
	return gcdList(a, b)[0]

def divs(d, c):
	return c % d == 0

def remAsLinComb(q):
	return (1, -q)

#@lru_cache
def gcdAsLinComb(qL):
	if len(qL) == 0:  #Corresponds with b = 0.  gcd(a,0) = a, so return 1*a + 0*b, or (1,0)
		return (1,0)
	elif len(qL) == 1:  #Corresponds with a = nb + r, and r = 0, so b is the gcd.  Return (0,1)
		return (0,1)
	else:
		#r_k = r_k-2 - n_k r_k-1
		lC2 = gcdAsLinComb(qL[:-2])
		lC1 = gcdAsLinComb(qL[:-1])
		return (lC2[0] - (qL[-2] * lC1[0]), lC2[1] - (qL[-2] * lC1[1]))

def old_solveLinCong(A, C, M):  #finds all x such that ax = c (mod m)
	D = gcdList(A, M)
	d = D[0]
	u, v = gcdAsLinComb(D[1])
	if divs(d, C):
		m = M // d
		x0 = ((C // d) * u)
		if m == 0:
			return [x0]
		else:
			x0 %= m
			return [x0 + (i * m) for i in range(d)]
	else:
		return []

def solveLinCong(A, C, M, kName = 'k'):  #finds all x such that ax = c (mod m)
	D = gcdList(A, M)
	d = D[0]
	u, v = gcdAsLinComb(D[1])
	if divs(d, C):
		m = M // d
		#print('A : ', A, '   C: ', C, '   M: ', M, '   d: ', d,'   u: ', u)
		x0 = ((C // d) * u)
		#print('x0: ',x0)
		if m == 0:
			return x0, dict()
		else:
			x0 %= m
			return (x0 + linComb({kName: m})), {kName: range(d)}
	else:
		return None, {kName: None}

def invert(a, m):
	ans = int(solveLinCong(a, 1, m)[0].assume(k = 0))
	if ans == None:
		raise ValueError('Cannot invert "' + str(a) + '" under the modulus "' + str(m) + '".')
	else:
		return ans

def old_solveDioEqn(aList, C, M = 0):  #finds solutions to a1 x1 + a2 x2 + a3 x3 ... = c (mod m).  Returns solutions ([x0 LinComb, x1 LinComb, ...], validRanges dict).  Might change to [[x0,x1,x2...],[x0',x1',x3'...]
	if len(aList) == 0:  #a0 x0 = C (mod M)
		return dict(), dict()
	else:
		xDict, kRanges = solveDioEqn(aList[:-1], C, gcd(aList[-1], M))  #solutions require a1 x1 + a2 x2 ... a(n-1) x(n-1) = c (mod gcd(an, m))
		print('xDict :', xDict)
		n = len(aList) - 1
		RHS = C
		temp = list()
		for i in range(n):
			temp.append(['x' + str(i), aList[i]])
		RHS -= linComb(dict(temp))
		print('RHS: ',RHS)
		c = RHS.assume(**xDict)
		print('c: ',c)
		xVal, kRange = solveLinCong(aList[n], c, M, kName = 'k' + str(n))
		xDict['x' + str(n)] = xVal
		kRanges.update(kRange)
		return xDict, kRanges

def solveDioEqn(tXComb, C, M = 0, kName = 'k'):  #finds solutions to a1 x1 + a2 x2 + a3 x3 ... = c (mod m).  Returns solutions ([x0 LinComb, x1 LinComb, ...], validRanges dict).  Might change to [[x0,x1,x2...],[x0',x1',x3'...]
	xComb = linComb(tXComb)
	if len(xComb) == 0:  #Nothing... = C (mod M)
		return dict(), dict()
	else:
		term = set(xComb).pop()
		coeff = xComb.pop(term)
		xDict, kRanges = solveDioEqn(xComb, C, gcd(coeff, M), kName = kName)  #solutions require a1 x1 + a2 x2 ... a(n-1) x(n-1) = c (mod gcd(an, m))
		print('xDict :', xDict)
		n = len(xComb)
		RHS = C - xComb
		print('RHS: ',RHS)
		c = RHS.assume(**xDict)
		print('c: ',c)
		xVal, kRange = solveLinCong(coeff, c, M, kName = kName + '.' + str(n))
		xDict[term] = xVal
		kRanges.update(kRange)
		return xDict, kRanges

def solveDioSys(argList, kName = 'k'):
	res = dict() # res = {'x': -LinComb for x, 'y': -LinComb for y, ...}
	for args in argList:
		rem = set(args[0]) - set(res)
		xComb = args[0].assume(**res)
		C = args[1] - xComb.pop('')
		if len(args) > 2:
			M = args[2]
		else:
			M = 0
		kDict = solveDioEqn(xComb, C, M, kName)[0]
		tRes = res
		for term in rem:
			tRes[term] = linComb(dict([[term,1]]))
		res = dict()
		for key in tRes:
			res[key] = tRes[key].assume(**kDict)
	return res

def old_factor(n):
	temp = n
	acc = dict()
	i = 2
	if temp < 0:
		temp *= -1
		acc[-1] = 1
	while temp > 1:
		if divs(i, temp):
			temp //= i
			acc[i] = acc.get(i,0) + 1
		else:
			i += 1
	return acc

def factor(n):
	temp = n
	acc = dict()
	if temp < 0:
		temp *= -1
		acc[-1] = 1
	items = primes.__iter__()
	p = items.__next__()
	tSqrt = floorSqRt(temp)
	while temp > 1:
		if divs(p, temp):
			temp //= p
			acc[p] = acc.get(p, 0) + 1
			tSqrt = floorSqRt(temp)
		elif p > tSqrt:
			p = temp
		else:
			p = items.__next__()
	return acc

@ioDebug
def lSymbol(a, b):
	if not (b in primes):
		raise ValueError('lSymbol\'s second argument must be prime.  The given argument was:  ' + str(b))
	if a >= b:
		print('Taking Modulus')
		return lSymbol(a % b, b)
	elif a == 2:
		print('Shifting to Negatives')
		return lSymbol(a - b, b)
	elif (a == 1) or (a == 0):
		print('Reached Trivial')
		return 1
	elif a == -1:
		print('Simple Case')
		return (-1) ** (((b - 1)//2) % 2)
	elif a in primes:
		print('Reciprocating')
		if ((a % 4) == 3) and ((b % 4) == 3):
			print('Negating')
			return -lSymbol(b, a)
		else:
			return lSymbol(b, a)
	else:
		tTemp = factor(a)
		print('Factoring to:  ', tTemp)
		temp = set()
		for key in tTemp:
			if (tTemp[key] % 2) == 1:
				temp.add(key)
		acc = 1
		for item in temp:
			acc *= lSymbol(item, b)
		return acc

@ioDebug
def qResSolve(tA, p): #For solving x^2 = a mod p
	#if lSymbol(tA, p) == -1:
	#	return None
	#else:
	acc = 1
	a = tA
	a %= p
	while True:
		print(acc, a)  #At all stages, a * acc^2 = tA mod p
		temp = factor(a)
		a = 1
		for fact in temp:
			acc *= fact ** (temp[fact] // 2)
			if temp[fact] % 2:
				a *= fact
		acc %= p
		if a == 1:
			break
		a += p
	return acc

def mQuadRed(a, b, c, m):  #Changes ax^2 + bx + c = 0 mod m to (x - h) = k mod m
	e = invert(a, m) # Now we have x^2 + e b x + e c = 0 mod m
	b1 = (e * b) % m
	if not divs(2, b1):
		b1 += m #m should be odd...
	h = (-b1 // 2) % m
	return ((h ** 2) - (e * c)) % m, m, h

def contFracGen(x, depth = 100):
	out = [int(x//1)]
	x -= out[-1]
	while x != 0 and depth > 0:
		x = 1/x
		out.append(int(x//1))
		x -= out[-1]
		depth -= 1
	return out

def contFracToFrac(aList):
	a = list(aList)
	x = Fraction(0)
	while len(a) > 0:
		x += a.pop()
		x = 1/x
	return 1/x

def old_fastExp(b, e, m = 0):  #Uses binary, and modular reductions if applicable.
	expList = []  #it should be the case that L[i] = b^(2^i)
	def lAssign(item):
		if m != 0:
			item %= m
		expList.append(item)
	ind = 0
	lAssign(b)
	while True:
		ind += 1
		if 2**ind > e:
			break
		lAssign(expList[-1]**2)
	ind -= 1
	acc = 1
	while ind >= 0:
		exp = 2**ind
		if e >= exp:
			e -= exp
			acc *= expList[ind]
			if m != 0:
				acc %= m
		ind -= 1
	return acc

def fastExp(b, e, m = 0):
	acc = 1
	while e > 0:
		if m != 0:
			b %= m
		if e % 2:
			e -= 1
			acc *= b
			if m != 0:
				acc %= m
		e //= 2
		b **= 2
	return acc

def old_floorLog(y, b):
	temp = 1
	exp = 0
	while True:
		temp *= b
		if temp > y:
			break
		exp += 1
	return exp

def floorLog(y, b):
	L = 0
	U = 1
	Out = b
	while Out <= y:
		L = U
		U *= 2
		Out **= 2
	while U - L > 1:
		temp = (U + L) // 2
		if fastExp(b, temp) <= y:
			L = temp
		else:
			U = temp
	return L

def floorSqRt(n):
	L = 0  #L^2 <= n
	U = 2  #n < U^2
	Out = 4
	while Out <= n:  #Increasing
		L = U
		U = Out
		Out *= Out
	#Now L^2 <= n < U^2;  U = L^2
	while U - L > 1:
		temp = (U + L) // 2
		if temp * temp <= n:
			L = temp
		else:
			U = temp
	return L

def pollFactAttempt(N, a, B):
	for p in primes:
		if p > B:
			break
		a = fastExp(a, (p ** floorLog(B, p)), N)
	out = gcdList(a - 1, N)
	print(a, out)
	return out[0]












