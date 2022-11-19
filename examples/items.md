# Fair item allocation algorithms


```python
import fairpy
divide = fairpy.divide
```



`fairpy` contains various algorithms for fair allocation of items,
both divisible and indivisible.
Before starting the algorithms, let us create some inputs for them.


```python
input_3_agents = {"Alice":  {"z":12, "y":10, "x":8, "w":7, "v":4, "u":1},
          "Dina":   {"z":14, "y":9, "x":15, "w":4, "v":9, "u":12},
          "George": {"z":19, "y":16, "x":8, "w":6, "v":5, "u":1},
           }

input_2_agents = {
    "Alice":  {"a": 2, "b": 6, "c": 3, "d":3,"e":1,"f":7,"g":15,"h":21,"i":4,"j":22,"k":7,"l":10,"m":11,"n":22,"o":6,"p":7,"q":16,"r":12,"s":3,"t":28,"u":39,"v":4,"w":9,"x":1,"y":17,"z":99},
    "George": {"a": 2, "b": 4, "c": 3, "d":1,"e":0,"f":7,"g":16,"h":21,"i":4,"j":23,"k":7,"l":10,"m":11,"n":22,"o":6,"p":9,"q":16,"r":10,"s":3,"t":24,"u":39,"v":2,"w":9,"x":5,"y":17,"z":100},
}
```



## DISCRETE ALLOCATION:
Round robin:

```python
print(divide(fairpy.items.round_robin, input_3_agents))
```

```
Alice gets {w,z} with value 19.
Dina gets {u,x} with value 27.
George gets {v,y} with value 21.
```



Utilitarian matching:

```python
print(divide(fairpy.items.utilitarian_matching, input_3_agents))
```

```
Alice gets {y} with value 10.
Dina gets {x} with value 15.
George gets {z} with value 19.
```



Iterated maximum matching:

```python
print(divide(fairpy.items.iterated_maximum_matching, input_3_agents))
```

```
Alice gets {w,y} with value 17.
Dina gets {u,x} with value 27.
George gets {v,z} with value 24.
```



PROPm allocation:

```python
print(divide(fairpy.items.propm_allocation, input_3_agents))
```

```
Alice gets {x,y} with value 18.
Dina gets {u,v,w} with value 25.
George gets {z} with value 19.
```



Garg-Taki algorithm for 3/4 MMS allocation:

```python
print(divide(fairpy.items.three_quarters_MMS_allocation, input_3_agents))
```

```
Alice gets {z} with value 12.
Dina gets {u,v,x} with value 36.
George gets {w,y} with value 22.
```



Oh-Procaccia-Suksompong algorithm for 2 agents EF1 allocation:

```python
print(divide(fairpy.items.two_agents_ef1, input_2_agents))
```

```
Alice gets {a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s} with value 178.
George gets {t,u,v,w,x,y,z} with value 196.
```



## FRACTIONAL ALLOCATION:
Utilitarian fractional allocation:

```python
print(divide(fairpy.items.max_sum_allocation, input_3_agents).round(3))
```

```
Alice gets { 100.0% of w} with value 7.
Dina gets { 100.0% of x, 100.0% of v, 100.0% of u} with value 36.
George gets { 100.0% of z, 100.0% of y} with value 35.
```



Max product (aka Nash optimal) fractional allocation:

```python
print(divide(fairpy.items.max_product_allocation, input_3_agents).round(3))
```

```
Alice gets { 50.0% of z, 38.7% of x, 100.0% of w} with value 16.1.
Dina gets { 61.3% of x, 100.0% of v, 100.0% of u} with value 30.2.
George gets { 50.0% of z, 100.0% of y} with value 25.5.
```



Leximin (aka egalitarian) fractional allocation:

```python
print(divide(fairpy.items.leximin_optimal_allocation, input_3_agents).round(3))
```

```
Alice gets { 66.8% of z, 91.2% of x, 100.0% of w} with value 22.3.
Dina gets { 8.8% of x, 100.0% of v, 100.0% of u} with value 22.3.
George gets { 33.2% of z, 100.0% of y} with value 22.3.
```



Efficient envy-free allocation with bounded sharing:

```python
print(divide(fairpy.items.efficient_envyfree_allocation_with_bounded_sharing, input_3_agents).round(3))
```

```
Alice gets { 50.0% of z, 38.7% of x, 100.0% of w} with value 16.1.
Dina gets { 61.3% of x, 100.0% of v, 100.0% of u} with value 30.2.
George gets { 50.0% of z, 100.0% of y} with value 25.5.
```



Efficient Envy-free allocation with minimum-sharing:

```python
print(divide(fairpy.items.envyfree_allocation_with_min_sharing, input_3_agents).round(3))
```

```
Alice gets { 100.0% of y, 100.0% of w} with value 17.
Dina gets { 100.0% of x, 100.0% of u} with value 27.
George gets { 100.0% of z, 100.0% of v} with value 24.
```


For more information see:

* [List of item allocation algorithms currently implemented](../fairpy/items/README.md).
* [List of item allocation algorithms for future work](../fairpy/items/README-future.md).

---
Markdown generated automatically from [items.py](items.py) using [Pweave](http://mpastell.com/pweave) 0.30.3 on 2022-11-19.
