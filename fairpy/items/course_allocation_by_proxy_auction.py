



from ast import List
from collections import defaultdict
from fairpy.agents import AdditiveAgent
from fairpy.allocations import Allocation
import pytest

def create_bid_sets(num_players, bid_set_size):
    """
    This function create the bid set for each Agent with this bids he can buy courses
    >>> create_bid_sets(3,2)
    [[6, 1], [5, 3], [4, 2]]
    """
    # Define the global bid set B as a list of integers from 1 to num_players*bid_set_size
    B = [i for i in range(1, num_players*bid_set_size+1)]
  
    # Initialize a list to hold the bid sets
    bid_sets = [[] for _ in range(num_players)]
  
    # Sort the bids in decreasing order
    B = sorted(B, reverse=True)
  
    turn_list = create_turns(num_players=num_players,num_picks=num_players*bid_set_size)
    for i in range(len(turn_list)):
        bid_sets[turn_list[i]].append(B[i])
  
    # Return the list of bid sets
    return bid_sets

def create_turns(num_players, num_picks):
    """
    This function create a an array that represt turn of each player by index to create a fair bids.
    >>> create_turns(3,6)
    [0, 1, 2, 1, 2, 0]
    """
    turns = []
  
    for i in range(num_picks):
        # Add the player to the turns list, rotating the order of the picks between rounds
        turns.append((i + (i // num_players)) % num_players)
        # The expression (i + (i // num_players)) % num_players rotates the order of the picks between rounds
    return turns

def has_common_object(list1, list2):
    """
    This function is checking if 2 lists have at list 1 common element.
    >>> has_common_object([0,1],[5,6])
    False
    >>> has_common_object([0,5],[5,6])
    True
    """
    commons_objects = [element for element in list1 if element in list2]
    return True if commons_objects else False
def calculate_b_star(Bi,B_tag_i,p_Ac):
    """
    This function used to calculate b* from the articale b* is bid that is inside Bi and not inside B_tag and also is bigger than
    p_Ac.
    >>> calculate_b_star([1,6],[1],3)
    6
    """
    Bi_without_B_tag_i_ = [bid for bid in Bi if bid not in B_tag_i and bid > p_Ac]
    return min(Bi_without_B_tag_i_) if Bi_without_B_tag_i_ else None
def calculate_b_double_star(Bi,B_tag_i,b_star):
    """
    This function used to calculate b** from the articale b** is bid that is inside Bi and not inside B_tag and also is bigger or equal to
    b_star.
    >>> calculate_b_double_star([2,5],[2],3)
    5
    """
    Bi_without_B_tag_i_ = [bid for bid in Bi if bid not in B_tag_i and bid >= b_star]
    return min(Bi_without_B_tag_i_) if Bi_without_B_tag_i_ else None
           
def course_allocation(agents: list[AdditiveAgent],course_capacity:int,course_list:str,course_amount_per_agent:int) -> Allocation:
    """
    Allocates the given courses to the given agents using the 'Course allocation by proxy auction' algorithm which
    garantees efficient Pareto by Uthor Scott Duke Kominers, Mike Ruberry and Jonathan Ullman
    Department of Economics, Harvard University, and Harvard Business School 
    (http://scottkom.com/articles/Kominers_Ruberry_Ullman_Course_Allocation_with_Appendix.pdf)
    :param agents: The agents who participate in the allocation and there course preferences.
    :param course_capacity: The courses capacity.
    :param course_list: The names of the courses.
    :param course_amount_per_agent how many courses each agent can take.
    :return: An allocation for each of the agents.
    >>> Alice = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,}, name="Alice")
    >>> Bob = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3, }, name="Bob")
    >>> Eve = AdditiveAgent({"c2": 1, "c3": 2, "c1": 3, }, name="Eve")
    >>> agents = [Alice,Bob,Eve]
    >>> allocation = course_allocation(agents,2,["c1","c2","c3"],2)
    >>> {agents[i].name():allocation[i] for i,_ in enumerate(agents)}
    {'Alice': {c1,c3}, 'Bob': {c1,c2}, 'Eve': {c2,c3}}


    Two exampels that represent a problem in the algo where its better for Bob to give false preferences and get a better result
    >>> Alice = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,"c4":4}, name="Alice")
    >>> Bob = AdditiveAgent({"c2": 1, "c3": 2, "c4": 3,"c1":4 }, name="Bob")
    >>> agents = [Alice,Bob]
    >>> allocation = course_allocation(agents,1,["c1","c2","c3","c4"],2)
    >>> {agents[i].name():allocation[i] for i,_ in enumerate(agents)}
    {'Alice': {c1,c2}, 'Bob': {c3,c4}}


    >>> Alice = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,"c4":4}, name="Alice")
    >>> Bob = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,"c4":4 }, name="Bob")
    >>> agents = [Alice,Bob]
    >>> allocation = course_allocation(agents,1,["c1","c2","c3","c4"],2)
    >>> {agents[i].name():allocation[i] for i,_ in enumerate(agents)}
    {'Alice': {c1,c4}, 'Bob': {c2,c3}}
    """
    list_of_course_preference = [[] for _ in agents]
    for i,agent in enumerate(agents):
        list_of_course_preference [i] = sorted([course for course in course_list],key= lambda x: agent.value({x})) 
    bids_coins =create_bid_sets(len(agents),course_amount_per_agent)
    Ac = {}
    for course in course_list:
        Ac[course] = [] 
    active = True
    while active:
        active = False
        for i in range(len(agents)):
            B_TAG = []
            for course in list_of_course_preference[i]:
                if has_common_object(bids_coins[i],Ac[course]) is False:
                    p_Ac  = 0 if len(Ac[course])< course_capacity else min(Ac[course])
                    b_star = calculate_b_star(bids_coins[i],B_TAG,p_Ac)
                    if b_star:
                        B_TAG.append(b_star)
                        Ac[course].append(min([bid for bid in bids_coins[i] if bid > p_Ac ]))
                        if len(Ac[course]) > course_capacity: Ac[course].remove(min(Ac[course]))
                        active = True
                else:
                    b_star = [bid for bid in bids_coins[i] if bid in Ac[course]][0]
                    b_double_star = calculate_b_double_star(bids_coins[i],B_TAG,b_star)
                    B_TAG.append(b_double_star) if b_double_star else Ac[course].remove(b_star)
    bundle = defaultdict(list)
    for i,agent in enumerate(agents):
        for course in course_list:
            if [bid for bid in bids_coins[i] if bid in Ac[course]]: bundle[agent.name()].append(course)
    return Allocation(agents=[agent.name() for agent in agents], bundles=bundle)
if __name__ == "__main__":
    import doctest
    doctest.testmod()

   


