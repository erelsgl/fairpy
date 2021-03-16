#!python3

from fairpy.divisible.agents import ValuationMatrix
from fairpy.divisible.allocations import AllocationMatrix

from fairpy.divisible.min_sharing_impl.ConsumptionGraph import ConsumptionGraph
from fairpy.divisible.min_sharing_impl.GraphGenerator import GraphGenerator

from abc import ABC, abstractmethod

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

    def find_allocation_with_min_sharing(self, num_of_decimal_digits:int=3)->AllocationMatrix:
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

        alloc.round(num_of_decimal_digits)
        self.min_sharing_number = alloc.num_of_sharings()
        if self.min_sharing_number >= self.valuation.num_of_agents:
            raise AssertionError("Num of sharings is {} but it should be at most {}.\n{}".format(self.min_sharing_number, self.valuation.num_of_agents-1,alloc))
        return self.min_sharing_allocation


