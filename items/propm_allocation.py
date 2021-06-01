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
from fairpy import valuations, ValuationMatrix, Allocation
from typing import List, Set
from copy import deepcopy


def insert_agent_into_allocation(agent: int, item: int, allocated_bundles: List[List[int]]):
    """
    If agent's i value of item j is greater than 1/n, we can allocate item j to i and solve
    the remaining subproblem. This function inserts agent i with item j to the subproblem
    allocation.
    """
    for bundle in allocated_bundles:
        for i, allocated_item in enumerate(bundle):
            if allocated_item >= item:
                bundle[i] = allocated_item + 1
    allocated_bundles.insert(agent, [item])


def divide(v: ValuationMatrix) -> List[List[int]]:
    """"
    In stage 1 the divider agent having index 0 partitions the goods into bundles.
    """
    total_value = v.verify_normalized()
    item_order = sorted(v.objects(), key=lambda j: v[0, j])

    bundles = []
    divided_items_count = 0
    divided_value = 0
    for bundle_index in v.agents():
        bundle_value = 0
        item_index = divided_items_count
        while item_index < v.num_of_objects and (
                bundle_value + v[0, item_order[item_index]]) * (
                v.num_of_agents - bundle_index) + divided_value <= total_value:
            bundle_value += v[0, item_order[item_index]]
            item_index += 1

        bundles.append(
            list(map(lambda t: item_order[t], range(divided_items_count, item_index))))
        divided_items_count = item_index
        divided_value += bundle_value
    return bundles


def update_decomposition(v: ValuationMatrix, agents: List[Set[int]], items: List[List[int]], bundle: List[int],
                         candidate: int) -> Set[int]:
    """
    UpdateDecomposition subroutine
    for each i (agents[i], items[i]) represents a subproblem of decomposition
    bundle is S_t bundle
    candidate is agent k from the paper
    """
    iter = len(agents) + 1

    subproblem_graph = nx.DiGraph()
    subproblem_graph.add_node(0, agents={candidate}, items=[])
    for i in range(1, iter):
        subproblem_graph.add_node(i, agents=agents[i - 1], items=items[i - 1])
    subproblem_graph.add_node(iter, agents=set(), items=bundle)

    subproblem_agents = nx.get_node_attributes(subproblem_graph, 'agents')
    subproblem_items = nx.get_node_attributes(subproblem_graph, 'items')
    for node_from in range(iter):
        for node_to in range(1, iter + 1):
            print(node_from, node_to, iter)
            agent = next((a for a in subproblem_agents[node_from] if v.agent_value_for_bundle(a, subproblem_items[
                node_to]) * v.num_of_agents >= v.verify_normalized() * len(subproblem_agents[node_to])), None)
            if agent is not None:
                subproblem_graph.add_edge(node_from, node_to, agent=agent)

    reachable = []
    for parent, child in nx.dfs_edges(subproblem_graph, 0):
        nx.set_node_attributes(subproblem_graph, {child: parent}, "parent")
        reachable.append(child)

    parent = nx.get_node_attributes(subproblem_graph, "parent")
    edge_agent = nx.get_edge_attributes(subproblem_graph, "agent")
    if iter in reachable is not None:
        print('kek')
        node_to = parent.get(iter)
        agents.append({edge_agent[(node_to, iter)]})
        items.append(bundle)
        if node_to == 0:
            return set().union(*agents)
        agents[node_to - 1].remove(edge_agent[(node_to, iter)])
        node_from = parent.get(node_to)
        while node_from != 0:
            agents[node_from - 1].remove(edge_agent[(node_from, node_to)])
            agents[node_to - 1].add(edge_agent[(node_from, node_to)])
            node_to = node_from
            node_from = parent.get(node_to)
        agents[node_to - 1].add(candidate)
        return set().union(*agents)

    for node_to in reachable:
        for agent in subproblem_agents[node_to]:
            if v.num_of_agents * v.agent_value_for_bundle(agent, sum(items, []) + bundle) <= iter:
                print('kak')
                agents[node_to - 1].remove(agent)
                node_from = parent[node_to]
                while node_from != 0:
                    agents[node_from - 1].remove(edge_agent[(node_from, node_to)])
                    agents[node_to - 1].add(edge_agent[(node_from, node_to)])
                    node_to = node_from
                    node_from = parent.get(node_to)
                agents[node_to - 1].add(candidate)
                return set().union(*agents)

    agents = [set().union(*agents)]
    agents[0].add(candidate)
    items = [sum(items, [])]
    items[0] += bundle
    return agents[0]


def solve(agents) -> List[List[int]]:
    """
    recursive function which takes valuations and returns a PROPm allocation
    as a list of bundles
    """
    v = valuations.matrix_from(agents)
    if v.num_of_agents == 0 or v.num_of_objects == 0:
        return []

    total_value = v.normalize()

    for agent in v.agents():
        for item in v.objects():
            if v[agent][item] * v.num_of_agents > total_value:
                allocation = solve(v.without_agent(agent).without_object(object))
                insert_agent_into_allocation(agent, item, allocation)
                return allocation

    bundles = divide(v)
    remaining_agents = set(range(1, v.num_of_agents))
    subproblems_agents = []
    subproblems_items = []

    for iter in range(1, v.num_of_agents + 1):
        considered_items = sum(bundles[:iter], [])

        candidates = list([agent for agent in remaining_agents if
                           v.num_of_agents * v.agent_value_for_bundle(agent, considered_items) > iter * total_value])
        decomposition_agents = set().union(*subproblems_agents)
        while len(candidates) > 0 and len(decomposition_agents) < iter:
            decomposition_agents = update_decomposition(v, subproblems_agents, subproblems_items, bundles[iter - 1],
                                                        candidates[0])
            remaining_agents = set([agent for agent in range(1, v.num_of_agents) if agent not in decomposition_agents])
            candidates = list([agent for agent in remaining_agents if v.num_of_agents * \
                               v.agent_value_for_bundle(agent, considered_items) > iter * total_value])

        if len(decomposition_agents) < iter:
            subproblems_agents.append(remaining_agents)
            subproblems_items.append(sum(bundles[iter:], []))

            allocation = list([[] for _ in range(v.num_of_agents)])
            allocation[0] = bundles[iter - 1]

            for agents, items in zip(subproblems_agents, subproblems_items):
                agents = list(sorted(agents))
                subproblem = v.submatrix(agents, items)
                solution = solve(subproblem)
                for i, agent in enumerate(agents):
                    for j in solution[i]:
                        allocation[agent].append(items[j])

            return allocation


def propm_allocation(agents) -> Allocation:
    """
    Function that takes a valuation matrix and returns PROPm allocation of goods.
    """
    values = valuations.matrix_from(deepcopy(agents))
    bundles = solve(agents)
    return Allocation(values, bundles)
