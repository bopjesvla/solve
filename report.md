---
title: |
    Solutions for the First Part \
    \vfill
    \large{Automated Reasoning}\
    Radboud University Nijmegen\
    October 2019
author:
    - Authored by Bob de Ruiter
header-includes:
    - \usepackage{float}
    - \usepackage{changepage}
    - \floatplacement{figure}{H}
---

\newpage

# Introduction

`z3py`, an interface to `z3`, was used to build the formulae in all exercises. Clauses are programmatically added to the outer conjunction with repeated calls to `solver.add`. The following utility functions are used throughout the document:

```python
def makeIntVar(sol, name, min_val, max_val):
    v = Int(name)
    sol.add(v >= min_val, v <= max_val)
    return v

def scalar_product(a,x):
    return Sum([ai*xi for ai,xi in zip(a,x)])

def eval_it(mod, it):
  return np.vectorize(lambda x: mod.eval(x).as_long())(np.array(it, dtype='object'))
```

# Solutions

The code is submitted along with this document. Non-boilerplate code is documented below. 

## 1

Amounts and weights are defined in the same order as their corresponding names:

```python
amounts = [4, 10000, 8, 10, 20]
weights = [800, 1100, 1000, 2500, 200]
names = 'nuzzles prittles skipples crottles dupples'.split()

trucks = 8
pallets_per_truck = 8
cap = 8000
explosive = False
```

Exercise 1 is an optimization task:

```python
sol = Optimize()

z = Int("z")

...

sol.maximize(z)
```

A m x n matrix X is introduced, where m is the number of trucks and n is the number of different products. X~ij~ encodes the amount of product j in truck i:

```python
x = np.array([[make_truck_amount(i, j) for j in range(len(amounts))]
             for i in range(trucks)])
```

An amount is an integer bounded by 0 and an optional maximum. This maximum is fixed to 1 if product j is nuzzles, to 0 if product j is skipples and truck i is not one of the cooling trucks:

```python
def make_truck_amount(i, j):
    am = Int(f"x({i},{names[j]})")

    if names[j] == 'skipples' and i > 2:
        sol.add(am == 0)
    else:
        sol.add(am >= 0)
        if names[j] == 'nuzzles':
            sol.add(am <= 1)
    return am
```

Each truck can have no more than 8 pallets weighing a total of 8000 kg. Additionally, if the explosive rule is in effect, a truck cannot have both prittles and crottles:

```python
for i in range(trucks):
    sol.add(Sum(x[i].tolist()) <= pallets_per_truck)
    sol.add(scalar_product2(sol, x[i].tolist(), weights) <= cap)
    if explosive:
        sol.add(Or(x[i,1] == 0, x[i,3] == 0))
```

For each product except for prittles, the maximum number of pallets should be on the trucks:

```python
for j in range(len(amounts)):
    if j != 1:
        sol.add(Sum(x[:,j].tolist()) == amounts[j])
```

The number of pallets of prittles should be maximized:

```python
sol.add(z == Sum(x[:,1].tolist()))

# objective
sol.maximize(z)
```

Optimize, get the model, get the values in matrix X, and get the number of pallets of prittles:

```python
while sol.check() == sat:
    ...
    mod = sol.model()
    matrix = np.vectorize(mod.eval)(x)
    print(matrix)
    print("z:", mod.eval(z))
```

Without the explosive rule, this returns:

```python
[[0 2 0 2 3]
 [1 3 1 1 2]
 [1 3 1 1 2]
 [1 1 6 0 0]
 [1 1 0 2 4]
 [0 7 0 0 1]
 [0 2 0 2 4]
 [0 2 0 2 4]]
z: 21
```

With the explosive rule, this returns:

```python
[[0 0 2 2 4]
 [1 0 1 2 4]
 [0 0 5 1 2]
 [1 6 0 0 1]
 [1 0 0 2 5]
 [0 7 0 0 1]
 [0 0 0 3 2]
 [1 6 0 0 1]]
z: 19
```

The maximum number of pallets of prittles decreases from 21 to 19 when the explosive rule is introduced.

## 2

I decided to immediately maximize the distance between centers:

```python
sol = Optimize()
```

The first two components are power components:

