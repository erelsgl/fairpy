#!python3

"""
An implementation of a PO+PROP1 allocation algorithm. Reference:

    Haris Aziz, Herve Moulin and Fedor Sandomirskiy (2020).
    ["A polynomial-time algorithm for computing a Pareto optimal and almost proportional allocation"](https://www.sciencedirect.com/science/article/pii/S0167637720301024).
    Operations Research Letters. 
    * Algorithm 1, starting at step 3.

Programmer: Tom Latinn
Since:  2021-02
"""


import queue
import networkx as nx
from fairpy.agents import AdditiveAgent, Bundle, List
from fairpy.items.allocations_fractional import FractionalAllocation
from networkx.algorithms import bipartite, find_cycle

#Main functions

def find_po_and_prop1_allocation(Gx: bipartite, fpo_alloc: FractionalAllocation, items: Bundle) -> FractionalAllocation:
    """
    This function implements the algorithm starting at step 3.

    INPUT:
    * Gx - An acyclic consumption graph: a bipartite graph describing which agent consumes which object. 
    * fpo_alloc: A fractionally-Pareto-optimal fractional allocation corresponding to the given consumption graph.
        NOTE: Converting a general allocation to an fPO allocation with an acyclic consumption graph should be done by a different algorithm in a previous step (step 2).
    * items: Set of items to allocate.

    OUTPUT:
    * Fractional allocation which is an integral allocation (since all fractions are 0.0 or 1.0),
    which is PO and PROP1

    First example:
    Case 1: Only one player(must get everything),Items with positive utility.
    >>> agent1 = AdditiveAgent({"x": 1, "y": 2, "z": 4}, name="agent1")
    >>> list_of_agents_for_func = [agent1]
    >>> items_for_func ={'x','y','z'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'x':1.0,'y':1.0, 'z':1.0}])
    >>> G = nx.Graph()
    >>> G.add_node(agent1)
    >>> G.add_node('x')
    >>> G.add_node('y')
    >>> G.add_node('z')
    >>> G.add_edge(agent1, 'x')
    >>> G.add_edge(agent1, 'y')
    >>> G.add_edge(agent1, 'z')
    >>> alloc = find_po_and_prop1_allocation(G, alloc_y_for_func, items_for_func)
    >>> print(alloc)
    agent1's bundle: {x,y,z},  value: 7.0
    <BLANKLINE>
    >>> alloc.is_complete_allocation()
    True

    Case 2: Only one player(must get everything),Items with negative utility.
    >>> agent1= AdditiveAgent({"x": -1, "y": -2, "z": -4}, name="agent1")
    >>> list_of_agents_for_func = [agent1]
    >>> items_for_func ={'x','y','z'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'x':1.0,'y':1.0, 'z':1.0}])
    >>> G = nx.Graph()
    >>> G.add_node(agent1)
    >>> G.add_node('x')
    >>> G.add_node('y')
    >>> G.add_node('z')
    >>> G.add_edge(agent1, 'x')
    >>> G.add_edge(agent1, 'y')
    >>> G.add_edge(agent1, 'z')
    >>> alloc = find_po_and_prop1_allocation(G, alloc_y_for_func, items_for_func)
    >>> print(alloc)
    agent1's bundle: {x,y,z},  value: -7.0
    <BLANKLINE>
    >>> alloc.is_complete_allocation()
    True

    Case 3: Only one player(must get everything),Items with negative and positive utilitys.
    >>> agent1 = AdditiveAgent({"x": -1, "y": 2, "z": -4}, name="agent1")
    >>> list_of_agents_for_func = [agent1]
    >>> items_for_func ={'x','y','z'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'x':1.0,'y':1.0, 'z':1.0}])
    >>> G = nx.Graph()
    >>> G.add_node(agent1)
    >>> G.add_node('x')
    >>> G.add_node('y')
    >>> G.add_node('z')
    >>> G.add_edge(agent1, 'x')
    >>> G.add_edge(agent1, 'y')
    >>> G.add_edge(agent1, 'z')
    >>> alloc = find_po_and_prop1_allocation(G, alloc_y_for_func, items_for_func)
    >>> print(alloc)
    agent1's bundle: {x,y,z},  value: -3.0
    <BLANKLINE>
    >>> alloc.is_complete_allocation()
    True

    Second example:
    (example 3 in the second part of the work)
    >>> agent1 = AdditiveAgent({"a": 10, "b": 100, "c": 80, "d": -100}, name="agent1")
    >>> agent2 = AdditiveAgent({"a": 20, "b": 100, "c": -40, "d": 10}, name="agent2")
    >>> G = nx.Graph()
    >>> all_agents = [agent1, agent2]
    >>> all_items = {'a', 'b', 'c', 'd'}
    >>> G.add_nodes_from(all_agents + list(all_items))
    >>> G.add_edges_from([[agent1, 'b'], [agent1, 'c'], [agent2, 'a'], [agent2, 'b'], [agent2, 'd']])
    >>> alloc_y_for_func = FractionalAllocation(all_agents, [{'a':0.0,'b':0.3,'c':1.0,'d':0.0},{'a':1.0,'b':0.7,'c':0.0,'d':1.0}])
    >>> alloc = find_po_and_prop1_allocation(G, alloc_y_for_func, all_items)
    >>> print(alloc)
    agent1's bundle: {b,c},  value: 180.0
    agent2's bundle: {a,d},  value: 30.0
    <BLANKLINE>
    >>> alloc.is_complete_allocation()
    True


    Third example:
    Case 1:
    (example 5 in the second part of the work)
    >>> agent1= AdditiveAgent({"a": 100, "b": 10, "c": 50, "d": 100 ,"e": 70,"f": 100, "g": 300, "h": 40, "i": 30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": 40, "d": 90 ,"e": 90,"f": 100, "g": 30, "h": 80, "i": 90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": 30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": 90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": 200, "b": 40, "c": 20, "d": 80 ,"e": 300,"f": 100, "g": 30, "h": 60, "i": 180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": 100, "g": 300, "h": 120, "i": 180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.0,'b':0.0,'c':1.0,'d':1.0,'e':0.0,'f':0.2,'g':0.0,'h':0.0,'i':0.0},{'a':0.0,'b':0.0,'c':0.0,'d':0.0,'e':0.8,'f':0.4,'g':0.0,'h':0.0,'i':0.0},{'a':0.0,'b':0.0,'c':0.0,'d':0.0,'e':0.0,'f':0.2,'g':1.0,'h':0.0,'i':0.0},{'a':1.0,'b':0.0,'c':0.0,'d':0.0,'e':0.2,'f':0.0,'g':0.0,'h':0.0,'i':0.0},{'a':0.0,'b':1.0,'c':0.0,'d':0.0,'e':0.0,'f':0.2,'g':0.0,'h':1.0,'i':1.0}])
    >>> G = nx.Graph()
    >>> G.add_node(agent1)
    >>> G.add_node(agent2)
    >>> G.add_node(agent3)
    >>> G.add_node(agent4)
    >>> G.add_node(agent5)
    >>> G.add_node('a')
    >>> G.add_node('b')
    >>> G.add_node('c')
    >>> G.add_node('d')
    >>> G.add_node('e')
    >>> G.add_node('f')
    >>> G.add_node('g')
    >>> G.add_node('h')
    >>> G.add_node('i')
    >>> G.add_edge(agent1, 'c')
    >>> G.add_edge(agent1, 'd')
    >>> G.add_edge(agent1, 'f')
    >>> G.add_edge(agent2, 'e')
    >>> G.add_edge(agent2, 'f')
    >>> G.add_edge(agent3, 'f')
    >>> G.add_edge(agent3, 'g')
    >>> G.add_edge(agent4, 'a')
    >>> G.add_edge(agent4, 'e')
    >>> G.add_edge(agent5, 'b')
    >>> G.add_edge(agent5, 'h')
    >>> G.add_edge(agent5, 'i')
    >>> G.add_edge(agent5, 'f')
    >>> alloc = find_po_and_prop1_allocation(G, alloc_y_for_func, items_for_func)
    >>> # print(alloc)  # Below is ONE possible output.
    # agent1's bundle: {c,d,f},  value: 250.0
    # agent2's bundle: {e},  value: 90.0
    # agent3's bundle: {g},  value: 300.0
    # agent4's bundle: {a},  value: 200.0
    # agent5's bundle: {b,h,i},  value: 350.0
    # <BLANKLINE>
    >>> alloc.is_complete_allocation()
    True

    Case 2:
    (example 4 in the second part of the work)
    >>> agent1= AdditiveAgent({"a": -100, "b": -10, "c": -50, "d":-100 ,"e": -70,"f": -100, "g": -200, "h": -40, "i": -30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": -20, "b": -20, "c": -40, "d": -90 ,"e": -90,"f": -100, "g": -100, "h": -80, "i": -90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": -10, "b": -30, "c": -30, "d": -40 ,"e": -180,"f": -100, "g": -200, "h": -20, "i": -90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": -200, "b": -40, "c": -20, "d": -80 ,"e": -300,"f": -100, "g": -100, "h": -60, "i": -180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": -50, "b": -50, "c": -10, "d": -60 ,"e": -90,"f": -100, "g": -200, "h": -120, "i": -180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.0,'b':1.0,'c':0.0,'d':0.0,'e':1.0,'f':0.2,'g':0.0,'h':0.0,'i':1.0},{'a':0.0,'b':0.0,'c':0.0,'d':0.0,'e':0.0,'f':0.2,'g':0.0,'h':0.0,'i':0.0},{'a':1.0,'b':0.0,'c':0.0,'d':1.0,'e':0.0,'f':0.2,'g':0.0,'h':1.0,'i':0.0},{'a':0.0,'b':0.0,'c':0.0,'d':0.0,'e':0.0,'f':0.2,'g':1.0,'h':0.0,'i':0.0},{'a':0.0,'b':0.0,'c':1.0,'d':0.0,'e':0.0,'f':0.2,'g':0.0,'h':0.0,'i':0.0}])
    >>> G = nx.Graph()
    >>> G.add_node(agent1)
    >>> G.add_node(agent2)
    >>> G.add_node(agent3)
    >>> G.add_node(agent4)
    >>> G.add_node(agent5)
    >>> G.add_node('a')
    >>> G.add_node('b')
    >>> G.add_node('c')
    >>> G.add_node('d')
    >>> G.add_node('e')
    >>> G.add_node('f')
    >>> G.add_node('g')
    >>> G.add_node('h')
    >>> G.add_node('i')
    >>> G.add_edge(agent1, 'b')
    >>> G.add_edge(agent1, 'e')
    >>> G.add_edge(agent1, 'f')
    >>> G.add_edge(agent1, 'i')
    >>> G.add_edge(agent2, 'f')
    >>> G.add_edge(agent3, 'a')
    >>> G.add_edge(agent3, 'd')
    >>> G.add_edge(agent3, 'f')
    >>> G.add_edge(agent3, 'h')
    >>> G.add_edge(agent4, 'g')
    >>> G.add_edge(agent4, 'f')
    >>> G.add_edge(agent5, 'c')
    >>> G.add_edge(agent5, 'f')
    >>> alloc = find_po_and_prop1_allocation(G, alloc_y_for_func, items_for_func)
    >>> print(alloc) #in my example I gave f to agent1, but the algorithm gave it to agent2
    agent1's bundle: {b,e,i},  value: -110.0
    agent2's bundle: {f},  value: -100.0
    agent3's bundle: {a,d,h},  value: -70.0
    agent4's bundle: {g},  value: -100.0
    agent5's bundle: {c},  value: -10.0
    <BLANKLINE>
    >>> alloc.is_complete_allocation()
    True

    Case 3:
    (example 6 in the second part of the work)
    >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 300, "g": -300, "h": -40, "i": 30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 300, "h": 80, "i": 90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": -30, "c": 30, "d": 40 ,"e": 180,"f": 300, "g": 30, "h": 20, "i": -90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": -200, "b": 40, "c": -20, "d": 80 ,"e": -300,"f": 300, "g": 300, "h": 60, "i": -180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": 100, "g": 300, "h": -120, "i": 180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.0,'b':0.0,'c':1.0,'d':0.0,'e':0.0,'f':0.4,'g':0.0,'h':0.0,'i':0.0},{'a':0.0,'b':0.0,'c':0.0,'d':1.0,'e':0.0,'f':0.0,'g':0.5,'h':1.0,'i':0.0},{'a':0.0,'b':0.0,'c':0.0,'d':0.0,'e':1.0,'f':0.4,'g':0.0,'h':0.0,'i':0.0},{'a':0.0,'b':0.0,'c':0.0,'d':0.0,'e':0.0,'f':0.0,'g':0.5,'h':0.0,'i':0.0},{'a':1.0,'b':1.0,'c':0.0,'d':0.0,'e':0.0,'f':0.2,'g':0.0,'h':0.0,'i':1.0}])
    >>> G = nx.Graph()
    >>> G.add_node(agent1)
    >>> G.add_node(agent2)
    >>> G.add_node(agent3)
    >>> G.add_node(agent4)
    >>> G.add_node(agent5)
    >>> G.add_node('a')
    >>> G.add_node('b')
    >>> G.add_node('c')
    >>> G.add_node('d')
    >>> G.add_node('e')
    >>> G.add_node('f')
    >>> G.add_node('g')
    >>> G.add_node('h')
    >>> G.add_node('i')
    >>> G.add_edge(agent1, 'c')
    >>> G.add_edge(agent1, 'f')
    >>> G.add_edge(agent2, 'd')
    >>> G.add_edge(agent2, 'h')
    >>> G.add_edge(agent2, 'g')
    >>> G.add_edge(agent3, 'e')
    >>> G.add_edge(agent3, 'f')
    >>> G.add_edge(agent4, 'g')
    >>> G.add_edge(agent5, 'a')
    >>> G.add_edge(agent5, 'b')
    >>> G.add_edge(agent5, 'i')
    >>> G.add_edge(agent5, 'f')
    >>> alloc = find_po_and_prop1_allocation(G, alloc_y_for_func, items_for_func)
    >>> print(alloc)
    agent1's bundle: {c,f},  value: 350.0
    agent2's bundle: {d,g,h},  value: 470.0
    agent3's bundle: {e},  value: 180.0
    agent4's bundle: {},  value: 0.0
    agent5's bundle: {a,b,i},  value: 280.0
    <BLANKLINE>
    >>> alloc.is_complete_allocation()
    True

    Fourth example: A general situation, in which the new division is indeed a pareto improvement of the original division
    (example 7 in the second part of the work)
    >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 100, "g": -300, "h": -40, "i": 30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 30, "h": 80, "i": 90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": -30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": -90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": -200, "b": 40, "c": -20, "d": 80 ,"e": -300,"f": 100, "g": 30, "h": 60, "i": -180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": -100, "g": 300, "h": -120, "i": 180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.0,'b':1.0,'c':0.0,'d':0.0,'e':1.0,'f':1.0,'g':0.0,'h':0.0,'i':0.4},{'a':0.0,'b':0.0,'c':0.0,'d':1.0,'e':0.0,'f':0.0,'g':0.0,'h':1.0,'i':0.0},{'a':0.0,'b':0.0,'c':1.0,'d':0.0,'e':0.0,'f':0,'g':1.0,'h':0.0,'i':0.0},{'a':0.0,'b':0.0,'c':0.0,'d':0.0,'e':0.0,'f':0.0,'g':0.0,'h':0.0,'i':0.0},{'a':1.0,'b':0.0,'c':0.0,'d':0.0,'e':0.0,'f':0.0,'g':0.0,'h':0.0,'i':0.6}])
    >>> G = nx.Graph()
    >>> G.add_node(agent1)
    >>> G.add_node(agent2)
    >>> G.add_node(agent3)
    >>> G.add_node(agent4)
    >>> G.add_node(agent5)
    >>> G.add_node('a')
    >>> G.add_node('b')
    >>> G.add_node('c')
    >>> G.add_node('d')
    >>> G.add_node('e')
    >>> G.add_node('f')
    >>> G.add_node('g')
    >>> G.add_node('h')
    >>> G.add_node('i')
    >>> G.add_edge(agent1, 'e')
    >>> G.add_edge(agent1, 'b')
    >>> G.add_edge(agent1, 'f')
    >>> G.add_edge(agent1, 'i')
    >>> G.add_edge(agent2, 'd')
    >>> G.add_edge(agent2, 'h')
    >>> G.add_edge(agent3, 'c')
    >>> G.add_edge(agent3, 'g')
    >>> G.add_edge(agent5, 'a')
    >>> G.add_edge(agent5, 'i')
    >>> alloc = find_po_and_prop1_allocation(G, alloc_y_for_func, items_for_func)
    >>> print(alloc)
    agent1's bundle: {b,e,f,i},  value: 210.0
    agent2's bundle: {d,h},  value: 170.0
    agent3's bundle: {c,g},  value: 330.0
    agent4's bundle: {},  value: 0.0
    agent5's bundle: {a},  value: 50.0
    <BLANKLINE>
    >>> alloc.is_complete_allocation()
    True

    """
    # Check input
    try:
        find_cycle(Gx)
        raise Exception("There are cycles in the given graph")
    except nx.NetworkXNoCycle:
        pass

    #Algorithm
    Q = queue.Queue()
    while Gx.number_of_edges() > len(items):  #If each item belongs to exactly one agent, the number of edges in the graph will necessarily be the same as the number of items
        agent = find_agent_sharing_item(Gx, items)
        Q.put(agent)  #Because of the deletion of edges in the graph we will never put again an agent who has previously entered Q
        while len(Q.queue) != 0:  #If the queue is not empty
            curr_agent = Q.get(0)  #Get the first agent from the queue
            dict_of_items_curr_agent_share = get_dict_of_items_curr_agent_share(curr_agent, fpo_alloc)
            add_neighbors_to_Q(Q, dict_of_items_curr_agent_share)
            if dict_of_items_curr_agent_share != {}:  #Check that the agent is actually sharing items
                for item, agents in dict_of_items_curr_agent_share.items():
                    if curr_agent.value(item) > 0:  #If a positive utility
                        update_fpo_alloc_and_Gx(curr_agent, item, agents, fpo_alloc, Gx) #Gave to the curr_agent the item
                    else:  #If a negative utility
                        other_agent = agents[0]  #Gave another agent the item
                        agents.remove(other_agent)
                        agents.append(curr_agent)
                        update_fpo_alloc_and_Gx(other_agent, item, agents, fpo_alloc, Gx)
    return fpo_alloc


