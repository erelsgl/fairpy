
cimport cython
import numpy as np
cimport numpy as np


@cython.boundscheck(False)
@cython.wraparound(False)
cdef void swap_columns(np.ndarray[np.float64_t, ndim=2] matrix, int idx_1, int idx_2):
    cdef np.ndarray[np.float64_t, ndim=1] temp = np.copy(matrix[:, idx_1])
    matrix[:, idx_1] = matrix[:, idx_2]
    matrix[:, idx_2] = temp

@cython.boundscheck(False)
@cython.wraparound(False)
cdef float get_max(np.ndarray[np.float64_t, ndim=1] agent_valuation, np.ndarray[np.float64_t, ndim=1] payments):
    cdef int i
    cdef float max_val = agent_valuation[0] - payments[0]
    for i in range(1, len(agent_valuation)):
        if agent_valuation[i] - payments[i] > max_val:
            max_val = agent_valuation[i] - payments[i]
    return max_val

@cython.boundscheck(False)
@cython.wraparound(False)
cdef int get_argmax(np.ndarray[np.float64_t, ndim=1] agent_valuation, np.ndarray[np.float64_t, ndim=1] payments):
    cdef int i, max_idx = 0
    cdef float max_val = agent_valuation[0] - payments[0]
    for i in range(1, len(agent_valuation)):
        if agent_valuation[i] - payments[i] > max_val:
            max_idx = i
            max_val = agent_valuation[i] - payments[i]
    return max_idx

@cython.boundscheck(False)
@cython.wraparound(False)
cdef float get_second_max(int idx, np.ndarray[np.float64_t, ndim=1] agent_valuation, np.ndarray[np.float64_t, ndim=1] payments):
    cdef int i
    cdef float max_val = -float('inf')
    for i in range(len(agent_valuation)):
        if i == idx:
            continue
        if agent_valuation[i] - payments[i] > max_val:
            max_val = agent_valuation[i] - payments[i]
    return max_val



@cython.boundscheck(False)
@cython.wraparound(False)
cpdef envy_free_approximation_cython(object allocation, float eps=0):
    cdef np.ndarray[np.float64_t, ndim=2] value_matrix = allocation.utility_profile_matrix()
    cdef np.ndarray[np.float64_t, ndim=1] payments = np.zeros(allocation.num_of_agents)
    cdef list bundles = [[i] for i in range(allocation.num_of_agents)]
    cdef float u1, u2, temp_p
    cdef list temp
    cdef int agent_j, agent_i = 0, still_envy = 1
    while still_envy:
        still_envy = 0
        # run on all agents and check if exist ε-envy
        for agent_i in range(len(value_matrix)):
            if value_matrix[agent_i][agent_i] - payments[agent_i] < get_max(value_matrix[agent_i], payments) - eps:
                # get the agent with max utility
                agent_j = get_argmax(value_matrix[agent_i], payments)
                u1 = get_max(value_matrix[agent_i], payments)
                u2 = get_second_max(agent_j, value_matrix[agent_i], payments)
                # replace payment value
                swap_columns(value_matrix, agent_i, agent_j)
                temp = bundles[agent_i]
                bundles[agent_i] = bundles[agent_j]
                bundles[agent_j] = temp
                # replace payment value
                temp_p = payments[agent_i]
                payments[agent_i] = payments[agent_j] + (u1 - u2) + eps
                payments[agent_j] = temp_p
                still_envy = 1
    return {"allocation": bundles, "payments": payments.tolist()}

