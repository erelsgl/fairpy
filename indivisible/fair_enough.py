"""
Fair Enough: Guaranteeing Approximate Maximin Shares

Authors: David Kurokawa, Ariel D. Procaccia, and Junxing Wang
See https://dl.acm.org/doi/10.1145/3140756

@article{10.1145/3140756,
    author = {Kurokawa, David and Procaccia, Ariel D. and Wang, Junxing},
    title = {Fair Enough: Guaranteeing Approximate Maximin Shares},
    year = {2018},
    issue_date = {March 2018},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    volume = {65},
    number = {2},
    issn = {0004-5411},
    url = {https://doi.org/10.1145/3140756},
    doi = {10.1145/3140756},
    abstract = {We consider the problem of fairly allocating indivisible goods, focusing on a recently introduced
    notion of fairness called maximin share guarantee: each player’s value for his allocation should be at least as
    high as what he can guarantee by dividing the items into as many bundles as there are players and receiving his
    least desirable bundle. Assuming additive valuation functions, we show that such allocations may not exist, but
    allocations guaranteeing each player 2/3 of the above value always exist. These theoretical results have direct
    practical implications.},
    journal = {J. ACM},
    month = feb,
    articleno = {8},
    numpages = {27},
    keywords = {Computational fair division}
}

Programmer: Shai Aharon
Since:  2021-02
"""

from fairpy.indivisible.agents import *
from fairpy.indivisible.allocations import *
import fairpy.indivisible.partitions as partitions

from itertools import combinations_with_replacement
import networkx as nx
import numpy as np
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
    >>> calc_gamma(1e10)
    0.6666666666888889
    """
    n_odd = c - (1 - c % 2)

    return (2 * n_odd) / (3 * n_odd - 1)


def divide_c_MMS_partition(c: int, items: list, item_value_dict: dict) -> List[Bundle]:
    """
    Computed the MMS given the number of agents and the "value function"
    :param c: Number of agents
    :param items: A list of the values for each item
    :return: The partitioning the holds the MMS

    >>> mms_part = divide_c_MMS_partition(3,['a', 'c', 'd', 'e', 'f'],{'a': 5, 'b': 5, 'c': 3, 'd': 4, 'e': 5, 'f': 5})
    >>> [sorted(x) for x in mms_part]
    [['a'], ['c', 'd'], ['e', 'f']]
    >>> mms_part = divide_c_MMS_partition(4,['a', 'c', 'd', 'e', 'f'],{'a': 5, 'b': 5, 'c': 3, 'd': 4, 'e': 5, 'f': 5})
    >>> [sorted(x) for x in mms_part]
    [['a'], ['c', 'd'], ['e'], ['f']]
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


def createEnvyGraph(agents: Dict[str, AdditiveAgent]) -> nx.DiGraph:
    """
    Creates an Envy Graph from the agents and their bundles.
    An Envy Graph, is a directed graph, which each node represents an agent. For every two nodes represeting
    agent u and v, there will be an edge from u to v if agent u belives agent v's bundle is worth more then his.
    @param agents: The list of agents
    @return: The Envy Graph
    >>> Alice = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 4, "h": 5, "i": 3, "j": 3, "k": 3, "l": 1}, name="Alice")
    >>> Alice.aq_items = ['h','a']
    >>> Bob = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 3, "h": 4, "i": 2, "j": 2, "k": 2, "l": 1}, name="Bob")
    >>> Bob.aq_items = ['g', 'k']
    >>> Eve = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 4, "h": 4, "i": 2, "j": 3, "k": 2, "l": 1}, name="Eve")
    >>> Eve.aq_items = ['j', 'i']
    >>> agents = {x.name():x for x in [Alice,Bob,Eve]}
    >>> list(createEnvyGraph(agents).edges)
    [('Alice', 'Bob'), ('Eve', 'Bob')]
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


def getGmmItem(agent: AdditiveAgent, items: List[str], gamma: float) -> str:
    """
    Finds an item that is has a value of at least GMM for the given agent.
    @param agent: The Agent.
    @param items: The remaining items.
    @param gamma: The Gamma factor.
    @return: The items name as a string, if there is no item with a value of at least GMMS returns None

    >>> Alice = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1}, name="Alice")
    >>> Alice.mms = Alice.value_1_of_c_MMS(3)
    >>> items = ['a', 'b', 'c', 'd', 'e', 'f']
    >>> gamma = 0.75
    >>> item = getGmmItem(Alice,items,gamma)
    >>> item is None
    True
    >>> Alice = AdditiveAgent({"a": .1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1}, name="Alice")
    >>> Alice.mms = Alice.value_1_of_c_MMS(3)
    >>> items = ['a', 'b', 'c', 'd', 'e', 'f']
    >>> gamma = 0.75
    >>> getGmmItem(Alice,items,gamma)
    'b'
    """
    gmm_items = [k for k in items if
                 agent.map_good_to_value[k] >= (agent.mms * gamma)]
    if gmm_items:
        return gmm_items[0]
    return None


def handleCycles(envy_graph: nx.DiGraph, agents_dict: Dict[str, AdditiveAgent]) -> bool:
    """
    Handles the cycles in the Envy Graph, replaces the bundles 'down-the stream'.
    @param envy_graph: The Envy-Graph
    @param agents_dict: The Agents in the Graph
    @return: True if there was a cycle, o.w. False.

    >>> Alice = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 4, "h": 5, "i": 3, "j": 3, "k": 3, "l": 1}, name="Alice")
    >>> Alice.aq_items = ['h', 'd']
    >>> Bob = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 3, "h": 8, "i": 2, "j": 2, "k": 2, "l": 1}, name="Bob")
    >>> Bob.aq_items =['g', 'k']
    >>> Eve = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 4, "h": 4, "i": 2, "j": 3, "k": 2, "l": 1}, name="Eve")
    >>> Eve.aq_items = ['j', 'i']
    >>> agents_dict = {x.name():x for x in [Alice,Bob,Eve]}
    >>> envy_graph = createEnvyGraph(agents_dict)
    >>> handleCycles(envy_graph, agents_dict)
    True
    >>> [x.aq_items for x in agents_dict.values()]
    [['g', 'k'], ['h', 'd'], ['j', 'i']]
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


