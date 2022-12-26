from Course import Course
from Student import Student
import time
import random
import copy
from functools import cmp_to_key
from TabuList import TabuList 
import doctest

def reset_update_prices(price_vector, courses:list[Course]):
    i = 0 
    for course in courses:
        course.capacity = 0 
        course.price = price_vector[i]
        i += 1

def reset_students(students:list[Student], max_budget: float):
    for student in students:
            student.budget = max_budget 
            student.courses = []

def map_price_demand(price_vector:list[float], max_budget: float, students:list[Student], 
                     courses:list[Course]):
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
    def alpha_error(price_vector):
        map_price_demand(price_vector, max_budget, students, courses)
        s = 0
        for course in courses:
            s = s + (course.max_capacity - course.capacity)**2
        return s
    pStar = [] 
    start_time = time.time()
    best_error = float("inf")
    random.seed(seed)
    while(time.time() - start_time < time_to):
        price_vector = [((random.randint(1, 9)/10)*max_budget) for i in range(len(courses))]
        map_price_demand(price_vector, max_budget, students, courses)
        search_error = alpha_error(price_vector)
        tabu_list = TabuList(5)
        c = 0
        while c < 5:
            queue = []
            temp_price_vector = copy.deepcopy(price_vector)
            for i in range(0, len(price_vector)):
                temp = copy.deepcopy(price_vector)
                wow = (random.randint(-9, 9))/10
                temp[i] += (wow)*temp[i]
                queue.append(temp)
            queue = sorted(queue, key=lambda x: alpha_error(x))
            found_step = False
            while(queue and not found_step):#3
                temp = queue.pop()
                if temp not in tabu_list:
                    found_step = True
            #end of while 3
            if(not queue) : c = 5
            else:
                price_vector = temp_price_vector
                tabu_list.add(temp)
                current_error = alpha_error(price_vector)
                if(current_error < search_error):
                    search_error = current_error
                    c = 0
                else:
                    c = c + 1
                #end of if
                if(current_error < best_error):
                    best_error = current_error
                    pStar = price_vector
            #end of if
        #end of while 2
    #end of while 1
    #those two lines for example
    price_vector = pStar
    map_price_demand(price_vector, max_budget, students, courses)
    #****************************************************************88
    #at the end of time looped we return the price vector
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

    print(algorithm1(students, courses, max_budget, time_to= 24, seed = 3))#2
    # print(algorithm1(students, courses, max_budget, time_to= 8, seed = 3))#6

check_this()