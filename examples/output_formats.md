# Output formats
The output of a fair division allocation is usually an `Allocation` object.


```python
from fairpy.items.utilitarian_matching import utilitarian_matching
agent_values = {"avi": {"x":5, "y": 4}, "beni": {"x":2, "y":3}, "gadi": {"x":3, "y":2}}
agent_capacities = {"avi":2,"beni":1,"gadi":1}
agent_weights = {"avi":1, "gadi":10, "beni":100}
item_capacities = {"x":2, "y":2}
allocation = utilitarian_matching(agent_values, item_capacities=item_capacities, agent_capacities=agent_capacities, agent_weights=agent_weights)
```



You can see what bundle is given to each agent:

```python
print(allocation.map_agent_to_bundle())
```

```
{'avi': ['x', 'y'], 'beni': ['y'], 'gadi': ['x']}
```



and which agent/s hold/s each item:

```python
print(allocation.map_item_to_agents())
```

```
{'x': ['avi', 'gadi'], 'y': ['avi', 'beni']}
```



You can see the utility profile:

```python
print(allocation.utility_profile())
```

```
[9. 3. 3.]
```



and the utility matrix:

```python
print(allocation.utility_profile_matrix())
```

```
[[9. 4. 5.]
 [5. 3. 2.]
 [5. 2. 3.]]
```


---
Markdown generated automatically from [output_formats.py](output_formats.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2021-11-08.
