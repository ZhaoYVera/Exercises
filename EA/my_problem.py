import numpy as np
import geatpy as ea


class MyProblem(ea.Problem):
    def __init__(self):
        name = 'ZDT1'
        M = 2  # the number of aims
        maxormins = [1] * M  # 1: minimize, -1: maximize
        Dim = 30  # dimension of variables
        varTypes = [0] * Dim  # 0: continuous, 1: discrete
        lb = [0] * Dim
        ub = [1] * Dim
        lbin = [1] * Dim
        ubin = [1] * Dim

        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):
        # pop: object? of Population
        Vars = pop.Phen  # Phen: array, matrix of variable?
        ObjV1 = Vars[:, 0]
        gx = 1 + 9 * np.sum(Vars[:, 1:30], 1)
        hx = 1 - np.sqrt(ObjV1/gx)
        ObjV2 = gx*hx
        pop.ObjV = np.array([ObjV1, ObjV2]).T

    def calReferObjV(self):
        # calculate reference objective value
        N = 10000  # number of reference points
        ObjV1 = np.linspace(0, 1, N)
        # create uniformly distributed discrete points start from 0, end at 1, totally N points
        ObjV2 = 1 - np.sqrt(ObjV1)
        globalBestObjV = np.array([ObjV1, ObjV2]).T
        return globalBestObjV
