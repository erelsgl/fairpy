#!python3

"""
An implementation of a PROPm allocation algorithm. Reference:

    Artem Baklanov, Pranav Garimidi, Vasilis Gkatzelis, and Daniel Schoepflin (2021).
    ["PROPm Allocations of Indivisible Goods to Multiple Agents"](https://arxiv.org/abs/2105.11348).

Programmer: Maksim Timokhin
Since:  2021-05
"""

import networkx as nx
import numpy as np
from fairpy import ValuationMatrix
from typing import List
import logging

logger = logging.getLogger(__name__)


###
### Main function
###


def propm_allocation(v: ValuationMatrix) -> List[List[int]]:
    """
    recursive function which takes valuations and returns a PROPm allocation
    as a list of bundles
    >>> import numpy as np

    >>> v = ValuationMatrix([
    ... [0.25, 0.25, 0.25, 0.25, 0, 0],
    ... [0.25, 0, 0.26, 0, 0.25, 0.24],
    ... [0.25, 0, 0.24, 0, 0.25, 0.26]
    ... ])
    >>> propm_allocation(v)
    [[2, 3], [1, 5], [4, 0]]

    >>> partial_matrix = v._v[np.ix_([0, 1, 2], [0, 2, 1, 3, 4, 5])]  # rows 0,1,2 and columns 0,2,1,3,4,5
    >>> propm_allocation(ValuationMatrix(partial_matrix))
    [[2, 3], [0, 1], [4, 5]]

    >>> v = ValuationMatrix([
    ... [0, 0, 0, 0, 0, 0],
    ... [1, 2, 3, 4, 5, 6],
    ... [10, 20, 30, 40, 50, 60]
    ... ])
    >>> propm_allocation(v)
    [[], [0, 1, 2, 3], [4, 5]]
    """
    if v.num_of_agents == 0 or v.num_of_objects == 0:
        return []

    logger.info("Looking for PROPm allocation for %d agents and %d items", v.num_of_agents, v.num_of_objects)
    logger.info("Solving a problem defined by valuation matrix:\n %s", v)

    for agent in v.agents():
        if np.allclose(v[agent], 0.0):  # irrelevant agent - values everything at 0
            allocation = propm_allocation(v.without_agent(agent))
            allocation.insert(agent, [])
            return allocation

    total_value = v.normalize()

    logger.info("Normalized matrix:\n %s", v)

    for agent in v.agents():
        for item in v.objects():
            if v[agent][item] * v.num_of_agents > total_value:
                logger.info(
                    "Allocating item %d to agent %d as she values it as %f > 1/n",
                    item,
                    agent,
                    v[agent][item] / total_value,
                )

                allocation = propm_allocation(v.without_agent(agent).without_object(item))
                insert_agent_into_allocation(agent, item, allocation)
                return allocation

    bundles = divide_into_bundles(v)
    logger.info("Divider divides items into following bundles: %s", str(bundles))

    remaining_agents = set(range(1, v.num_of_agents))

    logger.info("Building decomposition:")
    decomposition = Decomposition(v)
    for t in range(1, v.num_of_agents + 1):
        considered_items = sum(bundles[:t], [])

        candidates = list(
            filter(
                lambda a: v.num_of_agents * v.agent_value_for_bundle(a, considered_items) > t * total_value,
                remaining_agents,
            )
        )
        logger.info(
            "There are %s remaining agents that prefer sharing first %s bundles rather than last %s: %s",
            len(candidates),
            str(candidates),
            t,
            v.num_of_agents - t,
        )

        while len(candidates) > 0 and decomposition.num_of_agents() < t:
            logger.info("Current decomposition:\n %s", str(decomposition))

            decomposition.update(candidates[0], bundles[t - 1])

            remaining_agents = set(range(1, v.num_of_agents)).difference(decomposition.get_all_agents())
            candidates = list(
                filter(
                    lambda a: v.num_of_agents * v.agent_value_for_bundle(a, considered_items) > t * total_value,
                    remaining_agents,
                )
            )

        if decomposition.num_of_agents() < t:
            decomposition.agents.append(remaining_agents)
            decomposition.bundles.append(sum(bundles[t:], []))
            logger.info("Final decomposition:\n %s", str(decomposition))

            logger.info("Allocating bundle %d to divider agent", t)
            allocation = list([[] for _ in range(v.num_of_agents)])
            allocation[0] = bundles[t - 1]

            for agents, bundle in zip(decomposition.agents, decomposition.bundles):
                agents = list(sorted(agents))
                sub_problem = v.submatrix(agents, bundle)
                solution = propm_allocation(sub_problem)
                for i, agent in enumerate(agents):
                    for j in solution[i]:
                        allocation[agent].append(bundle[j])

            return allocation


