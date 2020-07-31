from math import ceil
import numpy as np
from collections import defaultdict


class Grouping:
    def __init__(self, ll, m: float, check_func=None):
        self.combinations = []
        if any(x > m for x in ll):
            return
        self.ll = sorted(ll)
        self.n = len(ll)
        self.max = m
        self.num_parts = ceil(sum(ll)/m)
        self.check = check_func
        self.results = defaultdict(list)
        self.combine()

    # def check_feasible(self, lst):
    #     return sum(self.decode(lst)) <= self.max

    def combine(self):
        """
        int 1~n, partition them into parts as few as possible, i.e. num_parts,
        s.t. sum of values in each part no more than m
        """
        if self.num_parts == 1:
            if self.check is None or self.check():
                self.combinations.append((self.ll, ))
            return
        self.results[1].append(([self.ll[-1]], self.ll[:-1]))
        self.make_new_pattern(0, [self.ll[-1]], [], self.ll[:-1], 1)
        i = 2
        while i < self.num_parts:
            for item in self.results[i-1]:
                self.results[i].append((*item[:-1], [item[-1][-1]], item[-1][:-1]))
                self.make_new_pattern(0, [item[-1][-1]], item, item[-1][:-1], i)
            i += 1
        for item in self.results[self.num_parts-1]:
            if sum(item[-1]) <= self.max:
                if self.check is None or self.check():
                    self.combinations.append(item)

    def make_new_pattern(self, pos, old_pattern, assigned_pattern, rest, i):
        if pos == len(rest):
            return
        new_pattern = old_pattern + [rest[pos]]
        if sum(new_pattern) <= self.max:
            if self.check is None or self.check():
                self.results[i].append((*assigned_pattern[:-1], new_pattern, rest[:pos]+rest[pos+1:]))
                self.make_new_pattern(pos, new_pattern, assigned_pattern, rest[:pos]+rest[pos+1:], i)
                self.make_new_pattern(pos + 1, old_pattern, assigned_pattern, rest, i)


if __name__ == '__main__':
    # n = 0
    # def check_feasible(lst, m):
    #     global n
    #     n += 1
    #     return sum(lst) <= m
    # import random
    # cats = [random.random() for _ in range(9)]
    # r = Grouping(cats, 3, check_feasible)
    # for combination in r.combinations:
    #     print(combination)
    # print(n)
    miaos = list(np.arange(3)+1.7)
    rm = Grouping(miaos, 8)
