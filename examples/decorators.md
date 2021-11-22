# Decorators
fairpy allows algorithm developers to write them in a native format, that accepts a valuation matrix and returns an allocation matrix.
They can then easily adapt them to accept and return more user-friendly inputs, using decorators.


```python
from fairpy import convert_input_to_valuation_matrix, ValuationMatrix
import numpy as np
```



The algorithm below accepts a input a valuation matrix,  and return as output an allocation matrix.
The decorator allows it to accept other input formats.
It allocate the objects in turn, like "round robin" but without regard to valuations.


```python
@convert_input_to_valuation_matrix
def dummy_matrix_matrix_algorithm(instance, first_agent:int=0)->np.ndarray:
    valuation_matrix = instance
    num_agents = valuation_matrix.num_of_agents
    num_objects = valuation_matrix.num_of_objects
    bundles = np.zeros([num_agents,num_objects])
    i_agent = first_agent
    for i_object in range(num_objects):
        bundles[i_agent][i_object] = 1
        i_agent += 1
        if i_agent >= num_agents:
            i_agent = 0
    return bundles
```



Native calls (works even without the decorator):

```python
print(dummy_matrix_matrix_algorithm(ValuationMatrix([[11,22,33],[44,55,66]])).matrix)
print(dummy_matrix_matrix_algorithm(ValuationMatrix([[11,22,33],[44,55,66]]), first_agent=1).matrix)
```

```
[[1. 0. 1.]
 [0. 1. 0.]]
[[0. 1. 0.]
 [1. 0. 1.]]
```



Calls with a list of lists:

```python
print(dummy_matrix_matrix_algorithm([[11,22,33],[44,55,66]]))
print(dummy_matrix_matrix_algorithm([[11,22,33],[44,55,66]], first_agent=1))
```

```
Agent #0 gets { 100.0% of 0, 100.0% of 2} with value 44.
Agent #1 gets { 100.0% of 1} with value 55.

Agent #0 gets { 100.0% of 1} with value 22.
Agent #1 gets { 100.0% of 0, 100.0% of 2} with value 110.
```



Call with a dict mapping agent names to lists of values:

```python
input_dict_of_dicts = {"a": [11,22,33], "b": [44,55,66]}       
print(dummy_matrix_matrix_algorithm(input_dict_of_dicts))
print(dummy_matrix_matrix_algorithm(input_dict_of_dicts, first_agent=1))
```

```
a gets { 100.0% of 0, 100.0% of 2} with value 44.
b gets { 100.0% of 1} with value 55.

a gets { 100.0% of 1} with value 22.
b gets { 100.0% of 0, 100.0% of 2} with value 110.
```



Call with a dict mapping agent names to dict of values:

```python
input_dict_of_dicts = {"a": {"x":11,"y":22,"z":33}, "b": {"x":44,"y":55,"z":66}}       
print(dummy_matrix_matrix_algorithm(input_dict_of_dicts, first_agent=0))
print(dummy_matrix_matrix_algorithm(input_dict_of_dicts, first_agent=1))
```

```
a gets { 100.0% of x, 100.0% of z} with value 44.
b gets { 100.0% of y} with value 55.

a gets { 100.0% of y} with value 22.
b gets { 100.0% of x, 100.0% of z} with value 110.
```


---
Markdown generated automatically from [adaptors.py](adaptors.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2021-11-22.
