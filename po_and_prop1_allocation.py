import cvxpy
import networkx as nx
from indivisible.agents import AdditiveAgent, Bundle, List
from indivisible.allocations import Allocation, FractionalAllocation
from networkx.algorithms import bipartite, find_cycle

#Main functions
def find_fpo_allocation(agents: List[AdditiveAgent], items: Bundle, alloc_y: FractionalAllocation) -> (bipartite, FractionalAllocation):
    """
    # First example:   ###The problem with returning a graph is that we return an object so we return space in memory so I do not know how to check it
    Case 1: Only one player(must get everything),Items with positive utility.
    >>> agent1_for_func = AdditiveAgent({"x": 1, "y": 2, "z": 4}, name="agent1")
    >>> list_of_agents_for_func = [agent1_for_func]
    >>> alloc_y_for_func = Allocation([agent1_for_func], ["xyz"])
    >>> items_for_func = alloc_y_for_func.get_bundles()
    >>> utility_for_func = agent1_for_func.get_values()
    >>> find_fpo_allocation(list_of_agents_for_func,items_for_func,utility_for_func,alloc_y_for_func)
    (agent1's bundle: {x,y,z},  value: 7,  all values: [1, 2, 4] , )

    Case 2: Only one player(must get everything),Items with negative utility.
    >>> agent1_for_func.set_values([-1,-2,-4])
    >>> print(agent1_for_func.get_values())
    >>> find_fpo_allocation(list_of_agents_for_func,items_for_func,utility_for_func,alloc_y_for_func)
    (agent2's bundle: {x,y,z},  value: -7,  all values: [-1, -2, -4] , )

    Case 3: Only one player(must get everything),Items with negative and positive utilitys.
    >>> agent1_for_func.set_values([-1,2,-4])
    >>> find_fpo_allocation(list_of_agents_for_func,items_for_func,utility_for_func,alloc_y_for_func)
    (agent1's bundle: {x,y,z},  value: -3,  all values: [-1, 2, -4] , )

    Fourth example: original y allocation that is already fpo - there is no Pareto improvement so the output will be equal to the input.
     >>> agent1= AdditiveAgent({"a": -100, "b": -10, "c": -50, "d":-100 ,"e":-70,"f":-100, "g":-200, "h":-40, "i":-30}, name="agent1")
     >>> agent2= AdditiveAgent({"a": -20, "b": -20, "c": -40, "d":-90 ,"e":-90,"f":-100, "g":-100, "h":-80, "i":-90}, name="agent2")
     >>> agent3= AdditiveAgent({"a": -10, "b": -30, "c": -30, "d":-40 ,"e":-180,"f":-100, "g":-200, "h":-20, "i":-90}, name="agent3")
     >>> agent4= AdditiveAgent({"a": -200, "b": -40, "c": -20, "d":-80 ,"e":-300,"f":-100, "g":-100, "h":-60, "i":-180}, name="agent4")
     >>> agent5= AdditiveAgent({"a": -50, "b": -50, "c": -10, "d":-60 ,"e":-90,"f":-100, "g":-200, "h":-120, "i":-180}, name="agent5")
     >>> list_of_agents_for_func = [agent1, agent2, agent3, agent4, agent5]
     >>> utility_for_func=[]
     >>> for a in list_of_agents_for_func: utility_for_func.append(a.get_values())
     >>> #! alloc_y_for_func = Allocation([agent1, agent2, agent3,agent4, agent5], ["abcdefghi","abcdefghi","abcdefghi","abcdefghi","abcdefghi"])
     >>> items_for_func = alloc_y_for_func.get_bundles()
    """

    # B = nx.Graph()
    # # Add nodes with the node attribute "bipartite"
    # B.add_nodes_from([1, 2, 3, 4], bipartite=0)
    # B.add_nodes_from(["a", "b", "c"], bipartite=1)
    # # Add edges only between nodes of opposite node sets
    # B.add_edges_from([(1, "a"), (1, "b"), (2, "b"), (2, "c"), (3, "c"), (4, "a")])
    #EdgeView([(1, 'a'), (1, 'b'), (2, 'b'), (2, 'c'), (3, 'c'), (4, 'a')])
    #NodeView((1, 2, 3, 4, 'a', 'b', 'c'))

    # bipartite_graph = init_graph()
    # T = {}
    # while find_cycle(bipartite_graph, source=None, orientation=None) is not None:
    #     agent = cvxpy.Variable()
    #     object = cvxpy.Variable()
    return None, None


def find_po_and_prop1_allocation(agents: List[AdditiveAgent], items: Bundle, rights_b: List[List[float]]) -> Allocation:
    """

    """
    # agent1_for_func = AdditiveAgent({"x": 1, "y": 2, "z": 4}, name="agent1")
    # list_of_agents_for_func = [agent1_for_func]
    # alloc_y_for_func = Allocation([agent1_for_func], ["xyz"])
    # items_for_func = alloc_y_for_func.get_bundles()
    # utility_for_func = agent1_for_func.value(alloc_y_for_func.get_bundle(0))
    # B1 = nx.Graph()
    # print(find_fpo_allocation(list_of_agents_for_func, items_for_func, utility_for_func, alloc_y_for_func))

    return None

#Help functions
def init_graph() -> bipartite:
    # b = nx.Graph()
    # return b
    pass

if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))







