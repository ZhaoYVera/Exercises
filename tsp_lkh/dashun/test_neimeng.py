import json
import collections
import numpy as np
from tsp_lkh.main import LKH

with open('order_changchun_new(1).json', 'r', encoding='utf-8') as f:
    orders = json.loads(f.read())

data_deliver = collections.defaultdict(int)
for order in orders:
    data_deliver[order['end']] += order['volume']

sites_deliver = list(data_deliver.keys()) + ['吉林长春']

with open('distance_changchun_new.json', 'r', encoding='utf-8') as f:
    distance_list = json.loads(f.read())
my_distance_matrix = {}
for info in distance_list:
    start = info[0]
    end = info[1]
    distance = info[2]
    time = info[3]
    if start in my_distance_matrix:
        my_distance_matrix[start][end] = {'distance': distance, 'time': time}
    else:
        my_distance_matrix[start] = {end: {'distance': distance, 'time': time}}


def get_best_route(sites_name: list):
    num_sites = len(sites_name)
    distance_matrix = np.zeros((num_sites, num_sites))
    for i in range(num_sites):
        for j in range(i+1, num_sites):
            distance_matrix[i, j] = distance_matrix[j, i] = my_distance_matrix[sites_name[i]][sites_name[j]]['distance']
        distance_matrix[i, i] = np.inf
    # if 'S930' in sites_name:
    #     idx = sites_name.index('S930')
    # else:
    #     idx = distance_matrix[0, 1:].argmax() + 1
    # idx = distance_matrix[0, 1:].argmax() + 1
    # distance_matrix[farthest_idx, -1] = distance_matrix[-1, farthest_idx] = 1
    # distance_matrix[idx, -1] = distance_matrix[-1, idx] = 1
    solver = LKH(distance_matrix)
    tsp_result = solver.run()
    route = [sites_name[i] for i in tsp_result.iter_vertices()]
    print(route)
    return route


with open('lnglat_hub.json', 'r', encoding='utf-8') as f:
    lnglat_hub = json.loads(f.read())
with open('lnglat_normal.json', 'r', encoding='utf-8') as f:
    lnglat_normal = json.loads(f.read())

print('Action: deliver')
route_deliver = get_best_route(sites_deliver)

idd = route_deliver.index('吉林长春')
sites = list(reversed(route_deliver[:idd+1])) + list(reversed(route_deliver[idd+1:]))
lnglat = []
for site in sites:
    if site == '吉林长春':
        lnglat.append(lnglat_hub['吉林长春'])
    else:
        lnglat.append(lnglat_normal[site])

for i in lnglat:
    print('[', i, '],')

xx = []
yy = []
for i in lnglat:
    ii = i.split(',')
    xx.append(float(ii[0]))
    yy.append(float(ii[1]))

import matplotlib.pyplot as plt
plt.plot(xx, yy)
plt.show()
