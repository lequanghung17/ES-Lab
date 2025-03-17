
from pysat.solvers import Glucose3


def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]

def at_most_one_seq(clauses, variables, next_aux_var):
    n = len(variables)
    # Tạo các biến phụ s_1, ..., s_{n-1} với ID từ next_aux_var đến next_aux_var + n - 2.
    s_vars = list(range(next_aux_var, next_aux_var + n - 1))
    next_aux_var_updated = next_aux_var + n - 1

    # ¬x1 ∨ s1
    clauses.append([-variables[0], s_vars[0]])


    for i in range(1, n - 1):
        # (¬x_i ∨ s_i)
        clauses.append([-variables[i], s_vars[i]])
        # (¬s_{i-1} ∨ s_i)
        clauses.append([-s_vars[i - 1], s_vars[i]])
        # (¬x_i ∨ ¬s_{i-1})
        clauses.append([-variables[i], -s_vars[i - 1]])
        
    #  (¬x_n ∨ ¬s_{n-1})
    clauses.append([-variables[n - 1], -s_vars[n - 2]])

    return next_aux_var_updated

def at_least_one(clauses, variables):
    clauses.append(variables)

def exactly_one_seq(clauses, variables, next_aux_var):
    at_least_one(clauses, variables)
    next_aux_var = at_most_one_seq(clauses, variables, next_aux_var)
    return next_aux_var

# RETURN: Trả về các mệnh đề phù hợp để giả NQueens (clauses) 
#         và ID biến tiếp theo sau khi đã cấp phát các biến phụ (next_aux_var)

def generate_clauses_seq(n, board):
    clauses = []
    next_aux_var = n * n + 1

    # constraint 1: 
    for i in range(n):
        row_vars = board[i]
        next_aux_var = exactly_one_seq(clauses, row_vars, next_aux_var)

    # constraint 2:
    for j in range(n):
        col_vars = [board[i][j] for i in range(n)]
        next_aux_var = exactly_one_seq(clauses, col_vars, next_aux_var)

    # constraint 3:
    for i in range(n):
        for j in range(n):
            diag1 = []
            diag2 = []
            for k in range(1, n):
                if i + k < n and j + k < n:
                    diag1.append(board[i + k][j + k])
                if i + k < n and j - k >= 0:
                    diag2.append(board[i + k][j - k])
            if len(diag1) > 1:
                next_aux_var = at_most_one_seq(clauses, diag1, next_aux_var)
            if len(diag2) > 1:
                next_aux_var = at_most_one_seq(clauses, diag2, next_aux_var)

    return clauses, next_aux_var

# solve
def solve_nqueens_seq(n):
    board = generate_variables(n)  # Ma trận bàn cờ n x n
    clauses, _ = generate_clauses_seq(n, board)

    solver = Glucose3()
    for cl in clauses:
        solver.add_clause(cl)

    if solver.solve():
        model = solver.get_model()
        solution = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                var_id = board[i][j]
                if var_id in model:
                    solution[i][j] = 1
        return solution
    else:
        return None

def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))

n = 4  
solution = solve_nqueens_seq(n)
print_solution(solution)


#   clauses: danh sách các mệnh đề đang có
#   variables: danh sách các biến để add theo format AMO
#   next_aux_var: biến ID tiếp theo để cấp phát các biến phụ.
#   RETURN: trả về next_aux_var_updated: giá trị next_aux_var sau khi cấp phát các biến phụ.
#   n = 8 error