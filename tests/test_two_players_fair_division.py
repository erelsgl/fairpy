"""
Tests for two_players_fair_division.py

Two-player fair division of indivisible items: Comparison of algorithms
By: D. Marc Kilgour, Rudolf Vetschera

programmers: Itay Hasidi & Amichai Bitan
"""

from fairpy import fairpy
from fairpy.items.two_players_fair_division import *
import unittest

items = []
agents = []

agents.append([fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name='Alice'),
               fairpy.agents.AdditiveAgent({'a': 4, 'c': 2, 'd': 3, 'b': 1}, name='George')])
items.append(['a', 'b', 'c', 'd'])

agents.append([fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name='Alice'),
               fairpy.agents.AdditiveAgent({'a': 4, 'c': 2, 'd': 3, 'b': 1, 'e':6, 'f': 5}, name='George')])
items.append(['a', 'b', 'c', 'd', 'e', 'f'])

agents.append([fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}, name='Alice'),
               fairpy.agents.AdditiveAgent({'a': 4, 'c': 8, 'd': 5, 'b': 6, 'e': 7, 'f': 3, 'g': 1, 'h': 2}, name='George')])
items.append(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])

agents.append([fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10}, name='Alice'),
               fairpy.agents.AdditiveAgent({'a': 7, 'c': 4, 'd': 10, 'b': 2, 'e': 5, 'f': 3, 'g': 8, 'h': 1, 'i': 9, 'j': 6}, name='George')])
items.append(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])

agents.append([fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12}, name='Alice'),
               fairpy.agents.AdditiveAgent({'a': 10, 'c': 3, 'd': 7, 'b': 2, 'e' :9, 'f': 4, 'g': 8, 'h': 12, 'i': 5, 'j': 11, 'k': 1, 'l': 6}, name='George')])
