"""
"Achieving Envy-freeness and Equitability with Monetary Transfers" by Haris Aziz (2021),
    https://ojs.aaai.org/index.php/AAAI/article/view/16645

    Algorithm 1: Creating envy-freeness and equitability division with the help of a payment function.

    Programmers: Noamya Shani, Eitan Shenkolevski.
"""
from fairpy import Allocation, AgentList
import logging

logger = logging.getLogger()


def find_envy_freeness_and_equitability_with_payments(evaluation: AgentList):
    """
        A function that receives values of agents, initializes an initial alloction and sends it to the central function

        :param evaluation: A AgentList of the evaluations of each agent for each bundle

        >>> eval_1 = {"a": {"x": 40, "y": 20, "r": 30, "xy":65, "rx": 80, "rxy": 100}, "b": {"x": 10, "y":30, "r": 70, "xy":55, "rx": 79, "rxy": 90}}
        >>> find_envy_freeness_and_equitability_with_payments(evaluation=eval_1)
        {'allocation': {'a': ['r', 'x'], 'b': ['y']}, 'payments': {'a': 25.0, 'b': -25.0}}
        >>> eval_2 = {"A":{"x":70},"B":{"x":60},"C":{"x":40},"D":{"x":80},"E":{"x":55}}
        >>> find_envy_freeness_and_equitability_with_payments(evaluation=eval_2)
        {'allocation': {'A': [], 'B': [], 'C': [], 'D': ['x'], 'E': []}, 'payments': {'A': -16.0, 'B': -16.0, 'C': -16.0, 'D': 64.0, 'E': -16.0}}
        >>> eq_value = {"x":10,"y":5,"z":15, "xy": 15, "yz": 20, "xz": 25}
        >>> eval_3 = {"A":eq_value,"B":eq_value,"C":eq_value,"D":eq_value}
        >>> find_envy_freeness_and_equitability_with_payments(evaluation=eval_3)
        {'allocation': {'A': ['x'], 'B': ['y'], 'C': ['z'], 'D': []}, 'payments': {'A': 2.5, 'B': -2.5, 'C': 7.5, 'D': -7.5}}
        >>> a = {"x": 15, "y": 20, "z":10,"w":5, "xy": 45,"xz":25,"wx":20,"yz":30,"yw":30,"zw":20,"xyz":50,"xyw":50,"xzw":30,"yzw":40,"wxyz":50}
        >>> b = {"x": 30, "y": 35, "z":22,"w":7, "xy": 65,"xz":55,"wx":40,"yz":60,"yw":45,"zw":30,"xyz":90,"xyw":75,"xzw":65,"yzw":65,"wxyz":95}
        >>> c = {"x": 40, "y": 12, "z":13,"w":21, "xy": 55,"xz":55,"wx":65,"yz":25,"yw":35,"zw":35,"xyz":65,"xyw":75,"xzw":75,"yzw":50,"wxyz":90}
        >>> d = {"x": 5, "y": 7, "z":17,"w":19, "xy": 12,"xz":25,"wx":25,"yz":25,"yw":30,"zw":36,"xyz":30,"xyw":35,"xzw":45,"yzw":45,"wxyz":50}
        >>> eval_4 = {"A":a,"B":b,"C":c,"D":d}
        >>> find_envy_freeness_and_equitability_with_payments(evaluation = eval_4)
        {'allocation': {'A': [], 'B': ['y', 'x', 'z'], 'C': ['w'], 'D': []}, 'payments': {'A': -27.75, 'B': 62.25, 'C': -6.75, 'D': -27.75}}
    """
    if isinstance(evaluation, AgentList):
        eval = list(evaluation.all_items())
        bundles = [bundle for bundle in eval if len(bundle) == 1]
        agents = evaluation.agent_names()
    else:
        eval = list(list(evaluation.values()))[0]
        bundles = [bundle for bundle in eval if len(bundle) == 1]
        agents = evaluation.keys()
    allocation = {}
    i = 0
    while i < len(bundles):
        for agent in evaluation:
            if i < len(bundles):
                if agent not in allocation.keys():
                    allocation[agent] = []
                if len(allocation[agent]) > 0:
                    allocation[agent].append(bundles[i])
                else:
                    allocation[agent] = [bundles[i]]
            i = i + 1
    return make_envy_freeness_and_equitability_with_payments(evaluation, Allocation(agents, allocation))