def handItemToLoser(envy_graph: nx.DiGraph, agents_dict: Dict[str, AdditiveAgent],
                    all_agents: List[AdditiveAgent], items_remaining: List[str], allocation: Allocation) -> None:
    """
    Finds an agent that no-one is envy of, and allocates an item to him.
    @param envy_graph: The Envy-Graph
    @param agents_dict: The agents in the Graph
    @param all_agents: A list of the agents
    @param items_remaining: A list of all the items that have not been allocated
    @param allocation: The allocation of items

    >>> Alice = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 4, "h": 5, "i": 3, "j": 3, "k": 3, "l": 1}, name="Alice")
    >>> Alice.aq_items = ['h', 'd']
    >>> Bob = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 3, "h": 3, "i": 2, "j": 2, "k": 2, "l": 1}, name="Bob")
    >>> Bob.aq_items =['g', 'k']
    >>> Eve = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 4, "h": 4, "i": 2, "j": 3, "k": 2, "l": 1}, name="Eve")
    >>> Eve.aq_items = ['j', 'i']
    >>> agents_dict = {x.name():x for x in [Alice,Bob,Eve]}
    >>> envy_graph = createEnvyGraph(agents_dict)
    >>> items_remaining = ['d', 'b', 'f', 'k', 'l', 'j', 'i', 'h', 'a', 'e', 'c', 'g']
    >>> alloc = Allocation([Alice,Bob,Eve])
    >>> handItemToLoser(envy_graph,agents_dict,[Alice,Bob,Eve],items_remaining,alloc)
    >>> sorted(list(alloc.get_bundle(0)))
    ['d', 'g', 'h']
    """
    rev_di_graph = envy_graph.reverse()
    for n in rev_di_graph.nodes():
        if len(rev_di_graph.edges(n)) == 0:
            pop_item = items_remaining.pop()
            agnt = agents_dict[n]
            agnt.aq_items.append(pop_item)
            allocation.set_bundle(all_agents.index(agnt), set(agnt.aq_items))

            logger.info("\tAgent {} received item {}".format(agnt.name(), pop_item))
            return


def getHighestValue(agent: AdditiveAgent, items_list: List[str]) -> (float, Set[str]):
    """
    Finds the two highest valued items for the agent that have not been allocated and returns the combined value.
    @param agent: The agent.
    @param items_list: The list of items not been allocated
    @return: The bundle value

    >>> Alice = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 4, "h": 5, "i": 3, "j": 3, "k": 3, "l": 1}, name="Alice")
    >>> Alice.aq_items = ['h', 'd']
    >>> v,bndl = getHighestValue(Alice,items_list=list('abcdefghijkl'))
    >>> v,sorted(bndl)
    (10, ['d', 'g', 'h'])
    """
    items_sorted_by_agent = sorted([x for x in agent.desired_items if x[0] in items_list],
                                   key=lambda x: agent.map_good_to_value[x], reverse=True)
    bundle_items = set([x[0] for x in items_sorted_by_agent[:2]] + [agent.aq_items[1]])
    return agent.value(bundle_items), bundle_items


