from agents import *
from fe_cake_division_connected_pieces import ALG ,efCheck
import fe_cake_division_connected_pieces ,logging, sys

fe_cake_division_connected_pieces.logger.addHandler(logging.StreamHandler(sys.stdout))

Alice = PiecewiseConstantAgent1Sgemant([3,6,3], name="Alice")
George = PiecewiseConstantAgent1Sgemant([0,2,4,6], name="George")
Abraham = PiecewiseConstantAgent1Sgemant([6,4,2,0], name="Abraham")
Hanna = PiecewiseConstantAgent1Sgemant([3,3,3,3], name="Hanna")
epsilon  =0.1
all_agents = [Alice, George, Abraham, Hanna]
for a in all_agents:
    print(a)
print()
for epsilon in [0.1,0.2,0.3]:
    print("Allocation for epsilon = " + str(epsilon))
    alloc = ALG(all_agents, epsilon)
    print(alloc)
    print(efCheck(alloc, epsilon) + "\n")

print("-"*90)
Alice = PiecewiseConstantAgent1Sgemant([3,8,10], name="Alice")
George = PiecewiseConstantAgent1Sgemant([10,5,14,6], name="George")
Abraham = PiecewiseConstantAgent1Sgemant([4,14,12,0], name="Abraham")
Hanna = PiecewiseConstantAgent1Sgemant([4,9,13,3], name="Hanna")
all_agents = [Alice, George, Abraham, Hanna]
for a in all_agents:
    print(a)
print()
for epsilon in [0.1,0.2,0.3]:
    print("Allocation for epsilon = " + str(epsilon))
    alloc = ALG(all_agents, epsilon)
    print(alloc)
    print(efCheck(alloc, epsilon) + "\n")

print("-"*90)
Bob = PiecewiseConstantAgent1Sgemant([9,81,10,9], name="Bob")
Yoav = PiecewiseConstantAgent1Sgemant([3,7,5,1], name="Yoav")
Sam = PiecewiseConstantAgent1Sgemant([20,12,15,10], name="Sam")
Alice = PiecewiseConstantAgent1Sgemant([13,8,10], name="Alice")
George = PiecewiseConstantAgent1Sgemant([13,5,14,6], name="George")
Abraham = PiecewiseConstantAgent1Sgemant([14,4,12,6], name="Abraham")
Hanna = PiecewiseConstantAgent1Sgemant([14,9,13,7], name="Hanna")
all_agents = [Alice, George, Abraham, Hanna,Bob,Yoav,Sam]
for a in all_agents:
    print(a)
print()
for epsilon in [0.1,0.2,0.3]:
    print("Allocation for epsilon = " + str(epsilon))
    alloc = ALG(all_agents, epsilon)
    print(alloc)
    print(efCheck(alloc, epsilon) + "\n")