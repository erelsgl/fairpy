
from fairpy import AgentList
from typing import List, Tuple
import networkx as nx
from itertools import permutations

def bundles_from_edges(match:set, G:nx.Graph) -> dict:
    bundles = {}
    for edge in match:
        first_node = edge[0]
        second_node = edge[1]
        if G.nodes[first_node].get('isAgent', False):
            bundles[first_node] = [second_node]
        else:
            bundles[second_node] = [first_node]
    return bundles

def reduction_to_graph(agents:AgentList, items:List, threshold:float) -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(agents.agent_names())
    nx.set_node_attributes(G, True, 'isAgent')
    G.add_nodes_from(items)
    for agent in agents:
        for item in items:
            val_item = agent.value(item)
            if val_item >= threshold:
                G.add_edge(agent.name(), item)
    return G

def isBordaCount(agents:AgentList) -> bool:
    for agent in agents:
        agent_values = {agent.value(item) for item in agents.all_items()}
        if len (agent_values) < len(agents.all_items()):
            return False
        for val in range(len(agents.all_items())):
            if val not in agent_values:
                return False
    return True

def selection_by_order(agents:AgentList, items:list, allocation:List[list], num_iteration:int=1, order:list=None) -> Tuple[list,List[list]]:
    if not order:
        order = [i for i in range(len(agents))]
        order += reversed(order)

    for iter in range(num_iteration):
        for i in order:
            agent = agents[i]
            favorite_index = agent.best_index(items)
            favorite = items[favorite_index]
            allocation[i].append(favorite)
            items.remove(favorite)
    return items, allocation

def isEven(n):
    return n % 2 == 0

def get_agents_with_permutations_of_valuations(n,k):
    ans = []
    if n == 0 or k == 0:
        raise ValueError(f"n and k must be at least 0, but n={n}, k={k}")
    for i in permutations(range(k)):
        ans.append(list(i))
        if len(ans) == n:
            break
    return AgentList(ans)