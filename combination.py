from typing import List
import math
import numpy as np
import collections


def check_feasible(lst, m):
    return sum(lst) <= m


class Combination:
    def __init__(self, n, m: int, func=check_feasible):
        self.ll = list(np.arange(n) + 1)
        self.n = n
        self.max = m
        self.num_parts = math.ceil(sum(self.ll)/m)
        self.check = func
        self.results = collections.defaultdict(list)
        self.combinations = []
        self.combine()

    def combine(self):
        """
        int 1~n, partition them into parts as few as possible, i.e. num_parts,
        sum of each part no more than m
        ll: a sorted list of 1~n
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
            if self.check(item[-1], self.max):
                self.combinations.append(item)

    def make_new_part(self, pos, new_part, item, rest, i):
        if pos == len(rest):
            return
        new_part.append(rest[pos])
        del rest[pos]
        if self.check(new_part, self.max):
            self.results[i].append((*item[:-1], new_part.copy(), rest.copy()))
            self.make_new_part(pos, new_part, item, rest, i)
        else:
            rest.insert(pos, new_part.pop())
            return
        rest.insert(pos, new_part.pop())
        self.make_new_part(pos + 1, new_part, item, rest, i)


if __name__ == '__main__':
    r = Combination(9, 17)
    # for item in r.:
    #     print(item)
