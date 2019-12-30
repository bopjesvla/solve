from z3 import *
import numpy as np

courses = 6
max_courses = 3

sol = Optimize()

tonr = np.vectorize(IntVal)

# courses
students = tonr([[0,2],[1,3],[0,3], [4,5]])

profs = [[0,1], [2,3], [4,5], [4,5]]

course_classes = 3

class_max = course_classes * 100

classes = [course + offset for offset in range(0, class_max, 100) for course in np.unique(profs)]

class_size = 2

slots = list(range(7))

nr = lambda: Int('v_' + str(np.random.random()))

def choose_class(courses):
    v = nr()

    sol.add(Or([v == c + class_ for class_ in range(0, class_max, 100) for c in courses]))

# prof_class = [choose_class(p) for p in profs]

student_class = [[choose_class([c]) for c in s] for s in students]

def create_time():
    v = nr()
    sol.add(nr >= 0)
    sol.add(nr <= 6)

# 3 classes a day
class_times = [[create_time() for i in range(3)] for c in classes]

for c, t in zip(classes, class_times):
    sol.add(Distinct(class_times))
