#!python3

""" 
A demo program for finding welfare maximizing allocations with constraints.

Author: Erel Segal-Halevi
Since:  2021-05
"""
import fairpy
divide = fairpy.divide
from fairpy import Allocation
from fairpy.items.max_welfare import *
from fairpy.items.leximin import *
import numpy as np

import sys
logger.addHandler(logging.StreamHandler(sys.stdout))
# logger.setLevel(logging.INFO)


def show(title:str, z:Allocation, v:ValuationMatrix):
    utility_profile = z.utility_profile()
    utility_profile_matrix = z.utility_profile_matrix()
    print("\n", title, " = \n",z, "\n", utility_profile_matrix,"\n","product = ", np.prod(utility_profile))


def test(title:str, v:dict):
    print(f"\n\n{title}:")
    print("v = \n",v)
    # z = max_welfare_allocation(v,
    #         welfare_function=lambda utilities: sum([cvxpy.log(utility) for utility in utilities])
    #         ).round(3)
    # show("max-product",z,v)

    # z = max_welfare_allocation(v,
    #         welfare_function=lambda utilities: sum([cvxpy.log(utility) for utility in utilities]),
    #         allocation_constraint_function=lambda z: sum(z)==1
    #         ).round(3)
    # show("balanced max-product",z,v)

    # z = max_welfare_envyfree_allocation(v,
    #         welfare_function=lambda utilities: sum([cvxpy.log(utility) for utility in utilities]),
    #         allocation_constraint_function=lambda z: sum(z)==1
    #         ).round(3)
    # show("balanced-EF max-product",z,v)

    # z = max_welfare_allocation(v,
    #         welfare_function=lambda utilities: sum(utilities),
    #         allocation_constraint_function=lambda z: sum(z)==1
    #         ).round(3)
    # show("balanced max-sum",z,v)

    # z = max_welfare_envyfree_allocation(v,
    #         welfare_function=lambda utilities: sum(utilities),
    #         allocation_constraint_function=lambda z: sum(z)==1
    #         ).round(3)
    # show("balanced-EF max-sum",z,v)

    # z = max_welfare_allocation(v,
    #         welfare_function=lambda utilities: cvxpy.min(cvxpy.hstack(utilities)),
    #         allocation_constraint_function=lambda z: sum(z)==1
    #         ).round(3)
    # show("balanced max-min",z,v)

    # z = max_welfare_envyfree_allocation(v,
    #         welfare_function=lambda utilities: cvxpy.min(cvxpy.hstack(utilities)),
    #         allocation_constraint_function=lambda z: sum(z)==1
    #         ).round(3)
    # show("balanced-EF max-min",z,v)

    z = divide(leximin_optimal_allocation, v,
            allocation_constraint_function=lambda z: sum(z)==1
            ).round(3)
    show("balanced leximin",z,v)

    z = divide(leximin_optimal_envyfree_allocation, v,
            allocation_constraint_function=lambda z: sum(z)==1
            ).round(3)
    show("balanced-EF leximin",z,v)

    original_utilities = z.utility_profile()
    z = divide(pareto_dominating_allocation, v,
            original_utilities,
            allocation_constraint_function=lambda z: sum(z)==1
            ).round(3)
    new_utilities = z.utility_profile()
    if np.allclose(original_utilities,new_utilities):
        show("No Pareto-improvement! ",z,v)
        print("No Pareto improvement!")
    else:
        show("Pareto-improvement! ",z,v)

# test("Two goods and two agents",
#     v = {"Alice": [6,12] , "Bob": [12,18]})

def random_normalized_valuations(n:int):
    vals = np.random.randint(1,100,n)
    return vals*100/sum(vals)

test("Three goods and three agents",
    # v = {"Alice": np.random.randint(1,100,3) , "Bob": np.random.randint(1,100,3) , "Carl": np.random.randint(1,100,3)}
    # v = {"Alice": random_normalized_valuations(3) , "Bob": random_normalized_valuations(3) , "Carl": random_normalized_valuations(3)}
    # v = {'Alice': [50, 49, 1], 'Bob': [49, 50, 1], 'Chana': [1, 50, 49]}
    v = {'Alice': [60, 30, 10], 'Bob': [30, 40, 30], 'Carl': [10, 50, 40]},
    )
