import geatpy as ea
import numpy as np
import matplotlib.pyplot as plt


def aim(x):
    return x*np.sin(10*np.pi*x) + 2.0

x = np.linspace(-1, 2, 100)
plt.plot(x, aim(x))
plt.show()

# maximize aim(x) over [-1, 2]
x1 = [-1, 2]
b1 = [1, 1]  # 0 stands for boundary not include, 1 stands for boundary include
# parameters for ea.crtfld, output: filed
Encoding = 'BG'  # aaa kan bu dong
varType = np.array([0])  # array, stands for the type of variables, 0: continuous, 1: discrete
ranges = np.vstack([x1]).T  # array, variable
borders = np.vstack([b1]).T  # array, include boundary or not
# any difference between adding [] or not?
precisions = [4]  # precisions for variables, default=4 for each variable, only for 'BG'
codes = [1]  # only for 'BG', 0: binary, 1: gray
scales = [0]  # only for 'BG', sha???

NIND = 40  # population size
MAXGEN = 25  # max generations
FieldD = ea.crtfld(Encoding, varType, ranges, borders, precisions, codes, scales)
# output: array
# FieldD for 'BG': [lens of each variable in chromosome, lb, ub, codes, scales, lbin, upin, varType]
# FieldDR for 'RI' or 'P': [lb, ub, varType]
Lind = int(np.sum(FieldD[0, :]))  # lens of chromosome
obj_trace = np.zeros((MAXGEN, 2))  # for saving aim values
var_trace = np.zeros((MAXGEN, Lind))  # for saving the best chromosome of each generation

Chrom = ea.crtbp(NIND, Lind)  # create a binary chromosome matrix
variable = ea.bs2real(Chrom, FieldD)  # only for 'BG'??? decode??? transforming binary numbers into decimal numbers?
ObjV = aim(variable)
best_ind = np.argmax(ObjV)  # index of best aim value in a generation

for gen in range(MAXGEN):
    FitnV = ea.ranking(-ObjV)
    # input: ObjV: aim value for individuals, CV: constraints,
    # maxormins: default to minimize, useful for multi-variables
    # other parameters: ???
    # output: array, fitness value for individuals
    SelCh = Chrom[ea.selecting('rws', FitnV, NIND-1), :]
    # input: sel_f: how to select? 'dup', 'ecs', 'etour', 'otos', etc.
    # FitnV: array/int, Fitness Values/number of individuals, fitness value 1 for each individual
    # NSel: float, the scale to select
    # output: array, the index of selected individuals
    SelCh = ea.recombin('xovsp', SelCh, 0.7)
    # recombination
    # input: REC_F: function name for recombination, Chrom, RecOpt: probability of recombination
    # output: recombined Chrom matrix
    SelCh = ea.mutbin(Encoding, SelCh)  # mutation, optional parameter: probability of mutation

    Chrom = np.vstack([Chrom[best_ind, :], SelCh])
    variable = ea.bs2real(Chrom, FieldD)  # decode
    ObjV = aim(variable)

    best_ind = np.argmax(ObjV)
    obj_trace[gen, 0] = np.sum(ObjV) / NIND
    obj_trace[gen, 1] = ObjV[best_ind]  # the best aim value in each generation
    var_trace[gen, :] = Chrom[best_ind, :]

best_gen = np.argmax(obj_trace[:, 1])  # search maximum in column 1
print(f"The maximum aim: {obj_trace[best_ind, 1]}")
variable = ea.bs2real(var_trace[[best_ind], :], FieldD)
# decode of variable, input: Chrom: array, FieldD: array. output: Phenotype: array
print(f"The corresponding variable value: {variable[0, 0]}")
plt.plot(variable, aim(variable), 'bo')
plt.show()
