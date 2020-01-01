from z3 import *
import numpy as np

max_courses = 12

sol = Solver()

tonr = np.vectorize(IntVal)

nr = lambda: Int('v_' + str(np.random.random()))

# 50103 = 5th year, 1st class of 3rd subject

gemeen = 'nl en maat lo ckv anw'.split()
wi = ['wiA', 'wiB', 'wiC', 'wiD']
langs = ['fr', 'du', 'es']
extra = ['na', 'sk', 'bio', 'ec', 'gs', 'ak', 'bv', 'muziek', 'informatica']
all_courses = gemeen + wi + langs + extra

def generate_student():
    c = np.random.choice
    track = c(['nt', 'ng', 'em', 'cm'])

    lang2 = c(langs)
    lang3 = c([l for l in langs if l != lang2])

    if track == 'nt':
        courses = gemeen + [lang2, 'wiB', 'na', 'sk', c(['bio', 'wiD'])]
    elif track == 'ng':
        courses = gemeen + [lang2, c(['wiA', 'wiB']), 'bio', 'sk', c(['na', 'ak'])]
    elif track == 'em':
        courses = gemeen + [lang2, c(['wiA', 'wiB']), 'ec', 'gs', c(['ak', lang3])]
    elif track == 'cm':
        courses = gemeen + [lang2, c(['wiA', 'wiB', 'wiC']), 'gs', c(['ak', 'ec']), c(['bv', lang3])]

    year = c(list(range(6, 7)))
    courses += [c([e for e in extra if not e in courses + wi])]

    course_codes = np.array([all_courses.index(c) for c in courses])

    year_course_codes = course_codes + year * 10000

    return year_course_codes, course_codes, courses, year

print(len(all_courses), 'courses,', len(generate_student()[0]), 'per student')

# courses
# students = [[0,2],[1,3],[0,3], [4,5]]
students, codes, cnames, y = map(list, zip(*[generate_student() for i in range(30)]))

print(len(np.unique(students, axis=0)), 'unique course lists')

course_counts = dict(zip(*np.unique(students, return_counts=True)))

track_counts = []

profs = [[0,1], [2,3], [4,5], [4,5]]

def classes(course):
    return [course + 100 * class_ for class_ in range(course_counts[course] // 30 + 1)]

all_classes = [cl for course in np.unique(students) for cl in classes(course)]

# each class requires you to show up three times
class_blocks = 3

def create_time():
    v = nr()
    sol.add(v >= 0)
    sol.add(v <= 50)
    return v

class_times = [[create_time() for i in range(class_blocks)] for cl in all_classes]

for ct in class_times:
    sol.add(ct[1] >= ct[0])
    sol.add(ct[2] >= ct[1])

class_dict = dict(zip(all_classes, class_times))

class_size = 2

slots = list(range(7))

def choose_class(courses):
    v = [nr() for i in range(class_blocks)]

    sol.add(Or([And([stime == ctime for stime, ctime in zip(v, class_dict[cl])]) for c in courses for cl in classes(c)]))

    return v

# prof_class = [choose_class(p) for p in profs]

student_class = [[choose_class([c]) for c in s] for s in students]

for s in student_class:
    sol.add(Distinct([block for chosen_class in s for block in chosen_class]))

# student_times = [[ct for ct in class_times if ct[0] in s] for s in students]

choose_class()

# for c, t in zip(all_classes, class_times):
    # sol.add(Distinct(class_times))
    # for 

## check

num_solutions = 0
while sol.check() == sat:
    num_solutions += 1
    mod = sol.model()
    matrix = np.vectorize(mod.eval)(student_class)
    print(matrix)
    print()
    break

print()
print("num_solutions:", num_solutions)
