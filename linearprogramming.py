from typing import List
import numpy as np


class Simplex:
    """
    min z = c1x1 + c2x2 + ... + cnxn
    s.t. Ax <= b, x >= 0
    """
    def __init__(self, obj: List[float], max_mode=False):
        self.mat = np.array([0.] + obj) * (-1 if max_mode else 1)
        self.max_mode = max_mode
        # self.m = 1
        # self.n = len(obj)
        self.combinations = {}
        for i in range(len(obj)):
            self.combinations[i+1] = 0.

    def add_constraint(self, a: List[float], b: float):
        """
        add constraint: a1x1 + a2x2 + ... + anxn <= b
        """
        self.mat = np.vstack([self.mat, [b] + a])
        # self.m += 1

    def solve(self):
        m, n = self.mat.shape
        # add m-1 relaxed variables
        temp = np.vstack([np.zeros(m-1), np.eye(m-1)])
        basic = list(range(n-1, n+m-1))
        mat = self.mat = np.hstack([self.mat, temp])
        k = mat[1:, 0].argmin() + 1
        if mat[k, 0] < 0:  # 此时初始解 not feasible, 需要寻找新的初始解
            tmp = mat[0].copy()
            mat[0] = 0
            mat = np.hstack([mat, np.array([1]+[-1]*(m-1)).reshape((-1, 1))])
            self.pivot(mat, k, n+m-1, basic)
            if self.simplex(mat, basic, m, n)[0] != 0:  # 此时该线性规划问题无解
                return None
            if n+m-1 in basic:
                self.pivot(mat, np.where(mat[0, 1:] != 0)[0][0] + 1, basic.index(n), basic)
            self.mat = np.vstack([tmp, mat[1:, :-1]])
            for i, x in enumerate(basic[1:]):
                self.mat[0] = self.mat[0] - self.mat[0, x] * self.mat[i+1]
        result, combination = self.simplex(self.mat, basic, m, n)
        result *= (1 if self.max_mode else -1)
        for key in combination.keys():
            self.combinations[key] = combination[key]
        return result

    def simplex(self, mat, basic, m, n):
        while mat[0, 1:].min() < 0:  # 停止条件：z 的所有系数均不小于0
            # 出基变量：z的系数小于0的项，Bland规则：取下标最小的项
            col = np.where(mat[0, 1:] < 0)[0][0] + 1
            # 入基变量：对出基变量约束最紧的项
            cons = np.array([mat[i, 0]/mat[i, col] if mat[i, col] > 0 else np.inf for i in range(1, m)])
            row = cons.argmin() + 1
            if mat[row, col] <= 0:  # unbounded problem
                return None
            self.pivot(mat, row, col, basic)
        # for i in range(1, m):
        #     if basic[i] < n:
        #         self.combinations[i] = mat[i, 0]
        return mat[0, 0], {basic[i]: mat[i, 0] for i in range(1, m) if basic[i] < n}

    @staticmethod
    def pivot(mat, row, col, basic):
        m = mat.shape[0]
        mat[row] = mat[row]/mat[row, col]
        for i in range(m):
            if i == row:
                continue
            mat[i] -= mat[i, col] * mat[row]
        basic[row] = col


if __name__ == '__main__':
    ss = Simplex([1, -1], max_mode=True)
    ss.add_constraint([-1, -1], -1)
    ss.add_constraint([1, 1], 2)

    aa = Simplex([1, -1])
    aa.add_constraint([-1, -1], -1)
    aa.add_constraint([1, 1], 2)

    bb = Simplex([1, -1])
    bb.add_constraint([1, 1], 2)
