from docplex.mp.model import Model

# E = employees             # danh sách nhân viên
D = days                 # 0 đến 30
S = slot_indices         # 0 đến 7
MS = morning_slots       # ca sáng
AS = afternoon_slots     # ca chiều

mdl = Model("Employee Scheduling")

# Tập e, s, d đã được định nghĩa trước
ws = {(e, s, d): mdl.binary_var(name=f"ws_{e}_{s}_{d}") for e in E for s in S for d in D}
wd = {(e, d): mdl.binary_var(name=f"wd_{e}_{d}") for e in E for d in D}
ms = {(e, d): mdl.binary_var(name=f"ms_{e}_{d}") for e in E for d in D}
as_ = {(e, d): mdl.binary_var(name=f"as_{e}_{d}") for e in E for d in D}

# Ràng buộc 1: Nhu cầu lao động
for s in S:
    for d in D:
        mdl.add_constraint(mdl.sum(ws[e, s, d] for e in E) >= Req[s, d])

# Ràng buộc 2: ws -> wd
for e in E:
    for s in S:
        for d in D:
            mdl.add_constraint(ws[e, s, d] <= wd[e, d])

# Ràng buộc 6: ws -> ms hoặc as
for e in E:
    for d in D:
        for s in MS:
            mdl.add_constraint(ws[e, s, d] <= ms[e, d])
        for s in AS:
            mdl.add_constraint(ws[e, s, d] <= as_[e, d])

# Ràng buộc 7: Không làm sáng và chiều cùng lúc
for e in E:
    for d in D:
        mdl.add_constraint(ms[e, d] + as_[e, d] <= 1)

# Ràng buộc 5: Vắng mặt không làm
for (e, d), absent in Abse.items():
    if absent:
        mdl.add_constraint(wd[e, d] == 0)
