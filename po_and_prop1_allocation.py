import cvxpy
import networkx as nx
from indivisible.agents import AdditiveAgent, Bundle, List
from indivisible.allocations import Allocation, FractionalAllocation
from networkx.algorithms import bipartite, find_cycle

#Main functions

'''
This function receives a proportional allocation and returns an allocation that is fpo, meaning that the same allocation 
has no Paparto fractional improvement.
'''
def find_fpo_allocation(agents: List[AdditiveAgent], items: Bundle, alloc_y: FractionalAllocation) -> (bipartite, FractionalAllocation):
    """
    # First example:
    Case 1: Only one player(must get everything),Items with positive utility.
    >>> agent1_for_func = AdditiveAgent({"x": 1, "y": 2, "z": 4}, name="agent1")
    >>> list_of_agents_for_func = [agent1_for_func]
    >>> items_for_func ={'x','y','z'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'x':1,'y':1, 'z':1}])
    >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func,alloc_y_for_func)
    >>> print(Gx.edges())
    [('agent1', 'x'), ('agent1', 'y'), ('agent1', 'z')]
    >>> print(Gx.nodes())
    ['agent1', 'x', 'y', 'z']
    >>> print(alloc)
    agent1's bundle: {x,y,z},  value: 7

    Case 2: Only one player(must get everything),Items with negative utility.
    >>> agent1_for_func = AdditiveAgent({"x": -1, "y": -2, "z": -4}, name="agent1")
    >>> list_of_agents_for_func = [agent1_for_func]
    >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func,alloc_y_for_func)
    >>> print(Gx.edges())
    [('agent1', 'x'), ('agent1', 'y'), ('agent1', 'z')]
    >>> print(Gx.nodes())
    ['agent1', 'x', 'y', 'z']
    >>> print(alloc)
    agent1's bundle: {x,y,z},  value: -7

    Case 3: Only one player(must get everything),Items with negative and positive utilitys.
    >>> agent1_for_func = AdditiveAgent({"x": -1, "y": 2, "z": -4}, name="agent1")
    >>> list_of_agents_for_func = [agent1_for_func]
    >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func,alloc_y_for_func)
    >>> print(Gx.edges())
    [('agent1', 'x'), ('agent1', 'y'), ('agent1', 'z')]
    >>> print(Gx.nodes())
    ['agent1', 'x', 'y', 'z']
    >>> print(alloc)
    agent1's bundle: {x,y,z},  value: -3

    Second example:
    Case 1: original y allocation that is already fpo - there is no Pareto improvement so the output will be equal to the input.Items with positive utility.
    (example 5 in the second part of the work)
    >>> agent1= AdditiveAgent({"a": 100, "b": 10, "c": 50, "d": 100 ,"e": 70,"f": 100, "g": 300, "h": 40, "i": 30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": 40, "d": 90 ,"e": 90,"f": 100, "g": 30, "h": 80, "i": 90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": 30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": 90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": 200, "b": 40, "c": 20, "d": 80 ,"e": 300,"f": 100, "g": 30, "h": 60, "i": 180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": 100, "g": 300, "h": 120, "i": 180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0,'b':0,'c':1,'d':1,'e':0,'f':0.2,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0.8,'f':0.4,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0.2,'g':1,'h':0,'i':0},{'a':1,'b':0,'c':0,'d':0,'e':0.2,'f':0,'g':0,'h':0,'i':0},{'a':0,'b':1,'c':0,'d':0,'e':0,'f':0.2,'g':0,'h':1,'i':1}])
    >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func, alloc_y_for_func)
    >>> print(Gx.edges())
    [ ('agent1', 'c'), ('agent1', 'd'), ('agent1', 'f'), ('agent2', 'e'), ('agent2', 'f'), ('agent3', 'g'), ('agent3', 'f'), ('agent4', 'a'), ('agent4', 'e'), ('agent5', 'b'), ('agent5', 'f'), ('agent5', 'h'), ('agent5', 'i')]
    >>> print(Gx.nodes())
    ['agent1', 'agent1', 'agent3', 'agent4', 'agent5', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    >>> print(alloc)
    agent1's bundle: {c,d,f},  value: 170.0
    agent2's bundle: {e,f},  value: 112.0
    agent3's bundle: {f,g},  value: 320.0
    agent4's bundle: {a,e},  value: 260.0
    agent5's bundle: {b,f,h,i},  value: 370.0

    Case 2: original y allocation that is already fpo - there is no Pareto improvement so the output will be equal to the input.Items with negative utility.
    (example 4 in the second part of the work)
    >>> agent1= AdditiveAgent({"a": -100, "b": -10, "c": -50, "d":-100 ,"e": -70,"f": -100, "g": -200, "h": -40, "i": -30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": -20, "b": -20, "c": -40, "d": -90 ,"e": -90,"f": -100, "g": -100, "h": -80, "i": -90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": -10, "b": -30, "c": -30, "d": -40 ,"e": -180,"f": -100, "g": -200, "h": -20, "i": -90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": -200, "b": -40, "c": -20, "d": -80 ,"e": -300,"f": -100, "g": -100, "h": -60, "i": -180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": -50, "b": -50, "c": -10, "d": -60 ,"e": -90,"f": -100, "g": -200, "h": -120, "i": -180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0,'b':1,'c':0,'d':0,'e':1,'f':0.2,'g':0,'h':0,'i':1},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0.2,'g':0,'h':0,'i':0},{'a':1,'b':0,'c':0,'d':1,'e':0,'f':0.2,'g':0,'h':1,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0.2,'g':1,'h':0,'i':0},{'a':0,'b':0,'c':1,'d':0,'e':0,'f':0.2,'g':0,'h':0,'i':0}])
    >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func, alloc_y_for_func)
    >>> print(Gx.edges())
    [('agent1', 'b'), ('agent1', 'e'), ('agent1', 'f'), ('agent1', 'i'), ('agent2', 'f'), ('agent3', 'a'), ('agent3', 'd'), ('agent3', 'f'), ('agent3', 'h'), ('agent4', 'f'), ('agent4', 'g'), ('agent5', 'c'), ('agent5', 'f')]
    >>> print(Gx.nodes())
    ['agent1', 'agent1', 'agent3', 'agent4', 'agent5', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    >>> print(alloc)
    agent1's bundle: {b,e,f,i},  value: -130.0
    agent2's bundle: {f},  value: -20.0
    agent3's bundle: {a,d,f,h},  value: -90.0
    agent4's bundle: {f,g},  value: -120.0
    agent5's bundle: {c,f},  value: -30.0

    Case 3: original y allocation that is already fpo - there is no Pareto improvement so the output will be equal to the input.Items with negative and positive utilitys.
    (example 6 in the second part of the work)
    >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 300, "g": -300, "h": -40, "i": 30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 300, "h": 80, "i": 90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": -30, "c": 30, "d": 40 ,"e": 180,"f": 300, "g": 30, "h": 20, "i": -90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": -200, "b": 40, "c": -20, "d": 80 ,"e": -300,"f": 300, "g": 300, "h": 60, "i": -180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": 100, "g": 300, "h": -120, "i": 180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0,'b':0,'c':1,'d':0,'e':0,'f':0.4,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':1,'e':0,'f':0,'g':0.5,'h':1,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':1,'f':0.4,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0.5,'h':0,'i':0},{'a':1,'b':1,'c':0,'d':0,'e':0,'f':0.2,'g':0,'h':0,'i':1}])
    >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func, alloc_y_for_func)
    >>> print(Gx.edges())
    [('agent1', 'c'), ('agent1', 'f'), ('agent2', 'd'), ('agent2', 'g'), ('agent2', 'h'), ('agent3', 'e'), ('agent3', 'f'), ('agent4', 'g'), ('agent5', 'c'), ('agent5', 'a'), ('agent5', 'b'), ('agent5', 'f'), ('agent5', 'i')]
    >>> print(Gx.nodes())
    ['agent1', 'agent1', 'agent3', 'agent4', 'agent5', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    >>> print(alloc)
    agent1's bundle: {c,f},  value: 170.0
    agent2's bundle: {d,g,h},  value: 320.0
    agent3's bundle: {e,f},  value: 300.0
    agent4's bundle: {g},  value: 150.0
    agent5's bundle: {a,b,f,i},  value: 300.0

    Third example: A situation where there is only one fpo division
    >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 300, "g": -300, "h": -40, "i": -30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": -20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 300, "h": 80, "i": 90}, name="agent2")
    >>> list_of_agents_for_func = [agent1, agent2]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.5,'b':0.5,'c':0.5,'d':0.5,'e':0.5,'f':0.5,'g':0.5,'h':0.5,'i':0.5}])
    >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func, alloc_y_for_func)
    >>> print(Gx.edges())
    [('agent1', 'c'), ('agent1', 'f'), ('agent2', 'd'), ('agent2', 'g'), ('agent2', 'h'), ('agent3', 'e'), ('agent3', 'f'), ('agent4', 'g'), ('agent5', 'c'), ('agent5', 'a'), ('agent5', 'b'), ('agent5', 'f'), ('agent5', 'i')]
    >>> print(Gx.nodes())
    ['agent1', 'agent1', 'agent3', 'agent4', 'agent5', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    >>> print(alloc)
    agent1's bundle: {b,c,e,f},  value: 430.0
    agent2's bundle: {a,d,g,h,i},  value: 580.0

    Fourth example: A general situation, in which the new division is indeed a pareto improvement of the original division
    (example 7 in the second part of the work)
    >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 100, "g": -300, "h": -40, "i": 30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 30, "h": 80, "i": 90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": -30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": -90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": -200, "b": 40, "c": -20, "d": 80 ,"e": -300,"f": 100, "g": 30, "h": 60, "i": -180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": -100, "g": 300, "h": -120, "i": 180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.2,'b':0.7,'c':0,'d':0.2,'e':0.9,'f':0.5,'g':0,'h':0.2,'i':0.4},{'a':0.4,'b':0.2,'c':0,'d':0.2,'e':0,'f':0,'g':0.8,'h':0.3,'i':0.1},{'a':0.1,'b':0.1,'c':0.6,'d':0.4,'e':0,'f':0,'g':0.1,'h':0.2,'i':0.4},{'a':0.1,'b':0,'c':0.2,'d':0.1,'e':0.1,'f':0,'g':0.1,'h':0.3,'i':0},{'a':0.2,'b':0,'c':0.2,'d':0.1,'e':0,'f':0.5,'g':0,'h':0,'i':0.1}])
    >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func, alloc_y_for_func)
    >>> print(Gx.edges())
    [('agent1', 'b'), ('agent1', 'e'), ('agent1', 'f'), ('agent1', 'i'), ('agent2', 'd'), ('agent2', 'h'), ('agent3', 'c'), ('agent3', 'g'), ('agent5', 'a'), ('agent5', 'i')]
    >>> print(Gx.nodes())
    ['agent1', 'agent1', 'agent3', 'agent4', 'agent5', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    >>> print(alloc)
    agent1's bundle: {b,e,f,i},  value: 192.0
    agent2's bundle: {d,h},  value: 170.0
    agent3's bundle: {c,g},  value: 330.0
    agent4's bundle: {},  value: 0.0
    agent5's bundle: {a,i},  value: 158.0

    """
    b = nx.Graph()
    return (b, None)

