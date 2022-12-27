import networkx as nx
import numpy as np
from Calculation_Assistance import *
from fairpy.agentlist import AgentList

"""
    "Fair Rent Division on a Budget"
    
    Based on:
    "Fair Rent Division on a Budget" by Procaccia, A., Velez, R., & Yu, D. (2018), https://doi.org/10.1609/aaai.v32i1.11465
    The algorithm calculates Maximum-rent envy-free allocation in a fully connected economy, or in simple words,
    calculates a fair rent division under budget constraints.
    
    Programmers: Daniel Sela and Asif Rot
    Date: 27-12-2022
"""
def maximum_rent_envy_free(agentsList: AgentList, rent: float, budget: dict):
    """
    This function implements Algorithm 1 from the article.
    :param agentsList: agent whit rooms and valuation for each room by agent
    :param rent: total rent house
    :budget: the budget of each agent
    :return: Maximum-rent envy-free allocation in a fully connected economy.
             sigma: N -> A , p : is vector of prices for each room
    """
    sigma = {}
    p = {}
    sigma, p = spliddit(agentsList, rent)

    # It is for calculate the ∆ let Δ ∈ R such that
    # (σ,(pa −Δ)a∈A)∈Fb(N,C,v,r−nΔ) and there is i∈N such that pσ(i) =bi
    temp = []
    for i in sigma.keys():
        temp.append(p[sigma[i]] - budget[i])
    delta = max(temp)

    # p ← (pσ(i) − Δ)i∈N
    for i in sigma.keys():
        p[sigma[i]] = round(p[sigma[i]] - delta, 3)
    # # r ← r−nΔ
    rent -= len(agentsList) * delta

    # budget_graph ---> Γ_b(σ,p) ≡ (N,E), where E = {(i, j) : viσ(i) −pσ(i) = viσ(j) −pσ(i) and pσ(j) < bi}
    budget_graph = build_budget_aware_graph(sigma, p, budget, agentsList)
    while not check_while(budget_graph, budget, p, sigma):
        # Case1
        if not check_case_1(budget, p, sigma):
            # Δ ← min i∈N (bi − pσ(i))
            temp = []
            for i in sigma.keys():
                temp.append(budget[i] - p[sigma[i]])
            delta = min(temp)
            # p ← (pa + Δ) a∈A
            for i in p.keys():
                p[i] += delta
            # r ← r + nΔ
            rent = rent + len(N) * delta
        # Case2
        else:
            sigma = case_2(sigma, p, budget, agentsList)
        # Update the new budget-aware graph
        budget_graph = build_budget_aware_graph(sigma, p, budget, val)
    # print(f"the max total rent is {rent} \nthe sigma is {sigma} \nthe vector p is {p}")
    return rent, (sigma, p)


def check_while(budget_graph, budget: dict, p: dict, sigma: dict):
    """
        Exist i∈N s.t. p_σ(i) =bi and i is not avertex of a cycle of Γb(σ, p)
        :return: if exist i return true
    """
    for i in sigma.keys():
        if budget[i] == p[sigma[i]]:
            cycle = nx.simple_cycles(budget_graph)
            x = list(cycle)
            if x == []:
                return True
            else:
                for c in cycle:
                    if i in c:
                        return True
    return False


def check_case_1(budget: dict, p: dict, sigma: dict):
    """
     exist i∈N s.t. pσ(i) =bi
     :return: if exist i return true
    """
    for i in sigma.keys():
        if budget[i] == p[sigma[i]]:
            return True
    return False


