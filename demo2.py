#!python3

"""
Demonstrates how to use fairpy for indivisible item allocation.

Programmer: Erel Segal-Halevi
Since: 2021-05
"""


import fairpy

items = ["green", "red", "blue", "yellow"]
agents = {
    "Avi": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Batya": {"green": 12, "red":8, "blue": 4, "yellow": 2} }


fairpy.round_robin(items, agents, agent_order=["Avi", "Batya"])


# cut_and_choose.logger.addHandler(logging.StreamHandler(sys.stdout))
# cut_and_choose.logger.setLevel(logging.INFO)

# last_diminisher.logger.addHandler(logging.StreamHandler(sys.stdout))
# last_diminisher.logger.setLevel(logging.INFO)
