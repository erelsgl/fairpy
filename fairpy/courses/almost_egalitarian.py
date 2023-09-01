"""
Implement an "almost-egalitarian" course allocation,
by rounding a linear program.

Programmer: Erel Segal-Halevi.
Since: 2023-07
"""

from fairpy.courses.instance    import Instance
from fairpy.courses.allocation_utils import AllocationBuilder
from fairpy.courses.iterated_maximum_matching import iterated_maximum_matching
from fairpy.courses.fractional_egalitarian import fractional_egalitarian_utilitarian_allocation
from fairpy.courses.explanations import *

import cvxpy, numpy as np, networkx
from cvxpy_leximin import Problem, Leximin
from fairpy.solve import solve
import matplotlib.pyplot as plt # for plotting the consumption graph (for debugging)


import logging
logger = logging.getLogger(__name__)

MIN_EDGE_FRACTION=0.01
def almost_egalitarian_allocation(alloc: AllocationBuilder, surplus_donation:bool=False, explanation_logger:ExplanationLogger=ExplanationLogger(), **solver_options):
    """
    Finds an almost-egalitarian allocation.
    :param alloc: an allocation builder, which tracks the allocation and the remaining capacity for items and agents. of the fair course allocation problem. 
    :param surplus_donation: if True, agents who gain utility from previously-removed edges will donate some of their edges to others.

    >>> from fairpy.courses.adaptors import divide

    >>> from dicttools import stringify

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=1, item_capacities=1)
    >>> stringify(divide(almost_egalitarian_allocation, instance=instance))
    "{avi:['x'], beni:['w']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=2, item_capacities=1)
    >>> stringify(divide(almost_egalitarian_allocation, instance=instance))
    "{avi:['x', 'y'], beni:['w', 'z']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=3, item_capacities=2)
    >>> stringify(divide(almost_egalitarian_allocation, instance=instance))
    "{avi:['x', 'y', 'z'], beni:['w', 'y', 'z']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=4, item_capacities=2)
    >>> stringify(divide(almost_egalitarian_allocation, instance=instance))
    "{avi:['w', 'x', 'y', 'z'], beni:['w', 'x', 'y', 'z']}"
    """
    # fractional_allocation = fractional_leximin_optimal_allocation(alloc.remaining_instance(), **solver_options) # Too slow

    explanation_logger.info("\nAlgorithm Almost-Egalitarian starts.\n")

    fractional_allocation = fractional_egalitarian_utilitarian_allocation(alloc.remaining_instance(), **solver_options)
    explanation_logger.explain_fractional_allocation(fractional_allocation, alloc.instance)

    fractional_allocation_graph = consumption_graph(fractional_allocation, min_fraction=MIN_EDGE_FRACTION, agent_item_value=lambda agent,item:alloc.remaining_agent_item_value[agent][item])
    explanation_logger.debug("\nfractional_allocation_graph:\n%s", fractional_allocation_graph.edges.data())

    explanation_logger.info("\nStarting to round the fractional allocation.\n")


    def agent_item_tuple(edge):
        if edge[0] in alloc.remaining_agents():
            return (edge[0],edge[1])
        else:
            return (edge[1],edge[0])
        
    agent_surplus = {agent: 0 for agent in alloc.remaining_agents()}

    def add_surplus (agent, value_to_add):
        agent_surplus[agent] += value_to_add
        items_to_remove = []
        for neighbor_item in fractional_allocation_graph.neighbors(agent):
            current_neighbor_weight = fractional_allocation_graph[agent][neighbor_item]['weight']
            current_neighbor_value  = current_neighbor_weight * alloc.remaining_agent_item_value[agent][neighbor_item]
            if current_neighbor_value <= agent_surplus[agent]:
                explanation_logger.info("  You have a surplus of %g, so you donate your share of %g%% in course %s (value %g)", agent_surplus[agent], np.round(100*current_neighbor_weight), neighbor_item, current_neighbor_value, agents=agent)
                items_to_remove.append(neighbor_item)
                agent_surplus[agent] -= current_neighbor_value
        for neighbor_item in items_to_remove:
            remove_edge_from_graph(agent, neighbor_item)


    def remove_edge_from_graph(agent,item):
        """
        Remove the edge (agent,item) from the graph, and redistribute its weight among the neighboring agents of item.
        """
        weight_for_redistribution = fractional_allocation[agent][item] # this weight should be redistributed to other neighbors of the item
        fractional_allocation[agent][item] = 0
        if fractional_allocation_graph.has_edge(agent,item):
            fractional_allocation_graph.remove_edge(agent,item)
        surplus_to_add = {}
        for neighbor_agent in fractional_allocation_graph.neighbors(item):
            current_neighbor_weight = fractional_allocation_graph[neighbor_agent][item]['weight']

            weight_to_add = min(weight_for_redistribution, 1-current_neighbor_weight)
            fractional_allocation[neighbor_agent][item] = fractional_allocation_graph[neighbor_agent][item]['weight'] = current_neighbor_weight + weight_to_add
            weight_for_redistribution -= weight_to_add

            value_to_add = weight_to_add*alloc.remaining_agent_item_value[agent][item]
            explanation_logger.info("  Edge (%s,%s) is removed, so you receive additional %g%% of course %s (value %g).", agent,item,np.round(100*weight_to_add),item, value_to_add, agents=neighbor_agent)
            surplus_to_add[neighbor_agent] = value_to_add
            if weight_for_redistribution<=0:
                break
        if surplus_donation:
            for neighbor_agent,value_to_add in surplus_to_add.items():
                add_surplus(neighbor_agent, value_to_add)


    def remove_agent_from_graph(agent):
        """
        Remove the agent from the graph, and redistribute its belongings among the neighboring agents of these items.
        """
        neighbors = list(fractional_allocation_graph.neighbors(agent))
        for item in neighbors:
            remove_edge_from_graph(agent,item)

    # draw_bipartite_weighted_graph(fractional_allocation_graph, alloc.remaining_agents())
    while fractional_allocation_graph.number_of_edges()>0:
        # Look for an item leaf:
        # edges_with_fraction_near_1 = [(u,v) for u,v in fractional_allocation_graph.edges if fractional_allocation_graph[u][v]['weight'] >= 1-2*MIN_EDGE_FRACTION]
        # max_value_edge = max(edges_with_fraction_near_1, key=lambda u,v: fractional_allocation_graph[u][v]['value'])

        found_item_leaf = False
        for item in list(alloc.remaining_items()):
            if item in fractional_allocation_graph.nodes:
                item_neighbors = list(fractional_allocation_graph.neighbors(item))
                for agent in item_neighbors:
                    if fractional_allocation[agent][item] >= 1-2*MIN_EDGE_FRACTION:
                        # Give an entire unit of the item to the neighbor agent
                        alloc.give(agent, item)
                        explanation_logger.info("Course %s is a leaf node, and you are its only neighbor, so you get all of it to yourself.", item, agents=agent)
                        fractional_allocation[agent][item] = 0
                        fractional_allocation_graph.remove_edge(agent,item)
                        if not agent in alloc.remaining_agent_capacities:
                            explanation_logger.info("You have received %s and you have no remaining capacity.", alloc.bundles[agent], agents=agent)
                            remove_agent_from_graph(agent)
                        explanation_logger.debug("\nfractional_allocation_graph:\n%s", fractional_allocation_graph.edges.data())
                        found_item_leaf = True
        if found_item_leaf:
            # draw_bipartite_weighted_graph(fractional_allocation_graph, alloc.remaining_agents())
            continue

        # No item is a leaf - look for an agent leaf:
        found_agent_leaf = False
        for agent in alloc.remaining_agents():
            if not agent in fractional_allocation_graph:
                continue
            if fractional_allocation_graph.degree[agent]==1:
                # A leaf agent: disconnect him from his only neighbor (since it is a good)
                item = next(fractional_allocation_graph.neighbors(agent))
                if fractional_allocation_graph.degree[item]>1:
                    explanation_logger.info("\nYou are a leaf node, so you lose your only neighbor %s", item, agents=agent)
                    remove_agent_from_graph(agent)
                else:
                    fractional_allocation[agent][item] = 0
                    fractional_allocation_graph.remove_edge(agent,item)
                    if agent not in alloc.remaining_agent_capacities:
                        logger.warn("Agent %s is the only one who could get item %s, but the agent has no remaining capacity!", agent, item)
                    elif item not in alloc.remaining_item_capacities:
                        logger.warn("Agent %s is the only one who could get item %s, but the item has no remaining capacity!", agent, item)
                    else:
                        alloc.give(agent, item)
                        explanation_logger.info("Both you and course %s are leaf nodes, so you get all of it to yourself.", item, agents=agent)

                explanation_logger.debug("\nfractional_allocation_graph:\n%s", fractional_allocation_graph.edges.data())
                found_agent_leaf = True
                break  # after removing one agent, proceed to remove leaf items
        if found_agent_leaf:
            # draw_bipartite_weighted_graph(fractional_allocation_graph, alloc.remaining_agents())
            continue

        # No leaf at all - remove an edge with a small weight:
        edge_with_min_weight = min(fractional_allocation_graph.edges(), key=lambda edge:fractional_allocation_graph[edge[0]][edge[1]]["weight"])
        min_weight = fractional_allocation_graph[edge_with_min_weight[0]][edge_with_min_weight[1]]["weight"]
        logger.warn("No leafs - removing edge %s with minimum weight %g", edge_with_min_weight, min_weight)
        explanation_logger.info("There are no leaf nodes, but the edge %s has minimum weight %g, so it is removed.", edge_with_min_weight, min_weight, agents=agent)
        remove_edge_from_graph(*agent_item_tuple(edge_with_min_weight))

    iterated_maximum_matching(alloc)  # Avoid waste
    return alloc.sorted()


