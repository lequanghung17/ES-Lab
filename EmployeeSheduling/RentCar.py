from pysat.solvers import Glucose3
from pysat.card import CardEnc
from itertools import combinations
from pysat.formula import IDPool
import random


var_count = 0
employees = 0
days = 0
morning_shifts = 0
afternoon_shifts = 0
shifts = 0

# 1 Đảm bảo yêu cầu làm việc
def shift_requirement_constraint(wsd, requirements):
    global var_count
    vpools = IDPool(start_from=var_count + 1)   
    clauses = []
    for d in range(days):
        for s in range(shifts):
            req = requirements[d][s]  # Required number of employees for shift s on day d
            shift_vars = [wsd[d][s][e] for e in range(employees)]  # Get all employees for shift s on day d
            
            if req >= 0:
                # At least 'req' employees must be assigned
                cnf = CardEnc.atleast(lits=shift_vars, bound=req, encoding=1,vpool=vpools)
                var_count += cnf.nv
                clauses.extend(cnf.clauses)
    
    return clauses
# 2 Kích hoạt biến làm việc
def work_variable_constraint(wsd, wd):
    clauses = []
    for e in range(employees):
        for d in range(days):
            for s in range(shifts):
                clauses.append([-wsd[d][s][e], wd[d][e]])
    return clauses

# 3 Nếu nhân viên abs trong ngày thì nhân viên đấy không làm việc
def absence_constraint(wd, absences):
    #global num_employees, num_days
    clauses = []
    for e in range (employees):
        for d in range (days):
            if(absences[e][d]):
                clauses.append([-wd[d][e]])
    return clauses


# 4 Phân loại 2 ca sáng và chiều
def shift_type_constraint(wsd, wms, was):
    #global num_employees, num_days, num_morning_shifts, num_afternoon_shifts
    clauses = []
    for e in range (employees):
        for d in range (days):
            for s in range(morning_shifts):
                clauses.append([-wsd[d][s][e],wms[d][e]])
    for e in range (employees):
        for d in range (days):
            for s in range(morning_shifts,shifts):
                clauses.append([-wsd[d][s][e],was[d][e]])
    return clauses


# 5 Chỉ cho phép làm 1 ca (sáng/chiều) mỗi ngày
def one_shift_constraint(wms, was):
    clauses = []
    for e in range(employees):
        for d in range(days):
            clauses.append([-wms[d][e],-was[d][e]])
    return clauses

#6 cân bằng ca sáng chiều
def shift_balance_constraint(wms, was , per, max_d):
    global var_count
    vpools = IDPool(start_from=var_count + 1)   
    clauses = []
    for d in range(days - per + 1):
        for e in range(employees):
            morning_shifts = [wms[d + k][e] for k in range(per)]
            afternoon_shifts = [was[d + k][e] for k in range(per)]
            # Ràng buộc tổng ca sáng <= tổng ca chiều + max_d
            cnf = CardEnc.atmost(lits=afternoon_shifts + [-m for m in morning_shifts], bound=max_d + per, encoding=1,vpool=vpools)
            var_count += cnf.nv
            clauses.extend(cnf.clauses)
            # Ràng buộc tổng ca sáng >= tổng ca chiều - max_d
            cnf = CardEnc.atmost(lits=morning_shifts + [-a for a in afternoon_shifts], bound=max_d + per, encoding=1,vpool=vpools)
            var_count += cnf.nv
            clauses.extend(cnf.clauses)
    return clauses
#6 cân bằng ca sáng chiều
def shift_balance_constraint(wms, was , per, max_d):
    global var_count
    clauses = []
     

# 7 Giới hạn thời gian làm việc/ngày
def max_work_constraint(wsd, max_we):
    clauses = []
    for e in range(employees):
        for d in range(days):
            shifts = [wsd[d][s][e] for s in range(shifts)]
            
            # Tổng số ca trong ngày không vượt quá max_we
            for subset in combinations(shifts, max_we + 1):
                clauses.append([-s for s in subset])
    return clauses

# 8 Đảm bảo làm việc đủ liên tục
def min_continuous_shift_constraint(wsd, min_ce):
    clauses = []
    for e in range(employees):
        for d in range(days):
            for s1 in range(shifts - 1):  # s1 s2 liên tiếp
                s2 = s1 + 1 # s2 = s1 + 1
                clauses.append([-wsd[d][0][e], wsd[d][1][e]])
                clauses.append([-wsd[d][morning_shifts][e],wsd[d][morning_shifts+1][e]])
                for s3 in range(s2 + 1, min(s2 + min_ce, shifts)):  # nếu s3-s2 <mince
                    clauses.append([wsd[d][s1][e], -wsd[d][s2][e], wsd[d][s3][e]])
    return clauses

# 9 Đảm bảo làm việc liên tục không quá nhiều
def max_continuous_shift_constraint(wsd, max_ce):
    clauses = []
    for e in range(employees):
        for d in range(days):
            for s in range(shifts - max_ce):  # Ensure we have enough shifts to check max_ce + 1
                clause = [-wsd[d][s + k][e] for k in range(max_ce + 1)]
                clauses.append(clause)
    return clauses

# 10 Đảm bảo số ngày làm việc liên tiếp
def max_continuous_work_constraint(wd, max_cwe):
    clauses = []
    for e in range(employees):
        for d in range(days - max_cwe):
            clause = [-wd[d + k][e] for k in range(max_cwe + 1)]
            clauses.append(clause)
    return clauses

#11 Đảm bảo số ngày nghỉ liên tiếp
def max_continuous_rest_constraint(wd, max_cre):
    clauses = []
    for e in range(employees):
        for d in range(days - max_cre):
            clause = [wd[d + k][e] for k in range(max_cre + 1)]
            clauses.append(clause)
    return clauses
