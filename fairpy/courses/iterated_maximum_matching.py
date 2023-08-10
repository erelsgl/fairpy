#!python3

"""

The Iterated Maximum Matching algorithm for fair item allocation. Reference:

    Johannes Brustle, Jack Dippel, Vishnu V. Narayan, Mashbat Suzuki, Adrian Vetta (2019).
    ["One Dollar Each Eliminates Envy"](https://arxiv.org/abs/1912.02797).
    * Algorithm 1.

Programmer: Erel Segal-Halevi
Since : 2021-05
"""


from fairpy.courses.graph_utils import many_to_many_matching_using_network_flow
from fairpy.courses.instance    import Instance
from fairpy.courses.allocation_utils import AllocationBuilder

import logging
logger = logging.getLogger(__name__)
dummy_logger = logging.getLogger('dummy')


def iterated_maximum_matching(alloc:AllocationBuilder, adjust_utilities:bool=False, explanation_logger=dummy_logger):
    """
    Builds a allocation using Iterated Maximum Matching.
    :param alloc: an allocation builder, which tracks the allocation and the remaining capacity for items and agents. of the fair course allocation problem. 
    :param adjust_utilities: if True, the utilities of agents, who did not get their max-value item in the current iteration, will be adjusted to give them a higher chance in the next iteration.

    >>> from dicttools import stringify
    >>> from fairpy.courses.adaptors import divide

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=1, item_capacities=1)
    >>> map_agent_name_to_bundle = divide(iterated_maximum_matching,instance=instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x'], beni:['w']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=2, item_capacities=1)
    >>> map_agent_name_to_bundle = divide(iterated_maximum_matching,instance=instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x', 'y'], beni:['w', 'z']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=3, item_capacities=2)
    >>> map_agent_name_to_bundle = divide(iterated_maximum_matching,instance=instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x', 'y', 'z'], beni:['w', 'y', 'z']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=4, item_capacities=2)
    >>> map_agent_name_to_bundle = divide(iterated_maximum_matching,instance=instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['w', 'x', 'y', 'z'], beni:['w', 'x', 'y', 'z']}"

    ### item conflicts:
    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=4, item_capacities=2, item_conflicts={"x": ["w"], "w": ["x"]})
    >>> map_agent_name_to_bundle = divide(iterated_maximum_matching,instance=instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x', 'y', 'z'], beni:['w', 'y', 'z']}"
    """
    iteration = 1
    while len(alloc.remaining_item_capacities)>0 and len(alloc.remaining_agent_capacities)>0:
        logger.info("\nIteration %d", iteration)
        explanation_logger.info("\nIteration %d:", iteration)
        logger.info("  remaining_agent_capacities: %s", alloc.remaining_agent_capacities)
        logger.info("  remaining_item_capacities: %s", alloc.remaining_item_capacities)
        logger.debug("  remaining_agent_item_value: %s", alloc.remaining_agent_item_value)
        map_agent_to_bundle = many_to_many_matching_using_network_flow(
            items=alloc.remaining_items(), 
            item_capacity=alloc.remaining_item_capacities.__getitem__, 
            agents=alloc.remaining_agents(),
            agent_capacity=lambda _:1,
            agent_item_value=lambda agent,item: alloc.remaining_agent_item_value[agent][item])
        # logger.info("Matching: %s", dict(map_agent_to_bundle))

        agents_with_empty_bundles = [agent for agent,bundle in map_agent_to_bundle.items() if len(bundle)==0]
        for agent in agents_with_empty_bundles:
            logger.info("  Agent %s cannot be given any more items.", agent)
            explanation_logger.info("[%s]  All remaining courses are not acceptable to you.", agent)
            alloc.remove_agent(agent)
            del map_agent_to_bundle[agent]

        map_agent_to_item = {agent: bundle[0] for agent,bundle in map_agent_to_bundle.items()}

        logger.info("Matching: ")

        if adjust_utilities:
            map_agent_to_value = {
                agent: alloc.remaining_agent_item_value[agent][map_agent_to_item[agent]]
                for agent in map_agent_to_item.keys()
            }
            map_agent_to_max_possible_value = {
                agent: max([alloc.remaining_agent_item_value[agent][item] for item in alloc.remaining_items()])
                for agent in map_agent_to_item.keys()
            }
            for agent,item in map_agent_to_item.items():
                logger.info("  Agent %s gets item %s with value %g (max possible: %g).", agent, item, map_agent_to_value[agent], map_agent_to_max_possible_value[agent])
                explanation_logger.info("[%s]  You get course %s. Its value for you is %g. The maximum possible value you could get in this iteration is %g", agent, item, map_agent_to_value[agent], map_agent_to_max_possible_value[agent])
                alloc.give(agent,item)
            if alloc.remaining_items():
                for agent,item in map_agent_to_item.items():
                    next_best_item = max(alloc.remaining_items(), key=lambda item:alloc.remaining_agent_item_value[agent][item])
                    current_value_of_next_best_item = alloc.remaining_agent_item_value[agent][next_best_item]
                    utility_difference = map_agent_to_max_possible_value[agent] - map_agent_to_value[agent]
                    if utility_difference>0:
                        alloc.remaining_agent_item_value[agent][next_best_item] += utility_difference
                        explanation_logger.info("[%s]  As compensation, we added the difference %g to your next-best course, %s", agent, utility_difference, item)
                        logger.info("   Increasing value of agent %s to next-best item %s from %g to %g", agent, next_best_item, current_value_of_next_best_item, current_value_of_next_best_item+utility_difference)
                    else:
                        pass

        else:
            for agent,item in map_agent_to_item.items():
                logger.info("  Agent %s gets item %s.", agent, item)
                explanation_logger.info("[%s]  You get course %s", agent, item)
                alloc.give(agent,item)
        iteration += 1


def iterated_maximum_matching_adjusted(alloc:AllocationBuilder):
    return iterated_maximum_matching(alloc, adjust_utilities=True)

def iterated_maximum_matching_unadjusted(alloc:AllocationBuilder):
    return iterated_maximum_matching(alloc, adjust_utilities=False)


iterated_maximum_matching.logger = logger





if __name__ == "__main__":
    import doctest
    print("\n",doctest.testmod(), "\n")

    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.WARNING)

    explanation_logger = logging.getLogger("explanation")
    explanation_logger.addHandler(logging.StreamHandler())
    explanation_logger.setLevel(logging.INFO)

    from fairpy.courses.adaptors import divide_random_instance
    num_of_agents = 30
    num_of_items = 10

    print("\n\nIterated Maximum Matching without adjustments:")
    divide_random_instance(algorithm=iterated_maximum_matching, adjust_utilities=False,
                           num_of_agents=num_of_agents, num_of_items=num_of_items, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
                           item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
                           random_seed=1)

    print("\n\nIterated Maximum Matching with adjustments:")
    divide_random_instance(algorithm=iterated_maximum_matching, adjust_utilities=True, explanation_logger=explanation_logger,
                           num_of_agents=num_of_agents, num_of_items=num_of_items, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
                           item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
                           random_seed=1)
