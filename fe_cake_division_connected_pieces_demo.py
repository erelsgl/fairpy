from agents import *
from fe_cake_division_connected_pieces import ALG ,efCheck
import fe_cake_division_connected_pieces ,logging, sys

fe_cake_division_connected_pieces.logger.addHandler(logging.StreamHandler(sys.stdout))
#fe_cake_division_connected_pieces.setLevel(logging.INFO)

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