def cycleAllocation(agents_dict: Dict[str, Allocation], item_list: List[str], reverse: bool = False) -> None:
    """
    Allocated each agent with his highest item that has not been allocated.
    @param agents_dict: Agents
    @param item_list: Non allocated items
    @param reverse: If False iterates over the agents in alphabetical order, O.W in reverse order.

    >>> Alice = AdditiveAgent({"a": 9, "b": 8, "c": 7, "d": 9, "e": 3, "f": 6, }, name="Alice")
    >>> Alice.aq_items = []
    >>> Bob = AdditiveAgent({"a":   9, "b": 8, "c": 7, "d": 9, "e": 3, "f": 6, }, name="Bob")
    >>> Bob.aq_items = []
    >>> Eve = AdditiveAgent({"a":   9, "b": 8, "c": 7, "d": 9, "e": 3, "f": 6, }, name="Eve")
    >>> Eve.aq_items = []
    >>> agents_dict = {x.name():x for x in [Alice,Bob,Eve]}
    >>> items_remaining = list('abcdef')
    >>> cycleAllocation(agents_dict,items_remaining,False)
    >>> [(x.name(),sorted(x.aq_items)) for x in agents_dict.values()]
    [('Alice', ['a']), ('Bob', ['d']), ('Eve', ['b'])]
    >>> cycleAllocation(agents_dict,items_remaining,True)
    >>> [(x.name(),sorted(x.aq_items)) for x in agents_dict.values()]
    [('Alice', ['a', 'e']), ('Bob', ['d', 'f']), ('Eve', ['b', 'c'])]
    """
    logger.info('\tItems remaining: ' + ','.join(item_list))
    for k, p in sorted(agents_dict.items(), reverse=reverse):
        max_item = max([x for x in p.desired_items if x[0] in item_list], key=lambda x: p.map_good_to_value[x])
        item_list.remove(max_item)
        p.aq_items.append(max_item)
        logger.info("\tAgent {} took item {} Value: {}".format(p.name(), max_item, p.map_good_to_value[max_item]))