def make_envy_freeness_and_equitability_with_payments(evaluation: AgentList, allocation: Allocation):
    """
    :param evaluation: A dictionary of the evaluations of each agent for each bundle
    :param allocation: The initial allocation

    >>> eval_1 = {"a": {"x": 40, "y": 20, "r": 30, "xy":65, "rx": 80, "rxy": 100}, "b": {"x": 10, "y":30, "r": 70, "xy":55, "rx": 79, "rxy": 90}}
    >>> allocation_1 = {"a": ["y"], "b": ["x", "r"]}
    >>> make_envy_freeness_and_equitability_with_payments(evaluation = eval_1, allocation= Allocation(agents = ["a", "b"],bundles = allocation_1))
    {'allocation': {'a': ['y', 'r', 'x'], 'b': []}, 'payments': {'a': 50.0, 'b': -50.0}}
    >>> eval_2 = {"A":{"x":70},"B":{"x":60},"C":{"x":40},"D":{"x":80},"E":{"x":55}}
    >>> allocation_2 = {"A": ["x"], "B": [], "C": [], "D": [], "E": []}
    >>> make_envy_freeness_and_equitability_with_payments(evaluation = eval_2, allocation = Allocation(agents = ["A", "B", "C", "D", "E"],bundles = allocation_2))
    {'allocation': {'A': [], 'B': [], 'C': [], 'D': ['x'], 'E': []}, 'payments': {'A': -16.0, 'B': -16.0, 'C': -16.0, 'D': 64.0, 'E': -16.0}}
    >>> eq_value = {"x":10,"y":5,"z":15, "xy": 15, "yz": 20, "xz": 25}
    >>> eval_3 = {"A":eq_value,"B":eq_value,"C":eq_value,"D":eq_value}
    >>> allocation_3 = {"A":["x"], "B":["y"], "C":["z"], "D":[]}
    >>> make_envy_freeness_and_equitability_with_payments(evaluation = eval_3, allocation = Allocation(agents = ["A", "B", "C", "D"],bundles = allocation_3))
    {'allocation': {'A': ['x'], 'B': ['y'], 'C': ['z'], 'D': []}, 'payments': {'A': 2.5, 'B': -2.5, 'C': 7.5, 'D': -7.5}}
    >>> a = {"x": 15, "y": 20, "z":10,"w":5, "xy": 45,"xz":25,"wx":20,"yz":30,"yw":30,"zw":20,"xyz":50,"xyw":50,"xzw":30,"yzw":40,"wxyz":50}
    >>> b = {"x": 30, "y": 35, "z":22,"w":7, "xy": 65,"xz":55,"wx":40,"yz":60,"yw":45,"zw":30,"xyz":90,"xyw":75,"xzw":65,"yzw":65,"wxyz":95}
    >>> c = {"x": 40, "y": 12, "z":13,"w":21, "xy": 55,"xz":55,"wx":65,"yz":25,"yw":35,"zw":35,"xyz":65,"xyw":75,"xzw":75,"yzw":50,"wxyz":90}
    >>> d = {"x": 5, "y": 7, "z":17,"w":19, "xy": 12,"xz":25,"wx":25,"yz":25,"yw":30,"zw":36,"xyz":30,"xyw":35,"xzw":45,"yzw":45,"wxyz":50}
    >>> eval_4 = {"A":a,"B":b,"C":c,"D":d}
    >>> allocation_4={"A":["x"], "B":["y"], "C":["z"], "D":["w"]}
    >>> make_envy_freeness_and_equitability_with_payments(evaluation = eval_4, allocation = Allocation(agents = ["A", "B", "C", "D"],bundles = allocation_4))
    {'allocation': {'A': [], 'B': ['y', 'x', 'z'], 'C': ['w'], 'D': []}, 'payments': {'A': -27.75, 'B': 62.25, 'C': -6.75, 'D': -27.75}}
    """
    if isinstance(allocation, Allocation):
        allocation = allocation.map_agent_to_bundle() #convert Allocation to dict
    still_envy = True
    while still_envy:  #The algorithm continue to run as long as there is envy
        still_envy = False
        for curr_agent in allocation:  #Go through each of the agents to check if they are jealous
            is_envy = compare_2_bundles_and_transfer(curr_agent, allocation, evaluation)
            if is_envy:
                still_envy = True
    sw_ave = calcuSWave(allocation, evaluation)  #calculate the average social welfare of the current allocation
    payments = {}
    for agent in allocation:
        payments[agent] = get_value(agent, allocation[agent], evaluation) - sw_ave   #Calculation of the payment to each agent (the distance of the evaluation of the current bundle from the average of social welfare)
    return {"allocation": allocation, "payments": payments}