#-----------------Help functions---------------------
'''
The function receives as input:
Gx - bipartite graph without circles
items: The group of agents' items

The function returns as output:
The first AdditiveAgent shared item
'''
def find_agent_sharing_item(Gx: bipartite, items: Bundle) -> AdditiveAgent:
    """
    >>> agent1 = AdditiveAgent({"a": 100, "b": 10, "c": 50}, name="agent1")
    >>> agent2 = AdditiveAgent({"a": 20, "b": 20, "c": 40}, name="agent2")
    >>> agent3 = AdditiveAgent({"a": 10, "b": 30, "c": 30}, name="agent3")
    >>> G = nx.Graph()
    >>> G.add_node(agent1)
    >>> G.add_node(agent2)
    >>> G.add_node(agent3)
    >>> G.add_node('a')
    >>> G.add_node('b')
    >>> G.add_node('c')
    >>> G.add_edge(agent1,'a')
    >>> G.add_edge(agent2,'a')
    >>> items_for_func = {'a','b','c'}
    >>> find_agent_sharing_item(G,items_for_func).name()
    'agent1'

    >>> agent1= AdditiveAgent({"a": 100, "b": 10, "c": 50, "d": 100 ,"e": 70,"f": 100, "g": 300, "h": 40, "i": 30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": 40, "d": 90 ,"e": 90,"f": 100, "g": 30, "h": 80, "i": 90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": 30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": 90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": 200, "b": 40, "c": 20, "d": 80 ,"e": 300,"f": 100, "g": 30, "h": 60, "i": 180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": 100, "g": 300, "h": 120, "i": 180}, name="agent5")
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> G = nx.Graph()
    >>> G.add_node(agent1)
    >>> G.add_node(agent2)
    >>> G.add_node(agent3)
    >>> G.add_node(agent4)
    >>> G.add_node(agent5)
    >>> G.add_node('a')
    >>> G.add_node('b')
    >>> G.add_node('c')
    >>> G.add_node('d')
    >>> G.add_node('e')
    >>> G.add_node('f')
    >>> G.add_node('g')
    >>> G.add_node('h')
    >>> G.add_node('i')
    >>> G.add_edge(agent1, 'c')
    >>> G.add_edge(agent1, 'd')
    >>> G.add_edge(agent1, 'f')
    >>> G.add_edge(agent2, 'e')
    >>> G.add_edge(agent2, 'f')
    >>> G.add_edge(agent3, 'f')
    >>> G.add_edge(agent3, 'g')
    >>> G.add_edge(agent4, 'a')
    >>> G.add_edge(agent4, 'e')
    >>> G.add_edge(agent5, 'b')
    >>> G.add_edge(agent5, 'h')
    >>> G.add_edge(agent5, 'i')
    >>> G.add_edge(agent5, 'f')
    >>> # find_agent_sharing_item(G,items_for_func) #the output can be:
    # agent1 is an agent with additive valuations: a=100 b=10 c=50 d=100 e=70 f=100 g=300 h=40 i=30
    """
    for i in items:
        neighbors_of_i = [n for n in Gx.neighbors(i)]
        if len(neighbors_of_i) > 1:
            return neighbors_of_i[0]

