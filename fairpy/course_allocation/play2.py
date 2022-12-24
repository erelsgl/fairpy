from Course import Course
from Student import Student
from functools import cmp_to_key
import doctest

def mapping_csp(courses:list[Course], students:list[Student], helper:dict, students_matrix:list[list[bool]]):
    def get_course(s: Student, stud_num:int) -> bool:
        for i in range(0, len(s.preferences)):
            if (s.budget >= s.preferences[i].price and
                   students_matrix[stud_num][helper.get(s.preferences[i].name)] == False and
                   s.preferences[i].capacity < s.preferences[i].max_capacity):
                s.courses.append(s.preferences[i])
                s.budget = s.budget - s.preferences[i].price
                s.preferences[i].capacity += 1
                students_matrix[stud_num][helper.get(s.preferences[i].name)] = True
                s.preferences.pop(i)
                return True
        return False
    while True:
        flag = False
        i = 0
        for student in students:
            if (len(student.preferences) > 0):
                if (get_course(student,i)):
                    flag = True
            i += 1
        if (not flag):
            break

def algorithm3(courses, students, students_matrix:list[list[bool]],csp_students:callable =mapping_csp)->list:
    helper = {}
    count = 0
    for course in courses:
        helper[course.name] = count
        count += 1
    while(True):
        flag = True
        for student in sorted(students, key=cmp_to_key(Student.comperator),reverse=True):
            before_budget = student.budget
            before_inc = student.courses
            student.budget *= 1.1
            csp_students(courses, students, helper, students_matrix)
            if(not(before_inc == student.courses)):
                flag = False
                break
            else:
                student.budget  = before_budget
        if(flag):
            break
    return students_matrix

def check_this():
    a = Course(name='a', price= 12, capacity =3 , max_capacity=5)
    b = Course(name='b', price = 2, capacity =4 , max_capacity=4)
    c = Course(name='c', price=4.5, capacity =3 , max_capacity=5)
    courses = [a, b, c]
    s1 = Student(name='s1', budget=10.5, year=2,courses=[c,b], preferences=([c, b]))
    s2 = Student(name='s2', budget=10.5, year=2,courses=[c,b], preferences=([b, c, a]))
    s3 = Student(name='s3', budget=3, year=2,courses=[b,a], preferences=([b, a, c]))
    s4 = Student(name='s4', budget=3, year=2,courses=[b,a], preferences=([a, b, c]))
    s5 = Student(name='s5', budget=0.5, year=2,courses=[a,c],  preferences=([a, b, c]))
    students = [s1, s2, s3, s4, s5]
    students_matrix = [[False, True, True], [False, True, True], [True, True, False], [True, True, False], [True, False, True]]
    # students_matrix = [[False,True,True],[True,False,True],[False,True,True],[True,False,True],[False,True,True]]
    # mapping_csp(courses, students, helper, students_matrix)
    print(algorithm3(courses, students ,students_matrix,mapping_csp))
    #[[False,True,True],[True,False,True],[True,True,True],[True,True,True],[True,True,True]]


check_this()

