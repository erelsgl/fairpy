"""
Demo for picking_sequence.

Programmer: Erel Segal-Halevi.
Since: 2023-07.
"""

import fairpy
from fairpy.courses import round_robin

import logging
round_robin.logger.addHandler(logging.StreamHandler())
round_robin.logger.setLevel(logging.INFO)

# The preference rating of the courses for each of the students:
valuations = {
    "Alice": {"c1":2, "c2": 3, "c3": 4},
    "Bob": {"c1": 4, "c2": 5, "c3": 6}
}
agent_capacities = {"Alice": 2, "Bob": 1}
course_capacities = {"c1": 2, "c2": 1, "c3": 1}

# instance = fairpy.courses.Instance(agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations)
# print(round_robin(instance))

print(fairpy.courses.divide(round_robin, agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations))




