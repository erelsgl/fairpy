# Fair cake-cutting algorithms
Cake-cutting algorithms require `Agent` objects that can answer `mark` and `eval` queries.
Some such Agent objects are already defined.


```python
from fairpy.agents import PiecewiseUniformAgent, PiecewiseConstantAgent, agents_from

# 'Alice has two desired intervals, 0..1 and 3..6. Each interval has value 1:
Alice = PiecewiseUniformAgent ([(0,1),(3,6)], name="Alice")   
# 'George has four desired intervals: 0..1 with value 1, 1..2 with value 3, etc:
George = PiecewiseConstantAgent([1,3,5,7],    name="George")  
print(Alice)
print(George)
```

```
Alice is an agent with a Piecewise-uniform agent with desired regions
[(0, 1), (3, 6)] and total value=4
George is an agent with a Piecewise-constant valuation with values [1
3 5 7] and total value=16
```



Now, we can let our agents play 'cut and choose'.


```python
from fairpy.cake import cut_and_choose

allocation = cut_and_choose.asymmetric_protocol([Alice, George])
print(allocation)
```

```
Alice gets {(4.0, 6)} with value 2.
George gets {(0, 4.0)} with value 16.
```



To better understand what is going on, we can use logging:


```python
import logging, sys
cut_and_choose.logger.addHandler(logging.StreamHandler(sys.stdout))
cut_and_choose.logger.setLevel(logging.INFO)

print(cut_and_choose.asymmetric_protocol([Alice, George]))
print(cut_and_choose.asymmetric_protocol([George, Alice]))
```

```
The cutter (Alice) cuts at 4.00.
The chooser (George) chooses the leftmost piece.
Alice gets {(4.0, 6)} with value 2.
George gets {(0, 4.0)} with value 16.

The cutter (George) cuts at 2.80.
The chooser (Alice) chooses the rightmost piece.
George gets {(0, 2.8)} with value 8.
Alice gets {(2.8, 6)} with value 3.
```



Here is another protocol - symmetric cut-and-choose:

```python
print(cut_and_choose.symmetric_protocol([Alice, George]))
```

```
The agents mark at 4.000000, 2.800000
The cake is cut at 3.400000.
George's mark is to the left of Alice's mark.
Alice gets {(3.4, 6)} with value 2.6.
George gets {(0, 3.4)} with value 11.8.
```



Here is an algorithm for more than two agents:


```python
from fairpy.cake import last_diminisher

last_diminisher.logger.addHandler(logging.StreamHandler(sys.stdout))
last_diminisher.logger.setLevel(logging.INFO)

from fairpy.cake.valuations import PiecewiseConstantValuation
print(last_diminisher.last_diminisher(agents_from([
    PiecewiseConstantValuation([1,3,5,7]), 
    PiecewiseConstantValuation([7,5,3,1]),
    PiecewiseConstantValuation([4,4,4,4]),
    PiecewiseConstantValuation([16,0,0,0]),
    ])))
```

```

4 agents remain, and recursively allocate the cake starting at
0.000000 among them.
Agent #0 marks at 2.000000
Agent #1 diminishes the current mark to 0.571429.
Agent #2 does not diminish the current mark.
Agent #3 diminishes the current mark to 0.250000.
Agent #3 is the last diminisher, and gets the piece
[0.000000,0.250000].

3 agents remain, and recursively allocate the cake starting at
0.250000 among them.
Agent #0 marks at 2.050000
Agent #1 diminishes the current mark to 0.821429.
Agent #2 does not diminish the current mark.
Agent #1 is the last diminisher, and gets the piece
[0.250000,0.821429].

2 agents remain, and recursively allocate the cake starting at
0.821429 among them.
Agent #0 marks at 2.164286
Agent #2 diminishes the current mark to 1.821429.
Agent #2 is the last diminisher, and gets the piece
[0.821429,1.821429].

One agent remains (Agent #0), and receives the entire remaining cake
starting at 1.8214285714285714.
Agent #0 gets {(1.8214285714285714, 4)} with value 12.5.
Agent #1 gets {(0.25, 0.8214285714285714)} with value 4.
Agent #2 gets {(0.8214285714285714, 1.8214285714285714)} with value 4.
Agent #3 gets {(0, 0.25)} with value 4.
```



To turn off logging:


```python
cut_and_choose.logger.logger.setLevel(logging.WARNING)
```

```
---------------------------------------------------------------------------AttributeError
Traceback (most recent call
last)~\AppData\Local\Temp/ipykernel_9436/1620946758.py in <module>
----> 1 cut_and_choose.logger.logger.setLevel(logging.WARNING)
AttributeError: 'Logger' object has no attribute 'logger'
```


---
Markdown generated automatically from [cake.py](cake.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2021-11-08.
