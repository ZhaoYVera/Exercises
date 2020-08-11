import json
import collections
import numpy as np
from tsp_lkh.main import LKH
import matplotlib.pyplot as plt


class BestDeliverRoute:
    def __init__(self, orders: list, time_distance_matrix):
        self.orders = orders.copy()
        self.total_quantity = sum(order['volume'] for order in self.orders)
        self.sites = set(order['end'] for order in self.orders)
        self.time_distance_mat = time_distance_matrix
        self.route = None

    def get_time_distance_matrix(self, sites: list):
        num_sites = len(sites)
        my_time_mat = np.zeros((num_sites, num_sites))
        my_distance_mat = np.zeros((num_sites, num_sites))
        for i in range(num_sites):
            for j in range(i+1, num_sites):
                my_time_mat[i, j] = my_time_mat[j, i] = self.time_distance_mat[sites[i]][sites[j]]['time']
                my_distance_mat[i, j] = my_distance_mat[j, i] = self.time_distance_mat[sites[i]][sites[j]]['distance']
            # my_time_mat[i, i] = my_distance_mat[i, i] = np.inf
        return {'time': my_time_mat, 'distance': my_distance_mat}

    def get_best_route(self, start_site=None, end_site=None, factor='distance'):
        sites_set = self.sites.copy()
        if start_site is not None:
            sites_set.add(start_site)
        if end_site is not None:
            sites_set.add(end_site)
        sites_name = list(sites_set)
        num_sites = len(sites_name)
        mat = self.get_time_distance_matrix(sites_name)[factor]
        if start_site is not None:
            start_idx = sites_name.index(start_site)
            if end_site is not None:
                end_idx = sites_name.index(end_site)
            else:
                end_idx = mat[start_idx].argmax()
        else:
            if end_site is not None:
                end_idx = sites_name.index(end_site)
                start_idx = mat[end_idx].argmax()
            else:
                start_idx = end_idx = 0
        mat[start_idx, end_idx] = mat[end_idx, start_idx] = 1
        solver = LKH(mat)
        tsp_result = solver.run()
        tsp_idx = list(tsp_result.iter_vertices())
        s_idx = tsp_idx.index(start_idx)
        e_idx = tsp_idx.index(end_idx)
        if s_idx == e_idx:
            if start_site is None:
                route_idx = tsp_idx
            else:
                route_idx = tsp_idx[s_idx:]+tsp_idx[:s_idx]
        elif (s_idx+1) % num_sites == e_idx:
            route_idx = tsp_idx[s_idx::-1] + tsp_idx[:s_idx:-1]
        elif (e_idx+1) % num_sites == s_idx:
            route_idx = tsp_idx[s_idx:] + tsp_idx[:s_idx]
        else:
            raise ValueError('Not get route starting and ending at specified sites.')
        route = self.route = [sites_name[i] for i in route_idx]
        return route

    def iter_best_route_lnglat(self, lnglat_dict, start_site=None, end_site=None, factor='distance'):
        route = self.get_best_route(start_site, end_site, factor) if self.route is None else self.route
        for site in route:
            lnglat = lnglat_dict[site]
            yield lnglat

    def plot_lnglat(self, lnglat_dict, start_site=None, end_site=None, factor='distance'):
        lngs = []
        lats = []
        for lnglat in self.iter_best_route_lnglat(lnglat_dict, start_site, end_site, factor):
            lng_lat = lnglat.split(',')
            lngs.append(lng_lat[0])
            lats.append(lng_lat[1])
        plt.plot(lngs, lats)
        plt.show()

    def iter_sorted_orders(self, start_site=None, end_site=None, factor='distance'):
        route = self.get_best_route(start_site, end_site, factor) if self.route is None else self.route
        for site in route:
            for order in self.orders:
                if order['end'] == site:
                    yield order

    def iter_deliver_areas(self, start_site=None, end_site=None, factor='distance'):
        route = self.get_best_route(start_site, end_site, factor) if self.route is None else self.route
        curr = route[0]
        if curr not in self.sites:
            yield curr
        for site in route:
            for order in self.orders:
                if order['end'] == site and order['deliver_area'] != curr:
                    curr = order['deliver_area']
                    yield curr
        last = route[-1]
        if last not in self.sites:
            yield last

    def route_cost(self, start_site=None, end_site=None, factor='distance', circle=True):
        route = self.get_best_route(start_site, end_site, factor) if self.route is None else self.route
        cost = 0
        n = len(route)
        for i in range(1, n):
            cost += self.time_distance_mat[route[i-1]][route[i]][factor]
        if circle:
            cost += self.time_distance_mat[route[-1]][route[0]][factor]
        return cost


if __name__ == '__main__':

    # -------data for distance and time--------------------------------------------------------------

    with open('distance_changchun_new.json', 'r', encoding='utf-8') as f:
        distance_list = json.loads(f.read())
    my_time_distance_matrix = {}
    # for info_list in distance_list:
    for info in distance_list:
        start = info[0]
        end = info[1]
        distance = info[2]
        time = info[3]
        if start in my_time_distance_matrix:
            my_time_distance_matrix[start][end] = {'distance': distance, 'time': time}
        else:
            my_time_distance_matrix[start] = {end: {'distance': distance, 'time': time}}

    # --------data for orders------------------------------------------------------------------------

    with open('order_changchun_new(1).json', 'r', encoding='utf-8') as f:
        orders_deliver = json.loads(f.read())

    # data_deliver = collections.defaultdict(int)
    # for order in orders:
    #     data_deliver[order['end']] += order['volume']

    # --------data for lnglat------------------------------------------------------------------------

    with open('lnglat_hub.json', 'r', encoding='utf-8') as f:
        lnglat_hub = json.loads(f.read())
    with open('lnglat_normal.json', 'r', encoding='utf-8') as f:
        lnglat_normal = json.loads(f.read())
    lnglat_normal.update(lnglat_hub)

    test_changchun_new = BestDeliverRoute(orders_deliver, my_time_distance_matrix)
    for area in test_changchun_new.iter_deliver_areas(start_site='吉林长春', end_site='吉林长春'):
        print(area)
    for item in test_changchun_new.iter_best_route_lnglat(lnglat_normal):
        print('[', item, '],')
