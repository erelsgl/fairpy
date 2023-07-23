
"""
Allocates the given courses to the given agents using a proxy auction, which guarantees Pareto efficiency.

Reference:
    Scott Duke Kominers, Mike Ruberry and Jonathan Ullman:
    'Course allocation by proxy auction',
    [WINE 2010](https://link.springer.com/chapter/10.1007/978-3-642-17572-5_49),
    [Full version](http://scottkom.com/articles/Kominers_Ruberry_Ullman_Course_Allocation_with_Appendix.pdf)

Programmer: Avihu Goren
Since:  2023-01
"""


from collections import defaultdict
from fairpy.courses.instance  import Instance
import logging

logger = logging.getLogger(__name__)

def course_allocation_by_proxy_auction(instance:Instance):
    """
    :param agents: The agents who participate in the allocation and there course preferences.
    :param course_capacity: The courses capacity.
    :param course_list: The names of the courses.
    :param course_amount_per_agent how many courses each agent can take.
    :return: An allocation for each of the agents.
    >>> valuations = {"Alice": {"c1": 1, "c2": 2, "c3": 3,} ,"Bob": {"c1": 1, "c2": 2, "c3": 3, }, "Eve": {"c2": 1, "c3": 2, "c1": 3, }}
    >>> instance = Instance(valuations=valuations, item_capacities=2, agent_capacities=2)
    >>> course_allocation_by_proxy_auction(instance)
    {'Alice': ['c1', 'c3'], 'Bob': ['c1', 'c2'], 'Eve': ['c2', 'c3']}

    Two exampels that represent a problem in the algo where its better for Bob to give false preferences and get a better result
    >>> valuations = {"Alice": {"c1": 1, "c2": 2, "c3": 3, "c4": 4} ,"Bob": {"c2": 1, "c3": 2, "c4": 3, "c1": 4}}
    >>> instance = Instance(valuations=valuations, item_capacities=1, agent_capacities=2)
    >>> course_allocation_by_proxy_auction(instance)
    {'Alice': ['c1', 'c2'], 'Bob': ['c3', 'c4']}

    >>> valuations = {"Alice": {"c1": 1, "c2": 2, "c3": 3, "c4": 4} ,"Bob": {"c1": 1, "c2": 2, "c3": 3, "c4": 4}}
    >>> instance = Instance(valuations=valuations, item_capacities=1, agent_capacities=2)
    >>> course_allocation_by_proxy_auction(instance)
    {'Alice': ['c1', 'c4'], 'Bob': ['c2', 'c3']}
    """
    # instance: Instance 
    list_of_course_preference = [[] for _ in instance.agents]

    for i,agent in enumerate(instance.agents):
        list_of_course_preference[i] = sorted(instance.items, key= lambda x: instance.agent_item_value(agent,x))
    bids_coins = create_bid_sets(instance.agents, instance.agent_capacity)
    logger.info(f"Created the bids for each player: {bids_coins}")

    Ac = {}
    for course in instance.items:
        Ac[course] = [] 
    active = True

    while active:
        active = False
        for i,agent in enumerate(instance.agents):
            B_TAG = []
            logger.info(f"{agent} starts its turn")

            for course in list_of_course_preference[i]:
                if has_common_object(bids_coins[i],Ac[course]) is False:
                    p_Ac  = 0 if len(Ac[course])< instance.item_capacity(course) else min(Ac[course])
                    b_star = calculate_b_star(bids_coins[i],B_TAG,p_Ac)
                    if b_star:
                        B_TAG.append(b_star)
                        min_bid_to_add = min([bid for bid in bids_coins[i] if bid > p_Ac ])
                        Ac[course].append(min_bid_to_add)
                        logger.info(f"Agent {instance} added bid coin {min_bid_to_add} for course {course}")
                        if len(Ac[course]) > instance.item_capacity(course): 
                            Ac[course].remove(min(Ac[course]))
                            logger.info(f"Bid coin {p_Ac} removed from {course} bids group current bids are:{Ac[course]}")
                        active = True

                else:
                    b_star = [bid for bid in bids_coins[i] if bid in Ac[course]][0]
                    b_double_star = calculate_b_double_star(bids_coins[i],B_TAG,b_star)

                    if b_double_star:
                        B_TAG.append(b_double_star)

                    else:
                        Ac[course].remove(b_star)
                        logger.info(f"Bid coin {b_star} removed from {course} current bids are:{Ac[course]}")

            logger.info(f"{agent} end its turn")

    bundles = defaultdict(list)
    for i,agent in enumerate(instance.agents):
        for course in instance.items:
            if [bid for bid in bids_coins[i] if bid in Ac[course]]: 
                bundles[agent].append(course)
    logger.info(f"Algorithm ends successfully")
    return dict(bundles)




########### Auxiliary functions


def create_bid_sets(agents, agent_capacity):
    """
    This function create the bid set for each Agent with this bids he can buy courses
    >>> create_bid_sets(range(3), lambda _:2)
    [[6, 1], [5, 2], [4, 3]]
    """
    # Define the global bid set B as a list of integers from 1 to num_players*bid_set_size
    num_of_bids = sum([agent_capacity(agent) for agent in agents])
    B = list(reversed(range(1, num_of_bids+1)))

    # Initialize a list to hold the bid sets
    bid_sets = [[] for _ in range(len(agents))]
    turn_list = create_turns(num_players=len(agents), num_picks=num_of_bids)
    for i in range(len(turn_list)):
        bid_sets[turn_list[i]].append(B[i])
  
    # Return the list of bid sets
    return bid_sets

def create_turns(num_players, num_picks):
    """
    This function create a an array that represents the turn of each player by index to create a fair bids.
    >>> create_turns(3,9)
    [0, 1, 2, 2, 1, 0, 0, 1, 2]
    """
    turns = []
  
    for i in range(int(num_picks / num_players)):
        if i % 2 == 0:
            turns.extend(range(0,num_players))
        else:
            turns.extend(reversed(range(0,num_players)))
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
           


if __name__ == "__main__":
    # logging.basicConfig(level = logging.INFO)
    import doctest
    print(doctest.testmod())
