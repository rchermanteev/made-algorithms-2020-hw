import sys


def convert_input(operation, start_idx, end_idx):
    return operation, int(start_idx), int(end_idx)


class FenwickTree:
    def __init__(self, arr, sum_arr=None):
        self.arr = arr
        self.size = len(arr)
        self.sum_arr = sum_arr
        if self.sum_arr is None:
            self.build_tree()

    @staticmethod
    def func_fenwick(idx):
        return idx & (idx + 1)

    def build_tree(self):
        self.sum_arr = [0 for _ in range(self.size)]
        for i in range(self.size):
            self.add(i, self.arr[i])

    def add(self, idx, value):
        while idx < self.size:
            self.sum_arr[idx] += value
            idx = idx | (idx + 1)

    def get(self, idx):
        res = 0
        while idx >= 0:
            res += self.sum_arr[idx]
            idx = self.func_fenwick(idx) - 1

        return res

    def set(self, idx, value):
        dif = value - self.arr[idx]
        self.arr[idx] = value
        self.add(idx, dif)

    def sum(self, idx_left, idx_right):
        if idx_left == 0:
            return self.get(idx_right)

        return self.get(idx_right) - self.get(idx_left - 1)


len_arr = int(sys.stdin.readline())
array = list(map(int, sys.stdin.readline().split()))
requests = [convert_input(*line.rstrip().split()) for line in sys.stdin.readlines()]

fenw_tree = FenwickTree(array)
for req in requests:
    if req[0] == "sum":
        print(fenw_tree.sum(req[1] - 1, req[2] - 1))
    elif req[0] == "set":
        fenw_tree.set(req[1] - 1, req[2])
