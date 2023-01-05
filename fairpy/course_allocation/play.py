import time
import random
from Course import Course
from Student import Student
from functools import cmp_to_key
import doctest
import logging
from algorithm1 import algorithm1,Course,Student,random,TabuList,copy,map_price_demand,reset_update_prices,cmp_to_key,reset_students,time
from algorithm2 import algorithm2,Course,Student,csp_mapping,copy,math,cmp_to_key
from algorithm3 import algorithm3,mapping_csp

def get_courses_students_matrix(students: list[Student], courses: list[Course]) -> list[list[bool]]:
    # Initialize the matrix with all False values
    matrix = [[False for _ in courses] for _ in students]
    
    # Loop through each student and mark the courses they are enrolled in as True
    for i, student in enumerate(students):
        for course in student.courses:
            j = courses.index(course)
            matrix[i][j] = True
    
    return matrix
    # Transpose the matrix
    return [list(row) for row in zip(*matrix)]

if __name__ == '__main__':
    times = []
    for i in range(1,4):
        start_time = time.time()
        # Generate 10 courses
        courses = []
        for i in range(10*i):
            name = chr(ord('a') + i)
            price = random.randint(5, 15)
            capacity = 0
            max_capacity = random.randint(3, 10)
            courses.append(Course(name=name, price=price, capacity=capacity, max_capacity=max_capacity))

        # Generate 40 students
        students = []
        for i in range(40*i):
            name = 's' + str(i+1)
            budget = random.randint(15, 25)
            year = random.randint(1, 4)
            preferences = random.sample(courses, random.randint(3, 7))
            students.append(Student(name=name, budget=budget, year=year, courses=courses, preferences=preferences))

        max_budget = 25
        price_vector1 = algorithm1(courses=courses,max_budget=max_budget, seed=i, students=students,time_to=10)
        map_price_demand(price_vector=price_vector1,courses=courses,max_budget=max_budget,students=students)

        p_scalar = max_budget- 0.1

        price_vector2 = algorithm2(price_vector=[course.price for course in courses], maximum=p_scalar,
            eps=0.5, csp_mapping=csp_mapping, students=students, courses=courses)

        print(price_vector2)
        # map_price_demand(price_vector=price_vector2,courses=courses,max_budget=max_budget,students=students)
        reset_students(students,max_budget)
        reset_update_prices(price_vector=price_vector2,courses=courses)
        csp_mapping(students,courses)

        algorithm3(courses=courses, students=students,
            students_matrix= get_courses_students_matrix(students,courses))
        times.append((time.time() - start_time))

    print(times)



