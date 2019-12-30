from utils import *
from z3 import *
import numpy as np
import matplotlib.pyplot as plt
import itertools

sol = Optimize()

# The running time of job i is i+ 5, fori= 1,2, . . . ,12.

ilist = np.arange(1,13,dtype=int)
dur = ilist + 5

start = [Int(f's({i})') for i in ilist]
end = [s + int(d) for s, d in zip(start, dur)]

for s in start:
    sol.add(s >= 0)

job = lambda i: i - 1

# Job 3 may only start if jobs 1 and 2 have been finished.
# Job 5 may only start if jobs 3 and 4 have been finished.
# Job 7 may only start if jobs 3, 4 and 6 have been finished.
# Job 9 may only start if jobs 5 and 8 have been finished.
# Job 11 may only start if job 10 has been finished.
# Job 12 may only start if jobs 9 and 11 have been finished.

order = [
    (3, [1,2]),
    (5, [3,4]),
    (7, [3,4,6]),
    (11, [10]),
    (12, [9,11]),
]

for o, prereqs in order:
    for prereq in prereqs:
        sol.add(start[job(o)] >= end[job(prereq)])

# Job 8 may not start earlier than job 5.

sol.add(start[job(8)] >= start[job(5)])

# Jobs 5,7 en 10 require a special equipment of which only one copy is available, so no two of these jobs may run at the same time.

usesame = [5,7,10]

for j1, j2 in itertools.combinations(usesame, 2):
        sol.add(Or(end[job(j1)] <= start[job(j2)], end[job(j2)] <= start[job(j1)]))

z = Int('z')

for e in end:
    sol.add(e <= z)

sol.minimize(z)

num_solutions = 0
while sol.check() == sat:
    num_solutions += 1
    mod = sol.model()
    start = eval_it(mod, start)
    end = eval_it(mod, end)
    print('start:',start)
    print('  end:',end)

    print("z:", mod.eval(z))
    break
