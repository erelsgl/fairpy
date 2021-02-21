import cvxpy
import networkx as nx
from indivisible.agents import AdditiveAgent, Bundle, List
from indivisible.allocations import Allocation, FractionalAllocation, get_items_of_agent_in_alloc
from networkx.algorithms import bipartite, find_cycle, cycle_basis, simple_cycles

#Main functions
'''
This function gets a list of agents, all the items and the rights of each agent on each item.
And it returns a whole allocation which is PO and PROP1.
'''
# def find_po_and_prop1_allocation(agents: List[AdditiveAgent], items: Bundle, rights_b: List[dict]) -> Allocation:
    # """
    # # First example:
    # Case 1: Only one player(must get everything),Items with positive utility.
    # >>> agent1_for_func = AdditiveAgent({"x": 1, "y": 2, "z": 4}, name="agent1")
    # >>> list_of_agents_for_func = [agent1_for_func]
    # >>> items_for_func ={'x','y','z'}
    # >>> rights_b_for_func = [{'x':1,'y':1, 'z':1}]
    # >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    # >>> print(alloc)
    # agent1's bundle: {x,y,z},  value: 7
    #
    # Case 2: Only one player(must get everything),Items with negative utility.
    # >>> agent1_for_func = AdditiveAgent({"x": -1, "y": -2, "z": -4}, name="agent1")
    # >>> list_of_agents_for_func = [agent1_for_func]
    # >>> items_for_func ={'x','y','z'}
    # >>> rights_b_for_func = [{'x':1,'y':1, 'z':1}]
    # >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    # >>> print(alloc)
    # agent1's bundle: {x,y,z},  value: -7
    #
    # Case 3: Only one player(must get everything),Items with negative and positive utilitys.
    # >>> agent1_for_func = AdditiveAgent({"x": -1, "y": 2, "z": -4}, name="agent1")
    # >>> list_of_agents_for_func = [agent1_for_func]
    # >>> items_for_func ={'x','y','z'}
    # >>> rights_b_for_func = [{'x':1,'y':1, 'z':1}]
    # >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    # >>> print(alloc)
    # agent1's bundle: {x,y,z},  value: -3
    #
    # Second example:
    # Case 1:
    # (example 5 in the second part of the work)
    # >>> agent1= AdditiveAgent({"a": 100, "b": 10, "c": 50, "d": 100 ,"e": 70,"f": 100, "g": 300, "h": 40, "i": 30}, name="agent1")
    # >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": 40, "d": 90 ,"e": 90,"f": 100, "g": 30, "h": 80, "i": 90}, name="agent2")
    # >>> agent3= AdditiveAgent({"a": 10, "b": 30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": 90}, name="agent3")
    # >>> agent4= AdditiveAgent({"a": 200, "b": 40, "c": 20, "d": 80 ,"e": 300,"f": 100, "g": 30, "h": 60, "i": 180}, name="agent4")
    # >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": 100, "g": 300, "h": 120, "i": 180}, name="agent5")
    # >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    # >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    # >>> rights_b_for_func = [{'a':0,'b':0,'c':1,'d':1,'e':0,'f':0.2,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0.8,'f':0.4,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0.2,'g':1,'h':0,'i':0},{'a':1,'b':0,'c':0,'d':0,'e':0.2,'f':0,'g':0,'h':0,'i':0},{'a':0,'b':1,'c':0,'d':0,'e':0,'f':0.2,'g':0,'h':1,'i':1}]
    # >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    # >>> print(alloc)
    # agent1's bundle: {c,d,f},  value: 250.0
    # agent2's bundle: {e},  value: 90.0
    # agent3's bundle: {g},  value: 300.0
    # agent4's bundle: {a},  value: 200.0
    # agent5's bundle: {b,h,i},  value: 350.0
    #
    #  Case 2: original y allocation that is already fpo - there is no Pareto improvement so the output will be equal to the input.Items with negative utility.
    #  (example 4 in the second part of the work)
    # >>> agent1= AdditiveAgent({"a": -100, "b": -10, "c": -50, "d":-100 ,"e": -70,"f": -100, "g": -200, "h": -40, "i": -30}, name="agent1")
    # >>> agent2= AdditiveAgent({"a": -20, "b": -20, "c": -40, "d": -90 ,"e": -90,"f": -100, "g": -100, "h": -80, "i": -90}, name="agent2")
    # >>> agent3= AdditiveAgent({"a": -10, "b": -30, "c": -30, "d": -40 ,"e": -180,"f": -100, "g": -200, "h": -20, "i": -90}, name="agent3")
    # >>> agent4= AdditiveAgent({"a": -200, "b": -40, "c": -20, "d": -80 ,"e": -300,"f": -100, "g": -100, "h": -60, "i": -180}, name="agent4")
    # >>> agent5= AdditiveAgent({"a": -50, "b": -50, "c": -10, "d": -60 ,"e": -90,"f": -100, "g": -200, "h": -120, "i": -180}, name="agent5")
    # >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    # >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    # >>> rights_b_for_func = [{'a':0,'b':1,'c':0,'d':0,'e':1,'f':0.2,'g':0,'h':0,'i':1},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0.2,'g':0,'h':0,'i':0},{'a':1,'b':0,'c':0,'d':1,'e':0,'f':0.2,'g':0,'h':1,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0.2,'g':1,'h':0,'i':0},{'a':0,'b':0,'c':1,'d':0,'e':0,'f':0.2,'g':0,'h':0,'i':0}]
    # >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    # >>> print(alloc)
    # agent1's bundle: {b,e,f,i},  value: -210.0
    # agent2's bundle: {},  value: 0.0
    # agent3's bundle: {a,d,h},  value: -70.0
    # agent4's bundle: {g},  value: -100.0
    # agent5's bundle: {c},  value: -30.0
    #
    # Case 3: original y allocation that is already fpo - there is no Pareto improvement so the output will be equal to the input.Items with negative utility.
    # (example 6 in the second part of the work)
    # >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 300, "g": -300, "h": -40, "i": 30}, name="agent1")
    # >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 300, "h": 80, "i": 90}, name="agent2")
    # >>> agent3= AdditiveAgent({"a": 10, "b": -30, "c": 30, "d": 40 ,"e": 180,"f": 300, "g": 30, "h": 20, "i": -90}, name="agent3")
    # >>> agent4= AdditiveAgent({"a": -200, "b": 40, "c": -20, "d": 80 ,"e": -300,"f": 300, "g": 300, "h": 60, "i": -180}, name="agent4")
    # >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": 100, "g": 300, "h": -120, "i": 180}, name="agent5")
    # >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    # >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    # >>> rights_b_for_func = [{'a':0,'b':0,'c':1,'d':0,'e':0,'f':0.4,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':1,'e':0,'f':0,'g':0.5,'h':1,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':1,'f':0.4,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0.5,'h':0,'i':0},{'a':1,'b':1,'c':0,'d':0,'e':0,'f':0.2,'g':0,'h':0,'i':1}]
    # >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    # >>> print(alloc)
    # agent1's bundle: {c,f},  value: 350.0
    # agent2's bundle: {d,g,h},  value: 470.0
    # agent3's bundle: {e},  value: 180.0
    # agent4's bundle: {},  value: 0.0
    # agent5's bundle: {a,b,i},  value: 280.0
    #
    # Third example: A situation where there is only one fpo division
    # >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 300, "g": -300, "h": -40, "i": -30}, name="agent1")
    # >>> agent2= AdditiveAgent({"a": 20, "b": -20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 300, "h": 80, "i": 90}, name="agent2")
    # >>> list_of_agents_for_func = [agent1, agent2]
    # >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    # >>> rights_b_for_func =[{'a':0.5,'b':0.5,'c':0.5,'d':0.5,'e':0.5,'f':0.5,'g':0.5,'h':0.5,'i':0.5}]
    # >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    # >>> print(alloc)
    # agent1's bundle: {b,c,e,f},  value: 430.0
    # agent2's bundle: {a,d,g,h,i},  value: 580.0
    #
    # Fourth example: A general situation, in which the new division is indeed a pareto improvement of the original division
    # (example 7 in the second part of the work)
    # >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 100, "g": -300, "h": -40, "i": 30}, name="agent1")
    # >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 30, "h": 80, "i": 90}, name="agent2")
    # >>> agent3= AdditiveAgent({"a": 10, "b": -30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": -90}, name="agent3")
    # >>> agent4= AdditiveAgent({"a": -200, "b": 40, "c": -20, "d": 80 ,"e": -300,"f": 100, "g": 30, "h": 60, "i": -180}, name="agent4")
    # >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": -100, "g": 300, "h": -120, "i": 180}, name="agent5")
    # >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    # >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    # >>> rights_b_for_func = [{'a':0.2,'b':0.7,'c':0,'d':0.2,'e':0.9,'f':0.5,'g':0,'h':0.2,'i':0.4},{'a':0.4,'b':0.2,'c':0,'d':0.2,'e':0,'f':0,'g':0.8,'h':0.3,'i':0.1},{'a':0.1,'b':0.1,'c':0.6,'d':0.4,'e':0,'f':0,'g':0.1,'h':0.2,'i':0.4},{'a':0.1,'b':0,'c':0.2,'d':0.1,'e':0.1,'f':0,'g':0.1,'h':0.3,'i':0},{'a':0.2,'b':0,'c':0.2,'d':0.1,'e':0,'f':0.5,'g':0,'h':0,'i':0.1}]
    # >>> alloc = find_po_and_prop1_allocation(list_of_agents_for_func,items_for_func,rights_b_for_func)
    # >>> print(alloc)
    # agent1's bundle: {b,e,f,i},  value: 210.0
    # agent2's bundle: {d,h},  value: 170.0
    # agent3's bundle: {c,g},  value: 330.0
    # agent4's bundle: {},  value: 0.0
    # agent5's bundle: {a},  value: 50.0
    # """
    # alloc_y = FractionalAllocation(agents, rights_b)
    # (Gx, fpo_alloc) = find_fpo_allocation(agents, items, alloc_y)
    # final_alloc = find_po_and_prop1_allocation(Gx, fpo_alloc, items)
    # return final_alloc