```python
chip_w = 30
chip_h = 30

comps = [(4, 3), (4, 3), (4, 5), (4, 6), (5, 20), (6, 9), (6, 10),
         (6, 11), (7, 8), (7, 12), (10, 10), (10, 20)]
```

Components can be rotated 90 degrees, meaning that either the width is set to the first component measurement and the height is set to the second, or the height is set to the first and the width is set to the second:

```python
def create_dim(i, d1, d2):
    w = Int(f'w({i})')
    h = Int(f'h({i})')
    sol.add(Or(And(w == d1, h == d2), And(w == d2, h == d1)))
    return i, w, h

dims = [create_dim(i, d1, d2) for i, (d1, d2) in enumerate(comps)]
```

Components should be positioned entirely on the grid. Coordinates encode the top left corner of the component in a top-left origin coordinate system:

```python
def create_pos(i, w, h):
    x = Int(f'x({i})')
    sol.add(x >= 0)
    sol.add(x <= chip_w - w)
    y = Int(f'y({i})')
    sol.add(y >= 0)
    sol.add(y <= chip_h - h)
    return x, y

pos = np.concatenate((dims, [create_pos(i, w, h) for i, w, h in dims]), 1)
```

Components cannot overlap. As such, for any non-duplicate pair of components, one of the following has to be true:

- The top of the component 1 (y1) is at least its height (h1) above the top of component 2 (y2)
- y2 is at least h2 above y1
- The left of the component 1 (x1) is at least its width (w1) to the left of the left of component 2 (x2)
- x2 is at least w2 to the left of x1

```python
for i1, w1, h1, x1, y1 in pos:
    for i2, w2, h2, x2, y2 in pos:
        if not (x1 is x2):
            sol.add(Or(x2 + w2 <= x1, x2 >= x1 + w1, y2 + h2 <= y1, y2 >= y1 + h1))
    ...
```

Each non-power component should be next to a power component, meaning that the non-power component and one power component either overlap on the x-axis and are right next to each other on the y-axis, or the other way around:

```python
for i1, w1, h1, x1, y1 in pos:
    ...
    if i1 >= 2:
        next_to_pow = [Or(
            And(x1 + w1 > xpow, x1 < xpow + wpow, Or(y1 == ypow + hpow, y1 + h1 == ypow)),
            And(y1 + h1 > ypow, y1 < ypow + hpow, Or(x1 == xpow + wpow, x1 + w1 == xpow))
        ) for ipow, wpow, hpow, xpow, ypow in pos[:2]]
        sol.add(Or(*next_to_pow))
```

Here, `pos[:2]` holds the positions of the power components. The outermost `Or(*...)` makes sure that at least one of the clauses in `next_to_pow` is true. That is, the non-power component is next to at least one power component.

Maximize the maximum of the horizontal and the vertical difference in power component centers:

```python
ipc1, wpc1, hpc1, xpc1, ypc1 = pos[0]
ipc2, wpc2, hpc2, xpc2, ypc2 = pos[1]

sol.add(Or(
    xpc1 + wpc1 / 2 - (xpc2 + wpc2 / 2) >= z,
    ypc1 + hpc1 / 2 - (ypc2 + hpc2 / 2) >= z
))

sol.maximize(z)
```

![Plot of resulting layout](Figure_1.png)

This yields a distance between centers of 18.

Plotting the layout:

```python
grid = np.zeros((chip_w, chip_h)) - 4

for i, (w, h, x, y) in enumerate(res):
    print(x, y, w,h)
    grid[x:x+w,y:y+h] = i
print("z:", mod.eval(z))
print(grid)
plt.imshow(grid.T)
plt.show()
```

## 3

Initializing the variables for start times, as well as the helper variables for end times:

```python
ilist = np.arange(1,13,dtype=int)
dur = ilist + 5

start = [Int(f's({i})') for i in ilist]
end = [s + int(d) for s, d in zip(start, dur)]

for s in start:
    sol.add(s >= 0)
```

A helper function for the one-indexed job list:

```python
job = lambda i: i - 1
```

(job, prerequisites) tuples:

```python
order = [
    (3, [1,2]),
    (5, [3,4]),
    (7, [3,4,6]),
    (11, [10]),
    (12, [9,11]),
]
```

