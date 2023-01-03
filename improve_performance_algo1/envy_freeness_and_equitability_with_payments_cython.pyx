from fairpy import Allocation

cdef str list_to_sort_str(list bundle):
    sort_str = "".join(sorted(bundle))
    return sort_str

cdef float get_value(str agent, list bundle, dict eval_func):
    curr_bundles = list_to_sort_str(bundle) #Convert the list to a sorted string
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
            sum_values = sum_values + eval_func[agent][list_to_sort_str(allocation[agent])]
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


