# from docplex.cp.model import CpoModel

# mdl = CpoModel()

# ws = {(e, s, d): mdl.binary_var(name=f"ws_{e}_{s}_{d}") for e in E for s in S for d in D}
# wd = {(e, d): mdl.binary_var(name=f"wd_{e}_{d}") for e in E for d in D}
# ms = {(e, d): mdl.binary_var(name=f"ms_{e}_{d}") for e in E for d in D}
# as_ = {(e, d): mdl.binary_var(name=f"as_{e}_{d}") for e in E for d in D}

# # Ràng buộc 1
# for s in S:
#     for d in D:
#         mdl.add(mdl.sum(ws[e, s, d] for e in E) >= Req[s, d])

# # Ràng buộc 2
# for e in E:
#     for s in S:
#         for d in D:
#             mdl.add(ws[e, s, d] <= wd[e, d])

# # Ràng buộc 6 & 7
# for e in E:
#     for d in D:
#         mdl.add(ms[e, d] + as_[e, d] <= 1)
#         for s in MS:
#             mdl.add(ws[e, s, d] <= ms[e, d])
#         for s in AS:
#             mdl.add(ws[e, s, d] <= as_[e, d])

# # Ràng buộc 5: vắng mặt
# for (e, d), absent in Abse.items():
#     if absent:
#         mdl.add(wd[e, d] == 0)
