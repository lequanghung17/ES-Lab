import random


num_employees = 30 
month = 1
num_days = 31  
time_slots = ['07:00-09:00', '09:00-11:00', '11:00-13:00', 
              '13:00-15:00', '15:00-17:00', '17:00-19:00', 
              '19:00-21:00', '21:00-24:00']
num_slots = len(time_slots)  


employees = []
for e in range(num_employees):
    num_abs_days = random.randint(4, 8)
    # Chọn ngẫu nhiên các ngày nghỉ
    abs_days = random.sample(range(num_days), num_abs_days)
    # Tạo chuỗi nhị phân 0-1 cho ngày nghỉ
    abs_binary = ['1' if i in abs_days else '0' for i in range(num_days)]
    
    employee = {
    
        'Abs': abs_binary  # Chuỗi nhị phân thể hiện ngày nghỉ (1: nghỉ, 0: làm)
    }
    employees.append(employee)

Reqs = {}
for d in range(1, num_days + 1): 
    for s in time_slots:  
        Reqs[(s, d)] = random.randint(1, 3)  


print("Thông tin yêu cầu số nhân viên cho mỗi ca mỗi ngày (Reqs,d):")
for d in range(1, num_days + 1):
    print(f"Ngày {d}:")
    for s in time_slots:
        print(f"  {s}: {Reqs[(s, d)]} nhân viên")

print("\nThông tin nhân viên:")
for e in range(num_employees):
    print(f"emp {e + 1}: {employees[e]}")
