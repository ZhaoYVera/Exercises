import graph
import collections

len_way = collections.defaultdict(int)
init_way = ('s')
len_way[init_way] = 0
v_al = {'s'}



def transfer_into_set(dict):
    set_way = []
    for atuple in dict:
        new_set = set(atuple)
        set_way.append(new_set)
    return set_way



while graph.v_nodes not in transfer_into_set(len_way.keys()):
    way = min(zip(len_way.values(), len_way.keys()))
    del len_way[way[1]]
    for v in graph.v_nodes:
        if (way[1][-1], v) in graph.l_betnodes.keys():
            new_way = list(way[1])
            new_way.append(v)
            len_way[tuple(new_way)] = way[0] + graph.l_betnodes[way[1][-1], v]

            v_al.add(v)


result = collections.defaultdict(int)
for way in len_way.keys():
    if set(way) == graph.v_nodes:
        result[way] = len_way[way]


print(result)



