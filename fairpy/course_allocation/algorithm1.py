'''
Heuristic search algorithm through price space, originally developed in Othman et al. 2010
designed to give each student a fixed budget at first and try find the must corresponding
price vector to approximate competitive equilibrium with lowest clearing error.
programmers : Aviv Danino & Ori Ariel
'''


from Course import Course
from Student import Student
from functools import cmp_to_key
from TabuList import TabuList 
import numpy as np
import time
import random
import copy
import doctest
import logging


logger = logging.getLogger(__name__)
console = logging.StreamHandler() 
logfile = logging.FileHandler("my_logger1.log", mode="w") 
logger.handlers = [console,logfile]
logfile.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: Line %(lineno)d: %(message)s'))

logger.setLevel(logging.DEBUG)
console.setLevel(logging.INFO)

def reset_update_prices(price_vector, courses):
    '''
    reset prices of courses and capacity
    >>> a = Course(name='a', price=0, max_capacity=5)
    >>> b = Course(name='b', price=0, max_capacity=3)
    >>> c = Course(name='c', price=0, max_capacity=5)
    >>> courses = [a, b, c]

    >>> s1 = Student(name='s1', budget=15, preferences=([c, b]))
    >>> s2 = Student(name='s2', budget=15, preferences=([b, c, a]))
    >>> s3 = Student(name='s3', budget=15, preferences=([b, a]))
    >>> s4 = Student(name='s4', budget=15, preferences=([a, c]))
    >>> s5 = Student(name='s5', budget=15, preferences=([a, b, c]))
    >>> students = [s1, s2, s3, s4, s5]
    >>> max_budget = 15
    >>> reset_update_prices([7,8,9], courses)
    >>> [course.capacity for course in courses]
    [0, 0, 0]
    >>> [course.price for course in courses]
    [7, 8, 9]
    '''
    i = 0 
    for course in courses:
        course.capacity = 0 
        course.price = price_vector[i]
        i += 1

def reset_students(students, max_budget: float):
    '''
    reset budget and courses for students
    >>> a = Course(name='a', price=0, max_capacity=5)
    >>> b = Course(name='b', price=0, max_capacity=3)
    >>> c = Course(name='c', price=0, max_capacity=5)
    >>> courses = [a, b, c]

    >>> s1 = Student(name='s1', budget=0, preferences=([c, b]))
    >>> s2 = Student(name='s2', budget=0, preferences=([b, c, a]))
    >>> s3 = Student(name='s3', budget=0, preferences=([b, a]))
    >>> s4 = Student(name='s4', budget=0, preferences=([a, c]))
    >>> s5 = Student(name='s5', budget=0, preferences=([a, b, c]))
    >>> students = [s1, s2, s3, s4, s5]
    >>> max_budget = 15
    >>> reset_students(students, max_budget)
    >>> [student.budget for student in students]
    [15, 15, 15, 15, 15]
    >>> [student.courses for student in students]
    [[], [], [], [], []]
    '''
    for student in students:
            student.budget = max_budget 
            student.courses = []

def map_price_demand(price_vector, max_budget: float, students, 
                     courses):
        '''
        ****adding more documention about here
        mapping price vector to demands of students
        >>> a = Course(name='a', price=0, capacity = 0, max_capacity=5)
        >>> b = Course(name='b', price=0, capacity = 0,max_capacity=3)
        >>> c = Course(name='c', price=0, capacity = 0,max_capacity=5)
        >>> courses = [a, b, c]

        >>> s1 = Student(name='s1', budget=0, preferences=([c, b]))
        >>> s2 = Student(name='s2', budget=0, preferences=([b, c, a]))
        >>> s3 = Student(name='s3', budget=0, preferences=([b, a]))
        >>> s4 = Student(name='s4', budget=0, preferences=([a, c]))
        >>> s5 = Student(name='s5', budget=0, preferences=([a, b, c]))
        >>> students = [s1, s2, s3, s4, s5]
        >>> max_budget = 15
        >>> price_vector = [7,8,7]
        >>> map_price_demand(price_vector, max_budget, students, courses)
        >>> [str(course) for course in courses]
        ['course name: a capacity 3/5 and priced 7', 'course name: b capacity 4/3 and priced 8', 'course name: c capacity 3/5 and priced 7']
        '''
        #different functions to each
        #testing working for changes in function -- DELETE
        reset_update_prices(price_vector, courses)
        reset_students(students, max_budget)
        def get_course(s:Student):
            for preference in s.preferences:
                if (s.budget >= preference.price and 
                    preference not in s.courses):
                    s.courses.append(preference)
                    s.budget = s.budget - preference.price
                    preference.capacity += 1
        for student in students:
            if (len(student.preferences) > len(student.courses)):
                get_course(student)

