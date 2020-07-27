from typing import List
import math
import numpy as np
import collections


class Combination:
    def __init__(self, ll, m: int, check_func=None):
        ll.sort()
        self.n = len(ll)
        self.ll = list(np.arange(self.n)+1)
        self.ll_dict = {}
        for i in range(self.n):
            self.ll_dict[i+1] = ll[i]
        self.max = m
        self.num_parts = math.ceil(sum(ll)/m)
        self.check = check_func
        self.results = collections.defaultdict(list)
        self.combinations = []
        self.combine()

    # def check_feasible(self, lst):
    #     return sum(self.decode(lst)) <= self.max

    def decode(self, lst):
        output = []
        for i in lst:
            output.append(self.ll_dict[i])
        return output.copy()

    def get_combinations(self):
        rs = []
        for combination in self.combinations:
            decode_combination = []
            for item in combination:
                decode_combination.append(self.decode(item))
            rs.append(decode_combination.copy())
        return rs

    def combine(self):
        """
        int 1~n, partition them into parts as few as possible, i.e. num_parts,
        s.t. sum of each part no more than m
        """
        if self.num_parts == 1:
            self.combinations.append(self.ll)
            return
        self.results[1].append(([self.ll[-1]], self.ll[:-1]))
        self.make_new_part(0, [self.ll[-1]], [], self.ll[:-1], 1)
        i = 2
        while i < self.num_parts:
            for item in self.results[i-1]:
                self.results[i].append((*item[:-1], [item[-1][-1]], item[-1][:-1]))
                self.make_new_part(0, [item[-1][-1]], item, item[-1][:-1], i)
            i += 1
        for item in self.results[self.num_parts-1]:
            if self.check(self.decode(item[-1]), self.max):
                self.combinations.append(item)

    def make_new_part(self, pos, new_part, item, rest, i):
        if pos == len(rest):
            return
        new_part.append(rest[pos])
        del rest[pos]
        if self.check(self.decode(new_part), self.max):
            self.results[i].append((*item[:-1], new_part.copy(), rest.copy()))
            self.make_new_part(pos, new_part, item, rest, i)
        else:
            rest.insert(pos, new_part.pop())
            return
        rest.insert(pos, new_part.pop())
        self.make_new_part(pos + 1, new_part, item, rest, i)


if __name__ == '__main__':
    def check_feasible(lst, m):
        return sum(lst) <= m
    r = Combination(list(np.arange(6)+1.5), 13, check_feasible)
    for item in r.get_combinations():
        print(item)
