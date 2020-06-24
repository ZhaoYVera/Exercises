from __future__ import annotations
from operator import itemgetter
from dataclasses import dataclass, field, make_dataclass
from typing import Any
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import csgraph_from_dense, minimum_spanning_tree
from priorityqueue import PQLL
from linked_list import SLinkedList
import time
import matplotlib.pyplot as plt

plt.style.use('seaborn')


class DenseGraph:

    def __init__(self, adj_mat: np.array, is_complete: bool = True):
        """The vertices of a graph are set to be (0, 1, 2,...,n-1).
        :param adj_mat -- A dense graph is represented by an n-by-n numpy arrary weight_mat such that
        weight_mat[i, j] is the weight of edge(i, j). Note that if the graph is directed,
        the edge order is from i to j. If j is not adjacent to i, then weight_mat[i, j] = np.nan
        By default, weight_mat[i, i] = np.nan
        :param is_complete -- whether the graph is complete.
        """
        self.adj_mat = adj_mat.copy()
        self.n = len(adj_mat)
        self.is_complete = is_complete

    def __iter__(self):
        """Iterating over the vertices of the graph"""
        yield from range(self.n)

    def e_weight(self, i, j):
        """Weight of edge(i, j)"""
        return self.adj_mat[i, j]

    def adj(self, i, is_end=False):
        """returns a generator of adjacent vertices of vertex i.
        If is_end=True, then the graph is directed, and adjacency is defined to be
        that there is an edge whose end is i.
        """
        if self.is_complete:
            # If the graph is complete, then the adjacent vertices are everything except i
            yield from range(i)
            yield from range(i + 1, self.n)
        else:
            nbrs = self.adj_mat[:, i] if is_end else self.adj_mat[i]
            for j in nbrs:
                if not np.isnan(j):
                    yield j

    @classmethod
    def build_random_complete_graph(cls, n, non_edge_val=0):
        adj_mat = np.random.random((n, n))
        adj_mat += adj_mat.T  # make a symmetric matrix, hence undirected graph
        adj_mat[range(n), range(n)] = non_edge_val
        return cls(adj_mat, is_complete=True)


@dataclass(order=True)
class PrimVertex:
    """A vertex class whose attributes are used in Prim's Minimum spanning tree algorithm."""
    id: int = field(compare=False)
    key: float = field(default=np.inf, compare=True)  # The distance to the identified tree component
    parent: int = field(default=None, compare=False)  # parent id in the final MST
    known: bool = field(default=False, compare=False)  #

    def __eq__(self, other):
        return isinstance(other, PrimVertex) and self.id == other.id


# @deco_timer
def prim_llist(graph):
    """Implementation of Prim's Algorithm by linked list"""
    vertices = [PrimVertex(id=i, key=np.inf) for i in range(graph.n)]
    vertices[0].key = 0
    q = SLinkedList(vertices)
    while not q.empty:
        v0 = q.pop_min()
        v0.known = True
        for v_id in graph.adj(v0.id):
            v = vertices[v_id]
            w0 = graph.e_weight(v0.id, v.id)
            if not v.known and w0 < v.key:
                v.key = w0
                v.parent = v0.id
    # report the total edge weight of the mst
    result = sum(graph.e_weight(vertex.parent, vertex.id) for vertex in vertices[1:])
    print(f"the total edge weight of the mst is {result}")
    return result


# @deco_timer
def prim_array(graph):
    """Implementation of Prim's Algorithm by array(i.e. python list)"""
    vertices = [PrimVertex(id=i, key=np.inf) for i in range(graph.n)]
    vertices[0].key = 0
    q = list(vertices)
    while len(q) > 0:
        ix, v0 = min(enumerate(q), key=itemgetter(1))
        del q[ix]
        v0.known = True
        for v_id in graph.adj(v0.id):
            v = vertices[v_id]
            w0 = graph.e_weight(v0.id, v.id)
            if not v.known and w0 < v.key:
                v.key = w0
                v.parent = v0.id
        # report the total edge weight of the mst
    result = sum(graph.e_weight(vertex.parent, vertex.id) for vertex in vertices[1:])
    print(f"the total edge weight of the mst is {result}")
    return result


def prim_bheap(graph):
    pass


def test_arr_ll():
    n_ls = [2 ** k for k in range(7, 12)]
    n_trials = 10
    ll_perf = []
    arr_perf = []
    for n in n_ls:
        print(f"Computing {n}")
        ll_perf.append(0)
        arr_perf.append(0)
        for _ in range(n_trials):
            graph = DenseGraph.build_random_complete_graph(n)
            t0 = time.perf_counter()
            a1 = prim_llist(graph)
            t1 = time.perf_counter()
            ll_perf[-1] += t1 - t0
            t0 = time.perf_counter()
            a2 = prim_array(graph)
            t1 = time.perf_counter()
            arr_perf[-1] += t1 - t0
            assert abs(a1 - a2) < 10 ** -8
            ll_perf[-1] = ll_perf[-1] / n_trials
            arr_perf[-1] = arr_perf[-1] / n_trials
        n_trials -= 1
    plt.loglog(n_ls, ll_perf, label='linked list')
    plt.loglog(n_ls, arr_perf, label='array')
    plt.legend()
    plt.show()


def test_arr_scipy():
    n_ls = [2 ** k for k in range(7, 14)]
    n_trials = 10
    sc_perf = []
    arr_perf = []
    for n in n_ls:
        print(f"Computing {n}")
        sc_perf.append(0)
        arr_perf.append(0)
        for _ in range(n_trials):
            graph = DenseGraph.build_random_complete_graph(n)
            t0 = time.perf_counter()
            # graph_sp = csgraph_from_dense(graph.adj_mat)
            t = minimum_spanning_tree(graph.adj_mat)
            a1 = t.sum()
            t1 = time.perf_counter()
            sc_perf[-1] += t1 - t0
            t0 = time.perf_counter()
            a2 = prim_array(graph)
            t1 = time.perf_counter()
            arr_perf[-1] += t1 - t0
            assert abs(a1 - a2) < 10 ** -8
        sc_perf[-1] /= n_trials
        arr_perf[-1] /= n_trials
        n_trials -= 1
    plt.loglog(n_ls, sc_perf, 'o-', label='scipy')
    plt.loglog(n_ls, arr_perf, 'o-', label='array')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    test_arr_scipy()
    print('haha')
