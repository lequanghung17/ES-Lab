from pysat.solvers import Glucose3

def LapLichThi():
    subjects = ['A', 'B', 'C', 'D', 'E']
    num_sub = len(subjects)
    
    # Mã hóa ngày 
    def d1(m): return m * 3 + 1  
    def d2(m): return m * 3 + 2  
    def s(m): return m * 3 + 3   
    
    g = Glucose3()

    # Ràng buộc 1: Mỗi môn phải có một ngày hợp lệ (01, 10 hoặc 11)
    for m in range(num_sub):
        g.add_clause([d1(m), d2(m)])  

    # Ràng buộc 2: Một môn chỉ có một ca (sáng hoặc chiều)
    for m in range(num_sub):
        g.add_clause([s(m), -s(m)])  

    # Ràng buộc 3: Môn A và B không được thi cùng một ngày
    g.add_clause([-d1(0), -d1(1), d2(0), d2(1)])  # d1(A) ≠ d1(B) hoặc d2(A) ≠ d2(B)
    g.add_clause([d1(0), d1(1), -d2(0), -d2(1)])

    # Ràng buộc 4: Môn C chỉ được thi vào buổi sáng
    g.add_clause([-s(2)])  # s(C) = 0 (chỉ sáng)

    # # Ràng buộc 5: Không có hai môn nào thi cùng ca trong cùng một ngày
    # for i in range(num_sub):
    #     for j in range(i + 1, num_sub):
    #         g.add_clause([-d1(i), -d1(j), -d2(i), -d2(j), s(i), -s(j)])  
    #         g.add_clause([-d1(i), -d1(j), -d2(i), -d2(j), -s(i), s(j)])  
    

    if g.solve():
        model = g.get_model()
        schedule = {}

        for m in range(num_sub):
            day = 1 if (model[d1(m) - 1] <= 0 and model[d2(m) - 1] > 0) else \
                  2 if (model[d1(m) - 1] > 0 and model[d2(m) - 1] <= 0) else 3
            session = 'S' if model[s(m) - 1] <= 0 else 'C'
            schedule[subjects[m]] = (day, session)
        
        print("Lịch thi hợp lệ:")
        for subject, (day, session) in schedule.items():
            print(f"Môn {subject}: Ngày {day}, Ca {session}")
    else:
        print("Không có lịch thi hợp lệ.")


LapLichThi()
