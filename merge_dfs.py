import math
from typing import Iterable, List
from itertools import chain


class Visit:
    def __init__(self, name, quantity, operation='tihuo'):
        self.name = name
        self.quantity = quantity
        self.operation = operation

    def __repr__(self):
        return self.name


class Truck:
    def __init__(self, name, cubage):
        self.name = name
        self.cubage = cubage

    def __repr__(self):
        return self.name


dache = Truck('da', 12.5)
xiaoche = Truck('xiao', 9.6)


def merge_trip(tripl: list, tripr: list):
    # trip1, trip2: list of Visit
    xiehuodian = None
    for visit in reversed(tripl):
        if visit.operation == 'xiehuo':
            xiehuodian = visit
            break
    visits = []
    for visit in tripl + tripr:
        if visit.operation == 'tihuo':
            visits.append(visit)
    sum_quantity = sum([visit.quantity for visit in visits])
    num_xiao = math.ceil(sum_quantity/xiaoche.cubage)
    num_da = math.ceil(sum_quantity/dache.cubage)
    if num_xiao == 1:
        # visits.append(xiehuodian)
        return [(set(visits), )], xiaoche  # 后面再排路顺
    elif num_da == 1:
        # visits.append(xiehuodian)
        return [(set(visits), )], dache
    elif num_da > 3:
        return  # return None, 意味着不能拼在一起
    elif num_da < num_xiao:
        che = dache
        num_trip = num_da
    else:
        che = xiaoche
        num_trip = num_xiao
    # 确定用大/小车，几轮次。至此，num_trip 只可能为 2 或 3
    visits.sort(key=(lambda x: x.quantity), reverse=True)
    results = []
    trip1 = [visits[0]]
    if num_trip == 2:
        trip2 = []
        rest_visits = visits[1:]
        for visit in rest_visits:
            merge_dfs(trip1, trip2, visit, rest_visits, che, results)

    if num_trip == 3:
        if check_feasible(visits[:2], che):
            trip2 = []
            trip3 = []
            rest_visits = visits[1:]
            for visit in rest_visits:
                merge3_dfs(trip1, trip2, trip3, visit, rest_visits, che, results)
        else:
            trip2 = [visits[1]]
            if check_feasible(visits[1:3], che):
                trip3 = []
                rest_visits = visits[2:]
                for visit in rest_visits:
                    merge3_dfs(trip1, trip2, trip3, visit, rest_visits, che, results)
            else:
                trip3 = [visits[2]]
                rest_visits = visits[3:]
                for visit in rest_visits:
                    merge3_dfs(trip1, trip2, trip3, visit, rest_visits, che, results)
    if results:
        # QAQ = []
        # for result in results:
        #     QAQ.append((list(result[0])+[xiehuodian]+list(result[1])+[xiehuodian], che.name))
        # return QAQ
        return results, che
    raise ValueError("轮次不够")


def merge_dfs(trip1, trip2, visit, rest_visits, che, results):
    new_rest_visits = rest_visits.copy()
    new_rest_visits.remove(visit)
    if check_feasible(trip1 + [visit], che):
        if not new_rest_visits:
            result = (set(trip1+[visit]), set(trip2))
            # if result not in results:
            results.append(result)
        else:
            merge_dfs(trip1+[visit], trip2, new_rest_visits[0], new_rest_visits, che, results)
    if check_feasible(trip2+[visit], che):
        if not new_rest_visits:
            result = (set(trip1), set(trip2 + [visit]))
            # if result not in results:
            results.append(result)
        else:
            merge_dfs(trip1, trip2+[visit], new_rest_visits[0], new_rest_visits, che, results)
    return


def merge3_dfs(trip1, trip2, trip3, visit, rest_visits, che, results):
    new_rest_visits = rest_visits.copy()
    new_rest_visits.remove(visit)
    if check_feasible(trip1+[visit], che):
        if not new_rest_visits:
            result = (set(trip1+[visit]), set(trip2), set(trip3))
            if result not in results:
                results.append(result)
        else:
            merge3_dfs(trip1+[visit], trip2, trip3, new_rest_visits[0], new_rest_visits, che, results)
    if check_feasible(trip2+[visit], che):
        if not new_rest_visits:
            result = (set(trip1), set(trip2+[visit]), set(trip3))
            if result not in results:
                results.append(result)
        else:
            merge3_dfs(trip1, trip2+[visit], trip3, new_rest_visits[0], new_rest_visits, che, results)
    if check_feasible(trip3+[visit], che):
        if not new_rest_visits:
            result = (set(trip1), set(trip2), set(trip3+[visit]))
            if result not in results:
                results.append(result)
        else:
            merge3_dfs(trip1, trip2, trip3+[visit], new_rest_visits[0], new_rest_visits, che, results)
    return


def check_feasible(trip: list, che):
    if trip:
        return sum([visit.quantity for visit in trip]) <= che.cubage
    else:
        return True


def ha_feasible(route):
    return


def split_multitrip(visits: List[Visit], check_feasible: callable):
    """
    visits: 所有提货点， 已按照货量从小到大排好
    """
    sum_quantity = sum([visit.quantity for visit in visits])
    num_xiao = math.ceil(sum_quantity/xiaoche.cubage)
    num_da = math.ceil(sum_quantity/dache.cubage)
    if num_xiao > 3:
        return
    if num_xiao == 1:
        return set(visits), xiaoche
    if num_da == 1:
        return set(visits), dache
    if num_da == num_xiao:
        num_trip = num_xiao
        che = xiaoche
    else:
        num_trip = num_da
        che = dache
    results = []
    rest_visits = visits.copy()
    trips = next_pattern(rest_visits, check_feasible, che)
    num_trip -= 1
    while num_trip > 1:
        num_trip -= 1
        for trip in trips:
            rest_visits = list(filter((lambda x: x not in chain(*trip)), rest_visits))
            patterns = next_pattern(rest_visits, check_feasible, che)
            trips = [trip.append(pattern) for pattern in patterns]
    for trip in trips:
        rest_visits = list(filter((lambda x: x not in chain(*trip)), rest_visits))
        if check_feasible(rest_visits, che):
            results.append(trips.append(rest_visits))


def next_pattern(rest_visits: List[Visit], check_feasible: callable, che):
    pattern = [rest_visits[-1]]
    patterns = [pattern.copy()]
    for visit in rest_visits:
        if not check_feasible(pattern+[visit], che):
            return patterns
        else:
            patterns.append(pattern+[rest_visits[0]])




if __name__ == '__main__':
    a = Visit('A', 5)
    b = Visit('B', 5)
    c = Visit('C', 4)
    d = Visit('D', 4)
    e = Visit('E', 2)
    f = Visit('F', 1)
    s = Visit('S', 200, 'xiehuo')
    tripl = [a, s, c, s]
    tripr = [b, s]
    r = merge_trip(tripl, tripr)
