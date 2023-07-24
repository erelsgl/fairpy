"""
Interface to the SP algorithm from the following paper:

> ["Optimization-based Mechanisms for the Course Allocation Problem"](https://pubsonline.informs.org/doi/epdf/10.1287/ijoc.2018.0849)
>
> by: Hoda Atef Yekta and Robert Day
>
> INFORMS Journal of Computing, 2020

Programmers: Joseph Schtein, Itay Simchayev, Lihi Belfer
"""


from fairpy.courses.instance    import Instance
from fairpy.courses.yekta_day_impl.main import algorithm, logger
from fairpy.courses.yekta_day_impl.course import OOPCourse
from fairpy.courses.yekta_day_impl.student import OOPStudent
from fairpy.courses.iterated_maximum_matching import iterated_maximum_matching
from fairpy.courses.allocation_utils import AllocationBuilder
import logging


def yekta_day(alloc: AllocationBuilder):
    """
    :param alloc: an allocation builder, which tracks the allocation and the remaining capacity for items and agents. of the fair course allocation problem. 

    >>> from dicttools import stringify
    >>> from fairpy.courses.adaptors import divide

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=1, item_capacities=1)
    >>> map_agent_name_to_bundle = divide(yekta_day, instance=instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x'], beni:['w']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=2, item_capacities=1)
    >>> map_agent_name_to_bundle = divide(yekta_day, instance=instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x', 'y'], beni:['w', 'z']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=3, item_capacities=2)
    >>> map_agent_name_to_bundle = divide(yekta_day, instance=instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x', 'y', 'z'], beni:['w', 'y', 'z']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=4, item_capacities=2)
    >>> map_agent_name_to_bundle = divide(yekta_day, instance=instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['w', 'x', 'y', 'z'], beni:['w', 'x', 'y', 'z']}"
    """
    student_list = [
        OOPStudent(id=agent, capacity=alloc.remaining_agent_capacities[agent], student_office=0, 
                   enrolled_or_not_enrolled={item:0 for item in alloc.remaining_items()}, 
                   cardinal={item:alloc.remaining_agent_item_value[agent][item] for item in alloc.remaining_items()},
                   forbid_enrollment_in_same_course_group=False)
        for agent in alloc.remaining_agents()
    ]
    # [OOPStudent(1, 3, 1, {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0},{'aa 1': 400, 'ab 1': 150, 'ac 1': 230, 'ad 1': 200, 'ae 1': 20}), \
    #     OOPStudent(2, 3, 1, {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0}, {'aa 1': 245, 'ab 1': 252, 'ac 1': 256, 'ad 1': 246, 'ae 1': 1}), \
    #     OOPStudent(3, 3, 1, {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0}, {'aa 1': 243, 'ab 1': 230, 'ac 1': 240, 'ad 1': 245, 'ae 1': 42}),\
    #     OOPStudent(4, 3, 1, {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0}, {'aa 1': 251, 'ab 1': 235, 'ac 1': 242, 'ad 1': 201, 'ae 1': 71})]

    course_list = [
        OOPCourse(
             id_num=item, id_g=item, course_name=item, capacity_bounds=alloc.remaining_item_capacities[item], 
             start_time=None, end_time=None, semester=None, day=None, lec=None, office_num=None, elect=None, overlap_courses=[]
        )
        for item in alloc.remaining_items()
    ]
    #  course1 = OOPCourse(1, 10, 'aa 1', 2, '09:00:00', '11:00:00', 'a', 'Monday',  'l', 1, True)
    #  course2 = OOPCourse(2, 7, 'ab 1', 3, '11:00:00', '14:00:00', 'a', 'Sunday',  'e', 1, True)
    #  course3 = OOPCourse(3, 8, 'ac 1', 3, '12:00:00', '16:00:00', 'a', 'Wednesday',  'r', 1, True)
    #  course4 = OOPCourse(4, 6, 'ad 1', 2, '10:00:00', '13:00:00', 'a', 'Monday',  'e', 1, True)
    #  course5 = OOPCourse(5, 9, 'ae 1', 2, '12:00:00', '15:00:00', 'a', 'Thursday',  'r', 1, True)
    #  overlap_course(tmp_course_list)  # Currently we do not check whether courses overlap. This is left for the secretaries.

    algorithm(student_list, course_list)
    for student in student_list:
        student_bundle = list(filter(student.enrolled_or_not.__getitem__, alloc.remaining_items()))
        alloc.give_bundle(student.id, student_bundle)
    logger.info("Yekta-Day allocation: %s", alloc.sorted())

    iterated_maximum_matching(alloc)  # Avoid waste
    return alloc.sorted()




if __name__ == "__main__":
    import doctest
    print("\n",doctest.testmod(), "\n")

    # logger.addHandler(logging.StreamHandler())
    # logger.setLevel(logging.INFO)

    # iterated_maximum_matching.logger.addHandler(logging.StreamHandler())
    # iterated_maximum_matching.logger.setLevel(logging.INFO)

    from fairpy.courses.adaptors import divide_random_instance
    divide_random_instance(algorithm=yekta_day, 
                           num_of_agents=10, num_of_items=4, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
                           item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
                           random_seed=1)
