# Input formats

Many algorithms in `fairpy` use loggers. This is useful for understanding how the algorithm works. Logging is based on the standard python `logging` library:

```python
import fairpy, sys, logging
fairpy.items.round_robin.logger.addHandler(logging.StreamHandler(sys.stdout))
fairpy.items.round_robin.logger.setLevel(logging.INFO)

instance = {
    "Ami": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Tami": {"green": 12, "red":8, "blue": 4, "yellow": 2} }
fairpy.items.round_robin(instance)
```

which yields:

```
Round Robin with agent-order [0, 1] and items ['green', 'red', 'blue', 'yellow']
Ami takes green (value 8)
Tami takes red (value 8)
Ami takes blue (value 6)
Tami takes yellow (value 2)
```

You can configure the `round_robin` method with optional arguments such as the order of agents, 
or the subset of items to allocate. This makes it easy to use it as a subroutine 
in more complex algorithms.

```python
fairpy.items.round_robin(instance, agent_order=[1,0], items=["green", "red", "blue"])
```

```
Round Robin with agent-order [1, 0] and items ['green', 'red', 'blue']
Tami takes green (value 12)
Ami takes red (value 7)
Tami takes blue (value 4)
```

You can turn off logging like this:

```python
fairpy.items.round_robin.logger.setLevel(logging.WARNING)
```

You can turn logging on/off for each module separately.
