#import graph
import collections



v_nodes = {'s', 'a', 'b', 'c', 'e', 'd'}

l_betnodes = {('s', 'a'): 3, ('a', 's'): 3, ('a', 'b'): 6, ('b', 'a'): 6, ('b', 's'): 9, ('s', 'b'): 9,
    ('s','c'): 1, ('c', 's'): 1, ('c', 'd'): 7, ('d', 'c'): 7, ('d', 'e'): 2, ('e', 'd'): 2,
    ('e', 's'): 8, ('s', 'e'): 8}

dist = collections.defaultdict(int)
for u in v_nodes:
    dist[u] = 999

dist['s'] = 0

H = dist.copy()
nullset = {}
while (H != nullset):
    w = min(zip(H.values(), H.keys()))
    del H[w[1]]
    for v in v_nodes:
        if (w[1], v) in l_betnodes:
            if dist[v] > w[0] + l_betnodes[(w[1], v)]:
                dist[v] = w[0] + l_betnodes[(w[1], v)]
                H[v] = dist[v]


print(dist)
