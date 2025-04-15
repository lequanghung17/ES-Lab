from pysat.solvers import Glucose3, Solver
from pysat.card import CardEnc
import random

total_var = 0

# At most one using sequential counter
def at_most_zero(var, S):
    n = len(var)
    clauses = []
    
    # (1): Biến R(i, j) = true khi x(i, j) = true
    for i in range(2, n):
        clauses.append([-var[i], S[i]])
    # (2): R(i, j) = true nếu R(i, j - 1) = true
    for i in range(2, n):
        clauses.append([-S[i - 1], S[i]])
    # (3): R(i, j) = false nếu toàn bộ biến x(j) thuộc tập w = false
    #                      nói cách khác x(j) = false & R(i, j - 1) = false
    for i in range(2, n):
        clauses.append([var[i], S[i - 1], -S[i]])
        
    return clauses

def at_most_one(var, S):
    n = len(var)
    clauses = []
    
    # Generate clauses
    clauses.extend(at_most_zero(var, S))
    # (4): đảm bảo ít nhất có 1 biến x(i, j) = true
    for i in range(2, n):
        clauses.append([-var[i], -S[i - 1]])  
     
    return clauses

def create_groups(variables, w):
    groups = [[-1]]
    temp = []
    count = 0
    
    for i in range(len(variables)):
        if (count == w):
            count = 0
            groups.append(temp)
            temp = []
        temp.append(variables[i])
        count += 1
    groups.append(temp)
    
    return groups

def process_group(group):
    global total_var
    
    variables = [-1] + group
    register = [-1, variables[1]] + [total_var + i + 1 for i in range(len(variables) - 2)]
    total_var += len(register) - 2
    
    clauses = at_most_one(variables, register)
    
    return clauses, register

# Ladder AMO constraint
def SCAMO(variables, w):
    global total_var
    
    num = len(variables)
    total_var = num
    all_clauses = []
    register = [[-1]]
    
    # Tạo các window biến chứa w phần tử
    groups = create_groups(variables, w)
    
    # AMO, AMZ cho các window biến
    # Window đầu tiên
    first_group_clauses, first_group_register = process_group(groups[1][::-1])
    all_clauses.extend(first_group_clauses)
    register.append(first_group_register)
    
    # Các window tiếp theo
    for i, group in enumerate(groups[2:], start=2):
        # AMO thứ tự xuôi
        normal_group_clauses, normal_group_register = process_group(group)
        all_clauses.extend(normal_group_clauses)
        register.append(normal_group_register)
        
        # AMO thứ tự ngược (trừ window cuối cùng)
        if i < len(groups) - 1:
            reverse_group_clauses, reverse_group_register = process_group(group[::-1])
            all_clauses.extend(reverse_group_clauses)
            register.append(reverse_group_register)
            
    # Kết nối các blocks lại với nhau
    i = 1
    while (i < len(register)):
        first_block_register = register[i]
        second_block_register = register[i + 1]
        2
        clauses = []
        for j in range(1, w):
            if (w - j) < len(first_block_register) and j < len(second_block_register):
                clauses.append([-first_block_register[w - j], -second_block_register[j]])
        
        all_clauses.extend(clauses)
        i += 2
    
    return all_clauses         
    
def solve(num, w):
    variables = [i for i in range(1, num + 1)]
    clauses = SCAMO(variables, w)
    
    # print(clauses)
    
    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)
    
    if solver.solve():
        model = solver.get_model()
        return [0 if model[i] < 0 else 1 for i in range(num)]
    
num = 100
w = 17
solution = solve(num, w)
print(solution)