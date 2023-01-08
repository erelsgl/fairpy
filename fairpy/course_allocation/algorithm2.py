import copy
import math
from Course import Course
from Student import Student
from functools import cmp_to_key
import doctest
import logging
import threading
import concurrent.futures
WORKERS=4

logger = logging.getLogger(__name__)
console = logging.StreamHandler() 
logfile = logging.FileHandler("my_logger2.log", mode="w") 
logger.handlers = [console,logfile]
logfile.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: Line %(lineno)d: %(message)s'))

logger.setLevel(logging.DEBUG)
console.setLevel(logging.WARNING)

def csp_mapping(students:list[Student],courses:list[Course]):
    '''
    >>> a = Course(name='a', price=2.4, capacity=0, max_capacity=5)
    >>> b = Course(name='b', price=5, capacity=0, max_capacity=4)
    >>> c = Course(name='c', price=10.4, capacity=0, max_capacity=5)
    >>> courses = [a, b, c]
    >>> s1 = Student(name='s1', budget=18, year=1, courses=[], preferences=([c, b]))
    >>> s2 = Student(name='s2', budget=18, year=1, courses=[], preferences=([b, c, a]))
    >>> s3 = Student(name='s3', budget=18, year=1, courses=[], preferences=([b, a]))
    >>> s4 = Student(name='s4', budget=18, year=1, courses=[], preferences=([a, c]))
    >>> s5 = Student(name='s5', budget=18, year=1, courses=[], preferences=([a, b, c]))
    >>> s6 = Student(name='s6', budget=18, year=1, courses=[], preferences=([a, c, b]))
    >>> students = [s1, s2, s3, s4, s5, s6]
    >>> csp_mapping(students, courses)
    >>> [str(course) for course in courses]
    ['course name: a capacity 5/5 and priced 2.4', 'course name: b capacity 5/4 and priced 5', 'course name: c capacity 5/5 and priced 10.4']
    '''
    def get_course(s) -> bool:
        for preference in s.preferences:
            if (s.budget >= preference.price and 
                preference not in s.courses):
                s.courses.append(preference)
                s.budget = s.budget - preference.price
                preference.capacity += 1
                return True
        return False
    for course in courses:
        course.capacity = 0 
    while True:
        flag = False
        for student in students:
            if (len(student.preferences) >  len(student.courses)):
                if (get_course(student)):
                    flag = True
        if(not flag):
            break

def process_copy(student:Student, i):
    copy_student = copy.deepcopy(student)
    copy_student.preferences = []
    for pre in copy_student.preferences:
        copy_student.preferences.append(pre)
    return copy_student, i

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
    ## this section is for finding j_hat in line 1
    wow = []
    for s in students:
        a = copy.deepcopy(s)
        a.preferences = []
        for pre in s.preferences:
            a.preferences.append(pre)
        wow.append(a)
    flag = False
    # if(sorted([student.budget for student in students])[-1] < maximum):
    #     #the algorithm requires maximum to be less than maximum budget
    #     # maximum = sorted([student.budget for student in students])[-1]
    #     # logger.warning("maximum greater than max budget")
    logger.debug("%g is the greatest budget", sorted([student.budget for student in students])[-1])

    csp_mapping(wow, courses)
    J_hat = sorted(courses, key=cmp_to_key(Course.comperator))[-1]
    ##till here line 1 in algorithm 2
    while((J_hat.capacity-J_hat.max_capacity > 0 and not J_hat.mark) or (maximum-J_hat.price <= eps)): #2
        d_star = math.floor((J_hat.capacity-J_hat.max_capacity)/2) #3
        p_l = J_hat.price #4
        p_h = maximum #5
        logger.debug("low : %g", p_l)
        logger.debug("high : %g", p_h)
        while(True): #6
            J_hat.price = (p_l + p_h)/2 #7
            ##same here as above, for line 8 if section

            ### try with proccess pool

            wow = []
            for s in students:
                a = copy.deepcopy(s)
                a.preferences = []
                for pre in s.preferences:
                    a.preferences.append(pre)
                wow.append(a)   

            # stitch on the wound       
            # dict_to_sort = {}
            # with concurrent.futures.ProcessPoolExecutor(max_workers=WORKERS) as executor:
            #     futures = [executor.submit(process_copy, students[i], i) for i in range(len(students))] 
            #     for future in concurrent.futures.as_completed(futures):   # return each result as soon as it is completed:
            #         dict_to_sort[future.result()[0]] = future.result()[1]
            # sorteda = sorted(dict_to_sort.items(), key = lambda x:x[1])
            # wow = [b[0] for b in sorteda]
            # wow = []
            ### try with proccess pool

            csp_mapping(wow,courses) # mapping here after price changes
            if((J_hat.capacity-J_hat.max_capacity) >= d_star): #line 8
                p_l = J_hat.price #9
            else: #10
                p_h = J_hat.price #11
            if(p_h - p_l <= eps): #13
                J_hat.price = p_h #14
                J_hat.mark = True #14
                break #part of 13
        logger.debug("new price %g for course %s", J_hat.price, J_hat.name)
        J_hat = sorted(courses, key=cmp_to_key(Course.comperator))[-1] #15
        # if(J_hat.capacity <= J_hat.max_capacity or maximum-J_hat.price <= eps):
        #     return [c.price for c in courses]
    return [c.price for c in courses] #return at the end

if __name__=="__main__":
    import pytest
    pytest.main(args=["fairpy/course_allocation"])