
"""
Demo for the 3 course allocation algorithm. Reference:
    Eric Budish, Gérard P. Cachon, Judd B. Kessler, Abraham Othman (2017) Course Match: A Large-Scale Implementation of
    Approximate Competitive Equilibrium from Equal Incomes for Combinatorial Allocation. Operations Research 65(2):314-336.
    https://doi.org/10.1287/opre.2016.1544
Programmers : Aviv Danino & Ori Ariel
Since:  2023-01
"""


import time
import random
from Course import Course
from Student import Student
from functools import cmp_to_key
import fairpy.adaptors as adaptors
from algorithm1 import algorithm1, random, TabuList, copy, map_price_demand, reset_update_prices, cmp_to_key, reset_students, time
from algorithm2 import algorithm2, csp_mapping, copy, math, cmp_to_key
from algorithm3 import algorithm3, mapping_csp


def get_courses_students_matrix(students, courses):
    # Initialize the matrix with all False values
    matrix = [[False for _ in courses] for _ in students]

    # Loop through each student and mark the courses they are enrolled in as True
    for i, student in enumerate(students):
        for course in student.courses:
            j = courses.index(course)
            matrix[i][j] = True

    return matrix


if __name__ == '__main__':
    # random.seed(3)
    start_time = time.time()
    # Generate 10 courses
    courses = []
    for j in range(10):
        name = chr(ord('a') + j)
        price = 0
        capacity = 0
        max_capacity = random.randint(3, 10)
        courses.append(Course(name=name,price=price,
            capacity=capacity, max_capacity=max_capacity))

    # Generate 40 students
    students = []
    for k in range(40):
        name = 's' + str(k+1)
        budget = 20
        year = random.randint(1, 4)
        preferences = random.sample(courses, random.randint(3, 7))
        students.append(Student(name=name, budget=budget,
            year=year, courses=courses, preferences=preferences))

    max_budget = 20
    price_vector1 = adaptors.divide(algorithm1,input=students,courses=courses, max_budget=max_budget, seed=3, time_to=10)

    # price_vector1 = algorithm1(
    # courses=courses, max_budget=max_budget, seed=3, students=students, time_to=10)
    map_price_demand(price_vector=price_vector1, courses=courses,
        max_budget=max_budget, students=students)
    p_scalar = (max_budget)
    price_vector2 =adaptors.divide(algorithm2,input=[course.price for course in courses],maximum=p_scalar,
        eps=0.5, csp_mapping=csp_mapping, students=students, courses=courses)
    # price_vector2 = algorithm2(price_vector=[course.price for course in courses], maximum=p_scalar,
    #     eps=0.5, csp_mapping=csp_mapping, students=students, courses=courses)
    print(price_vector2)
    # map_price_demand(price_vector=price_vector2,courses=courses,max_budget=max_budget,students=students)
    reset_students(students, max_budget)
    reset_update_prices(price_vector=price_vector2, courses=courses)
    csp_mapping(students, courses)
    adaptors.divide(algorithm3,input=courses,students_matrix=get_courses_students_matrix(students, courses),students=students)    
    # algorithm3(courses=courses, students=students,
    #     students_matrix=get_courses_students_matrix(students, courses))
    for s in courses:
        print(s)
    print("***********")
    print(time.time() - start_time)

    
    



                
