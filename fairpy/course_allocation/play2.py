from Course import Course
from Student import Student
from functools import cmp_to_key
from TabuList import TabuList 
import time
import random
import copy
import doctest
import logging

logger = logging.getLogger(__name__)
console = logging.StreamHandler()  # writes to stderr (= cerr)
logfile = logging.FileHandler("my_logger1.log", mode="w") 
logger.handlers = [console,logfile]
logfile.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: Line %(lineno)d: %(message)s'))

logger.setLevel(logging.DEBUG)
console.setLevel(logging.INFO)

def reset_update_prices(price_vector, courses:list[Course]):
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

def reset_students(students:list[Student], max_budget: float):
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

def map_price_demand(price_vector:list[float], max_budget: float, students:list[Student], 
                     courses:list[Course]):
        '''
        mapping price vector to demands of students
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
        >>> price_vector = [7,8,7]
        >>> map_price_demand(price_vector, max_budget, students, courses)
        >>> [str(course) for course in courses]
        ['course name: a capacity 3/5 and priced 7', 'course name: b capacity 4/3 and priced 8', 'course name: c capacity 3/5 and priced 7']
        '''
        reset_update_prices(price_vector, courses)
        reset_students(students, max_budget)
        def get_course(s) -> bool:
            for i in range(0, len(s.preferences)):
                if (s.budget >= s.preferences[i].price and 
                    s.preferences[i] not in s.courses):
                    s.courses.append(s.preferences[i])
                    s.budget = s.budget - s.preferences[i].price
                    s.preferences[i].capacity += 1
                    return True
            return False
        while True:
            flag = False
            for student in students:
                if (len(student.preferences) > 0):
                    if (get_course(student)):
                        flag = True
            if(not flag):
                break 

def algorithm1(students:list[Student], courses:list[Course], max_budget:float, time_to:float, seed:int) -> list:
    '''
    Heuristic search algorithm through price space, originally developed in Othman et al. 2010
    designed to give each student a fixed budget at first and try find the must corresponding
    price vector to approximate competitive equilibrium with lowest clearing error.
    programmers : Aviv Danino & Ori Ariel

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
    [5.3999999999999995, 5.3999999999999995, 1.8]
    '''
    def alpha_error(price_vector):
        map_price_demand(price_vector, max_budget, students, courses)
        s = 0
        for course in courses:
            s = s + (course.max_capacity - course.capacity)**2
        return s
    pStar = [] 
    start_time = time.time()
    best_error = float("inf")
    random.seed(seed) #to hold the random number generator
    while(time.time() - start_time < time_to):
        price_vector = [((random.randint(1, 9)/10)*max_budget) for i in range(len(courses))]
        map_price_demand(price_vector, max_budget, students, courses)
        search_error = alpha_error(price_vector)
        tabu_list = TabuList(5)
        c = 0
        while c < 5:
            queue = []
            for i in range(0, len(price_vector)):
                temp = copy.deepcopy(price_vector)
                temp[i] = (random.randint(1, 9)/10)*max_budget
                queue.append(temp)
            queue = sorted(queue, key=lambda x: alpha_error(x))
            # for price in queue:
            found_step = False
            while(queue and not found_step):#3
                temp = queue.pop()
                if temp not in tabu_list:
                    logger.debug("%s", str(temp))
                    found_step = True
            #end of while 3
            if(not queue) : c = 5
            else:
                price_vector = temp
                tabu_list.add(temp)
                current_error = alpha_error(price_vector)
                if(current_error < search_error):
                    search_error = current_error
                    logger.debug("best error is %d", search_error)
                    c = 0
                else:
                    c = c + 1
                #end of if
                if(current_error < best_error):
                    best_error = current_error
                    pStar = price_vector
                    logger.info("best error is %d and it price vector \n%s", best_error, str(pStar))
            #end of if
        #end of while 2
    #end of while 1
    return pStar

def check_this():
    a = Course(name='a', price=0, capacity=0, max_capacity=5)
    b = Course(name='b', price=0, capacity=0, max_capacity=4)
    c = Course(name='c', price=0, capacity=0, max_capacity=5)
    d = Course(name='d', price=0, capacity=0, max_capacity=3)
    e = Course(name='e', price=0, capacity=0, max_capacity=7)
    f = Course(name='f', price=0, capacity=0, max_capacity=2)
    courses = [a, b, c, d, e, f]
    s1 = Student(name='s1', budget=18, year=1, courses=[], preferences=([c, b, e, f]))
    s2 = Student(name='s2', budget=18, year=1, courses=[], preferences=([b, c, a, e]))
    s3 = Student(name='s3', budget=18, year=1, courses=[], preferences=([b, a, d]))
    s4 = Student(name='s4', budget=18, year=1, courses=[], preferences=([a, b, c]))
    s5 = Student(name='s5', budget=18, year=1, courses=[], preferences=([d, a,e, b, c]))
    s6 = Student(name='s6', budget=18, year=1, courses=[], preferences=([a, e,c,f, b]))
    s7 = Student(name='s7', budget=18, year=1, courses=[], preferences=([c,d ,b]))
    s8 = Student(name='s8', budget=18, year=1, courses=[], preferences=([b, c, a]))
    s9 = Student(name='s9', budget=18, year=1, courses=[], preferences=([b,f,e, a]))
    s10 = Student(name='s10', budget=18, year=1, courses=[], preferences=([d ,f]))
    s11 = Student(name='s11', budget=18, year=1, courses=[], preferences=([d,e,f]))
    s12 = Student(name='s12', budget=18, year=1, courses=[], preferences=([d,f,e]))
    students = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12]
    max_budget = 18
    print(algorithm1(students, courses, max_budget, time_to= 1, seed = 3))
check_this()