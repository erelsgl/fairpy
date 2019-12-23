"""
Implementation of an Approximation Algorithm for computing continuous
division of a cake among n agents in order to maximize the welfare.

Reference:

    Yonatan Aumann, Yair Dombb, Avinatan Hassidim (2012). "Computing socially-efficient cake divisions".
    Proceedings of AAMAS 2013, 343--350. Algorithms 1 and 2.

Programmer: Jonathan Diamant
Since: 2019-12
"""
from agents import *

def discretization_procedure(agents: List[Agent], epsilone):
    """

    :param agents: List of agents. assumption: for each agent: agent.eval(0, agent.cake_length()) == 1
    :param epsilone: A bound
    :return: A discrete approximation version of the cake

    >>> a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    >>> b = PiecewiseConstantAgent([0.23, 0.7, 0.07])
    >>> list = [a,b]
    >>> discretization_procedure(list, 0.2)
    [0, 0.8, 1.22, 1.5057142857142858, 1.7914285714285716, 2.3828571428571435, 3]
    """
    size_of_the_cake = max([agent.cake_length() for agent in agents])
    a = 0
    C = [0]
    condition = [agent.eval(a,size_of_the_cake) > epsilone for agent in agents]
    while any(condition):
        values = []
        for i in agents:
            x = i.mark(a, epsilone)
            if (x != None):
                values.append(x)
        b = min(values)
        C.append(b)
        a = b
        condition = [agent.eval(a, size_of_the_cake) > epsilone for agent in agents]
    C.append(size_of_the_cake)
    return C


def  discrete_utilitarian_welfare_approximation():
    pass
if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
    a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    b = PiecewiseConstantAgent([0.23, 0.7, 0.07])
    list = [a, b]
    c = discretization_procedure(list, 0.2)
    for i in range(6):
        print("{},{}: a {}, b {}\n".format(c[i], c[i + 1],a.eval(c[i], c[i + 1]), b.eval(c[i], c[i + 1])))

    print(c)