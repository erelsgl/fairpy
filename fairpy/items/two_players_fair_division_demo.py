"""
Demo for two_players_fair_division.py

Two-player fair division of indivisible items: Comparison of algorithms
By: D. Marc Kilgour, Rudolf Vetschera

programmers: Itay Hasidi & Amichai Bitan
"""

import fairpy
from fairpy.items.two_players_fair_division import *


Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name='Alice')
George = fairpy.agents.AdditiveAgent({'a': 2, 'b': 5, 'c': 4, 'd': 1, 'e': 3, 'f': 6}, name='George')
items = ['a', 'b', 'c', 'd', 'e', 'f']

print("sequential:\n", sequential([Alice, George], items))
print("restricted_simple:\n", restricted_simple([Alice, George], items))
print("singles_doubles:\n", singles_doubles([Alice, George], items))
print("iterated_singles_doubles:\n", iterated_singles_doubles([Alice, George], items))
print("s1:\n", s1([Alice, George], items))
print("l1:\n", l1([Alice, George], items))
print("top_down:\n", top_down([Alice, George], items))
print("top_down_alternating:\n", top_down_alternating([Alice, George], items))
print("bottom_up:\n", bottom_up([Alice, George], items))
print("bottom_up_alternating:\n", bottom_up_alternating([Alice, George], items))
print("trump:\n", trump([Alice, George], items))