def almost_egalitarian_without_donation(alloc:AllocationBuilder, **kwargs):
    return almost_egalitarian_allocation(alloc, surplus_donation=False, **kwargs)

def almost_egalitarian_with_donation(alloc:AllocationBuilder, **kwargs):
    return almost_egalitarian_allocation(alloc, surplus_donation=True, **kwargs)


almost_egalitarian_allocation.logger = logger


def consumption_graph(allocation:dict, min_fraction=0.01, agent_item_value=None)->networkx.Graph:
    """
    Generate the consumption graph of the given allocation.
    It is a bipartite graph between agents and items, where there is an edge if the agent consumes a positive amount of the item.
    """
    G = networkx.Graph()
    for agent,bundle in allocation.items():
        for item,fraction in bundle.items():
            if fraction>=min_fraction:
                value = None if agent_item_value is None else agent_item_value(agent,item)
                G.add_edge(agent,item, weight=np.round(fraction,2), value=value)
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
    # import doctest, sys
    # print("\n",doctest.testmod(), "\n")

    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.WARNING)

    from fairpy.courses.adaptors import divide_random_instance
    num_of_agents = 30
    num_of_items = 10

    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))

    console_explanation_logger = ConsoleExplanationLogger()
    files_explanation_logger = FilesExplanationLogger({
        f"s{i+1}": f"{dir_path}/logs/s{i+1}.log"
        for i in range(num_of_agents)
    }, mode='w', level=logging.INFO)
    string_explanation_logger = StringsExplanationLogger(f"s{i+1}" for i in range(num_of_agents))

    divide_random_instance(algorithm=almost_egalitarian_allocation, 
                           explanation_logger=files_explanation_logger,
                           num_of_agents=num_of_agents, num_of_items=num_of_items, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
                           item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
                           random_seed=1)
