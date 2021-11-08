# Loggers
Many algorithms in fairpy use logging. This is useful for understanding how the algorithm works.
Logging is based on the standard python `logging` library:


```python
import fairpy, sys, logging

instance = {
    "Ami": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Tami": {"green": 12, "red":8, "blue": 4, "yellow": 2} }

fairpy.items.round_robin.logger.addHandler(logging.StreamHandler(sys.stdout))
fairpy.items.round_robin.logger.setLevel(logging.INFO)
fairpy.items.round_robin(instance)
```

```

Round Robin with agent-order [0, 1] and items ['green', 'red', 'blue',
'yellow']
Ami takes green (value 8)
Tami takes red (value 8)
Ami takes blue (value 6)
Tami takes yellow (value 2)
```

```
Ami gets {blue,green} with value 14.
Tami gets {red,yellow} with value 10.
```



Another run with different parameters:


```python
fairpy.items.round_robin(instance, agent_order=[1,0], items=["green", "red", "blue"])
```

```

Round Robin with agent-order [1, 0] and items ['green', 'red', 'blue']
Tami takes green (value 12)
Ami takes red (value 7)
Tami takes blue (value 4)
```

```
Ami gets {red} with value 7.
Tami gets {blue,green} with value 16.
```



You can turn off logging for each module separately:


```python
fairpy.items.round_robin.logger.setLevel(logging.WARNING)
fairpy.items.round_robin(instance)
```

```
Ami gets {blue,green} with value 14.
Tami gets {red,yellow} with value 10.
```


---
Markdown generated automatically from [loggers.py](loggers.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2021-11-08.
