import itertools
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc
from pysat.solvers import Glucose3
import cplex
#from itertools import combinations

slot_times = [
    "07:00-09:00", "09:00-11:00", "11:00-13:00", "13:00-15:00",
    "15:00-17:00", "17:00-19:00", "19:00-21:00", "21:00-24:00"
]
num_slots = len(slot_times)
slot_indices = list(range(num_slots)) # 0 đến 7

num_days = 31
days = list(range(num_days)) # 0 đến 30 (ánh xạ từ Ngày 1 đến Ngày 31)

num_employees = 30
employees = [f'emp{i+1}' for i in range(num_employees)]

morning_slots = [0, 1, 2]
afternoon_slots = [3, 4, 5, 6, 7]

# --- Yêu cầu nhân viên (Req_sd) ---
# Chuyển đổi đầu vào thành dictionary
Req = {}
req_data_text = """
Ngày 1: 1, 3, 3, 1, 3, 2, 1, 1
Ngày 2: 1, 3, 3, 1, 2, 3, 3, 2
Ngày 3: 2, 2, 1, 2, 3, 2, 1, 2
Ngày 4: 1, 2, 3, 2, 2, 2, 1, 3
Ngày 5: 2, 2, 1, 1, 3, 2, 2, 1
Ngày 6: 3, 3, 2, 1, 2, 3, 2, 3
Ngày 7: 1, 3, 2, 2, 3, 1, 1, 2
Ngày 8: 3, 2, 2, 3, 1, 3, 3, 3
Ngày 9: 2, 2, 1, 3, 2, 1, 2, 1
Ngày 10: 1, 1, 1, 3, 1, 3, 3, 3
Ngày 11: 1, 3, 3, 2, 3, 3, 2, 3
Ngày 12: 3, 3, 1, 2, 2, 2, 1, 3
Ngày 13: 1, 2, 3, 1, 3, 2, 3, 2
Ngày 14: 1, 1, 2, 1, 3, 3, 3, 2
Ngày 15: 1, 2, 1, 1, 2, 3, 2, 2
Ngày 16: 1, 3, 3, 2, 2, 2, 3, 1
Ngày 17: 3, 1, 3, 1, 3, 2, 1, 1
Ngày 18: 3, 1, 1, 2, 1, 3, 2, 2
Ngày 19: 2, 2, 3, 1, 1, 2, 2, 3
Ngày 20: 2, 2, 3, 3, 1, 3, 3, 1
Ngày 21: 1, 3, 1, 3, 2, 1, 1, 1
Ngày 22: 3, 2, 1, 3, 2, 2, 3, 3
Ngày 23: 1, 1, 3, 3, 3, 2, 3, 1
Ngày 24: 3, 2, 2, 2, 3, 1, 2, 2
Ngày 25: 1, 2, 1, 1, 1, 1, 2, 2
Ngày 26: 3, 1, 1, 2, 1, 1, 2, 1
Ngày 27: 3, 1, 2, 1, 1, 3, 2, 2
Ngày 28: 2, 2, 1, 2, 3, 2, 2, 3
Ngày 29: 3, 1, 2, 1, 3, 2, 1, 2
Ngày 30: 1, 2, 2, 1, 3, 3, 1, 2
Ngày 31: 3, 2, 3, 1, 1, 1, 1, 3
"""
lines = req_data_text.strip().split('\n')
for i, line in enumerate(lines):
    day_index = i
    parts = line.split(':')
    counts = [int(c.strip()) for c in parts[1].split(',')]
    for slot_index, count in enumerate(counts):
        Req[(day_index, slot_index)] = count

