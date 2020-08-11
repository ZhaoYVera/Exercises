import json
import collections
import numpy as np
from tsp_lkh.main import LKH

with open('distance_changchun(1).json', 'r', encoding='utf-8') as f:
    distance_list = json.loads(f.read())
my_distance_matrix = {}
# for info_list in distance_list:
for info in distance_list:
    start = info[0]
    end = info[1]
    distance = info[2]
    time = info[3]
    if start in my_distance_matrix:
        my_distance_matrix[start][end] = {'distance': distance, 'time': time}
    else:
        my_distance_matrix[start] = {end: {'distance': distance, 'time': time}}

with open('order_changchun(1).json', 'r', encoding='utf-8') as f:
    orders = json.loads(f.read())

orders_pickup = orders['pickup']
orders_deliver = orders['deliver']
orders_pd = orders['城配']

data_pickup = collections.defaultdict(int)
# for order in orders_pickup:
#     order_id = order['订单号']
#     start_site_id = order['start']
#     end_site_id = order['end']
#     start_hub = order['start_hub']
#     end_end = order['end_hub']
#     volume = order['volume']
#     data_pickup[order_id] = {'volume': volume, 'start': start_site_id}

for order in orders_pickup:
    data_pickup[order['start']] += order['volume']

data_deliver = collections.defaultdict(int)
for order in orders_deliver:
    data_deliver[order['end']] += order['volume']

data_pd = collections.defaultdict(int)
for order in orders_pd:
    data_pd[order['end']] += order['volume']

sites_pickup = list(data_pickup.keys()) + ['吉林长春']
sites_deliver = list(data_deliver.keys()) + list(data_pd.keys()) + ['吉林长春']
# sites_deliver = ['S1368', 'S1427'] + sites_deliver


def get_best_route(sites_name: list):
    num_sites = len(sites_name)
    distance_matrix = np.zeros((num_sites, num_sites))
    for i in range(num_sites):
        for j in range(i+1, num_sites):
            distance_matrix[i, j] = distance_matrix[j, i] = my_distance_matrix[sites_name[i]][sites_name[j]]['distance']
        distance_matrix[i, i] = np.inf
    farthest_idx = distance_matrix[0, :-1].argmax()
    distance_matrix[farthest_idx, -1] = distance_matrix[-1, farthest_idx] = 1
    solver = LKH(distance_matrix)
    tsp_result = solver.run()
    route = [sites_name[i] for i in tsp_result.iter_vertices()]
    print(route)
    return route


print('Action: pickup')
route_pickup = get_best_route(sites_pickup)
print('Action: deliver')
route_deliver = get_best_route(sites_deliver)

with open('lnglat_hub.json', 'r', encoding='utf-8') as f:
    lnglat_hub = json.loads(f.read())
with open('lnglat_normal.json', 'r', encoding='utf-8') as f:
    lnglat_normal = json.loads(f.read())

# pickup_lnglat = []
# for site in route_pickup:
#     if site == '吉林长春':
#         pickup_lnglat.append(lnglat_hub['吉林长春'])
#     else:
#         pickup_lnglat.append(lnglat_normal[site])
# print(pickup_lnglat)
# for i in pickup_lnglat:
#     print(i)
# deliver_lnglat = []
# for site in route_deliver:
#     if site == '吉林长春':
#         deliver_lnglat.append(lnglat_hub['吉林长春'])
#     else:
#         deliver_lnglat.append(lnglat_normal[site])
# print(deliver_lnglat)
# for i in deliver_lnglat:
#     print(i)

# sites = ['S295', 'S289', 'S033', '吉林长春', 'S1371', 'S1321', 'S587', 'S1057', 'S487', 'S1201', 'S485', 'S651', 'S1238', 'S643', 'S744', 'S745', 'S832', 'S833']
sites = ['S295', 'S289', 'S033', '吉林长春'] + list(reversed(route_deliver))[1:]
lnglat = []
for site in sites:
    if site == '吉林长春':
        lnglat.append(lnglat_hub['吉林长春'])
    else:
        lnglat.append(lnglat_normal[site])
# print(deliver_lnglat)
for i in lnglat:
    print('[', i, '],')

