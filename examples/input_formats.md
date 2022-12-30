# Input formats


```python
import fairpy
divide = fairpy.divide
```



`fairpy` allows various input formats, so that you can easily use it on your own data,
whether for applications or for research.
For example, suppose you want to divide candies among your children.
It is convenient to collect their preferences in a dict of dicts:


```python
input = {
    "Ami": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Tami": {"green": 12, "red":8, "blue": 4, "yellow": 2} }
allocation = divide(fairpy.items.round_robin, input)
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
print(divide(fairpy.items.round_robin, {"Ami": [8,7,6,5], "Tami": [12,8,4,2]}))
print(divide(fairpy.items.round_robin, [[8,7,6,5], [12,8,4,2]]))
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
input = np.random.randint(1,100,[2,4])
print(input)
allocation = divide(fairpy.items.round_robin, input)
print(allocation)
```

```
[[10 20  5 11]
 [51 85 93 90]]
Agent #0 gets {1,3} with value 31.
Agent #1 gets {0,2} with value 144.
```


---
Markdown generated automatically from [input_formats.py](input_formats.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-11-19.
