#!python3

"""
Truthful auction of Heterogeneous Divisible Goods with an approximation algorithm.

References:

    Yonatan Aumann, Yair Dombb, Avinatan Hassidim (2015):
    "Auctioning time: Truthful auctions of heterogeneous divisible goods"
    ACM Transactions on Economics and Computation, 4(1).

Programmers: Naama Berman and Yonatan Lifshitz
Since: 2019-12
"""

from fairpy.agents import *
from fairpy import Allocation

import random, logging
from typing import *
from networkx import *
from math import *

logger = logging.getLogger(__name__)

def stringify_agent_piece_graph(g: Graph):
    """ Convert an agent-piece graph into a string, for display and testing """
    return str([(agent.name(), piece, data) for (agent,piece,data) in g.edges(data=True)])

def stringify_edge_set(s: set):
    """ Convert an agent-piece graph into a string, for display and testing """
    return str(sorted([(agent.name(), piece) for (agent,piece) in s]))

def equally_sized_pieces(agents: List[Agent], piece_size: float) -> Allocation:
    """
    Algorithm 1.
    Approximation algorithm of the optimal auction for uniform-size pieces.

    Complexity and approximation:
    - Requires only 2 / l values from each agent.
    - Runs in time polynomial in n + 1 / l.
    - Approximates the optimal welfare by a factor of 2.

    :param agents: A list of Agent objects.
    :param piece_size: Size of an equally sized piece (in the paper: l).
    :return: A cake-allocation, not necessarily all the cake will be allocated.

    The doctest will work when the set of edges will return according lexicographic order
    >>> Alice = PiecewiseConstantAgent([100, 1], "Alice")
    >>> Bob = PiecewiseConstantAgent([2, 90], "Bob")
    >>> equally_sized_pieces([Alice, Bob], 0.5)
    Alice gets {(0, 1)} with value 100.
    Bob gets {(1, 2)} with value 90.
    <BLANKLINE>

    The doctest will work when the set of edges will return according lexicographic order
    >>> Alice = PiecewiseConstantAgent([1, 1, 1, 1, 1], "Alice")
    >>> Bob = PiecewiseConstantAgent([3, 3, 3, 1, 1], "Bob")
    >>> equally_sized_pieces([Alice, Bob], 3 / 5)
    Alice gets {(2, 5)} with value 3.
    Bob gets {(0, 3)} with value 9.
    <BLANKLINE>
    """
    # > Bob gets {(0, 3)} with value 9.00

    # Initializing variables and asserting conditions
    num_of_agents = len(agents)
    if num_of_agents == 0:
        raise ValueError("There must be at least one agent")
    if not 0 < piece_size <= 1:
        raise ValueError("Piece size must be between 0 and 1")

    logger.info("Piece size (l) = %f", piece_size)
    delta = 1 - int(1 / piece_size) * piece_size
    logger.info("Delta := 1 - floor(1 / l) * l = %f", delta)

    logger.info("Create the partitions P_0_l and P_d_l")
    # Creating the partition of the pieces that start from 0
    partition_0_l = create_partition(piece_size)
    logger.info("  The partition P_0_l (l-sized pieces starting at 0) = %s", partition_0_l)
    # Creating the partition of the pieces that start from delta
    partition_delta_l = create_partition(piece_size, start=delta)
    logger.info("  The partition P_d_l (l-sized pieces starting at delta) = %s", partition_delta_l)
    # Merging the partitions to one partition
    all_partitions = partition_0_l + partition_delta_l

    length = max([a.cake_length() for a in agents])
    # Normalizing the partitions to match the form of the pieces allocation of the Agents
    normalize_partitions = [(int(p[0] * length), int(p[1] * length)) for p in all_partitions]
    normalize_partitions_0_l = [(int(p[0] * length), int(p[1] * length)) for p in partition_0_l]
    normalize_partitions_delta_l = [(int(p[0] * length), int(p[1] * length)) for p in partition_delta_l]

    # Evaluating the pieces of the partition for every agent there is
    logger.info("For each piece (in both partitions) and agent: compute the agent's value of the piece.")
    evaluations = {}
    # Get evaluation for every piece
    for piece in normalize_partitions:
        # For every piece get evaluation for every agent
        for agent in agents:
            evaluations[(agent, piece)] = agent.eval(start=piece[0], end=piece[1])
    # Create the matching graph
    # One side is the agents, the other side is the partitions and the weights are the evaluations
    logger.info("Create the partition graphs G_0_l and G_d_l")
    g_0_l = create_matching_graph(agents, normalize_partitions_0_l, evaluations)
    logger.info("  The graph G_0_l = %s", stringify_agent_piece_graph(g_0_l))
    g_delta_l = create_matching_graph(agents, normalize_partitions_delta_l, evaluations)
    logger.info("  The graph G_d_l = %s", stringify_agent_piece_graph(g_delta_l))

    # Set the edges to be in order, (Agent, partition)
    logger.info("Compute maximum weight matchings for each graph respectively")
    edges_set_0_l = fix_edges(max_weight_matching(g_0_l))
    logger.info("  The edges in G_0_l = %s", stringify_edge_set(edges_set_0_l))
    edges_set_delta_l = fix_edges(max_weight_matching(g_delta_l))
    logger.info("  The edges in G_d_l = %s", stringify_edge_set(edges_set_delta_l))

    logger.info("Choose the heavier among the matchings")
    # Check which matching is heavier and choose it
    if calculate_weight(g_delta_l, edges_set_delta_l) > calculate_weight(g_0_l, edges_set_0_l):
        edges_set = edges_set_delta_l
    else:
        edges_set = edges_set_0_l

    # Find the agents that are in the allocation that was chosen
    chosen_agents = [agent for (agent,piece) in edges_set]
    chosen_agents.sort(key=lambda agent:agent.name())
    # Create allocation

    pieces = len(chosen_agents)*[None]
    # Add the edges to the allocation
    for edge in edges_set:
        pieces[chosen_agents.index(edge[0])] = [edge[1]]
    return Allocation(chosen_agents, pieces)


