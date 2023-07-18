import logging
from copy import deepcopy

import logging
logger = logging.getLogger(__name__)


def check_budget(order):
    sum_bidding = 0
    order_values = list(order.values())
    for i in range(len(order_values)):
        sum_bidding += order_values[i]

    if sum_bidding > 1000:
        raise Exception("Sorry, the sum of bidding is can't be summarized above 1000")

    else:
        return True


def create_ordinal_order(order):
    count = 1
    ordinal = list(order.values())
    course_names = list(order.keys())
    for i in range(len(ordinal)):
        ind = ordinal.index(max(ordinal))
        ordinal[ind] = count
        count += 1

    output = deepcopy(order)
    for i in range(len(output)):
        output[course_names[i]] = ordinal[i]

    return output


class OOPStudent:

    def __init__(self, id: int, capacity: int, student_office: int, enrolled_or_not_enrolled: dict, cardinal: dict,
                 forbid_enrollment_in_same_course_group:bool=True):
        self.id = id
        self.capacity = capacity   # The number of courses that this student needs to enroll to
        self.enrolled_num = 0
        self.cardinal_order = deepcopy(cardinal)
        self.changeable_cardinal_order = deepcopy(cardinal)
        self.enrolled_or_not = enrolled_or_not_enrolled  # dictionary that the key is course name and the value
           # represents if the student is enroll or not when 1 mean enrolled while 0 is not enroll yet
        self.ordinal_order = create_ordinal_order(self.cardinal_order)
        self.changeable_ordinal_order = deepcopy(self.ordinal_order)
        self.cardinal_utility = 0
        self.ordinal_utility = 0
        self.office = student_office
        self.forbid_enrollment_in_same_course_group= forbid_enrollment_in_same_course_group

    def if_student_enroll(self, course_name):
        return self.enrolled_or_not[course_name] == 1

    def get_id(self):
        return self.id

    def get_office(self):
        return self.office

    def get_ordinal(self):
        return self.ordinal_order

    def get_cardinal(self):
        return self.cardinal_order

    def get_changeable_cardinal(self):
        return self.changeable_cardinal_order

    def get_cardinal_utility(self):
        return self.cardinal_utility

    def get_ordinal_utility(self):
        return self.ordinal_utility

    def get_remaining_capacity(self):
        return self.capacity

    def get_enrolment_status(self):
        return self.enrolled_or_not

    def enrolled_to_other_option(self, course_name):
        """
        After the student has enrolled to a course in some course-group,
              we have to ensure that no other courses of the same course-group are given to the student.

        WARNING: This function currently relies on slicing the course name, which is very unreliable. 
                 Use at your own risk!

        >>> s = OOPStudent(1, 5, 1, {'aa 1': 0, 'aa 2': 0, 'ab 1': 0, 'ab 2': 0, 'ac 1': 0},\
{'aa 1': 40, 'aa 2': 7, 'ab 1': 30, 'ab 2': 20, 'ac 1': 13})
        >>> s.got_enrolled('aa 1')
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'aa 2': 0, 'ab 1': 30, 'ab 2': 20, 'ac 1': 13}
        >>> s.got_enrolled('ab 2')
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'aa 2': 0, 'ab 1': 0, 'ab 2': 0, 'ac 1': 13}
         >>> s = OOPStudent(1, 5, 1, {'aa 1': 0, 'aa 2': 0, 'ab 1': 0, 'ab 2': 0, 'ac 1': 0},\
{'aa 1': 40, 'aa 2': 7, 'ab 1': 30, 'ab 2': 20, 'ac 1': 13})
        >>> s.got_enrolled('ac 1')
        >>> s.get_changeable_cardinal()
        {'aa 1': 40, 'aa 2': 7, 'ab 1': 30, 'ab 2': 20, 'ac 1': 0}
        >>> s.got_enrolled('aa 2')
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'aa 2': 0, 'ab 1': 30, 'ab 2': 20, 'ac 1': 0}
        """
        sliced_name = course_name[:-2]
        names = list(self.changeable_cardinal_order.keys())
        index_first = names.index(sliced_name + ' 1')  # Searching for <course-name> 1 such that after him there will be
        # <course-name> 2 <course-name> 3 and so on
        not_found = True
        while not_found:
            if index_first < len(names) and names[index_first][:-2] == sliced_name:
                self.changeable_cardinal_order[names[index_first]] = 0
                index_first += 1
            else:
                not_found = False  # In case if the course named has changed so we stop here

    def delete_current_preference(self):
        """
        >>> s = OOPStudent(1, 5, 1, {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0},\
{'aa 1': 40, 'ab 1': 7, 'ac 1': 30, 'ad 1': 20, 'ae 1': 13})
        >>> s.delete_current_preference()
        40
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'ab 1': 7, 'ac 1': 30, 'ad 1': 20, 'ae 1': 13}
        >>> s.delete_current_preference()
        30
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'ab 1': 7, 'ac 1': 0, 'ad 1': 20, 'ae 1': 13}
        >>> s.delete_current_preference()
        20
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'ab 1': 7, 'ac 1': 0, 'ad 1': 0, 'ae 1': 13}
        >>> s.delete_current_preference()
        13
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'ab 1': 7, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0}
        >>> s.delete_current_preference()
        7
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0}
        >>> s = OOPStudent(1, 5, 1, {'aa 1': 0, 'aa 2': 0, 'ab 1': 0, 'ab 2': 0, 'ac 1': 0},\
{'aa 1': 40, 'aa 2': 7, 'ab 1': 30, 'ab 2': 20, 'ac 1': 13})
        >>> s.got_enrolled('aa 2')
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'aa 2': 0, 'ab 1': 30, 'ab 2': 20, 'ac 1': 13}
        >>> s.delete_current_preference()
        30
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'aa 2': 0, 'ab 1': 0, 'ab 2': 20, 'ac 1': 13}
        """
        cardinal_value = list(self.changeable_cardinal_order.values())
        cardinal_keys = list(self.changeable_cardinal_order.keys())
        max_value_index = cardinal_value.index(max(cardinal_value))
        course_name = cardinal_keys[max_value_index]
        self.changeable_cardinal_order[course_name] = 0
        cardinal_value[max_value_index] = 0
        return self.cardinal_order[course_name] # WATCH OUT Returning the original value when deleting and not changed
                                                # value

    def get_next_preference(self, return_original_or_not):
        """
        >>> s = OOPStudent(1, 5, 1, {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0},\
{'aa 1': 40, 'ab 1': 7, 'ac 1': 30, 'ad 1': 20, 'ae 1': 13})
        >>> s.get_next_preference(False)
        {'aa 1': 40}
        >>> s.got_enrolled('aa 1')
        >>> s.get_next_preference(False)
        {'ac 1': 30}
        >>> s.got_enrolled('ae 1')
        >>> s.get_next_preference(False)
        {'ac 1': 30}
        >>> s.got_enrolled('ac 1')
        >>> s.get_next_preference(False)
        {'ad 1': 20}
        """
        changeable_cardinal_value = list(self.changeable_cardinal_order.values())
        changeable_cardinal_keys = list(self.changeable_cardinal_order.keys())
        cardinal_value = list(self.cardinal_order.values())
        max_value_index = changeable_cardinal_value.index(max(changeable_cardinal_value))
        if return_original_or_not:
            return {changeable_cardinal_keys[max_value_index]: changeable_cardinal_value[max_value_index]},\
                   {changeable_cardinal_keys[max_value_index]: cardinal_value[max_value_index]}

        else:
            return {changeable_cardinal_keys[max_value_index]: changeable_cardinal_value[max_value_index]}

    def get_number_of_enrollments(self):
        return self.enrolled_num

    def add_gap(self, gap=0):
        """
        >>> s = OOPStudent(1, 5, 1, {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0},\
{'aa 1': 40, 'ab 1': 7, 'ac 1': 30, 'ad 1': 20, 'ae 1': 13})
        >>> s.delete_current_preference()
        40
        >>> s.add_gap(0)
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'ab 1': 7, 'ac 1': 30, 'ad 1': 20, 'ae 1': 13}
        >>> s.delete_current_preference()
        30
        >>> s.add_gap(10)
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'ab 1': 7, 'ac 1': 0, 'ad 1': 30, 'ae 1': 13}
        >>> s.delete_current_preference()
        20
        >>> s.add_gap(5)
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'ab 1': 7, 'ac 1': 0, 'ad 1': 0, 'ae 1': 18}
        >>> s.delete_current_preference()
        13
        >>> s.add_gap(25)
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'ab 1': 32, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0}
        >>> s.delete_current_preference()
        7
        >>> s.add_gap(10)
        >>> s.get_changeable_cardinal()
        {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0}
        """


        cardinal_value = list(self.changeable_cardinal_order.values())
        cardinal_keys = list(self.changeable_cardinal_order.keys())
        if cardinal_value.count(0) != len(cardinal_value):
            max_value_index = cardinal_value.index(max(cardinal_value))
            course_name = cardinal_keys[max_value_index]
            self.changeable_cardinal_order[course_name] = cardinal_value[max_value_index] + gap
            logger.info("student: %s, add to course: %s, the rejected amount: %d, original bid: %d"
                         ", total bid: %s", self.id, course_name, gap, self.changeable_cardinal_order[course_name]-gap
                         ,self.changeable_cardinal_order[course_name])


    def receive_unspent_points(self, highest_rejected, course_name):
        if self.enrolled_or_not[course_name] == 1: # Make Sure the student enrolled to the course
            gap = self.cardinal_order[course_name] - highest_rejected
            cardinal_value = list(self.changeable_cardinal_order.values())
            cardinal_keys = list(self.changeable_cardinal_order.keys())
            max_value_index = cardinal_value.index(max(cardinal_value))
            if gap < 0: # In case when the gap is negative we can understand this student is pay less than the rejected
                # student so we don't want to lower the bid and if the gap is negative we won't change the bids for this
                # studnt
                gap = 0
            self.changeable_cardinal_order[cardinal_keys[max_value_index]] += gap
            if gap > 0:
                logger.info(
                    "Returning points from: %s, to: %s, returning amount: %d, original bid: %d student ID: %s"
                    , course_name, cardinal_keys[max_value_index], gap,
                    self.changeable_cardinal_order[cardinal_keys[max_value_index]]-gap, self.id)


    def get_current_highest_bid(self):
        """
         >>> s = OOPStudent(1, 5, 1, {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0, 'af 1': 0},\
{'aa 1': 40, 'ab 1': 7, 'ac 1': 30, 'ad 1': 20, 'ae 1': 13, 'af 1': 28})
        >>> s.delete_current_preference()
        40
        >>> s.delete_current_preference()
        30
        >>> s.delete_current_preference()
        28
        >>> s.delete_current_preference()
        20
        >>> s.delete_current_preference()
        13
        >>> s2 = OOPStudent(1, 5, 1, {'aa 1': 0, 'aa 2': 0, 'ab 1': 0, 'ab 2': 0, 'ac 1': 0, 'ac 2': 0, 'ad 1': 0},\
{'aa 1': 40, 'aa 2': 40, 'ab 1': 30, 'ab 2': 30, 'ac 1': 13, 'ac 2': 13, 'ad 1': 18})
        >>> s2.delete_current_preference()
        40
        >>> s2.delete_current_preference()
        40
        >>> s2.delete_current_preference()
        30
        >>> s2.delete_current_preference()
        30
        >>> s2.delete_current_preference()
        18
        >>> s2.delete_current_preference()
        13
        >>> s2.delete_current_preference()
        13
        """
        changeable_cardinal_value = list(self.changeable_cardinal_order.values())
        index = changeable_cardinal_value.index(max(changeable_cardinal_value))
        return changeable_cardinal_value[index]

    def current_highest_ordinal(self):
        changeable_ordinal_value = list(self.changeable_ordinal_order.values())
        index = changeable_ordinal_value.index(max(changeable_ordinal_value))
        return changeable_ordinal_value[index]

    def got_enrolled(self, course_name):
        """
        >>> s = OOPStudent(1, 5, 1, {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0, 'af 1': 0},\
{'aa 1': 40, 'ab 1': 7, 'ac 1': 30, 'ad 1': 20, 'ae 1': 13, 'af 1': 28})
        >>> s.got_enrolled('aa 1')
        >>> s.enrolled_or_not
        {'aa 1': 1, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0, 'af 1': 0}
        >>> s.changeable_cardinal_order
        {'aa 1': 0, 'ab 1': 7, 'ac 1': 30, 'ad 1': 20, 'ae 1': 13, 'af 1': 28}
        >>> s.got_enrolled('ad 1')
        >>> s.enrolled_or_not
        {'aa 1': 1, 'ab 1': 0, 'ac 1': 0, 'ad 1': 1, 'ae 1': 0, 'af 1': 0}
        >>> s.changeable_cardinal_order
        {'aa 1': 0, 'ab 1': 7, 'ac 1': 30, 'ad 1': 0, 'ae 1': 13, 'af 1': 28}
        >>> s.got_enrolled('ac 1')
        >>> s.enrolled_or_not
        {'aa 1': 1, 'ab 1': 0, 'ac 1': 1, 'ad 1': 1, 'ae 1': 0, 'af 1': 0}
        >>> s.changeable_cardinal_order
        {'aa 1': 0, 'ab 1': 7, 'ac 1': 0, 'ad 1': 0, 'ae 1': 13, 'af 1': 28}
        >>> s.got_enrolled('af 1')
        >>> s.enrolled_or_not
        {'aa 1': 1, 'ab 1': 0, 'ac 1': 1, 'ad 1': 1, 'ae 1': 0, 'af 1': 1}
        >>> s.changeable_cardinal_order
        {'aa 1': 0, 'ab 1': 7, 'ac 1': 0, 'ad 1': 0, 'ae 1': 13, 'af 1': 0}
        >>> s.got_enrolled('af 1')
        Student:  1 , is already enrolled to the course:  af 1
        >>> s.got_enrolled('ae 1')
        >>> s.enrolled_or_not
        {'aa 1': 1, 'ab 1': 0, 'ac 1': 1, 'ad 1': 1, 'ae 1': 1, 'af 1': 1}
        >>> s.changeable_cardinal_order
        {'aa 1': 0, 'ab 1': 7, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0, 'af 1': 0}
        >>> s.got_enrolled('ab 1')
        Student:  1  got to the limit of courses enrollment
        >>> s.changeable_cardinal_order
        {'aa 1': 0, 'ab 1': 7, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0, 'af 1': 0}
        >>> s2 = OOPStudent(1, 5, 1, {'aa 1': 0, 'aa 2': 0, 'ab 1': 0, 'ab 2': 0, 'ac 1': 0, 'ac 2': 0, 'ad 1': 0},\
{'aa 1': 40, 'aa 2': 40, 'ab 1': 30, 'ab 2': 30, 'ac 1': 13, 'ac 2': 13, 'ad 1': 18})
        >>> s2.got_enrolled('aa 2')
        >>> s2.enrolled_or_not
        {'aa 1': 0, 'aa 2': 1, 'ab 1': 0, 'ab 2': 0, 'ac 1': 0, 'ac 2': 0, 'ad 1': 0}
        >>> s2.changeable_cardinal_order
        {'aa 1': 0, 'aa 2': 0, 'ab 1': 30, 'ab 2': 30, 'ac 1': 13, 'ac 2': 13, 'ad 1': 18}
        >>> s2.got_enrolled('ac 1')
        >>> s2.enrolled_or_not
        {'aa 1': 0, 'aa 2': 1, 'ab 1': 0, 'ab 2': 0, 'ac 1': 1, 'ac 2': 0, 'ad 1': 0}
        >>> s2.changeable_cardinal_order
        {'aa 1': 0, 'aa 2': 0, 'ab 1': 30, 'ab 2': 30, 'ac 1': 0, 'ac 2': 0, 'ad 1': 18}
        >>> s2.got_enrolled('ad 1')
        >>> s2.enrolled_or_not
        {'aa 1': 0, 'aa 2': 1, 'ab 1': 0, 'ab 2': 0, 'ac 1': 1, 'ac 2': 0, 'ad 1': 1}
        >>> s2.changeable_cardinal_order
        {'aa 1': 0, 'aa 2': 0, 'ab 1': 30, 'ab 2': 30, 'ac 1': 0, 'ac 2': 0, 'ad 1': 0}
        >>> s2.got_enrolled('ab 2')
        >>> s2.enrolled_or_not
        {'aa 1': 0, 'aa 2': 1, 'ab 1': 0, 'ab 2': 1, 'ac 1': 1, 'ac 2': 0, 'ad 1': 1}
        >>> s2.changeable_cardinal_order
        {'aa 1': 0, 'aa 2': 0, 'ab 1': 0, 'ab 2': 0, 'ac 1': 0, 'ac 2': 0, 'ad 1': 0}
        """

        if self.capacity > 0 and self.enrolled_or_not[course_name] == 0:
            #logger.info("We enroll student with ID %s to coursed named %s", self.id, course_name)
            self.capacity -= 1
            self.cardinal_utility += self.cardinal_order[course_name]
            self.changeable_cardinal_order[course_name] = 0
            self.changeable_ordinal_order[course_name] = 0
            self.enrolled_or_not[course_name] = 1
            self.enrolled_num += 1
            self.ordinal_utility += len(self.ordinal_order) - self.ordinal_order[course_name] + 1
            if self.forbid_enrollment_in_same_course_group:
                self.enrolled_to_other_option(course_name)

        elif self.enrolled_or_not[course_name] == 1:
            print("Student: ", self.id, ", is already enrolled to the course: ", course_name)

        else:
            print("Student: ", self.id, " got to the limit of courses enrollment")

    def to_string(self):
        print("Student id:", self.id, ", The cardinal order is: ", self.cardinal_order, "\n"  "The ordinal is: ",
              self.ordinal_order, "\n", "the number of courses that student has been enrolled is ", self.enrolled_num,
              "\n", "The courses that: ", self.id, " enrolled are: ")

        for key, value in self.enrolled_or_not.items():
            if value == 1:
                print(key)

        print("The cardinal utility is: ", self.cardinal_utility, ", The ordinal utility is: ", self.ordinal_utility)


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
