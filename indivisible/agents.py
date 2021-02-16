#!python3

"""
Defines agents with various kinds of valuation functions over indivisible items.

Programmer: Erel Segal-Halevi
Since: 2020-04
"""


from abc import ABC, abstractmethod
from dicttools import stringify

import math, itertools
from fractions import Fraction

import fairpy.indivisible.partitions as partitions

from typing import *
Item = Any
Bundle = Set[Item]


class Agent(ABC):
    """
    An abstract class that describes a participant in an algorithm for indivisible item allocation.
    It can evaluate a set of items.
    It may also have a name, which is used only in demonstrations and for tracing. The name may be left blank (None).

    Optionally, it can also represent several agents with an identical valuation function.
    """

    def __init__(self, desired_items:Bundle, name:str=None, duplicity:int=1):
        """
        :param desired_items: the set of all goods that are desired by this agent/s.
        :param name [optional]: a display-name for the agent in logs and printouts.
        :param duplicity [optional]: the number of agent/s with the same valuation function.
        """
        if name is not None:
            self._name = name
        self.desired_items_list = sorted(desired_items)
        self.desired_items = set(desired_items)
        self.total_value_cache = self.value(self.desired_items)
        self.duplicity = duplicity

    def name(self):
        if hasattr(self, '_name') and self._name is not None:
            return self._name
        else:
            return "Anonymous"

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


    def best_index(self, allocation:List[Bundle])->int:
        """
        Returns an index of a bundle that is most-valuable for the agent.
        :param   partition: a list of k sets.
        :return: an index in [0,..,k-1] that points to a bundle whose value for the agent is largest.
        If there are two or more best bundles, the first index is returned.

        >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 3})
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

        >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4})
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

        >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4})
        >>> a.value_except_worst_c_goods(set("xy"), c=1)
        2
        """
        if len(bundle) <= c: return 0
        else: return max([
            self.value(bundle.difference(sub_bundle))
            for sub_bundle in itertools.combinations(bundle, c)
        ])


    def values_1_of_c_partitions(self, c:int=1):
        """
        Generates the minimum values in all partitions into c bundles.

        >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w":0})
        >>> sorted(a.values_1_of_c_partitions(c=2))
        [1, 2, 3]

        """
        for partition in partitions.partitions_to_exactly_c(self.desired_items_list, c):
            yield min([self.value(bundle) for bundle in partition])


    def value_1_of_c_MMS(self, c:int=1)->int:
        """
        Calculates the value of the 1-out-of-c maximin-share ( https://en.wikipedia.org/wiki/Maximin-share )

        >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4})
        >>> a.value_1_of_c_MMS(c=1)
        4
        >>> a.value_1_of_c_MMS(c=2)
        1
        >>> a.value_1_of_c_MMS(c=3)
        0
        >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w":0})
        >>> a.value_1_of_c_MMS(c=2)
        3
        """
        if c > len(self.desired_items):
            return 0
        else:
            return max(self.values_1_of_c_partitions(c))

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



class MonotoneAgent(Agent):
    """
    Represents an agent or several agents with a general monotone valuation function.

    >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4}, name="Alice")
    >>> a
    Alice is an agent with monotone valuations. Desired goods: ['x', 'y']
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
    >>> MonotoneAgent({"x": 1, "y": 2, "xy": 4}, duplicity=2)
    Anonymous are 2 agents with monotone valuations. Desired goods: ['x', 'y']

    """
    def __init__(self, map_bundle_to_value:Dict[Bundle,float], name:str=None, duplicity:int=1):
        """
        Initializes an agent with a given valuation function.
        :param map_bundle_to_value: a dict that maps each subset of goods to its value.
        :param duplicity: the number of agents with the same valuation.
        """
        self.map_bundle_to_value = {frozenset(bundle):value for bundle,value in  map_bundle_to_value.items()}
        self.map_bundle_to_value[frozenset()] = 0   # normalization: the value of the empty bundle is always 0
        desired_items = max(map_bundle_to_value.keys(), key=lambda k:map_bundle_to_value[k])
        super().__init__(desired_items, name=name, duplicity=duplicity)

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
        if self.duplicity==1:
            return "{} is an agent with monotone valuations. Desired goods: {}".format(self.name(), sorted(self.desired_items))
        else:
            return "{} are {} agents with monotone valuations. Desired goods: {}".format(self.name(), self.duplicity, sorted(self.desired_items))


