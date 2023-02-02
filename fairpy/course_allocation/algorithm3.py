'''
The algorithm takes input of student-course allocations 
and restricted demand functions based on students, class, year and budget surplus.
It then modifies the allocations based on the 
input demand functions and the ordering of the students, 
returns an altered allocations of students to courses.
'''


from Course import Course
from Student import Student
from functools import cmp_to_key
import doctest


import logging
logger = logging.getLogger(__name__)


def mapping_csp(courses, students, helper:dict, students_matrix):
    '''
    >>> a = Course(name='a', price=12, capacity=1 ,max_capacity=5)
    >>> b = Course(name='b', price=2, capacity=3 ,max_capacity=3)
    >>> c = Course(name='c', price=4.5, capacity=3 ,max_capacity=5)
    >>> courses = [a, b, c]

    >>> s1 = Student(name='s1', budget=10.5, courses=[b,c],preferences=([c, b]))
    >>> s2 = Student(name='s2', budget=10.5, courses=[b,c] ,year=2 ,preferences=([b, c, a]))
    >>> s3 = Student(name='s3', budget=15, courses=[b], year=3, preferences=([b, a]))
    >>> s4 = Student(name='s4', budget=0.5, courses=[a,c], year=3, preferences=([a, c]))
    >>> s5 = Student(name='s5', budget=4, courses=[a], preferences=([a, b, c]))
    >>> students = [s1, s2, s3, s4, s5]
    
    >>> students_matrix = [[False,True,True],[False,True,True],[False,True,False],[True,False,True],[True,False,False]]
    >>> helper = {}
    >>> count = 0
    >>> for course in courses:
    ...     helper[course.name] = count
    ...     count += 1
    >>> mapping_csp( courses ,students, helper ,students_matrix)
    >>> [str(course) for course in courses]
    ['course name: a capacity 2/5 and priced 12', 'course name: b capacity 3/3 and priced 2', 'course name: c capacity 3/5 and priced 4.5']
    '''
    def get_course(s: Student, stud_num:int) -> bool:
        for preference in s.preferences:
            if (s.budget >= preference.price and 
                preference not in s.courses and
                students_matrix[stud_num][helper.get(preference.name)] == False and
                preference.capacity < preference.max_capacity):
                s.courses.append(preference)
                s.budget = s.budget - preference.price
                preference.capacity += 1
                students_matrix[stud_num][helper.get(preference.name)] = True
                logger.debug("change in (%g, %g) in matrix from 0 to 1", stud_num, helper.get(preference.name))
                return True
        return False
    while True:
        flag = False
        i = 0
        for student in students:
            if (len(student.preferences) > len(student.courses)):
                if (get_course(student,i)):
                    flag = True
            i += 1
        if (not flag):
            break

def print_matrix(students, courses, students_matrix):
    s = ""
    for i in range(len(students)):
        for j in range(len(courses)):
            s+=str(students_matrix[i][j]) 
            s+= ", "
        s+="\n"
    return s

def algorithm3(courses, students, students_matrix,csp_students:callable =mapping_csp):
    '''
    Automated aftermarket allocations with increased budget and restricted allocations
    >>> a = Course(name='a', price= 12, capacity =3 , max_capacity=5)
    >>> b = Course(name='b', price = 2, capacity =4 , max_capacity=4)
    >>> c = Course(name='c', price=4.5, capacity =3 , max_capacity=5)
    >>> courses = [a, b, c]
    >>> s1 = Student(name='s1', budget=10.5, year=2,courses=[c,b], preferences=([c, b]))
    >>> s2 = Student(name='s2', budget=10.5, year=2,courses=[c,b], preferences=([b, c, a]))
    >>> s3 = Student(name='s3', budget=3, year=2,courses=[b,a], preferences=([b, a, c]))
    >>> s4 = Student(name='s4', budget=3, year=2,courses=[b,a], preferences=([a, b, c]))
    >>> s5 = Student(name='s5', budget=0.5, year=2,courses=[a,c],  preferences=([a, b, c]))
    >>> students = [s1, s2, s3, s4, s5]
    >>> students_matrix = [[False, True, True], [False, True, True], [True, True, False], [True, True, False], [True, False, True]]
    >>> algorithm3(courses, students ,students_matrix,mapping_csp)
    [[False, True, True], [False, True, True], [True, True, False], [True, True, False], [True, False, True]]
    '''    
    logger.debug(print_matrix(students, courses, students_matrix))    
    #create dict for easy traversal
    helper = {}
    count = 0
    for course in courses:
        helper[course.name] = count
        count += 1
    ## not part of algorithm
    csp_students(courses, students, helper, students_matrix)
    done = False
    while(not done): #1
        done = True
        for student in sorted(students, key=cmp_to_key(Student.comperator),reverse=True):
            before_budget = student.budget
            before_inc = student.courses
            student.budget *= 1.1
            csp_students(courses, students, helper, students_matrix)
            if(not(before_inc == student.courses)):
                done = False
                break #break of for loop and not while loop
    logger.debug(logger.debug(print_matrix(students, courses, students_matrix)))
    return students_matrix

algorithm3.logger = logger


if __name__=="__main__":
    import pytest
    #run algorithm and test of the algorithm
    pytest.main(args=[__file__, __file__[:-3]+"_test.py"])