def list_to_sort_str(bundle: list):
    """
    A function that sorts a list and turns it into a string
    :param bundle: A list that we will sort and turn into a string
    >>> list_to_sort_str(["a","c","b"])
    'abc'
    >>> list_to_sort_str(["v","t","y","b","r","k","e"])
    'bekrtvy'
    >>> list_to_sort_str(["z","y","x","w","f","s","q"])
    'fqswxyz'
    """
    sort_str = "".join(sorted(bundle))
    return sort_str


def get_value(agent: str, boundle: list, eval_func: dict):
    """"
    A function that returns an agent's evaluation of a particular bundle
    :param agent: the name of the agent
    :param boundle: List the elements in the given bundle
    :param eval_func: A dictionary of the evaluations of each agent for each bundle

    >>> eval_1 = {"a": {"x": 40, "y": 20, "r": 30, "xy":65, "rx": 80, "rxy": 100}, "b": {"x": 10, "y":30, "r": 70, "xy":55, "rx": 79, "rxy": 90}}
    >>> eval_2 = {"A": {"x": 70}, "B": {"x": 60}, "C": {"x": 40}, "D": {"x": 80}, "E": {"x": 55}}
    >>> get_value("a",["y"], eval_1)
    20
    >>> get_value("b",["x", "r"], eval_1)
    79
    >>> get_value("B",["x"], eval_2)
    60
    >>> get_value("A",[], eval_2)
    0
    """
    curr_bundles = list_to_sort_str(boundle) #Convert the list to a sorted string
    if curr_bundles:  #if the bundle not empty
        return eval_func[agent][curr_bundles]
    return 0


def compare_2_bundles_and_transfer(agent_a: str, allo: dict, eval_func: dict):
    """
    A function that checks if transferring a bundle to a certain agent will increase the SW, and if so transfers
    :param agent_a: the name of the cuurent agent
    :param allo: The current allocation
    :param eval_func: A dictionary of the evaluations of each agent for each bundle

    >>> eval_1 = {"a": {"x": 40, "y": 20, "r": 30, "xy":65, "rx": 80, "rxy": 100}, "b": {"x": 10, "y":30, "r": 70, "xy":55, "rx": 79, "rxy": 90}}
    >>> allocation_1 = {"a": ["y"], "b": ["x", "r"]}
    >>> eval_2 = {"A": {"x": 70}, "B": {"x": 60}, "C": {"x": 40}, "D": {"x": 80}, "E": {"x": 55}}
    >>> allocation_2 = {"A": ["x"], "B": [], "C": [], "D": [], "E": []}
    >>> compare_2_bundles_and_transfer("a",allocation_1, eval_1)
    True
    >>> print(allocation_1["a"])
    ['y', 'x', 'r']
    >>> compare_2_bundles_and_transfer("b",allocation_1, eval_1)
    False
    >>> compare_2_bundles_and_transfer("B",allocation_2, eval_2)
    False
    >>> print(allocation_2["D"])
    []
    >>> compare_2_bundles_and_transfer("D",allocation_2, eval_2)
    True
    >>> print(allocation_2["D"])
    ['x']
    """
    is_envy = False
    for agent_b in allo:  #Go through all the agents (except the current agent) and check if transferring their bundle to them increases social welfare
        if agent_b != agent_a:
            if get_value(agent_a, allo[agent_a] + allo[agent_b], eval_func) > get_value(agent_a, allo[agent_a], eval_func) + get_value(agent_b, allo[agent_b], eval_func):
                allo[agent_a] = allo[agent_a] + allo[agent_b]  #Making the transfer
                allo[agent_b] = []  #agent_b lost his bundle
                is_envy = True  # set is_envy to True because there is jealousy here
                logger.debug("agent %s took agent %s's bundle", agent_a, agent_b)
    return is_envy


