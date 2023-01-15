#!python3

"""
Defines various kinds of valuation functions over indivisible items. Classes:
* Valuation
* MonotoneValuation
* AdditiveValuation
* BinaryValuation
* ValuationMatrix

Programmer: Erel Segal-Halevi
Since: 2021-04
"""


from abc import ABC, abstractmethod
from numbers import Number
from collections.abc import Iterable
import numpy as np

from dicttools import stringify

import math, itertools
from fractions import Fraction

from fairpy.bundles import FractionalBundle

from typing import *
Item = Any
Bundle = Set[Item]

import prtpy
from more_itertools import set_partitions


class Valuation(ABC):
    """
    An abstract class that describes a valuation function.
    It can evaluate a set of items.
    """

    def __init__(self, desired_items:Bundle):
        """
        :param desired_items: the set of all goods that are desired by this agent/s.
        """
        self.desired_items_list = sorted(desired_items)
        self.desired_items = set(desired_items)
        self.total_value_cache = self.value(self.desired_items)

    @abstractmethod
    def value(self, bundle:Bundle)->float:
        """
        :return: the value for this agent of the given set of items.
        """
        pass

    def total_value(self)->float:
        """
        :return: the value for this agent of all items together.
        """
        return self.total_value_cache

    def all_items(self):
        """
        :return: the set of all items handled by this valuation.
        """
        return self.desired_items

    def best_index(self, allocation:List[Bundle])->int:
        """
        Returns an index of a bundle that is most-valuable for the agent.
        :param   partition: a list of k sets.
        :return: an index in [0,..,k-1] that points to a bundle whose value for the agent is largest.
        If there are two or more best bundles, the first index is returned.

        >>> a = AdditiveValuation({"x": 1, "y": 2, "z": 3})
        >>> a.best_index(["xy","z"])
        0
        >>> a.best_index(["y","xz"])
        1
        """
        return max(range(len(allocation)), key=lambda i:self.value(allocation[i]))


    def value_except_best_c_goods(self, bundle:Bundle, c:int=1)->int:
        """
        Calculates the value of the given bundle when the "best" (at most) c goods are removed from it.
        Formally, it calculates:
              min [G subseteq bundle] value (bundle - G)
        where G is a subset of duplicity at most c.
        This is a subroutine in checking whether an allocation is EF1.

        >>> a = MonotoneValuation({"x": 1, "y": 2, "xy": 4})
        >>> a.value_except_best_c_goods(set("xy"), c=1)
        1
        >>> a.value_except_best_c_goods(set("xy"), c=2)
        0
        >>> a.value_except_best_c_goods(set("x"), c=1)
        0
        >>> a.value_except_best_c_goods(set(), c=1)
        0
        """
        if len(bundle) <= c: return 0
        else: return min([
            self.value(bundle.difference(sub_bundle))
            for sub_bundle in itertools.combinations(bundle, c)
        ])

    def value_except_worst_c_goods(self, bundle:Bundle, c:int=1)->int:
        """
        Calculates the value of the given bundle when the "worst" c goods are removed from it.
        Formally, it calculates:
              max [G subseteq bundle] value (bundle - G)
        where G is a subset of duplicity at most c.
        This is a subroutine in checking whether an allocation is EFx.

        >>> a = MonotoneValuation({"x": 1, "y": 2, "xy": 4})
        >>> a.value_except_worst_c_goods(set("xy"), c=1)
        2
        """
        if len(bundle) <= c: return 0
        else: return max([
            self.value(bundle.difference(sub_bundle))
            for sub_bundle in itertools.combinations(bundle, c)
        ])

    def value_1_of_c_MMS(self, c:int=1)->int:
        """
        Calculates the value of the 1-out-of-c maximin-share ( https://en.wikipedia.org/wiki/Maximin-share )

        >>> a = MonotoneValuation({"x": 1, "y": 2, "xy": 4})
        >>> a.value_1_of_c_MMS(c=1)
        4
        >>> a.value_1_of_c_MMS(c=2)
        1
        >>> a.value_1_of_c_MMS(c=3)
        0
        """
        if c > len(self.desired_items):
            return 0
        else:
            return max(
                min([self.value(bundle) for bundle in partition])
                for partition in set_partitions(self.desired_items_list, c)
            )

    def value_proportional_except_c(self, num_of_agents:int, c:int):
        """
        Calculates the proportional value of that agent, when the c most valuable goods are ignored.
        This is a subroutine in checking whether an allocation is PROPc.
        """
        return Fraction(self.value_except_best_c_goods(self.desired_items, c) , num_of_agents)

    def is_EFc(self, own_bundle:Bundle, all_bundles:List[Bundle], c: int) -> bool:
        """
        Checks whether the current agent finds the given allocation envy-free-except-c-goods (EFc).
        :param own_bundle:   the bundle consumed by the current agent.
        :param all_bundles:  the list of all bundles.
        :return: True iff the current agent finds the allocation EFc.
        """
        own_value = self.value(own_bundle)
        for other_bundle in all_bundles:
            if own_value < self.value_except_best_c_goods(other_bundle, c):
                return False
        return True

    def is_EF1(self, own_bundle:Bundle, all_bundles:List[Bundle]) -> bool:
        """
        Checks whether the current agent finds the given allocation envy-free-except-1-good (EF1).
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation EF1.
        """
        return self.is_EFc(own_bundle, all_bundles, c=1)

    def is_EFx(self, own_bundle:Bundle, all_bundles:List[Bundle])->bool:
        """
        Checks whether the current agent finds the given allocation EFx.
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation EFx.
        """
        own_value = self.value(own_bundle)
        for other_bundle in all_bundles:
            if own_value < self.value_except_worst_c_goods(other_bundle, c=1):
                return False
        return True

    def is_EF(self, own_bundle:Bundle, all_bundles:List[Bundle])->bool:
        """
        Checks whether the current agent finds the given allocation envy-free.
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation envy-free.
        """
        own_value = self.value(own_bundle)
        for other_bundle in all_bundles:
            if own_value < self.value(other_bundle):
                return False
        return True

    def is_1_of_c_MMS(self, own_bundle:Bundle, c:int, approximation_factor:float=1)->bool:
        return self.value(own_bundle) >= self.value_1_of_c_MMS(c)*approximation_factor

    def is_PROPc(self, own_bundle:Bundle, num_of_agents:int, c:int)->bool:
        """
        Checks whether the current agent finds the given allocation PROPc
        When there are k agents, an allocation is PROPc for an agent
        if his value for his own bundle is at least 1/k of his value for the following bundle:
            [all the goods except the best c].
        :param own_bundle:   the bundle consumed by the current agent.
        :param num_of_agents:  the total number of agents.
        :param c: how many best-goods to exclude from the total bundle.
        :return: True iff the current agent finds the allocation PROPc.
        """
        return self.value(own_bundle) >= self.value_proportional_except_c(num_of_agents, c)

    def is_PROP(self, own_bundle:Bundle, num_of_agents:int)->bool:
        """
        Checks whether the current agent finds the given allocation proportional.
        :param own_bundle:     the bundle consumed by the current agent.
        :param num_of_agents:  the total number of agents.
        :return: True iff the current agent finds the allocation PROPc.
        """
        return self.is_PROPc(own_bundle, num_of_agents, c=0)



