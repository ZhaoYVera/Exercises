

class TourArray:
    def __init__(self, route: list):
        self.size = len(route)
        if sorted(route) != list(range(self.size)):
            raise ValueError(f"Input must be a permutation of {self.size}")
        self.route = route.copy()
        self.inverse_route = [0, ]*self.size
        for i, k in enumerate(route):
            self.inverse_route[k] = i

    def check_feasible(self, v: list, p_2k_2: list):  # O(n) if p_2k_2 empty, O(k) if not
        # Gao lao shi Chao qiang!
        # p_2k_2 stands for the permutation of the first (2k-2) break_vs in the route
        if not p_2k_2:  # O(n) in worst case
            # set v0 in front of v1 in the route
            if self.route.index(v[0]) > self.route.index(v[1]):
                self.route.reverse()
                for i, k in enumerate(self.route):
                    self.inverse_route[k] = i
        # get the permutation of last two break_vs
        node1 = len(v)-2 if self.route.index(v[-1]) > self.route.index(v[-2]) else len(v)-1
        node2 = len(v)-1 if node1 == len(v)-2 else len(v)-2
        p_2k = p_2k_2.copy()
        for i in p_2k_2:  # O(k)
            if self.route.index(v[i]) > self.route.index(v[node1]):
                p_2k.insert(i-1, node1)
                p_2k.insert(i, node2)
                break
        if len(p_2k) == len(p_2k_2):
            p_2k.append(node1)
            p_2k.append(node2)
        # q: the inverse permutation w.r.t. p_2k
        q = [0, ]*len(p_2k)
        for i, k in enumerate(p_2k):  # O(k)
            q[k] = i

        incl = [0, len(v)-1]
        # First jump v[0] to v[2k-1] = v[-1]
        while len(incl) < len(v):  # O(k)
            index = q[incl[-1]]
            item2append = p_2k[index - 1] if index % 2 == 0 else p_2k[(index + 1) % len(v)]
            if item2append == 0:
                break
            incl.append(item2append)
            item2append = incl[-1] - 1 if incl[-1] % 2 == 0 else incl[-1] + 1
            if item2append == 0:
                break
            incl.append(item2append)
        return len(incl) == len(v)

    def k_exchange(self, v: list):  # O(n*k^2) ???
        initial_index = max(self.route.index(v[0]), self.route.index(v[1]))
        tmp_route = self.route[initial_index:] + self.route[:initial_index]  # O(n)
        # cut the tour to get several fragment w.r.t. v
        fragments = []
        first_v_index = 0
        while first_v_index < self.size:  # O(n)
            next_v_index = first_v_index+1
            while next_v_index < self.size:
                if tmp_route[next_v_index] not in v:
                    next_v_index += 1
                else:
                    break
            fragments.append(tmp_route[first_v_index:next_v_index+1])
            first_v_index = next_v_index + 1
        # relink the fragments into a new route
        # pair2del = {}
        pair2add = {}
        for i in range(len(v) // 2):  # O(k)
            # pair2del[v[2 * i]] = v[2 * i + 1]
            # pair2del[v[2 * i + 1]] = v[2 * i]
            pair2add[v[2 * i - 1]] = v[2 * i]
            pair2add[v[2 * i]] = v[2 * i - 1]
        new_route = []
        first_node = v[-1]
        for _ in range(len(fragments)):  # O(n*k^2)
            last_node = -1
            for fragment in fragments:  # O(n*k)
                if first_node == fragment[0]:
                    new_route += fragment
                    fragments.remove(fragment)
                    last_node = fragment[-1]
                    break
                elif first_node == fragment[-1]:  # O(n) in worst case
                    new_route += reversed(fragment)
                    fragments.remove(fragment)
                    last_node = fragment[0]
                    break
            first_node = pair2add[last_node]
        self.route = new_route.copy()
        for i, k in enumerate(new_route):
            self.inverse_route[k] = i
        return

