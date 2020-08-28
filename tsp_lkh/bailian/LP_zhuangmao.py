import pulp
import numpy as np
from Exercises.tsp_lkh.bailian.node import Node
from Exercises.tsp_lkh.main import LKH
from typing import List
from collections import defaultdict
import math


def cats_in_cars(nums: list, cars: list, cats: list, alpha=1):
    """
    nums: nums[0] and nums[1] are the given number of cars,
    cars: cars[0] and cars[1] are the corresponding volume of cars,
    cats: this list are the volume of cats.
    alpha: (0, 1), Balance between full big cars and small tails.
    rtype: solution, which car to choose for each cat
    """
    n = len(cats)
    m = sum(nums)
    if cars[1] > cars[0]:
        cars = reversed(cars)
        nums = reversed(nums)
    b = [cars[0] for ele in range(nums[0])] + [cars[1] for ele in range(nums[1])]
    cat_in_car = [(i, j) for i in range(m) for j in range(n)]
    prob = pulp.LpProblem("CatCars", pulp.LpMaximize)
    x = pulp.LpVariable.dicts("delta(car,cat)", cat_in_car, cat=pulp.LpBinary)
    if nums[1] != 0:  # 尽量少装最后一车
        prob += sum([cats[j] * (alpha * sum([x[(i, j)] for i in range(nums[0])]) - x[(m - 1, j)]) for j in range(n)])
    else:
        prob += sum([cats[j] * (sum([x[(i, j)] for i in range(nums[0])]) - x[(m - 1, j)]) for j in range(n)])
    for j in range(n):
        prob += sum([x[(i, j)] for i in range(m)]) == 1, "One" + str(j)
    for i in range(m):
        prob += sum([x[(i, j)] * cats[j] for j in range(n)]) <= b[i], "Volume" + str(i)
    prob.solve()
    xx = np.zeros((m, n), dtype=float)
    for i in range(m):
        for j in range(n):
            xx[i][j] = int(x[(i, j)].varValue) * cats[j]
    res2 = [cars[0] - sum([cats[j] * x[(i, j)].varValue for j in range(n)]) for i in range(nums[0])]
    last = sum([cats[j] * x[(m - 1, j)].varValue for j in range(n)])
    res1 = b[-1] - last
    # if last != 0:
    if True:
        print("Status:", pulp.LpStatus[prob.status])
        print(f"Solution (car, cat): \n{xx}")
        print(f"The residual for the last car is {res1},\n"
              f"and the residual for the big cars are {res2}.")
    solution = [i for j in range(n) for i in range(m) if x[(i, j)].varValue == 1]
    return solution, last


def pin(car_size: float, cats: List[List[Node]], distance_matrix):
    """
    nums: nums[0] and nums[1] are the given number of cars,
    cars: cars[0] and cars[1] are the corresponding volume of cars,
    cats: this list are the volume of cats.
    alpha: (0, 1), Balance between full big cars and small tails.
    rtype: solution, which car to choose for each cat
    """
    n = len(cats)
    total_volume = 0
    for item in cats:
        total_volume += sum(node.volume for node in item)
    k = math.ceil(total_volume/car_size)
    cat_in_car = [(i, j) for i in range(k) for j in range(n)]
    prob = pulp.LpProblem("CatCars", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("delta(car,cat)", cat_in_car, cat=pulp.LpBinary)

    # 总路程最短
    def cost4round(nodes: List[Node]):
        if not nodes:
            return 0
        #  get proper distance matrix
        root_nodes = [Node(name='起点')] + nodes
        m = len(root_nodes)
        mat = np.zeros((m, m))
        for i in range(m):
            for j in range(i+1, m):
                mat[i, j] = mat[j, i] = distance_matrix[root_nodes[i].name][root_nodes[j].name]
        # calculate route cost by LKH
        lucky = 3
        rr = LKH(mat)
        rr_tour0 = rr.create_initial_tour(sd=lucky)
        cost = rr.run(rr_tour0).route_cost(mat)
        return cost

    def get_nodes(ll: list):
        nodes = []
        for idx in range(len(ll)):
            if ll[idx] == 1:
                nodes.extend(cats[idx])
        return nodes

    prob += sum([cost4round(get_nodes([x[(i, j)] for j in range(n)])) for i in range(k)])
    # 约束条件
    for j in range(n):
        prob += sum([x[(i, j)] for i in range(k)]) == 1, "One" + str(j)
    for i in range(k):
        prob += sum([x[(i, j)] * sum(node.volume for node in cats[j]) for j in range(n)]) <= car_size, "Volume" + str(i)

    prob.solve()
    print(pulp.LpStatus[prob.status])
    solution = [i for j in range(n) for i in range(k) if x[(i, j)].varValue == 1]
    print(solution)
    partition_dict = defaultdict(list)
    for xuhao in range(n):
        partition_dict[solution[xuhao]].extend(cats[xuhao])
    return list(partition_dict.values())


if __name__ == '__main__':
    nums = [7, 0]
    cars = [12, 0]
    cats = [5] * 10
    # nums[0] = int(sum(cats) // cars[0]) + 3
    # last = 0
    # while last == 0:
    #     nums[0] -= 1
    #     solution, last = cats_in_cars(nums, cars, cats)
    solution, last = cats_in_cars(nums, cars, cats)
    print(solution)
