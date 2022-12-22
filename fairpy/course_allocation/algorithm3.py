from Course import Course
from Student import Student
from fairpy.items.valuations import ValuationMatrix
import doctest


a = Course(name='a', price=12, max_capacity=5)
b = Course(name='b', price=2, max_capacity=3)
c = Course(name='c', price=4.5, max_capacity=5)
courses = [a, b, c]

s1 = Student(name='s1', budget=17,preferences=([c, b]))
s2 = Student(name='s2', budget=17, year=2 ,preferences=([b, c, a]))
s3 = Student(name='s3', budget=17, year=3, preferences=([b, a]))
s4 = Student(name='s4', budget=17, year=3, preferences=([a, c]))
s5 = Student(name='s5', budget= 17, preferences=([a, b, c]))
students = [s1, s2, s3, s4, s5]


def mapping_csp(students: list[Student] = students, courses: list[Course] = courses) -> dict:
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
            if (not flag):
                break
            return {student.name: list(student.courses) for student in students}

def sort_function(students_list:list)->list:
    def compare(a:Student, b:Student):
        if(a.year - b.year == 0):
            return a.budget - b.budget
        return a.year - b.year 
    return sorted(students_list, cmp = compare)

def sort_oversubscribtion(course_list:list[Course])->list[Course]:
    '''
    sort function for sorting the must oversubscribed course
    '''
    def compare(a:Course, b:Course):
        return (a.capacity - a.max_capacity) - (b.capacity - b.max_capacity)
    return sorted(course_list, cmp = compare)

def algorithm3(students_matrix:list[list[bool]],csp_students:callable =mapping_csp,sort_func:callable = sort_function)->list:
    '''
    Automated aftermarket allocations with increased budget and restricted allocations

    >>> a = Course(name='a', price=12, ,capacity =2 ,max_capacity=5)
    >>> b = Course(name='b', price=2,capacity =3 , max_capacity=4)
    >>> c = Course(name='c', price=4.5, capacity =5 , max_capacity=5)
    >>> courses = [a, b, c]
    >>> s1 = Student(name='s1', budget=17, year=2, preferences=([c, b]))
    >>> s2 = Student(name='s2', budget=17, year=2 ,preferences=([b, c, a]))
    >>> s3 = Student(name='s3', budget=17, year=2, preferences=([b, a, c]))
    >>> s4 = Student(name='s4', budget=17, year=2, preferences=([a, b, c]))
    >>> s5 = Student(name='s5', budget= 17, year=2,  preferences=([a, b, c]))
    >>> students = [s1, s2, s3, s4, s5]
    >>> def mapping_csp(students: list, courses: list) -> dict:
    ...     def get_course(s: Student) -> bool:
    ...         for i in range(0, len(s.preferences)):
    ...             if (s.budget >= s.preferences[i].price):
    ...                 s.courses.append(s.preferences[i])
    ...                 s.budget = s.budget - s.preferences[i].price
    ...                 s.preferences[i].capacity += 1
    ...                 s.preferences.pop(i)
    ...                 return True
    ...         return False
    ...     while True:
    ...         flag = False
    ...         for student in students:
    ...             if (len(student.preferences) > 0):
    ...                 if (get_course(student)):
    ...                     flag = True
    ...         if (not flag):
    ...             break
    ...         return {student.name: list(student.courses) for student in students}
    >>> def sort_function(students_list:list)->list:
    ...     def compare(a:Student, b:Student):
    ...         if(a.year - b.year == 0):
    ...             return a.budget - b.budget
    ...         return a.year - b.year 
    ...     return sorted(students_list, cmp = compare)
    >>> a = Course(name='a', price=12, ,capacity =2 ,max_capacity=5)
    >>> b = Course(name='b', price=2,capacity =3 , max_capacity=4)
    >>> c = Course(name='c', price=4.5, capacity =5 , max_capacity=5)
    >>> courses = [a, b, c]
    >>> s1 = Student(name='s1', budget=17, year=2, preferences=([c, b]))
    >>> s2 = Student(name='s2', budget=17, year=2 ,preferences=([b, c, a]))
    >>> s3 = Student(name='s3', budget=17, year=2, preferences=([b, a, c]))
    >>> s4 = Student(name='s4', budget=17, year=2, preferences=([a, b, c]))
    >>> s5 = Student(name='s5', budget= 17, year=2,  preferences=([a, b, c]))
    >>> students_matrix = [[0,1,1],[1,0,1],[0,1,1],[1,0,1],[0,1,1]]
    >>> algorithm3(students_matrix,mapping_csp,sort_function)
    [[0,1,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1]]
    >>> a = Course(name='a', price=12, ,capacity =4 ,max_capacity=5)
    >>> b = Course(name='b', price=2,capacity =2 , max_capacity=3)
    >>> c = Course(name='c', price=4.5, capacity =3 , max_capacity=5)
    >>> courses = [a, b, c]
    >>> s1 = Student(name='s1', budget=17, year=1, preferences=([a, b]))
    >>> s2 = Student(name='s2', budget=17, year=2 ,preferences=([b, c, a]))
    >>> s3 = Student(name='s3', budget=17, year=3, preferences=([a, c]))
    >>> s4 = Student(name='s4', budget=17, year=3, preferences=([a, b, c]))
    >>> s5 = Student(name='s5', budget= 17, year=1,  preferences=([b, c]))
    >>> students = [s1, s2, s3, s4, s5]
    >>> students_matrix = [[1,1,0],[1,0,1],[1,0,1],[1,0,0],[0,1,1]]
    >>> algorithm3(students_matrix,mapping_csp,sort_function)
    [[1,1,0],[1,0,1],[1,0,1],[1,1,1],[0,1,1]]
    '''
    while(True):
        flag = True
        for student in sort_func(students):
            before_budget = student.budget
            before_inc = student.courses
            student.budget *= 1.1
            csp_students()
            if(not(before_inc == student.courses)):
                flag = False
                break
            else:
                student.budget  = before_budget
        if(flag):
            break