#function returning alpha error 
def alpha_error(price_vector, max_budget, students, courses):
    map_price_demand(price_vector, max_budget, students, courses)
    s = 0
    for course in courses:
        s = s + (course.max_capacity - course.capacity)**2
    return s

#
def get_demand_vector(courses):
    lst = []
    for course in courses:
        lst.append(f"{course.capacity}/{course.max_capacity}")
    return lst


def algorithm1(students, courses, max_budget:float, time_to:float, seed:int = 3, counter = 0):
    '''
    Heuristic search algorithm through price space, originally developed in Othman et al. 2010
    designed to give each student a fixed budget at first and try find the must corresponding
    price vector to approximate competitive equilibrium with lowest clearing error.
    programmers : Aviv Danino & Ori Ariel

    counter : parameter designed to help for testing in different machines 

    >>> a = Course(name='a', price=0, capacity=0, max_capacity=5)
    >>> b = Course(name='b', price=0, capacity=0, max_capacity=4)
    >>> c = Course(name='c', price=0, capacity=0, max_capacity=5)
    >>> courses = [a, b, c]
    >>> s1 = Student(name='s1', budget=18, year=1, courses=[], preferences=([c, b]))
    >>> s2 = Student(name='s2', budget=18, year=1, courses=[], preferences=([b, c, a]))
    >>> s3 = Student(name='s3', budget=18, year=1, courses=[], preferences=([b, a]))
    >>> s4 = Student(name='s4', budget=18, year=1, courses=[], preferences=([a, b, c]))
    >>> s5 = Student(name='s5', budget=18, year=1, courses=[], preferences=([a, b, c]))
    >>> s6 = Student(name='s6', budget=18, year=1, courses=[], preferences=([a, c, b]))
    >>> students = [s1, s2, s3, s4, s5, s6]
    >>> max_budget = 18
    >>> algorithm1(students, courses, max_budget, time_to= 2.0, seed = 3)
    [4.86, 2.34, 6.66]
    '''
    logger_counter = 0
    if time_to < 0.01:
        logger.warning("to little time can crash the program")
    pStar = [] 
    start_time = time.time()
    best_error = float("inf")
    #for better testing 
    random_state = np.random.RandomState(seed=3)
    while(time.time() - start_time < time_to):
        price_vector = [((random_state.randint(low=1,high=99)/100)*max_budget) for i in range(len(courses))]
        search_error = alpha_error(price_vector, max_budget, students, courses)
        tabu_list = TabuList(5)
        c = 0
        while c < tabu_list.size:
            queue = []
            for i in range(0, len(price_vector)):
                temp = copy.deepcopy(price_vector)
                temp[i] = (random_state.randint(low=1,high=99)/100)*max_budget
                queue.append(temp)  
            queue = sorted(queue, key=lambda x: alpha_error(x, max_budget, students, courses))
            found_step = False
            while(queue and not found_step):#3
                temp = queue.pop()
                #need function for demand check in tabu list
                map_price_demand(temp, max_budget, students, courses)
                if get_demand_vector(courses) not in tabu_list:
                    logger.debug("%s", str(temp))
                    found_step = True
            #end of while 3
            if(not queue) : c = tabu_list.size
            else:
                price_vector = temp
                #add the demands and not the price vector
                current_error = alpha_error(price_vector, max_budget, students, courses)
                tabu_list.add(get_demand_vector(courses))
                logger.debug((get_demand_vector(courses)))
                if(current_error < search_error):
                    search_error = current_error
                    logger.debug("search error is %d", search_error)
                    c = 0
                else:
                    c = c + 1
                #end of if
                if(current_error < best_error):
                    logger_counter += 1
                    best_error = current_error
                    pStar = price_vector
                    logger.info("best error is %d ", best_error)
                    logger.debug("and its price vector is %s", pStar)
                    if(logger_counter == counter):
                        time_to = 0
                        c = tabu_list.size
                
            #end of if
        #end of while 2
    #end of while 1

    logger.debug(logger_counter)
    return pStar
if __name__=="__main__":
    import pytest
    #run algorithm and test of the algorithm 
    pytest.main(args=["fairpy/course_allocation/algorithm1.py", "fairpy/course_allocation/algorithm1_test.py"])
