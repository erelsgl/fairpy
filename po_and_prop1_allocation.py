import queue

import cvxpy
import networkx as nx
from indivisible.agents import AdditiveAgent, Bundle, List
from indivisible.allocations import Allocation, FractionalAllocation, get_items_of_agent_in_alloc, stringify_bundle
from networkx.algorithms import bipartite

#Main functions
from networkx.utils import make_str


def add_neighbors_to_Q(Q, dict_of_items_curr_agent_share):
    for agents in dict_of_items_curr_agent_share.values():
        for agent in agents:
            if agent not in Q.queue:
                Q.put(agent)


def find_po_and_prop1_allocation(Gx: nx, fpo_alloc: FractionalAllocation, items: Bundle) -> Allocation:
    """
    # >>> agent1= AdditiveAgent({"a": 100, "b": 10, "c": 50}, name="agent1")
    # >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": 40}, name="agent2")
    # >>> agent3= AdditiveAgent({"a": 10, "b": 30, "c": 30}, name="agent3")
    # >>> G = nx.Graph()
    # >>> G.add_node('agent1')
    # >>> G.add_node('agent2')
    # >>> G.add_node('agent3')
    # >>> G.add_node('a')
    # >>> G.add_node('b')
    # >>> G.add_node('c')
    # >>> G.add_edge(agent1,'a')
    # >>> G.add_edge(agent2,'a')
    # >>> G.add_edge(agent1,'b')
    # >>> G.add_edge(agent2,'b')
    # >>> G.add_edge(agent3,'c')
    # >>> items_for_func = {'a','b','c'}
    # >>> list_of_agents_for_func = [agent1, agent2, agent3]
    # >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':1/3,'b':1/3,'c':1/3},{'a':1/3,'b':1/3,'c':1/3},{'a':1/3,'b':1/3,'c':1/3}])
    # >>> find_po_and_prop1_allocation(G,alloc_y_for_func,items_for_func)
    """
    Q = queue.Queue()
    while Gx.number_of_edges() > len(items):
        agent = find_agent_sharing_item(Gx, items)
        Q.put(agent)
        while len(Q.queue) != 0:
            curr_agent = Q.get(0)
            dict_of_items_curr_agent_share = get_dict_of_items_curr_agent_share(curr_agent, fpo_alloc)
            add_neighbors_to_Q(Q, dict_of_items_curr_agent_share)
            if dict_of_items_curr_agent_share != {}:
                for item, agents in dict_of_items_curr_agent_share.items():
                    if curr_agent.map_good_to_value[item] > 0:
                        update_fpo_alloc_and_Gx(curr_agent, item, agents, fpo_alloc, Gx)
                    else:
                        other_agent = agents[0]
                        agents.append(curr_agent)
                        update_fpo_alloc_and_Gx(other_agent, item, agents, fpo_alloc, Gx)
    # result = FractionalAllocation_to_Allocation(fpo_alloc)
    return fpo_alloc


#-----------------Help functions---------------------
def init_graph(agents: List[AdditiveAgent], items: Bundle, Gx: bipartite, alloc: FractionalAllocation) -> None:
    init_nodes(agents, items, Gx)
    init_edges(alloc, Gx)

def init_nodes(agents: List[AdditiveAgent], items: Bundle, Gx: bipartite) -> None:
    """
    >>> agent1_for_func = AdditiveAgent({"x": 1, "y": 2, "z": 4}, name="agent1")
    >>> list_of_agents_for_func = [agent1_for_func]
    >>> items_for_func ={'x','y','z'}
    >>> G = nx.Graph()
    >>> init_nodes(list_of_agents_for_func, items_for_func,G )
    >>> print(G.nodes())
    ['agent1', 'x', 'y', 'z']

    >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 300, "g": -300, "h": -40, "i": 30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 300, "h": 80, "i": 90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": -30, "c": 30, "d": 40 ,"e": 180,"f": 300, "g": 30, "h": 20, "i": -90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": -200, "b": 40, "c": -20, "d": 80 ,"e": -300,"f": 300, "g": 300, "h": 60, "i": -180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": 100, "g": 300, "h": -120, "i": 180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> G = nx.Graph()
    >>> init_nodes(list_of_agents_for_func, items_for_func,G )
    >>> print(G.nodes())
    ['agent1', 'agent2', 'agent3', 'agent4', 'agent5', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    """
    part0 = []
    for agent in agents:
        part0.append(agent.name())

    Gx.add_nodes_from(part0, bipartite=0)
    Gx.add_nodes_from(sorted(items), bipartite=1)

