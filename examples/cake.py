#' # Fair cake-cutting algorithms

import fairpy
divide = fairpy.divide

#' Cake-cutting algorithms require `Agent` objects that can answer `mark` and `eval` queries.
#' Some such Agent objects are already defined.

from fairpy import PiecewiseUniformAgent, PiecewiseConstantAgent

#' Alice has two desired intervals, 0..1 and 3..6. Each interval has value 1:
Alice = PiecewiseUniformAgent ([(0,1),(3,6)], name="Alice")   
#' George has four desired intervals: 0..1 with value 1, 1..2 with value 3, etc:
George = PiecewiseConstantAgent([1,3,5,7],    name="George")  
print(Alice)
print(George)

#' Now, we can let our agents play 'cut and choose'.
from fairpy.cake import cut_and_choose

allocation = divide(cut_and_choose.asymmetric_protocol, [Alice, George])
print(allocation)

#' To better understand what is going on, we can use logging:

import logging, sys
cut_and_choose.logger.addHandler(logging.StreamHandler(sys.stdout))
cut_and_choose.logger.setLevel(logging.INFO)

print(divide(cut_and_choose.asymmetric_protocol, [Alice, George]))

#'

print(divide(cut_and_choose.asymmetric_protocol, [George, Alice]))

#' Here is another protocol - symmetric cut-and-choose:
print(divide(cut_and_choose.symmetric_protocol, [Alice, George]))

#' Here is an algorithm for more than two agents:

from fairpy.cake import last_diminisher

last_diminisher.logger.addHandler(logging.StreamHandler(sys.stdout))
last_diminisher.logger.setLevel(logging.INFO)

from fairpy.cake.valuations import PiecewiseConstantValuation
print(divide(last_diminisher.last_diminisher, [
    PiecewiseConstantValuation([1,3,5,7]), 
    PiecewiseConstantValuation([7,5,3,1]),
    PiecewiseConstantValuation([4,4,4,4]),
    PiecewiseConstantValuation([16,0,0,0]),
    ]))

#' To turn off logging:

cut_and_choose.logger.setLevel(logging.WARNING)

#' For more information see:
#'
#' * [List of cake-cutting algorithms currently implemented](../fairpy/cake/README.md).
#' * [List of cake-cutting algorithms for future work](../fairpy/cake/README-future.md).
