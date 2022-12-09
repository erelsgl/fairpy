#!python3

"""
Adapts algorithms, using a specific input and output formats, to accept various other input/output formats.

Programmer: Erel Segal-Halevi
Since: 2021-11
"""
import numpy as np
from typing import Any, Callable, List
from fairpy import ValuationMatrix, AllocationMatrix, Allocation
from fairpy.bundles import FractionalBundle
from functools import wraps


def convert_input_to_valuation_matrix(algorithm: Callable)->Allocation:
    """
    Adapts an algorithm, that accepts as input a ValuationMatrix object,
    to accept various other input formats.

    >>> # Available input formats:

    >>> input_matrix = np.ones([2,3])        # a numpy array of valuations.
    >>> convert_input_to_valuation_matrix(dummy_matrix_list_algorithm)(input_matrix)
    Agent #0 gets {0,2} with value 2.
    Agent #1 gets {1} with value 1.
    <BLANKLINE>
    >>> convert_input_to_valuation_matrix(dummy_matrix_matrix_algorithm)(input_matrix)
    Agent #0 gets { 100.0% of 0, 100.0% of 2} with value 2.
    Agent #1 gets { 100.0% of 1} with value 1.
    <BLANKLINE>

    >>> input_list_of_lists = [[1,4,7],[6,3,0]]     # a list of lists.
    >>> convert_input_to_valuation_matrix(dummy_matrix_list_algorithm)(input_list_of_lists)
    Agent #0 gets {0,2} with value 8.
    Agent #1 gets {1} with value 3.
    <BLANKLINE>
    >>> convert_input_to_valuation_matrix(dummy_matrix_matrix_algorithm)(input_list_of_lists)
    Agent #0 gets { 100.0% of 0, 100.0% of 2} with value 8.
    Agent #1 gets { 100.0% of 1} with value 3.
    <BLANKLINE>

    >>> input_dict_of_lists = {"a": [1,2,3], "b": [4,5,6]}      # a dict mapping agent names to list of values.
    >>> convert_input_to_valuation_matrix(dummy_matrix_list_algorithm)(input_dict_of_lists)
    a gets {0,2} with value 4.
    b gets {1} with value 5.
    <BLANKLINE>
    >>> convert_input_to_valuation_matrix(dummy_matrix_matrix_algorithm)(input_dict_of_lists)
    a gets { 100.0% of 0, 100.0% of 2} with value 4.
    b gets { 100.0% of 1} with value 5.
    <BLANKLINE>

    >>> input_dict_of_dicts = {"a": {"x":1,"y":2,"z":3}, "b": {"x":4,"y":5,"z":6}}       # a dict mapping agent names to dict of values.
    >>> convert_input_to_valuation_matrix(dummy_matrix_list_algorithm)(input_dict_of_dicts)
    a gets {x,z} with value 4.
    b gets {y} with value 5.
    <BLANKLINE>
    >>> convert_input_to_valuation_matrix(dummy_matrix_matrix_algorithm)(input_dict_of_dicts)
    a gets { 100.0% of x, 100.0% of z} with value 4.
    b gets { 100.0% of y} with value 5.
    <BLANKLINE>
    >>> convert_input_to_valuation_matrix(dummy_matrix_matrix_algorithm)(input_dict_of_dicts, first_agent=1)
    a gets { 100.0% of y} with value 2.
    b gets { 100.0% of x, 100.0% of z} with value 10.
    <BLANKLINE>

    >>> input_dict_of_dicts = {"a": {"x":4,"y":2,"z":6}, "b": {"x":1,"y":5,"z":3}}       # a dict mapping agent names to dict of values; REVERSE ORDER
    >>> convert_input_to_valuation_matrix(utilitarian_matrix_list_algorithm)(input_dict_of_dicts)
    a gets {x,z} with value 10.
    b gets {y} with value 5.
    <BLANKLINE>
    >>> convert_input_to_valuation_matrix(utilitarian_matrix_matrix_algorithm)(input_dict_of_dicts)
    a gets { 100.0% of x, 100.0% of z} with value 10.
    b gets { 100.0% of y} with value 5.
    <BLANKLINE>

    >>> input_dict_of_dicts = {"b": {"x":1,"y":5,"z":3}, "a": {"x":4,"y":2,"z":6}}       # a dict mapping agent names to dict of values; REVERSE ORDER
    >>> convert_input_to_valuation_matrix(utilitarian_matrix_list_algorithm)(input_dict_of_dicts)
    b gets {y} with value 5.
    a gets {x,z} with value 10.
    <BLANKLINE>
    >>> convert_input_to_valuation_matrix(utilitarian_matrix_matrix_algorithm)(input_dict_of_dicts)
    b gets { 100.0% of y} with value 5.
    a gets { 100.0% of x, 100.0% of z} with value 10.
    <BLANKLINE>
    """
    @wraps(algorithm)
    def adapted_algorithm(input, *args, **kwargs):

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
    return adapted_algorithm



