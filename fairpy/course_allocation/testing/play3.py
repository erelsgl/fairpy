from Course import Course
from Student import Student
import copy
a = Course(name='a', price=9, max_capacity=5)
b = Course(name='b', price=2, max_capacity=3)
c = Course(name='c', price=4.5, max_capacity=5)
s1 = Student(name='s1', budget=15, preferences=([c, b]))
s2 = Student(name='s2', budget=15, preferences=([b, c, a]))
s3 = Student(name='s3', budget=15, preferences=([b, a]))
s4 = Student(name='s4', budget=15, preferences=([a, c]))
s5 = Student(name='s5', budget=15, preferences=([a, b, c]))
courses = [a, b, c]
students = [s1, s2, s3, s4, s5]
wow = []
for s in students:
    a = copy.deepcopy(s)
    a.preferences = s.preferences[:]
    # for pre in s.preferences:
    #     a.preferences.append(pre)
    wow.append(a)

for i in range(len(students)):
    print((wow[i]))
    print((students[i]))