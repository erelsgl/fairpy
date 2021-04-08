#!python3

"""
An implementation of the 2/3-fraction MMS approximation.

Reference:

    David Kurokawa, Ariel Procaccia, Junxing Wang (2018).
    ["Fair Enough: Guaranteeing Approximate Maximin Shares"](https://dl.acm.org/doi/abs/10.1145/3140756).
    Journal of the ACM.   *Algorithm 1.*

Programmer: Shai Aharon
Since:  2021-02
"""

import fairpy.indivisible.partitions as partitions
from fairpy.indivisible.agents import Agent, AdditiveAgent

from typing import *
Item = Any
Bundle = List[Item]

import networkx as nx
import logging

logger = logging.getLogger(__name__)


def calc_gamma(c: int) -> float:
    """
    Calculates the gamma factor (2*odd(n))/(3*odd(n)-1)
    odd(n) - means the closest odd number to n that is not lager then n.
    :param c: The number of agents.
    :return: The Gamma factor

    >>> calc_gamma(3)
    0.75
    >>> calc_gamma(30)
    0.6744186046511628
    >>> calc_gamma(int(1e10))
    0.6666666666888889
    """
    n_odd = c - (1 - c % 2)

    return (2 * n_odd) / (3 * n_odd - 1)


def divide_c_mms_partition(c: int, items: list, item_value_dict: dict) -> List[Bundle]:
    """
    Computed the MMS given the number of agents and the "value function"
    :param c: Number of agents
    :param items: A list of the values for each item
    :param item_value_dict: A dictionary holding each items value
    :return: The partitioning the holds the MMS

    >>> items_lst = ['a','b' ,'c', 'd', 'e', 'f']
    >>> items__val_dict = {'a': 5, 'b': 5, 'c': 3, 'd': 4, 'e': 5, 'f': 5}
    >>> mms_part = divide_c_mms_partition(3,items_lst,items__val_dict)
    >>> [sorted(x) for x in mms_part]
    [['b', 'c'], ['a', 'd'], ['e', 'f']]
    >>> mms_part = divide_c_mms_partition(4,items_lst,items__val_dict)
    >>> [sorted(x) for x in mms_part]
    [['a'], ['b'], ['c', 'd'], ['e', 'f']]
    """
    maxi_min = -1
    partition = []

    # Iterates over all possible partitions
    for tmp_partition in partitions.partitions_to_exactly_c(items, c):
        min_val = float('inf')
        for bund in tmp_partition:
            # Calculate the value of the bundle
            p_val = sum([item_value_dict[itm] for itm in bund])
            # Updates min value
            min_val = min(min_val, p_val)

        # Updates maximin value
        if maxi_min < min_val:
            partition = tmp_partition
            maxi_min = min_val

    return [set(x) for x in partition]


def create_envy_graph(agents: Dict[str, AdditiveAgent]) -> nx.DiGraph:
    """
    Creates an Envy Graph from the agents and their bundles.
    An Envy Graph, is a directed graph, which each node represents an agent. For every two nodes represeting
    agent u and v, there will be an edge from u to v if agent u belives agent v's bundle is worth more then his.
    @param agents: The list of agents
    @return: The Envy Graph
    >>> Alice = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 4, "e": 1}, name="Alice")
    >>> Alice.aq_items = ['a','b']
    >>> Bob = AdditiveAgent({"a": 1, "b": 1, "c": 2, "d": 1, "e": 5}, name="Bob")
    >>> Bob.aq_items = ['c', 'd']
    >>> Eve = AdditiveAgent({"a": 3, "b": 1, "c": 1, "d": 1, "e": 2}, name="Eve")
    >>> Eve.aq_items = ['e']
    >>> agents_dict = {x.name():x for x in [Alice,Bob,Eve]}
    >>> list(create_envy_graph(agents_dict).edges)
    [('Alice', 'Bob'), ('Bob', 'Eve'), ('Eve', 'Alice')]
    """

    di_graph = nx.DiGraph()
    for p in agents.values():
        di_graph.add_node(p.name())
        p_value = p.value(p.aq_items)
        for p2 in agents.values():
            if p is p2:
                continue
            p2_value = p.value(p2.aq_items)
            if p2_value > p_value:
                di_graph.add_edge(p.name(), p2.name())
                logger.info("\t{}->{},".format(p.name(), p2.name()))
    return di_graph


