import json
from typing import Sequence, List
from collections import defaultdict
import numpy as np
import math
import matplotlib.pyplot as plt
from Exercises.tsp_lkh.main import LKH
from grouping import Grouping
# from Exercises.tsp_lkh.bailian.dijkstra_tree import create_init_tree


class Node:
    def __init__(self, name, volume=0, weight=0, time_window=None, lng=None, lat=None, district=None):
        self.name = name
        self.volume = volume
        self.weight = weight
        self.time_window = time_window
        self.layer = 0
        self.parent = None
        self.children = []
        self.lng = lng
        self.lat = lat
        self.district = district

    def __repr__(self):
        return self.name


class Tree:
    def __init__(self, root: Node, rest_nodes: List[Node], time_distance_matrix, time_matrix):
        self.rest_nodes = rest_nodes
        self.root = root
        self.nodes = [root] + rest_nodes
        self.td_matrix = time_distance_matrix
        self.time_matrix = time_matrix
        self.create_init_tree()

    def create_init_tree(self):
        dist = defaultdict(float)
        dist[0] = 0
        for i in range(len(self.rest_nodes)):
            dist[i + 1] = np.inf
        rest = dist.copy()
        while rest:
            adding_node_idx = min(rest, key=lambda x: rest[x])
            adding_node = self.nodes[adding_node_idx]
            if adding_node.parent is not None:
                adding_node.parent.children.append(adding_node)
                adding_node.layer = adding_node.parent.layer + 1
            del rest[adding_node_idx]
            for v in rest.keys():
                if dist[v] > dist[adding_node_idx] + self.td_matrix[adding_node.name][self.nodes[v].name]:
                    dist[v] = dist[adding_node_idx] + self.td_matrix[adding_node.name][self.nodes[v].name]
                    self.nodes[v].parent = adding_node
                    rest[v] = dist[v]
        return self.nodes

    @staticmethod
    def get_branch(subtree_root: Node):
        subtree_list = [subtree_root]

        def get_children(node: Node):
            if node.children:
                subtree_list.extend(node.children)
                for child_node in node.children:
                    get_children(child_node)
        get_children(subtree_root)
        return subtree_list

    def get_leaves(self):
        leaves = []
        for node in self.rest_nodes:
            if not node.children:
                leaves.append(node)
        return leaves

    def sum_volume(self, branch_root):
        branch = self.get_branch(branch_root)
        return sum(node.volume for node in branch)

    def sum_weight(self, branch_root):
        branch = self.get_branch(branch_root)
        return sum(node.weight for node in branch)

    def length_branch(self, branch_root):
        branch = self.get_branch(branch_root)
        length = 0
        for node in branch[1:]:
            length += self.td_matrix[node.name][node.parent.name]
        return length

    @staticmethod
    def cut_relink(branch_root: Node, new_parent_node: Node):
        prev_parent = branch_root.parent
        prev_parent.children.remove(branch_root)
        branch_root.parent = new_parent_node
        branch_root.layer = new_parent_node.layer + 1
        new_parent_node.children.append(branch_root)

        def change_layer(node: Node):
            if node.children:
                for child in node.children:
                    child.layer = node.layer + 1
                    change_layer(child)
            return
        change_layer(branch_root)
        return

    def iter_root2leaf(self):
        results = []

        def dfs_route(curr_route, sub_node: Node):
            if not sub_node.children:
                results.append(curr_route.copy())
                return
            for child in sub_node.children:
                dfs_route(curr_route+[child], child)

        dfs_route([self.root], self.root)
        return results

    def plot_tree(self):
        for route in self.iter_root2leaf():
            plt.plot([node.lng for node in route], [node.lat for node in route], '+-')
        plt.show()

    def grade(self, node: Node):
        min_dist = min(self.td_matrix[node.name][other.name] for other in self.nodes if other != node)
        dist2parent = self.td_matrix[node.name][node.parent.name]
        score = min_dist - dist2parent
        return score

    def get_ranking(self, nodes: List[Node], truck_size):
        ranking = []
        for node in nodes:
            branch_size = len(self.get_branch(node))
            sum_volume = self.sum_volume(node)
            sum_distance = self.length_branch(node) + self.td_matrix[self.root.name][node.name]
            candidate_nodes = self.rest_nodes.copy()
            for sub_node in self.get_branch(node):
                candidate_nodes.remove(sub_node)
            min_link2other = min(self.td_matrix[node.name][other.name] for other in candidate_nodes)
            score = 1000/abs(truck_size - sum_volume)
            score += math.exp(sum_distance/(branch_size*10000))
            score += math.exp(min_link2other/1000)
            ranking.append((score, node))
            # print(f"name = {node.name}, branch_size = {branch_size}, sum_volume = {sum_volume}, "
            #       f"sum_distance = {sum_distance}, min_link2other = {min_link2other}, score = {score}")
        ranking.sort(reverse=True)
        return ranking[0][1]

    def get_layer_nodes(self, layer_num):
        if layer_num == 0:
            return [self.root]
        layer_nodes = []
        for node in self.rest_nodes:
            if node.layer == layer_num:
                layer_nodes.append(node)
        layer_nodes.sort(key=lambda x: (len(self.get_branch(x)), self.length_branch(x), self.grade(x)))
        return layer_nodes

    def cut_branch(self, cutting_node: Node):
        linking_node_candidate = self.rest_nodes.copy()
        for node in self.get_branch(cutting_node):
            linking_node_candidate.remove(node)
        linking_node_idx = min(enumerate(self.td_matrix[cutting_node.name][other.name]
                                         for other in linking_node_candidate),
                               key=lambda x: x[1])[0]
        self.cut_relink(cutting_node, linking_node_candidate[linking_node_idx])
        return

    def merge(self, final_branch_num=6):
        layer1_num = len(self.get_layer_nodes(1))
        while layer1_num > final_branch_num:
            cutting_node = self.get_layer_nodes(1)[0]
            self.cut_branch(cutting_node)
            layer1_num = len(self.get_layer_nodes(1))
        return

    def merge_leaves(self):
        leaves = self.get_leaves()
        leaves.sort(key=self.grade)
        # mean_length = sum(self.td_matrix[leaf.name][leaf.parent.name] for leaf in leaves)/len(leaves)
        for leaf in leaves:
            # if self.td_matrix[leaf.name][leaf.parent.name] > mean_length:
            self.cut_branch(leaf)
        return

    def divide(self, truck_size=12):
        division = []
        rest = self.rest_nodes.copy()
        while rest:
            branch_root = self.get_ranking(rest, truck_size)
            branch = self.get_branch(branch_root)
            # branch_root.parent.children.remove(branch_root)
            for node in branch:
                rest.remove(node)
            if sum(node.volume for node in branch) > truck_size:
                scores = []
                for node in branch:
                    if node != branch_root:
                        # branch_size = len(self.get_branch(node))
                        sum_volume = self.sum_volume(node)
                        # sum_distance = self.length_branch(node) + self.td_matrix[self.root.name][node.name]
                        # for sub_node in self.get_branch(node):
                        #     candidate_nodes.remove(sub_node)
                        min_link2other = min(self.td_matrix[node.name][other.name] for other in rest) if not rest \
                            else self.td_matrix[self.root.name][node.name]
                        score = 1000 / (truck_size + sum_volume - self.sum_volume(branch_root))
                        # score += math.exp(sum_distance / (branch_size * 10000))
                        score -= math.exp(min_link2other / 10000)
                        scores.append((score, node))
                scores.sort(reverse=True)
                cut_node = scores[0][1]
                if not rest:
                    self.cut_relink(cut_node, self.root)
                else:
                    linking_node_idx = min(enumerate(self.td_matrix[cut_node.name][other.name]
                                                     for other in rest),
                                           key=lambda x: x[1])[0]
                    self.cut_relink(cut_node, rest[linking_node_idx])
                for node in self.get_branch(cut_node):
                    branch.remove(node)
                    rest.append(node)
            division.append((branch.copy(), sum(node.volume for node in branch)))
            branch_root.parent.children.remove(branch_root)
        for branch in division:
            print(f"branch_size = {len(branch[0])}, total_volume = {branch[1]}")
        print(len(division))
        return division

    def merge_round(self, division, truck_size):

        def earning_combine(branch1, branch2):

            def get_proper_mat(branch):
                start_branch = [self.root] + branch
                n = len(start_branch)
                mat = np.zeros((n, n))
                for i in range(n):
                    for j in range(i+1, n):
                        mat[i][j] = mat[j][i] = self.td_matrix[start_branch[i].name][start_branch[j].name]
                return mat
            mat1 = get_proper_mat(branch1)
            mat2 = get_proper_mat(branch2)
            mat_total = get_proper_mat(branch1+branch2)
            cost1 = LKH(mat1, use_dual_ascent=False, use_alpha_cand=False).run().route_cost(mat1)
            cost2 = LKH(mat2, use_dual_ascent=False, use_alpha_cand=False).run().route_cost(mat2)
            cost_total = LKH(mat_total, use_dual_ascent=False, use_alpha_cand=False).run().route_cost(mat_total)

            earning = cost_total - cost1 - cost2
            return earning
        ranking = []
        for branch1 in division:
            for branch2 in division:
                if branch1 != branch2:
                    if branch1[1] + branch2[1] > truck_size:
                        continue
                    earning = earning_combine(branch1[0], branch2[0])
                    if earning < 0:
                        ranking.append((earning, branch1, branch2))
        ranking.sort(key=lambda x: x[0])
        if ranking:
            branch1 = ranking[0][1]
            branch2 = ranking[0][2]
            division.remove(branch1)
            division.remove(branch2)
            new_branch = (branch1[0] + branch2[0], branch1[1] + branch2[1])
            division.append(new_branch)
            self.merge_round(division, truck_size)
        else:
            return division

    def run(self, truck_size=12):
        division = self.divide(truck_size)
        self.merge_round(division, truck_size)
        for branch in division:
            print(f"branch_size = {len(branch[0])}, total_volume = {branch[1]}")
        print(len(division))
        return division

    def total_cost(self):
        division = self.run()
        total_cost = 0
        total_time_cost = 0

        def get_proper_mat(branch):
            start_branch = [self.root] + branch
            n = len(start_branch)
            mat = np.zeros((n, n))
            for i in range(n):
                for j in range(i + 1, n):
                    mat[i][j] = mat[j][i] = self.td_matrix[start_branch[i].name][start_branch[j].name]
            return mat

        def get_proper_time_mat(branch):
            start_branch = [self.root] + branch
            n = len(start_branch)
            mat = np.zeros((n, n))
            for i in range(n):
                for j in range(i + 1, n):
                    mat[i][j] = mat[j][i] = self.time_matrix[start_branch[i].name][start_branch[j].name]
            return mat
        result = {}
        for i in range(len(division)):
            branch = division[i]
            dist_mat = get_proper_mat(branch[0])
            time_mat = get_proper_time_mat(branch[0])
            route = LKH(dist_mat, use_alpha_cand=False, use_dual_ascent=False).run()
            dist_cost = route.route_cost(dist_mat)
            time_cost = route.route_cost(time_mat) + len(branch) * 900 + 1800
            total_cost += dist_cost
            total_time_cost += time_cost
            result[i] = {'branch': branch[0], 'total_volume': branch[1], 'distance': dist_cost, 'time': time_cost}

            print(f"branch_size = {len(branch[0])}, total_volume = {branch[1]}, distance = {dist_cost}, time = {time_cost}")
        print(len(division))
        print(f"total distance cost: {total_cost}, total time cost: {total_time_cost}")
        return result

    def get_truck_num(self, working_time):
        result = self.total_cost()
        times = []
        for item in result.values():
            times.append(item['time'])
        truck_num = math.ceil(sum(times)/working_time)
        times.sort(reverse=True)

        def grouping(time_list, num):
            group = []
            for i in range(num):
                group.append([0])
            for tt in time_list:
                i = 0
                while True:
                    if sum(group[i] + [tt]) < working_time:
                        group[i].append(tt)
                        break
                    i += 1
                    if i == num:
                        return None
            return num
        while True:
            if grouping(times, truck_num) is None:
                truck_num += 1
            break
        return truck_num