'''
This function gets a list of agents, all the items and the rights of each agent on each item.
And it returns a whole allocation which is PO and PROP1.
'''
def find_po_and_prop1_allocation(agents: List[AdditiveAgent], items: Bundle, rights_b: List[dict]) -> Allocation:
    """
    # First example:
    Case 1: Only one player(must get everything),Items with positive utility.
    >>> agent1_for_func = AdditiveAgent({"x": 1, "y": 2, "z": 4}, name="agent1")
    >>> list_of_agents_for_func = [agent1_for_func]
    >>> items_for_func ={'x','y','z'}
    >>> rights_b_for_func = [{'x':1,'y':1, 'z':1}]
    >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    >>> print(alloc)
    agent1's bundle: {x,y,z},  value: 7

    Case 2: Only one player(must get everything),Items with negative utility.
    >>> agent1_for_func = AdditiveAgent({"x": -1, "y": -2, "z": -4}, name="agent1")
    >>> list_of_agents_for_func = [agent1_for_func]
    >>> items_for_func ={'x','y','z'}
    >>> rights_b_for_func = [{'x':1,'y':1, 'z':1}]
    >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    >>> print(alloc)
    agent1's bundle: {x,y,z},  value: -7

    Case 3: Only one player(must get everything),Items with negative and positive utilitys.
    >>> agent1_for_func = AdditiveAgent({"x": -1, "y": 2, "z": -4}, name="agent1")
    >>> list_of_agents_for_func = [agent1_for_func]
    >>> items_for_func ={'x','y','z'}
    >>> rights_b_for_func = [{'x':1,'y':1, 'z':1}]
    >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    >>> print(alloc)
    agent1's bundle: {x,y,z},  value: -3

    Second example:
    Case 1:
    (example 5 in the second part of the work)
    >>> agent1= AdditiveAgent({"a": 100, "b": 10, "c": 50, "d": 100 ,"e": 70,"f": 100, "g": 300, "h": 40, "i": 30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": 40, "d": 90 ,"e": 90,"f": 100, "g": 30, "h": 80, "i": 90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": 30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": 90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": 200, "b": 40, "c": 20, "d": 80 ,"e": 300,"f": 100, "g": 30, "h": 60, "i": 180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": 100, "g": 300, "h": 120, "i": 180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> rights_b_for_func = [{'a':0,'b':0,'c':1,'d':1,'e':0,'f':0.2,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0.8,'f':0.4,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0.2,'g':1,'h':0,'i':0},{'a':1,'b':0,'c':0,'d':0,'e':0.2,'f':0,'g':0,'h':0,'i':0},{'a':0,'b':1,'c':0,'d':0,'e':0,'f':0.2,'g':0,'h':1,'i':1}]
    >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    >>> print(alloc)
    agent1's bundle: {c,d,f},  value: 250.0
    agent2's bundle: {e},  value: 90.0
    agent3's bundle: {g},  value: 300.0
    agent4's bundle: {a},  value: 200.0
    agent5's bundle: {b,h,i},  value: 350.0

     Case 2: original y allocation that is already fpo - there is no Pareto improvement so the output will be equal to the input.Items with negative utility.
     (example 4 in the second part of the work)
    >>> agent1= AdditiveAgent({"a": -100, "b": -10, "c": -50, "d":-100 ,"e": -70,"f": -100, "g": -200, "h": -40, "i": -30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": -20, "b": -20, "c": -40, "d": -90 ,"e": -90,"f": -100, "g": -100, "h": -80, "i": -90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": -10, "b": -30, "c": -30, "d": -40 ,"e": -180,"f": -100, "g": -200, "h": -20, "i": -90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": -200, "b": -40, "c": -20, "d": -80 ,"e": -300,"f": -100, "g": -100, "h": -60, "i": -180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": -50, "b": -50, "c": -10, "d": -60 ,"e": -90,"f": -100, "g": -200, "h": -120, "i": -180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> rights_b_for_func = [{'a':0,'b':1,'c':0,'d':0,'e':1,'f':0.2,'g':0,'h':0,'i':1},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0.2,'g':0,'h':0,'i':0},{'a':1,'b':0,'c':0,'d':1,'e':0,'f':0.2,'g':0,'h':1,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0.2,'g':1,'h':0,'i':0},{'a':0,'b':0,'c':1,'d':0,'e':0,'f':0.2,'g':0,'h':0,'i':0}]
    >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    >>> print(alloc)
    agent1's bundle: {b,e,f,i},  value: -210.0
    agent2's bundle: {},  value: 0.0
    agent3's bundle: {a,d,h},  value: -70.0
    agent4's bundle: {g},  value: -100.0
    agent5's bundle: {c},  value: -30.0

    Case 3: original y allocation that is already fpo - there is no Pareto improvement so the output will be equal to the input.Items with negative utility.
    (example 6 in the second part of the work)
    >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 300, "g": -300, "h": -40, "i": 30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 300, "h": 80, "i": 90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": -30, "c": 30, "d": 40 ,"e": 180,"f": 300, "g": 30, "h": 20, "i": -90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": -200, "b": 40, "c": -20, "d": 80 ,"e": -300,"f": 300, "g": 300, "h": 60, "i": -180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": 100, "g": 300, "h": -120, "i": 180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> rights_b_for_func = [{'a':0,'b':0,'c':1,'d':0,'e':0,'f':0.4,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':1,'e':0,'f':0,'g':0.5,'h':1,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':1,'f':0.4,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0.5,'h':0,'i':0},{'a':1,'b':1,'c':0,'d':0,'e':0,'f':0.2,'g':0,'h':0,'i':1}]
    >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    >>> print(alloc)
    agent1's bundle: {c,f},  value: 350.0
    agent2's bundle: {d,g,h},  value: 470.0
    agent3's bundle: {e},  value: 180.0
    agent4's bundle: {},  value: 0.0
    agent5's bundle: {a,b,i},  value: 280.0

    Third example: A situation where there is only one fpo division
    >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 300, "g": -300, "h": -40, "i": -30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": -20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 300, "h": 80, "i": 90}, name="agent2")
    >>> list_of_agents_for_func = [agent1, agent2]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> rights_b_for_func =[{'a':0.5,'b':0.5,'c':0.5,'d':0.5,'e':0.5,'f':0.5,'g':0.5,'h':0.5,'i':0.5}]
    >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    >>> print(alloc)
    agent1's bundle: {b,c,e,f},  value: 430.0
    agent2's bundle: {a,d,g,h,i},  value: 580.0

    Fourth example: A general situation, in which the new division is indeed a pareto improvement of the original division
    (example 7 in the second part of the work)
    >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 100, "g": -300, "h": -40, "i": 30}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 30, "h": 80, "i": 90}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": -30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": -90}, name="agent3")
    >>> agent4= AdditiveAgent({"a": -200, "b": 40, "c": -20, "d": 80 ,"e": -300,"f": 100, "g": 30, "h": 60, "i": -180}, name="agent4")
    >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": -100, "g": 300, "h": -120, "i": 180}, name="agent5")
    >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    >>> rights_b_for_func = [{'a':0.2,'b':0.7,'c':0,'d':0.2,'e':0.9,'f':0.5,'g':0,'h':0.2,'i':0.4},{'a':0.4,'b':0.2,'c':0,'d':0.2,'e':0,'f':0,'g':0.8,'h':0.3,'i':0.1},{'a':0.1,'b':0.1,'c':0.6,'d':0.4,'e':0,'f':0,'g':0.1,'h':0.2,'i':0.4},{'a':0.1,'b':0,'c':0.2,'d':0.1,'e':0.1,'f':0,'g':0.1,'h':0.3,'i':0},{'a':0.2,'b':0,'c':0.2,'d':0.1,'e':0,'f':0.5,'g':0,'h':0,'i':0.1}]
    >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    >>> print(alloc)
    agent1's bundle: {b,e,f,i},  value: 210.0
    agent2's bundle: {d,h},  value: 170.0
    agent3's bundle: {c,g},  value: 330.0
    agent4's bundle: {},  value: 0.0
    agent5's bundle: {a},  value: 50.0
    """
    alloc_y = FractionalAllocation(agents, rights_b)
    (Gx, fpo_alloc) = find_fpo_allocation(agents, items, alloc_y)
    final_alloc = find_po_and_prop1_allocation(Gx, fpo_alloc)
    return final_alloc


#-----------------Help functions---------------------
def init_graph() -> bipartite:
    pass

def find_po_and_prop1_allocation(Gx: bipartite, fpo_alloc: FractionalAllocation) -> Allocation:
    pass

def FractionalAllocation_to_Allocation(fpo_alloc: FractionalAllocation) -> Allocation:
    pass

if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))









