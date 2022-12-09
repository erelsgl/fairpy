from Course import Course
from Student import Student

def algorithm1(max_budget:int, map_price_demand:callable, sort_alpha:callable, time:float) -> list:
    '''
    Heuristic search algorithm through price space, originally developed in Othman et al. 2010
    designed to give each student a fixed budget at first and try find the must corresponding
    price vector to approximate competitive equilibrium with lowest clearing error.
    programmers : Aviv Danino & Ori Ariel
    '''
    pass


def test1(): 
    a = Course(name='a', price=12, max_capacity=5)
    b = Course(name='b', price=2, max_capacity=3)
    c = Course(name='c', price=4.5, max_capacity=5)
    courses = [a, b, c]

    s1 = Student(name='ss1', budget=15, preferences=([c, b]))
    s2 = Student(name='s2', budget=15, preferences=([b, c, a]))
    s3 = Student(name='s3', budget=15, preferences=([b, a]))
    s4 = Student(name='s4', budget=15, preferences=([a, c]))
    s5 = Student(name='s5', budget=15, preferences=([a, b, c]))
    students = [s1, s2, s3, s4, s5]


    def sort_alpha(courses_list:list)->list:
        import random
        list_of_lists = []
        for i in len(courses_list):
            delta = 0.2 * temp[i].price
            temp = courses_list
            temp[i].price = temp[i].price - temp[i].price*random.random()*0.2
            list_of_lists.append(temp)
        def compare(a:list, b:list):
            def alpha_error(lst:list):
                s = 0
                for course in lst:
                    s = s + (course.max_capacity - course.capacity)**2
                return s
            return alpha_error(a) - alpha_error(b)
        return sorted(list_of_lists, cmp = compare)

    def map_price_demand(students:list, courses:list)->dict:
        def get_course(s:Student)->bool:
            for i in range(0,len(s.preferences)):
                if(s.budget >= s.preferences[i].price):
                    s.courses.append(s.preferences[i])
                    s.budget = s.budget - s.preferences[i].price
                    s.preferences[i].capacity += 1 
                    s.preferences.pop(i)
                    return True
            return False
        while True:
            flag = False 
            for student in students:
                if(len(student.preferences) > 0):
                    if(get_course(student)):
                        flag = True
            if(not flag):
                break
        return {course.name: course.capacity for course in courses}
    max_budget = 15
    assert algorithm1(max_budget, map_price_demand, sort_alpha, time = 0) == [9,2,4.5]

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

    def sort_alpha(courses_list:list)->list:
        import random
        list_of_lists = []
        for i in len(courses_list):
            delta = 0.2 * temp[i].price
            temp = courses_list
            temp[i].price = temp[i].price - temp[i].price*random.random()*0.2
            list_of_lists.append(temp)
        def compare(a:list, b:list):
            def alpha_error(lst:list):
                s = 0
                for course in lst:
                    s = s + (course.max_capacity - course.capacity)**2
                return s
            return alpha_error(a) - alpha_error(b)
        return sorted(list_of_lists, cmp = compare)

    def map_price_demand(students:list, courses:list)->dict:
        def get_course(s:Student)->bool:
            for i in range(0,len(s.preferences)):
                if(s.budget >= s.preferences[i].price):
                    s.courses.append(s.preferences[i])
                    s.budget = s.budget - s.preferences[i].price
                    s.preferences[i].capacity += 1 
                    s.preferences.pop(i)
                    return True
            return False
        while True:
            flag = False 
            for student in students:
                if(len(student.preferences) > 0):
                    if(get_course(student)):
                        flag = True
            if(not flag):
                break
        return {course.name: course.capacity for course in courses}
    max_budget = 18
    assert algorithm1(max_budget, map_price_demand, sort_alpha, time = 0) == [2.4,5,10.4]


def test3(): 
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


    def sort_alpha(courses_list:list)->list:
        import random
        list_of_lists = []
        for i in len(courses_list):
            delta = 0.2 * temp[i].price
            temp = courses_list
            temp[i].price = temp[i].price - temp[i].price*random.random()*0.2
            list_of_lists.append(temp)
        def compare(a:list, b:list):
            def alpha_error(lst:list):
                s = 0
                for course in lst:
                    s = s + (course.max_capacity - course.capacity)**2
                return s
            return alpha_error(a) - alpha_error(b)
        return sorted(list_of_lists, cmp = compare)

    def map_price_demand(students:list, courses:list)->dict:
        def get_course(s:Student)->bool:
            for i in range(0,len(s.preferences)):
                if(s.budget >= s.preferences[i].price):
                    s.courses.append(s.preferences[i])
                    s.budget = s.budget - s.preferences[i].price
                    s.preferences[i].capacity += 1 
                    s.preferences.pop(i)
                    return True
            return False
        while True:
            flag = False 
            for student in students:
                if(len(student.preferences) > 0):
                    if(get_course(student)):
                        flag = True
            if(not flag):
                break
        return {course.name: course.capacity for course in courses}
    max_budget = 10
    assert algorithm1(max_budget, map_price_demand, sort_alpha, time = 0) == [6,4,6]