# Output formats

The output of a fair division algorithm in `fairpy` is usually an `Allocation` object

```python
import fairpy
instance = {
    "Ami": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Tami": {"green": 12, "red":8, "blue": 4, "yellow": 2} }
allocation = fairpy.items.round_robin(instance)
```

You can see what bundle is given to each agent:

```python
print(allocation.map_agent_to_bundle())
```
```
{'Ami': ['blue', 'green'], 'Tami': ['red', 'yellow']}
```

You can also see which agent holds each item:

```python
print(allocation.map_item_to_agents())
```
```
{'blue': ['Ami'], 'green': ['Ami'], 'red': ['Tami'], 'yellow': ['Tami']}
```

and the utility profile:

```python
print(allocation.utility_profile())
```
```
[14. 10.]
```