#how to stop Networkx from changing the order of nodes from (u,v) to (v,u)?
def init_edges(alloc: FractionalAllocation, Gx: bipartite) -> None:
    """
    >>> agent1_for_func = AdditiveAgent({"x": 1, "y": 2, "z": 4}, name="agent1")
    >>> list_of_agents_for_func = [agent1_for_func]
    >>> items_for_func ={'x','y','z'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'x':1,'y':1, 'z':1}])
    >>> G = nx.Graph()
    >>> init_edges(alloc_y_for_func, G)
    >>> print(G.edges())
    [('agent1', 'x'), ('agent1', 'y'), ('agent1', 'z')]

    >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 100, "g": -300, "h": -40, "i": 30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 30, "h": 80, "i": 90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": -30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": -90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": -200, "b": 40, "c": -20, "d": 80 ,"e": -300,"f": 100, "g": 30, "h": 60, "i": -180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": -100, "g": 300, "h": -120, "i": 180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.2,'b':0.7,'c':0,'d':0.2,'e':0.9,'f':0.5,'g':0,'h':0.2,'i':0.4},{'a':0.4,'b':0.2,'c':0,'d':0.2,'e':0,'f':0,'g':0.8,'h':0.3,'i':0.1},{'a':0.1,'b':0.1,'c':0.6,'d':0.4,'e':0,'f':0,'g':0.1,'h':0.2,'i':0.4},{'a':0.1,'b':0,'c':0.2,'d':0.1,'e':0.1,'f':0,'g':0.1,'h':0.3,'i':0},{'a':0.2,'b':0,'c':0.2,'d':0.1,'e':0,'f':0.5,'g':0,'h':0,'i':0.1}])
    >>> G = nx.Graph()
    >>> init_edges(alloc_y_for_func, G)
    >>> print(G.edges())
    [('agent1', 'a'), ('agent1', 'b'), ('agent1', 'd'), ('agent1', 'e'), ('agent1', 'f'), ('agent1', 'h'), ('agent1', 'i'), ('a', 'agent2'), ('a', 'agent3'), ('a', 'agent4'), ('a', 'agent5'), ('b', 'agent2'), ('b', 'agent3'), ('d', 'agent2'), ('d', 'agent3'), ('d', 'agent4'), ('d', 'agent5'), ('e', 'agent4'), ('f', 'agent5'), ('h', 'agent2'), ('h', 'agent3'), ('h', 'agent4'), ('i', 'agent2'), ('i', 'agent3'), ('i', 'agent5'), ('agent2', 'g'), ('g', 'agent3'), ('g', 'agent4'), ('agent3', 'c'), ('c', 'agent4'), ('c', 'agent5')]
    """
    for a, d in zip(alloc.agents, alloc.map_item_to_fraction):
        items_of_agent = get_items_of_agent_in_alloc(d)
        for item in items_of_agent:
            Gx.add_edge(a.name(), item)


