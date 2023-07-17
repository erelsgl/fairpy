"""
Allocates the given courses to the given agents using the 'Course allocation by proxy auction' algorithm which
garantees efficient Pareto.
Reference:
    Uthor Scott Duke Kominers, Mike Ruberry and Jonathan Ullman
    Department of Economics, Harvard University, and Harvard Business School 
    (http://scottkom.com/articles/Kominers_Ruberry_Ullman_Course_Allocation_with_Appendix.pdf)
Programmer: Avihu Goren
Since:  2023-01
"""

import pytest

from fairpy.agents import AdditiveAgent
from fairpy.courses.course_allocation_by_proxy_auction import course_allocation_by_proxy_auction

def test_none_fail_input_agents():
    assert pytest.raises(TypeError, course_allocation_by_proxy_auction, None, 5, ["c1", "c2", "c3", "c4"], 2)

        
def test_none_fail_input_capacity():
    Alice = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,}, name="Alice")
    Bob = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3, }, name="Bob")
    Eve = AdditiveAgent({"c2": 1, "c3": 2, "c1": 3, }, name="Eve")
    agents = [Alice,Bob,Eve]
    assert pytest.raises(TypeError, course_allocation_by_proxy_auction, agents, None, ["c1", "c2", "c3"], 1)

def test_big_input_no_exception_100():
    agents = []
    for i in range (0,100):
        agents.append(AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,"c4":4}, name=f"{i}"))
    try:
        allocation = course_allocation_by_proxy_auction(agents,25,["c1","c2","c3","c4"],1)
        for _,v in enumerate(allocation):
            assert len(v) == 1
    except Exception as e:
         assert False, "Big input of 1000 students raise an error"

@pytest.mark.skip("Takes too long for pytest")
def test_big_input_no_exception_1000():
    agents = []
    for i in range (0,1000):
        agents.append(AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,"c4":4}, name=f"{i}"))
    try:
        allocation = course_allocation_by_proxy_auction(agents,250,["c1","c2","c3","c4"],1)
        for _,v in enumerate(allocation):
            assert len(v) == 1
    except Exception as e:
         assert False, "Big input of 1000 students raise an error"

@pytest.mark.skip("Takes too long for pytest")
def test_big_input_no_exception_10000():
    agents = []
    for i in range (0,10000):
        agents.append(AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,"c4":4}, name=f"{i}"))
    try:
        course_allocation_by_proxy_auction(agents,250,["c1","c2","c3","c4"],2)
    except Exception as e:
         assert False, "Big input of 1000 students raise an error"

def test_fail_empty_agents():
    assert pytest.raises(ZeroDivisionError, course_allocation_by_proxy_auction, [], 5, ["c1", "c2", "c3", "c4"], 1)


def test_fail_zero_capacity():
    Alice = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,}, name="Alice")
    Bob = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3, }, name="Bob")
    Eve = AdditiveAgent({"c2": 1, "c3": 2, "c1": 3, }, name="Eve")
    agents = [Alice,Bob,Eve]
    assert pytest.raises(ValueError, course_allocation_by_proxy_auction, agents, 0, ["c1", "c2", "c3"], 1)

  
if __name__ == "__main__":
     pytest.main(["-v",__file__])

