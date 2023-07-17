import pathlib

HERE = pathlib.Path(__file__).parent
__version__ = (HERE / "VERSION").read_text().strip()


from fairpy.valuations import *
from fairpy.allocations import *
from fairpy.families import *
from fairpy.agents import *
from fairpy.agentlist import *
from fairpy.adaptors import *
import fairpy.items as items

# class items:
# 	from fairpy.items.picking_sequence import round_robin
# 	from fairpy.items.max_welfare import max_sum_allocation, max_power_sum_allocation, max_product_allocation, max_minimum_allocation, max_welfare_allocation, max_welfare_allocation_for_families
# 	from fairpy.items.leximin import leximin_optimal_allocation, leximin_optimal_envyfree_allocation, leximin_optimal_allocation_for_families
# 	from fairpy.items.one_of_threehalves_mms import bidirectional_bag_filling
# 	from fairpy.items.utilitarian_matching import utilitarian_matching
# 	from fairpy.items.iterated_maximum_matching import iterated_maximum_matching
# 	from fairpy.items.min_sharing import proportional_allocation_with_min_sharing, envyfree_allocation_with_min_sharing, maxproduct_allocation_with_min_sharing
# 	from fairpy.items.bounded_sharing import proportional_allocation_with_bounded_sharing, efficient_envyfree_allocation_with_bounded_sharing
# 	from fairpy.items.propm_allocation import propm_allocation
# 	from fairpy.items.undercut_procedure import undercut
# 	from fairpy.items.approximation_maximin_share import three_quarters_MMS_allocation
# 	from fairpy.items.fairly_allocating_few_queries import two_agents_ef1, three_agents_IAV


# class courses:
# 	from fairpy.courses.picking_sequence import picking_sequence, round_robin, serial_dictatorship, bidirectional_round_robin
# 	from fairpy.courses.instance import Instance
# 	from fairpy.courses.adaptors import divide, divide_random_instance
# 	from fairpy.courses.satisfaction import AgentBundleValueMatrix
# 	from fairpy.courses.iterated_maximum_matching import iterated_maximum_matching