A job should start only after each prerequisite has ended:

```python
for o, prereqs in order:
    for prereq in prereqs:
        sol.add(start[job(o)] >= end[job(prereq)])
```

Job 8 should not start before job 5 started:

```python
sol.add(start[job(8)] >= start[job(5)])
```

Jobs 5,7 en 10 require a special equipment of which only one copy is available, so no two of these jobs may run at the same time. As such, for each unique pair of jobs, one should end before the other starts.

```python
usesame = [5,7,10]

for j1, j2 in itertools.combinations(usesame, 2):
        sol.add(Or(end[job(j1)] <= start[job(j2)], end[job(j2)] <= start[job(j1)]))
```

Minimize the maximum of all job end times:

```python
z = Int('z')

for e in end:
    sol.add(e <= z)

sol.minimize(z)
```

Print results:

```python
mod = sol.model()
start = eval_it(mod, start)
end = eval_it(mod, end)
print('start:',start)
print('  end:',end)

print("z:", mod.eval(z))
```

Output:

```python
start: [ 0  0  7  0 27  0 15 27  0  0 15 31]
  end: [ 6  7 15  9 37 11 27 40 14 15 31 48]
z: 48
```

In the first line, the start times of the jobs are shown in order. The final job finishes at t=48.

## 4

We solve the problem for different values of n:

```python
for n in range(1,10):
    ...
```

Initialize given variables:

```python
    sol = Solver()

    ilist = np.arange(1,11)
    astart = IntVal(1)
    bstart = IntVal(1)
```

A helper variable is defined to keep track of which `if` branch is chosen:

```python
    branches = [Bool(f'branch({i})') for i in ilist]
```

Generate a list of variables. a[0] is the initial value of a, a[i] is a after step i. The same holds for b.

```python
    alist = [astart] + [Int(f'a({i})') for i in ilist]
    blist = [bstart] + [Int(f'b({i})') for i in ilist]
```

The loop body:

```python
    for i in ilist:
        sol.add(Or(
            And(
                alist[i] == alist[i-1] + 2 * blist[i-1],
                blist[i] == blist[i-1] + int(i),
                branches[i-1]
            ),
            And(
                blist[i] == alist[i-1] + blist[i-1],
                alist[i] == alist[i-1] + int(i),
                Not(branches[i-1])
            )
        ))
```

Here, the `Or` clause represents the branch on the if statement, while the `And` clause holds the actual assignments.

```python
    sol.add(blist[-1] == 600 + n)

    num_solutions = 0
    while sol.check() == sat:
        num_solutions += 1
        mod = sol.model()
        a = eval_it(mod, alist)
        b = eval_it(mod, blist)
        print('a:',a)
        print('b:',b)
        print('branches', np.vectorize(mod.eval)(branches))

        break
```

The output:

```python
a: [   1    3    5   15   19   24  108  115  427  436 1618]
b: [  1   2   5   8  23  42  48 156 164 591 601]
branches [True False True False False True False True False True]
a: [  1   2   4  12  26  31  37  44 254 480 490]
b: [  1   2   4   7  11  37  68 105 113 122 602]
branches [False False True True False False False True True False]
a: [  1   2   4  12  16  21  91 173 269 278 288]
b: [  1   2   4   7  19  35  41  48  56 325 603]
branches [False False True False False True True True False False]
a: [   1    2    6   14   28   33  111  118  430  439 1627]
b: [  1   2   4   7  11  39  45 156 164 594 604]
branches [False True True True False True False True False True]
a: [  1   2   6  14  28  50  82 126 134 444 454]
b: [  1   2   4   7  11  16  22  29 155 164 608]
branches [False True True True True True True False True False]
a: [  1   2   4  12  16  21  27 139 265 274 284]
b: [  1   2   4   7  19  35  56  63  71 336 610]
branches [False False True False False False True True False False]
```

This shows the program is unsafe for n = 1, 2, 4, 8, 10 and therefore safe for n = 3, 5, 6, 7, 9. `branches` shows what the question mark should be in each iteration in order to obtain the unsafe value. For example, the path for n=10 is `[False False True False False False True True False False]`.
