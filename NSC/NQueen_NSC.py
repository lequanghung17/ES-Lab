from pysat.solvers import Glucose3


def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]
def generate_extra_variables(k, n, start):
    return [[i*k + j + 1 + start for j in range(k)] for i in range(n - 1)]

def AtLeastK(clauses, variables, start, k):

    extravariables = generate_extra_variables(k, len(variables), start)
    
    start = extravariables[-1][-1]
    
    # 1. X_i → R_{i,1}  ⇔  ¬X_i ∨ R_{i,1}
    for i in range(len(variables) - 1):
        clauses.append([-variables[i], extravariables[i][0]])
        
    # 2. R_{i-1,j} → R_{i,j}  ⇔  ¬R_{i-1,j} ∨ R_{i,j}
    for i in range(1, len(variables) - 1):
        for j in range(min(i, k)):
            clauses.append([-extravariables[i - 1][j], extravariables[i][j]])
    
    # 3. X_i ∧ R_{i-1,j-1} → R_{i,j}  ⇔  ¬X_i ∨ ¬R_{i-1,j-1} ∨ R_{i,j}
    for i in range(1, len(variables) - 1):
        for j in range(1, min(i + 1, k)):
            clauses.append([-variables[i], -extravariables[i - 1][j - 1], extravariables[i][j]])
    
    # 4. ¬X_i ∧ ¬R_{i-1,j} → ¬R_{i,j}  ⇔  X_i ∨ R_{i-1,j} ∨ ¬R_{i,j}
    for i in range(1, len(variables) - 1):
        for j in range(min(i, k)):
            clauses.append([variables[i], extravariables[i - 1][j], -extravariables[i][j]])
    
    # 5. ¬X_i → ¬R_{i,i}  ⇔  X_i ∨ ¬R_{i,i}
    for i in range(k):
        clauses.append([variables[i], -extravariables[i][i]])
    
   # 6. ¬R_{i-1,j-1} → ¬R_{i,j}  ⇔  R_{i-1,j-1} ∨ ¬R_{i,j}
    for i in range(1, len(variables) - 1):
        for j in range(1, min(i + 1,k)):
            clauses.append([extravariables[i - 1][j - 1], -extravariables[i][j]])
    
    # 7. R_{n-1,k} ∨ (X_n ∧ R_{n-1,k-1})  ⇔  R_{n-1,k} ∨ X_n ^ R_{n-1,k} ∨ R_{n-1,k-1}
    clauses.append([extravariables[len(variables) - 2][k - 1], variables[len(variables) - 1]])
    if k - 2 >= 0:
        clauses.append([extravariables[len(variables) - 2][k - 1], extravariables[len(variables) - 2][k - 2]])

    return clauses, start

def AtMostK(clauses, variables, start, k):
    extravariables = generate_extra_variables(k, len(variables), start)
    
    start = extravariables[-1][-1]

    # 1. X_i → R_{i,1}  ⇔  ¬X_i ∨ R_{i,1}
    for i in range(len(variables) - 1):
        clauses.append([-variables[i], extravariables[i][0]])

    # 2. R_{i-1,j} → R_{i,j}  ⇔  ¬R_{i-1,j} ∨ R_{i,j}
    for i in range(1, len(variables) - 1):
        for j in range(min(i, k)):
            clauses.append([-extravariables[i - 1][j], extravariables[i][j]])
    
    # 3. X_i ∧ R_{i-1,j-1} → R_{i,j}  ⇔  ¬X_i ∨ ¬R_{i-1,j-1} ∨ R_{i,j}
    for i in range(1, len(variables) - 1):
        for j in range(1, min(i + 1, k)):
            clauses.append([-variables[i], -extravariables[i - 1][j - 1], extravariables[i][j]])
    
    # 8. X_i → ¬R_{i-1,k}  ⇔  ¬X_i ∨ ¬R_{i-1,k}
    for i in range(k, len(variables)):
        clauses.append([-variables[i], -extravariables[i - 1][k - 1]])
    
    return clauses, start

def ExactlyK (clauses, variables, start): # K = 1

    #with Nqueen, k = 1
    clauses, start = AtLeastK(clauses, variables, start, 1)
    clauses, start = AtMostK(clauses, variables, start, 1)
    return clauses, start


def NQueen_constraint(n, variables, start):

    clauses = []

    # constraint 1:
    for i in range(n):
        clauses, start = ExactlyK(clauses, variables[i], start)

    # constraint 2:
    for j in range(n):
        clauses, start = ExactlyK(clauses, [variables[i][j] for i in range(n)], start)


    # constraint 3:
    for i in range(n):
        for j in range(n):
            for h in range(1, n):
                if i + h < n and j + h < n:
                    clauses, start = AtMostK(clauses, [variables[i][j], variables[i + h][j + h]], start, 1)
                if i + h < n and j - h >= 0:
                    clauses, start = AtMostK(clauses, [variables[i][j], variables[i + h][j - h]], start, 1)

    return clauses, start

def solve_n_queens(n):
    
    
    variables = generate_variables(n)
    start = variables[-1][-1]
    clauses, start = NQueen_constraint(n, variables, start)

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



solution = solve_n_queens(n)
print_solution(solution)