def calcuSWave(allocation: dict, eval_func: dict):
    """
    A function to calculate the average social welfare of the current allocation
    :param allocation: The current allocation
    :param eval_func: A dictionary of the evaluations of each agent for each bundle

    >>> eval_1 = {"a": {"x": 40, "y": 20, "r": 30, "xy":65, "rx": 80, "rxy": 100}, "b": {"x": 10, "y":30, "r": 70, "xy":55, "rx": 79, "rxy": 90}}
    >>> allocation_1 = {"a": ["y"], "b": ["x", "r"]}
    >>> eval_2 = {"A": {"x": 70}, "B": {"x": 60}, "C": {"x": 40}, "D": {"x": 80}, "E": {"x": 55}}
    >>> allocation_2 = {"A": ["x"], "B": [], "C": [], "D": [], "E": []}
    >>> eq_value = {"x":10,"y":5,"z":15, "xy": 15, "yz": 20, "xz": 25}
    >>> eval_3 = {"A":eq_value, "B":eq_value, "C":eq_value, "D":eq_value}
    >>> allocation_3 = {"A":["x"], "B":["y"], "C":["z"], "D":[]}
    >>> calcuSWave(allocation_1, eval_1)
    49.5
    >>> calcuSWave(allocation_2, eval_2)
    14.0
    >>> calcuSWave(allocation_3, eval_3)
    7.5
    """
    sum_values = 0
    for agent in allocation:
        if allocation[agent]:  #Go through all the agents and sum up their social welfare in the given allocation
            sum_values = sum_values + eval_func[agent][list_to_sort_str(allocation[agent])]
            logger.debug("current sum_value after agent %s: %d", agent, sum_values)
    logger.info("average of SW: %f",sum_values / len(allocation))
    return sum_values / len(allocation)  #return the average (the received sum divided by the number of agents)


def check_equal(allo: dict, eval_func: dict, pay_list: dict):
    """
    A function to check if we have achieved equality
    :param allo: The current allocation
    :param eval_func: A dictionary of the evaluations of each agent for each bundle
    :param pay_list: A dictionary of each agent's payment

    >>> eval_2 = {"A": {"x": 70}, "B": {"x": 60}, "C": {"x": 40}, "D": {"x": 80}, "E": {"x": 55}}
    >>> allocation_2 = {"A": ["x"], "B": [], "C": [], "D": [], "E": []}
    >>> eq_value = {"x":10,"y":5,"z":15, "xy": 15, "yz": 20, "xz": 25}
    >>> eval_3 = {"A":eq_value, "B":eq_value, "C":eq_value, "D":eq_value}
    >>> allocation_3 = {"A":["x"], "B":["y"], "C":["z"], "D":[]}
    >>> check_equal(allocation_2, eval_2, {'A': 56.0, 'B': -14.0, 'C': -14.0, 'D': -14.0, 'E': -14.0})
    True
    >>> check_equal(allocation_2, eval_2, {'A': -16.0, 'B': -16.0, 'C': -15.0, 'D': 64.0, 'E': -16.0})
    False
    >>> check_equal(allocation_3, eval_3, {'A': -16.0, 'B': -16.0, 'C': -16.0, 'D': 64.0, 'E': -16.0})
    False
    >>> check_equal(allocation_3, eval_3, {'A': 2.5, 'B': -2.5, 'C': 7.5, 'D': -7.5})
    True
    """
    sw_list = []
    for agent in allo:
        val = get_value(agent, allo[agent], eval_func) - pay_list[agent]
        sw_list.append(val)
    is_equality = all(x == sw_list[0] for x in sw_list)
    return is_equality


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())




