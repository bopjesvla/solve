import numpy as np
from mip import *

m = Model(sense=MAXIMIZE)

nrcups = 7
bound = 8

x = np.array([[m.add_var(lb=0, ub=8) if t != 0 else (2 if c != 6 else 4) for c in range(nrcups)] for t in range(bound)])

largerm = x.copy()[:-1]

for t in range(bound):
    s = x[t]
    m += xsum(s) == 16
    if t < bound - 1:
        m2 = m.add_var(lb=0, ub=8)
        m3 = m.add_var(lb=0, ub=8)
        for i in range(nrcups):
            vc = x[t][i]
            vn = x[t+1][i]
            larger = xsum([v >= vc for v in s[:i]] + [v >= vc for v in s[i+1:]])
            largerm[t][i] = larger
            m += (larger != 0) + vn >= vc - 1. - (m2 - m3 <= 1) >= 1
            m += (larger != 1) + (m2 == vc) >= 1
            m += (larger != 1) + vn >= vc - (m2 - m3 <= 1)
            m += (larger != 2) + (m3 == vc) >= 1
            m += (larger == 0) + (larger == 1) + (vn >= vc) >= 1

            # sol.add(Implies(larger == 0., If(m2 - m3 < 1., vn >= vc - 2., vn >= vc - 1.)))
            # sol.add(Implies(larger == 1., And(m2 == vc, If(m2 - m3 < 1., vn >= vc, vn >= vc - 1.))))
            # sol.add(Implies(larger == 2., m3 == vc))
            # sol.add(Implies(larger >= 2., vn >= vc))

m.objective = (x[-5][0] >= 8)

status = m.optimize(max_seconds=300)

res = [[v.x for v in s] for s in x[1:]]
print(res)
