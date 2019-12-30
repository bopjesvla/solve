from utils import *
from z3 import *
import numpy as np
import matplotlib.pyplot as plt

sol = Optimize()

chip_w = 30
chip_h = 30

comps = [(4, 3), (4, 3), (4, 5), (4, 6), (5, 20), (6, 9), (6, 10),
         (6, 11), (7, 8), (7, 12), (10, 10), (10, 20)]
# comps = [(4,3), (3,2), (5,6), (8,8), (7,7)]

def create_dim(i, d1, d2):
    w = Int(f'w({i})')
    h = Int(f'h({i})')
    sol.add(Or(And(w == d1, h == d2), And(w == d2, h == d1)))
    return i, w, h

dims = [create_dim(i, d1, d2) for i, (d1, d2) in enumerate(comps)]

def create_pos(i, w, h):
    x = Int(f'x({i})')
    sol.add(x >= 0)
    sol.add(x <= chip_w - w)
    y = Int(f'y({i})')
    sol.add(y >= 0)
    sol.add(y <= chip_h - h)
    return x, y

pos = np.concatenate((dims, [create_pos(i, w, h) for i, w, h in dims]), 1)

for i1, w1, h1, x1, y1 in pos:
    for i2, w2, h2, x2, y2 in pos:
        if not (x1 is x2):
            sol.add(Or(x2 + w2 <= x1, x2 >= x1 + w1, y2 + h2 <= y1, y2 >= y1 + h1))
    if i1 >= 2:
        next_to_pow = [Or(
            And(x1 + w1 > xpow, x1 < xpow + wpow, Or(y1 == ypow + hpow, y1 + h1 == ypow)),
            And(y1 + h1 > ypow, y1 < ypow + hpow, Or(x1 == xpow + wpow, x1 + w1 == xpow))
            # And(x1 + w1 >= xpow, x1 <= xpow + wpow),
            # And(y1 + h1 >= ypow, y1 <= ypow + hpow)
        ) for ipow, wpow, hpow, xpow, ypow in pos[:2]]
        sol.add(Or(*next_to_pow))

ipc1, wpc1, hpc1, xpc1, ypc1 = pos[0]
ipc2, wpc2, hpc2, xpc2, ypc2 = pos[1]

z = Int('z')

sol.add(Or(
    xpc1 + wpc1 / 2 - (xpc2 + wpc2 / 2) >= z,
    ypc1 + hpc1 / 2 - (ypc2 + hpc2 / 2) >= z
))

sol.maximize(z)

num_solutions = 0
while sol.check() == sat:
    num_solutions += 1
    mod = sol.model()
    res = eval_it(mod, pos[:,1:])
    # matrix = np.vectorize(mod.eval)(grid)
    # res = [(mod.eval(x), mod.eval(y), mod.eval(w), mod.eval(h)) for (x,y), (w,h) in zip(pos, dims)]
    print(res)
    grid = np.zeros((chip_w, chip_h)) - 4

    for i, (w, h, x, y) in enumerate(res):
        print(x, y, w,h)
        grid[x:x+w,y:y+h] = i
    print("z:", mod.eval(z))
    print(grid)
    plt.imshow(grid.T)
    plt.show()
    break
