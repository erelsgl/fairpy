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
import copy
logger = logging.getLogger(__name__)


##### Algo 2

def initial_assignment_alfa_MSS(agents: List[AdditiveAgent], alfa:float):
    """

    """
    return agents, Allocation # TODO- check if need to return agants



##### Algo 3

def bag_filling_algorithm_alfa_MMS(agents: List[AdditiveAgent], alfa:float) -> Allocation:
    """

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
    >>> a = AdditiveAgent({"x": 2}, name="Alice")
    >>> agents=[a]
    >>> print(alfa_MMS_allocation(agents,0.75))
    Alice gets {x} with value 2.
    <BLANKLINE>
    >>> b = AdditiveAgent({"x": 1, "y": 2}, name="Blice")
    >>> agents=[b]
    >>> print(alfa_MMS_allocation(agents,0.75))
    Blice gets {x,y} with value 3.
    <BLANKLINE>
    >>> a = AdditiveAgent({"x": 1, "y": 2}, name="Alice") ### TODO chack
    >>> agents=[a, b]
    >>> print(alfa_MMS_allocation(agents,1))
    Alice gets {x} with value 1.
    Blice gets {y} with value 2.
    <BLANKLINE>
    """
 
    a=Allocation(agents=agents, bundles =  {"Alice":{"x"}})
    return a

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


    """

    return agents, Allocation

##### algo 7
def agents_conversion_to_ordered_instance(agents: List[AdditiveAgent]) :
    """


    """

    return agents #sorted

    
##### algo 8
def get_alfa_MMS_allocation_to_unordered_instance(agents_unordered: List[AdditiveAgent],agents_ordered:List[AdditiveAgent],ordered_allocation:Allocation) :
    """
    Get the MMS allocation for agents unordered valuations.
    :param agents_unordered: Unordered valuations agents.
    :param agents_ordered: Ordered valuations agents.
    :param ordered_allocation: MMS allocation for ordered valuations agents.
    :return allocation_matrix: ---

    allocation for one agent, one object
    >>> a = AdditiveAgent({"x": 2}, name="Alice")
    >>> agents=[a]
    >>> agents_ordered=agents_conversion_to_ordered_instance(agents)
    >>> temp=copy.deepcopy(agents_ordered)
    >>> ordered_alloc = alfa_MMS_allocation(temp,0.5)
    >>> print(get_alfa_MMS_allocation_to_unordered_instance(agents, agents_ordered, ordered_alloc))
    Alice gets {x} with value 2.
    <BLANKLINE>




    """

    return Allocation #sorted


if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
