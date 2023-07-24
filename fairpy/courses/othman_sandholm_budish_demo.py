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

import fairpy.courses
from fairpy import ValuationMatrix

import logging

fairpy.courses.othman_sandholm_budish.logger.addHandler(logging.StreamHandler())
fairpy.courses.othman_sandholm_budish.logger.setLevel(logging.INFO)

# The preference rating of the courses for each of the students:
utilities = numpy.array([[60,30,6,4],[6,2,42,26]])

# The capacity for each of the existing courses:
item_capacities = [2, 3, 1, 2]

# The maximum number of courses per student:
num_of_courses = 2

# The Placement of students in the courses according to the algorithm:
print(fairpy.courses.divide(fairpy.courses.othman_sandholm_budish, valuations=utilities, item_capacities=item_capacities, agent_capacities=num_of_courses))
