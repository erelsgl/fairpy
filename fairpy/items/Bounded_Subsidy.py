
from ast import Dict, List
from fairpy import AgentList
def bounded_subsidy(agents: List, goods: List, weights: Dict[str, int]):
    """
    One Dollar Each Eliminates Envy
    by Jack Dippel and Adrian Vetta (Preprint · December 2019) https://www.researchgate.net/publication/337781386_One_Dollar_Each_Eliminates_Envy
    Programmer: Eyad Amer

    Algorithem bounded_subsidy:
    The algorithm getting a list of agents, goods list and array of the weights of the goods
    and it's returns a bundle of agents when each of the holds the best allocation to his valuation of the goods.


    >>>  agents1 = ["Alice", "Bob"]
    >>>  goods1 = ["a", "b", "c", "d"]
    >>> weights1 = {agents[0]: ["a":0.4, "b":1, "c":0.8, "d":0.7], agents[1]: ["a":0.5, "b":0.9, "c":0.5, "d":1]}
    >>> print(bounded_subsidy(agents: List, goods: List, weights: Dict[str, int]))
    {"Alice": ["b", "c"], "Bob": ["a", "d"]}

    >>> agents1
    ["Alice", "Bob"]
    >>> goods1
    ["a", "b", "c", "d"]
    >>> weights1
    {agents[0]: ["a":0.4, "b":1, "c":0.8, "d":0.7], agents[1]: ["a":0.5, "b":0.9, "c":0.5, "d":1]}

    >>>  agents2 = ["Alice", "Bob"]
    >>>  goods2 = ["a", "b", "c", "d", "e", "f"]
    >>> weights2 = [agents[0]: {"a":1, "b":0.8, "c":0.5, "d":1, "e":0.3, "f":0], agents[1]: ["a":0.9, "b":0.2, "c":0.4, "d":0.7, "e":1, "f":0]}
    >>> print(bounded_subsidy(agents: List, goods: List, weights: Dict[str, int]))
    {"Alice": ["a", "b", "c"], "Bob": ["d", "e", "f"]}

    >>> agents2 
    ["Alice", "Bob"]
    >>> goods2 
    ["a", "b", "c", "d", "e", "f"]
    >>> weights2
    [agents[0]: {"a":1, "b":0.8, "c":0.5, "d":1, "e":0.3, "f":0], agents[1]: ["a":0.9, "b":0.2, "c":0.4, "d":0.7, "e":1, "f":0]}
    
    
    """ 

    return 0

# main function
if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))