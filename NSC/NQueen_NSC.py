from pysat.solvers import Glucose3


def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]
def generate_extra_variables(k, n, start):
    return [[i*k + j + 1 + start for j in range(k)] for i in range(n - 2)]

def AtLeastK(clauses, variables, start, k):

    extravariables = generate_extra_variables(k, len(variables), start)
    
    start = extravariables[-1][-1]
    
    # 1. X_i → R_{i,1}  ⇔  ¬X_i ∨ R_{i,1}
    for i in range(1, len(variables) - 1):
        clauses.append([-variables[i], extravariables[i - 1][0]])

    # 2. R_{i-1,j} → R_{i,j}  ⇔  ¬R_{i-1,j} ∨ R_{i,j}
    for i in range(2, len(variables) - 1):
        for j in range(min(i - 1, k)):
            clauses.append([-extravariables[i - 2][j], extravariables[i - 1][j]])
    
    # 3. X_i ∧ R_{i-1,j-1} → R_{i,j}  ⇔  ¬X_i ∨ ¬R_{i-1,j-1} ∨ R_{i,j}
    for i in range(2, len(variables) - 1):
        for j in range(1, min(i, k)):
            clauses.append([-variables[i], -extravariables[i - 2][j - 1], extravariables[i - 1][j]])
    
    # 4. ¬X_i ∧ ¬R_{i-1,j} → ¬R_{i,j}  ⇔  X_i ∨ R_{i-1,j} ∨ ¬R_{i,j}
    for i in range(2, len(variables) - 1):
        for j in range(min(i - 1, k)):
            clauses.append([variables[i], extravariables[i - 2][j], -extravariables[i - 1][j]])
    
    # 5. ¬X_i → ¬R_{i,i}  ⇔  X_i ∨ ¬R_{i,i}
    for i in range(1, k + 1):
        clauses.append([variables[i], -extravariables[i - 1][i - 1]])
    
    # 6. ¬R_{i-1,j-1} → ¬R_{i,j}  ⇔  R_{i-1,j-1} ∨ ¬R_{i,j}
    for i in range(2, len(variables) - 1):
        for j in range(1, min(i,k)):
            clauses.append([extravariables[i - 2][j - 1], -extravariables[i - 1][j]])
    
    # 7. R_{n-1,k} ∨ (X_n ∧ R_{n-1,k-1})  ⇔  R_{n-1,k} ∨ X_n ^ R_{n-1,k} ∨ R_{n-1,k-1}
    clauses.append([extravariables[len(variables) - 3][k - 1], variables[len(variables) - 1]])
    clauses.append([extravariables[len(variables) - 3][k - 1], extravariables[len(variables) - 3][k -2]])

    return clauses, start

def AtMostK(clauses, variables, start, k):
    extravariables = generate_extra_variables(k, len(variables), start)
    
    start = extravariables[-1][-1]

    # 1. X_i → R_{i,1}  ⇔  ¬X_i ∨ R_{i,1}
    for i in range(1, len(variables) - 1):
        clauses.append([-variables[i], extravariables[i - 1][0]])

    # 2. R_{i-1,j} → R_{i,j}  ⇔  ¬R_{i-1,j} ∨ R_{i,j}
    for i in range(2, len(variables) - 1):
        for j in range(min(i - 1, k)):
            clauses.append([-extravariables[i - 2][j], extravariables[i - 1][j]])
    
    # 3. X_i ∧ R_{i-1,j-1} → R_{i,j}  ⇔  ¬X_i ∨ ¬R_{i-1,j-1} ∨ R_{i,j}
    for i in range(2, len(variables) - 1):
        for j in range(1, min(i, k)):
            clauses.append([-variables[i], -extravariables[i - 2][j - 1], extravariables[i - 1][j]])
    
    # 8. X_i → ¬R_{i-1,k}  ⇔  ¬X_i ∨ ¬R_{i-1,k}
    for i in range(k + 1, len(variables)):
        clauses.append([-variables[i], -extravariables[i - 2][k - 1]])
    
    return clauses, start

def ExactlyK (clauses, variables, start,k): # K = 1

    #with Nqueen, k = 1
    k = 1
    clauses, start = AtLeastK(clauses, variables, start, k)
    clauses, start = AtMostK(clauses, variables, start, k)
    return clauses, start


def NQueen_constraint(clauses, variables, start, n, k):

    clauses = []

    # constraint 1:
    for i in range(n):
        clauses, start = ExactlyK(clauses, variables[i], start,k)

    # constraint 2:
    for j in range(n):
        clauses, start = ExactlyK(clauses, [variables[i][j] for i in range(n)], start,k)


    # constraint 3:
    for i in range(n):
        for j in range(n):
            for h in range(1, n):
                if i + h < n and j + h < n:
                    clauses, start = AtMostK(clauses, [variables[i][j], variables[i + k][j + k]], start, 1)
                if i + h < n and j - h >= 0:
                    clauses, start = AtMostK(clauses, [variables[i][j], variables[i + k][j - k]], start, 1)

    return clauses, start

def solve_n_queens(n,k):
    k = 1
    variables = generate_variables(n)
    start = variables[-1][-1]
    clauses, start = NQueen_constraint(clauses, variables, start, n, k)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        return [[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)]
    else:
        return None


def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))


n = 4
k = 1

solution = solve_n_queens(n,k)
print_solution(solution)


