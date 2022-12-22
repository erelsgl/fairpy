#bad logic, should use in csp mapping the same student and courses from beginining
import copy
import math
from Course import Course
from Student import Student
from functools import cmp_to_key
import doctest



def csp_mapping(students:list[Student],courses:list[Course]):
    def get_course(s) -> bool:
        for i in range(0, len(s.preferences)):
            if (s.budget >= s.preferences[i].price):
                s.courses.append(s.preferences[i])
                s.budget = s.budget - s.preferences[i].price
                s.preferences[i].capacity += 1
                s.preferences.pop(i)
                return True
        return False
    for course in courses:
        course.capacity = 0 
    while True:
        flag = False
        for student in students:
            if (len(student.preferences) > 0):
                if (get_course(student)):
                    flag = True
        if(not flag):
            break

def algorithm2(price_vector:list[float], maximum:int, eps:float, csp_mapping:callable, students1, courses)->list[float]:
    wow = []
    for s in students1:
        a = copy.deepcopy(s)
        a.preferences = []
        for pre in s.preferences:
            a.preferences.append(pre)
        wow.append(a)
    csp_mapping(wow, courses)
    J_hat = sorted(courses, key=cmp_to_key(Course.comperator))[-1]
    while(J_hat.capacity-J_hat.max_capacity > 0 and not J_hat.mark):
        d_star = math.floor((J_hat.capacity-J_hat.max_capacity)/2)
        p_l = J_hat.price
        p_h = maximum
        while(True):
            J_hat.price = (p_l + p_h)/2
            wow = []
            for s in students1:
                a = copy.deepcopy(s)
                a.preferences = []
                for pre in s.preferences:
                    a.preferences.append(pre)
                wow.append(a)
            csp_mapping(wow,courses) # mapping here after price changes
            if((J_hat.capacity-J_hat.max_capacity) >= d_star):
                p_l = J_hat.price
            else:
                p_h = J_hat.price
            if(p_h - p_l <= eps):
                J_hat.price = p_h
                J_hat.mark = True
                break
        J_hat = sorted(courses, key=cmp_to_key(Course.comperator))[-1]
        if(J_hat.capacity <= J_hat.max_capacity or maximum-J_hat.price <= eps):
            return [c.price for c in courses]
    return [c.price for c in courses]

# a = Course(name='a', price=9, max_capacity=5)
# b = Course(name='b', price=2, max_capacity=3)
# c = Course(name='c', price=4.5, max_capacity=5)
# courses = [a, b, c]

# s1 = Student(name='s1', budget=15, courses=[] ,preferences=([c, b]))
# s2 = Student(name='s2', budget=15, courses=[] ,preferences=([b, c, a]))
# s3 = Student(name='s3', budget=15, courses=[] ,preferences=([b, a]))
# s4 = Student(name='s4', budget=15, courses=[] ,preferences=([a, c]))
# s5 = Student(name='s5', budget=15, courses=[] ,preferences=([a, b, c]))
# # s5 = Student(s4)

# students1 = [s1, s2, s3, s4, s5]

def check_this():
    a = Course(name='a', price=6, capacity=0, max_capacity=3)
    b = Course(name='b', price=4, capacity=0, max_capacity=3)
    c = Course(name='c', price=6, capacity=0, max_capacity=3)
    courses = [a, b, c]


    s1 = Student(name='s1', budget=10, courses=[], preferences=([a]))
    s2 = Student(name='s2', budget=10, courses=[], preferences=([b,a]))
    s3 = Student(name='s3', budget=10, courses=[], preferences=([c]))
    s4 = Student(name='s4', budget=10, courses=[], preferences=([c,b]))
    s5 = Student(name='s5', budget=10, courses=[], preferences=([c, a, b]))

    students = [s1, s2, s3, s4, s5]

    eps = 1
    maximum = 10
    price_vector = [6,4,6]
    print(algorithm2(price_vector, maximum, eps, csp_mapping, students, courses))

check_this()