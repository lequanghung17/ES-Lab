from pysat.solvers import Glucose3
from itertools import combinations

solver = Glucose3()

def Naive_ALK(n,k):
    # ALK True = ALO n - k + 1 True

    for i in combinations(n, len(n) - k + 1):
        solver.add_clause(var for var in i)

def Naive_AMK(n,k):
    # AMK True = ALO k + 1 False

    for i in combinations(n, k + 1):
        solver.add_clause([-var for var in i])

def Naive_ExactlyK(n,k):
    Naive_ALK(n,k)
    Naive_AMK(n,k)

