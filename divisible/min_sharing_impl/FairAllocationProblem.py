#!python3
"""
    An abstract class for solving a min-sharing fair allocation problem.

    Programmer: Eliyahu Sattat
    Since:  2020
"""


from fairpy.divisible.agents import ValuationMatrix
from fairpy.divisible.allocations import AllocationMatrix

from fairpy.divisible.min_sharing_impl.ConsumptionGraph import ConsumptionGraph
from fairpy.divisible.min_sharing_impl.GraphGenerator import GraphGenerator
from fairpy.divisible.max_product import product_of_utilities

from time_limit import time_limit, TimeoutException

from abc import ABC, abstractmethod
import datetime, cvxpy

import logging
logger = logging.getLogger(__name__)


class FairAllocationProblem():
    """
    ‎This is an abstract class for solving a fair allocation problem.
    """

    def __init__(self ,valuation:ValuationMatrix):
        valuation = ValuationMatrix(valuation)
        self.valuation = valuation
        self.min_sharing_number = valuation.num_of_agents
        self.min_sharing_allocation = None
        self.graph_generator = GraphGenerator(valuation)
        self.find = False

    @abstractmethod
    def fairness_adjective(self)->str:
        """ 
        Return an adjective that describes the fairness criterion. For display and logging.
        """
        return "fair" 

    @abstractmethod
    def find_allocation_for_graph(self, consumption_graph: ConsumptionGraph)->AllocationMatrix:
        """ 
        Find an allocatin that corresponds to the given consumption graph and satisfies the fairness criterion. 
        :return the allocation, or None if none found.
        """
        pass


    def find_allocation_with_min_sharing(self, min_sharing_allocation:int=3)->AllocationMatrix:
        """
        Runs the min-sharing algorithm on this valuation matrix.

        :return the allocation with min sharing satisfying the criterion of `find_allocation_for_graph`.
        """
        allowed_num_of_sharings = 0
        logger.info("")
        while (allowed_num_of_sharings < self.valuation.num_of_agents) and (not self.find):
            logger.info("Looking for %s allocations with %d sharings", self.fairness_adjective(), allowed_num_of_sharings)
            self.graph_generator.set_maximum_allowed_num_of_sharings(allowed_num_of_sharings)
            for consumption_graph in self.graph_generator.generate_all_consumption_graph():
                if consumption_graph.get_num_of_sharing() != allowed_num_of_sharings:
                    continue
                alloc = self.find_allocation_for_graph(consumption_graph)
                if alloc is None:
                    continue
                self.find = True
                self.min_sharing_allocation = alloc
                logger.info(" -- Found an allocation with %d sharings, for consumption graph: \n%s", allowed_num_of_sharings, consumption_graph)
                logger.debug("-- Unrounded allocation:\n%s", alloc)
                break
            if self.find:
                break
            allowed_num_of_sharings += 1
        alloc.round(min_sharing_allocation)
        self.min_sharing_number = alloc.num_of_sharings()
        if self.min_sharing_number >= self.valuation.num_of_agents:
            raise AssertionError("Num of sharings is {} but it should be at most {}.\n{}".format(self.min_sharing_number, self.valuation.num_of_agents-1,alloc))
        return self.min_sharing_allocation


    def find_min_sharing_allocation_with_time_limit(self, num_of_decimal_digits:int=3, time_limit_in_seconds=999)->(str,float,AllocationMatrix,float):
        """
        Wraps the above algorithm with a time-limit.

        :return (status, time_in_seconds, allocation_matrix, prod_of_utils)
        """
        start = datetime.datetime.now()
        try:
            with time_limit(time_limit_in_seconds):
                allocation_matrix = self.find_allocation_with_min_sharing()
                status = "OK" if allocation_matrix.num_of_sharings() < self.valuation.num_of_agents else "Bug"
                prod_of_utils = product_of_utilities(allocation_matrix, self.valuation)
        except TimeoutException:
            status = "TimeOut"
            prod_of_utils =  -1
            allocation_matrix = ErrorAllocationMatrix()
        except cvxpy.error.SolverError:
            status = "SolverError"
            prod_of_utils = -1
            allocation_matrix = ErrorAllocationMatrix()
        except SystemError:
            status = "SystemError"
            prod_of_utils =  -1
            allocation_matrix = ErrorAllocationMatrix()
        except AssertionError:  # Indicates too many sharings
            status = "Bug"
            prod_of_utils =  -1
            allocation_matrix = ErrorAllocationMatrix()
        end = datetime.datetime.now()
        time_in_seconds = (end - start).total_seconds()
        return (status, time_in_seconds, allocation_matrix, prod_of_utils)



class ErrorAllocationMatrix(AllocationMatrix):
    """
    An allocation matrix that denotes an error in the algorithm.
    """

    def __init__(self):
        pass

    def num_of_sharings(self): 
        return -1
