import math
import numpy as np
import collections


class Combination:
    def __init__(self, ll, m: int, check_func=None):
        ll.sort()
        self.n = len(ll)
        self.ll = ll
        self.max = m
        self.num_parts = math.ceil(sum(ll)/m)
        self.check = check_func
        self.results = collections.defaultdict(list)
        self.combinations = []
        self.combine()

    # def check_feasible(self, lst):
    #     return sum(self.decode(lst)) <= self.max

    def combine(self):
        """
        int 1~n, partition them into parts as few as possible, i.e. num_parts,
        s.t. sum of values in each part no more than m
        """
        if self.num_parts == 1:
            self.combinations.append(self.ll)
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
            if self.check(item[-1], self.max):
                self.combinations.append(item)

    def make_new_pattern(self, pos, new_pattern, assigned_pattern, rest, i):
        if pos == len(rest):
            return
        new_pattern.append(rest[pos])
        del rest[pos]
        if self.check(new_pattern, self.max):
            self.results[i].append((*assigned_pattern[:-1], new_pattern.copy(), rest.copy()))
            self.make_new_pattern(pos, new_pattern, assigned_pattern, rest, i)
        else:
            rest.insert(pos, new_pattern.pop())
            return
        rest.insert(pos, new_pattern.pop())
        self.make_new_pattern(pos + 1, new_pattern, assigned_pattern, rest, i)


if __name__ == '__main__':
    def check_feasible(lst, m):
        return sum(lst) <= m
    r = Combination(list(np.arange(6)+1.5), 13, check_feasible)
    for combination in r.combinations:
        print(combination)
