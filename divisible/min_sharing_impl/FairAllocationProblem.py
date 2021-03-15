#!python3

from fairpy.divisible.ValuationMatrix import ValuationMatrix
from fairpy.divisible.AllocationMatrix import AllocationMatrix

from fairpy.divisible.min_sharing_impl.ConsumptionGraph import ConsumptionGraph
from fairpy.divisible.min_sharing_impl.GraphGenerator import GraphGenerator


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

    def find_allocation_with_min_sharing(self, num_of_decimal_digits:int=3)->AllocationMatrix:
        allowed_num_of_sharings = 0
        while (allowed_num_of_sharings < self.valuation.num_of_agents) and (not self.find):
            self.graph_generator.set_num_of_sharing_is_allowed(allowed_num_of_sharings)
            for consumption_graph in self.graph_generator.generate_all_consumption_graph():
                if consumption_graph.get_num_of_sharing() != allowed_num_of_sharings:
                    continue
                alloc = self.find_allocation_for_graph(consumption_graph)
                if alloc is None:
                    continue
                self.find = True
                self.min_sharing_allocation = alloc
                logger.info("Found allocation for consumption graph \n%s\nwith %d allowed sharings:\n%s",consumption_graph, allowed_num_of_sharings,alloc)
                break
            if self.find:
                break
            allowed_num_of_sharings += 1

        alloc.round(num_of_decimal_digits)
        self.min_sharing_number = alloc.num_of_sharings()
        if self.min_sharing_number >= self.valuation.num_of_agents:
            raise AssertionError("Num of sharings is {} but it should be at most {}.\n{}".format(self.min_sharing_number, self.valuation.num_of_agents-1,alloc))
        return self.min_sharing_allocation



    def find_allocation_for_graph(self,consumption_graph : ConsumptionGraph):
        """ This is overriden in FairProportionalAllocationProblem and FairEnvyFreeAlllocationProblem """
        pass
