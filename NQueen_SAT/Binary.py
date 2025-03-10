from pysat.solvers import Glucose3
import math

# Tạo biến cho bàn cờ N x N
def create_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]

# Mã hóa các điều kiện cho SAT
def encode_binary(clauses, target_var, auxiliary_vars):
    for var in auxiliary_vars:
        clauses.append([-target_var, var])

# Tạo các tổ hợp nhị phân
def generate_binary_patterns(size):
    binary_patterns = []
    for i in range(1 << size):  # = 2^size
        binary_patterns.append(format(i, '0' + str(size) + 'b'))  # Chuyển sang chuỗi nhị phân
    return binary_patterns

# Sinh các biến mới cần thiết cho việc mã hóa
def create_new_vars(current_end, total_vars):
    return [i for i in range(current_end + 1, current_end + math.ceil(math.log(total_vars, 2)) + 1)]

# Ràng buộc: Không có quá một quân hậu trên mỗi hàng hoặc cột
def at_most_one_queen(clauses, new_vars, line_vars):
    additional_vars = create_new_vars(n ** 2 + len(new_vars), len(line_vars))
    new_vars += additional_vars
    binary_patterns = generate_binary_patterns(len(additional_vars))

    for i in range(len(line_vars)):
        pattern = binary_patterns[i]
        clause = []
        for j in range(len(pattern) - 1, -1, -1):
            idx = len(pattern) - j - 1
            clause.append({True: additional_vars[idx], False: -additional_vars[idx]} [int(pattern[j]) == 1])

        encode_binary(clauses, line_vars[i], clause)

# Ràng buộc: Chính xác một quân hậu trong mỗi hàng hoặc cột
def exactly_one_queen(clauses, new_vars, line_vars):
    clauses.append(line_vars)
    at_most_one_queen(clauses, new_vars, line_vars)

# Tạo các mệnh đề CNF cho bài toán N-Queens
def generate_constraints(n, all_vars):
    clauses = []
    new_vars = []

    # Chính xác một quân hậu trong mỗi hàng
    for i in range(n):
        exactly_one_queen(clauses, new_vars, all_vars[i])

    # Chính xác một quân hậu trong mỗi cột
    for j in range(n):
        exactly_one_queen(clauses, new_vars, [all_vars[i][j] for i in range(n)])

    # Không có nhiều hơn một quân hậu trên mỗi đường chéo
    # Chéo từ dưới trái lên trên phải
    for i in range(1, n):
        diagonal = []
        row = i
        col = 0
        while row >= 0 and col < n:
            diagonal.append(all_vars[row][col])
            row -= 1
            col += 1
        at_most_one_queen(clauses, new_vars, diagonal)

    # Chéo từ trên trái xuống dưới phải
    for j in range(1, n - 1):
        diagonal = []
        row = n - 1
        col = j
        while row >= 0 and col < n:
            diagonal.append(all_vars[row][col])
            row -= 1
            col += 1
        at_most_one_queen(clauses, new_vars, diagonal)

    # Chéo từ dưới trái lên trên phải
    for i in range(n - 1):
        diagonal = []
        row = i
        col = 0
        while row < n and col < n:
            diagonal.append(all_vars[row][col])
            row += 1
            col += 1
        at_most_one_queen(clauses, new_vars, diagonal)

    # Chéo từ trên trái xuống dưới phải
    for j in range(1, n - 1):
        diagonal = []
        row = 0
        col = j
        while row < n and col < n:
            diagonal.append(all_vars[row][col])
            row += 1
            col += 1
        at_most_one_queen(clauses, new_vars, diagonal)

    return clauses

# Giải bài toán N-Queens
def solve_n_queens_problem(n):
    all_vars = create_variables(n)
    clauses = generate_constraints(n, all_vars)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        return [[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)]
    else:
        return None

# In ra bàn cờ giải pháp
def display_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))


n = 4
solution = solve_n_queens_problem(n)
display_solution(solution)
