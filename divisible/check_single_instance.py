#!python3

from algorithm.Version3.FairEnvyFreeAllocationProblem import FairEnvyFreeAllocationProblem
from algorithm.Version3.FairProportionalAllocationProblem import FairProportionalAllocationProblem

from tee_table.tee_table import TeeTable
from collections import OrderedDict

from spliddit import spliddit_instances, spliddit_instance, SPLIDDIT_GOODS, SPLIDDIT_TASKS
from allocations import find_allocation_with_min_sharing

import numpy as np


import logging, sys
logger = logging.getLogger(__name__)

logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)



TABLE_COLUMNS = ["instance_id","num_agents","num_resources","prop_status", "prop_time_in_seconds", "prop_num_sharing", "ef_status", "ef_time_in_seconds","ef_num_sharing"]

def debug_instance(instance_id, time_limit_in_seconds=1000):
    valuation_matrix = spliddit_instance(instance_id)
    (num_agents, num_resources) = valuation_matrix.shape
    print("\nInstance: ", instance_id, "\nValuations: \n", valuation_matrix)
    print("{} agents, {} resources".format(num_agents, num_resources))

    problem = FairProportionalAllocationProblem(valuation_matrix)
    (prop_status, prop_time_in_seconds, prop_num_sharing, prop_allocation) = \
        find_allocation_with_min_sharing(problem, time_limit_in_seconds=time_limit_in_seconds)

    problem = FairEnvyFreeAllocationProblem(valuation_matrix)
    (ef_status, ef_time_in_seconds, ef_num_sharing, ef_allocation) = \
        find_allocation_with_min_sharing(problem, time_limit_in_seconds=time_limit_in_seconds)

    print("\nProportional Allocation: \n", np.round(prop_allocation, decimals=2))
    print("Status: {}, #sharing: {}, time: {}".format(prop_status, prop_num_sharing, prop_time_in_seconds))
    print("\nEnvy-Free Allocation: \n", np.round(ef_allocation, decimals=2))
    print("Status: {}, #sharing: {}, time: {}".format(ef_status, ef_num_sharing, ef_time_in_seconds))


def create_results(results_csv_file:str, first_instance_id=1, time_limit_in_seconds=998):
    """
    Read all Spliddit instances and check the minimum sharing allocation.
    """
    results_table = TeeTable(TABLE_COLUMNS, results_csv_file)

    prev_valuation_matrix = np.zeros((1,1))
    for (instance_id, valuation_matrix) in spliddit_instances(first_id=first_instance_id):
        (num_agents, num_resources) = valuation_matrix.shape
        print("\nInstance: ", instance_id, "\nValuations: \n", valuation_matrix)
        print("{} agents, {} resources".format(num_agents,num_resources))

        if (np.array_equal(valuation_matrix,prev_valuation_matrix)):
            prop_time_in_seconds = -1
            prop_num_sharing = -1
            prop_status = "Duplicate"
            prop_allocation = []
            ef_time_in_seconds = -1
            ef_num_sharing = -1
            ef_status = "Duplicate"
            ef_allocation = []
        else:
            problem = FairProportionalAllocationProblem(valuation_matrix)
            (prop_status, prop_time_in_seconds, prop_num_sharing, prop_allocation) = \
                find_allocation_with_min_sharing(problem, time_limit_in_seconds=time_limit_in_seconds)

            problem = FairEnvyFreeAllocationProblem(valuation_matrix)
            (ef_status, ef_time_in_seconds, ef_num_sharing, ef_allocation) = \
                find_allocation_with_min_sharing(problem, time_limit_in_seconds=time_limit_in_seconds)

        print("\nProportional Allocation: \n", np.round(prop_allocation, decimals=2))
        print("Status: {}, #sharing: {}, time: {}".format(prop_status, prop_num_sharing, prop_time_in_seconds))
        print("\nEnvy-Free Allocation: \n", np.round(ef_allocation, decimals=2))
        print("Status: {}, #sharing: {}, time: {}".format(ef_status, ef_num_sharing, ef_time_in_seconds))

        results_table.add(OrderedDict((
            ("instance_id", str(instance_id)),
            ("num_agents", num_agents),
            ("num_resources", num_resources),
            ("prop_status", prop_status),
            ("prop_time_in_seconds", prop_time_in_seconds),
            ("prop_num_sharing", prop_num_sharing),
            ("ef_status", ef_status),
            ("ef_time_in_seconds", ef_time_in_seconds),
            ("ef_num_sharing", ef_num_sharing),
        )))
        prev_valuation_matrix = valuation_matrix

    results_table.done()


if __name__ == "__main__":
    results_file="4-results/100sec.csv"
    # create_results(results_file, time_limit_in_seconds=98, first_instance_id=50067)
    debug_instance(18)
    # debug_instance(23)
    # debug_instance(39925)