'''
The function receives as input:
fpo_alloc: Fractional allocation
curr_agent:  AdditiveAgent

The function returns as output:
dict That the keys in it are items that curr_agent share and the values in it are a list of agents that share the item
'''
def get_dict_of_items_curr_agent_share(curr_agent:  AdditiveAgent, fpo_alloc: FractionalAllocation) -> dict:
    """
    >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 100, "g": -300, "h": -40, "i": 30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 30, "h": 80, "i": 90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": -30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": -90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": -200, "b": 40, "c": -20, "d": 80 ,"e": -300,"f": 100, "g": 30, "h": 60, "i": -180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": -100, "g": 300, "h": -120, "i": 180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.0,'b':1.0,'c':0.0,'d':0.0,'e':1.0,'f':1.0,'g':0.0,'h':0.0,'i':0.4},{'a':0.0,'b':0.0,'c':0.0,'d':1.0,'e':0.0,'f':0.0,'g':0.0,'h':1.0,'i':0.0},{'a':0.0,'b':0.0,'c':1.0,'d':0.0,'e':0.0,'f':0,'g':1.0,'h':0.0,'i':0.0},{'a':0.0,'b':0.0,'c':0.0,'d':0.0,'e':0.0,'f':0.0,'g':0.0,'h':0.0,'i':0.0},{'a':1.0,'b':0.0,'c':0.0,'d':0.0,'e':0.0,'f':0.0,'g':0.0,'h':0.0,'i':0.6}])
    >>> d = get_dict_of_items_curr_agent_share(agent1, alloc_y_for_func)
    >>> {key: list(map(lambda agent:agent.name(), agents)) for key,agents in d.items()}
    {'i': ['agent5']}

    >>> agent1= AdditiveAgent({"a": 100, "b": 10, "c": 50, "d": 100 ,"e": 70,"f": 100, "g": 300, "h": 40, "i": 30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": 40, "d": 90 ,"e": 90,"f": 100, "g": 30, "h": 80, "i": 90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": 30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": 90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": 200, "b": 40, "c": 20, "d": 80 ,"e": 300,"f": 100, "g": 30, "h": 60, "i": 180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": 100, "g": 300, "h": 120, "i": 180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.0,'b':0.0,'c':1.0,'d':1.0,'e':0.0,'f':0.2,'g':0.0,'h':0.0,'i':0.0},{'a':0.0,'b':0.0,'c':0.0,'d':0.0,'e':0.8,'f':0.4,'g':0.0,'h':0.0,'i':0.0},{'a':0.0,'b':0.0,'c':0.0,'d':0.0,'e':0.0,'f':0.2,'g':1.0,'h':0.0,'i':0.0},{'a':1.0,'b':0.0,'c':0.0,'d':0.0,'e':0.2,'f':0.0,'g':0.0,'h':0.0,'i':0.0},{'a':0.0,'b':1.0,'c':0.0,'d':0.0,'e':0.0,'f':0.2,'g':0.0,'h':1.0,'i':1.0}])
    >>> d = get_dict_of_items_curr_agent_share(agent5, alloc_y_for_func)
    >>> {key: list(map(lambda agent:agent.name(), agents)) for key,agents in d.items()}
    {'f': ['agent1', 'agent2', 'agent3']}
    """
    result = {}
    index_of_agent = fpo_alloc.agents.index(curr_agent)
    for item, val in fpo_alloc.map_item_to_fraction[index_of_agent].items():
        if val > 0 and val != 1.0:
            list_of_agent_that_share_item = []
            for agent in fpo_alloc.agents:
                index_of_agent = fpo_alloc.agents.index(agent)
                if agent != curr_agent and fpo_alloc.map_item_to_fraction[index_of_agent][item] >0:
                    list_of_agent_that_share_item.append(agent)
            result[item] = list_of_agent_that_share_item
    return result

