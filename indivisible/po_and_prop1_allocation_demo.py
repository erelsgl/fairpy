#!python3

"""
Demonstration of the PO+PROP1 algorithm.

Programmer: Tom Latinn
Since: 2021-02
"""


import networkx as nx
from fairpy.indivisible.agents import AdditiveAgent
from fairpy.indivisible.allocations import FractionalAllocation
from fairpy.indivisible.po_and_prop1_allocation import find_po_and_prop1_allocation

agent1 = AdditiveAgent({"a": 10, "b": 100, "c": 80, "d": -100}, name="agent1")
agent2 = AdditiveAgent({"a": 20, "b": 100, "c": -40, "d": 10}, name="agent2")

print("Agent 1: {}\nAgent 2: {}".format(agent1, agent2))

G = nx.Graph()
G.add_node(agent1)
G.add_node(agent2)
G.add_node('a')
G.add_node('b')
G.add_node('c')
G.add_node('d')
G.add_edge(agent1, 'b')
G.add_edge(agent1, 'c')
G.add_edge(agent2, 'a')
G.add_edge(agent2, 'b')
G.add_edge(agent2, 'd')

print("Nodes of graph: {}\nEdges of graph: {}".format(G.nodes(), G.edges()))

items_for_func = {'a', 'b', 'c', 'd'}
list_of_agents_for_func = [agent1, agent2]
alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.0,'b': 0.3,'c':1.0,'d':0.0},{'a':1.0,'b':0.7,'c':0.0,'d':1.0}])
alloc = find_po_and_prop1_allocation(G, alloc_y_for_func, items_for_func)

print(alloc)