class MonotoneValuation(Valuation):
    """
    Represents a general monotone valuation function.

    >>> a = MonotoneValuation({"x": 1, "y": 2, "xy": 4})
    >>> a
    Monotone valuation on ['x', 'y'].
    >>> a.value("")
    0
    >>> a.value({"x"})
    1
    >>> a.value("yx")
    4
    >>> a.value({"y","x"})
    4
    >>> a.is_EF({"x"}, [{"y"}])
    False
    >>> a.is_EF1({"x"}, [{"y"}])
    True
    >>> a.is_EFx({"x"}, [{"y"}])
    True
    """
    def __init__(self, map_bundle_to_value:Dict[Bundle,float]):
        """
        Initializes an agent with a given valuation function.
        :param map_bundle_to_value: a dict that maps each subset of goods to its value.
        """
        self.map_bundle_to_value = {frozenset(bundle):value for bundle,value in  map_bundle_to_value.items()}
        self.map_bundle_to_value[frozenset()] = 0   # normalization: the value of the empty bundle is always 0
        desired_items = max(map_bundle_to_value.keys(), key=lambda k:map_bundle_to_value[k])
        super().__init__(desired_items)

    def value(self, bundle:Bundle)->int:
        """
        Calculates the agent's value for the given set of goods.
        """
        bundle = frozenset(bundle)
        if bundle in self.map_bundle_to_value:
            return self.map_bundle_to_value[bundle]
        else:
            raise ValueError(f"The value of {bundle} is not specified in the valuation function")

    def __repr__(self):
        return f"Monotone valuation on {sorted(self.desired_items)}."


