"""

Programmer: Ofec Israel

"""




import agents
from agents import PiecewiseLinearAgent
from agents import PiecewiseUniformAgent
from allocations import *
from truth_justice_cake_cutting import *

def test():
    print("test")
    
    
    a = PiecewiseUniformAgent([(0,0.39)], "a")
    b = PiecewiseUniformAgent([(0,0.6)], "b")
    c = PiecewiseUniformAgent([(0,0.1)], "c")

    cake = [(0,1)]
    agents = [a,b,c]
    
    allocations = algorithm1(agents, cake)
    
    print(allocations)

    
    a = PiecewiseLinearAgent([(0,0.2, 1,1)], "a")
    b = PiecewiseLinearAgent([(0.2,0.3, 1,1)], "b")
    agents = [a,b,c]
    
    allocations = algorithm2(agents)
    
    print(allocations)
    

if __name__ == "__main__":
    test()
    print("main")