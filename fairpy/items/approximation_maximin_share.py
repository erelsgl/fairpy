#!python3

""" 
Find an approximate MMS allocation.
Based on:

Stephen J. Willson
["Fair Division Using Linear Programming"](https://swillson.public.iastate.edu/FairDivisionUsingLPUnpublished6.pdf)
* Part 6, pages 20--27.

Programmer: Liad Nagi and Moriya Elgrabli 

See also: 

Since:  
"""

# import cvxpy
from fairpy import Allocation, ValuationMatrix, Agent, AdditiveValuation, convert_input_to_valuation_matrix
from fairpy import agents
from fairpy.agents import AdditiveAgent
from typing import Any, List

import logging
logger = logging.getLogger(__name__)


##### Algo 2

def initial_assignment_alfa_MSS(agents: List[AdditiveAgent], alfa:float):
    """
  
    """
    return agents, Allocation # TODO- check if need to return agants



##### Algo 3

def bag_filling_algorithm_alfa_MMS(agents: List[AdditiveAgent], alfa:float) -> Allocation:
    """
    Find the leximin-optimal (aka Egalitarian) allocation.
    :param instance: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
    The allocation should maximize the leximin vector of utilities.
    >>> logger.setLevel(logging.WARNING)
    
    """
    return agents, Allocation()


##### algo 1
def alfa_MMS_allocation(agents: List[AdditiveAgent], alfa:float) :
    """
    Find alfa_MMS_allocation for the given agents and valuations.
    :param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
    :param alfa: parameter for how much to approximate MMS allocation

    :return allocation_matrix: ---

    allocation for one agent, one object
    >>> a = AdditiveAgent({"x": 2}, name="a")  # one agent with one item
    >>> print(a)
    >>> agents=[a]
    >>> print(alfa_MMS_allocation(agents,0.75))
    a gets {x} with value 2.
    >>> print(agents[0].all_items())
    >>> print(agents==[])
    True
    """
 

    return Allocation(agents={"a"},bundles={{"a":{"x"}}})

##### Algo 5
##MMS <=1 for all agents, all  
def fixed_assignment(agents: List[AdditiveAgent], alfa:float):
    """
    
    """
    return agents, Allocation # TODO- check if need to return agants



##### Algo 6
def tentative_assignment(agents: List[AdditiveAgent], alfa:float):
    """
    
    """
    return agents, Allocation # TODO- check if need to return agants




##### algo 4
def three_quarters_MMS_allocation(agents: List[AdditiveAgent], alfa:float) :
    """
    Find the leximin-optimal (aka Egalitarian) allocation among families.
    :param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
    :param families: a list of lists. Each list represents a family and contains the indices of the agents in the family.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
    The allocation should maximize the leximin vector of utilities.
    

    """

    return agents, Allocation

##### algo 7
def agents_conversion_to_ordered_instance(agents: List[AdditiveAgent]) :
    """
    Find the leximin-optimal (aka Egalitarian) allocation among families.
    :param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
    :param families: a list of lists. Each list represents a family and contains the indices of the agents in the family.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
    The allocation should maximize the leximin vector of utilities.
    

    """

    return agents #sorted

    
##### algo 8
def get_alfa_MMS_allocation_to_unordered_instance(agents_unordered: List[AdditiveAgent],agents_orders:List[AdditiveAgent],ordered_allocation:Allocation) :
    """
    Find the leximin-optimal (aka Egalitarian) allocation among families.
    :param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
    :param families: a list of lists. Each list represents a family and contains the indices of the agents in the family.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
    The allocation should maximize the leximin vector of utilities.
    

    """

    return Allocation #sorted


if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
