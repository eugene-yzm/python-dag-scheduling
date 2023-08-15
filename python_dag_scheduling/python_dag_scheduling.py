from collections import defaultdict
from collections.abc import Callable

class Vertex:
	def __init__(self, label: str, value: int):
		self.label = label
		self.value = value

	def get_label(self):
		return self.label

	def get_value(self):
		return self.value

	def __key(self):
		return (self.label)

	def __hash__(self):
		return hash(self.__key())

	def __eq__(self, other):
		if isinstance(other, A):
			return self.__key() == other.__key()
		return NotImplemented

	def __repr__(self):
		return self.__key()

# Directed Edge
class Edge:
	def __init__(self, v1: Vertex, v2: Vertex):
		# v1 -> v2
		self.from_v = v1
		self.to_v = v2

	def get_from_v(self):
		return self.from_v

	def get_to_v(self):
		return self.to_v

	def __key(self):
		return (self.from_v, self.to_v)

	def __hash__(self):
		return hash(self.__key())

	def __eq__(self, other):
		if isinstance(other, A):
			return self.__key() == other.__key()
		return NotImplemented

class Graph:
	def __init__(self):
		self.V = set()
		self.E = set()

		# V -> List[E]
		self.assoc_edges = defaultdict(set)

	def get_V(self):
		return self.V

	def get_E(self):
		return self.E

	def add_v(self, v: Vertex):
		self.V.add(v)

	def add_e(self, e: Edge):
		self.E.add(e)
		self.assoc_edges[e.get_from_v()].add(e)
		self.assoc_edges[e.get_to_v()].add(e)

	def get_assoc(self, v: Vertex):
		return self.assoc_edges.get(v)

	def pop_v(self, v: Vertex):
		self.V.discard(v)
		st = self.assoc_edges.get(v)
		if st is not None:
			self.E = self.E.difference(st)

# use-case: sprint tasks capacity planning
def bounded_capacity_topological(g: Graph, constraints: dict) -> list[list[str]]:
	capacity = constraints.get("capacity")
	ans = []
	source = set(g.get_V())
	indeg = defaultdict(int)
	used = set()
	for e in g.get_E():
		indeg[e.get_to_v()] += 1
	for v in g.get_V():
		if indeg.get(v, 0) != 0:
			source.discard(v)

	while len(source) > 0:
		c = 0
		grp = []
		add_back = []
		while len(source) > 0:
			v = source.pop()
			if c + v.get_value() > capacity:
				add_back.append(v)
			else:
				c += v.get_value()
				grp.append(v)
				st = g.get_assoc(v)
				used.add(v)
				if st is not None:
					for e in st:
						indeg[e.get_to_v()] -= 1
						if indeg[e.get_to_v()] < 1:
							v2 = e.get_to_v()
							if v2 not in used:
								source.add(v2)
				g.pop_v(v)

		for v in add_back:
			if v not in used:
				source.add(v)
		ans.append(grp)

	return ans

def apply_strategy(g: Graph, constraints: dict, strategy: Callable[[Graph, int], list[list[str]]]):
	for i, sch_group in enumerate(strategy(g, constraints)):
		print(f"Group {i}: Selected Vertices: {sch_group}") 


def parse(s: str) -> Graph:
	# TODO come up with a tool specification

	gr = Graph()
	p=Vertex("P", 2)
	o=Vertex("O", 3)
	n=Vertex("N", 2)
	m=Vertex("M", 2)
	l=Vertex("L", 3)
	k=Vertex("K", 3)
	j=Vertex("J", 2)
	i=Vertex("I", 3)
	h=Vertex("H", 3)
	g=Vertex("G", 2)
	f=Vertex("F", 2)
	e=Vertex("E", 2)
	d=Vertex("D", 2)
	c=Vertex("C", 2)
	b=Vertex("B", 3)
	a=Vertex("A", 3)
	gr.add_v(a)
	gr.add_v(b)
	gr.add_v(c)
	gr.add_v(d)
	gr.add_v(e)
	gr.add_v(f)
	gr.add_v(g)
	gr.add_v(h)
	gr.add_v(i)
	gr.add_v(j)
	gr.add_v(k)
	gr.add_v(l)
	gr.add_v(m)
	gr.add_v(n)
	gr.add_v(o)
	gr.add_v(p)
	gr.add_e(Edge(f,g))
	gr.add_e(Edge(g,h))
	gr.add_e(Edge(g,i))
	gr.add_e(Edge(j,h))
	gr.add_e(Edge(j,i))
	gr.add_e(Edge(k,j))
	gr.add_e(Edge(k,m))
	gr.add_e(Edge(k,l))
	gr.add_e(Edge(p,l))
	gr.add_e(Edge(c,k))
	gr.add_e(Edge(c,g))
	gr.add_e(Edge(b,l))
	gr.add_e(Edge(a,l))
	gr.add_e(Edge(d,l))
	return gr

apply_strategy(parse(""), {"capacity": 12}, bounded_capacity_topological)

