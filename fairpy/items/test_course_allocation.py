import pytest

from fairpy.agents import AdditiveAgent
from fairpy.items.course_allocation_by_proxy_auction import course_allocation
@pytest.mark.xfail()
def test_none_fail_input_agents():
    course_allocation(None,5)
        
@pytest.mark.xfail()
def test_none_fail_input_capacity():
    Alice = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,}, name="Alice")
    Bob = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3, }, name="Bob")
    Eve = AdditiveAgent({"c2": 1, "c3": 2, "c1": 3, }, name="Eve")
    agents = [Alice,Bob,Eve]
    course_allocation(agents,None)

def test_big_input_no_exception_and_time_limit_1000():
    agents = []
    for i in range (0,1000):
        agents.append(AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,"c4":4}, name=f"{i}"))
    try:
        course_allocation(agents,250)
    except Exception as e:
         assert False, "Big input of 1000 students raise an error"

def test_big_input_no_exception_and_time_limit_10000():
    agents = []
    for i in range (0,10000):
        agents.append(AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,"c4":4}, name=f"{i}"))
    try:
        course_allocation(agents,250)
    except Exception as e:
         assert False, "Big input of 1000 students raise an error"

@pytest.mark.xfail()
def test_fail_empty_agents():
    course_allocation([],5)

@pytest.mark.xfail()
def test_fail_zero_capacity():
    Alice = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,}, name="Alice")
    Bob = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3, }, name="Bob")
    Eve = AdditiveAgent({"c2": 1, "c3": 2, "c1": 3, }, name="Eve")
    agents = [Alice,Bob,Eve]
    course_allocation(agents,0)

  
