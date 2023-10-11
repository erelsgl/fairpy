"""
Compare the performance of algorithms for fair course allocation.

To run this file, you need
    pip install experiments_csv

Programmer: Erel Segal-Halevi
Since: 2023-07
"""
import fairpy.courses as crs
from fairpy.courses.adaptors import divide
from typing import *
import numpy as np

max_value = 1000
normalized_sum_of_values = 1000


def course_allocation_with_random_instance_uniform(
    num_of_agents:int, num_of_items:int, 
    value_noise_ratio:float,
    algorithm:Callable,
    random_seed: int,):
    agent_capacity_bounds =  [6,6]
    item_capacity_bounds = [40,40]    
    np.random.seed(random_seed)
    instance = crs.Instance.random_uniform(
        num_of_agents=num_of_agents, num_of_items=num_of_items, normalized_sum_of_values=normalized_sum_of_values,
        agent_capacity_bounds=[6,6], 
        item_capacity_bounds=item_capacity_bounds, 
        item_base_value_bounds=[1,max_value],
        item_subjective_ratio_bounds=[1-value_noise_ratio, 1+value_noise_ratio]
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


def course_allocation_with_random_instance_szws(
    num_of_agents:int, num_of_items:int, 
    agent_capacity:int,
    supply_ratio:float,
    num_of_popular_items:int,
    mean_num_of_favorite_items:float,
    favorite_item_value_bounds:tuple[int,int],
    nonfavorite_item_value_bounds:tuple[int,int],
    algorithm:Callable,
    random_seed: int,):
    np.random.seed(random_seed)
    instance = crs.Instance.random_szws(
        num_of_agents=num_of_agents, num_of_items=num_of_items, normalized_sum_of_values=normalized_sum_of_values,
        agent_capacity=agent_capacity, 
        supply_ratio=supply_ratio, 
        num_of_popular_items=num_of_popular_items,
        mean_num_of_favorite_items=mean_num_of_favorite_items,
        favorite_item_value_bounds=favorite_item_value_bounds,
        nonfavorite_item_value_bounds=nonfavorite_item_value_bounds,
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
    experiment = experiments_csv.Experiment("results/", "course_allocation_szws.csv", backup_folder="results/backup/")

    TIME_LIMIT = 100

    # crs.almost_egalitarian_allocation.logger.addHandler(logging.StreamHandler())
    # crs.almost_egalitarian_allocation.logger.setLevel(logging.WARNING)

    input_ranges = {
        "num_of_agents": [100,200,300],                 # in SZWS: 100
        "num_of_items":  [25],                          # in SZWS: 25
        "agent_capacity": [5],                          # as in SZWS 
        "supply_ratio": [1.1, 1.25, 1.5],                    # as in SZWS
        "num_of_popular_items": [6, 9],                 # as in SZWS
        "mean_num_of_favorite_items": [2.6, 3.85],   # as in SZWS code https://github.com/marketdesignresearch/Course-Match-Preference-Simulator/blob/main/preference_generator_demo.ipynb
        "favorite_item_value_bounds": [(50,100)],         # as in SZWS code https://github.com/marketdesignresearch/Course-Match-Preference-Simulator/blob/main/preference_generator.py
        "nonfavorite_item_value_bounds": [(0,50)],        # as in SZWS code https://github.com/marketdesignresearch/Course-Match-Preference-Simulator/blob/main/preference_generator.py
        "algorithm": [
            crs.utilitarian_matching, 
            crs.iterated_maximum_matching_unadjusted, 
            crs.iterated_maximum_matching_adjusted, 
            # crs.serial_dictatorship,                  # Very bad performance
            # crs.course_allocation_by_proxy_auction,   # Very bad performance
            crs.round_robin, 
            crs.bidirectional_round_robin,
            crs.yekta_day,
            crs.almost_egalitarian_without_donation,
            crs.almost_egalitarian_with_donation,
            ],
        "random_seed": range(5),
    }
    experiment.run_with_time_limit(course_allocation_with_random_instance_szws, input_ranges, time_limit=TIME_LIMIT)

