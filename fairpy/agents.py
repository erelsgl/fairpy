#!python3

"""
Defines agents with various kinds of valuation functions.

Programmer: Erel Segal-Halevi
Since: 2020-04
"""

from fairpy.items.valuations import *
from fairpy.cake.valuations  import *

from abc import ABC, abstractmethod
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

    def __init__(self, valuation:Valuation, name:str=None, duplicity:int=1):
        """
        :param valuation: represents the agents' valuation function.
        :param name [optional]: a display-name for the agent in logs and printouts.
        :param duplicity [optional]: the number of agent/s with the same valuation function.
        """
        self.valuation = valuation
        if name is not None:
            self._name = name
        self.duplicity = duplicity

    def name(self):
        if hasattr(self, '_name') and self._name is not None:
            return self._name
        else:
            return "Anonymous"

    def value(self, bundle:Bundle)->float:
        return self.valuation.value(bundle)

    def total_value(self)->float:
        return self.valuation.total_value()

    def mark(self, start:float, target_value:float)->float:
        return self.valuation.mark(start, target_value)

    def eval(self, start:float, end:float)->float:
        return self.valuation.eval(start, end)

    def cake_length(self)->float:
        return self.valuation.cake_length()

    def partition_values(self, partition:list)->float:
        return self.valuation.partition_values(partition)

    def all_items(self):
        return self.valuation.all_items()


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
        return self.valuation.best_index(allocation)


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
        return self.valuation.value_except_best_c_goods(bundle,c)

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
        return self.valuation.value_except_worst_c_goods(bundle,c)


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
        >>> int(a.value_1_of_c_MMS(c=2))
        3
        """
        return self.valuation.value_1_of_c_MMS(c)

    def partition_1_of_c_MMS(self, c: int, items: list) -> List[Bundle]:
        return self.valuation.partition_1_of_c_MMS(c, items)


    def value_proportional_except_c(self, num_of_agents:int, c:int):
        """
        Calculates the proportional value of that agent, when the c most valuable goods are ignored.
        This is a subroutine in checking whether an allocation is PROPc.
        """
        return self.valuation.value_proportional_except_c(num_of_agents, c)

    def is_EFc(self, own_bundle:Bundle, all_bundles:List[Bundle], c: int) -> bool:
        """
        Checks whether the current agent finds the given allocation envy-free-except-c-goods (EFc).
        :param own_bundle:   the bundle consumed by the current agent.
        :param all_bundles:  the list of all bundles.
        :return: True iff the current agent finds the allocation EFc.
        """
        return self.valuation.is_EFc(own_bundle, all_bundles, c)

    def is_EF1(self, own_bundle:Bundle, all_bundles:List[Bundle]) -> bool:
        """
        Checks whether the current agent finds the given allocation envy-free-except-1-good (EF1).
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation EF1.
        """
        return self.valuation.is_EF1(own_bundle, all_bundles)

    def is_EFx(self, own_bundle:Bundle, all_bundles:List[Bundle])->bool:
        """
        Checks whether the current agent finds the given allocation EFx.
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation EFx.
        """
        return self.valuation.is_EFx(own_bundle, all_bundles)

    def is_EF(self, own_bundle:Bundle, all_bundles:List[Bundle])->bool:
        """
        Checks whether the current agent finds the given allocation envy-free.
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation envy-free.
        """
        return self.valuation.is_EF(own_bundle, all_bundles)

    def is_1_of_c_MMS(self, own_bundle:Bundle, c:int, approximation_factor:float=1)->bool:
        return self.valuation.is_1_of_c_MMS(own_bundle, c, approximation_factor)

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
        return self.valuation.is_PROPc(own_bundle, num_of_agents, c)

    def is_PROP(self, own_bundle:Bundle, num_of_agents:int)->bool:
        """
        Checks whether the current agent finds the given allocation proportional.
        :param own_bundle:     the bundle consumed by the current agent.
        :param num_of_agents:  the total number of agents.
        :return: True iff the current agent finds the allocation PROPc.
        """
        return self.valuation.is_PROP(own_bundle, num_of_agents)

    def __repr__(self):
        if self.duplicity==1:
            return f"{self.name()} is an agent with a {self.valuation.__repr__()}"
        else:
            return f"{self.name()} are {self.duplicity} agents with a {self.valuation.__repr__()}"



class MonotoneAgent(Agent):
    """
    Represents an agent or several agents with a general monotone valuation function.

    >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4}, name="Alice")
    >>> a
    Alice is an agent with a Monotone valuation on ['x', 'y'].
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
    Anonymous are 2 agents with a Monotone valuation on ['x', 'y'].

    """
    def __init__(self, map_bundle_to_value:Dict[Bundle,float], name:str=None, duplicity:int=1):
        """
        Initializes an agent with a given valuation function.
        :param map_bundle_to_value: a dict that maps each subset of goods to its value.
        :param duplicity: the number of agents with the same valuation.
        """
        super().__init__(MonotoneValuation(map_bundle_to_value), name, duplicity)


class AdditiveAgent(Agent):
    """
    Represents an agent or several agents with an additive valuation function.
    >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w":0}, name="Alice")
    >>> a
    Alice is an agent with a Additive valuation: w=0 x=1 y=2 z=4.
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
    >>> int(a.value_1_of_c_MMS(c=4))
    0
    >>> int(a.value_1_of_c_MMS(c=3))
    1
    >>> int(a.value_1_of_c_MMS(c=2))
    3
    >>> AdditiveAgent({"x": 1, "y": 2, "z": 4}, duplicity=2)
    Anonymous are 2 agents with a Additive valuation: x=1 y=2 z=4.

    """
    def __init__(self, map_good_to_value, name:str=None, duplicity:int=1):
        """
        Initializes an agent with a given additive valuation function.
        :param map_good_to_value: a dict that maps each single good to its value, or a list that lists the values of each good.
        :param duplicity: the number of agents with the same valuation.
        """
        super().__init__(AdditiveValuation(map_good_to_value), name=name, duplicity=duplicity)

    @staticmethod
    def list_from(input: Any)->List[Agent]:
        """
        Construct a list of additive agents from various input formats.
        >>> ### From dict of dicts:
        >>> the_list = AdditiveAgent.list_from({"Alice":{"x":1,"y":2}, "George":{"x":3,"y":4}})
        >>> the_list[0]
        Alice is an agent with a Additive valuation: x=1 y=2.
        >>> the_list[1].name()
        'George'
        >>> the_list[1].value({"x","y"})
        7
        >>> ### From dict of lists:
        >>> the_list = AdditiveAgent.list_from({"Alice":[1,2], "George":[3,4]})
        >>> the_list[1]
        George is an agent with a Additive valuation: v0=3 v1=4.
        >>> ### From list of dicts:
        >>> the_list = AdditiveAgent.list_from([{"x":1,"y":2}, {"x":3,"y":4}])
        >>> the_list[0]
        Agent #0 is an agent with a Additive valuation: x=1 y=2.
        >>> the_list[1].name()
        'Agent #1'
        >>> ### From list of lists:
        >>> the_list = AdditiveAgent.list_from([[1,2],[3,4]])
        >>> the_list[1]
        Agent #1 is an agent with a Additive valuation: v0=3 v1=4.
        >>> the_list[0].name()
        'Agent #0'
        >>> the_list[0].value({0,1})
        3
        """
        if isinstance(input, dict):
            return [
                AdditiveAgent(valuation, name=name)
                for name,valuation in input.items()
            ]
        elif isinstance(input, list):
            if len(input)==0:
                return []
            if isinstance(input[0], Agent):
                return input
            return [
                AdditiveAgent(valuation, name=f"Agent #{index}")
                for index,valuation in enumerate(input)
            ]
        else:
            raise ValueError(f"Input to list_from should be a dict or a list, but it is {type(input)}")


class BinaryAgent(Agent):
    """
    Represents an agent with binary valuations, or several agents with the same binary valuations.
    >>> a = BinaryAgent({"x","y","z"}, name="Alice")
    >>> a
    Alice is an agent with a Binary valuation who wants ['x', 'y', 'z'].
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
    Anonymous are 2 agents with a Binary valuation who wants ['x', 'y', 'z'].
    """
    def __init__(self, desired_items:Bundle, name:str=None, duplicity:int=1):
        super().__init__(BinaryValuation(desired_items), name=name, duplicity=duplicity)





######## CAKE AGENTS #######

class PiecewiseConstantAgent(Agent):
    """
    A PiecewiseConstantAgent is an Agent whose value function has a constant density on a finite number of intervals.

    >>> a = PiecewiseConstantAgent([11,22,33,44]) # Four desired intervals: the leftmost has value 11, the second one 22, etc.
    >>> a.total_value()
    110
    >>> a.cake_length()
    4
    >>> a.eval(1,3)
    55.0
    >>> a.mark(1, 77)
    3.5
    >>> a.name()
    'Anonymous'
    >>> a.value([(0,1),(2,3)])
    44.0
    >>> Alice = PiecewiseConstantAgent([11,22,33,44], "Alice")
    >>> Alice.name()
    'Alice'
    """
    def __init__(self, values:list, name:str=None, duplicity:int=1):
        super().__init__(PiecewiseConstantValuation(values), name=name, duplicity=1)



class PiecewiseConstantAgentNormalized(Agent):
    """
    >>> a = PiecewiseConstantAgentNormalized([11,22,33,44])
    >>> a.eval(0.5,1)
    0.7
    >>> np.round(a.eval(0.25,1),3)
    0.9
    >>> np.round(a.eval(0,0.25),3)
    0.1
    >>> np.round(a.eval(0,0.375),3)
    0.2
    >>> np.round(a.mark(0.5, 0.7),3)
    1.0
    >>> np.round(a.mark(0.375, 0.1),3)
    0.5
    >>> np.round(a.mark(0, 0.2),3)
    0.375
    >>> np.round(a.mark(0.25, 0.2),3)
    0.5
    >>> np.round(a.mark(0, 0.9),4)
    0.9375
    """
    def __init__(self, values:list, name:str=None, duplicity:int=1):
        super().__init__(PiecewiseConstantValuationNormalized(values), name=name, duplicity=1)



class PiecewiseConstantAgent1Segment(Agent):
    """
    """
    def __init__(self, values:list, name:str=None, duplicity:int=1):
        super().__init__(PiecewiseConstantValuation1Segment(values), name=name, duplicity=1)




class PiecewiseUniformAgent(Agent):
    """
    A PiecewiseUniformAgent is an Agent with a finite number of desired intervals, all of which have the same value-density (1).

    >>> a = PiecewiseUniformAgent([(0,1),(2,4),(6,9)])   # Three desired intervals: (0..1) and (2..4) and (6..9).
    >>> a.total_value()
    6
    >>> a.cake_length()
    9
    >>> a.eval(0,1.5)
    1.0
    >>> a.mark(0, 2)
    3
    >>> a.name()
    'Anonymous'
    >>> George = PiecewiseUniformAgent([(0,1),(2,4),(6,9)], "George")
    >>> George.name()
    'George'
    """
    def __init__(self, desired_regions:List[tuple], name:str=None, duplicity:int=1):
        super().__init__(PiecewiseUniformValuation(desired_regions), name=name, duplicity=1)


class PiecewiseLinearAgent(Agent):
    """
    Author: Tom Goldenberg
    Since:  2020-06

    A PiecewiseLinearAgent is an Agent whose value function has a piecewise linear density.
    PiecewiseLinearAgent([11,22],[1,0])
    the first list ([11,22]) is the value of pieces e.g. 1st piece has a value of 11 and the second has a value of 22
    the second list ([1,0]) are the slopes of the piece value, meaning: for each piece the corresponding lists will be used
     to build the equation y = mx + c => (y = 1*x + c, y = 0*x + c) and the 11 and 22 are the integral value of the equation
     from x_0 = 0 -> x_1 = 1
    >>> a = PiecewiseLinearAgent([11,22,33,44],[1,2,3,-2]) # Four desired intervals: the leftmost has value 11, the second one 22,  etc.
    >>> a.total_value()
    110
    >>> a.cake_length()
    4
    >>> a.eval(1,3)
    55.0
    >>> a.value([(0,1),(2,3)])
    44.0
    >>> a = PiecewiseLinearAgent([2],[1])
    >>> a.cake_length()
    1
    >>> a.total_value()
    2
    >>> a.value([(0,1)])
    2.0
    >>> a.eval(0,1)
    2.0
    >>> a = PiecewiseLinearAgent([2,2],[1,0])
    >>> a.total_value()
    4
    >>> a.value([(0,1)])
    2.0
    >>> a.value([(1,1.5)])
    1.0
    >>> a.value([(1,2)])
    2.0
    >>> a.value([(0.5,2)])
    3.125
    """
    def __init__(self, values: list, slopes: list, name:str=None, duplicity:int=1):
        super().__init__(PiecewiseLinearValuation(values,slopes), name=name, duplicity=1)






######## UTILITY FUNCTIONS #######


def _representative_item(input:Any):
    if isinstance(input, list):
        if len(input)==0:
            return None
        else:
            return input[0]
    elif isinstance(input, dict):
        if len(input)==0:
            return None
        else:
            return next(iter(input.values()))
    else:
        raise ValueError(f"input should be a list or a dict, but it is {type(input)}")


def agents_from(input:Any)->List[Agent]:
    """
    Attempts to construct a list of agents from various input formats.
    The returned value is a list of Agent objects.

    >>> ### From dict of dicts:
    >>> agents_from({"Alice":{"x":1,"y":2}, "George":{"x":3,"y":4}})[0]
    Alice is an agent with a Additive valuation: x=1 y=2.
    >>> agents_from({"Alice":[1,2], "George":[3,4]})[1]
    George is an agent with a Additive valuation: v0=3 v1=4.
    >>> ### From list of dicts:
    >>> agents_from([{"x":1,"y":2}, {"x":3,"y":4}])[0]
    Agent #0 is an agent with a Additive valuation: x=1 y=2.
    >>> ### From list of lists:
    >>> agents_from([[1,2],[3,4]])[1]
    Agent #1 is an agent with a Additive valuation: v0=3 v1=4.
    >>> ### From numpy array:
    >>> agents_from(np.ones([2,4]))[1]
    Agent #1 is an agent with a Additive valuation: v0=1.0 v1=1.0 v2=1.0 v3=1.0.

    >>> ### From list of valuations:
    >>> l = agents_from([AdditiveValuation([1,2]), BinaryValuation("xy")])
    >>> l[0]
    Agent #0 is an agent with a Additive valuation: v0=1 v1=2.
    >>> ### From list of agents:
    >>> agents_from([AdditiveAgent([1,2]), BinaryAgent("xy")])[0]
    Anonymous is an agent with a Additive valuation: v0=1 v1=2.
    """
    if isinstance(input,np.ndarray):
        input = ValuationMatrix(input)
    if isinstance(input,ValuationMatrix):
        return [
            Agent(AdditiveValuation(input[index]), name=f"Agent #{index}")
            for index in input.agents()
        ]
    input_0 = _representative_item(input)
    if input_0 is None:
        return []
    elif isinstance(input_0, Agent):  # The input is already a list of Agent objects - nothing more to do.
        return input
    elif hasattr(input_0, "value"):   # The input is a list of Valuation objects - we just need to add names.
        return [
            Agent(valuation, name=f"Agent #{index}")
            for index,valuation in enumerate(input)
        ]
    else:
        return AdditiveAgent.list_from(input)




def agent_names_from(input:Any)->List[str]:
    """
    Attempts to extract a list of agent names from various input formats.
    The returned value is a list of strings.

    >>> ### From dict:
    >>> agent_names_from({"Alice":{"x":1,"y":2}, "George":{"x":3,"y":4}})
    ['Alice', 'George']
    >>> ### From list of dicts:
    >>> agent_names_from([{"x":1,"y":2}, {"x":3,"y":4}])
    ['Agent #0', 'Agent #1']
    >>> ### From list of lists:
    >>> agent_names_from([[1,2],[3,4]])
    ['Agent #0', 'Agent #1']
    >>> ### From list of valuations:
    >>> agent_names_from([AdditiveValuation([1,2]), BinaryValuation("xy")])
    ['Agent #0', 'Agent #1']
    >>> ### From list of agents:
    >>> agent_names_from([AdditiveAgent([1,2], name="Alice"), BinaryAgent("xy", name="George")])
    ['Alice', 'George']
    >>> d = {"Alice": 123, "George": 456}
    >>> agent_names_from(d.keys())
    ['Alice', 'George']
    """
    if hasattr(input, "keys"):
        return sorted(input.keys())
    elif hasattr(input, 'num_of_agents'):
        num_of_agents = input.num_of_agents
        return [f"Agent #{i}" for i in range(num_of_agents)]

    if len(input)==0:
        return []

    input_0 = next(iter(input))
    if hasattr(input_0, "name"):  
        return [agent.name() for agent in input]
    elif isinstance(input_0, int):
        return [f"Agent #{index}" for index in input]
    elif isinstance(input_0, str):
        return list(input)  # convert to a list; keep the original order
    else:
        return [f"Agent #{i}" for i in range(len(input))]
        

if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