def get_gmm_item(agent: AdditiveAgent, items: List[str], gamma: float) -> Optional[str]:
    """
    Finds an item that is has a value of at least GMM for the given agent.
    @param agent: The Agent.
    @param items: The remaining items.
    @param gamma: The Gamma factor.
    @return: The items name as a string, if there is no item with a value of at least GMMS returns None

    >>> Alice = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1}, name="Alice")
    >>> Alice.mms = Alice.value_1_of_c_MMS(3)
    >>> items_lst = ['a', 'b', 'c', 'd', 'e', 'f']
    >>> gam = 0.75
    >>> item = get_gmm_item(Alice,items_lst,gam)
    >>> item is None
    True
    >>> Alice = AdditiveAgent({"a": .1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1}, name="Alice")
    >>> Alice.mms = Alice.value_1_of_c_MMS(3)
    >>> items_lst = ['a', 'b', 'c', 'd', 'e', 'f']
    >>> gam = 0.75
    >>> get_gmm_item(Alice,items_lst,gam)
    'b'
    """
    gmm_items = [k for k in items if
                 agent.map_good_to_value[k] >= (agent.mms * gamma)]
    if gmm_items:
        return gmm_items[0]
    return None


def handle_cycles(envy_graph: nx.DiGraph, agents_dict: Dict[str, AdditiveAgent]) -> bool:
    """
    Handles the cycles in the Envy Graph, replaces the bundles 'down-the stream'.
    @param envy_graph: The Envy-Graph
    @param agents_dict: The Agents in the Graph
    @return: True if there was a cycle, o.w. False.

    >>> Alice = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 4, "e": 1}, name="Alice")
    >>> Alice.aq_items = ['a','b']
    >>> Bob = AdditiveAgent({"a": 1, "b": 1, "c": 2, "d": 1, "e": 5}, name="Bob")
    >>> Bob.aq_items = ['c', 'd']
    >>> Eve = AdditiveAgent({"a": 3, "b": 1, "c": 1, "d": 1, "e": 2}, name="Eve")
    >>> Eve.aq_items = ['e']
    >>> agents_dict = {x.name():x for x in [Alice,Bob,Eve]}
    >>> envy_graph = create_envy_graph(agents_dict)
    >>> handle_cycles(envy_graph, agents_dict)
    True
    >>> [(x.name(),x.aq_items) for x in agents_dict.values()]
    [('Alice', ['c', 'd']), ('Bob', ['e']), ('Eve', ['a', 'b'])]
    """
    # Looking for Envy-cycles
    try:
        cycle = nx.find_cycle(envy_graph, orientation="original")
        for edge in cycle[:-1]:
            to_p, from_p = edge[0], edge[1]
            agents_dict[to_p].aq_items, agents_dict[from_p].aq_items = [agents_dict[from_p].aq_items,
                                                                        agents_dict[to_p].aq_items]
        logger.info("\tItems where exchanged in cycle {}".format('<-'.join([x[0] for x in cycle + cycle[:1]])))

        return True

    except nx.NetworkXNoCycle:
        logger.info("\tNo envy-cycles")
        return False


