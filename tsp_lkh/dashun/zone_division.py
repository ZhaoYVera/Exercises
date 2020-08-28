from typing import List
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt


class Site:
    def __init__(self, site_id, volume):
        self.site_id = site_id
        self.volume = volume
        self.parent = None
        self.children = []
        self.layer = 0

    def __repr__(self):
        return self.site_id


class PickupSite(Site):
    def __init__(self, site_id, volume):
        super().__init__(site_id, volume)
        self.num_cars = 1


class OrderDivision:
    def __init__(self, orders: List[Site], pickup_sites: List[Site], distance_matrix):
        self.orders = orders
        self.pickup_sites = pickup_sites
        self.distance_matrix = distance_matrix

    def create_mst(self):
        """
        create initial trees by Prim's algorithm
        """
        pass

    def create_init_tree(self):
        """
        create initial trees by Dijkstra's algorithm
        """
        all_sites = self.pickup_sites + self.orders
        dist = {}
        num_pickup = len(self.pickup_sites)
        for i in range(num_pickup):
            dist[i] = 0
        for i in range(len(self.orders)):
            dist[i + num_pickup] = np.inf
        rest = dist.copy()
        while rest:
            adding_site_idx = min(rest, key=lambda x: (rest[x], min(self.distance_matrix[x.site_id][other.site_id]
                                                                    for other in rest.keys() if other != x)))
            adding_site = all_sites[adding_site_idx]
            if adding_site.parent is not None:
                adding_site.parent.children.append(adding_site)
                adding_site.layer = adding_site.parent.layer + 1
            del rest[adding_site_idx]
            for v in rest.keys():
                if dist[v] > dist[adding_site_idx] + self.distance_matrix[adding_site.site_id][all_sites[v].site_id]:
                    dist[v] = dist[adding_site_idx] + self.distance_matrix[adding_site.site_id][all_sites[v].site_id]
                    all_sites[v].parent = adding_site
                    rest[v] = dist[v]
        return [self.get_branch(root) for root in self.pickup_sites]

    def plot_tree(self):
        results = []

        def dfs_route(curr_route, next_site: Site):
            if not next_site.children:
                results.append(curr_route.copy())
                return
            for child in next_site.children:
                dfs_route(curr_route + [child], child)

        for root in self.pickup_sites:
            dfs_route([root], root)
        for route in results:
            plt.plot([node.lng for node in route], [node.lat for node in route], '+-')
        plt.show()

    @staticmethod
    def get_branch(branch_root: Site):
        subtree_list = [branch_root]

        def get_children(site: Site):
            if site.children:
                subtree_list.extend(site.children)
                for child_node in site.children:
                    get_children(child_node)

        get_children(branch_root)
        return subtree_list

    def sum_volume(self, branch_root):
        branch = self.get_branch(branch_root)
        return sum(site.volume for site in branch)