class AdditiveValuation(Valuation):
    """
    Represents an additive valuation function.

    >>> ### Initialize from a dict
    >>> a = AdditiveValuation({"x": 1, "y": 2, "z": 4, "w":0})
    >>> a
    Additive valuation: w=0 x=1 y=2 z=4.
    >>> a.value(set())
    0
    >>> a.value({"w"})
    0
    >>> a.value("x")
    1
    >>> a.value({"x"})
    1
    >>> a.value("yx")
    3
    >>> a.value({"y","x","z"})
    7
    >>> a.is_EF({"y"}, [{"y"},{"x"},{"z"},set()])
    False
    >>> a.is_PROP({"y"}, 4)
    True
    >>> a.is_PROP({"y"}, 3)
    False
    >>> a.is_PROPc({"y"}, 3, c=1)
    True
    >>> a.is_EF1({"y"}, [{"x","z"}])
    True
    >>> a.is_EF1({"x"}, [{"y","z"}])
    False
    >>> a.is_EFx({"x"}, [{"y"}])
    True
    >>> int(a.value_1_of_c_MMS(c=4))
    0
    >>> int(a.value_1_of_c_MMS(c=3))
    1
    >>> int(a.value_1_of_c_MMS(c=2))
    3
    >>> list(a.all_items())
    ['x', 'y', 'z', 'w']

    >>> ### Initialize from a dict with long names
    >>> a = AdditiveValuation({"blue": 1, "green": 2, "z": 4, "w": 7})
    >>> a
    Additive valuation: blue=1 green=2 w=7 z=4.
    >>> a.value("blue")
    1
    >>> a.value({"green"})
    2
    >>> a.value({"blue","green"})
    3
    >>> a.value("zw")
    11

    >>> ### Initialize from a list
    >>> a = AdditiveValuation([11,22,44,0])  
    >>> a
    Additive valuation: v0=11 v1=22 v2=44 v3=0.
    >>> a.value(set())
    0
    >>> a.value(0)
    11
    >>> a.value({0})
    11
    >>> a.value({1})
    22
    >>> a.value({1,2})
    66
    >>> a.value({1,2,0})
    77
    >>> a.value(FractionalBundle(fractions=[0,0.5,0.5]))
    33.0
    >>> a.is_PROP({1}, 4)
    True
    >>> a.is_PROP({1}, 3)
    False
    >>> a.is_PROPc({1}, 3, c=1)
    True
    >>> a.is_EF1({1}, [{0,2}])
    True
    >>> a.is_EF1({0}, [{1,2}])
    False
    >>> int(a.value_1_of_c_MMS(c=4))
    0
    >>> int(a.value_1_of_c_MMS(c=3))
    11
    >>> int(a.value_1_of_c_MMS(c=2))
    33
    >>> a.all_items()
    {0, 1, 2, 3}
    """
    def __init__(self, map_good_to_value):
        """
        Initializes an agent with a given additive valuation function.
        :param map_good_to_value: a dict that maps each single good to its value, or a list that lists the values of individual items.
        """
        if isinstance(map_good_to_value, AdditiveValuation):
            map_good_to_value = map_good_to_value.map_good_to_value
            desired_items = map_good_to_value.desired_items
            all_items = map_good_to_value._all_items
        elif isinstance(map_good_to_value, dict):
            all_items = map_good_to_value.keys()
            desired_items = set([g for g in all_items if map_good_to_value[g]>0])
        elif isinstance(map_good_to_value, list) or isinstance(map_good_to_value, np.ndarray):
            all_items =  set(range(len(map_good_to_value)))
            desired_items = set([g for g in all_items if map_good_to_value[g]>0])
        else:
            raise ValueError(f"Input to AdditiveValuation should be a dict or a list, but it is {type(map_good_to_value)}")

        self.map_good_to_value = map_good_to_value
        self._all_items = all_items
        super().__init__(desired_items)

    def value(self, bundle:Bundle)->int:
        """
        Calculates the agent's value for the given good or set of goods.
        """
        if bundle is None:
            return 0
        elif isinstance(bundle,FractionalBundle):
            return sum([self.map_good_to_value[g] * fraction for g,fraction in bundle.enumerate_fractions()])
        elif isinstance(bundle, str):
            if bundle in self.map_good_to_value:
                return self.map_good_to_value[bundle]
            else:
                return sum([self.map_good_to_value[g] for g in bundle])
        elif isinstance(bundle, Iterable):   # set, list, str, etc.
            return sum([self.map_good_to_value[g] for g in bundle])
        elif isinstance(bundle,Number):                              # individual item
            return self.map_good_to_value[bundle]
        else:
            raise TypeError(f"Unsupported bundle type: {type(bundle)}")

    def all_items(self):
        return self._all_items

    def value_except_best_c_goods(self, bundle:Bundle, c:int=1)->int:
        """
        Calculates the value of the given bundle when the "best" (at most) c goods are removed from it.
        Formally, it calculates:
              min [G subseteq bundle] value (bundle - G)
        where G is a subset of duplicity at most c.
        This is a subroutine in checking whether an allocation is EFc.

        >>> a = AdditiveValuation({"x": 1, "y": 2, "z": 4})
        >>> a.value_except_best_c_goods(set("xyz"), c=1)
        3
        >>> a.value_except_best_c_goods(set("xyz"), c=2)
        1
        >>> a.value_except_best_c_goods(set("xy"), c=1)
        1
        >>> a.value_except_best_c_goods(set("xy"), c=2)
        0
        >>> a.value_except_best_c_goods(set("x"), c=1)
        0
        >>> a.value_except_best_c_goods(set(), c=1)
        0
        """
        if len(bundle) <= c: return 0
        sorted_bundle = sorted(bundle, key=lambda g: -self.map_good_to_value[g]) # sort the goods from best to worst
        return self.value(sorted_bundle[c:])  # remove the best c goods

    def value_except_worst_c_goods(self, bundle:Bundle, c:int=1)->int:
        """
        Calculates the value of the given bundle when the "worst" c goods are removed from it.
        Formally, it calculates:
              max [G subseteq bundle] value (bundle - G)
        where G is a subset of duplicity at most c.
        This is a subroutine in checking whether an allocation is EFx.

        >>> a = AdditiveValuation({"x": 1, "y": 2, "z": 4})
        >>> a.value_except_worst_c_goods(set("xyz"), c=1)
        6
        >>> a.value_except_worst_c_goods(set("xy"), c=1)
        2
        >>> a.value_except_worst_c_goods(set("xy"), c=2)
        0
        >>> a.value_except_worst_c_goods(set("x"), c=1)
        0
        >>> a.value_except_worst_c_goods(set(), c=1)
        0
        """
        if len(bundle) <= c: return 0
        sorted_bundle = sorted(bundle, key=lambda g: self.map_good_to_value[g])  # sort the goods from worst to best:
        return self.value(sorted_bundle[c:])  # remove the worst c goods


    def value_of_cth_best_good(self, c:int)->int:
        """
        Return the value of the agent's c-th most valuable good.

        >>> a = AdditiveValuation({"x": 1, "y": 2, "z": 4})
        >>> a.value_of_cth_best_good(1)
        4
        >>> a.value_of_cth_best_good(2)
        2
        >>> a.value_of_cth_best_good(3)
        1
        >>> a.value_of_cth_best_good(4)
        0
        """
        if c > len(self.desired_items):
            return 0
        else:
            sorted_values = sorted(self.map_good_to_value.values(), reverse=True)
            return sorted_values[c-1]

    def partition_1_of_c_MMS(self, c: int, items: list) -> List[Bundle]:
        """
        Compute a 1-out-of-c MMS partition of the given items.
        :param c: number of bundles in the partition.
        :param items: A list of the items to divide.
        :return: The partitioning that holds the MMS
        AUTHOR: Shai Aharon.
        SINCE: 2021-02

        >>> items = ['a','b' ,'c', 'd', 'e', 'f']
        >>> item_values = {'a': 1, 'b': 2, 'c': 4, 'd': 8, 'e': 16, 'f': 32}
        >>> valuation = AdditiveValuation(item_values)
        >>> mms_part = valuation.partition_1_of_c_MMS(3,items)
        >>> [sorted(x) for x in mms_part]
        [['a', 'b', 'c', 'd'], ['e'], ['f']]
        >>> mms_part = valuation.partition_1_of_c_MMS(4,items)
        >>> [sorted(x) for x in mms_part]
        [['a', 'b', 'c'], ['d'], ['e'], ['f']]
        >>> mms_part = valuation.partition_1_of_c_MMS(4,['a','b','c']) # just verify that there is no exception
        """
        partition = prtpy.partition(
            algorithm=prtpy.partitioning.integer_programming,
            numbins=c,
            items=items,
            valueof=lambda item: self.value(item),
            objective=prtpy.obj.MaximizeSmallestSum,
            outputtype=prtpy.out.Partition
        )
        return [set(x) for x in partition]


    def value_1_of_c_MMS(self, c:int=1)->int:
        """
        Calculates the value of the 1-out-of-c maximin-share ( https://en.wikipedia.org/wiki/Maximin-share )

        >>> a = AdditiveValuation({"x": 1, "y": 2, "z": 4, "w":0})
        >>> a.value_1_of_c_MMS(c=2)
        3.0
        """
        if c > len(self.desired_items):
            return 0
        else:
            return prtpy.partition(
                algorithm=prtpy.partitioning.integer_programming,
                numbins=c,
                items=self.desired_items,
                valueof=lambda item: self.value(item),
                objective=prtpy.obj.MaximizeSmallestSum,
                outputtype=prtpy.out.SmallestSum
            )



    def __repr__(self):
        if isinstance(self.map_good_to_value,dict):
            values_as_string = " ".join([f"{k}={v}" for k,v in sorted(self.map_good_to_value.items())])
        elif isinstance(self.map_good_to_value,list) or isinstance(self.map_good_to_value,np.ndarray):
            values_as_string = " ".join([f"v{i}={self.map_good_to_value[i]}" for i in range(len(self.map_good_to_value))])
        return f"Additive valuation: {values_as_string}."



