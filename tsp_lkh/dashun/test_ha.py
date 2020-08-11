import json
import collections
import numpy as np
from tsp_lkh.main import LKH

with open('order_ha.json', 'r', encoding='utf-8') as f:
    orders = json.loads(f.read())

orders_pickup = orders['pickup']
orders_deliver = orders['deliver']

data_pickup = collections.defaultdict(int)
for order in orders_pickup:
    data_pickup[order['start']] += order['volume']

data_deliver = collections.defaultdict(int)
for order in orders_deliver:
    data_deliver[order['end']] += order['volume']

sites_pickup = list(data_pickup.keys()) + ['黑龙江哈尔滨']
sites_deliver = list(data_deliver.keys()) + ['黑龙江哈尔滨']
sites_deliver = sites_deliver[1:]
# sites_deliver.remove('S1368')
# sites_deliver.remove('S1427')

with open('111.json', 'r', encoding='utf-8') as f:
    my_distance_matrix = json.loads(f.read())
# my_distance_matrix = {}
# for info_list in distance_list:
# for info in distance_list:
#     start = info[0]
#     end = info[1]
#     distance = info[2]
#     time = info[3]
#     if start in my_distance_matrix:
#         my_distance_matrix[start][end] = {'distance': distance, 'time': time}
#     else:
#         my_distance_matrix[start] = {end: {'distance': distance, 'time': time}}


def get_best_route(sites_name: list):
    num_sites = len(sites_name)
    distance_matrix = np.zeros((num_sites, num_sites))
    for i in range(num_sites):
        for j in range(i+1, num_sites):
            distance_matrix[i, j] = distance_matrix[j, i] = my_distance_matrix[sites_name[i]][sites_name[j]]
        distance_matrix[i, i] = np.inf
    if 'S930' in sites_name:
        idx = sites_name.index('S930')
    else:
        idx = distance_matrix[0, 1:].argmax() + 1
    # distance_matrix[farthest_idx, -1] = distance_matrix[-1, farthest_idx] = 1
    distance_matrix[idx, -1] = distance_matrix[-1, idx] = 1
    solver = LKH(distance_matrix)
    tsp_result = solver.run()
    route = [sites_name[i] for i in tsp_result.iter_vertices()]
    print(route)
    return route


with open('lnglat_hub.json', 'r', encoding='utf-8') as f:
    lnglat_hub = json.loads(f.read())
with open('lnglat_normal.json', 'r', encoding='utf-8') as f:
    lnglat_normal = json.loads(f.read())

print('Action: pickup')
route_pickup = get_best_route(sites_pickup)
print('Action: deliver')
route_deliver = get_best_route(sites_deliver)

# sites = ['S345', '黑龙江哈尔滨'] + route_deliver[2:] + route_deliver[:1]
# sites = route_deliver[2:] + route_deliver[:1]
idd = route_deliver.index('黑龙江哈尔滨')
# sites = ['S345', '黑龙江哈尔滨', 'S444', 'S235', 'S475', 'S580', 'S581', 'S582', 'S740', 'S1096', 'S640', 'S483', 'S465', 'S503', 'S1144', 'S699', 'S482', 'S532', 'S1146', 'S670', 'S389', 'S659', 'S390', 'S1289', 'S930', 'S1368', 'S1427', 'S956', 'S932', 'S978', 'S695', 'S901', 'S766', 'S414', 'S152']
sites = ['S345'] + list(reversed(route_deliver[:idd+1])) + list(reversed(route_deliver[idd+1:]))
lnglat = []
for site in sites:
    if site == '黑龙江哈尔滨':
        lnglat.append(lnglat_hub['黑龙江哈尔滨'])
    else:
        lnglat.append(lnglat_normal[site])

for i in lnglat:
    print('[', i, '],')
# xx = []
# yy = []
# for i in lnglat:
#     ii = i.split(',')
#     xx.append(float(ii[0]))
#     yy.append(float(ii[1]))
#
# import matplotlib.pyplot as plt
# plt.plot(xx, yy)
# plt.show()
# changchun_neimeng = ['S651', 'S485']
# ha_neimeng = ['S930', 'S1368', 'S1427', 'S956', 'S932', 'S978']
# ha_changchun = []
# for site in data_deliver.keys():
#     if site not in ha_neimeng:
#         ha_changchun.append(site)

# with open('order_neimeng_new.json', 'r', encoding='utf-8') as f:
#     order_neimeng_new = json.loads(f.read())
# with open('order_changchun_new.json', 'r', encoding='utf-8') as f:
#     order_changchun_new = json.loads(f.read())

# for order in orders_deliver:
#     if order['end'] in ha_neimeng:
#         order_neimeng_new.append(order)
#     if order['end'] in ha_changchun:
#         order_changchun_new.append(order)
#
# with open('order_neimeng_new2.json', 'w') as f:
#     json.dump(order_neimeng_new, f, ensure_ascii=False)
# with open('order_changchun_new2.json', 'w') as f:
#     json.dump(order_changchun_new, f, ensure_ascii=False)
