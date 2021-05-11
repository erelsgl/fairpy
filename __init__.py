#!python3
# From  https://stackoverflow.com/a/49375740/827927
# import os, sys
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from fairpy.valuations import *
from fairpy.allocations import *
from fairpy.agents import *

class items:
	from fairpy.items.round_robin import round_robin
	from fairpy.items.max_product import max_product_allocation
