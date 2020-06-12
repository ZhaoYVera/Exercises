from binaryheap import BinaryHeap

from test_graph import test_graph, s


def mst_prim(g, s):
    s.key = 0
    s.parent = s
    q = BinaryHeap(list(g))
    #tree = BinaryHeap([])
    tree = []
    while len(q.keys_list) > 0:
        u = q.delete_min_heap()
        u.judge_location = False
        #tree.insert_into_heap(u)
        tree.append(u)
        for v in u.adjacent.keys():
            if v.judge_location and u.adjacent[v] < v.key:
                v.parent = u
                q.decrease_key(v.id_heap, u.adjacent[v])
    return tree


#test_tree = mst_prim(test_graph, s)

#print([(node.name, node.parent.name, node.key) for node in test_tree])
