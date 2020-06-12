

class BinaryHeap:

    def __init__(self, keys_list, min_heap=True):
        self.keys_list = keys_list.copy()
        for i in range(len(self.keys_list)):
            self.keys_list[i].id_heap = i
        self.min_heap = min_heap
        self.build_heap()

    @staticmethod
    def parent(i):
        return int((i-1)/2)

    @staticmethod
    def left(i):
        return 2*i+1

    @staticmethod
    def right(i):
        return 2*i+2

    def oppo_num(self):
        for i in range(1, 1 + len(self.keys_list)):
            self.keys_list[i - 1].key = - self.keys_list[i - 1].key

    def max_heapify(self, i):

        while True:
            left = self.left(i)
            right = self.right(i)
            if left < len(self.keys_list) and self.keys_list[left].key > self.keys_list[i].key:
                largest = left
            else:
                largest = i
            if right < len(self.keys_list) and self.keys_list[right].key > self.keys_list[largest].key:
                largest = right

            if largest != i:
                exchange = self.keys_list[largest]
                self.keys_list[largest] = self.keys_list[i]
                self.keys_list[i] = exchange

                self.keys_list[largest].id_heap = largest
                self.keys_list[i].id_heap = i

                i = largest
            else:
                break

        return self.keys_list

    def build_heap(self):
        i = int(len(self.keys_list)/2)
        if self.min_heap:
            self.oppo_num()

        while i > -1:
            self.max_heapify(i)
            i += -1

        if self.min_heap:
            self.oppo_num()

        return self.keys_list

    def max_of_heap(self):
        if not self.min_heap:
            return self.keys_list[0]

    def min_of_heap(self):
        if self.min_heap:
            return self.keys_list[0]

    def compare_exchange_parent(self, i):
        p = self.parent(i)
        if self.keys_list[i] > self.keys_list[p]:
            exchange = self.keys_list[i]
            self.keys_list[i] = self.keys_list[p]
            self.keys_list[p] = exchange

            self.keys_list[i].id_heap = i
            self.keys_list[p].id_heap = p

        return self.keys_list

    def insert_into_heap(self, new):
        i = len(self.keys_list)

        if self.min_heap:
            self.oppo_num()
            new.key = -new.key

        self.keys_list.append(new)
        while True:
            p = self.parent(i)
            if self.keys_list[i].key > self.keys_list[p].key:
                exchange = self.keys_list[i]
                self.keys_list[i] = self.keys_list[p]
                self.keys_list[p] = exchange

                self.keys_list[i].id_heap = i
                self.keys_list[p].id_heap = p

                i = p
            else:
                break

        if self.min_heap:
            self.oppo_num()
        return self.keys_list

    def delete_extreme(self):
        n = len(self.keys_list)
        exchange = self.keys_list[0]
        self.keys_list[0] = self.keys_list[n - 1]
        self.keys_list[n - 1] = exchange

        self.keys_list[0].id_heap = 0
        self.keys_list[n - 1].id_heap = n - 1

        max_of_heap = self.keys_list.pop()
        self.max_heapify(0)
        return max_of_heap

    def delete_max_heap(self):
        if not self.min_heap:
            self.delete_extreme()

    def delete_min_heap(self):
        if self.min_heap:
            self.oppo_num()
            max_of_heap = self.delete_extreme()
            max_of_heap.key = - max_of_heap.key
            self.oppo_num()
            return max_of_heap

    def heap_sort(self):
        if self.min_heap:
            self.oppo_num()

        sorted_list = []
        for i in range(1, 1+len(self.keys_list)):
            next_max = self.delete_extreme()
            next_max.id_heap = i - 1
            sorted_list.append(next_max)
        self.keys_list = sorted_list

        if self.min_heap:
            self.oppo_num()
        return self.keys_list

    def change_key(self, x, k):
        if k > self.keys_list[x].key:
            self.keys_list[x].key = k
            while True:
                p = self.parent(x)
                if self.keys_list[x].key > self.keys_list[p].key:
                    exchange = self.keys_list[x]
                    self.keys_list[x] = self.keys_list[p]
                    self.keys_list[p] = exchange

                    self.keys_list[x].id_heap = x
                    self.keys_list[p].id_heap = p

                    x = p
                else:
                    break
        return self.keys_list

    def increase_key(self, x, k):
        # increases the value of element x’s key to the new value k,
        # which is assumed to be at least as large as x’s current key value

        if not self.min_heap:
            self.change_key(x, k)

    def decrease_key(self, x, k):
        if self.min_heap and x <= len(self.keys_list):
            self.oppo_num()
            self.keys_list = self.change_key(x, -k)
            self.oppo_num()
            return self.keys_list
