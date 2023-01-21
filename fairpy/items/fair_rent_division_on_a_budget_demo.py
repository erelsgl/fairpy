"""
    Demo for "Fair Rent Division on a Budget"

    Based on:
    "Fair Rent Division on a Budget" by Procaccia, A., Velez, R., & Yu, D. (2018), https://doi.org/10.1609/aaai.v32i1.11465

    Programmers: Daniel Sela and Asif Rot
    Date: 27-12-2022
"""
import fairpy
from fairpy.agentlist import AgentList
from fairpy.items.fair_rent_division_on_a_budget import optimal_envy_free

agentList1 = AgentList({'Alice': {'2ndFloor': 300, 'Basement': 250, 'MasterBedroom': 450},
                        'Bob': {'2ndFloor': 200, 'Basement': 300, 'MasterBedroom': 500},
                        'Clair': {'2ndFloor': 150, 'Basement': 500, 'MasterBedroom': 350}})

budget1 = {
    'Alice': 300,
    'Bob': 500,
    'Clair': 600,
}
rent1 = 1000

agentList2 = AgentList({
    'P1': {'Ra': 600, 'Rb': 100, 'Rc': 150, 'Rd': 150},
    'P2': {'Ra': 250, 'Rb': 250, 'Rc': 250, 'Rd': 250},
    'P3': {'Ra': 100, 'Rb': 400, 'Rc': 250, 'Rd': 250},
    'P4': {'Ra': 100, 'Rb': 200, 'Rc': 350, 'Rd': 350}
})
budget2 = {
    'P1': 600,
    'P2': 400,
    'P3': 400,
    'P4': 300
}
rent2 = 1000

print("solution agentList1")
print(fairpy.divide(algorithm=optimal_envy_free, input=agentList1, rent=rent1, budget=budget1))
print()
print("solution agentList2")
print(fairpy.divide(algorithm=optimal_envy_free, input=agentList2, rent=rent2, budget=budget2))
print("solution ex2")
ex2 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                 "Clair": {'1': 250, '2': 250, '3': 500}})

print(fairpy.divide(algorithm=optimal_envy_free, input=ex2, rent=1000, budget={'Alice': 300, 'Bob': 300, 'Clair': 300}))