# '''
# This function receives a proportional allocation and returns an allocation that is fpo, meaning that the same allocation
# has no Paparto fractional improvement.
# '''
# def find_fpo_allocation(agents: List[AdditiveAgent], items: Bundle, alloc_y: FractionalAllocation) -> (bipartite, FractionalAllocation):
    # """
    # # First example:
    # Case 1: Only one player(must get everything),Items with positive utility.
    # >>> agent1_for_func = AdditiveAgent({"x": 1, "y": 2, "z": 4}, name="agent1")
    # >>> list_of_agents_for_func = [agent1_for_func]
    # >>> items_for_func ={'x','y','z'}
    # >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'x':1,'y':1, 'z':1}])
    # >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func,alloc_y_for_func)
    # >>> print(Gx.edges())
    # [('agent1', 'x'), ('agent1', 'y'), ('agent1', 'z')]
    # >>> print(Gx.nodes())
    # ['agent1', 'x', 'y', 'z']
    # >>> print(alloc)
    # agent1's bundle: {x,y,z},  value: 7
    #
    # Case 2: Only one player(must get everything),Items with negative utility.
    # >>> agent1_for_func = AdditiveAgent({"x": -1, "y": -2, "z": -4}, name="agent1")
    # >>> list_of_agents_for_func = [agent1_for_func]
    # >>> items_for_func ={'x','y','z'}
    # >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'x':1,'y':1, 'z':1}])
    # >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func,alloc_y_for_func)
    # >>> print(Gx.edges())
    # [('agent1', 'x'), ('agent1', 'y'), ('agent1', 'z')]
    # >>> print(Gx.nodes())
    # ['agent1', 'x', 'y', 'z']
    # >>> print(alloc)
    # agent1's bundle: {x,y,z},  value: -7
    #
    # Case 3: Only one player(must get everything),Items with negative and positive utilitys.
    # >>> agent1_for_func = AdditiveAgent({"x": -1, "y": 2, "z": -4}, name="agent1")
    # >>> list_of_agents_for_func = [agent1_for_func]
    # >>> items_for_func ={'x','y','z'}
    # >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'x':1,'y':1, 'z':1}])
    # >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func,alloc_y_for_func)
    # >>> print(Gx.edges())
    # [('agent1', 'x'), ('agent1', 'y'), ('agent1', 'z')]
    # >>> print(Gx.nodes())
    # ['agent1', 'x', 'y', 'z']
    # >>> print(alloc)
    # agent1's bundle: {x,y,z},  value: -3
    #
    # Second example:
    # Case 1: original y allocation that is already fpo - there is no Pareto improvement so the output will be equal to the input.Items with positive utility.
    # (example 5 in the second part of the work)
    # >>> agent1= AdditiveAgent({"a": 100, "b": 10, "c": 50, "d": 100 ,"e": 70,"f": 100, "g": 300, "h": 40, "i": 30}, name="agent1")
    # >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": 40, "d": 90 ,"e": 90,"f": 100, "g": 30, "h": 80, "i": 90}, name="agent2")
    # >>> agent3= AdditiveAgent({"a": 10, "b": 30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": 90}, name="agent3")
    # >>> agent4= AdditiveAgent({"a": 200, "b": 40, "c": 20, "d": 80 ,"e": 300,"f": 100, "g": 30, "h": 60, "i": 180}, name="agent4")
    # >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": 100, "g": 300, "h": 120, "i": 180}, name="agent5")
    # >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    # >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    # >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0,'b':0,'c':1,'d':1,'e':0,'f':0.2,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0.8,'f':0.4,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0.2,'g':1,'h':0,'i':0},{'a':1,'b':0,'c':0,'d':0,'e':0.2,'f':0,'g':0,'h':0,'i':0},{'a':0,'b':1,'c':0,'d':0,'e':0,'f':0.2,'g':0,'h':1,'i':1}])
    # >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func, alloc_y_for_func)
    # >>> print(Gx.edges())
    # [ ('agent1', 'c'), ('agent1', 'd'), ('agent1', 'f'), ('agent2', 'e'), ('agent2', 'f'), ('agent3', 'g'), ('agent3', 'f'), ('agent4', 'a'), ('agent4', 'e'), ('agent5', 'b'), ('agent5', 'f'), ('agent5', 'h'), ('agent5', 'i')]
    # >>> print(Gx.nodes())
    # ['agent1', 'agent2', 'agent3', 'agent4', 'agent5', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    # >>> print(alloc)
    # agent1's bundle: {c,d,f},  value: 170.0
    # agent2's bundle: {e,f},  value: 112.0
    # agent3's bundle: {f,g},  value: 320.0
    # agent4's bundle: {a,e},  value: 260.0
    # agent5's bundle: {b,f,h,i},  value: 370.0
    #
    # Case 2: original y allocation that is already fpo - there is no Pareto improvement so the output will be equal to the input.Items with negative utility.
    # (example 4 in the second part of the work)
    # >>> agent1= AdditiveAgent({"a": -100, "b": -10, "c": -50, "d":-100 ,"e": -70,"f": -100, "g": -200, "h": -40, "i": -30}, name="agent1")
    # >>> agent2= AdditiveAgent({"a": -20, "b": -20, "c": -40, "d": -90 ,"e": -90,"f": -100, "g": -100, "h": -80, "i": -90}, name="agent2")
    # >>> agent3= AdditiveAgent({"a": -10, "b": -30, "c": -30, "d": -40 ,"e": -180,"f": -100, "g": -200, "h": -20, "i": -90}, name="agent3")
    # >>> agent4= AdditiveAgent({"a": -200, "b": -40, "c": -20, "d": -80 ,"e": -300,"f": -100, "g": -100, "h": -60, "i": -180}, name="agent4")
    # >>> agent5= AdditiveAgent({"a": -50, "b": -50, "c": -10, "d": -60 ,"e": -90,"f": -100, "g": -200, "h": -120, "i": -180}, name="agent5")
    # >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    # >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    # >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0,'b':1,'c':0,'d':0,'e':1,'f':0.2,'g':0,'h':0,'i':1},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0.2,'g':0,'h':0,'i':0},{'a':1,'b':0,'c':0,'d':1,'e':0,'f':0.2,'g':0,'h':1,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0.2,'g':1,'h':0,'i':0},{'a':0,'b':0,'c':1,'d':0,'e':0,'f':0.2,'g':0,'h':0,'i':0}])
    # >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func, alloc_y_for_func)
    # >>> print(Gx.edges())
    # [('agent1', 'b'), ('agent1', 'e'), ('agent1', 'f'), ('agent1', 'i'), ('agent2', 'f'), ('agent3', 'a'), ('agent3', 'd'), ('agent3', 'f'), ('agent3', 'h'), ('agent4', 'f'), ('agent4', 'g'), ('agent5', 'c'), ('agent5', 'f')]
    # >>> print(Gx.nodes())
    # ['agent1', 'agent2', 'agent3', 'agent4', 'agent5', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    # >>> print(alloc)
    # agent1's bundle: {b,e,f,i},  value: -130.0
    # agent2's bundle: {f},  value: -20.0
    # agent3's bundle: {a,d,f,h},  value: -90.0
    # agent4's bundle: {f,g},  value: -120.0
    # agent5's bundle: {c,f},  value: -30.0
    #
    # Case 3: original y allocation that is already fpo - there is no Pareto improvement so the output will be equal to the input.Items with negative and positive utilitys.
    # (example 6 in the second part of the work)
    # >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 300, "g": -300, "h": -40, "i": 30}, name="agent1")
    # >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 300, "h": 80, "i": 90}, name="agent2")
    # >>> agent3= AdditiveAgent({"a": 10, "b": -30, "c": 30, "d": 40 ,"e": 180,"f": 300, "g": 30, "h": 20, "i": -90}, name="agent3")
    # >>> agent4= AdditiveAgent({"a": -200, "b": 40, "c": -20, "d": 80 ,"e": -300,"f": 300, "g": 300, "h": 60, "i": -180}, name="agent4")
    # >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": 100, "g": 300, "h": -120, "i": 180}, name="agent5")
    # >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    # >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    # >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0,'b':0,'c':1,'d':0,'e':0,'f':0.4,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':1,'e':0,'f':0,'g':0.5,'h':1,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':1,'f':0.4,'g':0,'h':0,'i':0},{'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0.5,'h':0,'i':0},{'a':1,'b':1,'c':0,'d':0,'e':0,'f':0.2,'g':0,'h':0,'i':1}])
    # >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func, alloc_y_for_func)
    # >>> print(Gx.edges())
    # [('agent1', 'c'), ('agent1', 'f'), ('agent2', 'd'), ('agent2', 'g'), ('agent2', 'h'), ('agent3', 'e'), ('agent3', 'f'), ('agent4', 'g'), ('agent5', 'a'), ('agent5', 'b'), ('agent5', 'f'), ('agent5', 'i')]
    # >>> print(Gx.nodes())
    # ['agent1', 'agent2', 'agent3', 'agent4', 'agent5', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    # >>> print(alloc)
    # agent1's bundle: {c,f},  value: 170.0
    # agent2's bundle: {d,g,h},  value: 320.0
    # agent3's bundle: {e,f},  value: 300.0
    # agent4's bundle: {g},  value: 150.0
    # agent5's bundle: {a,b,f,i},  value: 300.0
    #
    # Third example: A situation where there is only one fpo division
    # >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 300, "g": -300, "h": -40, "i": -30}, name="agent1")
    # >>> agent2= AdditiveAgent({"a": 20, "b": -20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 300, "h": 80, "i": 90}, name="agent2")
    # >>> list_of_agents_for_func = [agent1, agent2]
    # >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    # >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.5,'b':0.5,'c':0.5,'d':0.5,'e':0.5,'f':0.5,'g':0.5,'h':0.5,'i':0.5},{'a':0.5,'b':0.5,'c':0.5,'d':0.5,'e':0.5,'f':0.5,'g':0.5,'h':0.5,'i':0.5}])
    # >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func, alloc_y_for_func)
    # >>> print(Gx.edges())
    # [('agent1', 'b'), ('agent1', 'c'), ('agent1', 'e'), ('agent1', 'f'), ('agent2', 'a'), ('agent2', 'd'), ('agent2', 'g'), ('agent2', 'h'), ('agent2', 'i')]
    # >>> print(Gx.nodes())
    # ['agent1', 'agent2', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    # >>> print(alloc)
    # agent1's bundle: {b,c,e,f},  value: 430.0
    # agent2's bundle: {a,d,g,h,i},  value: 580.0
    #
    # Fourth example: A general situation, in which the new division is indeed a pareto improvement of the original division
    # (example 7 in the second part of the work)
    # >>> agent1= AdditiveAgent({"a": -100, "b": 10, "c": 50, "d": -100 ,"e": 70,"f": 100, "g": -300, "h": -40, "i": 30}, name="agent1")
    # >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": -40, "d": 90 ,"e": -90,"f": -100, "g": 30, "h": 80, "i": 90}, name="agent2")
    # >>> agent3= AdditiveAgent({"a": 10, "b": -30, "c": 30, "d": 40 ,"e": 180,"f": 100, "g": 300, "h": 20, "i": -90}, name="agent3")
    # >>> agent4= AdditiveAgent({"a": -200, "b": 40, "c": -20, "d": 80 ,"e": -300,"f": 100, "g": 30, "h": 60, "i": -180}, name="agent4")
    # >>> agent5= AdditiveAgent({"a": 50, "b": 50, "c": 10, "d": 60 ,"e": 90,"f": -100, "g": 300, "h": -120, "i": 180}, name="agent5")
    # >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
    # >>> items_for_func = {'a','b','c','d','e','f','g','h','i'}
    # >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':0.2,'b':0.7,'c':0,'d':0.2,'e':0.9,'f':0.5,'g':0,'h':0.2,'i':0.4},{'a':0.4,'b':0.2,'c':0,'d':0.2,'e':0,'f':0,'g':0.8,'h':0.3,'i':0.1},{'a':0.1,'b':0.1,'c':0.6,'d':0.4,'e':0,'f':0,'g':0.1,'h':0.2,'i':0.4},{'a':0.1,'b':0,'c':0.2,'d':0.1,'e':0.1,'f':0,'g':0.1,'h':0.3,'i':0},{'a':0.2,'b':0,'c':0.2,'d':0.1,'e':0,'f':0.5,'g':0,'h':0,'i':0.1}])
    # >>> (Gx,alloc) = find_fpo_allocation(list_of_agents_for_func,items_for_func, alloc_y_for_func)
    # >>> print(Gx.edges())
    # [('agent1', 'b'), ('agent1', 'e'), ('agent1', 'f'), ('agent1', 'i'), ('agent2', 'd'), ('agent2', 'h'), ('agent3', 'c'), ('agent3', 'g'), ('agent5', 'a'), ('agent5', 'i')]
    # >>> print(Gx.nodes())
    # ['agent1', 'agent2', 'agent3', 'agent4', 'agent5', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    # >>> print(alloc)
    # agent1's bundle: {b,e,f,i},  value: 192.0
    # agent2's bundle: {d,h},  value: 170.0
    # agent3's bundle: {c,g},  value: 330.0
    # agent4's bundle: {},  value: 0.0
    # agent5's bundle: {a,i},  value: 158.0
    #
    # """
    # Gx = nx.DiGraph()
    # init_graph(agents, items, Gx, alloc_y)
    # T = []
    #
    # while cycle_basis(Gx):
    #     sum = 0
    #     constrains = []
    #     x = [[cvxpy.Variable() for i in items ] for a in agents]
    #     for agent in agents:
    #         for i in items:
    #             ui = agent.map_good_to_value[i]
    #             yi = alloc_y.map_item_to_fraction[i]
    #             sum += x[agent][i]*ui
    #
    #
    #     [sum([x[agent][i] for agent in agents]) == 1 for i in items]
    #
    #     [x[agent][i] == 0 for j in T]
    #
    #
    #     prob = cvxpy.Problem(
    #         cvxpy.Maximize(sum),
    #         constraints=[ui * x >= ui * yi])
    #     prob.solve()
    #
    #
    # return Gx, None