class AdditiveAgent(Agent):
    """
    Represents an agent or several agents with an additive valuation function.

    >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w":0}, name="Alice")
    >>> a
    Alice is an agent with additive valuations: w=0 x=1 y=2 z=4
    >>> a.value(set())
    0
    >>> a.value({"w"})
    0
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
    >>> a.value_1_of_c_MMS(c=4)
    0
    >>> a.value_1_of_c_MMS(c=3)
    1
    >>> a.value_1_of_c_MMS(c=2)
    3
    >>> AdditiveAgent({"x": 1, "y": 2, "z": 4}, duplicity=2)
    Anonymous are 2 agents with additive valuations: x=1 y=2 z=4

    """
    def __init__(self, map_good_to_value:dict, name:str=None, duplicity:int=1):
        """
        Initializes an agent with a given additive valuation function.
        :param map_good_to_value: a dict that maps each single good to its value.
        :param duplicity: the number of agents with the same valuation.
        """
        self.map_good_to_value = map_good_to_value
        desired_items = set([g for g,v in map_good_to_value.items() if v>0])
        super().__init__(desired_items, name=name, duplicity=duplicity)

    def value(self, bundle:Bundle)->int:
        """
        Calculates the agent's value for the given set of goods.
        """
        return sum([self.map_good_to_value[g] for g in bundle])

    def value_except_best_c_goods(self, bundle:Bundle, c:int=1)->int:
        """
        Calculates the value of the given bundle when the "best" (at most) c goods are removed from it.
        Formally, it calculates:
              min [G subseteq bundle] value (bundle - G)
        where G is a subset of duplicity at most c.
        This is a subroutine in checking whether an allocation is EFc.

        >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4})
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

        >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4})
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

        >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4})
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

    def __repr__(self):
        values_as_string = " ".join(["{}={}".format(k,v) for k,v in sorted(self.map_good_to_value.items())])
        if self.duplicity==1:
            return "{} is an agent with additive valuations: {}".format(self.name(), values_as_string)
        else:
            return "{} are {} agents with additive valuations: {}".format(self.name(), self.duplicity, values_as_string)



class BinaryAgent(Agent):
    """
    Represents an agent with binary valuations, or several agents with the same binary valuations.

    >>> a = BinaryAgent({"x","y","z"}, name="Alice")
    >>> a
    Alice is a binary agent who wants ['x', 'y', 'z']
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
    >>> BinaryAgent({"x","y","z"}, duplicity=2)
    Anonymous are 2 binary agents who want ['x', 'y', 'z']
    """

    def __init__(self, desired_items:Bundle, name:str=None, duplicity:int=1):
        """
        Initializes an agent with a given set of desired goods.
        :param desired_items: a set of strings - each string is a good.
        :param duplicity: the number of agents with the same set of desired goods.
        """
        super().__init__(desired_items, name=name, duplicity=duplicity)

    def value(self, bundle:Bundle)->int:
        """
        Calculates the agent's value for the given set of goods.

        >>> BinaryAgent({"x","y","z"}).value({"w","x","y"})
        2
        >>> BinaryAgent({"x","y","z"}).value({"x","y"})
        2
        >>> BinaryAgent({"x","y","z"}).value("y")
        1
        >>> BinaryAgent({"x","y","z"}).value({"w"})
        0
        >>> BinaryAgent({"x","y","z"}).value(set())
        0
        >>> BinaryAgent(set()).value({"x","y","z"})
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
        if self.duplicity==1:
            return "{} is a binary agent who wants {}".format(self.name(), sorted(self.desired_items))
        else:
            return "{} are {} binary agents who want {}".format(self.name(), self.duplicity, sorted(self.desired_items))

if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
