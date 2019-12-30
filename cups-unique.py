from z3 import *
import numpy as np

sol = Solver()
# sol = Optimize()

nrcups = 7
bound = 7

x = np.array([[Real(f"x({t},{c})") for c in range(nrcups)] for t in range(bound)])

# largerm = x.copy()[:-1]

for v_init in x[0,:-1]:
    sol.add(v_init == 2)

sol.add(x[0,-1] == 4)

for t in range(bound):
    s = x[t]
    sol.add(Sum(*s) == 16)
    if t < bound - 1:
        if t == 0:
            m1,m2,m3 = (4,2,2)
        else:
            m1,m2,m3 = Reals(f"m{t}_1 m{t}_2 m{t}_3")

            for v in s:
                sol.add(m1 >= v)
                sol.add((m2 >= v) != (m1 == v))
                sol.add((m3 >= v) != (m2 <= v))

            sol.add(Sum([If(m1 == v, 1, 0) for v in s]) == 1)
            sol.add(Sum([If(m2 == v, 1, 0) for v in s]) == 1)

            # sol.add(PbEq([(m1 == v, 1) for v in s], 1))
            # sol.add(PbEq([(m2 == v, 1) for v in s], 1))


        for i in range(nrcups):
            vc = x[t][i]
            vn = x[t+1][i]
            # larger = Sum([If(v > vc, 1., 0.) for v in s[:i]] + [If(v >= vc, 1., 0.) for v in s[i+1:]])
            sol.add(Implies(vc == m1, vn >= vc - If(m2 - m3 < 1, 2, 1)))
            sol.add(Implies(vc == m2, vn >= vc - If(m2 - m3 < 1, 0, 1)))
            sol.add(Implies(vc < m2, vn >= vc))

# objective
# sol.add(x[5][0] == 6)
sol.add(x[-1][0] > 7)

# z = x[-1][0]
# sol.maximize(z)

def toSMT2Benchmark(f, status="unknown", name="benchmark", logic=""):
    v = (Ast * 0)()
    return Z3_benchmark_to_smtlib_string(f.ctx_ref(), name, logic, status, "", 0, v, f.as_ast())

num_solutions = 0
while sol.check() == sat:
    num_solutions += 1
    mod = sol.model()
    matrix = np.vectorize(mod.eval)(x)
    # lmatrix = np.vectorize(mod.eval)(largerm)
    print(matrix)
    # print(lmatrix)
    break
if num_solutions == 0:
    print('nope')
