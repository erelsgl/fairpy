import time
import numpy as np
import pyximport
from improve_performance.cython_algorithm2 import envy_free_approximation_cython
from fairpy import ValuationMatrix, AllocationMatrix, Allocation
from fairpy.items.envy_free_approximation_division import envy_free_approximation_division

pyximport.install()

cy = []
py = []

for i in range(1, 21):
    shape = (i * 10, i * 10)
    v = np.random.randint(-i * 10, i * 10, size=shape)
    a = np.eye(i * 10, k=0, dtype=int)
    v2 = np.copy(v)
    alloc = Allocation(agents=ValuationMatrix(v), bundles=AllocationMatrix(a))
    alloc2 = Allocation(agents=ValuationMatrix(v2), bundles=AllocationMatrix(a))
    st = time.time()
    envy_free_approximation_cython(alloc, 0.1)
    cy.append(time.time() - st)
    st = time.time()
    envy_free_approximation_division(alloc2, 0.1)
    py.append(time.time() - st)

print("improve_performance", cy)
print("python", py)
diff = [y / x for x, y in zip(cy, py)]
print("diff:", diff)
