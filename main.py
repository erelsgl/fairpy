import networkx
from fairpy.agentlist import AgentList
from fairpy.allocations import Allocation


def algorithm1(agentsList: AgentList, rent: int, budget: dict) -> (int, Allocation):
    """
    "Fair Rent Division on a Budget", by Procaccia, A., Velez, R., & Yu, D. (2018), https://doi.org/10.1609/aaai.v32i1.11465
    The algorithm calculates Maximum-rent envy-free allocation in a fully connected economy, or in simple words,
    calculates a fair rent division under budget constraints.

    Algorithm 1:
                :param agentsList: Evaluation of each room by agent
                :param rent: Total rent
                :param budget: Each agent's budget
                :return:
                      - The rent after calculations
                      - Allocation - Dictionary of how much each agent has to pay for his room.
    Programmers: Asif Rot & Daniel Sela

    TESTS:
    >>> ex1 = AgentList({"Alice":{'1' : 250, '2' : 250, '3' : 500}, "Bob": {'1': 250, '2' : 250, '3' :500}, "Clair": {'1' :250, '2' : 500, '3' : 250}})
    >>> algorithm1(ex1, 1000, {'Alice': 250, 'Bob': 320, 'Clair': 430})
    (709.99, (Alice gets {1} with rent 70, Bob gets {2} with rent 320, Clair gets {3} with rent 320))

    >>> ex2 = AgentList({"Alice":{'1' : 250, '2' : 750}, "Bob": {'1': 250, '2' : 750}})
    >>> algorithm1(ex2, 1000, {'Alice': 600, 'Bob': 500})
    (918.75, (Alice gets {1} with rent 600, Bob gets {2} with rent 318.75))

    >>> ex3 = AgentList({"Alice":{'1' : 400, '2' : 600}, "Bob": {'1': 300, '2' : 700}})
    >>> algorithm1(ex3, 1000, {'Alice': 450, 'Bob': 550})
    (900, (Alice gets {1} with rent 350, Bob gets {2} with rent 550))
    """

    return 0  # Empty implementation


def algorithm2(agentsList: AgentList, rent: int, budget: dict) -> (int, Allocation):
    """
    "Fair Rent Division on a Budget", by Procaccia, A., Velez, R., & Yu, D. (2018), https://doi.org/10.1609/aaai.v32i1.11465
    The algorithm calculates fair rent division with optimal envy-free allocation subject to budget constraints.

    Algorithm 2:
                :param agentsList: Evaluation of each room by agent
                :param rent: Total rent
                :param budget: Each agent's budget
                :return:
                      - The rent after calculations
                      - Allocation - Dictionary of how much each agent has to pay for his room.
    Programmers: Asif Rot & Daniel Sela

    TESTS:
    >>> ex1 = AgentList({"Alice":{'1' : 250, '2' : 250, '3' : 500}, "Bob": {'1': 250, '2' : 250, '3' :500}, "Clair": {'1' :250, '2' : 500, '3' : 250}})
    >>> algorithm2(ex1, 1000, {'Alice': 250, 'Bob': 320, 'Clair': 430})
    (920, (Alice gets {1} with rent 130, Bob gets {2} with rent 270, Clair gets {3} with rent 520))

    >>> ex2 = AgentList({"Alice":{'1' : 250, '2' : 250, '3' : 500}, "Bob": {'1': 250, '2' : 250, '3' :500}, "Clair": {'1': 250, '2' : 250, '3' :500}})
    >>> algorithm2(ex2, 1000, {'Alice': 300, 'Bob': 300, 'Clair': 300})
    no solution

    >>> ex3 = AgentList({"Alice":{'1' : 250, '2' : 750}, "Bob": {'1': 250, '2' : 750}})
    >>> algorithm2(ex3, 1000, {'Alice': 600, 'Bob': 500})
    (918.75, (Alice gets {1} with rent 600, Bob gets {2} with rent 318.75))
    """

    return 0  # Empty implementation
