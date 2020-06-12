

V = {'s', 'a', 'b', 'c', 'e', 'd'}

l_betnodes = {('s', 'a'): 3, ('a', 's'): 3, ('a', 'b'): 6, ('b', 'a'): 6, ('b', 's'): 9, ('s', 'b'): 9,
    ('s','c'): 1, ('c', 's'): 1, ('c', 'd'): 7, ('d', 'c'): 7, ('d', 'e'): 2, ('e', 'd'): 2,
    ('e', 's'): 8, ('s', 'e'): 8}


class Vertex:
    def __init__(self, name, adjacent, key=999, parent=None, id_heap=0, judge_location=True):
        self.name = name
        self.adjacent = adjacent
        self.key = key
        self.parent = parent
        self.id_heap = id_heap
        self.judge_location = judge_location


s = Vertex('s', {})
a = Vertex('a', {})
b = Vertex('b', {})
c = Vertex('c', {})
d = Vertex('d', {})
e = Vertex('e', {})

s.adjacent = {a: 3, b: 9, c: 1, e: 8}
a.adjacent = {s: 3, b: 6}
b.adjacent = {a: 6, s: 9}
c.adjacent = {s: 1, d: 7}
d.adjacent = {c: 7, e: 2}
e.adjacent = {s: 8, d: 2}

test_graph = {s, a, b, c, d, e}
