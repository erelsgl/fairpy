"""
Demo for two_players_fair_division.py

Two-player fair division of indivisible items: Comparison of algorithms
By: D. Marc Kilgour, Rudolf Vetschera

programmers: Itay Hasidi & Amichai Bitan
"""

import fairpy
from fairpy.items.two_players_fair_division import *

agents_lst = []
items_lst = []

Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
items = ['computer', 'phone', 'tv', 'book']
agents_lst.append([Alice, George])
items_lst.append(items)
Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name='Alice')
George = fairpy.agents.AdditiveAgent({'a': 2, 'b': 6, 'c': 4, 'd': 1, 'e': 3, 'f': 5}, name='George')
items = ['a', 'b', 'c', 'd', 'e', 'f']
agents_lst.append([Alice, George])
items_lst.append(items)

for i in range(len(agents_lst)):
    print("Agents:\n", agents_lst[i],"\nItems:\n", items_lst[i], "\n")
    print("Top Down:\n", fairpy.divide(top_down, agents_lst[i], items_lst[i].copy()))
    print("Top Down Alternating:\n", fairpy.divide(top_down_alternating, agents_lst[i], items_lst[i].copy()))
    print("Bottom Up:\n", fairpy.divide(bottom_up, agents_lst[i], items_lst[i].copy()))
    print("Bottom Up Alternating:\n", fairpy.divide(bottom_up_alternating, agents_lst[i], items_lst[i].copy()))
    print("Trump:\n", fairpy.divide(trump, agents_lst[i], items_lst[i].copy()))

