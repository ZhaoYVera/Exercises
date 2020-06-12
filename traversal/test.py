import json
import collections
from operator import itemgetter
import numpy as np
from prim import CompleteGraph
from search_for_d import best_pi, alpha_nearness, weighted_total_weight, update_graph_weight

with open('20190101010101-001-Stations.json', 'r', encoding='utf-8') as f:
    stations = json.loads(f.read())

n = len(stations)
areas = []
for i in range(n):
    areas.append(stations[i]["area_id"])
areas = set(areas)
areas = list(areas)

partition_graph = collections.defaultdict(list)

for area in areas:
    for item in stations:
        if item['area_id'] == area:
            partition_graph[area].append(item['id'])

lengths = [len(item) for item in partition_graph.values()]
ix, length = max(enumerate(lengths), key=itemgetter(1))
nodes = list(partition_graph.values())[ix]

with open('20190101010101-001-MapMatrix.json', 'r') as f:
    distance_data = json.load(f)

distance_mat = np.zeros((len(nodes), len(nodes)))
for i in range(len(nodes)):
    for j in range(len(nodes)):
        distance_mat[i][j] = distance_data[nodes[i]][nodes[j]]['distance']

graph1 = CompleteGraph(distance_mat)
pi0 = [0 for _ in range(graph1.n)]
print(weighted_total_weight(graph1, pi0))
print(best_pi(graph1))
print(weighted_total_weight(graph1, best_pi(graph1)))