# --- Thuộc tính nhân viên (Ràng buộc cá nhân) ---
# emp_props_data = {
#     'emp1': {'MaxWe': 1, 'MinCe': 2, 'MaxCe': 5, 'MaxCWe': 6, 'MaxCRe': 2},
#     'emp2': {'MaxWe': 1, 'MinCe': 1, 'MaxCe': 4, 'MaxCWe': 5, 'MaxCRe': 2},
#     'emp3': {'MaxWe': 2, 'MinCe': 2, 'MaxCe': 4, 'MaxCWe': 5, 'MaxCRe': 4},
#     'emp4': {'MaxWe': 1, 'MinCe': 1, 'MaxCe': 4, 'MaxCWe': 5, 'MaxCRe': 4},
#     'emp5': {'MaxWe': 1, 'MinCe': 1, 'MaxCe': 3, 'MaxCWe': 5, 'MaxCRe': 3},
#     'emp6': {'MaxWe': 2, 'MinCe': 2, 'MaxCe': 5, 'MaxCWe': 6, 'MaxCRe': 3},
#     'emp7': {'MaxWe': 2, 'MinCe': 1, 'MaxCe': 4, 'MaxCWe': 7, 'MaxCRe': 4},
#     'emp8': {'MaxWe': 1, 'MinCe': 1, 'MaxCe': 4, 'MaxCWe': 5, 'MaxCRe': 4},
#     'emp9': {'MaxWe': 3, 'MinCe': 1, 'MaxCe': 5, 'MaxCWe': 6, 'MaxCRe': 3},
#     'emp10': {'MaxWe': 3, 'MinCe': 2, 'MaxCe': 4, 'MaxCWe': 5, 'MaxCRe': 3},
#     'emp11': {'MaxWe': 1, 'MinCe': 2, 'MaxCe': 5, 'MaxCWe': 7, 'MaxCRe': 4},
#     'emp12': {'MaxWe': 1, 'MinCe': 1, 'MaxCe': 3, 'MaxCWe': 4, 'MaxCRe': 4},
#     'emp13': {'MaxWe': 1, 'MinCe': 2, 'MaxCe': 3, 'MaxCWe': 6, 'MaxCRe': 2},
#     'emp14': {'MaxWe': 3, 'MinCe': 2, 'MaxCe': 3, 'MaxCWe': 6, 'MaxCRe': 2},
#     'emp15': {'MaxWe': 3, 'MinCe': 2, 'MaxCe': 5, 'MaxCWe': 7, 'MaxCRe': 2},
#     'emp16': {'MaxWe': 1, 'MinCe': 2, 'MaxCe': 4, 'MaxCWe': 5, 'MaxCRe': 3},
#     'emp17': {'MaxWe': 3, 'MinCe': 1, 'MaxCe': 4, 'MaxCWe': 5, 'MaxCRe': 3},
#     'emp18': {'MaxWe': 2, 'MinCe': 2, 'MaxCe': 4, 'MaxCWe': 5, 'MaxCRe': 4},
#     'emp19': {'MaxWe': 3, 'MinCe': 2, 'MaxCe': 3, 'MaxCWe': 6, 'MaxCRe': 2},
#     'emp20': {'MaxWe': 3, 'MinCe': 2, 'MaxCe': 5, 'MaxCWe': 6, 'MaxCRe': 4},
#     'emp21': {'MaxWe': 2, 'MinCe': 1, 'MaxCe': 4, 'MaxCWe': 4, 'MaxCRe': 4},
#     'emp22': {'MaxWe': 2, 'MinCe': 1, 'MaxCe': 3, 'MaxCWe': 4, 'MaxCRe': 3},
#     'emp23': {'MaxWe': 2, 'MinCe': 2, 'MaxCe': 5, 'MaxCWe': 5, 'MaxCRe': 2},
#     'emp24': {'MaxWe': 3, 'MinCe': 2, 'MaxCe': 5, 'MaxCWe': 5, 'MaxCRe': 3},
#     'emp25': {'MaxWe': 2, 'MinCe': 2, 'MaxCe': 4, 'MaxCWe': 5, 'MaxCRe': 3},
#     'emp26': {'MaxWe': 2, 'MinCe': 2, 'MaxCe': 3, 'MaxCWe': 7, 'MaxCRe': 2},
#     'emp27': {'MaxWe': 1, 'MinCe': 1, 'MaxCe': 4, 'MaxCWe': 4, 'MaxCRe': 3},
#     'emp28': {'MaxWe': 1, 'MinCe': 2, 'MaxCe': 4, 'MaxCWe': 5, 'MaxCRe': 4},
#     'emp29': {'MaxWe': 2, 'MinCe': 1, 'MaxCe': 3, 'MaxCWe': 4, 'MaxCRe': 3},
#     'emp30': {'MaxWe': 2, 'MinCe': 1, 'MaxCe': 5, 'MaxCWe': 5, 'MaxCRe': 4}
# }
# #(Absed)
# Abs = {}

