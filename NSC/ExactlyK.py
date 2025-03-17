from pysat.solvers import Glucose3

def generate_varibales(numbers):
    return [-1] + [i for i in range(1, numbers + 1)] # X ( bat dau tu 1)

def generate_extra_variables(k, n, start):
    return [[i*k + j + 1 + start for j in range(k)] for i in range(n - 2)] # R ( bat dau tu n + 1)


# NSC
# 1. X_i → R_{i,1}  ⇔  ¬X_i ∨ R_{i,1}
# 2. R_{i-1,j} → R_{i,j}  ⇔  ¬R_{i-1,j} ∨ R_{i,j}
# 3. X_i ∧ R_{i-1,j-1} → R_{i,j}  ⇔  ¬X_i ∨ ¬R_{i-1,j-1} ∨ R_{i,j}
# 4. ¬X_i ∧ ¬R_{i-1,j} → ¬R_{i,j}  ⇔  X_i ∨ R_{i-1,j} ∨ ¬R_{i,j}
# 5. ¬X_i → ¬R_{i,i}  ⇔  X_i ∨ ¬R_{i,i}
# 6. ¬R_{i-1,j-1} → ¬R_{i,j}  ⇔  R_{i-1,j-1} ∨ ¬R_{i,j}
# 7. R_{n-1,k} ∨ (X_n ∧ R_{n-1,k-1})  ⇔  R_{n-1,k} ∨ X_n ∨ R_{n-1,k-1}
# 8. X_i → ¬R_{i-1,k}  ⇔  ¬X_i ∨ ¬R_{i-1,k}
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

k = 6
n = 10
variables = generate_varibales(n)
start = variables[-1]
clauses = []

clauses, start = AtLeastK(clauses, variables, start, k)
clauses, start = AtMostK(clauses, variables, start, k)

solver = Glucose3()
for clause in clauses:
    solver.add_clause(clause)

if solver.solve():
    model = solver.get_model()
    print(model[:n])
else:
    print("No solution found.")

    