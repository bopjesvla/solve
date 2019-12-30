from z3 import *
import numpy as np

sol = Solver()
# sol = Optimize()

nrcups = 7
bound = 7

x = np.array([[Real(f"x({t},{c})") for c in range(nrcups)] for t in range(bound)])

largerm = x.copy()[:-1]

for v_init in x[0,:-1]:
    sol.add(v_init == 2.)

sol.add(x[0,-1] == 4.)

for t in range(bound):
    s = x[t]
    sol.add(Sum(*s) == 16)
    if t < bound - 1:
        m2,m3 = Reals(f"m{t}_2 m{t}_3")
        for i in range(nrcups):
            vc = x[t][i]
            vn = x[t+1][i]
            larger = Sum([If(v > vc, 1., 0.) for v in s[:i]] + [If(v >= vc, 1., 0.) for v in s[i+1:]])
            largerm[t][i] = larger

            sol.add(Implies(larger == 0., vn >= vc - If(m2 - m3 < 1, 2, 1)))
            sol.add(Implies(larger == 1., And(m2 == vc, vn >= vc - If(m2 - m3 < 1, 0, 1))))
            sol.add(Implies(larger == 2., m3 == vc))
            sol.add(Implies(larger >= 2., vn >= vc))

# objective
# sol.add(x[5][0] == 6)
sol.add(x[-1][0] > 8)

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
