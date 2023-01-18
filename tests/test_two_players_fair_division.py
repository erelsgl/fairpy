from fairpy import fairpy
from fairpy.items.two_players_fair_division import *


Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name='Alice')
George = fairpy.agents.AdditiveAgent({'a': 4, 'c': 2, 'd': 3, 'b': 1}, name='George')


def test_sequential():
    assert sequential([Alice, George], ['a', 'b', 'c', 'd']) == \
           [{'Alice': ['a', 'c'], 'George': ['b', 'd']}]


def test_restricted_simple():
    assert restricted_simple([Alice, George], ['a', 'b', 'c', 'd']) == \
           [{'Alice': ['a', 'c'], 'George': ['b', 'd']}]


def test_singles_doubles():
    assert singles_doubles([Alice, George], ['a', 'b', 'c', 'd']) == \
           [{'Alice': ['a', 'b'], 'George': ['d', 'c']}]


def test_iterated_singles_doubles():
    assert iterated_singles_doubles([Alice, George], ['a', 'b', 'c', 'd']) == \
           [{'Alice': ['a', 'b'], 'George': ['d', 'c']}]


def test_s1():
    assert s1([Alice, George], ['a', 'b', 'c', 'd']) == \
           [{'Alice': ['a', 'b'], 'George': ['d', 'c']}]


def test_l1():
    assert l1([Alice, George], ['a', 'b', 'c', 'd']) == \
           [{'Alice': ['a', 'b'], 'George': ['d', 'c']}]


def test_top_down():
    assert top_down([Alice, George], ['a', 'b', 'c', 'd']) == \
           [{'Alice': ['a', 'c'], 'George': ['b', 'd']}]


def test_top_down_alternating():
    assert top_down_alternating([Alice, George], ['a', 'b', 'c', 'd']) == \
           [{'Alice': ['a', 'd'], 'George': ['b', 'c']}]


def test_bottom_up():
    assert bottom_up([Alice, George], ['a', 'b', 'c', 'd']) == \
           [{'Alice': ['a', 'b'], 'George': ['d', 'c']}]


def test_bottom_up_alternating():
    assert bottom_up_alternating([Alice, George], ['a', 'b', 'c', 'd']) == \
        [{'Alice': ['a', 'c'], 'George': ['d', 'b']}]


def test_trump():
    assert trump([Alice, George], ['a', 'b', 'c', 'd']) == \
        [{'Alice': ['a', 'c'], 'George': ['b', 'd']}]

