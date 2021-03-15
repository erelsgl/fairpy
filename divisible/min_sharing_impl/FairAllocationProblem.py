#!python3

from fairpy.divisible.min_sharing_impl.ConsumptionGraph import ConsumptionGraph
from fairpy.divisible.min_sharing_impl.GraphGenerator import GraphGenerator
from fairpy.divisible.ValuationMatrix import ValuationMatrix
from fairpy.divisible.AllocationMatrix import AllocationMatrix


class FairAllocationProblem():
    """
    this class is abstract class for solve Fair Allocation Problem
    meaning - get agents valuation and a Fair Allocation
    """


    def __init__(self ,valuation:ValuationMatrix):
        valuation = ValuationMatrix(valuation)
        self.valuation = valuation
        self.num_of_agents = valuation.num_of_agents
        self.num_of_items = valuation.num_of_objects
        self.min_sharing_number = self.num_of_agents
        self.min_sharing_allocation = None
        self.graph_generator = GraphGenerator(valuation)
        self.find = False

    def find_allocation_with_min_shering(self):
        i = 0
        while (i < self.num_of_agents) and (not self.find):
            self.graph_generator.set_num_of_sharing_is_allowed(i)
            for consumption_graph in self.graph_generator.generate_all_consumption_graph():
                self.find_allocation_for_graph(consumption_graph)
            if self.find:
                break
            i += 1

        self.min_sharing_number = i
        if self.min_sharing_number >= self.num_of_agents:
            raise AssertionError("Num of sharings is {} but it should be at most {}", self.min_sharing_number, self.num_of_agents-1)
        return self.min_sharing_allocation



    def find_allocation_for_graph(self,consumption_graph : ConsumptionGraph):
        """ This is overriden in FairProportionalAllocationProblem and FairEnvyFreeAlllocationProblem """
        pass
