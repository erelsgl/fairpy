#!python3

import fairpy

instance = {
    "Ami": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Tami": {"green": 12, "red":8, "blue": 4, "yellow": 2} }

print("""
Many algorithms in fairpy use logging. This is useful for understanding how the algorithm works.
Logging is based on the standard python `logging` library:
""")

import sys, logging
fairpy.items.round_robin.logger.addHandler(logging.StreamHandler(sys.stdout))
fairpy.items.round_robin.logger.setLevel(logging.INFO)
print(fairpy.items.round_robin(instance))

print("""
You can configure the `round_robin` method with optional arguments such as the order of agents, 
or the subset of items to allocate. This makes it easy to use it as a subroutine 
in more complex algorithms.
""")

print(fairpy.items.round_robin(instance, agent_order=[1,0], items=["green", "red", "blue"]))

print("""
You can turn off logging for each module separately.
""")

fairpy.items.round_robin.logger.setLevel(logging.WARNING)
print(fairpy.items.round_robin(instance))
