



from ast import List
from fairpy.agents import AdditiveAgent
from fairpy.allocations import Allocation
import pytest

def course_allocation(agents: list[AdditiveAgent],course_capacity:int) -> Allocation:
    """
    Allocates the given courses to the given agents using the 'Course allocation by proxy auction' algorithm which
    garantees efficient Pareto by Uthor Scott Duke Kominers, Mike Ruberry and Jonathan Ullman
    Department of Economics, Harvard University, and Harvard Business School 
    (http://scottkom.com/articles/Kominers_Ruberry_Ullman_Course_Allocation_with_Appendix.pdf)
    :param agents: The agents who participate in the allocation and there course preferences.
    :param course_capacity: The courses capacity.
    :return: An allocation for each of the agents.
    >>> Alice = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,}, name="Alice")
    >>> Bob = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3, }, name="Bob")
    >>> Eve = AdditiveAgent({"c2": 1, "c3": 2, "c1": 3, }, name="Eve")
    >>> agents = [Alice,Bob,Eve]
    >>> allocation = course_allocation(agents,2)
    >>> {agents[i].name():agents[i].value(allocation[i]) for i,_ in enumerate(agents)}
    {'Alice': [c1,c3], 'Bob': [c1,c2], 'Eve': [c2,c3]}
    agents = AdditiveAgent.list_from({"Alice":[1,2,3], "Bob":[1,2,3],"Eve":[3,1,2]}
    >>> allocation = course_allocation(agents,2)    
    >>> {agents[i].name():agents[i].value(allocation[i]) for i,_ in enumerate(agents)}
    {'Alice': [c1,c3], 'Bob': [c1,c2], 'Eve': [c2,c3]}


    Two exampels that represent a problem in the algo where its better for Bob to give false preferences and get a better result
    >>> Alice = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,"c4":4}, name="Alice")
    >>> Bob = AdditiveAgent({"c2": 1, "c3": 2, "c4": 3,"c1":4 }, name="Bob")
    >>> allocation = course_allocation(agents,1)
    >>> {agents[i].name():agents[i].value(allocation[i]) for i,_ in enumerate(agents)}
    {'Alice': [c1,c2], 'Bob': [c3,c4]}


    >>> Alice = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,"c4":4}, name="Alice")
    >>> Bob = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,"c4":4 }, name="Bob")
    >>> allocation = course_allocation(agents,1)
    >>> {agents[i].name():agents[i].value(allocation[i]) for i,_ in enumerate(agents)}
    {'Alice': [c1,c4], 'Bob': [c2,c3]}
    """
    return []
if __name__ == "__main__":
    import doctest
    doctest.testmod()

   

   