def find_po_and_prop1_allocation(Gx: nx, fpo_alloc: FractionalAllocation, items: Bundle) -> Allocation:
    """
    >>> agent1= AdditiveAgent({"a": 100, "b": 10, "c": 50}, name="agent1")
    >>> agent2= AdditiveAgent({"a": 20, "b": 20, "c": 40}, name="agent2")
    >>> agent3= AdditiveAgent({"a": 10, "b": 30, "c": 30}, name="agent3")
    >>> G = nx.Graph()
    >>> G.add_node('agent1')
    >>> G.add_node('agent2')
    >>> G.add_node('agent3')
    >>> G.add_node('a')
    >>> G.add_node('b')
    >>> G.add_node('c')
    >>> G.add_edge(agent1,'a')
    >>> G.add_edge(agent2,'a')
    >>> G.add_edge(agent1,'b')
    >>> G.add_edge(agent2,'b')
    >>> G.add_edge(agent3,'c')
    >>> items_for_func = {'a','b','c'}
    >>> list_of_agents_for_func = [agent1, agent2, agent3]
    >>> alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':1/3,'b':1/3,'c':1/3},{'a':1/3,'b':1/3,'c':1/3},{'a':1/3,'b':1/3,'c':1/3}])
    >>> find_po_and_prop1_allocation(G,alloc_y_for_func,items_for_func)
    """
    Q = []
    if Gx.number_of_edges() > len(items):
        count_how_many_parts_for_item = get_how_many_parts_for_item(fpo_alloc, items)
    while Gx.number_of_edges() > len(items):
        agent = find_agent_sharing_item(Gx, items)
        Q.append(agent)
        while Q is not None:
            curr_agent = Q.pop(0)
            dict_of_items_curr_agent_share = get_dict_of_items_curr_agent_share(curr_agent, fpo_alloc)
            for item, agents in dict_of_items_curr_agent_share.items():
                if curr_agent.map_good_to_value[item] > 0:
                    give_all_item_to_agent(curr_agent, item, dict_of_items_curr_agent_share[item], fpo_alloc)
                else:
                    other_agent = list(dict_of_items_curr_agent_share.keys())[0]
                    give_all_item_to_agent(other_agent, item, dict_of_items_curr_agent_share[item], fpo_alloc)
    result = FractionalAllocation_to_Allocation(fpo_alloc)
    return result


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
    >>> G = nx.Graph()
    >>> G.add_node('agent1')
    >>> G.add_node('agent2')
    >>> G.add_node('agent3')
    >>> G.add_node('a')
    >>> G.add_node('b')
    >>> G.add_node('c')
    >>> G.add_edge('agent1','a')
    >>> G.add_edge('agent2','a')
    >>> items_for_func = {'a','b','c'}
    >>> find_agent_sharing_item(G,items_for_func)
    'agent1'
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
    for item, val in curr_agent.map_good_to_value.items():
        if val > 0:
            list_of_agent_that_share_item = []
            for agent in fpo_alloc.agents:
                if agent != curr_agent and agent.map_good_to_value[item]>0:
                    list_of_agent_that_share_item.append(agent)
            result[item] = list_of_agent_that_share_item
    return result


