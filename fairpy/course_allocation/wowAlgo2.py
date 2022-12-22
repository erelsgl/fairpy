#bad logic, should use in csp mapping the same student and courses from beginining
import copy
import math
from Course import Course
from Student import Student
from functools import cmp_to_key
import doctest


a = Course(name='a', price=9, max_capacity=5)
b = Course(name='b', price=2, max_capacity=3)
c = Course(name='c', price=4.5, max_capacity=5)
courses = [a, b, c]



def csp_mapping():
    s1 = Student(name='s1', budget=15, courses=[] ,preferences=([c, b]))
    s2 = Student(name='s2', budget=15, courses=[] ,preferences=([b, c, a]))
    s3 = Student(name='s3', budget=15, courses=[] ,preferences=([b, a]))
    s4 = Student(name='s4', budget=15, courses=[] ,preferences=([a, c]))
    s5 = Student(name='s5', budget=15, courses=[] ,preferences=([a, b, c]))
    students = [s1, s2, s3, s4, s5]
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
    # return {course.name: course.capacity for course in courses}

def algorithm2(price_vector:list[float], maximum:int, eps:float, csp_mapping:callable)->list[float]:
    csp_mapping()
    J_hat = sorted(courses, key=cmp_to_key(Course.comperator))[-1]
    while(J_hat.capacity-J_hat.max_capacity > 0):
        d_star = math.floor((J_hat.capacity-J_hat.max_capacity)/2)
        p_l = J_hat.price
        p_h = maximum
        while(True):
            J_hat.price = (p_l + p_h)/2
            csp_mapping() # mapping here after price changes
            if((J_hat.capacity-J_hat.max_capacity) >= d_star):
                p_l = J_hat.price
            else:
                p_h = J_hat.price
            if(p_h - p_l <= eps):
                J_hat.price = p_h
                break
        J_hat = sorted(courses, key=cmp_to_key(Course.comperator))[-1]
        if(J_hat.capacity <= J_hat.max_capacity):
            return [c.price for c in courses]
    return [c.price for c in courses]

eps = 1
maximum = 10
price_vector = [9,2,4.5]

print(algorithm2(price_vector, maximum, eps, csp_mapping))
