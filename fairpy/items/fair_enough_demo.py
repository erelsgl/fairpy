#!python3

"""
Demonstration of the Fair-Enough algorithm.

Programmer: Shai Aharon
Since: 2021-02
"""

from fairpy.agents import AdditiveAgent
from fairpy.items import fair_enough

import logging
import sys

fair_enough.logger.addHandler(logging.StreamHandler(sys.stdout))
fair_enough.logger.setLevel(logging.INFO)

Alice = AdditiveAgent(
    {"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1, "i": 1, "j": 1, "k": 1, "l": 1}, name="Alice")
Bob = AdditiveAgent(
    {"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1, "i": 1, "j": 1, "k": 1, "l": 1}, name="Bob")
Eve = AdditiveAgent(
    {"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1, "i": 1, "j": 1, "k": 1, "l": 1}, name="Eve")
agents = [Alice, Bob, Eve]

print("Agents:")
for agn in agents:
    print(agn)

print("Fair Enough Algorithm starting..\n")
allocation = fair_enough.fair_enough(agents, set("abcdefghikjl"))
print(allocation)
