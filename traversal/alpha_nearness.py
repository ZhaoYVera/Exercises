import numpy as np
from binaryheap import BinaryHeap
from prim import CompleteGraph, PrimVertex, prim_array
from operator import itemgetter


def mst_prim(g, source):
    source.key = 0
    source.parent = source
    for node in g:
        node.judge_location = True
    q = BinaryHeap(list(g))
    # tree = BinaryHeap([])
    tree = []
    while len(q.keys_list) > 0:
        u = q.delete_min_heap()
        u.judge_location = False
        # tree.insert_into_heap(u)
        tree.append(u)
        for v in u.adjacent.keys():
            if v.judge_location and u.adjacent[v] < v.key:
                v.parent = u
                q.decrease_key(v.id_heap, u.adjacent[v])
    return tree


test_g = CompleteGraph.build_random_complete_graph(5)


# build a M1T with nodes {1, 2, ..., n-1}
def build_m1t_prim(graph):
    vertices = [PrimVertex(id=i, key=np.inf) for i in range(graph.n - 1)]
    vertices[0].key = 0
    q = list(vertices)
    tree = []
    while len(q) > 0:
        ix, v0 = min(enumerate(q), key=itemgetter(1))
        del q[ix]
        v0.known = True
        tree.append(v0)
        for v_id in graph.adj(v0.id):
            if v_id != graph.n-1:
                v = vertices[v_id]
                w0 = graph.e_weight(v0.id, v.id)
                if not v.known and w0 < v.key:
                    v.key = w0
                    v.parent = v0.id
    # report the total edge weight of the mst
    length_mst = sum(graph.e_weight(vertex.parent, vertex.id) for vertex in vertices[1:])

    n = graph.n
    degree = [1 for _ in range(n)]
    degree[0] = 0
    for i in range(1, n - 1):
        v = vertices[i]
        degree[v.parent] += 1
    degree[n - 1] = 2
    list_n = sorted(graph.adj_mat[graph.n - 1])
    # save for special node
    return [length_mst, tree, degree]
    # build a minimum 1-tree by adding two shortest edge incident to node n


# beta_value: the length of the edge to be removed from the spanning tree when edge (i, j) is added
# for nodes {1, 2, ..., n-1}
# then alpha(i, j) = e(i, j) - beta(i, j)
def beta(tree):
    beta_value = np.ones((test_g.n-1, test_g.n-1))
    for i in range(test_g.n-1):
        beta_value[tree[i].id][tree[i].id] = 0
        for j in range(i+1, test_g.n-1):
            value = max(beta_value[tree[i].id][tree[j].parent], test_g.e_weight(tree[j].id, tree[j].parent))
            beta_value[tree[i].id][tree[j].id] = beta_value[tree[j].id][tree[i].id] = value
    return beta_value


print('beta = ')
print(beta(build_mst_prim(test_g)[1]))


def alpha_nearness(vertices, graph):
    n = graph.n
    alpha = np.ones((n, n))
    for i in range(n):
        alpha[i][i] = 0
        for j in range(i+1, n):
            if i == n-1 or j == n-1:
                list_n = sorted(graph.adj_mat[graph.n-1])
                alpha[i][j] = alpha[j][i] = list_n[1]
            elif i == vertices[j].parent or j == vertices[i].parent:
                alpha[i][j] = alpha[j][i] = 0
            else:
                alpha[i][j] = alpha[j][i] = graph.e_weight(i, j) - beta(build_m1t_prim(graph)[1])[i][j]
    return alpha


print('alpha = ')
print(alpha_nearness(vertices_list, test_g))
