#!python3

"""
Article name : Optimal Envy-Free Cake Cutting
Authors : Yuga J. Cohler, John K. Lai, David C. Parkes and Ariel D. Procaccia
Algorithm #1 : opt_piecewise_constant
Algorithm #2 : opt_piecewise_linear
Programmer: Tom Goldenberg
Since: 2020-05
"""

from agents import *
from allocations import *
import itertools as it
import logging
from queue import PriorityQueue

# logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


def opt_piecewise_constant(agents: List[Agent], values: List[List]) -> Allocation:
    """
    algorithm for finding an optimal EF allocation when agents have piecewise constant valuations.
    :param agents: a list of agents
    :param values: a list of lists holding the values for each interval
    :return: an optimal envy-free allocation

    >>> ALICE = PiecewiseUniformAgent([(0, 0.5), (0.7, 0.9)], "ALICE")
    >>> BOB = PiecewiseUniformAgent([(0.1, 0.8)], "BOB")
    >>> _values = [[0.5, 0.5], [1]]
    >>> print(str(opt_piecewise_constant([ALICE,BOB], _values)))
    > ALICE gets [(0, 1), (3, 4), (4, 5)] with value 0.6
    > BOB gets [(1, 2), (2, 3)] with value 0.857
    <BLANKLINE>
    """
    num_of_agents = len(agents)

    # Check for correct number of agents
    if num_of_agents < 2:
        raise ValueError(f'Optimal EF Cake Cutting works only for two agents or more')

    logging.debug(f'Valid Number of agents: {num_of_agents}')

    # Check for correct amount of values
    if num_of_agents != len(values):
        raise ValueError(f'Number of agents not equal to number of values')

    logging.debug(f'Valid Number of agents values: {len(values)}\n')

    # Check for each agent's region there is a matching value
    for agent, agent_values in zip(agents, values):
        logging.debug(f'Validating Agent {agent.name()}')
        if len(agent.desired_regions) != len(agent_values):
            raise ValueError(f'Missing values for agent {agent} intervals')
        logging.debug(f'Valid {len(agent_values)} values and {len(agent.desired_regions)} regions')

        # Check agents cake boundaries are valid and normalized
        for start, end in agent.desired_regions:
            if start < 0 or start > end or end > 1:
                raise ValueError(f'Agent {agent.name} cake boundaries are invalid ({start},{end})')
        logging.debug(f'Valid regions {agent.desired_regions}')

        # Check agents cake total value lower or equal to 1, if not normalize
        agent_cake_value = sum(agent_values)
        if agent_cake_value > 1 or agent_cake_value < 0:
            raise ValueError(f'Agent {agent.name()} cake total value is invalid: {agent_cake_value}')
        logging.debug(f'Valid cake total value: {agent_cake_value}')
        logging.debug(f'{agent.name()} in a valid Agent\n')

    # "Mark the boundaries of the reported intervals of all agents"
    # Create cake intervals boudaries
    boundaries = [cut for agent in agents for piece in agent.desired_regions for cut in piece]
    boundaries.sort()
    logging.debug(f'Cake boundaries are {boundaries}')

    # Create cake pieces intervals
    pieces = [(p_start, p_end) for p_start, p_end in zip(boundaries[:-1], boundaries[1:])]
    logging.debug(f'Cake pieces are {pieces}')

    piecewise_constant_agents = create_piecewise_constant_agents(agents=agents, values=values, pieces=pieces)
    norm_pieces = [(start, start + 1) for start in range(len(pieces))]
    possible_allocations = create_cake_allocation_options(piecewise_constant_agents=piecewise_constant_agents,
                                                          pieces=norm_pieces)

    while not possible_allocations.empty():
        val, alloc = possible_allocations.get()
        logging.debug(f'Allocation {alloc} with value:{-1 * val}')

        allocation_list = create_allocation_list(piecewise_constant_agents, alloc, norm_pieces)
        a = Allocation(piecewise_constant_agents)

        a.setPieces(allocation_list)
        if a.isEnvyFree(2):
            logging.debug(f'Allocation {allocation_list} is optimal and EF')
            return a
    logging.debug(f'Optimal EF allocation was not found')
    return False


def opt_piecewise_linear(agents: List[Agent], values: List[List], slopes: List[List]) -> Allocation:
    """
     algorithm for finding an optimal EF allocation when agents have piecewise linear valuations.
    :param agents: a list of agents
    :param values: a list of lists holding the values for each interval (start of the interval)
    :param slopes: a list of lists holding the slope for each interval
    :return: an optimal envy-free allocation
    >>> ALICE = PiecewiseUniformAgent([(0, 0.5), (0.7, 0.9)], "ALICE")
    >>> BOB = PiecewiseUniformAgent([(0.1, 0.8)], "BOB")
    >>> values = [[1, 2], [1]]
    >>> _slopes = [[1, -2], [2]]
    >>> print(str(opt_piecewise_constant([ALICE,BOB], values)))
    > ALICE gets [(0, 0.1), (0.7, 0.9)] with value 0.6
    > BOB gets [(0.1, 0.7)] with value 0.9
    """
    pass


def create_allocation_list(piecewise_constant_agents, alloc, norm_pieces):
    allocation_list = []
    for agent in piecewise_constant_agents:
        agent_pieces = [piece for assignment, piece in zip(alloc, norm_pieces) if assignment == agent.name()]
        allocation_list.append(agent_pieces)
    return allocation_list


def create_cake_allocation_options(piecewise_constant_agents, pieces):
    cake_option = []
    value_dict = []
    for piece_index in range(len(pieces)):
        piece_options = []
        piece_values = {}
        for agent in piecewise_constant_agents:
            if agent.values[piece_index] > 0:
                piece_options.append(agent.name())
                piece_values[agent.name()] = agent.values[piece_index]
        cake_option.append(piece_options)
        value_dict.append(piece_values)
    logging.debug(f'Cake options are: {cake_option}')
    logging.debug(f'Values dict: {value_dict}')

    allocation_options = list(it.product(*cake_option))
    logging.debug(f'Allocation options are: {allocation_options}')

    q = PriorityQueue()
    for allocation_option in allocation_options:
        val = sum([value_dict[index].get(agent) for index, agent in enumerate(allocation_option)])
        q.put((-1 * val, allocation_option))
    return q


def create_piecewise_constant_agents(agents, values, pieces):
    new_agents = []
    for agent,value in zip(agents, values):
        logging.debug(f'Creating piecewise constant agent for {agent.name()}')
        agent_new_pieces_values = [None]*len(pieces)
        piece_index = 0
        for piece_start, piece_end in pieces:
            logging.debug(f'Creating new value for piece ({piece_start},{piece_end})')
            for region, piece_value in zip(agent.desired_regions, value):
                logging.debug(f'Checking region: {region} with value of {piece_value}')
                if piece_start >= region[0] and piece_end <= region[1] and agent_new_pieces_values[piece_index] is None:
                    piece_fraction = (piece_end - piece_start)/(region[1] - region[0])
                    agent_new_pieces_values[piece_index] = (piece_value * piece_fraction)
                    logging.debug(f'Added value of {piece_value * piece_fraction} to new piece values list')
            if agent_new_pieces_values[piece_index] is None:
                agent_new_pieces_values[piece_index] = 0
                logging.debug(f'Added value of 0 to new piece values list')
            piece_index += 1
        new_agents.append(PiecewiseConstantAgent(agent_new_pieces_values, agent.name()))
    return new_agents


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures,tests))