###
### Subroutines
###

def insert_agent_into_allocation(agent: int, item: int, allocated_bundles: List[List[int]]):
    """
    If agent's i value of item j is greater than 1/n, we can allocate item j to i and solve
    the remaining sub-problem. This function inserts agent i with item j to the sub-problem
    allocation.
    >>> bundles = [[0, 2], [1, 3]]
    >>> insert_agent_into_allocation(0, 0, bundles)
    >>> bundles
    [[0], [1, 3], [2, 4]]
    >>> bundles = [[0, 2], [1, 3]]
    >>> insert_agent_into_allocation(1, 0, bundles)
    >>> bundles
    [[1, 3], [0], [2, 4]]
    """
    for bundle in allocated_bundles:
        for i, allocated_item in enumerate(bundle):
            if allocated_item >= item:
                bundle[i] = allocated_item + 1
    allocated_bundles.insert(agent, [item])


def divide_into_bundles(v: ValuationMatrix) -> List[List[int]]:
    """ "
    In stage 1 the divider agent having index 0 partitions the goods into bundles.
    >>> divide_into_bundles(ValuationMatrix([[0.5, 0, 0.5], [1/3, 1/3, 1/3]]))
    [[1, 0], [2]]
    >>> divide_into_bundles(ValuationMatrix([[0.25, 0.25, 0.25, 0.25, 0, 0], [0.25, 0, 0.26, 0, 0.25, 0.24], [0.25, 0, 0.24, 0, 0.25, 0.26]]))
    [[4, 5, 0], [1], [2, 3]]
    """
    total_value = v.verify_normalized()
    item_order = sorted(v.objects(), key=lambda j: v[0, j])

    bundles = []
    divided_items_count = 0
    divided_value = 0
    for bundle_index in v.agents():
        bundle_value = 0
        item_index = divided_items_count
        while (
            item_index < v.num_of_objects
            and (bundle_value + v[0, item_order[item_index]]) * (v.num_of_agents - bundle_index) + divided_value
            <= total_value
        ):
            bundle_value += v[0, item_order[item_index]]
            item_index += 1

        bundles.append(list(map(lambda t: item_order[t], range(divided_items_count, item_index))))
        divided_items_count = item_index
        divided_value += bundle_value
    return bundles


