#!python3

"""
Article name : Optimal Envy-Free Cake Cutting
Authors : Yuga J. Cohler, John K. Lai, David C. Parkes and Ariel D. Procaccia
Algorithm #1 : opt_piecewise_constant
Algorithm #2 : opt_piecewise_linear
Programmer: Tom Goldenberg
Since: 2020-05
"""
from logging import Logger

from agents import *
from allocations import *
import logging
import cvxpy
import numpy as np

logger: Logger = logging.getLogger(__name__)


def opt_piecewise_constant(agents: List[Agent]) -> Allocation:
    """
    algorithm for finding an optimal EF allocation when agents have piecewise constant valuations.
    :param agents: a list of PiecewiseConstantAgent agents
    :return: an optimal envy-free allocation

    >>> alice = PiecewiseConstantAgent([15,15,0,30,30], name='alice')
    >>> bob = PiecewiseConstantAgent([0,30,30,30,0], name='bob')
    >>> gin = PiecewiseConstantAgent([10,0,30,0,60], name='gin')
    >>> print(str(opt_piecewise_constant([alice,bob,gin])))
    > alice gets [(0.0, 1.0), (3.0, 4.0)] with value 45.0
    > bob gets [(1.0, 2.0), (2.0, 3.0)] with value 60.0
    > gin gets [(4.0, 5.0)] with value 60.0
    <BLANKLINE>
    >>> print(str(opt_piecewise_constant([alice,bob])))
    > alice gets [(0.0, 1.0), (3.0, 3.75), (4.0, 5.0)] with value 67.5
    > bob gets [(1.0, 2.0), (2.0, 3.0), (3.75, 4.0)] with value 67.5
    <BLANKLINE>
    >>> print(str(opt_piecewise_constant([alice,gin])))
    > alice gets [(0.0, 1.0), (1.0, 2.0), (3.0, 4.0)] with value 60.0
    > gin gets [(2.0, 3.0), (4.0, 5.0)] with value 90.0
    <BLANKLINE>
    >>> print(str(opt_piecewise_constant([gin,bob])))
    > gin gets [(0.0, 1.0), (2.0, 2.33), (4.0, 5.0)] with value 79.9
    > bob gets [(1.0, 2.0), (2.33, 3.0), (3.0, 4.0)] with value 80.1
    <BLANKLINE>
    """
    value_matrix = [list(agent.values) for agent in agents]
    num_of_agents = len(value_matrix)
    num_of_pieces = len(value_matrix[0])

    # Check for correct number of agents
    if num_of_agents < 2:
        raise ValueError(f'Optimal EF Cake Cutting works only for two agents or more')
    logger.info(f'Received {num_of_agents} agents')

    if not all([agent.cake_length() == agents[0].cake_length() for agent in agents]):
        raise ValueError(f'Agents cake lengths are not equal')
    logger.info(f'Each agent cake length is {agents[0].cake_length()}')

    # XiI[i][I] represents the fraction of interval I given to agent i. Should be in {0,1}.
    XiI = [[cvxpy.Variable(name=f'{agents[agent_index].name()} interval {piece_index} fraction', integer=False)
            for piece_index in range(num_of_pieces)]
           for agent_index in range(num_of_agents)]
    logger.info(f'Fraction matrix has {len(XiI)} rows (agents) and {len(XiI[0])} columns (intervals)')

    constraints = feasibility_constraints(XiI)

    agents_w = []
    for i in range(num_of_agents):
        value_of_i = sum([XiI[i][g] * value_matrix[i][g] for g in range(num_of_pieces)])
        agents_w.append(cvxpy.log(value_of_i))
        value_of_j = sum([XiI[j][g] * value_matrix[i][g]
                          for g in range(num_of_pieces)
                          for j in range(num_of_agents) if j != i])
        logger.info(f'Adding Envy-Free constraint for agent: {agents[i].name()},\n{value_of_j} <= {value_of_i}')
        constraints.append(value_of_j <= value_of_i)

    objective = sum(agents_w)
    logger.info(f'Objective function to maximize is {objective}')

    prob = cvxpy.Problem(cvxpy.Maximize(objective), constraints)
    prob.solve()
    logger.info(f'Problem status: {prob.status}')

    pieces_allocation = get_pieces_allocations(num_of_pieces, XiI)
    a = Allocation(agents)
    a.setPieces(pieces_allocation)
    logger.info(f'Allocation is envy-free {a.isEnvyFree(3)}')

    return a


def feasibility_constraints(XiI: list) -> list:
    """
    Generate the feasibility constraints of the given matrix, namely:
    * Each XiI is between 0 and 1;
    * For each g, the sum of XiI is 1.
    :param XiI: a list of lists of variables: XiI[i,g] is the amount of interval g given to agent i.
    :return: a list of constraints.
    """
    constraints = []
    num_of_agents = len(XiI)
    num_of_items = len(XiI[0])
    for g in range(num_of_items):
        sum_of_fractions = 1 == sum([XiI[i][g] for i in range(num_of_agents)])
        logger.info(f'Adding interval {g+1} "sum of fractions" constraint {sum_of_fractions}')
        constraints.append(sum_of_fractions)
        for i in range(num_of_agents):
            bound_fraction = [XiI[i][g] >= 0, XiI[i][g] <= 1]
            logger.info(f'Adding agent {i + 1} fraction constraint for piece {g + 1} {sum_of_fractions}')
            constraints += bound_fraction
    return constraints


def get_pieces_allocations(num_of_pieces: int, XiI: list) -> list:
    """
    Generate a list of interval allocation per agent
    :param num_of_pieces: number of intervals
    :param XiI: a list of lists of variables: XiI[i,g] is the amount of interval g given to agent i.
    :return: list of interval allocation per agent
    """
    piece_help = [0.0 for _ in range(num_of_pieces)]
    piece_alloc = []
    for fraction_list in XiI:
        agent_alloc = []
        for i in range(len(fraction_list)):
            fraction = np.round(fraction_list[i].value, 2)
            if fraction > 0:
                int_start = piece_help[i] + i
                agent_alloc.append((int_start, int_start + fraction))
                piece_help[i] += fraction
        piece_alloc.append(agent_alloc)
        logger.info(f'Agent {len(piece_alloc)} pieces are {agent_alloc}')
    return piece_alloc


# def opt_piecewise_linear(agents: List[Agent]) -> Allocation:
#     """
#      algorithm for finding an optimal EF allocation when agents have piecewise linear valuations.
#     :param agents: a list of agents
#     :return: an optimal envy-free allocation
#     >>> ALICE = PiecewiseUniformAgent([(0, 0.5), (0.7, 0.9)], "ALICE")
#     >>> BOB = PiecewiseUniformAgent([(0.1, 0.8)], "BOB")
#     >>> print(str(opt_piecewise_linear([ALICE,BOB])))
#     > ALICE gets [(0, 0.1), (0.7, 0.9)] with value 0.6
#     > BOB gets [(0.1, 0.7)] with value 0.9
#     """
#     pass


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
