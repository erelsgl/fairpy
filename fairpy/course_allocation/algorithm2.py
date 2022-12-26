import copy
import math
from Course import Course
from Student import Student
from functools import cmp_to_key
import doctest


def csp_mapping(students:list[Student],courses:list[Course]):
    def get_course(s) -> bool:
        for i in range(0, len(s.preferences)):
            if (s.budget >= s.preferences[i].price and 
                    s.preferences[i] not in s.courses):
                s.courses.append(s.preferences[i])
                s.budget = s.budget - s.preferences[i].price
                s.preferences[i].capacity += 1
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


def algorithm2(price_vector:list[float], maximum:int, eps:float, csp_mapping:callable, students, courses)->list[float]:
    '''
    Iterative oversubscription elimination algorithm, 
    reducing by half the excess demand of the most oversubscribed course with each pass,
    :param price_vector: given price vector 
    :param maximum: suprimum for the price
    :param eps: error tolerance
    :param csp_mapping: function to mapping students to courses
    :param students: students list
    :param courses: list of courses
    :return: price vector to prevent oversubscription
    >>> a = Course(name='a', price=6, capacity=0, max_capacity=3)
    >>> b = Course(name='b', price=4, capacity=0, max_capacity=3)
    >>> c = Course(name='c', price=6, capacity=0, max_capacity=3)
    >>> courses = [a, b, c]
    >>> s1 = Student(name='s1', budget=10, courses=[], preferences=([a]))
    >>> s2 = Student(name='s2', budget=10, courses=[], preferences=([b,a]))
    >>> s3 = Student(name='s3', budget=10, courses=[], preferences=([c]))
    >>> s4 = Student(name='s4', budget=10, courses=[], preferences=([c,b]))
    >>> s5 = Student(name='s5', budget=10, courses=[], preferences=([c, a, b]))
    >>> students = [s1, s2, s3, s4, s5]
    >>> eps = 1
    >>> maximum = 10
    >>> price_vector = [6,4,6]
    >>> algorithm2(price_vector, maximum, eps, csp_mapping, students, courses)
    [6, 4, 6]
    '''
    wow = []
    for s in students:
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
            for s in students:
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


def test1(): 
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
    
    eps = 1
    maximum = 10
    price_vector = [9,2,4.5]
    assert algorithm2(price_vector, maximum, eps, csp_mapping, students, courses) == [9,10,4.5]

def test2(): 
    a = Course(name='a', price=2.4, capacity=0, max_capacity=5)
    b = Course(name='b', price=5, capacity=0, max_capacity=4)
    c = Course(name='c', price=10.4, capacity=0, max_capacity=5)
    courses = [a, b, c]


    s1 = Student(name='s1', budget=18, year=1, courses=[], preferences=([c, b]))
    s2 = Student(name='s2', budget=18, year=1, courses=[], preferences=([b, c, a]))
    s3 = Student(name='s3', budget=18, year=1, courses=[], preferences=([b, a]))
    s4 = Student(name='s4', budget=18, year=1, courses=[], preferences=([a, c]))
    s5 = Student(name='s5', budget=18, year=1, courses=[], preferences=([a, b, c]))
    s6 = Student(name='s6', budget=18, year=1, courses=[], preferences=([a, c, b]))
    students = [s1, s2, s3, s4, s5, s6]
    eps = 1
    maximum = 10
    price_vector = [2.4,5,10.4]
    assert algorithm2(price_vector, maximum, eps, csp_mapping, students, courses) == [2.4,8.125,10.4]


def test3():
    a = Course(name='a', price=3, max_capacity=5)
    b = Course(name='b', price=4, max_capacity=3)
    c = Course(name='c', price=3, max_capacity=5)
    courses = [a, b, c]
    s1 = Student(name='s1', budget=10, preferences=([c, b]))
    s2 = Student(name='s2', budget=10, preferences=([b, c, a]))
    s3 = Student(name='s3', budget=10, preferences=([b, a]))
    s4 = Student(name='s4', budget=10, preferences=([a, b, c]))
    s5 = Student(name='s5', budget=10, preferences=([a, b, c]))
    students = [s1, s2, s3, s4, s5]
    eps = 0.1
    maximum = 6
    price_vector = [3,4,3]
    assert(algorithm2(price_vector, maximum, eps, csp_mapping, students, courses)==[3,6,3])