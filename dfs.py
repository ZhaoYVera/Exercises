from __future__ import annotations
from dataclasses import dataclass


class Graph:
    def __init__(self, adj):
        self.V = self.get_node(adj)
        self.adj = adj.copy()

    @staticmethod
    def get_node(adj):
        return adj.keys()


@dataclass
class Node:
    id: str
    color: str = None
    parent: Node = None
    d: int = 0
    f: int = 0

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


def dfs(graph):
    for item in graph.V:
        u = Node(item)
        u.color = 'white'
        u.parent = None
    time = [0]
    for item in graph.V:
        u = Node(item)
        if u.color == 'white':
            dfs_visit(graph, u, time)
    return graph


def dfs_visit(graph, u, time):
    time[0] += 1
    u.d = time[0]
    u.color = 'grey'
    for item in graph.adj[u]:
        v = Node(item)
        if v.color == 'white':
            v.parent = u
            dfs_visit(graph, v, time)
    u.color = 'black'
    time[0] += 1
    u.f = time[0]
    return


a = Node('a')
b = Node('b')
c = Node('c')
test_adj = {'a': 'bc',  'b': 'ac', 'c': 'ab'}
test_graph = Graph(test_adj)
graph1 = dfs(test_graph)
print([(item, Node(item).color) for item in graph1.V])
