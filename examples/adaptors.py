"""
Input adaptors can decorate any fair division function that takes an input in one format,
      and modify it so that it can accept an input in another format.

Programmer: Erel Segal-Halevi
Since: 2021-11-21
"""

from fairpy import adapt_matrix_algorithm, ValuationMatrix
import numpy as np

@adapt_matrix_algorithm
def dummy_matrix_matrix_algorithm(instance, first_agent:int=0)->np.ndarray:
    """ 
    A dummy algorithm used for demonstrating the matrix adaptor.
    It accepts an input a valuation matrix,  and return as output an allocation matrix.
    The decorator allows it to accept other input formats.

    It allocate the objects in turn, like "round robin" but without regard to valuations.
    """
    valuation_matrix = instance
    num_agents = valuation_matrix.num_of_agents
    num_objects = valuation_matrix.num_of_objects
    bundles = np.zeros([num_agents,num_objects])
    i_agent = first_agent
    for i_object in range(num_objects):
        bundles[i_agent][i_object] = 1
        i_agent += 1
        if i_agent >= num_agents:
            i_agent = 0
    return bundles



# Native call (works even without the adaptor):
print(dummy_matrix_matrix_algorithm(ValuationMatrix([[11,22,33],[44,55,66]])).matrix)
print(dummy_matrix_matrix_algorithm(ValuationMatrix([[11,22,33],[44,55,66]]), first_agent=1).matrix)

# Adapted calls (Works with the adaptor):
print(dummy_matrix_matrix_algorithm([[11,22,33],[44,55,66]], first_agent=1))
input_dict_of_dicts = {"a": {"x":1,"y":2,"z":3}, "b": {"x":4,"y":5,"z":6}}       # a dict mapping agent names to dict of values.
print(dummy_matrix_matrix_algorithm(input_dict_of_dicts, first_agent=1))
