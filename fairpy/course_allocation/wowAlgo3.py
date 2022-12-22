from Course import Course
from Student import Student
from functools import cmp_to_key
import doctest


students_matrix = [[False,True,True],[False,True,True],[False,True,False],[True,False,True],[True,True,False]]


a = Course(name='a', price=12, max_capacity=5)
b = Course(name='b', price=2, max_capacity=3)
c = Course(name='c', price=4.5, max_capacity=5)
courses = [a, b, c]

s1 = Student(name='s1', budget=10.5, courses=[b,c],preferences=([c, b]))
s2 = Student(name='s2', budget=10.5, courses=[b,c] ,year=2 ,preferences=([b, c, a]))
s3 = Student(name='s3', budget=15, courses=[b], year=3, preferences=([b, a]))
s4 = Student(name='s4', budget=0.5, courses=[a,c], year=3, preferences=([a, c]))
s5 = Student(name='s5', budget=4, courses=[a,b], preferences=([a, b, c]))
students = [s1, s2, s3, s4, s5]
def mapping_csp() -> dict:
    def get_course(s: Student, stud_num:int) -> bool:
        for i in range(0, len(s.preferences)):
            if (s.budget >= s.preferences[i].price and
                   students_matrix[stud_num][helper.get(s.preferences[i].name)] == False):
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

def algorithm3(students_matrix:list[list[bool]],csp_students:callable =mapping_csp)->list:
    while(True):
        flag = True
        for student in sorted(students, key=cmp_to_key(Student.comperator)):
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
    return students_matrix

helper = {'a' : 0, 'b' : 1, 'c' : 2}

print(algorithm3(students_matrix,mapping_csp))



# יהדות איטליה 12