def fair_enough(agents: List[AdditiveAgent], items: Bundle) -> Allocation:
    """
    Allocates the given items to the given agents using the 'Fair Enough' algorithm which
    garantees \gamma \cdot MaxiMin Share for each agent.

    :param agents: The agents who participate in the allocation.
    :param items: The items which are being allocated.
    :return: An allocation for each of the agents.

    Notes:
        The number of agents should be at least 3.
        There should be no more then 3n+4 items, where n is the number of agents.

    >>> Alice = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d":1,"e":1,"f":1}, name="Alice")
    >>> Bob = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d":1,"e":1,"f":1}, name="Bob")
    >>> Eve = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d":1,"e":1,"f":1}, name="Eve")
    >>> agents = [Alice,Bob,Eve]
    >>> allocation = fair_enough(agents,"abcdef")
    >>> {agents[i].name():agents[i].value(allocation.get_bundle(i)) for i,_ in enumerate(agents)}
    {'Alice': 2, 'Bob': 2, 'Eve': 2}
    >>> gamma = calc_gamma(3)
    >>> gamma
    0.75
    >>> Alice.is_1_of_c_MMS(allocation.get_bundle(0),3, gamma)
    True
    >>> Bob.is_1_of_c_MMS(allocation.get_bundle(1),3, gamma)
    True
    >>> Eve.is_1_of_c_MMS(allocation.get_bundle(1),3, gamma)
    True
    """

    agents_dict = {agn.name(): agn for agn in agents}
    allocation = Allocation(agents)
    gamma = calc_gamma(len(agents))
    logger.info("The Gamma is:{}".format(gamma))

    # Algorithm
    # Compute each agents MMS
    logger.info("Computing each agents MMS")
    for agn_name, agn_v in agents_dict.items():
        agn_v.mms = agn_v.value_1_of_c_MMS(len(agents_dict))
        logger.info("\t{}: MMS: {}\tGMMS: {:.3f}".format(agn_v.name(), agn_v.mms, agn_v.mms * gamma))

    logger.info("Stage 1")
    agent_eliminated = True
    items_remaining = list(items)
    while agent_eliminated:
        agent_eliminated = False
        for agn_name, agn_v in agents_dict.items():
            gmms_item = getGmmItem(agn_v, items_remaining, gamma)
            if gmms_item:
                agent_eliminated = True
                logger.info("\tAgent {} thinks item '{}' is worth at least his G-MMS".format(agn_name, gmms_item))

                agnt_idx = agents.index(agn_v)
                items_remaining.remove(gmms_item)
                allocation.set_bundle(agnt_idx, set(gmms_item))
                agents_dict.pop(agn_name)
                break

    logger.info("Stage 2")
    if len(agents_dict) == 2:
        p1, p2 = agents_dict.values()
        logger.info("\tAgents {} split the remaining items into 2-MMS groups".format(p1.name()))
        part_2 = divide_c_MMS_partition(2, items_remaining, p2.map_good_to_value)
        val_1, val_2 = p2.value(part_2[0]), p2.value(part_2[1])

        logger.info("\tGroup I: " + ','.join([x[0] for x in part_2[0]]))
        logger.info("\tValue: {}-{:.3f}\t{}-{:.3f}".format(p1.name(), p1.value(part_2[0]), p2.name(), val_1))
        logger.info("\tGroup II: " + ','.join([x[0] for x in part_2[1]]))
        logger.info("\tValue: {}-{:.3f}\t{}-{:.3f}".format(p1.name(), p1.value(part_2[1]), p2.name(), val_2))

        k1, k2 = 0, 1
        itm_grp_str = "FIRST"
        if val_1 < val_2:
            k1, k2 = 1, 0
            itm_grp_str = "SECOND"

        logger.info("\tAgent {} will take the {} group".format(p2.name(), itm_grp_str))
        for p, k in zip([p1, p2], [k1, k2]):
            agnt_idx = agents.index(p)
            allocation.set_bundle(agnt_idx, set(part_2[k]))

        return allocation
    logger.info("\tThere are more then 2 agents left, Stage 2 is skipped")

    # Stage 3-5
    has_eliminate = True
    while has_eliminate and items_remaining and agents_dict:
        has_eliminate = False
        tmp_items_list = list(items_remaining)
        # Cleaning the
        for ag in agents_dict.values():
            ag.aq_items = []
        logger.info("Stage 3")
        cycleAllocation(agents_dict, tmp_items_list, reverse=False)
        logger.info("Stage 4")
        cycleAllocation(agents_dict, tmp_items_list, reverse=True)

        logger.info("Stage 5")
        if tmp_items_list:
            for k, p in sorted(agents_dict.items()):
                potential_value, bundle_items = getHighestValue(p, tmp_items_list)

                if potential_value >= gamma * p.mms:
                    logger.info("\tAgent {} took {} with the value of {:.3f}".format(p.name(), ','.join(bundle_items),
                                                                                     potential_value))
                    has_eliminate = True
                    p.aq_items = [p.aq_items[1]]
                    [items_remaining.remove(p_obj[0]) for p_obj in bundle_items]

                    p.aq_items += bundle_items
                    allocation.set_bundle(agents.index(p), set(p.aq_items))
                    agents_dict.pop(p.name())
                    break
        else:
            logger.info("No Agent can reach his GMMS")
            items_remaining = tmp_items_list
            for k, v in agents_dict.items():
                allocation.set_bundle(agents.index(v), set(v.aq_items))

    if len(agents_dict) == 0 or len(items_remaining) == 0:
        logger.info("All agents have reached their G-MMS")
        return allocation

    # Stage 6-7
    logger.info("Stage 6-7")
    iter_count = 0
    while items_remaining:
        logger.info("Iteration: {}".format(iter_count))
        iter_count += 1

        envy_graph = createEnvyGraph(agents_dict)
        had_cycle = handleCycles(envy_graph, agents_dict)
        if not had_cycle:
            handItemToLoser(envy_graph, agents_dict, agents, items_remaining, allocation)

    return allocation


if __name__ == "__main__":
    import sys

    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)

    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

    # Alice = AdditiveAgent(
    #     {"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1, "i": 1, "j": 1, "k": 1, "l": 1}, name="Alice")
    # Bob = AdditiveAgent(
    #     {"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1, "i": 1, "j": 1, "k": 1, "l": 1}, name="Bob")
    # Eve = AdditiveAgent(
    #     {"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1, "i": 1, "j": 1, "k": 1, "l": 1}, name="Eve")
    # allocation = fair_enough([Alice, Bob, Eve], set("abcdefghikjl"))
    # print(allocation)
