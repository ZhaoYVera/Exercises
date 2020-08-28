import json
from typing import List
from collections import defaultdict
import numpy as np
import math
import matplotlib.pyplot as plt
from Exercises.tsp_lkh.main import LKH
from Exercises.tsp_lkh.bailian.LP_zhuangmao import cats_in_cars, pin
from Exercises.tsp_lkh.bailian.node import Node
# from Exercises.tsp_lkh.bailian.LP_zhuangmao import pin


class Tree:
    def __init__(self, root: Node, rest_nodes: List[Node], time_distance_matrix):
        self.rest_nodes = rest_nodes
        self.root = root
        self.nodes = [root] + rest_nodes
        self.distance_matrix = time_distance_matrix['distance']
        self.time_distance_matrix = time_distance_matrix
        self.partition = None

    def create_init_tree(self):
        """
        create the initial tree by Dijkstra's algorithm.
        The tree need to be modified before partition.
        """
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
                if dist[v] > dist[adding_node_idx] + self.distance_matrix[adding_node.name][self.nodes[v].name]:
                    dist[v] = dist[adding_node_idx] + self.distance_matrix[adding_node.name][self.nodes[v].name]
                    self.nodes[v].parent = adding_node
                    rest[v] = dist[v]
        return self.nodes

    def create_init_mst(self):
        """
        create the initial tree as MST by Prim's algorithm.
        no additional operations are required before partition.
        """
        q = self.nodes.copy()
        self.root.key = 0
        while q:
            idx, u = min(enumerate(q), key=lambda x: x[1].key)
            del q[idx]
            for v in q:
                if self.distance_matrix[u.name][v.name] < v.key:
                    v.parent = u
                    v.key = self.distance_matrix[u.name][v.name]
        for node in self.rest_nodes:
            node.parent.children.append(node)
        return

    @staticmethod
    def get_branch(branch_root: Node):
        subtree_list = [branch_root]

        def get_children(node: Node):
            if node.children:
                subtree_list.extend(node.children)
                for child_node in node.children:
                    get_children(child_node)
        get_children(branch_root)
        return subtree_list

    def get_leaves(self):
        leaves = []
        for node in self.rest_nodes:
            if not node.children:
                leaves.append(node)
        return leaves

    def get_proper_td_matrix(self, branch, factor='distance'):
        """
        get proper cost matrix for LKH & calculating route cost.
        """
        vertices = [self.root] + branch
        n = len(vertices)
        mat = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                mat[i][j] = mat[j][i] = self.time_distance_matrix[factor][vertices[i].name][vertices[j].name]
        return mat

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
            length += self.distance_matrix[node.name][node.parent.name]
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

    def plot_tree(self):
        results = []

        def dfs_route(curr_route, sub_node: Node):
            if not sub_node.children:
                results.append(curr_route.copy())
                return
            for child in sub_node.children:
                dfs_route(curr_route + [child], child)

        dfs_route([self.root], self.root)
        for route in results:
            plt.plot([node.lng for node in route], [node.lat for node in route], '+-')
        plt.show()

    def plot_routes(self):
        lucky = 3
        partition = self.run() if self.partition is None else self.partition
        for part in partition:
            start_part = [self.root] + part
            xx = []
            yy = []
            route = LKH(self.get_proper_td_matrix(part), use_dual_ascent=False, use_alpha_cand=False).run()
            for idx in route.iter_vertices():
                xx.append(start_part[idx].lng)
                yy.append(start_part[idx].lat)
            xx.append(self.root.lng)
            yy.append(self.root.lat)
            plt.plot(xx, yy, '+-')
        plt.show()

    def grade(self, node: Node):
        min_dist = min(self.distance_matrix[node.name][other.name] for other in self.nodes if other != node)
        dist2parent = self.distance_matrix[node.name][node.parent.name]
        score = min_dist - dist2parent
        return score

    def get_ranking(self, nodes: List[Node], truck_size):
        ranking = []
        for node in nodes:
            branch_size = len(self.get_branch(node))
            sum_volume = self.sum_volume(node)
            sum_distance = self.length_branch(node) + self.distance_matrix[self.root.name][node.name]
            candidate_nodes = self.rest_nodes.copy()
            for sub_node in self.get_branch(node):
                candidate_nodes.remove(sub_node)
            if candidate_nodes:
                min_link2other = min(self.distance_matrix[node.name][other.name] for other in candidate_nodes)
            else:
                min_link2other = self.distance_matrix[node.name][self.root.name]
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
        linking_node_idx = min(enumerate(self.distance_matrix[cutting_node.name][other.name]
                                         for other in linking_node_candidate),
                               key=lambda x: x[1])[0]
        self.cut_relink(cutting_node, linking_node_candidate[linking_node_idx])
        return

    def merge(self, final_branch_num=None, truck_size=12):
        if final_branch_num is None:
            final_branch_num = math.ceil(sum(node.volume for node in self.rest_nodes)/truck_size)
        layer1_num = len(self.get_layer_nodes(1))
        while layer1_num > final_branch_num:
            cutting_node = self.get_layer_nodes(1)[0]
            self.cut_branch(cutting_node)
            layer1_num = len(self.get_layer_nodes(1))
        return

    def merge_leaves(self):
        leaves = self.get_leaves()
        leaves.sort(key=self.grade)
        # mean_length = sum(self.distance_matrix[leaf.name][leaf.parent.name] for leaf in leaves)/len(leaves)
        for leaf in leaves:
            # if self.distance_matrix[leaf.name][leaf.parent.name] > mean_length:
            self.cut_branch(leaf)
        return

    def divide(self, truck_size=12, preprocess='dij'):
        if preprocess == 'dij':
            self.create_init_tree()
            self.merge()
            self.merge_leaves()
        elif preprocess == 'mst':
            self.create_init_mst()
        else:
            raise ValueError("preprocess choices: 'dij', 'mst'.")
        division_branch_volume = []
        rest = self.rest_nodes.copy()

        def cut4overload(waiting_root):
            scores = []
            total_volume = self.sum_volume(waiting_root)
            for node in branch:
                if node != waiting_root:
                    sum_volume = self.sum_volume(node)
                    score1 = 1000 / (truck_size + sum_volume - total_volume) \
                        if (truck_size + sum_volume - total_volume) != 0 else np.inf
                    min_link2other = min(self.distance_matrix[node.name][other.name] for other in rest) if rest \
                        else self.distance_matrix[self.root.name][node.name]
                    score2 = math.exp(min_link2other / 10000)
                    score = score1 - score2
                    scores.append((score1, score2, score, node))
            scores.sort(reverse=True)
            if scores[0][0] < 0:  # 只剪一枝不够
                scores.sort(key=lambda x: x[1])
                cut_node = scores[0][3]
                if rest:
                    linking_node_idx = min(enumerate(self.distance_matrix[cut_node.name][other.name]
                                                     for other in rest),
                                           key=lambda x: x[1])[0]
                    self.cut_relink(cut_node, rest[linking_node_idx])
                    for nnode in self.get_branch(cut_node):
                        rest.append(nnode)
                        branch.remove(nnode)
                else:
                    self.cut_relink(cut_node, self.root)
                    for nnode in self.get_branch(cut_node):
                        rest.append(nnode)
                        branch.remove(nnode)
                if sum(mnode.volume for mnode in branch) > truck_size:
                    return cut4overload(waiting_root)
            else:
                scores.sort(reverse=True)
                cut_node = scores[0][3]
                if not rest:
                    self.cut_relink(cut_node, self.root)
                else:
                    linking_node_idx = min(enumerate(self.distance_matrix[cut_node.name][other.name]
                                                     for other in rest),
                                           key=lambda x: x[1])[0]
                    self.cut_relink(cut_node, rest[linking_node_idx])
                for node in self.get_branch(cut_node):
                    branch.remove(node)
                    rest.append(node)

        while rest:
            branch_root = self.get_ranking(rest, truck_size)
            branch = self.get_branch(branch_root)
            for node in branch:
                rest.remove(node)
            if sum(node.volume for node in branch) > truck_size:  # 超载，进行评分、剪枝
                cut4overload(branch_root)
            division_branch_volume.append((branch.copy(), sum(node.volume for node in branch)))
            branch_root.parent.children.remove(branch_root)

        print("DIVIDE RESULT: ")
        for branch in division_branch_volume:
            print(f"branch_size = {len(branch[0])}, total_volume = {branch[1]}")
        print(f"number of division: {len(division_branch_volume)}")

        return division_branch_volume

    def merge_round(self, division_branch_volume, truck_size):
        lucky = 3

        def earning_combine(branch1, branch2, factor='distance'):
            mat1 = self.get_proper_td_matrix(branch1, factor)
            mat2 = self.get_proper_td_matrix(branch2, factor)
            mat_total = self.get_proper_td_matrix(branch1+branch2, factor)
            tour1 = LKH(mat1, use_dual_ascent=False, use_alpha_cand=False)
            init_tour1 = tour1.create_initial_tour(sd=lucky)
            cost1 = tour1.run(tour0=init_tour1).route_cost(mat1)
            tour2 = LKH(mat2, use_dual_ascent=False, use_alpha_cand=False)
            init_tour2 = tour2.create_initial_tour(sd=lucky)
            cost2 = tour2.run(tour0=init_tour2).route_cost(mat2)
            tour_total = LKH(mat_total, use_dual_ascent=False, use_alpha_cand=False)
            init_tour_total = tour_total.create_initial_tour(sd=lucky)
            cost_total = tour_total.run(tour0=init_tour_total).route_cost(mat_total)
            if factor == 'time':
                cost1 += len(branch1) * 900 + 1800
                cost2 += len(branch2) * 900 + 1800
                cost_total += len(branch1 + branch2) * 900 + 1800
            earning = cost_total - cost1 - cost2
            return earning
        ranking = []
        for i in range(len(division_branch_volume)):
            for j in range(i+1, len(division_branch_volume)):
                round_volume1 = division_branch_volume[i]
                round_volume2 = division_branch_volume[j]
                if round_volume1[1] + round_volume2[1] > truck_size:
                    continue
                earning = earning_combine(round_volume1[0], round_volume2[0])
                if earning > 0:
                    continue
                ranking.append((earning, round_volume1, round_volume2))
        ranking.sort(key=lambda x: x[0])
        if ranking:
            round_volume1 = ranking[0][1]
            round_volume2 = ranking[0][2]
            division_branch_volume.remove(round_volume1)
            division_branch_volume.remove(round_volume2)
            new_round = (round_volume1[0] + round_volume2[0], round_volume1[1] + round_volume2[1])
            division_branch_volume.append(new_round)
            self.merge_round(division_branch_volume, truck_size)
        else:
            return division_branch_volume

    def merge_round_yuqin(self, truck_size=12):
        division_branch_volume = self.divide()
        min_volume = min(item[1] for item in division_branch_volume)
        self.partition = []
        second_time = []
        for branch, volume in division_branch_volume:
            if volume > truck_size - min_volume:
                self.partition.append(branch)
            else:
                second_time.extend(branch)
        if second_time:
            for node in second_time:
                node.parent = None
                node.children = []
                node.layer = 0
            self.root.children = []
            second_tree = Tree(self.root, second_time, self.time_distance_matrix)
            self.partition.extend(second_tree.run())
        return self.partition

    def merge_round_yuqin2(self, truck_size=12):
        division_branch_volume = self.divide()
        min_volume = min(item[1] for item in division_branch_volume)
        self.partition = []
        second_time = []
        for branch, volume in division_branch_volume:
            if volume > truck_size - min_volume:
                self.partition.append(branch)
            else:
                second_time.append(Node(name=branch[0].name, volume=sum(node.volume for node in branch), branch_nodes=branch))
        if second_time:
            self.root.children = []
            second_tree = Tree(self.root, second_time, self.time_distance_matrix)
            result = second_tree.divide()
            for branch, volume in result:
                part = []
                for node in branch:
                    part.extend(node.branch_nodes)
                self.partition.append(part)
        return self.partition

    def merge_lp(self, truck_size=12):
        division_branch_volume = self.divide()
        branches = []
        for branch, _ in division_branch_volume:
            branches.append(branch)
        self.partition = pin(truck_size, branches, self.distance_matrix)
        return self.partition

    def run(self, truck_size=12, preprocess='dij'):
        division_branch_volume = self.divide(truck_size, preprocess)
        # self.merge_round(division_branch_volume, truck_size)
        self.merge_round_yuqin2()
        # for branch, volume in division_branch_volume:
        #     print(f"branch_size = {len(branch)}, total_volume = {volume}")
        # print(f"number of rounds: {len(division_branch_volume)}")

        partition = [branch for branch, volume in division_branch_volume]
        self.partition = partition
        return partition

    def total_cost(self, time4pickup=1800, time4deliver=900, truck_size=12, preprocess='dij'):
        lucky = 3
        partition = self.run(truck_size, preprocess) if self.partition is None else self.partition
        total_cost = 0
        total_time_cost = 0
        result = {}
        for i in range(len(partition)):
            branch = partition[i]
            dist_mat = self.get_proper_td_matrix(branch)
            time_mat = self.get_proper_td_matrix(branch, factor='time')
            tour = LKH(dist_mat, use_alpha_cand=False, use_dual_ascent=False)
            init_tour = tour.create_initial_tour(sd=lucky)
            route = tour.run(tour0=init_tour)
            dist_cost = route.route_cost(dist_mat)
            time_cost = route.route_cost(time_mat) + len(branch) * time4deliver + time4pickup
            total_cost += dist_cost
            total_time_cost += time_cost
            result[i] = {'branch': branch, 'total_volume': sum(node.volume for node in branch),
                         'distance': dist_cost, 'time': time_cost}

            print(f"branch_size = {len(branch)}, total_volume = {result[i]['total_volume']}, "
                  f"distance = {dist_cost}, time = {time_cost}, branch: {branch}")

        print(f"total rounds: {len(partition)}")
        print(f"total distance cost: {total_cost}, total time cost: {total_time_cost}")
        return result

    def get_truck_num(self, working_time):
        result = self.total_cost()
        time_list = []
        for item in result.values():
            time_list.append(int(item['time']))
        truck_num = (sum(time_list) // working_time) + 3
        last = 0
        while last == 0:
            truck_num -= 1
            solution, last = cats_in_cars([truck_num, 0], [working_time, 0], time_list)

        return truck_num


if __name__ == '__main__':
    with open('orders.json', 'r', encoding='utf-8') as f:
        orders = json.loads(f.read())
    orders1day = orders['2020-06-01']
    with open('lnglat_district.json', 'r', encoding='utf-8') as f:
        lnglat_dict = json.loads(f.read())
    Nodes = []
    for order in orders1day:
        if order['id'] not in ['盛石二店', '北京配送中心', '大连配送中心', '紫琅店', '全用店', '曹库残次']:  # \
                # + ['广同店', '昆明店', '双喜店', '广灵店', '霍定店', '景星店', '临青二店', '黄兴店', '延吉一店', '佳龙店', '广一店', '岭南店'] \
                # + ['延长一店', '延长店', '大华店', '延荣店', '京江店', '和宁店', '芷通店', '广东店', '西江店', '南仓店']:
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
                   rest_nodes=Nodes, time_distance_matrix=td_dict)
    # my_tree.create_init_tree()
    # my_tree.merge(5)
    # my_tree.merge_leaves()

    # my_tree.create_init_mst()
    # my_tree.plot_tree()
    # my_tree.divide()
    # my_tree.run()
    # my_tree.merge_round_yuqin2()
    # my_tree.plot_routes()
    # my_tree.merge_lp()
    # my_tree.total_cost()
    # print(f"number of trucks: {my_tree.get_truck_num(64800)}")

    # my_tree.plot_tree()
