# from fairpy import Allocation
# from typing import *
# cimport cython
#
# @cython.boundscheck(False)  # disable bounds checking for increased performance
# @cython.wraparound(False)  # disable negative indexing for increased performance
# cdef str list_to_sort_str(List[str] bundle):
#     sort_str = "".join(sorted(bundle))
#     return sort_str
#
# @cython.boundscheck(False)  # disable bounds checking for increased performance
# @cython.wraparound(False)  # disable negative indexing for increased performance
# cdef float get_value(str agent, List[str] boundle, Dict[str, Dict[str, int]] eval_func):
#     curr_bundles = list_to_sort_str(boundle) #Convert the list to a sorted string
#     if curr_bundles:  #if the bundle not empty
#         return eval_func[agent][curr_bundles]
#     return 0
#
# @cython.boundscheck(False)  # disable bounds checking for increased performance
# @cython.wraparound(False)  # disable negative indexing for increased performance
# cdef bint compare_2_bundles_and_transfer(str agent_a,Dict[str, List[str]] allo,Dict[str, Dict[str, int]] eval_func):
#     is_envy = False
#     for agent_b in allo:  #Go through all the agents (except the current agent) and check if transferring their bundle to them increases social welfare
#         if agent_b != agent_a:
#             if get_value(agent_a, allo[agent_a] + allo[agent_b], eval_func) > get_value(agent_a, allo[agent_a], eval_func) + get_value(agent_b, allo[agent_b], eval_func):
#                 allo[agent_a] = allo[agent_a] + allo[agent_b]  #Making the transfer
#                 allo[agent_b] = []  #agent_b lost his bundle
#                 is_envy = True  # set is_envy to True because there is jealousy here
#     return is_envy
#
#
# @cython.boundscheck(False)  # disable bounds checking for increased performance
# @cython.wraparound(False)  # disable negative indexing for increased performance
# cdef double calcuSWave(Dict[str, List[str]] allocation, Dict[str, Dict[str, int]] eval_func):
#     cdef double sum_values = 0
#     for agent in allocation:
#         if allocation[agent]:  #Go through all the agents and sum up their social welfare in the given allocation
#             sum_values = sum_values + eval_func[agent][list_to_sort_str(allocation[agent])]
#     return sum_values / len(allocation)  #return the average (the received sum divided by the number of agents)
#
#
# @cython.boundscheck(False)  # disable bounds checking for increased performance
# @cython.wraparound(False)  # disable negative indexing for increased performance
# cdef bint check_equal(Dict[str, List[str]] allo, Dict[str, Dict[str, int]] eval_func, Dict[str, int] pay_list):
#     cdef List[int] sw_list = []
#     for agent in allo:
#         val = get_value(agent, allo[agent], eval_func) - pay_list[agent]
#         sw_list.append(val)
#     is_equality = all(x == sw_list[0] for x in sw_list)
#     return is_equality
#
#
# @cython.boundscheck(False)  # disable bounds checking for increased performance
# @cython.wraparound(False)  # disable negative indexing for increased performance
# cpdef Dict[str, Union[Dict[str, List[str]], Dict[str, int]]] envy_freeness_and_equitability_with_payments(Dict[str, Dict[str, int]] evaluation, Allocation allocation):
#     if isinstance(allocation, Allocation):
#         allocation = allocation.map_agent_to_bundle() #convert Allocation to dict
#     cdef bool still_envy = True
#     while still_envy:  #The algorithm continue to run as long as there is envy
#         still_envy = False
#         for curr_agent in allocation:  #Go through each of the agents to check if they are jealous
#             is_envy = compare_2_bundles_and_transfer(curr_agent, allocation, evaluation)
#             if is_envy:
#                 still_envy = True
#     cdef double sw_ave = calcuSWave(allocation, evaluation)  #calculate the average social welfare of the current allocation
#     cdef Dict[str, int] payments = {}
#     for agent in allocation:
#         payments[agent] = get_value(agent, allocation[agent], evaluation) - sw_ave   #Calculation of the payment to each agent (the distance of the evaluation of the current bundle from the average of social welfare)
#     # logger.warning("check if %g", check_equal(allocation, evaluation, payments))
#     return {"allocation": allocation, "payments": payments}
#
#
#
# eval_1 = {"a": {"x": 40, "y": 20, "r": 30, "rx": 80, "rxy": 100}, "b": {"x": 10, "y":30, "r": 70, "rx": 79, "rxy": 90}}
# allocation_1 = {"a": ["y"], "b": ["x", "r"]}
#
# eval_2 = {"A": {"x": 70}, "B": {"x": 60}, "C": {"x": 40}, "D": {"x": 80}, "E": {"x": 55}}
# allocation_2 = {"A": ["x"], "B": [], "C": [], "D": [], "E": []}
#
# eq_value = {"x":10,"y":5,"z":15, "xy": 15, "yz": 20, "xz": 25}
# eval_3 = {"A":eq_value, "B":eq_value, "C":eq_value, "D":eq_value}
# allocation_3 = {"A":["x"], "B":["y"], "C":["z"], "D":[]}
#
# a = {"x": 15, "y": 20, "z":10,"w":5, "xy": 45,"xz":25,"wx":20,"yz":30,"yw":30,"zw":20,"xyz":50,"xyw":50,"xzw":30,"yzw":40,"wxyz":50}
# b = {"x": 30, "y": 35, "z":22,"w":7, "xy": 65,"xz":55,"wx":40,"yz":60,"yw":45,"zw":30,"xyz":90,"xyw":75,"xzw":65,"yzw":65,"wxyz":95}
# c = {"x": 40, "y": 12, "z":13,"w":21, "xy": 55,"xz":55,"wx":65,"yz":25,"yw":35,"zw":35,"xyz":65,"xyw":75,"xzw":75,"yzw":50,"wxyz":90}
# d = {"x": 5, "y": 7, "z":17,"w":19, "xy": 12,"xz":25,"wx":25,"yz":25,"yw":30,"zw":36,"xyz":30,"xyw":35,"xzw":45,"yzw":45,"wxyz":50}
# eval_4 = {"A":a, "B":b, "C":c, "D":d}
# allocation_4={"A":["x"], "B":["y"], "C":["z"], "D":["w"]}
#
# eval_10 = {"a": {"x": 40, "y": 20, "r": 30, "rx": 80, "rxy": 100}, "b": {"x": 10, "y":30, "r": 70, "rx": 79, "rxy": 90}}
# allocation_10 = {"a": ["y"], "b": ["x", "r"]}
# envy_freeness_and_equitability_with_payments(evaluation = eval_10, allocation= Allocation(agents = ["a", "b"],bundles = allocation_10))
# envy_freeness_and_equitability_with_payments(allocation_10, eval_10)
# # envy_freeness_and_equitability_with_payments(allocation_1, eval_1)
# # envy_freeness_and_equitability_with_payments(allocation_2, eval_2)
# # envy_freeness_and_equitability_with_payments(allocation_3, eval_3)
# # envy_freeness_and_equitability_with_payments(allocation_4, eval_4)
#
# # if __name__ == '__main__':
# #     import doctest
# #     doctest.testmod(verbose=True)
#
#
#
from fairpy import Allocation

