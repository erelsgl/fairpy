# Fair item allocation algorithms
Below are some algorithms for fair allocation of items,
both divisible and indivisible.


```python
import fairpy

instance = {"Alice":  {"z":12, "y":10, "x":8, "w":7, "v":4, "u":1},
          "Dina":   {"z":14, "y":9, "x":15, "w":4, "v":9, "u":12},
          "George": {"z":19, "y":16, "x":8, "w":6, "v":5, "u":1},
           }
```



Round robin:

```python
print(fairpy.items.round_robin(instance))
```

```
Alice gets {w,z} with value 19.
Dina gets {u,x} with value 27.
George gets {v,y} with value 21.
```



Utilitarian matching:

```python
print(fairpy.items.utilitarian_matching(instance))
```

```
Alice gets {y} with value 10.
Dina gets {x} with value 15.
George gets {z} with value 19.
```



Iterated maximum matching:

```python
print(fairpy.items.iterated_maximum_matching(instance))
```

```
Alice gets {w,y} with value 17.
Dina gets {u,x} with value 27.
George gets {v,z} with value 24.
```



PROPm allocation:

```python
print(fairpy.items.propm_allocation(instance))
```

```
Alice gets {x,y} with value 18.
Dina gets {u,v,w} with value 25.
George gets {z} with value 19.
```



Utilitarian fractional allocation:

```python
print(fairpy.items.max_sum_allocation(instance).round(3))
```

```
Alice gets { 100.0% of w} with value 7.
Dina gets { 100.0% of x, 100.0% of v, 100.0% of u} with value 36.
George gets { 100.0% of z, 100.0% of y} with value 35.
```



Max product (aka Nash optimal) fractional allocation:

```python
print(fairpy.items.max_product_allocation(instance).round(3))
```

```
Alice gets { 50.0% of z, 38.8% of x, 100.0% of w} with value 16.1.
Dina gets { 61.2% of x, 100.0% of v, 100.0% of u} with value 30.2.
George gets { 50.0% of z, 100.0% of y} with value 25.5.
```



Leximin (aka egalitarian) fractional allocation:

```python
print(fairpy.items.leximin_optimal_allocation(instance).round(3))
```

```
Alice gets { 66.8% of z, 91.2% of x, 100.0% of w} with value 22.3.
Dina gets { 8.8% of x, 100.0% of v, 100.0% of u} with value 22.3.
George gets { 33.2% of z, 100.0% of y} with value 22.3.
```



Efficient envy-free allocation with bounded sharing:

```python
print(fairpy.items.efficient_envyfree_allocation_with_bounded_sharing(instance).round(3))
```

```
Alice gets { 50.0% of z, 38.8% of x, 100.0% of w} with value 16.1.
Dina gets { 61.2% of x, 100.0% of v, 100.0% of u} with value 30.2.
George gets { 50.0% of z, 100.0% of y} with value 25.5.
```



Efficient Envy-free allocation with minimum-sharing:

```python
print(fairpy.items.envyfree_allocation_with_min_sharing(instance).round(3))
```

```
Alice gets { 100.0% of y, 100.0% of w} with value 17.
Dina gets { 100.0% of x, 100.0% of u} with value 27.
George gets { 100.0% of z, 100.0% of v} with value 24.
```


---
Markdown generated automatically from [items.py](items.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2021-11-08.
