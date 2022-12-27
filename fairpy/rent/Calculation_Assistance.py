import networkx as nx
import random
import cvxpy as cp
from fairpy.agentlist import AgentList


def spliddit(agentList: AgentList, rent: float):
    """
        This function for calculation of allocation by spliddit algorithm
    :param N: agent
    :param A: rooms
    :param val: value of room by each agent
    :param rent: total rent house
    :return: sigma: N -> A , p : is vector of prices for each room
    """
    N = []
    A = []
    for i in agentList.agent_names():
        N.append(i)
    for i in agentList.all_items():
        A.append(i)

    g = nx.Graph()
    g.add_nodes_from(N, bipartite=0)
    g.add_nodes_from(A, bipartite=1)
    for i, k in zip(N, range(len(N))):
        for j in A:
            g.add_edge(i, j, weight=agentList[k].value(j))

    alloc = nx.max_weight_matching(g, maxcardinality=True)
    dict_match = {}
    for i in alloc:
        if i[1] not in A:
            dict_match[i[1]] = i[0]
        else:
            dict_match[i[0]] = i[1]

    # dict_match = dict(sorted(dict_match.items(), key=lambda x: x[0]))
    variable = {}  # list of all the 'price' variables that present the price of any room
    for i in dict_match.values():
        variable["price " + str(i)] = cp.Variable()

    variable["M"] = cp.Variable()  # this variable care for the maximum
    objective = cp.Maximize(variable["M"])
    constraints = []
    # have 3 constrains
    # 1)  M <= v_iσ(i) - p_σ(i)
    for i in dict_match.keys():
        constraints.append(variable["M"] <= agentList[N.index(i)].value(dict_match[i]) - variable["price " + dict_match[i]])

    # 2) Check that without envy -> v_iσ(i) - p_σ(i) ≥ v_iσ(j) - p_σ(j)
    for i in dict_match.keys():
        for j in dict_match.keys():
            if i != j:
                constraints.append(agentList[N.index(i)].value(dict_match[i]) - variable["price " + dict_match[i]] >=
                                   agentList[N.index(i)].value(dict_match[j]) - variable["price " + dict_match[j]])
    # 3) ∑ P_i = rent
    total = 0
    for i in dict_match.keys():
        total += variable["price " + dict_match[i]]
    constraints.append(total == rent)

    prob = cp.Problem(objective, constraints)
    result = prob.solve()

    sigma = {}
    vector_p = {}
    for i in dict_match.keys():
        sigma[str(i)] = str(dict_match[i])
        vector_p[str(dict_match[i])] = round(float(variable["price " + dict_match[i]].value), 2)
    return sigma, vector_p


def if_allocation_is_envy_free(sigma: dict, vector_p: dict, value: dict[dict]):
    """
        This for check if allocation is envy free
    :return:
    """
    for i in sigma.keys():
        for j in sigma.keys():
            if i != j:
                left = value[i][sigma[i]] - vector_p[sigma[i]]
                right = value[i][sigma[j]] - vector_p[sigma[j]]
                if left < right:
                    return False
    return True


def build_budget_aware_graph(sigma: dict, vector_p: dict, budget: dict, agentList: AgentList) -> nx.DiGraph:
    """
        This function build budget aware envy graph ,Γ_b(σ, p) ≡ (N,E) , where
        E = {(i, j) : v_iσ(i) - p_σ(i) = v_iσ(j) - p_σ(i) and p_σ(j) < b_i}
    :param sigma: this function from agent to room
    :param vector_p: vector of prices for each room
    :param budget: agents budget
    :param val: the value of room by agent
    :return:  graph
    """
    budget_aware_graph = nx.DiGraph()
    for i in sigma.keys():
        for j in sigma.keys():
            if not i == j:
                left = agentList[agentList.agent_names().index(i)].value(sigma[i]) - vector_p[sigma[i]]
                # to build budget aware weak envy graph --> v_iσ(i) - p_σ(i) = v_iσ(j) - p_σ(i) and p_σ(j) < b_i
                if left == (agentList[agentList.agent_names().index(i)].value(sigma[j]) - vector_p[sigma[i]]) and budget[i] > vector_p[sigma[j]]:
                    budget_aware_graph.add_node(i)
                    budget_aware_graph.add_node(j)
                    budget_aware_graph.add_edge(i, j)

    return budget_aware_graph


