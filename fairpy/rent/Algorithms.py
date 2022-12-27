import networkx as nx
import numpy as np
from Calculation_Assistance import *
from fairpy.agentlist import AgentList


def algorithm_1(agentsList: AgentList, N: list, A: list, val: dict[dict], rent: float, budget: dict):
    sigma = {}
    p = {}
    sigma, p = spliddit(agentsList, rent)
    g = build_weak_envy_graph(sigma, p, val)
    components = nx.strongly_connected_components(g)
    for i in components:
        print(i)
    print()
    # delta = calculation_delta(sigma, p, val, rent, budget)
    # for i in sigma.keys():
    #     p[sigma[i]] = round(p[sigma[i]] - delta, 3)
    # rent -= delta
    budget_graph = build_budget_aware_graph(sigma, p, budget, val)
    while not check_while(budget_graph, budget, p, sigma):
        if not check_case_1(budget, p, sigma):
            temp = []
            for i in sigma.keys():
                temp.append(budget[i] - p[sigma[i]])
            delta = min(temp)
            for i in p.keys():
                p[i] += delta
            rent = rent + len(N) * delta
        else:
            sigma = case_2(sigma, p, budget, val)
        budget_graph = build_budget_aware_graph(sigma, p, budget, val)
    print(f"the max total rent is {rent} \nthe sigma is {sigma} \nthe vector p is {p}")
    return rent, (sigma, p)


def check_while(budget_graph, budget: dict, p: dict, sigma: dict):
    for i in sigma.keys():
        if budget[i] == p[sigma[i]]:
            cycle = nx.simple_cycles(budget_graph)
            for c in cycle:
                if i in c:
                    return True
    return False


def check_case_1(budget: dict, p: dict, sigma: dict):
    for i in sigma.keys():
        if budget[i] == p[sigma[i]]:
            return True
    return False


def case_2(sigma: dict, p: dict, budget: dict, agentsList: AgentList):
    """
        For reshuffle of sigma along cycle C of budget aware graph
    :return: new sigma
    """
    budget_graph = build_budget_aware_graph(sigma, p, budget, agentsList)
    for i in sigma.keys():
        if p[sigma[i]] == budget[i]:
            # find cycle in graph
            cycle = nx.simple_cycles(budget_graph)
            for c in cycle:
                if i in c:
                    temp = {}
                    # For reshuffle the rooms
                    for j in c:
                        temp[j] = sigma[j]
                    values = list(temp.values())
                    # Use the shuffle function to shuffle the values
                    random.shuffle(values)
                    # Create a new shuffled dictionary using the original keys and the shuffled values
                    shuffled_temp = {key: value for key, value in zip(temp.keys(), values)}
                    # for update new room for agent
                    for j in shuffled_temp.keys():
                        sigma[j] = shuffled_temp[j]
                    return sigma


def algorithm_2(N: list, A: list, agentsList: AgentList, rent: float, budget: dict):
    sigma = {}
    p = {}
    sigma, p = spliddit(agentsList, rent)  # compute (σ,p) ∈ F(N,A,v,r)
    graph = build_weak_envy_graph(sigma, p, agentsList)  # Γ(σ, p)
    SCC = nx.strongly_connected_components(graph)  # SCC = C , C ← strongly connected components of Γ(σ, p)
    ans_µc_pc = []
    """
    for each c ∈ C do:
        (μC,pC) ← output of Algorithm 1 on C, A(C), vC,and bC
    """
    for c in SCC:
        A_c = list([sigma[i] for i in sigma.keys() if i in c])
        V_c = {i: val[i] for i in sigma.keys() if i in c}
        B_c = {i: budget[i] for i in sigma.keys() if i in c}
        ans_µc_pc.append(algorithm_1(list(c), A_c, V_c, rent, B_c))
    # let μ:N →A
    µ = {}
    # for i in N:
    #     for c in SCC:
    #         if i in c:
    #             µ[i] =


if __name__ == '__main__':
    agentList1 = AgentList({'Alice': {'2ndFloor': 250, 'Basement': 250, 'MasterBedroom': 500},
                            'Bob': {'2ndFloor': 250, 'Basement': 250, 'MasterBedroom': 500},
                            'Clair': {'2ndFloor': 250, 'Basement': 500, 'MasterBedroom': 250}})

    lst = []
    for i in agentList1.all_items():
        lst.append(i)
    vals = []
    for i in range(len(agentList1.agent_names())):
        for j in agentList1.all_items():
            print(agentList1[i].value(j))
    print(vals)
    # N = ['Alice', 'Bob', 'Clair']
    # A = ['2ndFloor', 'Basement', 'MasterBedroom']
    # val = {
    #     'Alice': {'2ndFloor': 250, 'Basement': 250, 'MasterBedroom': 500},
    #     'Bob': {'2ndFloor': 250, 'Basement': 250, 'MasterBedroom': 500},
    #     'Clair': {'2ndFloor': 250, 'Basement': 500, 'MasterBedroom': 250},
    # }
    # budget = {
    #     'Alice': 200,
    #     'Bob': 100,
    #     'Clair': 200,
    # }
    # rent = 1000

    # N = ['P1', 'P2', 'P3', 'P4']
    # A = ['Ra', 'Rb', 'Rc', 'Rd']
    # val = {
    #     'P1': {'Ra': 600, 'Rb': 100, 'Rc': 150, 'Rd': 150},
    #     'P2': {'Ra': 250, 'Rb': 250, 'Rc': 250, 'Rd': 250},
    #     'P3': {'Ra': 100, 'Rb': 400, 'Rc': 250, 'Rd': 250},
    #     'P4': {'Ra': 100, 'Rb': 200, 'Rc': 350, 'Rd': 350}
    # }
    # budget = {
    #     'P1': 1000,
    #     'P2': 1000,
    #     'P3': 1000,
    #     'P4': 1000
    # }
    # rent = 1000
    #
    # ans = algorithm_1(N, A, agentList1, rent, budget)