"""
The algorithms below are dummy algorithms, used for demonstrating the adaptors.
They accept an input a valuation profile (as a list of lists, or valuation matrix),
     and return as output an allocation profile (as a list of lists, or allocation matrix).
They allocate the objects in turn, like "round robin" but without regard to valuations.
"""
def dummy_list_list_algorithm(valuations:List[List])->List[List]:
    """ 
    >>> dummy_list_list_algorithm([[11,22,33],[44,55,66]])
    [[0, 2], [1]]
    """
    num_agents = len(valuations)
    num_objects = len(valuations[0])
    bundles = [[] for _ in range(num_agents)]
    i_agent = 0
    for i_object in range(num_objects):
        bundles[i_agent].append(i_object)
        i_agent += 1
        if i_agent >= num_agents:
            i_agent = 0
    return bundles


def dummy_list_matrix_algorithm(valuations:List[List], first_agent:int=0)->np.ndarray:
    """ 
    >>> dummy_list_matrix_algorithm([[11,22,33],[44,55,66]])
    array([[1., 0., 1.],
           [0., 1., 0.]])
    >>> dummy_list_matrix_algorithm([[11,22,33],[44,55,66]], first_agent=1)
    array([[0., 1., 0.],
           [1., 0., 1.]])
    """
    num_agents = len(valuations)
    num_objects = len(valuations[0])
    bundles = np.zeros([num_agents,num_objects])
    i_agent = first_agent
    for i_object in range(num_objects):
        bundles[i_agent][i_object] = 1
        i_agent += 1
        if i_agent >= num_agents:
            i_agent = 0
    return bundles

def dummy_matrix_list_algorithm(valuations:ValuationMatrix)->List[List]:
    """ 
    >>> dummy_matrix_list_algorithm(ValuationMatrix([[11,22,33],[44,55,66]]))
    [[0, 2], [1]]
    """
    num_agents = valuations.num_of_agents
    num_objects = valuations.num_of_objects
    bundles = [[] for _ in range(num_agents)]
    i_agent = 0
    for i_object in range(num_objects):
        bundles[i_agent].append(i_object)
        i_agent += 1
        if i_agent >= num_agents:
            i_agent = 0
    return bundles

def dummy_matrix_matrix_algorithm(valuations:ValuationMatrix, first_agent:int=0)->np.ndarray:
    """ 
    >>> dummy_matrix_matrix_algorithm(ValuationMatrix([[11,22,33],[44,55,66]]))
    array([[1., 0., 1.],
           [0., 1., 0.]])
    >>> dummy_matrix_matrix_algorithm(ValuationMatrix([[11,22,33],[44,55,66]]), first_agent=1)
    array([[0., 1., 0.],
           [1., 0., 1.]])
    """
    num_agents = valuations.num_of_agents
    num_objects = valuations.num_of_objects
    bundles = np.zeros([num_agents,num_objects])
    i_agent = first_agent
    for i_object in range(num_objects):
        bundles[i_agent][i_object] = 1
        i_agent += 1
        if i_agent >= num_agents:
            i_agent = 0
    return bundles


def utilitarian_matrix_list_algorithm(valuations:ValuationMatrix)->List[List]:
    """ 
    >>> utilitarian_matrix_list_algorithm(ValuationMatrix([[44,22,66],[11,55,33]]))
    [[0, 2], [1]]
    """
    num_agents = valuations.num_of_agents
    num_objects = valuations.num_of_objects
    bundles = [[] for _ in range(num_agents)]
    for i_object in range(num_objects):
        i_agent = max(range(num_agents), key=lambda i_agent: valuations[i_agent][i_object])
        bundles[i_agent].append(i_object)
    return bundles


def utilitarian_matrix_matrix_algorithm(valuations:ValuationMatrix)->List[List]:
    """ 
    >>> utilitarian_matrix_matrix_algorithm(ValuationMatrix([[44,22,66],[11,55,33]]))
    array([[1., 0., 1.],
           [0., 1., 0.]])
    """
    num_agents = valuations.num_of_agents
    num_objects = valuations.num_of_objects
    bundles = np.zeros([num_agents,num_objects])
    for i_object in range(num_objects):
        i_agent = max(range(num_agents), key=lambda i_agent: valuations[i_agent][i_object])
        bundles[i_agent][i_object] = 1
    return bundles


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    # input_dict_of_dicts = {"b": {"x":1,"y":5,"z":3}, "a": {"x":4,"y":2,"z":6}}       # a dict mapping agent names to dict of values; REVERSE ORDER
    # convert_input_to_valuation_matrix(utilitarian_matrix_list_algorithm)(input_dict_of_dicts)

