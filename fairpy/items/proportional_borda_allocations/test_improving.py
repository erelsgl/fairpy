

from fairpy.items.proportional_borda_allocations.proportional_borda_allocations import *
from fairpy import AgentList
import pytest
from itertools import permutations
from typing import Callable
from itertools import chain
import utils
import improvingPreformance.utilsCpp as utilsCpp



def test_general():

    big_size = 50
    for n in chain(range(1, 20)):
        for p in chain(range(2,15), [big_size, big_size+1]):
            agentsI = get_agents_with_permutations_of_valuations(n, n*p)
            if utils.isEven(p):
                allocationI = proportional_division_with_p_even(agents=agentsI)
                assert is_proportional(allocationI, agentsI.all_items())
            if not utils.isEven(n):
                allocationI = proportional_division_with_number_of_agents_odd(agents=agentsI)
                assert is_proportional(allocationI, agentsI.all_items())
            allocationI = proportional_division(agents=agentsI)
            if utils.isEven(n) and not utils.isEven(p):
                assert is_proportional(allocationI, agentsI.all_items(), approximately=True)
            else:
                assert is_proportional(allocationI, agentsI.all_items())