'''
The function gives the whole item to curr_agent,
i.e, in fpo_alloc in this item it will have 1.0 and all the other agents that share it in the item will have 0.0
Also the function will delete the edges between the agents that divide it item and item
'''
def update_fpo_alloc_and_Gx(curr_agent: AdditiveAgent, item: str, list_of_agent_share_item: List, fpo_alloc: FractionalAllocation, Gx: bipartite) -> None:
    """
    >>> agent1 = AdditiveAgent({"a": 10, "b": 100, "c": 80, "d": -100}, name="agent1")
    >>> agent2 = AdditiveAgent({"a": 20, "b": 100, "c": -40, "d": 10}, name="agent2")
    >>> items_for_func = {'a', 'b', 'c', 'd'}
    >>> list_of_agents_for_func = [agent1, agent2]
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.0,'b':0.3,'c':1.0,'d':0.0},{'a':1.0,'b':0.7,'c':0.0,'d':1.0}])
    >>> G = nx.Graph()
    >>> G.add_node(agent1)
    >>> G.add_node(agent2)
    >>> G.add_node('a')
    >>> G.add_node('b')
    >>> G.add_node('c')
    >>> G.add_node('d')
    >>> G.add_edge(agent1, 'b')
    >>> G.add_edge(agent1, 'c')
    >>> G.add_edge(agent2, 'a')
    >>> G.add_edge(agent2, 'b')
    >>> G.add_edge(agent2, 'd')
    >>> print(alloc_y_for_func) # Before function
    agent1's bundle: {b,c},  value: 110.0
    agent2's bundle: {a,b,d},  value: 100.0
    <BLANKLINE>
    >>> update_fpo_alloc_and_Gx(agent2, 'b', [agent1], alloc_y_for_func, G)
    >>> print(alloc_y_for_func) #After function
    agent1's bundle: {c},  value: 80.0
    agent2's bundle: {a,b,d},  value: 130.0
    <BLANKLINE>

    """
    index_of_agent = fpo_alloc.agents.index(curr_agent)
    fpo_alloc.map_item_to_fraction[index_of_agent][item] = 1.0
    for agent in list_of_agent_share_item:
        index_of_agent = fpo_alloc.agents.index(agent)
        remove_edge(item, agent, Gx)
        fpo_alloc.map_item_to_fraction[index_of_agent][item] = 0.0
