# from ortools.sat.python import cp_model

# model = cp_model.CpModel()
# x = model.NewBoolVar("x")
# y = model.NewBoolVar("y")
# model.Add(x + y == 1)
# model.Maximize(x + 2 * y)

# solver = cp_model.CpSolver()
# status = solver.Solve(model)

# print("x =", solver.Value(x))
# print("y =", solver.Value(y))

from ortools.linear_solver import pywraplp # MIP


def main():
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SAT")
    if not solver:
        return

    infinity = solver.infinity()
    # x and y are integer non-negative variables.
    x = solver.IntVar(0.0, infinity, "x")
    y = solver.IntVar(0.0, infinity, "y")

    print("Number of variables =", solver.NumVariables())

    # x + 7 * y <= 17.5.
    solver.Add(x + 7 * y <= 17.5)

    # x <= 3.5.
    solver.Add(x <= 3.5)

    print("Number of constraints =", solver.NumConstraints())

    # Maximize x + 10 * y.
    solver.Maximize(x + 10 * y)

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print("Objective value =", solver.Objective().Value())
        print("x =", x.solution_value())
        print("y =", y.solution_value())
    else:
        print("The problem does not have an optimal solution.")

    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    print(f"Problem solved in {solver.nodes():d} branch-and-bound nodes")


if __name__ == "__main__":
    main()


#     from ortools.sat.python import cp_model # CP

# model = cp_model.CpModel()

# # Biến nguyên không âm
# x = model.NewIntVar(0, 100000, "x")

# # Biến nhị phân
# y = model.NewBoolVar("y")

# # Một mảng biến nguyên
# z = [model.NewIntVar(0, 10, f"z_{i}") for i in range(5)]

# # Ràng buộc
# model.Add(x + sum(z) <= 100)

# # Mục tiêu
# model.Maximize(x + y)

# # Giải
# solver = cp_model.CpSolver()
# status = solver.Solve(model)

# if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
#     print("x =", solver.Value(x))
#     print("y =", solver.Value(y))
#     print("z =", [solver.Value(v) for v in z])