cdef float get_value(str agent, list boundle, dict eval_func):
    curr_bundles = "".join(map(str, sorted(boundle))) #Convert the list to a sorted string
    if curr_bundles:  #if the bundle not empty
        return eval_func[agent][curr_bundles]
    return 0

cdef bint compare_2_bundles_and_transfer(str agent_a, dict allo, dict eval_func):
    cdef bint is_envy = False
    cdef str agent_b
    for agent_b in allo:  #Go through all the agents (except the current agent) and check if transferring their bundle to them increases social welfare
        if agent_b != agent_a:
            if get_value(agent_a, allo[agent_a] + allo[agent_b], eval_func) > get_value(agent_a, allo[agent_a], eval_func) + get_value(agent_b, allo[agent_b], eval_func):
                allo[agent_a] = allo[agent_a] + allo[agent_b]  #Making the transfer
                allo[agent_b] = []  #agent_b lost his bundle
                is_envy = True  # set is_envy to True because there is jealousy here
    return is_envy

cdef float calcuSWave(dict allocation, dict eval_func):
    cdef float sum_values = 0
    cdef str agent
    for agent in allocation:
        if allocation[agent]:  #Go through all the agents and sum up their social welfare in the given allocation
            sum_values = sum_values + eval_func[agent]["".join(sorted(allocation[agent]))]
    return sum_values / len(allocation)  #return the average (the received sum divided by the number of agents)

cdef bint list_sw(dict allo, dict eval_func, dict pay_list):
    cdef list sw_list = []
    cdef str agent
    for agent in allo:
        val = get_value(agent, allo[agent], eval_func) - pay_list[agent]
        sw_list.append(val)
    return all(x == sw_list[0] for x in sw_list)

cpdef envy_freeness_and_equitability_with_payments_cython(dict evaluation, object allocation):
    cdef dict allocation_map
    if isinstance(allocation, Allocation):
        allocation_map = allocation.map_agent_to_bundle() #convert Allocation to dict
    else:
        allocation_map = allocation
    cdef bint still_envy = True
    cdef str curr_agent
    while still_envy:  #The algorithm continue to run as long as there is envy
        still_envy = False

        for curr_agent in allocation_map:  #Go through each of the agents to check if they are jealous
            is_envy = compare_2_bundles_and_transfer(curr_agent, allocation_map, evaluation)
            if is_envy:
                still_envy = True
    cdef float sw_ave = calcuSWave(allocation_map, evaluation)  #calculate the average social welfare of the current allocation
    cdef dict payments = {}
    for agent in allocation_map:
        payments[agent] = get_value(agent, allocation_map[agent], evaluation) - sw_ave   #Calculation of the payment to each agent (the distance of the evaluation of the current bundle from the average of social welfare)
    return {"allocation": allocation_map, "payments": payments}