if __name__ == '__main__':
    with open('orders.json', 'r', encoding='utf-8') as f:
        orders = json.loads(f.read())
    orders1day = orders['2020-06-02']
    with open('lnglat_district.json', 'r', encoding='utf-8') as f:
        lnglat_dict = json.loads(f.read())
    Nodes = []
    for order in orders1day:
        if order['id'] != '盛石二店':
            lnglat = lnglat_dict[order['id']][0]
            lng, lat = lnglat.split(',')

            Nodes.append(Node(name=order['id'], volume=order['volume'],
                              weight=order['weight'], time_window=order['time_window'],
                              lng=float(lng), lat=float(lat)))
    with open('time_distance.json', 'r', encoding='utf-8') as f:
        td_list = json.loads(f.read())
    td_dict = {'time': defaultdict(dict), 'distance': defaultdict(dict)}
    for info in td_list:
        start = info[0]
        end = info[1]
        distance = info[2]
        time = info[3]
        td_dict['time'][start][end] = time
        td_dict['distance'][start][end] = distance

    root_lnglat = lnglat_dict['起点'][0]
    lng, lat = root_lnglat.split(',')
    my_tree = Tree(root=Node(name='起点', lng=float(lng), lat=float(lat)),
                   rest_nodes=Nodes, time_distance_matrix=td_dict['distance'], time_matrix=td_dict['time'])
    my_tree.merge(6)
    my_tree.merge_leaves()
    print(f"number of trucks: {my_tree.get_truck_num(46800)}")

    # my_tree.plot_tree()

    # node1 = Node(name='a1')
    # node2 = Node(name='a2')
    # node3 = Node(name='a3')
    # node4 = Node(name='a4')
    # node5 = Node(name='a5')
    # node1.layer = 0
    # node2.layer = 1
    # node3.layer = 1
    # node4.layer = 2
    # node5.layer = 2
    # node2.parent = node1
    # node3.parent = node1
    # node4.parent = node2
    # node5.parent = node2
    # node1.children = [node2, node3]
    # node2.children = [node4, node5]
    # my_tree = Tree([node1, node2, node3, node4, node5])
    # my_tree.get_branch(node1)
