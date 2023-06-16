"""
This module implements Adaptor functions for fair division algorithms.

The functions accept a division algorithm as an argument.

They allow you to call the algorithm with convenient input types,
such as: a list of values, or a dict that maps an item to its value.

Author: Erel Segal-Halevi
Since: 2022-10
"""

from typing import Callable, Any
from fairpy import AgentList, Allocation, ValuationMatrix, AllocationMatrix, FractionalBundle
import numpy as np


def divide(algorithm: Callable, input: Any, *args, **kwargs):
    """
    An adaptor function for item allocation.

    :param algorithm: a specific fair item allocation algorithm. Should accept one the following parameters: 
        agents: AgentList - a list of Agent objects;
        valuation_matrix: ValuationMatrix - a matrix V where V[i,j] is the value of agent i to item j.
    It can also accept additional parameters.

    :param input: the input to the algorithm, in one of the following forms:
       * dict of dicts mapping agent names to their valuations, e.g.: {"Alice":{"x":1,"y":2}, "George":{"x":3,"y":4}}
       * list of dicts, e.g. [{"x":1,"y":2}, {"x":3,"y":4}]. Agents are called by their number: "Agent #0", "Agent #1", etc.
       * list of lists, e.g. [[1,2],[3,4]]. Agents and items are called by their number.
       * numpy array, e.g.: np.ones([2,4])). 
       * list of Valuation objects, e.g. [AdditiveValuation([1,2]), BinaryValuation("xy")]
       * list of Agent objects, e.g. [AdditiveAgent([1,2]), BinaryAgent("xy")]

    :param kwargs: any other arguments expected by `algorithm`.

    :return: an allocation of the items among the agents.

    >>> from dicttools import stringify
    >>> import fairpy

    ### List of lists of values, plus an optional parameter:
    >>> divide(algorithm=fairpy.items.round_robin, input=[[11,22,44,0],[22,11,66,33]], agent_order=[1,0])
    Agent #0 gets {0,1} with value 33.
    Agent #1 gets {2,3} with value 99.
    <BLANKLINE>

    ### List of list of values, converted to a ValuationMatrix:
    >>> divide(algorithm=fairpy.items.leximin_optimal_allocation, input=[[3,3],[0,5]]).round(2)
    Agent #0 gets { 100.0% of 0, 25.0% of 1} with value 3.75.
    Agent #1 gets { 75.0% of 1} with value 3.75.
    <BLANKLINE>

    ### Dict mapping agent names to lists of values
    >>> divide(algorithm=fairpy.items.round_robin, input={"Alice": [11,22,44,0], "George": [22,11,66,33]})
    Alice gets {1,2} with value 66.
    George gets {0,3} with value 55.
    <BLANKLINE>


    ### Dict mapping agent names to lists of values, converted to a ValuationMatrix
    >>> divide(algorithm=fairpy.items.leximin_optimal_envyfree_allocation, input={"Alice": [3,3], "George": [0,5]}).round(2)
    Alice gets { 100.0% of 0, 25.0% of 1} with value 3.75.
    George gets { 75.0% of 1} with value 3.75.
    <BLANKLINE>

    ### Dict mapping agent names to lists of values:
    >>> divide(algorithm=fairpy.items.utilitarian_matching, input={"Alice": [11,22,44,0], "George": [22,11,66,33]})
    Alice gets {1} with value 22.
    George gets {2} with value 66.
    <BLANKLINE>

    ### Dict mapping agent names to dicts of values:
    >>> divide(algorithm=fairpy.items.iterated_maximum_matching, input={"Alice": {"w":11,"x":22,"y":44,"z":0}, "George": {"w":22,"x":11,"y":66,"z":33}})
    Alice gets {w,x} with value 33.
    George gets {y,z} with value 99.
    <BLANKLINE>

    ### Dict mapping agent names to dicts of values, converted to a ValuationMatrix:
    >>> divide(algorithm=fairpy.items.max_sum_allocation, input={"Alice": {"w":11,"x":22,"y":44,"z":0}, "George": {"w":22,"x":11,"y":66,"z":33}})
    Alice gets { 100.0% of x} with value 22.
    George gets { 100.0% of w, 100.0% of y, 100.0% of z} with value 121.
    <BLANKLINE>

    >>> divide(algorithm=fairpy.items.undercut, input={"Alex":{"a": 1,"b": 2, "c": 3, "d":4,"e": 5, "f":14},"Bob":{"a":1,"b": 1, "c": 1, "d":1,"e": 1, "f":7}})
    Alex gets {a,b,c,d,e} with value 15.
    Bob gets {f} with value 7.
    <BLANKLINE>

    >>> divide(algorithm=fairpy.items.three_quarters_MMS_allocation, input={"Alice": {"w":11,"x":22,"y":44,"z":0}, "George": {"w":22,"x":11,"y":66,"z":33}})
    Alice gets {y} with value 44.
    George gets {w,x,z} with value 66.
    <BLANKLINE>

    >>> prefs = AgentList({"avi": {"x":5, "y": 4}, "beni": {"x":2, "y":3}, "gadi": {"x":3, "y":2}})
    >>> alloc = divide(fairpy.items.utilitarian_matching, prefs, item_capacities={"x":2, "y":2})
    >>> stringify(alloc.map_agent_to_bundle())
    "{avi:['x'], beni:['y'], gadi:['x']}"
    >>> stringify(alloc.map_item_to_agents())
    "{x:['avi', 'gadi'], y:['beni']}"
    >>> agent_weights = {"avi":1, "gadi":10, "beni":100}
    >>> stringify(alloc.map_item_to_agents(sortkey=lambda name: -agent_weights[name]))
    "{x:['gadi', 'avi'], y:['beni']}"

    >>> alloc = divide(fairpy.items.utilitarian_matching, prefs, item_capacities={"x":2, "y":2}, agent_capacities={"avi":2,"beni":1,"gadi":1})
    >>> stringify(alloc.map_agent_to_bundle())
    "{avi:['x', 'y'], beni:['y'], gadi:['x']}"

    >>> prefs = AgentList([[5,4],[3,2]])
    >>> alloc = divide(fairpy.items.utilitarian_matching, prefs)
    >>> stringify(alloc.map_agent_to_bundle())
    '{Agent #0:[1], Agent #1:[0]}'
    >>> stringify(alloc.map_item_to_agents())
    "{0:['Agent #1'], 1:['Agent #0']}"

    >>> agents = AgentList({"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}})
    >>> alloc = divide(fairpy.items.iterated_maximum_matching, agents, item_capacities={"x":1,"y":1,"z":1,"w":1})
    >>> stringify(alloc.map_agent_to_bundle())
    "{avi:['x', 'y'], beni:['w', 'z']}"
    >>> stringify(alloc.map_item_to_agents())
    "{w:['beni'], x:['avi'], y:['avi'], z:['beni']}"

    ### Cake-cutting algorithm
    >>> from fairpy.agents import PiecewiseConstantAgent
    >>> from fairpy.cake import cut_and_choose
    >>> Alice = PiecewiseConstantAgent([33,33], "Alice")
    >>> George = PiecewiseConstantAgent([11,55], "George")
    >>> divide(algorithm=cut_and_choose.asymmetric_protocol, input=[Alice, George])
    Alice gets {(0, 1.0)} with value 33.
    George gets {(1.0, 2)} with value 55.
    <BLANKLINE>
    >>> divide(algorithm=cut_and_choose.asymmetric_protocol, input=[George, Alice])
    George gets {(1.4, 2)} with value 33.
    Alice gets {(0, 1.4)} with value 46.2.
    <BLANKLINE>
    """
    annotations_list = list(algorithm.__annotations__.items())
    first_argument_type = annotations_list[0][1]


    ### Convert input to AgentList
    if first_argument_type==AgentList:
        agent_list = AgentList(input)
        output = algorithm(agent_list, *args, **kwargs)
        if isinstance(output,Allocation):
            return output
        else:
            return Allocation(agent_list, output)


    ### Convert input to ValuationMatrix
    elif first_argument_type==ValuationMatrix:
        # Step 1. Adapt the input:
        valuation_matrix = list_of_valuations = object_names = agent_names = None
        if isinstance(input, ValuationMatrix): # instance is already a valuation matrix
            valuation_matrix = input
        elif isinstance(input, np.ndarray):    # instance is a numpy valuation matrix
            valuation_matrix = ValuationMatrix(input)
        elif isinstance(input, list) and isinstance(input[0], list):            # list of lists
            list_of_valuations = input
            valuation_matrix = ValuationMatrix(list_of_valuations)
        elif isinstance(input, dict):  
            agent_names = list(input.keys())
            list_of_valuations = list(input.values())
            if isinstance(list_of_valuations[0], dict): # maps agent names to dicts of valuations
                object_names = list(list_of_valuations[0].keys())
                list_of_valuations = [
                    [valuation[object] for object in object_names]
                    for valuation in list_of_valuations
                ]
            valuation_matrix = ValuationMatrix(list_of_valuations)
        else:
            raise TypeError(f"Unsupported input type: {type(input)}")

        # Step 2. Run the algorithm:
        output = algorithm(valuation_matrix, *args, **kwargs)
        
        # Step 3. Adapt the output:
        if isinstance(output,Allocation):
            return output
        if agent_names is None:
            agent_names = [f"Agent #{i}" for i in valuation_matrix.agents()]
        if isinstance(output, np.ndarray) or isinstance(output, AllocationMatrix):  # allocation matrix
            allocation_matrix = AllocationMatrix(output)
            if isinstance(input, dict):
                list_of_bundles = [FractionalBundle(allocation_matrix[i], object_names) for i in allocation_matrix.agents()]
                dict_of_bundles = dict(zip(agent_names,list_of_bundles))
                return Allocation(input, dict_of_bundles, matrix=allocation_matrix)
            else:
                return Allocation(valuation_matrix, allocation_matrix)
        elif isinstance(output, list):
            if object_names is None:
                list_of_bundles = output
            else:
                list_of_bundles = [
                    [object_names[object_index] for object_index in bundle]
                    for bundle in output
                ]
            dict_of_bundles = dict(zip(agent_names,list_of_bundles))
            return Allocation(input if isinstance(input,dict) else valuation_matrix, dict_of_bundles)
        else:
            raise TypeError(f"Unsupported output type: {type(output)}")

    else:
        return algorithm(input, *args, **kwargs)



if __name__ == "__main__":
    # from fairpy.items.round_robin import round_robin
    # print(divide(algorithm=round_robin, instance = [[11,22,44,0],[22,11,66,33]]))
    import doctest, sys
    (failures, tests) = doctest.testmod(report=True)
    print(f"{failures} failures, {tests} tests")
    # if failures > 0:
    #     sys.exit(1)
