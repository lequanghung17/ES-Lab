from ortools.sat.python import cp_model
import time

model = cp_model.CpModel()


slot_times = [
    "07:00-09:00", "09:00-11:00", "11:00-13:00", "13:00-15:00",
    "15:00-17:00", "17:00-19:00", "19:00-21:00", "21:00-24:00"
]
start = {}
end = {}
start[0] = 7*60
start[1] = 9*60
start[2] = 11*60
start[3] = 13*60
start[4] = 15*60
start[5] = 17*60
start[6] = 19*60
start[7] = 21*60
end[0] = 9*60
end[1] = 11*60
end[2] = 13*60
end[3] = 15*60
end[4] = 17*60
end[5] = 19*60
end[6] = 21*60
end[7] = 24*60

# start = {i: int(slot.split('-')[0].split(':')[0]) * 60 + int(slot.split('-')[0].split(':')[1]) for i, slot in enumerate(slot_times)}
# end = {i: int(slot.split('-')[1].split(':')[0]) * 60 + int(slot.split('-')[1].split(':')[1]) for i, slot in enumerate(slot_times)}
def mins(a):
    return end[a] - start[a]



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

Abs = {
    'emp1': ['0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '1'],
    'emp2': ['0', '0', '0', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0'],
    'emp3': ['0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0'],
    'emp4': ['0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0'],
    'emp5': ['0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1'],
    'emp6': ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0'],
    'emp7': ['1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0'],
    'emp8': ['1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '1', '1', '0', '0'],
    'emp9': ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0'],
    'emp10': ['1', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0'],
    'emp11': ['1', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0'],
    'emp12': ['0', '0', '1', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0'],
    'emp13': ['0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0'],
    'emp14': ['0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0'],
    'emp15': ['0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '1', '0', '1', '0', '1', '1', '0', '0', '0'],
    'emp16': ['1', '1', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0'],
    'emp17': ['1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0'],
    'emp18': ['0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
    'emp19': ['0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '1'],
    'emp20': ['0', '0', '1', '0', '0', '0', '0', '1', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0'],
    'emp21': ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '1', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '1'],
    'emp22': ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0'],
    'emp23': ['0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '1'],
    'emp24': ['0', '0', '0', '1', '0', '1', '0', '0', '1', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0'],
    'emp25': ['0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '1', '1', '0'],
    'emp26': ['0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0'],
    'emp27': ['1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0'],
    'emp28': ['0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0'],
    'emp29': ['0', '0', '1', '0', '0', '1', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '1', '1'],
    'emp30': ['0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '1', '0']
}

Per = 5
MaxD = 3
MaxWe = 4*60
MinWe = 2*60
MaxPe = 6*60
MinCe = 2*60
MaxCe = 5*60
MaxCWe = 7
MaxCRe = 5
We = 5000
WMem = 1000

E = employees             # danh sách nhân viên
D = days                 # 0 đến 30
S = slot_indices  # 0 đến 7
M = [1]    
MS = morning_slots       # ca sáng
AS = afternoon_slots     # ca chiều

wsd = {}
wd = {}
ms = {}
as_ = {}
wm = {}
w = {}


for e in E:
    w[e] = model.NewBoolVar(f"w_{e}") 
    for m in M:
        wm[e,m] = model.NewBoolVar(f"wm_{e}_{m}")
    for d in D:
        wd[e, d] = model.NewBoolVar(f"wd_{e}_{d}")
        ms[e, d] = model.NewBoolVar(f"ms_{e}_{d}")
        as_[e, d] = model.NewBoolVar(f"as_{e}_{d}")
        for s in S:
            wsd[e, s, d] = model.NewBoolVar(f"wsd_{e}_{s}_{d}")

cost = sum([We*w[e] for e in E] ) + sum([WMem*wm[e,m] for e in E for m in M])
model.Minimize(cost)
# cstr1
for s in S:
    for d in D:
        model.Add(sum([wsd[e, s, d] for e in E]) >= Req.get((d, s), 0))

# cstr2
for e in E:
    for s in S:
        for d in D:
            model.Add(wsd[e,s,d] <= wd[e,d])
            #model.AddImplication(wsd[e,s,d], wd[e,d])

# cstr3
for e in E:
    for m in M:
        for d in D:
            model.Add(wd[e, d] <= wm[e, m])
            #model.AddImplication(wd[e, d], wm[e, m])

# cstr4
for e in E:
    for m in M:
        model.Add(wm[e, m] <= w[e])
        #model.AddImplication(wm[e, m], w[e])

# cstr5
for e in E:
    for d in D:
        if Abs[e][d] == '1':
            model.Add(wd[e, d] == 0)

# cstr6,7

for e in E:
    for d in D:
        model.Add(ms[e, d] + as_[e, d] <= 1)
        for s in MS:
            model.Add(wsd[e, s, d] - ms[e, d] <= 0)
        for s in AS:
            model.Add(wsd[e, s, d] - as_[e, d] <= 0)

# cstr8
for e in E:
    for d in D:
        model.Add(ms[e,d] + as_[e,d]  <= 1)

# cstr9,10
for e in E: 
        for d_start in range(num_days - Per + 1):
                model.Add(sum([ms[e, d] - as_[e, d] for d in range(d_start, d_start+Per)]) <= MaxD)
                model.Add(sum([ms[e, d] - as_[e, d] for d in range(d_start, d_start+Per)]) >= -MaxD)


# cstr11
for e in E:
    for s1 in MS:
        for s2 in MS:
            if s1 < s2:
                for d in D:
                    if (end[s2] - start[s1]) > MaxPe:
                        model.Add(wsd[e, s1, d] + wsd[e, s2, d] <= 1)

#cstr12
for e in E:
    for s1 in AS:
        for s2 in AS:
            if s1 < s2:
                for d in D:
                    if (end[s2] - start[s1]) > MaxPe:
                        model.Add(wsd[e, s1, d] + wsd[e, s2, d] <= 1)


#cstr13
for e in E:
    for d in D:
        model.Add(sum(mins(s)*[wsd[e, s, d] for s in MS]) <= MaxWe)

#cstr14
for e in E:
    for d in D:
        model.Add(sum(mins(s)*[wsd[e, s, d] for s in AS]) <= MaxWe)

#cstr15
for e in E:
    for d in D:
        model.Add(sum(mins(s)*[wsd[e, s, d] for s in S]) >= MinWe*wd[e, d])

#cstr16
for e in E:
    for s1 in S:
        for s2 in S:
            for s3 in S:
                for d in D:

                    if end[s1] == start[s2] and end[s2] <= start[s3] and start[s3] - start[s2] < MinCe:
                        model.Add(wsd[e, s1, d] - wsd[e, s2, d] + wsd[e, s3, d] >= 0)
            

#cstr17
for e in E:
    max_consec_slots = MaxCe
    for d in days:
        for s in S:
            K_max = num_slots - s - 1
            for K in range(1, K_max + 1):
                if end[s + K_max - 1] - start[s] <= max_consec_slots < end[s+K_max] - start[s]:
                    window_vars = [wsd[e, s+k, d] for k in range(K+1)]
                    model.Add(sum(window_vars) <= max_consec_slots) 
            
#cstr18
for e in E:
    max_consec_work_days = MaxCWe
    for d_start in range(num_days - max_consec_work_days):
        window_vars = [wd[e, d] for d in range(d_start, d_start + max_consec_work_days + 1)]
        model.Add(sum(window_vars) <= max_consec_work_days)

#cstr19
for e in E:
    max_consec_rest_days = MaxCRe
    for d_start in range(num_days - max_consec_rest_days):
        window_vars = [wd[e, d] for d in range(d_start, d_start + max_consec_rest_days + 1)]
        # model.Add(sum(window_vars) >= 1) 
        model.AddBoolOr(window_vars) # biểu diễn logic OR bằng CP

# check KQ
def validate_solution(wsd, wd, ms, as_, w, wm, E, D, S, MS, AS, Req, Abs,
                      MinWe, MaxWe, MaxCWe, MaxCRe, MinCe, MaxCe, start, end):
    errors = []

    def mins(s):
        return end[s] - start[s]

    # Check yêu cầu yêu cầu slot
    for d in D:
        for s in S:
            assigned = sum(solver.Value(wsd[e, s, d])> 0.5 for e in E)
            required = Req.get((d, s), 0)
            if assigned < required:
                errors.append(f"Thiếu nhân sự cho slot {s} ngày {d+1}: cần {required}, có {assigned}")

    # Check vắng mặt
    for e in E:
        for d in D:
            if Abs[e][d] == '1' and solver.Value(wd[e, d]) > 0.5:
                errors.append(f"{e} làm việc trái với ngày vắng mặt (ngày {d+1})")

    # Check thời lượng ca sáng, chiều
    for e in E:
        for d in D:
            morning_work = sum(mins(s) * solver.Value(wsd[e, s, d]) for s in MS)
            if morning_work > MaxWe:
                errors.append(f"{e} làm quá giờ ca sáng (ngày {d+1})")
            afternoon_work = sum(mins(s) * solver.Value(wsd[e, s, d]) for s in AS)
            if afternoon_work > MaxWe:
                errors.append(f"{e} làm quá giờ ca chiều (ngày {d+1})")

    # Check thời lượng tối thiểu nếu có đi làm
    for e in E:
        for d in D:
            worked = solver.Value(wd[e, d]) > 0.5
            total = sum(mins(s) * solver.Value(wsd[e, s, d]) for s in S)
            if worked and total < MinWe:
                errors.append(f"{e} làm ít hơn tối thiểu trong ngày {d+1}")

    # Check tối đa số ngày làm liên tiếp
    for e in E:
        for d_start in range(len(D) - MaxCWe):
            days_worked = [solver.Value(wd[e, d]) > 0.5 for d in range(d_start, d_start + MaxCWe + 1)]
            if all(days_worked):
                errors.append(f"{e} làm việc quá {MaxCWe} ngày liên tiếp bắt đầu từ ngày {d_start+1}")

    # Check tối đa số ngày nghỉ liên tiếp (phải có ít nhất 1 ngày làm)
    for e in E:
        for d_start in range(len(D) - MaxCRe):
            days_worked = [solver.Value(wd[e, d]) > 0.5 for d in range(d_start, d_start + MaxCRe + 1)]
            if not any(days_worked):
                errors.append(f"{e} nghỉ quá {MaxCRe} ngày liên tiếp từ ngày {d_start+1}")

    # Check cách nhau giữa 3 ca quá gần (MinCe)
    for e in E:
        for d in D:
            for s1 in S:
                for s2 in S:
                    for s3 in S:
                        if end[s1] == start[s2] and end[s2] <= start[s3] and (start[s3] - start[s2] < MinCe):
                            v1 = solver.Value(wsd[e, s1, d])
                            v2 = solver.Value(wsd[e, s2, d])
                            v3 = solver.Value(wsd[e, s3, d])
                            if v1 > 0.5 and v2 > 0.5 and v3 > 0.5:
                                errors.append(f"{e} có 3 ca quá gần nhau (d{d+1}, slots {s1}, {s2}, {s3})")

    # Check số ca liên tiếp quá mức MaxCe
    for e in E:
        for d in D:
            for s in range(len(S) - MaxCe):
                window = [solver.Value(wsd[e, s + k, d]) > 0.5 for k in range(MaxCe + 1)]
                if all(window):
                    errors.append(f"{e} làm hơn {MaxCe} ca liên tiếp trong ngày {d+1} bắt đầu từ slot {s}")

    return errors

solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 60.0  # Optional timeout
start_time = time.time()  # Track solution time manually

status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print("Found a solution!")
    for e in E:
        for d in D:
            for s in S:
                if solver.Value(wsd[e, s, d]) == 1:
                    print(f"{e} làm việc ở slot {s} ngày {d+1}")
    
    print("Total cost:", solver.ObjectiveValue())
    print(f'Running time: {time.time() - start_time:.2f} seconds')
    errors = validate_solution(wsd, wd, ms, as_, w, wm, E, D, S, MS, AS, Req, Abs,
                               MinWe, MaxWe, MaxCWe, MaxCRe, MinCe, MaxCe, start, end)

    if not errors:
        print(" Lời giải hợp lệ với tất cả ràng buộc.")
    else:
        print(" Có lỗi trong lời giải:")
        for err in errors:
            print("-", err)
else:
    print("can't.")