# TO-DO create an convertor from csp to matrix format

def test1():
    a = Course(name='a', price=12, max_capacity=5)
    b = Course(name='b', price=2, max_capacity=3)
    c = Course(name='c', price=4.5, max_capacity=5)
    courses = [a, b, c]

    s1 = Student(name='s1', budget=17,preferences=([c, b]))
    s2 = Student(name='s2', budget=17, year=2 ,preferences=([b, c, a]))
    s3 = Student(name='s3', budget=17, year=3, preferences=([b, a]))
    s4 = Student(name='s4', budget=17, year=3, preferences=([a, c]))
    s5 = Student(name='s5', budget= 17, preferences=([a, b, c]))
    students = [s1, s2, s3, s4, s5]
    def mapping_csp(students: list, courses: list) -> dict:
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
            if (not flag):
                break
            return {student.name: list(student.courses) for student in students}
    def sort_function(students_list:list)->list:
        def compare(a:Student, b:Student):
            if(a.year - b.year == 0):
                return a.budget - b.budget
            return a.year - b.year 
        return sorted(students_list, cmp = compare)
    students_matrix = [[0,1,1],[0,1,1],[0,1,0],[1,0,1],[1,0,1]]
    assert algorithm3(students_matrix,mapping_csp,sort_function) == [[0,1,1],[0,1,1],[1,1,0],[1,0,1],[1,0,1]]

# def test2():
#     a = Course(name='a', price=2.4, capacity=0, max_capacity=5)
#     b = Course(name='b', price=5, capacity=0, max_capacity=4)
#     c = Course(name='c', price=10.4, capacity=0, max_capacity=5)
#     courses = [a, b, c]