items.append(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'])

print(agents, items)

def test_sequential():
    assert sequential(agents[0], items[0].copy()) == [{'Alice': ['a', 'c'], 'George': ['b', 'd']}]
    assert sequential(agents[1], items[1].copy()) == [{'Alice': ['a', 'c', 'e'], 'George': ['b', 'd', 'f']}]
    assert sequential(agents[2], items[2].copy()) == [{'Alice': ['a', 'b', 'c', 'e'], 'George': ['g', 'h', 'f', 'd']}]
    assert sequential(agents[3], items[3].copy()) == [{'Alice': ['a', 'b', 'd', 'e', 'g'], 'George': ['h', 'f', 'c', 'j', 'i']}, {'Alice': ['a', 'b', 'd', 'e', 'i'], 'George': ['h', 'f', 'c', 'j', 'g']}, {'Alice': ['a', 'c', 'd', 'e', 'g'], 'George': ['h', 'b', 'f', 'j', 'i']}, {'Alice': ['a', 'c', 'd', 'e', 'i'], 'George': ['h', 'b', 'f', 'j', 'g']}, {'Alice': ['a', 'c', 'd', 'e', 'g'], 'George': ['h', 'f', 'b', 'j', 'i']}, {'Alice': ['a', 'c', 'd', 'e', 'i'], 'George': ['h', 'f', 'b', 'j', 'g']}]
    assert sequential(agents[4], items[4].copy()) == [{'Alice': ['a', 'b', 'd', 'e', 'g', 'h'], 'George': ['k', 'c', 'f', 'i', 'l', 'j']}, {'Alice': ['a', 'c', 'd', 'e', 'g', 'h'], 'George': ['k', 'b', 'f', 'i', 'l', 'j']}]


def test_restricted_simple():
    assert restricted_simple(agents[0], items[0].copy()) == [{'Alice': ['a', 'c'], 'George': ['b', 'd']}]
    assert restricted_simple(agents[1], items[1].copy()) == [{'Alice': ['a', 'c', 'e'], 'George': ['b', 'd', 'f']}]
    assert restricted_simple(agents[2], items[2].copy()) == [{'Alice': ['a', 'b', 'c', 'e'], 'George': ['g', 'h', 'f', 'd']}]
    assert restricted_simple(agents[3], items[3].copy()) == [{'Alice': ['a', 'c', 'd', 'e', 'i'], 'George': ['h', 'b', 'f', 'j', 'g']}, {'Alice': ['a', 'c', 'd', 'e', 'g'], 'George': ['h', 'b', 'f', 'j', 'i']}, {'Alice': ['a', 'b', 'd', 'e', 'i'], 'George': ['h', 'f', 'c', 'j', 'g']}, {'Alice': ['a', 'b', 'd', 'e', 'g'], 'George': ['h', 'f', 'c', 'j', 'i']}]
    assert restricted_simple(agents[4], items[4].copy()) == [{'Alice': ['a', 'b', 'd', 'e', 'g', 'h'], 'George': ['k', 'c', 'f', 'i', 'l', 'j']}]



def test_singles_doubles():
    assert singles_doubles(agents[0], items[0].copy()) == [{'Alice': ['a', 'b'], 'George': ['d', 'c']}]
    assert singles_doubles(agents[1], items[1].copy()) == [{'Alice': ['e', 'a', 'b'], 'George': ['f', 'c', 'd']}]
    assert singles_doubles(agents[2], items[2].copy()) == [{'Alice': ['c', 'e', 'b', 'd'], 'George': ['h', 'g', 'f', 'a']}, {'Alice': ['c', 'e', 'b', 'a'], 'George': ['h', 'g', 'f', 'd']}]
    assert singles_doubles(agents[3], items[3].copy()) == [{'Alice': ['d', 'b', 'e', 'g', 'i'], 'George': ['j', 'a', 'c', 'f', 'h']}, {'Alice': ['d', 'b', 'e', 'f', 'i'], 'George': ['j', 'a', 'c', 'g', 'h']}, {'Alice': ['d', 'b', 'c', 'g', 'i'], 'George': ['j', 'a', 'e', 'f', 'h']}, {'Alice': ['d', 'b', 'c', 'f', 'i'], 'George': ['j', 'a', 'e', 'g', 'h']}, {'Alice': ['d', 'a', 'e', 'g', 'i'], 'George': ['j', 'c', 'b', 'f', 'h']}, {'Alice': ['d', 'a', 'e', 'g', 'h'], 'George': ['j', 'c', 'b', 'f', 'i']}, {'Alice': ['d', 'a', 'e', 'f', 'i'], 'George': ['j', 'c', 'b', 'g', 'h']}, {'Alice': ['d', 'a', 'b', 'g', 'i'], 'George': ['j', 'c', 'e', 'f', 'h']}, {'Alice': ['d', 'a', 'b', 'g', 'h'], 'George': ['j', 'c', 'e', 'f', 'i']}, {'Alice': ['d', 'a', 'b', 'f', 'i'], 'George': ['j', 'c', 'e', 'g', 'h']}]
    assert singles_doubles(agents[4], items[4].copy()) == [{'Alice': ['h', 'j', 'b', 'd', 'f', 'i'], 'George': ['l', 'k', 'a', 'c', 'e', 'g']}, {'Alice': ['h', 'j', 'b', 'd', 'f', 'g'], 'George': ['l', 'k', 'a', 'c', 'e', 'i']}, {'Alice': ['h', 'j', 'b', 'd', 'e', 'i'], 'George': ['l', 'k', 'a', 'c', 'f', 'g']}, {'Alice': ['h', 'j', 'b', 'd', 'e', 'g'], 'George': ['l', 'k', 'a', 'c', 'f', 'i']}, {'Alice': ['h', 'j', 'b', 'c', 'f', 'g'], 'George': ['l', 'k', 'a', 'd', 'e', 'i']}, {'Alice': ['h', 'j', 'b', 'c', 'e', 'i'], 'George': ['l', 'k', 'a', 'd', 'f', 'g']}, {'Alice': ['h', 'j', 'b', 'c', 'e', 'g'], 'George': ['l', 'k', 'a', 'd', 'f', 'i']}, {'Alice': ['h', 'j', 'a', 'b', 'f', 'i'], 'George': ['l', 'k', 'c', 'd', 'e', 'g']}, {'Alice': ['h', 'j', 'a', 'b', 'f', 'g'], 'George': ['l', 'k', 'c', 'd', 'e', 'i']}, {'Alice': ['h', 'j', 'a', 'b', 'e', 'i'], 'George': ['l', 'k', 'c', 'd', 'f', 'g']}, {'Alice': ['h', 'j', 'a', 'b', 'e', 'g'], 'George': ['l', 'k', 'c', 'd', 'f', 'i']}]


def test_iterated_singles_doubles():
    assert iterated_singles_doubles(agents[0], items[0].copy()) == [{'Alice': ['a', 'b'], 'George': ['d', 'c']}]
    assert iterated_singles_doubles(agents[1], items[1].copy()) == [{'Alice': ['e', 'a', 'b'], 'George': ['f', 'd', 'c']}]
    assert iterated_singles_doubles(agents[2], items[2].copy()) == [{'Alice': ['c', 'e', 'b', 'd'], 'George': ['h', 'g', 'f', 'a']}, {'Alice': ['c', 'e', 'b', 'a'], 'George': ['h', 'g', 'f', 'd']}]
    assert iterated_singles_doubles(agents[3], items[3].copy()) == [{'Alice': ['d', 'b', 'e', 'g', 'i'], 'George': ['j', 'a', 'c', 'f', 'h']}, {'Alice': ['d', 'b', 'e', 'f', 'i'], 'George': ['j', 'a', 'c', 'g', 'h']}, {'Alice': ['d', 'b', 'c', 'g', 'i'], 'George': ['j', 'a', 'e', 'f', 'h']}, {'Alice': ['d', 'b', 'c', 'f', 'i'], 'George': ['j', 'a', 'e', 'g', 'h']}, {'Alice': ['d', 'a', 'e', 'g', 'i'], 'George': ['j', 'c', 'b', 'f', 'h']}, {'Alice': ['d', 'a', 'e', 'g', 'h'], 'George': ['j', 'c', 'b', 'f', 'i']}, {'Alice': ['d', 'a', 'e', 'f', 'i'], 'George': ['j', 'c', 'b', 'g', 'h']}, {'Alice': ['d', 'a', 'b', 'g', 'i'], 'George': ['j', 'c', 'e', 'f', 'h']}, {'Alice': ['d', 'a', 'b', 'g', 'h'], 'George': ['j', 'c', 'e', 'f', 'i']}, {'Alice': ['d', 'a', 'b', 'f', 'i'], 'George': ['j', 'c', 'e', 'g', 'h']}]
    assert iterated_singles_doubles(agents[4], items[4].copy()) == [{'Alice': ['h', 'j', 'a', 'e', 'd', 'b'], 'George': ['l', 'k', 'i', 'g', 'f', 'c']}]


def test_s1():
    assert s1(agents[0], items[0].copy()) == [{'Alice': ['a', 'b'], 'George': ['d', 'c']}]
    assert s1(agents[1], items[1].copy()) == [{'Alice': ['e', 'b', 'd'], 'George': ['f', 'a', 'c']}, {'Alice': ['e', 'b', 'c'], 'George': ['f', 'a', 'd']}, {'Alice': ['e', 'a', 'b'], 'George': ['f', 'c', 'd']}]
    assert s1(agents[2], items[2].copy()) == [{'Alice': ['c', 'e', 'b', 'd'], 'George': ['h', 'g', 'f', 'a']}, {'Alice': ['c', 'e', 'b', 'a'], 'George': ['h', 'g', 'f', 'd']}]
    assert s1(agents[3], items[3].copy()) == [{'Alice': ['d', 'b', 'e', 'g', 'i'], 'George': ['j', 'a', 'c', 'f', 'h']}, {'Alice': ['d', 'b', 'e', 'g', 'h'], 'George': ['j', 'a', 'c', 'f', 'i']}, {'Alice': ['d', 'b', 'e', 'f', 'i'], 'George': ['j', 'a', 'c', 'g', 'h']}, {'Alice': ['d', 'b', 'e', 'f', 'h'], 'George': ['j', 'a', 'c', 'g', 'i']}, {'Alice': ['d', 'b', 'c', 'g', 'i'], 'George': ['j', 'a', 'e', 'f', 'h']}, {'Alice': ['d', 'b', 'c', 'g', 'h'], 'George': ['j', 'a', 'e', 'f', 'i']}, {'Alice': ['d', 'b', 'c', 'f', 'i'], 'George': ['j', 'a', 'e', 'g', 'h']}, {'Alice': ['d', 'b', 'c', 'f', 'h'], 'George': ['j', 'a', 'e', 'g', 'i']}, {'Alice': ['d', 'a', 'e', 'g', 'i'], 'George': ['j', 'c', 'b', 'f', 'h']}, {'Alice': ['d', 'a', 'e', 'g', 'h'], 'George': ['j', 'c', 'b', 'f', 'i']}, {'Alice': ['d', 'a', 'e', 'f', 'i'], 'George': ['j', 'c', 'b', 'g', 'h']}, {'Alice': ['d', 'a', 'e', 'f', 'h'], 'George': ['j', 'c', 'b', 'g', 'i']}, {'Alice': ['d', 'a', 'b', 'g', 'i'], 'George': ['j', 'c', 'e', 'f', 'h']}, {'Alice': ['d', 'a', 'b', 'g', 'h'], 'George': ['j', 'c', 'e', 'f', 'i']}, {'Alice': ['d', 'a', 'b', 'f', 'i'], 'George': ['j', 'c', 'e', 'g', 'h']}, {'Alice': ['d', 'a', 'b', 'f', 'h'], 'George': ['j', 'c', 'e', 'g', 'i']}]
    assert s1(agents[4], items[4].copy()) == [{'Alice': ['h', 'j', 'b', 'd', 'f', 'i'], 'George': ['l', 'k', 'a', 'c', 'e', 'g']}, {'Alice': ['h', 'j', 'b', 'd', 'f', 'g'], 'George': ['l', 'k', 'a', 'c', 'e', 'i']}, {'Alice': ['h', 'j', 'b', 'd', 'e', 'i'], 'George': ['l', 'k', 'a', 'c', 'f', 'g']}, {'Alice': ['h', 'j', 'b', 'd', 'e', 'g'], 'George': ['l', 'k', 'a', 'c', 'f', 'i']}, {'Alice': ['h', 'j', 'b', 'c', 'f', 'i'], 'George': ['l', 'k', 'a', 'd', 'e', 'g']}, {'Alice': ['h', 'j', 'b', 'c', 'f', 'g'], 'George': ['l', 'k', 'a', 'd', 'e', 'i']}, {'Alice': ['h', 'j', 'b', 'c', 'e', 'i'], 'George': ['l', 'k', 'a', 'd', 'f', 'g']}, {'Alice': ['h', 'j', 'b', 'c', 'e', 'g'], 'George': ['l', 'k', 'a', 'd', 'f', 'i']}, {'Alice': ['h', 'j', 'a', 'b', 'f', 'i'], 'George': ['l', 'k', 'c', 'd', 'e', 'g']}, {'Alice': ['h', 'j', 'a', 'b', 'f', 'g'], 'George': ['l', 'k', 'c', 'd', 'e', 'i']}, {'Alice': ['h', 'j', 'a', 'b', 'e', 'i'], 'George': ['l', 'k', 'c', 'd', 'f', 'g']}, {'Alice': ['h', 'j', 'a', 'b', 'e', 'g'], 'George': ['l', 'k', 'c', 'd', 'f', 'i']}]


def test_l1():
    assert l1(agents[0], items[0].copy()) == [{'Alice': ['a', 'b'], 'George': ['d', 'c']}]
    assert l1(agents[1], items[1].copy()) == [{'Alice': ['e', 'a', 'b'], 'George': ['f', 'd', 'c']}]
    assert l1(agents[2], items[2].copy()) == [{'Alice': ['c', 'e', 'b', 'd'], 'George': ['h', 'g', 'f', 'a']}, {'Alice': ['c', 'e', 'b', 'a'], 'George': ['h', 'g', 'f', 'd']}]
    assert l1(agents[3], items[3].copy()) == [{'Alice': ['d', 'b', 'e', 'g', 'i'], 'George': ['j', 'a', 'c', 'f', 'h']}, {'Alice': ['d', 'b', 'e', 'g', 'h'], 'George': ['j', 'a', 'c', 'f', 'i']}, {'Alice': ['d', 'b', 'e', 'f', 'i'], 'George': ['j', 'a', 'c', 'g', 'h']}, {'Alice': ['d', 'b', 'e', 'f', 'h'], 'George': ['j', 'a', 'c', 'g', 'i']}, {'Alice': ['d', 'b', 'c', 'g', 'i'], 'George': ['j', 'a', 'e', 'f', 'h']}, {'Alice': ['d', 'b', 'c', 'g', 'h'], 'George': ['j', 'a', 'e', 'f', 'i']}, {'Alice': ['d', 'b', 'c', 'f', 'i'], 'George': ['j', 'a', 'e', 'g', 'h']}, {'Alice': ['d', 'b', 'c', 'f', 'h'], 'George': ['j', 'a', 'e', 'g', 'i']}, {'Alice': ['d', 'a', 'e', 'g', 'i'], 'George': ['j', 'c', 'b', 'f', 'h']}, {'Alice': ['d', 'a', 'e', 'g', 'h'], 'George': ['j', 'c', 'b', 'f', 'i']}, {'Alice': ['d', 'a', 'e', 'f', 'i'], 'George': ['j', 'c', 'b', 'g', 'h']}, {'Alice': ['d', 'a', 'e', 'f', 'h'], 'George': ['j', 'c', 'b', 'g', 'i']}, {'Alice': ['d', 'a', 'b', 'g', 'i'], 'George': ['j', 'c', 'e', 'f', 'h']}, {'Alice': ['d', 'a', 'b', 'g', 'h'], 'George': ['j', 'c', 'e', 'f', 'i']}, {'Alice': ['d', 'a', 'b', 'f', 'i'], 'George': ['j', 'c', 'e', 'g', 'h']}, {'Alice': ['d', 'a', 'b', 'f', 'h'], 'George': ['j', 'c', 'e', 'g', 'i']}]
    assert l1(agents[4], items[4].copy()) == [{'Alice': ['h', 'j', 'a', 'e', 'd', 'b'], 'George': ['l', 'k', 'i', 'g', 'f', 'c']}]


def test_top_down():
    assert top_down(agents[0], items[0].copy()) == [['a', 'c'], ['b', 'd']]
    assert top_down(agents[1], items[1].copy()) == [['a', 'c', 'e'], ['b', 'd', 'f']]
    assert top_down(agents[2], items[2].copy()) == [['a', 'b', 'c', 'd'], ['g', 'h', 'f', 'e']]
    assert top_down(agents[3], items[3].copy()) == [['a', 'b', 'c', 'd', 'g'], ['h', 'f', 'e', 'j', 'i']]
    assert top_down(agents[4], items[4].copy()) == [['a', 'b', 'd', 'e', 'g', 'h'], ['k', 'c', 'f', 'i', 'l', 'j']]


def test_top_down_alternating():
    assert top_down_alternating(agents[0], items[0].copy()) == [['a', 'd'], ['b', 'c']]
    assert top_down_alternating(agents[1], items[1].copy()) == [['a', 'd', 'e'], ['b', 'c', 'f']]
    assert top_down_alternating(agents[2], items[2].copy()) == [['a', 'b', 'c', 'e'], ['g', 'h', 'f', 'd']]
    assert top_down_alternating(agents[3], items[3].copy()) == [['a', 'c', 'd', 'g', 'i'], ['h', 'b', 'f', 'e', 'j']]
    assert top_down_alternating(agents[4], items[4].copy()) == [['a', 'c', 'd', 'e', 'g', 'h'], ['k', 'b', 'f', 'i', 'l', 'j']]


def test_bottom_up():
    assert bottom_up(agents[0], items[0].copy()) == [['a', 'b'], ['d', 'c']]
    assert bottom_up(agents[1], items[1].copy()) == [['e', 'a', 'b'], ['f', 'd', 'c']]
    assert bottom_up(agents[2], items[2].copy()) == [['c', 'e', 'b', 'a'], ['h', 'g', 'f', 'd']]
    assert bottom_up(agents[3], items[3].copy()) == [['d', 'g', 'a', 'e', 'b'], ['j', 'i', 'h', 'f', 'c']]
    assert bottom_up(agents[4], items[4].copy()) == [['h', 'j', 'a', 'e', 'd', 'b'], ['l', 'k', 'i', 'g', 'f', 'c']]


def test_bottom_up_alternating():
    assert bottom_up_alternating(agents[0], items[0].copy()) == [['a', 'c'], ['d', 'b']]
    assert bottom_up_alternating(agents[1], items[1].copy()) == [['e', 'a', 'b'], ['f', 'd', 'c']]
    assert bottom_up_alternating(agents[2], items[2].copy()) == [['c', 'e', 'b', 'd'], ['h', 'g', 'f', 'a']]
    assert bottom_up_alternating(agents[3], items[3].copy()) == [['d', 'i', 'a', 'e', 'b'], ['j', 'h', 'g', 'f', 'c']]
    assert bottom_up_alternating(agents[4], items[4].copy()) == [['h', 'j', 'a', 'e', 'd', 'c'], ['l', 'k', 'i', 'g', 'f', 'b']]


def test_trump():
    assert trump(agents[0], items[0].copy()) == [['a', 'c'], ['b', 'd']]
    assert trump(agents[1], items[1].copy()) == [['a', 'c', 'e'], ['b', 'd', 'f']]
    assert trump(agents[2], items[2].copy()) == [['a', 'c', 'e', 'b'], ['g', 'h', 'f', 'd']]
    assert trump(agents[3], items[3].copy()) == [['a', 'c', 'd', 'g', 'i'], ['h', 'f', 'e', 'j', 'b']]
    assert trump(agents[4], items[4].copy()) == [['a', 'c', 'e', 'g', 'h', 'j'], ['k', 'b', 'i', 'l', 'f', 'd']]


if __name__ == '__main__':
    test_sequential()
    test_restricted_simple()
    test_singles_doubles()
    test_iterated_singles_doubles()
    test_s1()
    test_l1()
    test_top_down()
    test_top_down_alternating()
    test_bottom_up()
    test_bottom_up_alternating()
    test_trump()