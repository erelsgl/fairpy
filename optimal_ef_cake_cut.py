#!python3

"""
Article name : Optimal Envy-Free Cake Cutting
Authors : Yuga J. Cohler, John K. Lai, David C. Parkes and Ariel D. Procaccia
Algorithm #1 : opt_piecewise_constant
Algorithm #2 : opt_piecewise_linear
Programmer: Tom Goldenberg
Since: 2020-05
"""
import operator
from logging import Logger

from agents import *
from allocations import *
import logging
import cvxpy
import numpy as np

logger: Logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
    >>> alice = PiecewiseConstantAgent([10,20,5,0], name='alice')
    >>> bob = PiecewiseConstantAgent([0,20,10,5], name='bob')
    >>> print(str(opt_piecewise_constant([alice,bob])))
    > alice gets [(0.0, 1.0), (1.0, 1.57)] with value 21.4
    > bob gets [(1.57, 2.0), (2.0, 3.0), (3.0, 4.0)] with value 23.6
    <BLANKLINE>
    """
    # > alice gets [(0.0, 1.0), (1.0, 1.5)] with value 20.0
    # > bob gets [(1.5, 2.0), (2.0, 3.0), (3.0, 4.0)] with value 25.0

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
    XiI = [[cvxpy.Variable(name=f'{agents[agent_index].name()} interval {piece_index+1} fraction', integer=False)
            for piece_index in range(num_of_pieces)]
           for agent_index in range(num_of_agents)]
    logger.info(f'Fraction matrix has {len(XiI)} rows (agents) and {len(XiI[0])} columns (intervals)')

    constraints = feasibility_constraints(XiI)

    agents_w = []
    for i in range(num_of_agents):
        value_of_i = sum([XiI[i][g] * value_matrix[i][g] for g in range(num_of_pieces)])
        agents_w.append(value_of_i)
        # agents_w.append(cvxpy.log(value_of_i))
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
    for agent_index in range(len(agents)):
        logger.info(f'Agent {agents[agent_index].name()} details after allocation\n'
                    f'total cake value {agents[agent_index].cake_value()}\n'
                    f'total allocation value {agents[agent_index].piece_value(a.get_piece(agent_index))}\n'
                    f'received pieces {a.get_piece(agent_index)}')

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
        # testttt = []
        # for i in range(num_of_agents):
        #     logger.info(f'[i][g]=[{i}][{g}] XiI[i][g]={XiI[i][g]}')
        #     testttt.append(XiI[i][g])
        # logger.info(f'testttt= {testttt}')
        # logger.info(f'sum testttt= {sum(testttt)}')
        # logger.info(f'sum testttt= {cvxpy.sum(testttt, keepdims=True)}')
        logger.info(f'Adding interval {g+1} "sum of fractions == 1" constraint: {sum_of_fractions}')
        constraints.append(sum_of_fractions)
        for i in range(num_of_agents):
            bound_fraction = [XiI[i][g] >= 0, XiI[i][g] <= 1]
            logger.info(f'Adding agent {i + 1} fraction constraint for piece {g + 1} {bound_fraction[0]}, {bound_fraction[1]}')
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


def opt_piecewise_linear(agents: List[Agent]) -> Allocation:
    """
     algorithm for finding an optimal EF allocation when agents have piecewise linear valuations.
    :param agents: a list of agents
    :return: an optimal envy-free allocation
    >>> ALICE = PiecewiseUniformAgent([(0, 0.5), (0.7, 0.9)], "ALICE")
    >>> BOB = PiecewiseUniformAgent([(0.1, 0.8)], "BOB")
    >>> print(str(opt_piecewise_linear([ALICE,BOB])))
    > ALICE gets [(0, 0.1), (0.7, 0.9)] with value 0.6
    > BOB gets [(0.1, 0.7)] with value 0.9
    """

    def Y(i, op, j, intervals):
        return [(start, end) for start, end in intervals if op(agents[i].eval(start, end), agents[j].eval(start, end))]

    def isIntersect(poly_1, poly_2):
        logger.info(f'isIntersect: poly_1={poly_1}, poly_2={poly_2}')
        m_1, c_1 = poly_1.c if len(poly_1.c) > 1 else [0, poly_1.c[0]]
        m_2, c_2 = poly_2.c if len(poly_2.c) > 1 else [0, poly_2.c[0]]
        logger.info(f'isIntersect: m_1={m_1} c_1={c_1}, m_2={m_2} c_2={c_2}')
        return (((c_2 - c_1) / (m_1 - m_2)) if (m_1 - m_2) != 0 else 0.0)

    def R(x):
        if agents[1].eval(x[0], x[1]) > 0:
            return agents[0].eval(x[0], x[1]) / agents[1].eval(x[0], x[1])
        return 0

    def V_l(agent_index, inter_list):
        logger.info(f'V_list(agent_index={agent_index}, inter_list={inter_list})')
        return sum([V(agent_index, start, end) for start, end in inter_list])
    #     return sum([agents[agent_index].eval(start,end) for start,end in inter_list])

    def V(agent_index, start, end):
        logger.info(f'V(agent_index={agent_index},start={start},end={end})')
        return agents[agent_index].eval(start, end)

    def get_optimal_allocation(agents):
        intervals = [(start, start + 1) for start in range(agents[0].cake_length())]
        logger.info(f'getting optimal allocation for initial intervals: {intervals}')
        new_intervals = []
        allocs = [[], []]
        for piece, (start, end) in enumerate(intervals):
            logger.info(f'get_optimal_allocation: piece={piece}, start={start}, end={end}')
            mid = isIntersect(agents[0].piece_poly[piece], agents[1].piece_poly[piece])
            if mid > 0:
                logger.info(f'mid={mid}')
                new_intervals.append((start, mid))
                if V(0, start, mid) > V(1, start, mid):
                    allocs[0].append((start, mid))
                else:
                    allocs[1].append((start, mid))
                start = mid
            if V(0, start, end) > V(1, start, end):
                allocs[0].append((start, end))
            else:
                allocs[1].append((start, end))
            new_intervals.append((start, end))
        return allocs, new_intervals

    def Y_op_r(pieces, op, r):
        result = []
        for start, end in pieces:
            if agents[0].eval(start, end) < agents[1].eval(start, end) and op(R((start, end)), r):
                result.append((start, end))
        return result

    allocation, pieces = get_optimal_allocation(agents)

    a = Allocation(agents)
    a.setPieces(allocation)

    y_0_gt_1 = Y(0, operator.gt, 1, pieces)
    y_1_gt_0 = Y(1, operator.gt, 0, pieces)
    y_0_eq_1 = Y(0, operator.eq, 1, pieces)
    y_0_ge_1 = Y(0, operator.ge, 1, pieces)
    y_1_ge_0 = Y(1, operator.ge, 0, pieces)
    y_0_lt_1 = Y(0, operator.lt, 1, pieces)
    logger.info(f'y_0_gt_1 {y_0_gt_1}')
    logger.info(f'y_1_gt_0 {y_1_gt_0}')
    logger.info(f'y_0_eq_1 {y_0_eq_1}')
    logger.info(f'y_0_ge_1 {y_0_ge_1}')
    logger.info(f'y_1_ge_0 {y_1_ge_0}')

    if (V_l(0, y_0_ge_1) >= (agents[0].cake_value() / 2) and
        V_l(1, y_1_ge_0) >= (agents[1].cake_value() / 2)):

        if (V_l(0, y_0_gt_1) >= (agents[0].cake_value() / 2)):
            a.setPieces([y_0_gt_1, y_1_ge_0])
        else:
            missing_value = (agents[0].cake_value() / 2) - V_l(0, y_0_gt_1)
            interval_options = []
            for start, end in y_0_eq_1:
                mid = agents[0].mark(start, missing_value)
                logger.info(f'start {start}, end {end}, mid {mid}, missing value {missing_value}')
                if mid:
                    interval_options.append([(start, mid), (mid, end)])
            logger.info(f'int_opt {interval_options}')
            agent_0_inter, agent_1_inter = interval_options.pop()
            y_0_gt_1.append(agent_0_inter)
            y_1_gt_0.append(agent_1_inter)
            logger.info(f'agent 0 pieces {y_0_gt_1}')
            logger.info(f'agent 1 pieces {y_1_gt_0}')
            a.setPieces([y_0_gt_1, y_1_gt_0])
            return a

    if V_l(0, y_0_ge_1) < (agents[0].cake_value() / 2):
        ratio_dict = {x: R(x) for x in y_0_lt_1}
        y_le_r_dict = {r: Y_op_r(y_0_lt_1, operator.ge, r) for inter, r in ratio_dict.items()}
        valid_r_dict = {}
        for r, val in y_le_r_dict.items():
            temp_list = y_0_gt_1 + val
            if V_l(0, temp_list) >= (agents[0].cake_length() / 2):
                valid_r_dict[r] = val


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
