#!python3
"""
    An abstract class for solving a min-sharing fair allocation problem.

    Programmer: Eliyahu Sattat
    Since:  2020
"""


from fairpy import ValuationMatrix, AllocationMatrix

from fairpy.items.min_sharing_impl.ConsumptionGraph import ConsumptionGraph
from fairpy.items.min_sharing_impl.GraphGenerator import GraphGenerator

from fairpy.items.min_sharing_impl.time_limit import time_limit, TimeoutException

from abc import ABC, abstractmethod
import datetime, cvxpy, numpy as np
from typing import Tuple

import logging
logger = logging.getLogger(__name__)


class FairAllocationProblem(ABC):
    """
    This is an abstract class for solving a fair allocation problem.
    """

    def __init__(self ,valuation_matrix:ValuationMatrix):
        assert isinstance(valuation_matrix, ValuationMatrix)
        self.valuation = valuation_matrix
        self.min_sharing_number = valuation_matrix.num_of_agents
        self.min_sharing_allocation = None
        self.graph_generator = GraphGenerator(valuation_matrix)
        self.find = False

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
        return None


    def find_allocation_for_all_graphs_with_numsharings(self, allowed_num_of_sharings:int)->AllocationMatrix:
        allocation = None
        logger.info("Looking for %s allocations with %d sharings", self.fairness_adjective(), allowed_num_of_sharings)
        self.graph_generator.set_maximum_allowed_num_of_sharings(allowed_num_of_sharings)
        for consumption_graph in self.graph_generator.generate_all_consumption_graph():
            if consumption_graph.get_num_of_sharing() != allowed_num_of_sharings:
                continue
            allocation = self.find_allocation_for_graph(consumption_graph)
            if allocation is not None:
                logger.info(" -- Found an allocation with %d sharings, for consumption graph: \n%s", allowed_num_of_sharings, consumption_graph)
                logger.debug("-- Unrounded allocation:\n%s", allocation)
                break
        return allocation


    def find_allocation_with_min_sharing(self, num_of_decimal_digits:int=3)->AllocationMatrix:
        """
        Runs the min-sharing algorithm on this valuation matrix.

        :return the allocation with min sharing satisfying the criterion of `find_allocation_for_graph`.
        """
        allowed_num_of_sharings = 0
        logger.info("")
        allocation = None
        while (allowed_num_of_sharings < self.valuation.num_of_agents) and (not self.find):
            allocation = self.find_allocation_for_all_graphs_with_numsharings(allowed_num_of_sharings)
            if allocation is not None:
                break
            allowed_num_of_sharings += 1
        if allocation is None:
            raise AssertionError("No allocation found")
        allocation.round(num_of_decimal_digits)
        if allocation.num_of_sharings() >= self.valuation.num_of_agents:
            raise AssertionError("Num of sharings is {} but it should be at most {}.\n{}".format(self.min_sharing_number, self.valuation.num_of_agents-1,allocation))
        return allocation


    def find_min_sharing_allocation_with_time_limit(self, num_of_decimal_digits:int=3, time_limit_in_seconds=999)->Tuple[str,float,AllocationMatrix,float]:
        """
        Wraps the above algorithm with a time-limit.

        :return (status, time_in_seconds, allocation_matrix, prod_of_utils)
        """
        start = datetime.datetime.now()
        try:
            with time_limit(time_limit_in_seconds):
                allocation_matrix = self.find_allocation_with_min_sharing()
                status = "OK" if allocation_matrix.num_of_sharings() < self.valuation.num_of_agents else "Bug"
        except TimeoutException:
            status = "TimeOut"
            allocation_matrix = ErrorAllocationMatrix(default_num_of_sharings=self.valuation.num_of_agents-1)
        except cvxpy.error.SolverError:
            status = "SolverError"
            allocation_matrix = ErrorAllocationMatrix(default_num_of_sharings=self.valuation.num_of_agents-1)
        except SystemError:
            status = "SystemError"
            allocation_matrix = ErrorAllocationMatrix(default_num_of_sharings=self.valuation.num_of_agents-1)
        except AssertionError:  # Indicates too many sharings
            status = "Bug"
            allocation_matrix = ErrorAllocationMatrix(default_num_of_sharings=self.valuation.num_of_agents-1)
        end = datetime.datetime.now()
        time_in_seconds = (end - start).total_seconds()
        return (status, time_in_seconds, allocation_matrix)



class ErrorAllocationMatrix(AllocationMatrix):
    """
    An allocation matrix that denotes time-out or another error in the algorithm.
    """

    def __init__(self, default_num_of_sharings:int):
        self.default_num_of_sharings = default_num_of_sharings
        pass

    def num_of_sharings(self): 
        return self.default_num_of_sharings

    def __repr__(self):
        return "ErrorAllocationMatrix"

