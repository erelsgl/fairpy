#' # Loggers
#' Many algorithms in fairpy use logging. This is useful for understanding how the algorithm works.
#' Logging is based on the standard python `logging` library:

import fairpy, sys, logging

instance = {
    "Ami": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Tami": {"green": 12, "red":8, "blue": 4, "yellow": 2} }

fairpy.items.round_robin.logger.addHandler(logging.StreamHandler(sys.stdout))
fairpy.items.round_robin.logger.setLevel(logging.INFO)
fairpy.items.round_robin(instance)

#' Another run with different parameters:

fairpy.items.round_robin(instance, agent_order=[1,0], items=["green", "red", "blue"])

#' You can turn off logging for each module separately:

fairpy.items.round_robin.logger.setLevel(logging.WARNING)
fairpy.items.round_robin(instance)
