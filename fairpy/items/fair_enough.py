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

from fairpy.allocations import Allocation

from fairpy.items.fair_enough_utils import *

import networkx as nx

import logging
logger = logging.getLogger(__name__)


def fair_enough(agents: List[AdditiveAgent], items: Bundle) -> Allocation:
    """
    Allocates the given items to the given agents using the 'Fair Enough' algorithm which
    garantees gamma * MaxiMin Share for each agent.

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
    >>> allocation = fair_enough(agents,set("abcdef"))
    >>> {agents[i].name():agents[i].value(allocation[i]) for i,_ in enumerate(agents)}
    {'Alice': 2, 'Bob': 2, 'Eve': 2}
    >>> Alice = AdditiveAgent({"a": .21, "b": 1, "c": 1, "d":1,"e":1,"f":1}, name="Alice")
    >>> Bob = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d":1,"e":1,"f":1}, name="Bob")
    >>> Eve = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d":1,"e":1,"f":1}, name="Eve")
    >>> agents = [Alice,Bob,Eve]
    >>> allocation = fair_enough(agents,set("abcdef"))
    >>> {agents[i].name():agents[i].value(allocation[i]) for i,_ in enumerate(agents)}
    {'Alice': 1, 'Bob': 2, 'Eve': 3}
    >>> Alice = AdditiveAgent({"a": 1, "b": 1, "c": 1, "d":1,"e":1,"f":1,"g":1}, name="Alice")
    >>> Bob = AdditiveAgent({"a":   1, "b": 1, "c": 1, "d":1,"e":1,"f":1,"g":1}, name="Bob")
    >>> Eve = AdditiveAgent({"a":   1, "b": 1, "c": 1, "d":1,"e":1,"f":1,"g":1}, name="Eve")
    >>> agents = [Alice,Bob,Eve]
    >>> allocation = fair_enough(agents,set("abcdefg"))
    >>> {agents[i].name():agents[i].value(allocation[i]) for i,_ in enumerate(agents)}
    {'Alice': 2, 'Bob': 2, 'Eve': 2}
    >>> Alice = AdditiveAgent({"a":1.1, "b":1,"c":1,"d":1,"e":1,"f":1,"g":3.1  ,"h":2.9,"i":2,"j":3,"k":3,"l":1},name="Alice")
    >>> Bob = AdditiveAgent({"a":  1, "b":1,"c":1,"d":1,"e":1,"f":1,"g":4.4,"h":4.1,"i":2.1,"j":2,"k":2,"l":1},name="Bob")
    >>> Eve = AdditiveAgent({"a":  1, "b":1,"c":1,"d":1,"e":1,"f":1,"g":4  ,"h":4,"i":2,"j":3.2,"k":2.2,"l":1},name="Eve")
    >>> agents = [Alice,Bob,Eve]
    >>> allocation = fair_enough(agents,set("abcdefghijkl"))
    >>> {agents[i].name():agents[i].value(allocation[i]) for i,_ in enumerate(agents)}
    {'Alice': 9.9, 'Bob': 9.5, 'Eve': 13.2}
    >>> gamma = calc_gamma(3)
    >>> Alice.is_1_of_c_MMS(allocation[0], 3, gamma)
    True
    >>> Bob.is_1_of_c_MMS(allocation[1], 3, gamma)
    True
    >>> Eve.is_1_of_c_MMS(allocation[1], 3, gamma)
    True
    """

    agents_dict = {agn.name(): agn for agn in agents}
    allocations = len(agents)*[None]
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
            gmms_item = get_gmm_item(agn_v, items_remaining, gamma)
            if gmms_item:
                agent_eliminated = True
                logger.info("\tAgent {} thinks item '{}' is worth at least his G-MMS".format(agn_name, gmms_item))

                agnt_idx = agents.index(agn_v)
                items_remaining.remove(gmms_item)
                allocations[agnt_idx] = set(gmms_item)
                agents_dict.pop(agn_name)
                break

    logger.info("Stage 2")
    if len(agents_dict) == 2:
        p1, p2 = agents_dict.values()
        logger.info("\tAgents {} split the remaining items into 2-MMS groups".format(p1.name()))
        mms_2_part = p1.partition_1_of_c_MMS(2, items_remaining)
        val_1, val_2 = p2.value(mms_2_part[0]), p2.value(mms_2_part[1])

        logger.info("\tGroup I: " + ','.join([x[0] for x in mms_2_part[0]]))
        logger.info("\tValue: {}-{:.3f}\t{}-{:.3f}".format(p1.name(), p1.value(mms_2_part[0]), p2.name(), val_1))
        logger.info("\tGroup II: " + ','.join([x[0] for x in mms_2_part[1]]))
        logger.info("\tValue: {}-{:.3f}\t{}-{:.3f}".format(p1.name(), p1.value(mms_2_part[1]), p2.name(), val_2))

        k1, k2 = 1, 0
        itm_grp_str = "FIRST"
        if val_1 < val_2:
            k1, k2 = 0, 1
            itm_grp_str = "SECOND"

        logger.info("\tAgent {} will take the {} group".format(p2.name(), itm_grp_str))
        for p, k in zip([p1, p2], [k1, k2]):
            agnt_idx = agents.index(p)
            allocations[agnt_idx] = set(mms_2_part[k])
        return Allocation(agents, allocations)

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
        cycle_allocation(agents_dict, tmp_items_list, reverse=False)
        logger.info("Stage 4")
        cycle_allocation(agents_dict, tmp_items_list, reverse=True)

        logger.info("Stage 5")
        if tmp_items_list:
            for k, p in sorted(agents_dict.items()):
                potential_value, bundle_items = get_highest_value(p, tmp_items_list)

                if potential_value >= gamma * p.mms:
                    logger.info("\tAgent {} took {} with the value of {:.3f}".format(p.name(), ','.join(bundle_items),
                                                                                     potential_value))
                    has_eliminate = True
                    p.aq_items = [p.aq_items[1]]
                    [items_remaining.remove(p_obj[0]) for p_obj in bundle_items]

                    p.aq_items += bundle_items
                    allocations[agents.index(p)] = set(p.aq_items)
                    agents_dict.pop(p.name())
                    break
        else:
            logger.info("No Agent can reach his GMMS")
            items_remaining = tmp_items_list
            for k, v in agents_dict.items():
                allocations[agents.index(v)] = set(v.aq_items)

    if len(agents_dict) == 0 or len(items_remaining) == 0:
        logger.info("All agents have reached their G-MMS")
        return Allocation(agents, allocations)

    items_remaining.sort()  # For testing purposes
    # Stage 6-7
    logger.info("Stage 6-7")
    iter_count = 0
    while items_remaining:
        logger.info("Iteration: {}".format(iter_count))
        iter_count += 1

        envy_graph = create_envy_graph(agents_dict)
        had_cycle = handle_cycles(envy_graph, agents_dict)
        if not had_cycle:
            hand_item_to_non_envy(envy_graph, agents_dict, agents, items_remaining, allocations)

    return Allocation(agents, allocations)



if __name__ == "__main__":
    # import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