class BinaryValuation(Valuation):
    """
    Represents an additive binary valuation function.

    >>> a = BinaryValuation({"x","y","z"})
    >>> a
    Binary valuation who wants ['x', 'y', 'z'].
    >>> a.value({"x","w"})
    1
    >>> a.value({"y","z"})
    2
    >>> a.is_EF({"x","w"},[{"y","z"}])
    False
    >>> a.is_EF1({"x","w"},[{"y","z"}])
    True
    >>> a.is_EF1({"v","w"},[{"y","z"}])
    False
    >>> a.is_EF1(set(),[{"y","w"}])
    True
    >>> a.is_EF1(set(),[{"y","z"}])
    False
    >>> a.is_1_of_c_MMS({"x","w"}, c=2)
    True
    >>> a.is_1_of_c_MMS({"w"}, c=2)
    False
    """

    def __init__(self, desired_items:Bundle):
        """
        Initializes an agent with a given set of desired goods.
        :param desired_items: a set of strings - each string is a good.
        """
        super().__init__(desired_items)

    def value(self, bundle:Bundle)->int:
        """
        Calculates the agent's value for the given set of goods.

        >>> BinaryValuation({"x","y","z"}).value({"w","x","y"})
        2
        >>> BinaryValuation({"x","y","z"}).value({"x","y"})
        2
        >>> BinaryValuation({"x","y","z"}).value("y")
        1
        >>> BinaryValuation({"x","y","z"}).value({"w"})
        0
        >>> BinaryValuation({"x","y","z"}).value(set())
        0
        >>> BinaryValuation(set()).value({"x","y","z"})
        0
        """
        bundle = set(bundle)
        return len(self.desired_items.intersection(bundle))

    def value_except_best_c_goods(self, bundle:Bundle, c:int=1)->int:
        if len(bundle) <= c: return 0
        return self.value(bundle) - c

    def value_except_worst_c_goods(self, bundle:Bundle, c:int=1)->int:
        if len(bundle) <= c: return 0
        return self.value(bundle) - c

    def value_of_cth_best_good(self, c:int)->int:
        return 1 if self.total_value_cache >= c else 0

    def value_1_of_c_MMS(self, c:int=1)->int:
        return math.floor(self.total_value_cache / c)

    def __repr__(self):
        return f"Binary valuation who wants {sorted(self.desired_items)}."


