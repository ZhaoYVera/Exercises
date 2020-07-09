from __future__ import annotations
from dataclasses import dataclass


class Graph:
    def __init__(self, adj):
        self.V = self.get_node(adj)
        self.nodes = [Node(k) for k in self.V]
        self.adj = {}
        for u in self.V:
            self.adj[u] = []
            for node in self.nodes:
                if node.id in adj[u]:
                    self.adj[u].append(node)

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


# head function
def dfs(graph):
    for item in graph.nodes:
        item.color = 'white'
        item.parent = None
    time = [0]
    for item in graph.nodes:
        if item.color == 'white':
            dfs_visit(graph, item, time)
    return graph


def dfs_visit(graph, node, time):
    time[0] += 1
    node.d = time[0]
    node.color = 'grey'
    for item in graph.adj[node.id]:
        if item.color == 'white':
            item.parent = node
            dfs_visit(graph, item, time)
    node.color = 'black'
    time[0] += 1
    node.f = time[0]
    return


a = Node('a')
b = Node('b')
c = Node('c')
d = Node('d')
test_adj = {'a': 'bcd',  'b': 'ac', 'c': 'ab', 'd': 'a'}
test_graph = Graph(test_adj)
print([(node.id, node.color) for node in test_graph.nodes])
graph1 = dfs(test_graph)
print([(node.id, node.color, (node.parent.id if node.parent is not None else 'none'), node.d, node.f) for node in graph1.nodes])

# cha ting: only numbers 1-9
# except qi xiao dui!

all_tiles = (1, 2, 3, 4, 5, 6, 7, 8, 9)
quetou = tuple((tile, tile) for tile in all_tiles)
kezi = [(tile, tile, tile) for tile in all_tiles]
shunzi = [(i+1, i+2, i+3) for i in range(7)]
jiegous = kezi + shunzi


def check_in(jiegou, tiles: list):
    result = True
    tmp = tiles.copy()
    for i in jiegou:
        if i in tmp:
            tmp.remove(i)
        else:
            result = False
            break
    return result


def delete_jiegou(jiegou, tiles: list):
    # check_in before delete_jiegou
    tmp = tiles.copy()
    for i in jiegou:
        tmp.remove(i)
    return tmp


def cha_ting(tiles13: list):
    ting = False
    # adding another tile into 13 given tiles, check whether they admit 4*3+2
    for added_tile in all_tiles:
        tiles14 = tiles13 + [added_tile]
        # qv diao que tou
        # quetou = ((tile, tile) for tile in all_tiles)
        for duizi in quetou:
            if check_in(duizi, tiles14):
                tiles12 = delete_jiegou(duizi, tiles14)
                ting = check_hupai(tiles12)
                if not ting:
                    continue
                break
        if not ting:
            continue
        break
    return ting


def check_hupai(tiles):
    if not tiles:
        return True
    # 3, 3, 3, 3
    hupai = False
    jiegous = kezi + shunzi
    for jiegou in jiegous:
        if check_in(jiegou, tiles):
            tmp = delete_jiegou(jiegou, tiles)
            hupai = check_hupai(tmp)
            if not hupai:
                continue
    return hupai


test_tiles13 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 8]
print(cha_ting(test_tiles13))
