import geatpy as ea
from my_problem import MyProblem

problem = MyProblem()

Encoding = 'RI'
NIND = 50  # population size
Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)
population = ea.Population(Encoding, Field, NIND)

myAlgorithm = ea.moea_NSGA2_templet(problem, population)
myAlgorithm.MAXGEN = 200
myAlgorithm.drawing = 1

NDSet = myAlgorithm.run()
NDSet.save()

print('')