Per = 5
MaxD = 3
MaxWe = 4*60
MinWe = 2*60
MaxPe = 6*60
MinCe = 2*60
MaxCe = 5*60
MaxCWe = 4*60
MaxCRe = 3*60

vpool = IDPool()

def get_var(name, *args):
  """Lấy hoặc tạo ID biến duy nhất."""
  key = ('var', name) + tuple(str(a) for a in args) # Chuyển đổi args thành chuỗi để làm key
  return vpool.id(key)

# Biến quyết định (ánh xạ tên mô tả sang ID)
wsd = {(e, s, d): get_var('wsd', e, s, d)
       for e in employees for s in slot_indices for d in days}
wd = {(e, d): get_var('wd', e, d) for e in employees for d in days}
ms = {(e, d): get_var('ms', e, d) for e in employees for d in days} # Ca sáng
as_ = {(e, d): get_var('as', e, d) for e in employees for d in days} # Ca chiều


cnf = CNF()

# Ràng buộc 1: Đáp ứng nhu cầu 
# sum(wsd_esd for e in employees) >= Req[d,s]
for d in days:
    for s in slot_indices:
        required_count = Req.get((d, s), 0)
        if required_count > 0:
            vars_for_slot = [wsd[e, s, d] for e in employees]
            clauses = CardEnc.atleast(lits=vars_for_slot, bound=required_count, encoding=1, vpool=vpool)
            cnf.extend(clauses)

# Ràng buộc 2: ~wsd_esd V wd_ed
for e in employees:
    for d in days:
        for s in slot_indices:
            cnf.append([-wsd[e, s, d], wd[e, d]])

# Ràng buộc 5: Vắng mặt (Abs)
# ~wd_ed nếu Abs_ed là True
for e in employees:
    for d in days:
        if Abs.get((e, d), False):
            cnf.append([-wd[e, d]]) # Nếu vắng mặt, không được làm việc ngày đó

# Ràng buộc 6 & 7: wsd với ms/as 

for e in employees:
    for d in days:
        for s in morning_slots:
             cnf.append([-wsd[e, s, d], ms[e, d]])
        for s in afternoon_slots:
            cnf.append([-wsd[e, s, d], as_[e, d]])

# Ràng buộc 8: Không làm cả ca sáng và chiều 

for e in employees:
    for d in days:
        cnf.append([-ms[e, d], -as_[e, d]])

# Ràng buộc 11,12


# Ràng buộc 13, 14 (đơn giản hóa): Số ca làm việc tối đa mỗi ngày (MaxWe) 
# sum(wsd_esd for s in slots) <= MaxWe_e
for e in employees:
    max_slots_today = emp_props_data[e].get('MaxWe', num_slots) # Lấy giới hạn, mặc định là tất cả các ca
    for d in days:
        vars_today = [wsd[e, s, d] for s in slot_indices]
        # Tối đa 'max_slots_today' ca được làm
        clauses = CardEnc.atmost(lits=vars_today, bound=max_slots_today,encoding=1,  vpool=vpool)
        # for subset in combinations(vars_today, max_slots_today + 1):
        #     cnf.append([-s for s in subset])
        cnf.extend(clauses)
    
# Ràng buộc 15: Số ca làm việc tối thiểu mỗi ngày (MinWe)
# Chưa có MinWe
# for e in employees:
#     min_slots_today = emp_props_data[e].get('MinWe', num_slots) 
#     if min_slots_today > 0:
#         for d in days:
#             vars_today = [wsd[e, s, d] for s in slot_indices]
#             # Tối đa 'max_slots_today' ca được làm
#             clauses = CardEnc.atmost(lits=vars_today, bound=max_slots_today,encoding=1,  vpool=vpool)
#             # for subset in combinations(vars_today, max_slots_today + 1):
#             #     cnf.append([-s for s in subset])
#             cnf.extend(clauses)

