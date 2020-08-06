import json
import numpy as np
from tsp_lkh.main import LKH
from tsp_lkh.tour import TourArray as Tour
from collections import defaultdict

with open('time_distance_2.json', 'r', encoding='utf-8') as f:
    distance_list = json.loads(f.read())

sites = ['S001', 'S1324', 'S110', 'S062', 'S1234', 'S1354', 'S1172', 'S794', 'S1118', 'S217', 'S712', 'S1279',
         'S069', 'S1227', 'S983', 'S586', 'S984', 'S1010', 'S1007', 'S988', 'S1251', 'S1258', 'S1353', 'S1338',
         'S1295', 'S1254']
n = len(sites)
# distance_matrix = np.ones(n).reshape((n, n))
# for i in range(n):
#     for j in range(n):
#         distance_matrix[i, j] = distance_matrix[j, i] = origin_distance_matrix[]

distance_matrix = {}
for info_list in distance_list:
    for info in info_list:
        start = info[0]
        end = info[1]
        distance = info[2]
        time = info[3]
        if start in distance_matrix:
            distance_matrix[start][end] = {'distance': distance, 'time': time}
        else:
            distance_matrix[start] = {end: {'distance': distance, 'time': time}}

my_matrix = np.zeros(n*n).reshape((n, n))
for i in range(n):
    for j in range(i+1, n):
        my_matrix[i, j] = my_matrix[j, i] = distance_matrix[sites[i]][sites[j]]['distance']
for s in range(n):
    my_matrix[s][s] = np.inf

dashun_solver = LKH(my_matrix)
tour0 = Tour(list(range(n)))
result = dashun_solver.run()
route_num = [0]
for _ in range(n-1):
    cur = route_num[-1]
    next = result.links[cur, 1]
    route_num.append(next)
    cur = next
route_site = [sites[i] for i in route_num]

# ------------------------------------------------------------------------

with open('222.json', 'r', encoding='utf-8') as f:
    matrix_station_volume = json.loads(f.read())
stations = []
station_volume_dict = {}
for item in matrix_station_volume:
    stations.append(item['station'])
    station_volume_dict[item['station']] = item['volume']


def make_n_tour(num_rounds: int):
    stations_plus = stations + ['S001']*num_rounds
    total_num = len(stations_plus)
    matrix = np.zeros(total_num*total_num).reshape((total_num, total_num))
    matrix += np.inf
    for i in range(len(stations)):
        for j in range(i+1, total_num):
            matrix[i, j] = matrix[j, i] = distance_matrix[stations_plus[i]][stations_plus[j]]['time']
    solver = LKH(matrix, use_dual_ascent=False, max_depth=5)
    result_n = solver.run()
    route_num = [0]
    for _ in range(total_num - 1):
        cur = route_num[-1]
        next = result_n.links[cur, 1]
        route_num.append(next)
    # route_site = [sites[i] for i in route_num if i < len(stations) else 'S001']
    route_site = []
    for i in route_num:
        if i < len(stations):
            route_site.append(stations[i])
        else:
            route_site.append('S001')
    total_distance = result_n.route_cost(matrix)
    print(f'{num_rounds} rounds: route_site: {route_site}')
    print(f"{num_rounds} rounds: total_distance: {total_distance}")
    return route_site, total_distance


# results = {}
# for i in range(10):
#     route, cost = make_n_tour(i+1)
#     results[str(i+1)] = {'route': route, 'total_cost': cost}


def tour_cost(ll):
    cost = 0
    for i in range(len(ll)-1):
        cost += distance_matrix[ll[i]][ll[i+1]]['distance']
    cost += distance_matrix[ll[-1]][ll[0]]['distance']
    return cost


def tour_volume(ll):
    volume = 0
    for i in range(1, len(ll)):
        volume += station_volume_dict[ll[i]]
    return volume


with open('result_time.json', 'r') as f:
    results = json.loads(f.read())
results_cost_volume = defaultdict(list)
for i in results.keys():
    route = results[i]['route']
    xx = []
    for k, idx in enumerate(route):
        if idx == 'S001':
            xx.append(k)
    xx1 = xx[0]
    # route = route[xx1:] + route[:xx1]
    num_rounds = len(xx)
    rounds = []
    for j in range(num_rounds-1):
        rounds.append(route[xx[j]:xx[j+1]])
    rounds.append(route[xx[num_rounds-1]:]+route[:xx[0]])
    for round in rounds:
        results_cost_volume[i].append({'cost': tour_cost(round), 'volume': tour_volume(round), 'route': round.copy()})

for i in range(len(results_cost_volume)):
    print(f"For {i+1} rounds:")
    for item in results_cost_volume[str(i+1)]:
        print(item)
