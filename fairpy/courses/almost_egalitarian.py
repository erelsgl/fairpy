"""
Implement an "almost-egalitarian" course allocation,
by rounding a linear program.

Programmer: Erel Segal-Halevi.
Since: 2023-07
"""

from fairpy.courses.instance import Instance
from fairpy.courses.allocation_utils import AllocationBuilder
from fairpy.courses.fractional_egalitarian import fractional_leximin_optimal_allocation, fractional_egalitarian_utilitarian_allocation

import cvxpy, numpy as np, networkx
from cvxpy_leximin import Problem, Leximin
from fairpy.solve import solve
import matplotlib.pyplot as plt # for plotting the consumption graph (for debugging)


import logging
logger = logging.getLogger(__name__)

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
    # fractional_allocation = fractional_leximin_optimal_allocation(instance, **solver_options) # Too slow
    fractional_allocation = fractional_egalitarian_utilitarian_allocation(instance, **solver_options)
    logger.debug("\nfractional_allocation:\n%s", fractional_allocation)

    fractional_allocation_graph = consumption_graph(fractional_allocation)
    logger.debug("\nfractional_allocation_graph:\n%s", fractional_allocation_graph.edges.data())

    def remove_edge_from_graph(agent,item):
        """
        Remove the edge (agent,item) from the graph, and redistribute its weight among the neighboring agents of item.
        """
        weight_for_redistribution = fractional_allocation[agent][item] # this weight should be redistributed to other neighbors of the item
        fractional_allocation[agent][item] = 0
        fractional_allocation_graph.remove_edge(agent,item)
        for neighbor_agent in fractional_allocation_graph.neighbors(item):
            current_neighbor_weight = fractional_allocation_graph[neighbor_agent][item]['weight']
            if weight_for_redistribution <= 1 - current_neighbor_weight:
                fractional_allocation[neighbor_agent][item] = fractional_allocation_graph[neighbor_agent][item]['weight'] = current_neighbor_weight + weight_for_redistribution
                logger.info("\nAdd weight %g to (%s,%s)", weight_for_redistribution, neighbor_agent, item)
                break
            else:
                fractional_allocation[neighbor_agent][item] = fractional_allocation_graph[neighbor_agent][item]['weight'] = 1
                weight_for_redistribution -= 1 - current_neighbor_weight
                logger.info("\nSet to 1 the weight of (%s,%s)", neighbor_agent, item)

    def remove_agent_from_graph(agent):
        neighbors = list(fractional_allocation_graph.neighbors(agent))
        for item in neighbors:
            remove_edge_from_graph(agent,item)

    alloc = AllocationBuilder(instance)

    # draw_bipartite_weighted_graph(fractional_allocation_graph, instance.agents)
    while fractional_allocation_graph.number_of_nodes()>0:
        # Look for an item leaf:
        found_item_leaf = False
        for item in instance.items:
            if item in fractional_allocation_graph.nodes:
                item_neighbors = list(fractional_allocation_graph.neighbors(item))
                for agent in item_neighbors:
                    if fractional_allocation[agent][item] >= 0.99:
                        # Give an entire unit of the item to the neighbor agent
                        alloc.give(agent, item)
                        logger.info("\nItem %s is a leaf: give it to to agent %s", item, agent)
                        fractional_allocation[agent][item] = 0
                        fractional_allocation_graph.remove_edge(agent,item)
                        if not agent in alloc.remaining_agent_capacities:
                            logger.info("\nAgent %s has received %s and has no remaining capacity: remove it", agent, alloc.bundles[agent])
                            remove_agent_from_graph(agent)
                        logger.debug("\nfractional_allocation_graph:\n%s", fractional_allocation_graph.edges.data())
                        found_item_leaf = True
        if found_item_leaf:
            # draw_bipartite_weighted_graph(fractional_allocation_graph, instance.agents)
            continue

        # No item is a leaf - look for an agent leaf:
        found_agent_leaf = False
        for agent in instance.agents:
            if not agent in fractional_allocation_graph:
                continue
            if fractional_allocation_graph.degree[agent]==1:
                # A leaf agent: disconnect him from his only neighbor (since it is a good)
                item = next(fractional_allocation_graph.neighbors(agent))
                logger.info("\nAgent %s is a leaf: disconnect from the only neighbor %s", agent, item)
                remove_agent_from_graph(agent)
                logger.debug("\nfractional_allocation_graph:\n%s", fractional_allocation_graph.edges.data())
                found_agent_leaf = True
                break  # after removing one agent, proceed to remove leaf items
        if found_agent_leaf:
            # draw_bipartite_weighted_graph(fractional_allocation_graph, instance.agents)
            continue

        # No leaf at all - remove an edge with a small weight:
        # for edge in fractional_allocation_graph.edges():


        # If no leaf is found, break
        break
    return alloc.sorted()


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



if __name__ == "__main__":
    import doctest, sys
    # print("\n",doctest.testmod(), "\n")

    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.DEBUG)

    from fairpy.courses.adaptors import divide_random_instance
    divide_random_instance(algorithm=almost_egalitarian_allocation, 
                           num_of_agents=10, num_of_items=3, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
                           item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
                           random_seed=1, normalize_utilities=True)
