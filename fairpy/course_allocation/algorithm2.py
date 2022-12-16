from Course import Course
from Student import Student
import doctest
# from fairpy.items.valuations import ValuationMatrix



def sort_oversubscribtion(course_list:list[Course])->list:
    '''
    sort function for sorting the must oversubscribed course
    '''
    def compare(a:Course, b:Course):
        return (a.capacity - a.max_capacity) - (b.capacity - b.max_capacity)
    return sorted(course_list, cmp = compare)




def algorithm2(price_vector:list[float], maximum:int, eps:float, csp_mapping:callable)->list:
    '''
    Iterative oversubscription elimination algorithm, 
    reducing by half the excess demand of the most oversubscribed course with each pass,
    >>> def csp_mapping(students: list, courses: list) -> dict:
    ...    def get_course(s: Student) -> bool:
    ...        for i in range(0, len(s.preferences)):
    ...            if (s.budget >= s.preferences[i].price):
    ...                s.courses.append(s.preferences[i])
    ...                s.budget = s.budget - s.preferences[i].price
    ...                s.preferences[i].capacity += 1
    ...                s.preferences.pop(i)
    ...                return True
    ...        return False
    ...    while True:
    ...        flag = False
    ...        for student in students:
    ...            if (len(student.preferences) > 0):
    ...                if (get_course(student)):
    ...                    flag = True
    ...        if(not flag):
    ...            break
    ...    return {course.name: course.capacity for course in courses}
    >>> a = Course(name='a', price=3, max_capacity=5)
    ... b = Course(name='b', price=4, max_capacity=3)
    ... c = Course(name='c', price=3, max_capacity=5)
    ... courses = [a, b, c]

    ... s1 = Student(name='s1', budget=10, preferences=([c, b]))
    ... s2 = Student(name='s2', budget=10, preferences=([b, c, a]))
    ... s3 = Student(name='s3', budget=10, preferences=([b, a]))
    ... s4 = Student(name='s4', budget=10, preferences=([a, b, c]))
    ... s5 = Student(name='s5', budget=10, preferences=([a, b, c]))
    ... students = [s1, s2, s3, s4, s5]
    >>> eps = 0.1
    >>> maximum = 6
    >>> price_vector = [3,4,3]
    >>> algorithm2(price_vector, maximum, eps, csp_mapping)
    [3,5,3]
    >>> a = Course(name='a', price=12, max_capacity=5)
    ... b = Course(name='b', price=3, max_capacity=3)
    ... c = Course(name='c', price=4.5, max_capacity=5)
    ... courses = [a, b, c]

    ... s1 = Student(name='s1', budget=15, preferences=([c, b]))
    ... s2 = Student(name='s2', budget=15, preferences=([b, c, a]))
    ... s3 = Student(name='s3', budget=15, preferences=([b, a]))
    ... s4 = Student(name='s4', budget=15, preferences=([a, b, c]))
    ... s5 = Student(name='s5', budget=15, preferences=([a, b, c]))
    ... students = [s1, s2, s3, s4, s5]
    >>> eps = 1
    >>> maximum = 10
    >>> price_vector = [9,3,4.5]
    >>> algorithm2(price_vector, maximum, eps, csp_mapping)
    [9,6,4.5]

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
    def csp_mapping(students: list, courses: list) -> dict:
        def get_course(s: Student) -> bool:
            for i in range(0, len(s.preferences)):
                if (s.budget >= s.preferences[i].price):
                    s.courses.append(s.preferences[i])
                    s.budget = s.budget - s.preferences[i].price
                    s.preferences[i].capacity += 1
                    s.preferences.pop(i)
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
        return {course.name: course.capacity for course in courses}
    eps = 1
    maximum = 10
    price_vector = [9,2,4.5]
    assert algorithm2(price_vector, maximum, eps, csp_mapping) == [9,8,3]

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

    def csp_mapping(students: list, courses: list) -> dict:
        def get_course(s: Student) -> bool:
            for i in range(0, len(s.preferences)):
                if (s.budget >= s.preferences[i].price):
                    s.courses.append(s.preferences[i])
                    s.budget = s.budget - s.preferences[i].price
                    s.preferences[i].capacity += 1
                    s.preferences.pop(i)
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
        return {course.name: course.capacity for course in courses}
    eps = 1
    maximum = 10
    price_vector = [2.4,5,10.4]
    assert algorithm2(price_vector, maximum, eps, csp_mapping) == [2.4,5.625,10.4]

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

    def csp_mapping(students: list, courses: list) -> dict:
        def get_course(s: Student) -> bool:
            for i in range(0, len(s.preferences)):
                if (s.budget >= s.preferences[i].price):
                    s.courses.append(s.preferences[i])
                    s.budget = s.budget - s.preferences[i].price
                    s.preferences[i].capacity += 1
                    s.preferences.pop(i)
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
        return {course.name: course.capacity for course in courses}
    eps = 1
    maximum = 10
    price_vector = [6,4,6]
    assert algorithm2(price_vector, maximum, eps, csp_mapping) == [6,4,6]
