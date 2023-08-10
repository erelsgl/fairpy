"""
Check whether using long agent and item names as keys affects the runtime performance of algorithms for fair course allocation.

To run this file, you need
    pip install experiments_csv

Programmer: Erel Segal-Halevi
Since: 2023-08
"""
import fairpy.courses as crs
from fairpy.courses.adaptors import divide
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
    agent_name_size:int, item_name_size:int,
    random_seed: int,):
    np.random.seed(random_seed)
    instance = crs.Instance.random(
        num_of_agents=num_of_agents, num_of_items=num_of_items, normalized_sum_of_values=normalized_sum_of_values,
        agent_capacity_bounds=agent_capacity_bounds, 
        item_capacity_bounds=item_capacity_bounds, 
        item_base_value_bounds=[1,max_value],
        item_subjective_ratio_bounds=[1-value_noise_ratio, 1+value_noise_ratio],
        agent_name_template= ("s"*agent_name_size)+"{index}",
        item_name_template= ("c"*agent_name_size)+"{index}",
        )
    allocation = divide(algorithm, instance)
    matrix = crs.AgentBundleValueMatrix(instance, allocation)
    matrix.use_normalized_values()
    return {
        "utilitarian_value": matrix.utilitarian_value(),
        "egalitarian_value": matrix.egalitarian_value(),
        "max_envy": matrix.max_envy(),
        "mean_envy": matrix.mean_envy(),
        "max_deficit": matrix.max_deficit(),
        "mean_deficit": matrix.mean_deficit(),
        "num_with_top_1": matrix.count_agents_with_top_rank(1),
        "num_with_top_2": matrix.count_agents_with_top_rank(2),
        "num_with_top_3": matrix.count_agents_with_top_rank(3),
    }


if __name__ == "__main__":
    import logging, experiments_csv
    experiments_csv.logger.setLevel(logging.INFO)
    experiment = experiments_csv.Experiment("results/", "check_effect_of_name_size.csv", backup_folder="results/backup/")

    TIME_LIMIT = 100

    crs.almost_egalitarian_allocation.logger.addHandler(logging.StreamHandler())
    crs.almost_egalitarian_allocation.logger.setLevel(logging.WARNING)

    input_ranges = {
        "num_of_agents": [300],
        "num_of_items":  [30],
        "value_noise_ratio": [0.5],
        "agent_name_size": [1,10,100,1000],
        "item_name_size": [1,10,100,1000],
        "algorithm": [
            crs.iterated_maximum_matching_adjusted, 
            crs.bidirectional_round_robin,
            ],
        "random_seed": range(5),
    }
    experiment.run_with_time_limit(course_allocation_with_random_instance, input_ranges, time_limit=TIME_LIMIT)



# RESULTS: No effect at all.