def hand_item_to_non_envy(envy_graph: nx.DiGraph, agents_dict: Dict[str, AdditiveAgent],
                          all_agents: List[AdditiveAgent], items_remaining: List[str], allocations: List[List[Any]]) -> None:
    """
    Finds an agent that no-one is envy of, and allocates an item to him.
    @param envy_graph: The Envy-Graph
    @param agents_dict: The agents in the Graph
    @param all_agents: A list of the agents
    @param items_remaining: A list of all the items that have not been allocated
    @param allocations: The allocation of items

    >>> Alice = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 4, "e": 1}, name="Alice")
    >>> Alice.aq_items = ['a']
    >>> Bob = AdditiveAgent({"a": 1, "b": 1, "c": 2, "d": 1, "e": 5}, name="Bob")
    >>> Bob.aq_items = ['c']
    >>> Eve = AdditiveAgent({"a": 3, "b": 1, "c": 1, "d": 1, "e": 2}, name="Eve")
    >>> Eve.aq_items = ['b']
    >>> agents_dict = {x.name():x for x in [Alice,Bob,Eve]}
    >>> envy_graph = create_envy_graph(agents_dict)
    >>> items_remaining = list('de')
    >>> alloc = [None,None,None]
    >>> hand_item_to_non_envy(envy_graph,agents_dict,[Alice,Bob,Eve],items_remaining,alloc)
    >>> sorted(list(alloc[1]))
    ['c', 'e']
    """
    rev_di_graph = envy_graph.reverse()
    for n in rev_di_graph.nodes():
        if len(rev_di_graph.edges(n)) == 0:
            pop_item = items_remaining.pop()
            agnt = agents_dict[n]
            agnt.aq_items.append(pop_item)
            allocations[all_agents.index(agnt)] = set(agnt.aq_items)
            logger.info("\tAgent {} received item {}".format(agnt.name(), pop_item))
            return


def get_highest_value(agent: AdditiveAgent, items_list: List[str]) -> (float, Set[str]):
    """
    Finds the two highest valued items for the agent that have not been allocated and returns the combined value.
    @param agent: The agent.
    @param items_list: The list of items not been allocated
    @return: The bundle value

    >>> Alice = AdditiveAgent({"a": 3, "b": 2, "c": 3, "d": 4, "e": 1, "f": 1}, name="Alice")
    >>> Alice.aq_items = ['a', 'd']
    >>> v,bndl = get_highest_value(Alice,items_list=list('bcef'))
    >>> v,sorted(bndl)
    (9, ['b', 'c', 'd'])
    """
    items_sorted_by_agent = sorted([x for x in agent.desired_items if x[0] in items_list],
                                   key=lambda x: agent.map_good_to_value[x], reverse=True)
    bundle_items = set([x[0] for x in items_sorted_by_agent[:2]] + [agent.aq_items[1]])
    return agent.value(bundle_items), bundle_items


def cycle_allocation(agents_dict: Dict[str,Agent], item_list: List[Item], reverse: bool = False) -> None:
    """
    Allocated each agent with his highest item that has not been allocated.
    @param agents_dict: Agents
    @param item_list: Non allocated items
    @param reverse: If False iterates over the agents in alphabetical order, O.W in reverse order.

    >>> Alice = AdditiveAgent({"a": 9, "b": 8, "c": 7, "d": 11, "e": 3, "f": 6, }, name="Alice")
    >>> Alice.aq_items = []
    >>> Bob = AdditiveAgent({"a":   9, "b": 8, "c": 7, "d": 11, "e": 3, "f": 6, }, name="Bob")
    >>> Bob.aq_items = []
    >>> Eve = AdditiveAgent({"a":   9, "b": 8, "c": 7, "d": 11, "e": 3, "f": 6, }, name="Eve")
    >>> Eve.aq_items = []
    >>> agents_dict = {x.name():x for x in [Alice,Bob,Eve]}
    >>> items_remaining = list('abcdef')
    >>> cycle_allocation(agents_dict,items_remaining,False)
    >>> [(x.name(),sorted(x.aq_items)) for x in agents_dict.values()]
    [('Alice', ['d']), ('Bob', ['a']), ('Eve', ['b'])]
    >>> cycle_allocation(agents_dict,items_remaining,True)
    >>> [(x.name(),sorted(x.aq_items)) for x in agents_dict.values()]
    [('Alice', ['d', 'e']), ('Bob', ['a', 'f']), ('Eve', ['b', 'c'])]
    """
    logger.info('\tItems remaining: ' + ','.join(item_list))
    for k, p in sorted(agents_dict.items(), reverse=reverse):
        max_item = max([x for x in p.desired_items if x[0] in item_list], key=lambda x: p.map_good_to_value[x])
        item_list.remove(max_item)
        p.aq_items.append(max_item)
        logger.info("\tAgent {} took item {} Value: {}".format(p.name(), max_item, p.map_good_to_value[max_item]))



if __name__ == "__main__":
    # import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
