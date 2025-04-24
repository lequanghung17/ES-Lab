
from docplex.mp.model import Model
import os

os.environ['PATH'] += r';C:\Program Files\IBM\ILOG\CPLEX_Studio_Community2212\cplex\bin\x64_win64'

# Tạo model đơn giản
mdl = Model("cplex_test")

# Biến x, y
x = mdl.binary_var(name="x")
y = mdl.binary_var(name="y")
z = mdl.continuous_var(name="z")
k = mdl.integer_var(name="k")

# Ràng buộc: x + 2y ≤ 2
mdl.add_constraint(x + 2*y <= 2)

# Mục tiêu: maximize x + y
mdl.maximize(x + y)

# Giải
solution = mdl.solve(log_output=True)

# In kết quả
if solution:
    print("✅ CPLEX chạy OK!")
    print("x =", x.solution_value)
    print("y =", y.solution_value)
    print("Objective =", mdl.objective_value)
else:
    print("❌ Không tìm thấy lời giải.")



# from docplex.cp.model import CpoModel   # CP

# # Tạo model CP
# mdl = CpoModel()

# # Biến x, y là nhị phân (0 hoặc 1)
# x = mdl.binary_var(name="x")
# y = mdl.binary_var(name="y")

# # Biến nguyên k
# k = mdl.integer_var(name="k", lb=0, ub=1000)  # Giới hạn trên giả định

# # Ràng buộc: x + 2y ≤ 2
# mdl.add(x + 2 * y <= 2)

# # Hàm mục tiêu: maximize x + y
# mdl.add(mdl.maximize(x + y))

# # Giải model
# solution = mdl.solve(log_output=True)

# # In kết quả
# if solution:
#     print("✅ CP Optimizer chạy OK!")
#     print("x =", solution[x])
#     print("y =", solution[y])
#     print("Objective =", solution.get_objective_value())
# else:
#     print("❌ Không tìm thấy lời giải.")
