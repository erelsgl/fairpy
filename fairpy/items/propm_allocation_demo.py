import fairpy
from fairpy.items.propm_allocation import propm_allocation

import logging
propm_allocation.logger.addHandler(logging.StreamHandler())
propm_allocation.logger.setLevel(logging.INFO)

instance1 = {
    'agent0': 
        {'x0': 282.0, 'x1': 0.0, 'x2': 118.0, 'x3': 18.0, 'x4': 0.0, 'x5': 282.0, 'x6': 282.0, 'x7': 18.0}, 
    'agent1': 
        {'x0': 177.0, 'x1': 39.0, 'x2': 180.0, 'x3': 62.0, 'x4': 187.0, 'x5': 53.0, 'x6': 192.0, 'x7': 110.0}
}
print(fairpy.divide(propm_allocation, instance1))


instance2 = {
    'agent0': {'x0': 0.0, 'x1': 1000.0}, 
    'agent1': {'x0': 0.0, 'x1': 1000.0}
}
print(fairpy.divide(propm_allocation, instance2))