def give_all_item_to_agent(curr_agent, item, list_of_agent_share_item, fpo_alloc):
    pass


def FractionalAllocation_to_Allocation(fpo_alloc: FractionalAllocation) -> Allocation:
    pass

if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    # agent1= AdditiveAgent({"a": 100, "b": 10, "c": 50}, name="agent1")
    # agent2= AdditiveAgent({"a": 20, "b": 20, "c": 40}, name="agent2")
    # agent3= AdditiveAgent({"a": 10, "b": 30, "c": 30}, name="agent3")
    # G = nx.Graph()
    # G.add_node('agent1')
    # G.add_node('agent2')
    # G.add_node('agent3')
    # G.add_node('a')
    # G.add_node('b')
    # G.add_node('c')
    # G.add_edge(agent1,'a')
    # G.add_edge(agent2,'a')
    # G.add_edge(agent1,'b')
    # G.add_edge(agent2,'b')
    # G.add_edge(agent3,'c')
    # items_for_func = {'a','b','c'}
    # list_of_agents_for_func = [agent1, agent2, agent3]
    # alloc_y_for_func = FractionalAllocation(list_of_agents_for_func, [{'a':1/3,'b':1/3,'c':1/3},{'a':1/3,'b':1/3,'c':1/3},{'a':1/3,'b':1/3,'c':1/3}])
    # find_po_and_prop1_allocation(G,alloc_y_for_func,items_for_func)





