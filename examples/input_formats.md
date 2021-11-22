# Input formats
fairpy allows various input formats, so that you can easily use it on your own data,
whether for applications or for research.
For example, suppose you want to divide candies among your children.
It is convenient to collect their preferences in a dict of dicts:


```python
import fairpy
instance = {
    "Ami": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Tami": {"green": 12, "red":8, "blue": 4, "yellow": 2} }
allocation = fairpy.items.round_robin(instance)
```



You can then see the resulting allocation with the agents' real names:


```python
print(allocation)
```

```
Ami gets {blue,green} with value 14.
Tami gets {red,yellow} with value 10.
```



For research, passing a dict of dicts as a parameter may be too verbose.
You can call the same algorithm with only the values, or only the value matrix:


```python
print(fairpy.items.round_robin({"Ami": [8,7,6,5], "Tami": [12,8,4,2]}))
print(fairpy.items.round_robin([[8,7,6,5], [12,8,4,2]]))
```

```
Ami gets {0,2} with value 14.
Tami gets {1,3} with value 10.

Agent #0 gets {0,2} with value 14.
Agent #1 gets {1,3} with value 10.
```



For experiments, you can use a numpy random matrix:


```python
import numpy as np
instance = np.random.randint(1,100,[2,4])
print(instance)
allocation = fairpy.items.round_robin(instance)
print(allocation)
```

```
[[37 39 81 51]
 [ 1 33 42 57]]
Agent #0 gets {1,2} with value 120.
Agent #1 gets {0,3} with value 58.
```


---
Markdown generated automatically from [input_formats.py](input_formats.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2021-11-22.
