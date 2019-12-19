from Numbers import gcd

def lcm(a,b):
	return a*b//gcd(a,b)

class Cycle:
	
	def __init__(self, *input):
		input = list(input)
		if len(input) <= 1:
			self.data = list()
			self.order = 1
		start = min(input)
		for i in input:
			if input.count(i) != 1:
				raise ValueError('Repeated Inicies in Cycle Definition')
		while input[0] != start:
			input.append(input.pop(0))
		self.data = input
		self.order = len(input)
	
	def __call__(self, input):
		try:
			i = self.data.index(input)
		except ValueError:
			return input
		except:
			raise
		else:
			if i == self.order - 1:
				return self.data[0]
			return self.data[i + 1]

	def __str__(self):
		return '(' + ', '.join(map(lambda i: str(i), self.data)) + ')'
	
	def __repr__(self):
		return 'Cycle' + str(self)
	
	def __eq__(self, other):
		return self.data == other.data
	
	def __iter__(self):
		return iter(self.data)
	
	def __lt__(self, other):
		i = 0
		while True:
			try:
				if self.data[i] < other.data[i]:
					return True
				i += 1
			except IndexError:
				return self.order < other.order
			except:
				raise
	
	def __le__(self, other):
		return (self < other) or (self == other)
	
	def __len__(self):
		return self.order

class Cycles:
	
	def __init__(self, *input):
		cycles = [Cycle(*i) for i in input][::-1]
		items = set()
		for i in input:
			items.update(set(i))
		final = list()
		order = 1
		while len(items) > 0:
			i = min(items)
			cycle = list()
			while i not in cycle:
				items.remove(i)
				cycle.append(i)
				for j in cycles:
					i = j(i)
			if len(cycle) >= 2:
				order = lcm(order,len(cycle))
				final.append(Cycle(*cycle))
		self.data = final
		self.data.sort()
		self.order = order
	
	def __mul__(self, other):
		return Cycles(*self.data, *other.data)
	
	def __call__(self, input):
		functions = self.data[::-1]
		for i in functions:
			input = i(input)
		return input
	
	def __eq__(self, other):
		items = set()
		for i in self.data:
			items.update(set(i))
		for i in other.data:
			items.update(set(i))
		return all(map(lambda i: self(i) == other(i), items))
	
	def __lt__(self, other):
		i = 0
		while True:
			try:
				if self.data[i] < other.data[i]:
					return True
				i += 1
			except IndexError:
				return self.order < other.order
			except:
				raise
	
	def __le__(self, other):
		return (self < other) or (self == other)
	
	def __str__(self):
		return ''.join(map(lambda i: str(i), self.data))
	
	def __repr__(self):
		return 'Cycles(' + ', '.join(map(lambda i: repr(i), self.data)) + ')'

def Generate(*args):
	elements = list()
	new = [*args]
	while len(new) > 0:
		elements.extend(new)
		new = list()
		for i in elements:
			for j in elements:
				k = i*j
				if (k not in elements) and (k not in new):
					new.append(k)
	elements.sort()
	return elements




