def discrete_setting(agents: List[Agent], pieces: List[Tuple[float, float]]) -> Allocation:
    """
    Algorithm 2.
    Approximation algorithm of the optimal auction for a discrete cake with known piece sizes.

    Complexity and approximation:
    - Requires at most 2m values from each agent.
    - Runs in time polynomial in n + log m.
    - Approximates the optimal welfare by a factor of log m + 1.

    :param agents: A list of Agent objects.
    :param pieces: List of sized pieces.
    :return: A cake-allocation.

    The doctest will work when the set of edges will return according lexicographic order
    >>> Alice = PiecewiseConstantAgent([100, 1], "Alice")
    >>> Bob = PiecewiseConstantAgent([2, 90], "Bob")
    >>> discrete_setting([Alice, Bob], [(0, 1), (1, 2)])
    Alice gets {(0, 1)} with value 100.
    Bob gets {(1, 2)} with value 90.
    <BLANKLINE>

    """
    # Set m to be the number of pieces in the given partition
    m = len(pieces)
    # Set r to be log of the number of pieces
    r = int(log(m, 2))

    max_weight = 0
    max_match = None

    logger.info("For every t = 0,...,r create the 2 ^ t-partition, partition sequence of 2 ^ t items.")
    logger.info("Denote the t-th partition by Pt.")
    # Go over the partition by powers of 2
    for t in range(0, r + 1):
        logger.info("Iteration t = %d", t)
        # Change the partition to be a partition with 2^t size of every piece
        partition_i = change_partition(pieces, t)

        logger.info("For each piece and agent: compute the agent's value of the piece.")
        # Evaluate every piece in the new partition
        evaluations = {}
        # Go over every piece in the partition
        for piece in partition_i:
            # Go over each Agent
            for agent in agents:
                # Evaluate the piece according to the Agent
                evaluations[(agent, piece)] = agent.eval(start=piece[0], end=piece[1])

        logger.info("create the partition graph G - Pt=%d", t)
        # Create the matching graph according to the new partition
        g_i = create_matching_graph(agents, partition_i, evaluations)
        logger.info("Compute a maximum weight matching Mt in the graph GPt")
        # Find the max weight matching of the graph and get the set of edges of the matching
        edges_set = max_weight_matching(g_i)
        # Set the edges to be in order, (Agent, partition)
        edges_set = fix_edges(edges_set)
        # Calculate the sum of the weights in the edges set
        weight = calculate_weight(g_i, edges_set)
        # Check for the max weight
        if weight > max_weight:
            max_weight = weight
            # Keep the edges set of the max weight
            max_match = edges_set

    # Get the agents that are part of the edges of the max weight
    chosen_agents = [edge[0] for edge in max_match]
    chosen_agents.sort(key=lambda agent:agent.name())
    # Create the allocation
    pieces = len(chosen_agents)*[None]
    # Add the edges to the allocation
    for edge in max_match:
        pieces[chosen_agents.index(edge[0])] = [edge[1]]
    return Allocation(chosen_agents, pieces)


