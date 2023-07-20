"""
Compare the performance of algorithms for fair course allocation, that return fractional allocations.

To run this file, you need
    pip install experiments_csv

Programmer: Erel Segal-Halevi
Since: 2023-07
"""
from fairpy.courses.fractional_egalitarian import *
from fairpy.courses import Instance
from typing import *
import numpy as np

agent_capacity_bounds =  [6,6]
item_capacity_bounds = [40,40]
max_value = 1000
normalized_sum_of_values = 1000


def course_allocation_with_random_instance(
    num_of_agents:int, num_of_items:int, 
    value_noise_ratio:float,
    algorithm:Callable,
    random_seed: int,):
    np.random.seed(random_seed)
    instance = Instance.random(
        num_of_agents=num_of_agents, num_of_items=num_of_items, normalized_sum_of_values=normalized_sum_of_values,
        agent_capacity_bounds=agent_capacity_bounds, 
        item_capacity_bounds=item_capacity_bounds, 
        item_base_value_bounds=[1,max_value],
        item_subjective_ratio_bounds=[1-value_noise_ratio, 1+value_noise_ratio]
        )
    allocation = algorithm(instance)
    return {
        
    }


if __name__ == "__main__":
    import logging, experiments_csv
    experiments_csv.logger.setLevel(logging.INFO)
    experiment = experiments_csv.Experiment("results/", "fractional_course_allocation.csv", backup_folder="results/backup/")

    TIME_LIMIT = 60
    input_ranges = {
        # "num_of_agents": [10,20,50,100,200,300],
        "num_of_agents": [10,20,50],
        # "num_of_items":  [5,10,20,30],
        "num_of_items":  [5,10,20],
        "value_noise_ratio": [0.3],
        "algorithm": [
            # fractional_egalitarian_allocation, 
            # fractional_egalitarian_utilitarian_allocation, 
            fractional_leximin_optimal_allocation, 
            ],
        "random_seed": range(5),
    }

    # fractional_leximin_optimal_allocation.logger.addHandler(logging.StreamHandler())
    # fractional_leximin_optimal_allocation.logger.setLevel(logging.DEBUG)
    # input_ranges_error = {
    #     "num_of_agents": [50],
    #     "num_of_items":  [5],
    #     "value_noise_ratio": [0.3],
    #     "algorithm": [fractional_leximin_optimal_allocation],
    #     "random_seed": [0],
    # }

    experiment.run_with_time_limit(course_allocation_with_random_instance, input_ranges, time_limit=TIME_LIMIT)


# RESULTS: 
# * egalitarian is fastest; 
# * egalitarian_utilitarian takes twice (naturally);
# * leximin is much slower.

