from pysat.solvers import Glucose3


days = [1, 2, 3]  
sessions = ['S', 'C']  
subjects = ['A', 'B', 'C', 'D', 'E'] 


def var(m, d, s):
    return subjects.index(m) * len(days) * len(sessions) + (d - 1) * len(sessions) + (0 if s == 'S' else 1) + 1


clauses = []

# Ràng buộc 1: Mỗi môn học phải thi một lần
for m in subjects:
    possible_slots = [var(m, d, s) for d in days for s in sessions]
    clauses.append(possible_slots) 
    for i in range(len(possible_slots)):
        for j in range(i + 1, len(possible_slots)):
            clauses.append([-possible_slots[i], -possible_slots[j]])  

# Ràng buộc 2: Một môn không thể thi cả sáng và chiều trong cùng một ngày
for m in subjects:
    for d in days:
        clauses.append([-var(m, d, 'S'), -var(m, d, 'C')])


# Ràng buộc 3: Môn A và môn B không được thi cùng một ngày
for d in days:
    for s in sessions:
        clauses.append([-var('A', d, s), -var('B', d, s)] )

# Ràng buộc 4: Môn C chỉ thi vào buổi sáng
for d in days:
    clauses.append([-var('C', d, 'C')])  
    clauses.append([var('C', d, 'S') for d in days])  

# Ràng buộc 5: 2 mon khong the thi cung 1 ca
for d in days:
    for s in sessions:
        for m1 in subjects:
            for m2 in subjects:
                if m1 < m2: 
                    clauses.append([-var(m1, d, s), -var(m2, d, s)])


solver = Glucose3()
for clause in clauses:
    solver.add_clause(clause)

if solver.solve():
    model = solver.get_model()
    schedule = {}
    
    for m in subjects:
        for d in days:
            for s in sessions:
                if model[var(m, d, s) - 1] >= 0 :
                    schedule[m] = (d, s)
    
    print("Lịch thi hợp lệ:")
    for m, (d, s) in schedule.items():
        print(f"Môn {m}: Ngày {d}, Ca {s}")
else:
    print("Không có lịch thi hợp lệ.")