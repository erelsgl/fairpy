"""
Implement an "almost-egalitarian" course allocation,
by rounding a linear program.

Programmer: Erel Segal-Halevi.
Since: 2023-07
"""

from fairpy.courses.instance import Instance
from fairpy.courses.allocation_utils import sorted_allocation, rounded_allocation
from fairpy.courses.linear_programming_utils import allocation_variables, allocation_constraints

import cvxpy, numpy as np, networkx
from cvxpy_leximin import Problem, Leximin
from fairpy.solve import solve
import matplotlib.pyplot as plt # for plotting the consumption graph (for debugging)


import logging
logger = logging.getLogger(__name__)

def fractional_leximin_optimal_allocation(instance: Instance, normalize_utilities=True, **solver_options):
    """
    Find the leximin-optimal (aka Egalitarian) allocation.
    :param instance: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
    :param allocation_constraint_function: a predicate w: R -> {true,false} representing an additional constraint on the allocation variables.
    :param solver_options: kwargs sent to the cvxpy solver.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
    The allocation should maximize the leximin vector of utilities.
    >>> logger.setLevel(logging.WARNING)
    >>> np.set_printoptions(precision=3)

    >>> instance = Instance(valuations=[[5,0],[3,3]])
    >>> a = fractional_leximin_optimal_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 0.75, 1: 0.0}, 1: {0: 0.25, 1: 1.0}}

    >>> instance = Instance(valuations=[[3,0],[5,5]])
    >>> a = fractional_leximin_optimal_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 1.0, 1: 0.0}, 1: {0: 0.0, 1: 1.0}}

    >>> instance = Instance(valuations=[[5,5],[3,0]])
    >>> a = fractional_leximin_optimal_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 0.0, 1: 1.0}, 1: {0: 1.0, 1: 0.0}}

    >>> instance = Instance(valuations=[[3,0,0],[0,4,0],[5,5,5]])
    >>> a = fractional_leximin_optimal_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 1.0, 1: 0.0, 2: 0.0}, 1: {0: 0.0, 1: 1.0, 2: 0.0}, 2: {0: 0.0, 1: 0.0, 2: 1.0}}

    >>> instance = Instance(valuations=[[4,0,0],[0,3,0],[5,5,10],[5,5,10]])
    >>> a = fractional_leximin_optimal_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 1.0, 1: 0.0, 2: 0.0}, 1: {0: 0.0, 1: 1.0, 2: 0.0}, 2: {0: 0.0, 1: 0.0, 2: 0.5}, 3: {0: 0.0, 1: 0.0, 2: 0.5}}

    >>> instance = Instance(valuations=[[3,0,0],[0,3,0],[5,5,10],[5,5,10]])
    >>> a = fractional_leximin_optimal_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 1.0, 1: 0.0, 2: 0.0}, 1: {0: 0.0, 1: 1.0, 2: 0.0}, 2: {0: 0.0, 1: 0.0, 2: 0.5}, 3: {0: 0.0, 1: 0.0, 2: 0.5}}

    >>> instance = Instance(valuations=[[1/3, 0, 1/3, 1/3],[1, 1, 1, 0]])
    >>> a = fractional_leximin_optimal_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 1.0, 1: 0.0, 2: 1.0, 3: 1.0}, 1: {0: 0.0, 1: 1.0, 2: 0.0, 3: 0.0}}
    """

    allocation_vars, raw_utilities, normalized_utilities = allocation_variables(instance)
    utilities = normalized_utilities if normalize_utilities else raw_utilities
    problem = Problem(
        Leximin(utilities.values()),
        constraints=allocation_constraints(instance, allocation_vars),
        **solver_options
    )
    solve(problem, solvers = [(cvxpy.SCIPY, {'method':'highs-ds'})])  # highs-ds is a variant of simplex (guaranteed to return a corner solution)
    allocation_matrix = {agent: {item: allocation_vars[agent][item].value+0 for item in instance.items} for agent in instance.agents}
    # logger.debug("\nAllocation_matrix:\n%s", allocation_matrix)
    # logger.debug("\nRaw utilities:\n%s", {agent: raw_utilities[agent].value+0 for agent in instance.agents})
    # logger.debug("\nMax utilities:\n%s", {agent: instance.agent_maximum_value(agent) for agent in instance.agents})
    # logger.debug("\nNormalized utilities:\n%s", {agent: normalized_utilities[agent].value+0 for agent in instance.agents})
    return allocation_matrix



def consumption_graph(allocation:dict, min_fraction=0.01)->networkx.Graph:
    """
    Generate the consumption graph of the given allocation.
    It is a bipartite graph between agents and items, where there is an edge if the agent consumes a positive amount of the item.
    """
    G = networkx.Graph()
    for agent,bundle in allocation.items():
        for item,fraction in bundle.items():
            if fraction>=min_fraction:
                G.add_edge(agent,item, weight=np.round(fraction,2))
    return G



def draw_bipartite_weighted_graph(G: networkx.Graph, top_nodes:list):
    draw_options = {
        "font_size": 10,
        "node_size": 700,
        "node_color": "yellow",
        "edgecolors": "black",
        "linewidths": 1,
        "width": 1,
        "with_labels": True
    }
    pos = networkx.bipartite_layout(G, top_nodes)
    networkx.draw(G, **draw_options, pos=pos)
    networkx.draw_networkx_edge_labels(G, pos, networkx.get_edge_attributes(G, "weight"))
    plt.show()


