from Course import Course
from Student import Student
from functools import cmp_to_key
import cvxpy as cp
import doctest
import logging



logger = logging.getLogger(__name__)
console = logging.StreamHandler()  # writes to stderr (= cerr)
logfile = logging.FileHandler("my_logger3.log", mode="w") 
logger.handlers = [console,logfile]
logfile.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: Line %(lineno)d: %(message)s'))

logger.setLevel(logging.DEBUG)
console.setLevel(logging.INFO)

import cvxpy as cp

def map_students_to_courses(students: list[Student], courses: list[Course]) -> dict[Student, list[Course]]:
     # Create a variable for each student-course pair
    x = cp.Variable((len(students), len(courses)), boolean=True)
    
    # Constraint: the total number of students in each course cannot exceed the course's maximum capacity
    constraints = [cp.sum(x, axis=0) <= [course.max_capacity for course in courses]]

    objectives_courses = []
    # Constraint: each student can only be assigned to courses within their budget
    for i, student in enumerate(students):
        constraints.append(cp.sum(cp.multiply(x[i, :], [course.price for course in courses])) <= student.budget)
        objective = cp.sum(cp.multiply(x[i, :], [course.price for course in courses]))
        objectives_courses.append(objective)

    # objectives_courses = []
    # # Constraint: each student can only be assigned to courses within their budget
    # for i, student in enumerate(students):
    #     constraints.append(cp.sum(cp.multiply(x[i, :], [course.price for course in courses])) <= student.budget)
    #     objective = cp.Minimize(cp.sum(cp.multiply(x[i, :], [course.price for course in courses])))
    #     objectives_courses.append(objective)
    
    
    # Constraint: each student can only be assigned to courses in their preferences
    for i, student in enumerate(students):
        preferences = [j for j, course in enumerate(courses) if course in student.preferences]
        constraints.append(x[i, preferences] == 1)
    

    # Objective: minimize the total cost of the courses taken by the students, giving priority to higher year students and then lower priority to students with the highest budget
    # prices_matrix = cp.diag([course.price for course in courses])
    # year_matrix = cp.diag([student.year for student in students])
    # prices_matrix = cp.diag([course.price for course in courses])
    # course_prices = [course.price for course in courses]
    # objective1 = cp.Minimize(cp.sum(cp.multiply(x, course_prices), axis=0))
    objective1 = cp.Minimize(sum(objectives_courses))

    # objective = cp.Minimize(cp.sum(cp.multiply(x, prices_matrix)) + cp.sum(cp.multiply(x, year_matrix)) - cp.sum(cp.multiply(x, [student.budget for student in students])))    
    # Solve the optimization problem
    problem = cp.Problem(objective1, constraints)
    problem.solve()
    
    # Map the students to the courses they were assigned to
    assignment = {}
    # for i, student in enumerate(students):
    #     # indices = []
    #     # for k, course in enumerate(courses):
    #     #     if(x[i,k].value):
    #     #         indices.append(k)
    #     indices = [j for j, val in enumerate(x[i, :]) if val.value]
    #     assignment[student] = [courses[j] for j in indices]
    return x



def mapping_csp(courses:list[Course], students:list[Student], helper:dict, students_matrix:list[list[bool]]):
    def get_course(s: Student, stud_num:int) -> bool:
        for i in range(0, len(s.preferences)):
            if (s.budget >= s.preferences[i].price and
                   students_matrix[stud_num][helper.get(s.preferences[i].name)] == False and
                   s.preferences[i] not in s.courses and
                   s.preferences[i].capacity < s.preferences[i].max_capacity):
                s.courses.append(s.preferences[i])
                s.budget = s.budget - s.preferences[i].price
                s.preferences[i].capacity += 1
                students_matrix[stud_num][helper.get(s.preferences[i].name)] = True
                logger.debug("change in (%g, %g) in matrix from 0 to 1", stud_num, helper.get(s.preferences[i].name))
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
    s = ""
    for i in range(len(students)):
        for j in range(len(courses)):
            s+=str(students_matrix[i][j]) 
            s+= ", "
        s+="\n"
    logger.debug(s)
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
        s = ""
        for i in range(len(students)):
            for j in range(len(courses)):
                s += str(students_matrix[i][j]) 
                s+= ", "
            s+="\n"
        logger.debug(s)
    return students_matrix

def check_this():
    a = Course(name='a', price=3.4, capacity=4, max_capacity=5)
    b = Course(name='b', price=5, capacity=4, max_capacity=4)
    c = Course(name='c', price=10.4, capacity=4, max_capacity=5)
    courses = [a,b,c]
    s1 = Student(name='s1', budget=2.6, year=1, courses=[c,b], preferences=([c, b]))
    s2 = Student(name='s2', budget=2.6, year=2, courses=[c,b], preferences=([b, c, a]))
    s3 = Student(name='s3', budget=9.6, year=3, courses=[a,b], preferences=([b, a]))
    s4 = Student(name='s4', budget=4.2, year=3, courses=[a,c], preferences=([a, c]))
    s5 = Student(name='s5', budget=9.6, year=1, courses=[a,b], preferences=([a, b, c]))
    s6 = Student(name='s6', budget=4.2, year=3, courses=[a,c], preferences=([a, c, b]))
    students = [s1, s2, s3, s4, s5, s6]
    students_matrix = [[False, True, True], [False, True, True], [True, True, False], [True, False, True], [True, True, False], [True, False, True]]
    for student in map_students_to_courses(students,courses):
        for s in student:
            print(s.value)
    # print(algorithm3(courses, students, students_matrix, mapping_csp))
check_this()