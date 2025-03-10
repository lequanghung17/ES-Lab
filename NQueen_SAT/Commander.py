from pysat.solvers import Glucose3
import math

# Tạo các biến nhị phân cho bàn cờ NxN
def create_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]

# Mã hóa ràng buộc AMO và ALO cho các nhóm
def encode_commander(clauses, group_vars, commander):
    
    if isinstance(group_vars[0], list):
        group_vars = [var for sublist in group_vars for var in sublist]
    
    
    group_vars = [int(var) for var in group_vars]
    commander = int(commander)
    
    # AMO ALO
    # nếu commander đúng thì 1 giá trị trong gr đúng
    clauses.append([commander] + [-var for var in group_vars])  # commander đúng nếu trong gr có gt đúng
    for var1 in group_vars:
        for var2 in group_vars:
            if var1 != var2:
                clauses.append([-var1, -var2])  # amo gt đúng
    
    # nếu commander sai thì sai cả
    for var in group_vars:
        clauses.append([-commander, -var])


def generate_clauses(n, variables):
    clauses = []
    new_vars = n * n + 1  # Khởi tạo các biến mới cho các nhóm
    
    # constraint 1
    for i in range(n):
        row = variables[i]
        # Ràng buộc ít nhất một quân hậu trong mỗi hàng
        clauses.append(row)
        # Ràng buộc không có hai quân hậu trong mỗi hàng
        for j in range(n):
            for k in range(j + 1, n):
                clauses.append([-row[j], -row[k]])
    
    # constraint 2
    for j in range(n):
        for i in range(n):
            for k in range(i + 1, n):
                clauses.append([-variables[i][j], -variables[k][j]])

    #  constraint 3
    for i in range(n):
        for j in range(n):
            for k in range(1, n):
                if i + k < n and j + k < n:
                    clauses.append([-variables[i][j], -variables[i+k][j+k]])

   
    for i in range(n):
        for j in range(n):
            for k in range(1, n):
                if i + k < n and j - k >= 0:
                    clauses.append([-variables[i][j], -variables[i+k][j-k]])

    # Commander Encoding: Chia các nhóm và thêm ràng buộc
    group_size = 3  # Mỗi nhóm có 3 biến 
    for i in range(0, n, group_size):
        group_vars = [variables[i][j] for j in range(group_size)]
        commander = new_vars
        new_vars += 1
        encode_commander(clauses, group_vars, commander)
    
    return clauses


def solve_n_queens(n):
    variables = create_variables(n)  # Tạo các biến cho bàn cờ
    clauses = generate_clauses(n, variables)  # Tạo các mệnh đề CNF cho các ràng buộc

    solver = Glucose3()  # Khởi tạo SAT solver
    for clause in clauses:
        clause = [int(x) for x in clause]  # Đảm bảo tất cả các giá trị trong mệnh đề là số nguyên
        solver.add_clause(clause)  # Thêm mệnh đề vào solver

    if solver.solve():  
        model = solver.get_model()  
        return [[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)]  # Chuyển đổi mô hình thành bàn cờ
    else:
        return None 

# in
def display_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))


n = 4
solution = solve_n_queens(n)
display_solution(solution)