# Ràng buộc 17: Số ca làm việc liên tục tối đa (MaxCe)
# Không được làm nhiều hơn MaxCe_e ca liên tục
# ~wsd_esd V ~wsd_e,s+1,d V ... V ~wsd_e,s+MaxCe,d
for e in employees:
    max_consec_slots = emp_props_data[e]['MaxCe']
    for d in days:
        for s_start in range(num_slots - max_consec_slots):
            window_vars = [wsd[e, s, d] for s in range(s_start, s_start + max_consec_slots + 1)]
            # ít nhất 1 false
            # clauses = CardEnc.atleast(lits=window_vars, bound=max_consec_slots, encoding = 1,vpool=vpool)
            # cnf.extend(clauses)
            cnf.append([-v for v in window_vars]) 

# Ràng buộc 18: Số ngày làm việc liên tục tối đa (MaxCWe)
# Không được làm nhiều hơn MaxCWe_e ngày liên tục
# ~wd_ed V ~wd_e,d+1 V ... V ~wd_e,d+MaxCWe,d
print("  Mã hóa ràng buộc số ngày làm liên tục tối đa (MaxCWe)...")
for e in employees:
    max_consec_work_days = emp_props_data[e]['MaxCWe']
    for d_start in range(num_days - max_consec_work_days):
        window_vars = [wd[e, d] for d in range(d_start, d_start + max_consec_work_days + 1)]
        cnf.append([-v for v in window_vars]) 

# Ràng buộc 19: Số ngày nghỉ liên tục tối đa (MaxCRe) 
# Không được nghỉ nhiều hơn MaxCRe_e ngày liên tục
# wd_ed V wd_e,d+1 V ... V wd_e,d+MaxCRe,d
print("  Mã hóa ràng buộc số ngày nghỉ liên tục tối đa (MaxCRe)...")
for e in employees:
    max_consec_rest_days = emp_props_data[e]['MaxCRe']
    for d_start in range(num_days - max_consec_rest_days):
        window_vars = [wd[e, d] for d in range(d_start, d_start + max_consec_rest_days + 1)]
        cnf.append(window_vars) 



sum_clause = len(cnf.clauses)
sum_new_var = vpool.top
# def gen_var_work(employees, days):
#     global var_count
#     list = [[var_count + i + j * num_employees + 1 for i in range (num_employees)]for j in range (num_days)]
#     var_count+=(num_days*num_employees)
#     return list


# def gen_var_shift(employees,num_slots, days):
#     global var_count
#     list = [[[var_count + i + j * num_employees + k * num_employees * num_slots + 1 for i in range (num_employees)]for j in range (num_shifts)] for k in range(num_days)]
#     var_count+=(num_days * num_employees * num_slots)
#     return list


with Glucose3(bootstrap_with=cnf.clauses) as g:
    is_satisfiable = g.solve()
    model = g.get_model() # Lấy model nếu có

if is_satisfiable:
    print("\nTìm thấy một lịch trình khả thi!")

    # Giải mã model
    schedule = {d: {s: [] for s in slot_indices} for d in days}
    positive_vars = {abs(lit): (lit > 0) for lit in model} # Tạo dict để tra cứu nhanh

    print("\n--- Lịch trình chi tiết ---")
    for d in days:
        print(f"\nNgày {d+1}:")
        for s in slot_indices:
            assigned_employees = []
            for e in employees:
                var_id = wsd.get((e, s, d))
                if var_id and positive_vars.get(var_id, False):
                    assigned_employees.append(e)
            req_count = Req.get((d, s), 0)
            slot_time_str = slot_times[s]
            print(f"  Ca {slot_time_str} (YC: {req_count}, TP: {len(assigned_employees)}): {', '.join(assigned_employees) if assigned_employees else '---'}")

    # In lịch trình của từng nhân viên
    print("\n--- Lịch trình theo nhân viên ---")
    for e in employees:
        print(f"\nNhân viên {e}:")
        worked_today = False
        for d in days:
            shifts_worked = []
            for s in slot_indices:
                 var_id = wsd.get((e, s, d))
                 if var_id and positive_vars.get(var_id, False):
                     shifts_worked.append(slot_times[s])
            if shifts_worked:
                 print(f"  Ngày {d+1}: Làm ca {', '.join(shifts_worked)}")
                 worked_today = True
            # else: # Chỉ in những ngày làm việc để gọn
            #     print(f"  Ngày {d+1}: Nghỉ")
        if not worked_today:
             print("  (Không làm ngày nào)")


else:
    print("\nKhông tìm thấy lịch trình khả thi nào đáp ứng tất cả các ràng buộc cứng.")