#     s1 = Student(name='s1', budget=18, year=1, courses=[], preferences=([c, b]))
#     s2 = Student(name='s2', budget=18, year=2, courses=[], preferences=([b, c, a]))
#     s3 = Student(name='s3', budget=18, year=3, courses=[], preferences=([b, a]))
#     s4 = Student(name='s4', budget=18, year=3, courses=[], preferences=([a, c]))
#     s5 = Student(name='s5', budget=18, year=1, courses=[], preferences=([a, b, c]))
#     s6 = Student(name='s6', budget=18, year=3, courses=[], preferences=([a, c, b]))
#     students = [s1, s2, s3, s4, s5, s6]
#     def mapping_csp(students: list, courses: list) -> dict:
#         def get_course(s: Student) -> bool:
#             for i in range(0, len(s.preferences)):
#                 if (s.budget >= s.preferences[i].price):
#                     s.courses.append(s.preferences[i])
#                     s.budget = s.budget - s.preferences[i].price
#                     s.preferences[i].capacity += 1
#                     s.preferences.pop(i)
#                     return True
#             return False
#         while True:
#             flag = False
#             for student in students:
#                 if (len(student.preferences) > 0):
#                     if (get_course(student)):
#                         flag = True
#             if (not flag):
#                 break
#             return {student.name: list(student.courses) for student in students}
#     def sort_function(students_list:list)->list:
#         def compare(a:Student, b:Student):
#             if(a.year - b.year == 0):
#                 return a.budget - b.budget
#             return a.year - b.year 
#         return sorted(students_list, cmp = compare)
#     students_matrix = [[0,1,1],[0,1,1],[1,1,0],[1,0,1],[1,1,0],[1,0,1]]
#     assert algorithm3(students_matrix,mapping_csp,sort_function) == [[0,1,1],[0,1,1],[1,1,0],[1,0,1],[1,1,1],[1,0,1]]

    
# def test3():
#     a = Course(name='a', price=6, capacity=0, max_capacity=3)
#     b = Course(name='b', price=4, capacity=0, max_capacity=3)
#     c = Course(name='c', price=6, capacity=0, max_capacity=3)
#     courses = [a, b, c]


#     s1 = Student(name='s1', budget=10, year= 1,courses=[], preferences=([a]))
#     s2 = Student(name='s2', budget=10, year= 2,courses=[], preferences=([b,a]))
#     s3 = Student(name='s3', budget=10, year= 3,courses=[], preferences=([c]))
#     s4 = Student(name='s4', budget=10, year= 3,courses=[], preferences=([c,b]))
#     s5 = Student(name='s5', budget=10, year= 2,courses=[], preferences=([c, a, b]))

#     students = [s1, s2, s3, s4, s5]

#     def mapping_csp(students: list, courses: list) -> dict:
#         def get_course(s: Student) -> bool:
#             for i in range(0, len(s.preferences)):
#                 if (s.budget >= s.preferences[i].price):
#                     s.courses.append(s.preferences[i])
#                     s.budget = s.budget - s.preferences[i].price
#                     s.preferences[i].capacity += 1
#                     s.preferences.pop(i)
#                     return True
#             return False
#         while True:
#             flag = False
#             for student in students:
#                 if (len(student.preferences) > 0):
#                     if (get_course(student)):
#                         flag = True
#             if (not flag):
#                 break
#             return {student.name: list(student.courses) for student in students}
#     def sort_function(students_list:list)->list:
#         def compare(a:Student, b:Student):
#             if(a.year - b.year == 0):
#                 return a.budget - b.budget
#             return a.year - b.year 
#         return sorted(students_list, cmp = compare)
#     students_matrix = [[1,0,0],[1,1,0],[0,0,1],[0,1,1],[0,1,1]]
#     assert algorithm3(students_matrix,mapping_csp,sort_function) == [[1,0,0],[1,1,0],[0,0,1],[0,1,1],[0,1,1]]