'''
The function receives the two vertices that make up the side, which are: item and agent
And the graph.
And removes the edge from the graph. Since adding the edge to the graph is sometimes added as (u, v) and sometimes as (v, u) 
we will try to subtract in both arrangements. For sure one of the attempts will throw an error so it's okay to skip an ascent.
'''
def remove_edge(item: str, agent: AdditiveAgent, Gx: bipartite) -> None:
    """
    >>> agent1 = AdditiveAgent({"a": 100, "b": 10, "c": 50}, name="agent1")
    >>> agent2 = AdditiveAgent({"a": 20, "b": 20, "c": 40}, name="agent2")
    >>> G = nx.Graph()
    >>> G.add_node(agent1)
    >>> G.add_node(agent2)
    >>> G.add_node('a')
    >>> G.add_node('b')
    >>> G.add_node('c')
    >>> G.add_node('d')
    >>> G.add_edge(agent1, 'b')
    >>> G.add_edge(agent1, 'c')
    >>> G.add_edge(agent2, 'a')
    >>> G.add_edge(agent2, 'b')
    >>> G.add_edge(agent2, 'd')
    >>> print([(agent.name(),item) for (agent,item) in G.edges()]) # Before function
    [('agent1', 'b'), ('agent1', 'c'), ('agent2', 'a'), ('agent2', 'b'), ('agent2', 'd')]
    >>> remove_edge(agent2, 'b', G)
    >>> print([(agent.name(),item) for (agent,item) in G.edges()]) # After function
    [('agent1', 'b'), ('agent1', 'c'), ('agent2', 'a'), ('agent2', 'd')]
    """
    remove_u_v(item, agent, Gx)
    remove_u_v(agent, item, Gx)

'''
Help function for function remove_edge. this function is the one that do the action of delete the edge from the graph
'''
def remove_u_v(item: str, agent: AdditiveAgent, Gx: bipartite) -> None:
    try:
        Gx.remove_edge(item, agent)
    except nx.NetworkXError:
        pass

'''
The function gets the queue to which you will add neighbors, and a dictionary that has all the agents with whom the agent 
shares the items - meaning all his neighbors will be there.
The function adds only once the same agent.
'''
def add_neighbors_to_Q(Q: queue, dict_of_items_curr_agent_share: dict) -> None:
    """
    >>> agent1= AdditiveAgent({"a": 100, "b": 10, "c": 50, "d": 100 ,"e": 70,"f": 100, "g": 300, "h": 40, "i": 30}, name="agent1")
    >>> agent3= AdditiveAgent({"a": 10, "b": 30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": 90}, name="agent3")
    >>> d={'f': [agent1 , agent3]}
    >>> q = queue.Queue()
    >>> add_neighbors_to_Q(q, d)
    >>> print([a.name() for a in q.queue])
    ['agent1', 'agent3']
    """
    for agents in dict_of_items_curr_agent_share.values():
        for agent in agents:
            if agent not in Q.queue:
                Q.put(agent)

if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))








