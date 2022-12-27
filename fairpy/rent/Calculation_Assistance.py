import networkx as nx
import random
import cvxpy as cp
from fairpy.agentlist import AgentList


def spliddit(agentList: AgentList, rent: float):
    """
        This function for calculation of allocation by spliddit algorithm
        By Linear Programming of :
            max M
            M,pσ(1),...,pσ(n)
                    s.t.
                    ,
                    ∑_i∈N pσ(i) = r ,
                    ∀i ∈ N , v_iσ(i) − p_σ(i))
                    ∀i,j∈N, v_iσ(i) - p_σ(i) ≥ v_iσ(j) - p_σ(j)
    :param agentList:  agent whit rooms and valuation for each room by agent
    :param rent: total rent house
    :param N: list of agent
    :param A: list of room
    :return: sigma: N -> A , p : is vector of prices for each room
    """
    # it take the typing agent List and moves to the component for comfortable
    N = []
    A = []
    for i in agentList.agent_names():
        N.append(i)
    for i in agentList.all_items():
        A.append(i)

    # Build bipartite graph
    g = nx.Graph()
    g.add_nodes_from(N, bipartite=0)
    g.add_nodes_from(A, bipartite=1)
    for i, k in zip(N, range(len(N))):
        for j in A:
            g.add_edge(i, j, weight=agentList[k].value(j))
    # max weight matching in graph
    alloc = nx.max_weight_matching(g, maxcardinality=True)
    dict_match = {}
    for i in alloc:
        if i[1] not in A:
            dict_match[i[1]] = i[0]
        else:
            dict_match[i[0]] = i[1]

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

    # Solve
    prob = cp.Problem(objective, constraints)
    result = prob.solve()

    # The result
    sigma = {}
    vector_p = {}
    for i in dict_match.keys():
        sigma[str(i)] = str(dict_match[i])
        vector_p[str(dict_match[i])] = round(float(variable["price " + dict_match[i]].value), 2)

    return sigma, vector_p


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
    budget_aware_graph.add_nodes_from(list(sigma.keys()))
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
    weak_envy_graph.add_nodes_from(list(sigma.keys()))
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


def LP1(µ:dict,rent , val: dict[dict],budget:dict):
    """
        This function for calculation of LP(1) from article.
        LP(1) is : Linear Programming of :
            max M
            M,pσ(1),...,pσ(n)
                    s.t.
                    ,
                    ∑_i∈N pσ(i) = r ,
                    ∀s ∈ [t] ,  x ≤ fs (v_1σ(1) − p_σ(1),...,v_nσ(n) − p_σ(n))
                    ∀i,j∈N, v_iσ(i) - p_σ(i) ≥ v_iσ(j) - p_σ(j)
                    ∀i∈N ,  p_σ(i) ≤b_i

        :param µ:  µ: N -> A
        :param rent: total rent house
        :param val: the valuation of each room by agent
        :param budget: total rent house
        :return: if LP(1) for μ is feasible return µ: N -> A , p : is vector of prices for each room Else
                "no solution"
        """
    variable = {}  # list of all the 'price' variables that present the price of any room
    for i in µ.values():
        variable["price " + str(i)] = cp.Variable()

    variable["M"] = cp.Variable()  # this variable care for the maximum
    objective = cp.Maximize(variable["M"])
    constraints = []
    # have 4 constrains
    # 1)  M <= v_iσ(i) - p_σ(i)
    for i in µ.keys():
        constraints.append(variable["M"] <= val[i][µ[i]] - variable["price " + µ[i]])

    # 2) Check that without envy -> v_iσ(i) - p_σ(i) ≥ v_iσ(j) - p_σ(j)
    for i in µ.keys():
        for j in µ.keys():
            if i != j:
                constraints.append(val[i][µ[i]] - variable["price " + µ[i]] >=
                                   val[i][µ[j]] - variable["price " + µ[j]])

    # 3) p_σ(i) ≤ b_i
    for i in µ.keys():
        constraints.append(variable["price " + µ[i]] <= budget[i])

    # 4) ∑ P_i = rent
    total = 0
    for i in µ.keys():
        total += variable["price " + µ[i]]
    constraints.append(total == rent)

    prob = cp.Problem(objective, constraints)
    result = prob.solve()

    if prob.status == 'optimal':
        sigma = {}
        vector_p = {}
        for i in µ.keys():
            sigma[str(i)] = str(µ[i])
            vector_p[str(µ[i])] = round(float(variable["price " + µ[i]].value), 2)
        return sigma, vector_p
    else:
        return "no solution"


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
