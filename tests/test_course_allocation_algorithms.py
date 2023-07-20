"""
Test that course-allocation algorithms return a feasible solution on random instances.

Programmer: Erel Segal-Halevi
Since:  2023-07
"""

import pytest

import fairpy.courses as crs
import numpy as np

      
# @pytest.mark.skip("Takes too long for pytest")
def test_feasibility():
    algorithms = [
        crs.utilitarian_matching, 
        crs.iterated_maximum_matching, 
        crs.serial_dictatorship,                  # Very bad performance
        # crs.course_allocation_by_proxy_auction,   # ValueError: Algorithm: course_allocation_by_proxy_auction: Agent s12 has capacity 2, but received more items: ['c3', 'c5', 'c10'].
        crs.round_robin, 
        crs.bidirectional_round_robin,
        crs.yekta_day,
        crs.almost_egalitarian_allocation,
        ]
    for i in range(10):
        np.random.seed(i)
        instance = crs.Instance.random(
            num_of_agents=70, num_of_items=10, normalized_sum_of_values=1000,
            agent_capacity_bounds=[2,6], 
            item_capacity_bounds=[20,40], 
            item_base_value_bounds=[1,1000],
            item_subjective_ratio_bounds=[0.5, 1.5]
            )
        for algorithm in algorithms:
            allocation = algorithm(instance)
            crs.validate_allocation(instance, allocation, title=f"Seed {i}, algorithm {algorithm.__name__}")

  
if __name__ == "__main__":
     pytest.main(["-v",__file__])

