# from ortools.sat.python import cp_model

# model = cp_model.CpModel()

# ws = {}
# wd = {}
# ms = {}
# as_ = {}

# for e in E:
#     for d in D:
#         wd[e, d] = model.NewBoolVar(f"wd_{e}_{d}")
#         ms[e, d] = model.NewBoolVar(f"ms_{e}_{d}")
#         as_[e, d] = model.NewBoolVar(f"as_{e}_{d}")
#         for s in S:
#             ws[e, s, d] = model.NewBoolVar(f"ws_{e}_{s}_{d}")

# # Ràng buộc 1
# for s in S:
#     for d in D:
#         model.Add(sum(ws[e, s, d] for e in E) >= Req[s, d])

# # Ràng buộc 2
# for e in E:
#     for s in S:
#         for d in D:
#             model.Add(ws[e, s, d] <= wd[e, d])

# # Ràng buộc 6 & 7
# for e in E:
#     for d in D:
#         model.Add(ms[e, d] + as_[e, d] <= 1)
#         for s in MS:
#             model.Add(ws[e, s, d] <= ms[e, d])
#         for s in AS:
#             model.Add(ws[e, s, d] <= as_[e, d])
