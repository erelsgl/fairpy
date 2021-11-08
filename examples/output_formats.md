# Output formats

The output of a fair division algorithm in `fairpy` is usually an `Allocation` object.
The following code runs an algorithm for weighted utilitarian matching: 
there are discrete items with different capacities, and there are agents with different capacities and different weights.
The goal is to assign items to agents such that the weighted sum of utilities is maximum.

```python
from fairpy.items import utilitarian_matching
agent_values = {"avi": {"x":5, "y": 4}, "beni": {"x":2, "y":3}, "gadi": {"x":3, "y":2}}
agent_capacities = {"avi":2,"beni":1,"gadi":1}
agent_weights = {"avi":1, "gadi":10, "beni":100}
item_capacities = {"x":2, "y":2}
allocation = utilitarian_matching(agent_values, item_capacities=item_capacities, agent_capacities=agent_capacities, agent_weights=agent_weights)
```

You can see what bundle is given to each agent, and which agent holds each item:

```python
print(allocation.map_agent_to_bundle())
print(allocation.map_item_to_agents())
```
```
{'avi': ['x', 'y'], 'beni': ['y'], 'gadi': ['x']}

{'x': ['avi', 'gadi'], 'y': ['avi', 'beni']}
```

You can see the utility profile, as well as the utility matrix:

```python
print(allocation.utility_profile())
print(allocation.utility_profile_matrix())
```
```
[9. 3. 3.]

[[9. 4. 5.]
 [5. 3. 2.]
 [5. 2. 3.]]
```
Based on these, you can easily compute e.g. the utilitarian value, egalitarian value, number of envy pairs, largest envy, etc.