class ValuationMatrix:
    """
    A valuation matrix is a matrix v in which each row represents an agent, 
        each column represents an object, and v[i][j] is the value of agent i to object j.
    
    It can be initialized by:

    * A 2-dimensional numpy array (np.ndarray);
    * A list of lists;
    * Another ValuationMatrix.

    >>> v = ValuationMatrix([[1,4,7],[6,3,0]])    # Initialize from a list of lists
    >>> v[0,1]   # value for agent 0 of item 1
    4
    >>> v[0][1]  # value for agent 0 of item 1
    4
    >>> v[0]     # values for agent 0
    array([1, 4, 7])
    >>> v
    [[1 4 7]
     [6 3 0]]
    >>> for agent in v.agents(): print(v[agent])
    [1 4 7]
    [6 3 0]
    >>> v.agent_value_for_bundle(0, [0,2])
    8
    >>> v.agent_value_for_bundle(0, FractionalBundle([1,0,1]))  # equivalent to the above
    8
    >>> v.agent_value_for_bundle(0, FractionalBundle([0.5,0,1.5]))
    11.0
    >>> v.agent_value_for_bundle(1, [1,0])
    9
    >>> v.agent_value_for_bundle(1, None)
    0
    >>> v.without_agent(0)
    [[6 3 0]]
    >>> v.without_object(1)
    [[1 7]
     [6 0]]
    >>> v = ValuationMatrix(np.ones([2,3]))        # Initialize from a numpy array.
    >>> v
    [[1. 1. 1.]
     [1. 1. 1.]]
    >>> int(v.agent_value_for_bundle(0,[1,2]))
    2
    >>> v2 = ValuationMatrix(v)
    >>> v2
    [[1. 1. 1.]
     [1. 1. 1.]]
    """

    def __init__(self, valuation_matrix: np.ndarray):
        if isinstance(valuation_matrix, list):
            valuation_matrix = np.array(valuation_matrix)
        elif isinstance(valuation_matrix, ValuationMatrix):
            valuation_matrix = valuation_matrix._v

        self._v = valuation_matrix
        self.num_of_agents = len(valuation_matrix)
        self.num_of_objects = 0 if self.num_of_agents == 0 else len(valuation_matrix[0])

    def agents(self):
        return range(self.num_of_agents)

    def objects(self):
        return range(self.num_of_objects)

    def __getitem__(self, key):
        if isinstance(key,tuple):
            return self._v[key[0]][key[1]]  # agent's value for a single object
        else:
            return self._v[key]             # agent's values for all objects

    def agent_value_for_bundle(self, agent:int, bundle:Bundle)->float:
        if bundle is None:
            return 0
        elif isinstance(bundle,FractionalBundle):
            return sum([self._v[agent][object] * fraction for object,fraction in enumerate(bundle.fractions)])
        else:
            return sum([self._v[agent][object] for object in bundle])


    def without_agent(self, agent:int)->'ValuationMatrix':
        """
        :return a copy of this valuation matrix, in which the given agent is removed.
        """
        if isinstance(agent,int):
            return ValuationMatrix(np.delete(self._v, agent, axis=0))
        else:
            raise IndexError(f"agent index should be an integer, but it is {agent}")
            

    def without_object(self, object:int)->'ValuationMatrix':
        """
        :return a copy of this valuation matrix, in which the given object is removed.
        """
        if isinstance(object,int):
            return ValuationMatrix(np.delete(self._v, object, axis=1))
        else:
            raise IndexError(f"object index should be an integer, but it is {object}")

    def submatrix(self, agents: List[int], objects: List[int]):
        """
        :return a submatrix of this valuation matrix, containing only specified agents and objects.
        """
        return ValuationMatrix(self._v[np.ix_(agents, objects)])

    def verify_ordered(self)->bool:
        """
        Verifies that the instance is ordered --- all valuations are ordered by descending value.

        >>> v = ValuationMatrix([[7,4,1],[6,3,0]])
        >>> v.verify_ordered()
        >>> v = ValuationMatrix([[7,4,1],[6,0,3]])
        >>> v.verify_ordered()
        Traceback (most recent call last):
        ...
        ValueError: Valuations of agent 1 are not ordered: [6 0 3]
        """
        for i in self.agents():
            v_i = self._v[i]
            if any(v_i[j] < v_i[j+1] for j in range(self.num_of_objects-1)):
                raise ValueError(f"Valuations of agent {i} are not ordered: {v_i}")

    def total_values(self) -> np.ndarray:
        """
        Returns a 1-dimensional array in which elemenet i is the total value of agent i for all items.
        """
        return np.sum(self._v, axis=1, keepdims=False)

    def normalize(self) -> float:
        """
        Normalize valuation matrix so that each agent has equal total value of all items.
        In case of integer values they remain integer to avoid floating point inaccuracies.
        :return the common value after normalization.

        >>> v = ValuationMatrix([[5., 12., 3],[30, 13, 7]])
        >>> v.normalize()
        1
        >>> v
        [[0.25 0.6  0.15]
         [0.6  0.26 0.14]]
        >>> v = ValuationMatrix([[5, 12, 3],[20, 2, 8]])
        >>> v.normalize()
        60
        >>> v
        [[15 36  9]
         [40  4 16]]
        """
        total_values = self.total_values()
        if issubclass(self._v.dtype.type, np.integer):
            new_total_value = np.lcm.reduce(total_values)
            for i in self.agents():
                self._v[i] *= (new_total_value // total_values[i])
            return new_total_value
        else:
            for i in self.agents():
                self._v[i] /= total_values[i]
            return 1

    def verify_normalized(self) -> int:
        """
        Check if total value of each agent is the same. Return total value.
        """
        total_values = np.sum(self._v, axis=1)
        if not np.allclose(total_values, total_values[0]):
            raise ValueError(f"Valuation matrix is not normalized. Total values: {total_values}")
        return total_values[0]

    def equals(self, other)->bool:
        return np.array_equal(self._v, other._v)

    def __repr__(self):
        return np.array2string (self._v, max_line_width=100)		



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))

