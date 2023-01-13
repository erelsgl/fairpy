import doctest

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
    >>> agentList1 = AgentList({'P1': {'Ra': 600, 'Rb': 100, 'Rc': 150},'P2': {'Ra': 250, 'Rb': 250, 'Rc': 250},'P3': {'Ra': 100, 'Rb': 400, 'Rc': 250}})
    >>> spliddit(agentList1, 1000)
    ({'P1': 'Ra', 'P3': 'Rb', 'P2': 'Rc'}, {'Rc': 166.67, 'Rb': 316.67, 'Ra': 516.67})

    >>> agentList2 = AgentList({'P1': {'Ra': 500, 'Rb': 250, 'Rc': 250},'P2': {'Ra': 300, 'Rb': 400, 'Rc': 300},'P3': {'Ra': 700, 'Rb': 100, 'Rc': 200}})
    >>> spliddit(agentList2, 1000)
    ({'P3': 'Ra', 'P2': 'Rb', 'P1': 'Rc'}, {'Rc': 150.0, 'Rb': 250.0, 'Ra': 600.0})
    """
    # Taking the AgentList type and splitting it to lists and dictionary
    N = [i for i in agentList.agent_names()]
    A = [i for i in agentList.all_items()]

    # Build bipartite graph
    g = nx.Graph()
    g.add_nodes_from(N, bipartite=0)
    g.add_nodes_from(A, bipartite=1)

    [g.add_edge(i, j, weight=agentList[k].value(j)) for i, k in zip(N, range(len(N))) for j in A]
    # max weight matching in graph
    alloc = nx.max_weight_matching(g, maxcardinality=True)
    dict_match = {}
    for i in alloc:
        if i[1] not in A:
            dict_match[i[1]] = i[0]
        else:
            dict_match[i[0]] = i[1]

    # variable is a list of all the 'price' variables that present the price of any room
    variable = {f"price {i}": cp.Variable() for i in dict_match.values()}

    variable["M"] = cp.Variable()  # this variable care for the maximum
    objective = cp.Maximize(variable["M"])
    constraints = []

    # have 3 constrains
    # 1)  M <= v_(iσ(i)) - p_(σ(i))
    for i in dict_match.keys():
        constraints.append(variable["M"] <= agentList[N.index(i)].value(dict_match[i]) - variable["price " + dict_match[i]])
    constraints = [variable["M"] <= agentList[N.index(i)].value(dict_match[i]) - variable[f"price {dict_match[i]}"] for
                   i in dict_match.keys()]

    # 2) Check that without envy -> v_(iσ(i)) - p_(σ(i)) ≥ v_(iσ(j)) - p_(σ(j))
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
    sigma = {str(i): str(dict_match[i]) for i in dict_match.keys()}
    vector_p = {str(dict_match[i]): round(float(variable["price " + dict_match[i]].value), 2) for i in dict_match.keys()}

    sigma = dict(sorted(sigma.items(), key=lambda x: x[1]))
    vector_p = dict(sorted(vector_p.items(), key=lambda x: x[1]))
    return sigma, vector_p


def build_budget_aware_graph(sigma: dict, vector_p: dict, budget: dict, agentList: AgentList) -> nx.DiGraph:
    """
        This function build budget aware envy graph ,Γ_b(σ, p) ≡ (N,E) , where
        E = {(i, j) : v_(iσ(i)) - p_(σ(i)) = v_(iσ(j)) - p_(σ(i)) and p_(σ(j)) < b_i}
    :param sigma: Dictionary for room per agent
    :param vector_p: Vector of prices for each room
    :param budget: Agents' budget
    :param val: The values of room per agent
    :return: Directed Graph
    """
    budget_aware_graph = nx.DiGraph()
    budget_aware_graph.add_nodes_from(list(sigma.keys()))
    for i in sigma.keys():
        for j in sigma.keys():
            if not i == j:
                left = agentList[agentList.agent_names().index(i)].value(sigma[i]) - vector_p[sigma[i]]
                # building budget aware weak envy graph --> v_(iσ(i)) - p_(σ(i)) = v_(iσ(j)) - p_(σ(i)) and p_(σ(j)) < b_i
                if left == (agentList[agentList.agent_names().index(i)].value(sigma[j]) - vector_p[sigma[i]]) and budget[i] > vector_p[sigma[j]]:
                    budget_aware_graph.add_edge(i, j)

    return budget_aware_graph


def build_weak_envy_graph(sigma: dict, vector_p: dict, agentList: AgentList) -> nx.DiGraph:
    """
        This function for build weak envy graph , Γ(σ, p) ≡ (N,E) ,where
        (i, j) ∈ E if and only if v_iσ(i) - p_σ(i) = v_iσ(j) - p_σ(j)
    :param sigma: Dictionary for room per agent
    :param vector_p: Vector of prices for each room
    :param val: The values of room per agent
    :return: Directed Graph
    """
    weak_envy_graph = nx.DiGraph()
    weak_envy_graph.add_nodes_from(list(sigma.keys()))
    for i in sigma.keys():
        for j in sigma.keys():
            if not i == j:
                left = (agentList[agentList.agent_names().index(i)].value(sigma[i]) - vector_p[sigma[i]])
                # to build weak envy graph --> v_iσ(i) - p_σ(i) = v_iσ(j) - p_σ(j)
                if left == (agentList[agentList.agent_names().index(i)].value(sigma[j]) - vector_p[sigma[j]]):
                    weak_envy_graph.add_edge(i, j)
    return weak_envy_graph


def LP1(µ: dict, rent, val: dict, budget: dict):
    """
        This function is for calculation of LP(1) from the article.
        LP(1) is : Linear Programming of :
            max M
    {M,pσ(1),...,pσ(n)}
                    s.t.
                    ∑_i∈N p(σ(i)) = r,
                    ∀s ∈ [t],  M ≤ fs (v_(1σ(1)) − p_(σ(1)), ..., v_(nσ(n)) − p_(σ(n)))
                    ∀i,j∈N, v_(iσ(i)) - p_(σ(i)) ≥ v_(iσ(j)) - p_(σ(j))
                    ∀i∈N,  p_(σ(i)) ≤ b_i

        :param µ:  µ: N -> A
        :param rent: Total rent
        :param val: Evaluation for each room by agent
        :param budget: Each agent's budget
        :return: if LP(1) for μ is feasible return µ: N -> A , p : is vector of prices for each room Else
                "no solution"
        >>> agentList1 = AgentList({'P1': {'Ra': 600, 'Rb': 100, 'Rc': 150},'P2': {'Ra': 250, 'Rb': 250, 'Rc': 250},'P3': {'Ra': 100, 'Rb': 400, 'Rc': 250}})
        >>> µ , p = spliddit(agentList1, 1000)
        >>> val = {'P1': {'Ra': 600, 'Rb': 100, 'Rc': 150},'P2': {'Ra': 250, 'Rb': 250, 'Rc': 250},'P3': {'Ra': 100, 'Rb': 400, 'Rc': 250}}
        >>> LP1(µ,1000,val,{'P1':500,'P2':500,'P3':400})
        ({'P1': 'Ra', 'P3': 'Rb', 'P2': 'Rc'}, {'Ra': 500.0, 'Rb': 325.0, 'Rc': 175.0})

         >>> agentList2 = AgentList({'P1': {'Ra': 500, 'Rb': 250, 'Rc': 250},'P2': {'Ra': 300, 'Rb': 400, 'Rc': 300},'P3': {'Ra': 700, 'Rb': 100, 'Rc': 200}})
         >>> µ , p = spliddit(agentList2, 1000)
         >>> val = {'P1': {'Ra': 500, 'Rb': 250, 'Rc': 250},'P2': {'Ra': 300, 'Rb': 400, 'Rc': 300},'P3': {'Ra': 700, 'Rb': 100, 'Rc': 200}}
         >>> LP1(µ,1000,val,{'P1':200,'P2':400,'P3':700})
         ({'P3': 'Ra', 'P2': 'Rb', 'P1': 'Rc'}, {'Ra': 600.0, 'Rb': 250.0, 'Rc': 150.0})
        """
    # variable = {}  # list of all the 'price' variables that present the price of any room
    variable = {f"price {i}": cp.Variable() for i in µ.values()}

    variable["M"] = cp.Variable()  # this variable care for the maximum
    objective = cp.Maximize(variable["M"])
    constraints = []
    # have 4 constrains
    # 1)  M <= v_(iσ(i)) - p_(σ(i))
    for i in µ.keys():
        constraints.append(variable["M"] <= val[i][µ[i]] - variable["price " + µ[i]])

    # 2) Check that without envy -> v_(iσ(i)) - p_(σ(i)) ≥ v_(iσ(j)) - p_(σ(j))
    for i in µ.keys():
        for j in µ.keys():
            if i != j:
                constraints.append(val[i][µ[i]] - variable["price " + µ[i]] >=
                                   val[i][µ[j]] - variable["price " + µ[j]])

    # 3) p_(σ(i)) ≤ b_i
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
        sigma = {str(i): str(µ[i]) for i in µ.keys()}
        vector_p = {str(µ[i]): round(float(variable["price " + µ[i]].value), 2) for i in µ.keys()}
        return sigma, vector_p
    else:
        return "no solution"


if __name__ == '__main__':
    doctest.testmod()
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
