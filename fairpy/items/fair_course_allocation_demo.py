"""
Article Name:
"Finding Approximate Competitive Equilibria: Efficient and Fair Course Allocation" (2010)

Authors:
Abraham Othman, Tuomas Sandholm and Eric Budish.

Link:
https://dl.acm.org/doi/abs/10.5555/1838206.1838323

Programmer:
Tahel Zecharia.

The algorithm performs a fair and equal allocation as much as possible
between courses for students given a list of preferences for each student.

"""
import numpy

import fairpy
from fairpy import ValuationMatrix
from fairpy.items import fair_course_allocation_implementation
from fairpy.items.fair_course_allocation_implementation import general_course_allocation

import logging

fair_course_allocation_implementation.logger.addHandler(logging.StreamHandler())
fair_course_allocation_implementation.logger.setLevel(logging.INFO)

# The preference rating of the courses for each of the students:
utilities = ValuationMatrix(numpy.array([[1, 2, 33, 44, 34],
                             [4, 9, 19, 64, 88],
                             [60, 80, 7, 3, 14],
                             [58, 76, 95, 5, 2],
                             [7, 70, 33, 47, 63],
                             [3, 6, 1, 64, 33],
                             [88, 2, 4, 6, 78],
                             [53, 39, 7, 3, 14],
                             [58, 9, 33, 54, 2],
                             [7, 8, 34, 47, 28]]))

# The capacity for each of the existing courses:
capacity = [2, 3, 1, 2, 3]

# The maximum number of courses per student:
num_of_courses = 2

# The Placement of students in the courses according to the algorithm:
allocation = general_course_allocation(utilities, capacity, num_of_courses)
print(allocation)

# print(fairpy.divide(general_course_allocation, utilities, capacity, num_of_courses))
