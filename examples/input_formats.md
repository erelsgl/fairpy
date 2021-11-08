# Input formats

`fairpy` allows various input formats, so that you can easily use it on your own data,
whether for applications or for research.
For example, suppose you want to divide candies among your children.
It is convenient to collect their preferences in a dict of dicts:

```python
import fairpy
instance = {
    "Ami": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Tami": {"green": 12, "red":8, "blue": 4, "yellow": 2} }
allocation = fairpy.items.round_robin(instance)
print(allocation)
```

which yields:

```
Ami gets {blue,green} with value 14.
Tami gets {red,yellow} with value 10.
```

Passing a dict of dicts as a parameter may be too verbose.
You can call the same algorithm with only names and values, or only values:

```python
fairpy.items.round_robin({"Ami": [8,7,6,5], "Tami": [12,8,4,2]})
fairpy.items.round_robin([[8,7,6,5], [12,8,4,2]])
```

You can also use a numpy matrix:

```python
import numpy as np
fairpy.items.round_robin(np.random.randint(1,100,[2,4]))
```

Printing the result of the last statement may give, for example:

```
Agent #0 gets {2,3} with value 137.
Agent #1 gets {0,1} with value 135.
```

