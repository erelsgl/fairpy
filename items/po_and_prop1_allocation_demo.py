#!python3

"""
Demonstration of the PO+PROP1 algorithm.

Programmer: Tom Latinn
Since: 2021-02
"""


import networkx as nx
from fairpy.agents import AdditiveAgent
from fairpy.items.allocations_fractional import FractionalAllocation
from fairpy.items.po_and_prop1_allocation import find_po_and_prop1_allocation

agent1 = AdditiveAgent({"a": 10, "b": 100, "c": 80, "d": -100}, name="agent1")
agent2 = AdditiveAgent({"a": 20, "b": 100, "c": -40, "d": 10}, name="agent2")

print("Agent 1: {}\nAgent 2: {}".format(agent1, agent2))

all_items  = {'a', 'b', 'c', 'd'}
all_agents = [agent1, agent2]
initial_allocation = FractionalAllocation(all_agents, 
	[{'a':0.0,'b': 0.3,'c':1.0,'d':0.0},{'a':1.0,'b':0.7,'c':0.0,'d':1.0}
	])

print("Initial allocation", initial_allocation)

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

new_allocation = find_po_and_prop1_allocation(G, initial_allocation, all_items)

print(new_allocation)