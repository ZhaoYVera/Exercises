import math
import numpy as np
import collections
from typing import List
# from .utilities import AtomOrder


class Grouping:
    def __init__(self, ll: List, m: float, check_func=None):
        self.cat_comb = []
        ll.sort(key=lambda g: g.mass)
        if ll[-1].mass > m:
            return
        self.n = len(ll)
        self.ll = ll
        self.max = m
        self.num_parts = math.ceil(sum(ele.mass for ele in ll)/m)
        self.check = check_func
        self.results = collections.defaultdict(list)
        self.combine()

    def combine(self):
        """
        int 1~n, partition them into parts as few as possible, i.e. num_parts,
        s.t. sum of values in each part no more than m
        """
        if self.num_parts == 1:
            sites = [visit.site for visit in self.ll]
            if len(sites) == len(set(sites)):
                self.cat_comb.append((self.ll, ))
            return
        self.results[1].append(([self.ll[-1]], self.ll[:-1]))
        self.make_new_pattern(0, [self.ll[-1]], [], self.ll[:-1], 1)
        i = 2
        while i < self.num_parts:
            for *prev_rounds, rest in self.results[i-1]:
                self.results[i].append((*prev_rounds, [rest[-1]], rest[:-1]))
                self.make_new_pattern(0, [rest[-1]], prev_rounds, rest[:-1], i)
            i += 1
        for item in self.results[self.num_parts-1]:
            if sum([ele.mass for ele in item[-1]]) <= self.max:
                rest_sites = [ele.site for ele in item[-1]]
                if len(rest_sites) == len(set(rest_sites)):
                    if self.check is None or self.check():
                        self.cat_comb.append(item)

    def make_new_pattern(self, pos, old_pattern, assigned_pattern, rest, i):
        if pos == len(rest):
            return
        if any(rest[pos].site == ele.site for ele in old_pattern):
            return self.make_new_pattern(pos + 1, old_pattern, assigned_pattern, rest, i)
        new_pattern = old_pattern + [rest[pos]]
        if sum(ele.mass for ele in new_pattern) <= self.max:
            if self.check is None or self.check():
                new_rest = rest[:pos] + rest[pos+1:]
                self.results[i].append((*assigned_pattern, new_pattern, new_rest))
                self.make_new_pattern(pos, new_pattern, assigned_pattern, new_rest, i)
                self.make_new_pattern(pos + 1, old_pattern, assigned_pattern, rest, i)


if __name__ == '__main__':
    def check_feasible(lst, m):
        return sum(lst) <= m

    class Atom:
        def __init__(self, i, mass, site):
            self.i = i
            self.mass = mass
            self.site = site

        def __repr__(self):
            return str(self.i)

    import random
    random.seed(98)
    a = [Atom(i, i + 0.6, str(random.randint(0, 6))) for i in range(6)]
    for atom in a:
        print(atom.i, atom.site)
    r = Grouping(a, 6)
    for combination in r.cat_comb:
        print(combination)
