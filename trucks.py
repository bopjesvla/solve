from utils import *
from z3 import *
import numpy as np

# pallets
amounts = [4, 10000, 8, 10, 20]
weights = [800, 1100, 1000, 2500, 200]
names = 'nuzzles prittles skipples crottles dupples'.split()

trucks = 8
pallets_per_truck = 8
cap = 8000
explosive = True

sol = Optimize()

z = Int("z")

def make_truck_amount(i, j):
    am = Int(f"x({i},{names[j]})")

    if names[j] == 'skipples' and i > 2:
        sol.add(am == 0)
    else:
        sol.add(am >= 0)
        if names[j] == 'nuzzles':
            sol.add(am <= 1)
    return am

x = np.array([[make_truck_amount(i, j) for j in range(len(amounts))] for i in range(trucks)])

for i in range(trucks):
    sol.add(Sum(x[i].tolist()) <= pallets_per_truck)
    sol.add(scalar_product(x[i].tolist(), weights) <= cap)
    if explosive:
        sol.add(Or(x[i,1] == 0, x[i,3] == 0))

for j in range(len(amounts)):
    if j != 1:
        sol.add(Sum(x[:,j].tolist()) == amounts[j])

sol.add(z == Sum(x[:,1].tolist()))

# objective
sol.maximize(z)

num_solutions = 0
while sol.check() == sat:
    num_solutions += 1
    mod = sol.model()
    matrix = np.vectorize(mod.eval)(x)
    print(matrix)
    print("z:", mod.eval(z))
    print()
    getGreaterSolution(sol,mod,z)

print()
print("num_solutions:", num_solutions)