def build_weak_envy_graph(sigma: dict, vector_p: dict, agentList: AgentList) -> nx.DiGraph:
    """
        This function for build weak envy graph , Γ(σ, p) ≡ (N,E) ,where
        (i, j) ∈ E if and only if v_iσ(i) - p_σ(i) = v_iσ(j) - p_σ(j)
    :param sigma: this function from agent to room
    :param vector_p: vector of prices for each room
    :param val: the value of room by agent
    :return:
    """
    weak_envy_graph = nx.DiGraph()
    for i in sigma.keys():
        for j in sigma.keys():
            if not i == j:
                left = (agentList[agentList.agent_names().index(i)].value(sigma[i]) - vector_p[sigma[i]])
                # to build weak envy graph --> v_iσ(i) - p_σ(i) = v_iσ(j) - p_σ(j)
                if left == (agentList[agentList.agent_names().index(i)].value(sigma[j]) - vector_p[sigma[j]]):
                    weak_envy_graph.add_node(i)
                    weak_envy_graph.add_node(j)
                    weak_envy_graph.add_edge(i, j)
    return weak_envy_graph


def calculation_delta(sigma: dict, vector_p: dict, agentList: AgentList, rent: float, budget: dict):
    count = 0
    flag = True
    while flag:
        count += 1
        s = random.randint(rent, rent + count * 100)
        µ, q = spliddit(list(sigma.keys()), list(sigma.values()), agentList, s)
        for i in µ.values():
            if q[i] != vector_p[i] + (s - rent) / len(µ.keys()):
                flag = False
                break
        if not flag:
            flag = True
        else:
            for i in sigma.keys():
                if budget[i] == vector_p[sigma[i]]:
                    return (s - rent) / len(µ.keys())
            flag = True


if __name__ == '__main__':
    # N = ['a', 'b', 'c']
    # A = ['small', 'mid', 'big']
    # val = {
    #     'a': {'small': 250, 'mid': 250, 'big': 500},
    #     'b': {'small': 250, 'mid': 500, 'big': 250},
    #     'c': {'small': 200, 'mid': 200, 'big': 600},
    # }
    # rent = 1000
    # budget = {
    #     'a': 600,
    #     'b': 350,
    #     'c': 500
    # }
    # ans = spliddit(N, A, val, rent)
    # print(*ans, sep="\n")
    # if_allocation_is_envy_free(ans[0], ans[1], val)
    # # graph = build_graph(ans[0], ans[1], val)
    # # SCC_weak_envy_graph(graph[1])
    # N = ['P1', 'P2', 'P3', 'P4']
    # A = ['Ra', 'Rb', 'Rc', 'Rd']
    agentList1 = AgentList({'bob': {'Ra': 600, 'Rb': 100, 'Rc': 150, 'Rd': 150},
                            'alice': {'Ra': 250, 'Rb': 250, 'Rc': 250, 'Rd': 250},
                            'dor': {'Ra': 100, 'Rb': 400, 'Rc': 250, 'Rd': 250},
                            'clair': {'Ra': 100, 'Rb': 200, 'Rc': 350, 'Rd': 350}})
    val = {
        'bob': {'Ra': 600, 'Rb': 100, 'Rc': 150, 'Rd': 150},
        'alice': {'Ra': 250, 'Rb': 250, 'Rc': 250, 'Rd': 250},
        'dor': {'Ra': 100, 'Rb': 400, 'Rc': 250, 'Rd': 250},
        'clair': {'Ra': 100, 'Rb': 200, 'Rc': 350, 'Rd': 350}
    }
    rent = 1000
    budget = {
        'bob': 1000,
        'alice': 1000,
        'dor': 1000,
        'clair': 1000
    }
    # N = ['Alice', 'Bob', 'Clair']
    # A = ['2ndFloor', 'Basement', 'MasterBedroom']
    # val = {
    #     'Alice': {'2ndFloor': 250, 'Basement': 250, 'MasterBedroom': 500},
    #     'Bob': {'2ndFloor': 250, 'Basement': 250, 'MasterBedroom': 500},
    #     'Clair': {'2ndFloor': 250, 'Basement': 500, 'MasterBedroom': 250},
    # }
    # rent = 1000
    sigma, p = spliddit(agentList1, rent)
    build_weak_envy_graph(sigma, p, agentList1)
    build_budget_aware_graph(sigma, p, budget, agentList1)
