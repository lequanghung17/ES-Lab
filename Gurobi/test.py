import gurobipy as gp
from gurobipy import GRB

model = gp.Model("test_model")
x = model.addVar(name="x")
model.setObjective(x, GRB.MAXIMIZE)
model.addConstr(x <= 10, "c0")
model.optimize()

print(f"x = {x.X}")