def case_2(sigma: dict, p: dict, budget: dict, agentsList: AgentList):
    """
        For reshuffle of sigma along cycle C of budget aware graph.
        find i∈N s.t.pσ(i) = bi and i is a vertex of a cycle C of Γb(σ, p)
        σ ← reshuffle of σ along C
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
    return sigma


def optimal_envy_free(agentsList: AgentList, rent: float, budget: dict):
    """
        This function implements Algorithm 2 from the article.
        :param agentsList: agent whit rooms and valuation for each room by agent
        :param rent: total rent house
        :budget: the budget of each agent
        :return:  Optimal envy-free allocation subject to budget constraints.
                 µ: N -> A , p : is vector of prices for each room
        """
    # line 124-132 : it take the typing agent List and moves to the component for comfortable
    N = list([i for i in agentsList.agent_names()])
    A = list([i for i in agentsList.all_items()])
    val = {}
    for i in N:
        tempA = {}
        for j in A:
            tempA[j] = agentsList[N.index(i)].value(j)
        val[i] = tempA
    # compute (σ,p) ∈ F(N,A,v,r)
    sigma = {}
    p = {}
    sigma, p = spliddit(agentsList, rent)  # compute (σ,p) ∈ F(N,A,v,r)

    # Γ(σ, p) : weak envy graph by Γ(σ,p) ≡ (N,E), where (i, j) ∈ E if and only if viσ(i) − pσ(i) = viσ(j) − pσ(j)
    # graph = Γ(σ, p)
    graph = build_weak_envy_graph(sigma, p, agentsList)
    # SCC = C , C ← strongly connected components of Γ(σ, p)
    SCC = nx.strongly_connected_components(graph)

    ans_µc_pc = []
    """
    for each c ∈ C do:
        (μ_c,p_c) ← output of Algorithm 1 on C, A(C), vC,and bC
    """
    lst_SCC = list(SCC)
    for c in lst_SCC:
        tempAgentC = {}
        # N_c = let N_c bet the set of agent from strongly connected components
        N_c = list([i for i in N if i in c])
        # A_c = let A(C) be the set of rooms received by agents in C
        A_c = list([sigma[i] for i in sigma.keys() if i in c])
        # let vC and B_c be the restrictions of the two vectors to C
        V_c = {}
        for i in c:
            tempA = {}
            for j in A_c:
                tempA[j] = agentsList[N_c.index(i)].value(j)
            V_c[i] = tempA
        B_c = {i: budget[i] for i in sigma.keys() if i in c}
        # New rent for calculated on c
        new_rent = sum(p[sigma[i]] for i in c)
        for i in c:
            tempAgentC[i] = V_c[i]
        # (μC,pC) ← output of Algorithm 1 on C, A(C), V_c, and B_c
        ans_µc_pc.append(maximum_rent_envy_free(AgentList(tempAgentC), new_rent, B_c))

    µ = {}
    # let μ:N →A s.t. for all i ∈ N , μ(i) = μ_C(i) for c ∈ C s.t. i ∈ C
    for i in agentsList.agent_names():
        for c in lst_SCC:
            if i in c:
                for j in ans_µc_pc:
                    µc = dict(j[1][0])
                    if i in µc:
                        µ[i] = µc[i]

    # if LP(1) for μ is feasible , ans_LP1 = (µ,p)
    ans_LP1 = LP1(µ, rent, val, budget)
    if ans_LP1 != "no solution":
        # p ← solution of LP (1) for μ return (μ, p)
        print(f"--------THE RESULT-------- \n µ : {ans_LP1[0]} , p : {ans_LP1[1]}")
        return ans_LP1
    else:
        print(f"--------THE RESULT-------- \n 'no solution'")
        return "no solution"


if __name__ == '__main__':
    agentList1 = AgentList({'Alice': {'2ndFloor': 250, 'Basement': 250, 'MasterBedroom': 500},
                            'Bob': {'2ndFloor': 250, 'Basement': 250, 'MasterBedroom': 500},
                            'Clair': {'2ndFloor': 250, 'Basement': 500, 'MasterBedroom': 250}})

    agentList2 = AgentList({
        'P1': {'Ra': 600, 'Rb': 100, 'Rc': 150, 'Rd': 150},
        'P2': {'Ra': 250, 'Rb': 250, 'Rc': 250, 'Rd': 250},
        'P3': {'Ra': 100, 'Rb': 400, 'Rc': 250, 'Rd': 250},
        'P4': {'Ra': 100, 'Rb': 200, 'Rc': 350, 'Rd': 350}
    })
    budget = {
        'P1': 600,
        'P2': 400,
        'P3': 400,
        'P4': 300
    }
    rent = 1000
    ans = optimal_envy_free(agentList2, rent, budget)
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