class Decomposition:
    """
    this class represents decomposition of problem into sub-problems
    sub-problem i is defined by pair (agents[i], bundles[i])
    """

    def __init__(self, values: ValuationMatrix):
        self.v = values
        self.total_value = values.verify_normalized()
        self.agents = []
        self.bundles = []

    def __repr__(self):
        return "\n".join(
            [
                f"sub-problem {i}:\n\tagents : {list(agents)}\n\tgoods : {bundle}"
                for i, (agents, bundle) in enumerate(zip(self.agents, self.bundles))
            ]
        )

    def num_of_agents(self):
        """
        this method returns number of agents in decomposition
        """
        return sum(map(len, self.agents))

    def num_of_objects(self):
        """
        this method returns number of goods in decomposition
        """
        return sum(map(len, self.bundles))

    def get_all_agents(self):
        """
        this method returns set containing all agents in decomposition
        """
        return set().union(*self.agents)

    def get_all_items(self):
        """
        this method returns list containing all items in decomposition
        """
        return sum(self.bundles, [])

    def update(self, candidate, bundle):
        """
        UpdateDecomposition subroutine

        bundle is S_t bundle
        candidate is agent k from the paper
        """
        logger.info("Updating decomposition trying to add agent %d and bundle %s", candidate, str(bundle))

        t = len(self.bundles) + 1

        sub_problem_graph = nx.DiGraph()
        sub_problem_graph.add_node(0, agents={candidate}, bundle=[])
        for i in range(1, t):
            sub_problem_graph.add_node(i, agents=self.agents[i - 1], bundle=self.bundles[i - 1])
        sub_problem_graph.add_node(t, agents=set(), bundle=bundle)

        sub_problem_agents = nx.get_node_attributes(sub_problem_graph, "agents")
        sub_problem_bundle = nx.get_node_attributes(sub_problem_graph, "bundle")
        for node_from in range(t):
            for node_to in range(1, t + 1):
                agent = next(
                    filter(
                        lambda a: self.v.agent_value_for_bundle(a, sub_problem_bundle[node_to]) * self.v.num_of_agents
                        >= self.total_value * max(1, len(sub_problem_agents[node_to])),
                        sub_problem_agents[node_from],
                    ),
                    None,
                )

                if agent is not None:
                    sub_problem_graph.add_edge(node_from, node_to, agent=agent)

        reachable = set()
        for parent, child in nx.dfs_edges(sub_problem_graph, 0):
            nx.set_node_attributes(sub_problem_graph, {child: parent}, "parent")
            reachable.add(child)

        parent = nx.get_node_attributes(sub_problem_graph, "parent")
        edge_agent = nx.get_edge_attributes(sub_problem_graph, "agent")
        if t in reachable:
            logger.info("Case 1: bundle's vertex is reachable from candidate's vertex in sub-problem graph")

            self.agents.append(set())
            self.bundles.append(bundle)

            node_to = t
            node_from = parent[node_to]
            while node_from != 0:
                logger.info("Moving agent %d from sub-problem %d to sub-problem %d", node_from - 1, node_to - 1)
                self.agents[node_from - 1].remove(edge_agent[(node_from, node_to)])
                self.agents[node_to - 1].add(edge_agent[(node_from, node_to)])
                node_to = node_from
                node_from = parent[node_to]

            logger.info("Adding agent %d to sub-problem %d", candidate, node_to - 1)
            self.agents[node_to - 1].add(candidate)
            return

        for node_to in reachable:
            for agent in sub_problem_agents[node_to]:
                if self.v.num_of_agents * self.v.agent_value_for_bundle(agent, self.get_all_items() + bundle) <= t:
                    logger.info(
                        "Case 2: agent's %d vertex is reachable from the candidate's in sub-problem graph"
                        "and she prefers sharing last n-t bundles rather than first t",
                        agent,
                    )

                    logger.info("Removing agent %d from decomposition", agent)
                    self.agents[node_to - 1].remove(agent)

                    node_from = parent[node_to]
                    while node_from != 0:
                        logger.info("Moving agent %d from sub-problem %d to sub-problem %d", node_from - 1, node_to - 1)
                        self.agents[node_from - 1].remove(edge_agent[(node_from, node_to)])
                        self.agents[node_to - 1].add(edge_agent[(node_from, node_to)])
                        node_to = node_from
                        node_from = parent[node_to]

                    logger.info("Adding agent %d to sub-problem %d")
                    self.agents[node_to - 1].add(candidate)
                    return

        logger.info(
            "Case 3: bundle's t vertex is not reachable from candidate's and all reachable agents of decomposition "
            "prefer first %d bundles rather than last %d",
            t,
            self.v.num_of_agents - t,
        )
        logger.info("Merging all sub-problems into one and adding candidate and bundle")
        self.agents = [self.get_all_agents().union({candidate})]
        self.bundles = [self.get_all_items() + bundle]



propm_allocation.logger = logger

if __name__ == "__main__":
    import sys

    logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