def almost_egalitarian_allocation(instance: Instance, **solver_options):
    """
    Finds an almost-egalitarian allocation.

    >>> from dicttools import stringify

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=1, item_capacities=1)
    >>> stringify(almost_egalitarian_allocation(instance))
    "{avi:['x'], beni:['w']}"

    # >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=2, item_capacities=1)
    # >>> stringify(almost_egalitarian_allocation(instance))
    # "{avi:['x', 'y'], beni:['w', 'z']}"

    # >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=3, item_capacities=2)
    # >>> stringify(almost_egalitarian_allocation(instance))
    # "{avi:['x', 'y', 'z'], beni:['w', 'y', 'z']}"

    # >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=4, item_capacities=2)
    # >>> stringify(almost_egalitarian_allocation(instance))
    # "{avi:['w', 'x', 'y', 'z'], beni:['w', 'x', 'y', 'z']}"
    """
    fractional_allocation = fractional_leximin_optimal_allocation(instance, **solver_options)
    logger.debug("\nfractional_allocation:\n%s", fractional_allocation)

    fractional_allocation_graph = consumption_graph(fractional_allocation)
    logger.debug("\nfractional_allocation_graph:\n%s", fractional_allocation_graph.edges.data())

    bundles = {agent: set() for agent in instance.agents}    # Each bundle is a set, since each agent can get at most one seat in each course


    # draw_bipartite_weighted_graph(fractional_allocation_graph, instance.agents)
    while fractional_allocation_graph.number_of_nodes()>0:
        # Look for an item leaf:
        found_item_leaf = False
        edges_to_remove = []
        for item in instance.items:
            if item in fractional_allocation_graph.nodes:
                item_neighbors = list(fractional_allocation_graph.neighbors(item))
                for agent in item_neighbors:
                    if fractional_allocation[agent][item] >= 0.99:
                        # Give an entire unit of the item to the neighbor agent
                        bundles[agent].add(item)
                        logger.info("\nItem %s is a leaf: give it to to agent %s", item, agent)
                        fractional_allocation[agent][item] = 0
                        fractional_allocation_graph.remove_edge(agent,item)
                        logger.debug("\nfractional_allocation_graph:\n%s", fractional_allocation_graph.edges.data())
                        found_item_leaf = True
        # fractional_allocation_graph.remove_edges_from(edges_to_remove)
        if found_item_leaf:
            # draw_bipartite_weighted_graph(fractional_allocation_graph, instance.agents)
            continue

        # No item is a leaf - look for an agent leaf:
        found_agent_leaf = False
        for agent in instance.agents:
            if fractional_allocation_graph.degree[agent]==1:
                # A leaf agent: disconnect him from his only neighbor (since it is a good)
                item = next(fractional_allocation_graph.neighbors(agent))
                logger.info("\nAgent %s is a leaf: disconnect from the only neighbor %s", agent, item)
                weight_for_redistribution = fractional_allocation[agent][item] # this weight should be redistributed to other neighbors
                # fractional_allocation_graph.remove_node(agent)
                fractional_allocation[agent][item] = 0
                fractional_allocation_graph.remove_edge(agent,item)
                assert (fractional_allocation_graph.degree[item]>=1)
                for neighbor_agent in fractional_allocation_graph.neighbors(item):
                    current_neighbor_weight = fractional_allocation[neighbor_agent][item] 
                    if weight_for_redistribution <= 1 - current_neighbor_weight:
                        fractional_allocation[neighbor_agent][item] += weight_for_redistribution
                        fractional_allocation_graph[neighbor_agent][item]['weight'] = fractional_allocation[neighbor_agent][item]
                        logger.info("\nAdd weight %g to (%s,%s)", weight_for_redistribution, neighbor_agent, item)
                        break
                    else:
                        fractional_allocation[neighbor_agent][item] = 1
                        weight_for_redistribution -= 1 - current_neighbor_weight
                        fractional_allocation_graph[neighbor_agent][item]['weight'] = fractional_allocation[neighbor_agent][item]
                        logger.info("\nSet to 1 the weight of (%s,%s)", neighbor_agent, item)
                logger.debug("\nfractional_allocation_graph:\n%s", fractional_allocation_graph.edges.data())
                found_agent_leaf = True
                break  # after removing one agent, proceed to remove leaf items
        if found_agent_leaf:
            # draw_bipartite_weighted_graph(fractional_allocation_graph, instance.agents)
            continue
        
        # If no leaf is found, break
        break
            
    return sorted_allocation(bundles)
    

    # return sorted_allocation(bundles)



if __name__ == "__main__":
    import doctest, sys
    print("\n",doctest.testmod(), "\n")

    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.DEBUG)

    from fairpy.courses.adaptors import divide_random_instance
    divide_random_instance(algorithm=almost_egalitarian_allocation, 
                           num_of_agents=10, num_of_items=3, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
                           item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
                           random_seed=1, normalize_utilities=True)