def find_agent_sharing_item(Gx: bipartite, items: Bundle) -> str:
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
    >>> find_agent_sharing_item(G,items_for_func)
    agent1 is an agent with additive valuations: a=100 b=10 c=50
    """
    for i in items:
        neighbors_of_i = [n for n in Gx.neighbors(i)]
        if len(neighbors_of_i) > 1:
            return neighbors_of_i[0]

def get_how_many_parts_for_item(fpo_alloc, items):
    list_of_parts_for_item = [0]*len(items)
    for i, agent in enumerate(fpo_alloc.agents):
        for j, item in enumerate(fpo_alloc.map_item_to_fraction[i].keys()):
            if agent.map_good_to_value[item] > 0:
                list_of_parts_for_item[j] += 1
    return list_of_parts_for_item


def get_dict_of_items_curr_agent_share(curr_agent, fpo_alloc):
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

def update_fpo_alloc_and_Gx(curr_agent, item, list_of_agent_share_item, fpo_alloc, Gx):
    index_of_agent = fpo_alloc.agents.index(curr_agent)
    fpo_alloc.map_item_to_fraction[index_of_agent][item] = 1.0
    for agent in list_of_agent_share_item:
        index_of_agent = fpo_alloc.agents.index(agent)
        remove_edge(item, agent, Gx)
        fpo_alloc.map_item_to_fraction[index_of_agent][item] = 0.0

def remove_edge(item, name, Gx):
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
    >>> remove_edge(agent2, 'b', G)
    """

    remove_u_v(item, name, Gx)
    remove_v_u(item, name, Gx)

def remove_u_v(item, name, Gx):
    try:
        Gx.remove_edge(item, name)
    except nx.NetworkXError:
        pass

def remove_v_u(item, name, Gx):
    try:
        Gx.remove_edge(name, item)
    except nx.NetworkXError:
        pass


def make_values_int(d):
    for key,val in d.items():
        d[key] = int(val)


def make_items_str(list_of_items):
    result = ""
    for item in list_of_items:
        result += item
    return result


def FractionalAllocation_to_Allocation(fpo_alloc: FractionalAllocation) -> Allocation:
    """
    >>> agent1 = AdditiveAgent({"a": 100, "b": 10, "c": 50}, name="agent1")
    >>> agent2 = AdditiveAgent({"a": 20, "b": 20, "c": 40}, name="agent2")
    >>> items_for_func = {'a', 'b', 'c', 'd'}
    >>> list_of_agents_for_func = [agent1, agent2]
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.0,'b':1.0,'c':1.0,'d':0.0},{'a':1.0,'b':0.0,'c':0.0,'d':1.0}])
    >>> alloc = FractionalAllocation_to_Allocation(alloc_y_for_func)
    >>> print(alloc)
    """
    list_of_items = []
    for i,d in enumerate(fpo_alloc.map_item_to_fraction):
        make_values_int(d)
        list_of_items.append(make_items_str(get_items_of_agent_in_alloc(d)))
    allocation = Allocation(fpo_alloc.agents, list_of_items)
    return allocation

if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    # agent1 = AdditiveAgent({"a": 100, "b": 10, "c": 50}, name="agent1")
    # agent2 = AdditiveAgent({"a": 20, "b": 20, "c": 40}, name="agent2")
    # agent3 = AdditiveAgent({"a": 10, "b": 30, "c": 30}, name="agent3")
    # G = nx.Graph()
    # G.add_node(agent1)
    # G.add_node(agent2)
    # # G.add_node('agent3')
    # G.add_node('a')
    # G.add_node('b')
    # G.add_node('c')
    # G.add_node('d')
    # G.add_edge(agent1, 'b')
    # G.add_edge(agent1, 'c')
    # G.add_edge(agent2, 'a')
    # G.add_edge(agent2, 'b')
    # G.add_edge(agent2, 'd')
    # items_for_func = {'a', 'b', 'c', 'd'}
    # list_of_agents_for_func = [agent1, agent2]
    # alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.0,'b':0.5,'c':1.0,'d':0.0},{'a':1.0,'b':0.5,'c':0.0,'d':1.0}])
    # alloc = find_po_and_prop1_allocation(G,alloc_y_for_func,items_for_func)
    # print(alloc)
    # agent1 = AdditiveAgent({"a": 100, "b": 10, "c": 50}, name="agent1")
    # agent2 = AdditiveAgent({"a": 20, "b": 20, "c": 40}, name="agent2")
    # items_for_func = {'a', 'b', 'c', 'd'}
    # list_of_agents_for_func = [agent1, agent2]
    # alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.0,'b':1.0,'c':1.0,'d':0.0},{'a':1.0,'b':0.0,'c':0.0,'d':1.0}])
    # alloc = FractionalAllocation_to_Allocation(alloc_y_for_func)
    # print(alloc)






