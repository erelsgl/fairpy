"""
Compare the performance of algorithms for the many-to-many matching problem.

To run this file, you need
    pip install experiments_csv


Programmer: Erel Segal-Halevi
Since: 2023-07
"""

from fairpy.courses.graph_utils import many_to_many_matching_using_network_flow, many_to_many_matching_using_node_cloning
from fairpy.courses.instance import Instance
from typing import *
import numpy as np

def many_to_many_matching_on_random_instance(
    num_of_agents:int, num_of_items:int, 
    agent_capacity:int,
    item_capacity:int,
    max_value:int,
    normalized_sum_of_values:int,
    random_seed: int, # dummy parameter, to allow multiple instances of the same run
    algorithm:Callable):
    np.random.seed()
    instance = Instance.random_uniform(
        num_of_agents=num_of_agents, num_of_items=num_of_items, normalized_sum_of_values=normalized_sum_of_values,
        agent_capacity_bounds=[agent_capacity,agent_capacity], 
        item_capacity_bounds=[item_capacity,item_capacity], 
        item_value_bounds=[1,max_value])
    allocation = algorithm(
         agents=instance.agents, agent_capacity=instance.agent_capacity,
         items=instance.items, item_capacity=instance.item_capacity,
         agent_item_value=instance.agent_item_value)
    return {
        "matching_size": sum([len(bundle) for agent,bundle in allocation.items()])
    }


if __name__ == "__main__":
    import logging, experiments_csv
    experiments_csv.logger.setLevel(logging.INFO)
    experiment = experiments_csv.Experiment("results/", "many_to_many_matchings.csv", backup_folder=None)

    TIME_LIMIT = 100
    input_ranges = {
        "num_of_agents": [10,20,40,80,160],
        "num_of_items":  [10,20,40,80,160],
        "agent_capacity": [1, 2, 4, 8, 16],
        "item_capacity": [1, 2, 4, 8, 16],
        "max_value": [10, 100, 1000],
        "normalized_sum_of_values": [1000],
        "algorithm": [many_to_many_matching_using_network_flow, many_to_many_matching_using_node_cloning],
        "random_seed": range(5),
    }
    experiment.run_with_time_limit(many_to_many_matching_on_random_instance, input_ranges, time_limit=TIME_LIMIT)


# RESULTS: decisive victory to many_to_many_matching_using_network_flow.