def continuous_setting(agents: List[Agent]) -> Allocation:
    """
    Algorithm 3.
    Approximation algorithm of the optimal auction for a continuous cake.

    Complexity and approximation:
    - Requires at most 2n2 values from each agent.
    - Runs in time polynomial in n.
    - Approximates the optimal welfare by a factor of O(log n).

    :param agents: A list of Agent objects.
    :return: A cake-allocation.

    >>> Alice1 = PiecewiseConstantAgent([100, 1], "Alice")
    >>> Alice2 = PiecewiseConstantAgent([100, 1], "Alice")
    >>> continuous_setting([Alice1, Alice2])
    Alice gets {(0, 2.0)} with value 101.
    <BLANKLINE>
    """
    # set n to be the number of agents
    n = len(agents)
    logger.info("Choose n/2 agents at random. Denote this set by S.")
    # Choose randomly half of the agents
    s = random.choices(agents, k=n//2)
    # Create a new partition
    partitions = set()
    # Add the start to the partition
    partitions.add(0)

    logger.info("For every agent i in S, ask i to divide [0, 1] into 2n intervals of equal worth")
    # Go over all the agents that were chosen
    for a in s:
        start = 0
        # Get pieces with value of 2n
        for i in range(0,2*n):
            end = a.mark(start, a.total_value() / (2 * n))
            # if the piece is out of boundaries we don't add it to the partition
            if end is None:
                break
            end = float("%.4f" % end)
            # Add the piece to the partition
            partitions.add(end)
            start = end

    partitions = list(partitions)
    # Sort the pieces
    partitions = sorted(partitions)

    logger.info("Generate a partition J by taking the union of all boundary points reported by the agents of S.")
    # Turn the list of the pieces into one partition
    start = partitions[0]
    pieces = []
    # Go over all the parts of the partitions and turn it to one partition
    for part in partitions[1:]:
        p = (start, part)
        pieces.append(p)
        start = part

    logger.info("Invoke Algorithm 2 on the rest of the agents and on the sequence of items in J")
    # Get the agents that were nor chosen
    agents = list(set(agents) - set(s))
    # Find the best allocation for those agents with the partition we generated and use Algo 2 to do that
    res = discrete_setting(agents, pieces)
    # Return the allocation
    return res


def create_partition(size: float, start: float=0) -> List[Tuple[float, float]]:
    """
    Used in algorithm 1.
    Creating a partition of [0, 1] with equally sized pieces of given size starting from a given start.
    :param size: The size of the pieces.
    :param start: The location the pieces will start from.
    :return: A partition as described.

    >>> create_partition(0.5, 0)
    [(0, 0.5), (0.5, 1.0)]

    """
    #print("create_partition: size- ", size, "start- ", start)
    res = []
    end = start + size
    # Iterate until we divide all the cake into pieces
    while end <= 1:
        # add the piece to the list
        res.append((start, end))
        start = end
        end = start + size
    #print("create_partition: return value- ", res)
    return res


def fix_edges(edges_set: Set[Tuple[Agent, Tuple[float, float]]]) -> Set[Tuple[Agent, Tuple[float, float]]]:
    """
    Used in algorithm 1 and 2.
    Fix the edge format, sometimes the edges are written backwards
    since the matching algorithm does not care about the edge direction.
    Each edge contains agent and a piece, this function will make sure the agent comes first in the edge.
    :param edges_set: A set of edges to fix.
    :return: A copy of the fixed set of edges.

    >>> Alice = PiecewiseConstantAgent([100, 1], "Alice")
    >>> Bob = PiecewiseConstantAgent([2, 90], "Bob")
    >>> partitions = [(0, 1), (1, 2)]
    >>> edges_set = {(Alice, (0, 1.4889))}
    >>> fix_edges(edges_set)
    [(Alice is an agent with a Piecewise-constant valuation with values [100   1] and total value=101, (0, 1.4889))]
    """
    ret = []
    # Go over all the edges and check if they are in the right order
    for edge in edges_set:
        # If the partition is first we swap the sides of the edge
        if not isinstance(edge[0], Agent):
            ret.append((edge[1], edge[0]))
        else:
            # The Agent is first and we leave it like that
            ret.append((edge[0], edge[1]))
    # we return the set of edges when all the edges are in the right order of (Agent, partition)

    return ret


def change_partition(partition: List[tuple], t: int) -> List[tuple]:
    """
    Used in algorithm 2.
    Create a partition from original partition where each 2 ^ t pieces are united.
    :param partition: The original partition.
    :param t: Defines the size of the new partition.
    :return: A partition with pieces with 2 ^ t size.

    >>> change_partition([(0.0, 1.0), (1.0, 2.0)], 1)
    [(0.0, 2.0)]

    """

    ret = []
    # Go over all the original partitions with 2^t jumps
    for start in range(0, len(partition) - 2 ** t + 1, 2 ** t):
        end = start + 2 ** t - 1
        # Add the new joined partition to the list
        ret.append((partition[start][0], partition[end][1]))
    return ret


def calculate_weight(g: Graph, edges_set: Set[Tuple[Agent, Tuple[float, float]]]) -> float:
    """
    Used in algorithm 2.
    Calculates the weight of a match over a graph.
    :param g: The graph with all the weights.
    :param edges_set: The edges of the matching - for which we will sum the weight.
    :return: A single number - the total weight.

    >>> Alice = PiecewiseConstantAgent([100, 1], "Alice")
    >>> Bob = PiecewiseConstantAgent([2, 90], "Bob")
    >>> partitions = [(0, 1), (1, 2)]
    >>> g = create_matching_graph([Alice, Bob], partitions, {(Alice, (0, 1)): 100.0, (Bob, (0, 1)): 2.0, (Alice, (1, 2)): 1.0, (Bob, (1, 2)): 90.0})
    >>> calculate_weight(g, {(Bob,(1,2)), (Alice, (0,1))})
    190.0

    """
    ret = 0
    # Go over all the weights of the edges and sum the weights
    for edge in edges_set:
        ret += g.get_edge_data(edge[0], edge[1])['weight']
    return ret


def create_matching_graph(left: List[Agent], right: List[Tuple[float, float]],
                          weights: Dict[Tuple[Agent, Tuple[float, float]], float])-> Graph:
    """
    Used in algorithm 2 and 3.
    Creating a weighted bi-partition graph that represents agents, cake pieces and values.
    :param left: List of agents.
    :param right: List of cake pieces.
    :param weights: A dictionary from agents to pieces - represents the value of each agent to each piece.
    :return: A graph object from the given parameters.

    >>> Alice = PiecewiseConstantAgent([100, 1], "Alice")
    >>> Bob = PiecewiseConstantAgent([2, 90], "Bob")
    >>> partitions = [(0, 1), (1, 2)]
    >>> g = create_matching_graph([Alice, Bob], partitions, {(Alice, (0, 1)): 100.0, (Bob, (0, 1)): 2.0, (Alice, (1, 2)): 1.0, (Bob, (1, 2)): 90.0})
    >>> list(g.edges(data=True))
    [(Alice is an agent with a Piecewise-constant valuation with values [100   1] and total value=101, (0, 1), {'weight': 100.0}), (Alice is an agent with a Piecewise-constant valuation with values [100   1] and total value=101, (1, 2), {'weight': 1.0}), (Bob is an agent with a Piecewise-constant valuation with values [ 2 90] and total value=92, (0, 1), {'weight': 2.0}), (Bob is an agent with a Piecewise-constant valuation with values [ 2 90] and total value=92, (1, 2), {'weight': 90.0})]

    """

    # Create the graph
    g = Graph()
    # g.edges(data = True)
    # Set the left side of the graph to be the Agents
    g.add_nodes_from(left, bipartite=0)
    # Set the right side of the graph to be the partitions
    g.add_nodes_from(right, bipartite=1)
    # Set the edges of the graph with their weights
    for key, value in weights.items():
        g.add_edge(key[0], key[1], weight=value)
    return g


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
