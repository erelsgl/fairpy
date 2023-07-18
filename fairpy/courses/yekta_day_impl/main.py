from copy import deepcopy, copy
import logging
from fairpy.courses.yekta_day_impl.course import OOPCourse
from fairpy.courses.yekta_day_impl.course_group import Course_group
from fairpy.courses.yekta_day_impl.student import OOPStudent
from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)


def check_overlap(student_object,
                  course_object, cal=True):  # Check if there is an overlap course to the course we tried to enroll
    """
      >>> student = OOPStudent(1, 5, 1, {'aa':0, 'ab': 1, 'ac': 0, 'ad': 0, 'ae': 1}, {'aa':0, 'ab': 20, 'ac': 30, 'ad': 40, 'ae': 0})
      >>> course = OOPCourse(1, 2, 'aa', 5, '12:00:00', '15:00:00', 'a', 'Monday', 'l', 1, True)
      >>> overlap_tmp1 = OOPCourse(3, 5, 'ab', 5, '14:00:00', '17:00:00', 'b', 'Thursday', 'l', 1,\
  True, [])
      >>> overlap_tmp2 = OOPCourse(2, 4, 'ac', 5, '11:00:00', '13:00:00', 'a', 'Sunday', 'l', 1,\
  True, [])
      >>> overlap_tmp3 = OOPCourse(5, 7, 'ad', 5, '12:00:00', '16:00:00', 'a', 'Sunday', 'l', 1,\
  True, [])
      >>> overlap_tmp4 = OOPCourse(3, 6, 'ae', 5, '12:00:00', '16:00:00', 'a', 'Wednesday', 'l', 1,\
  True, [])
      >>> course.set_overlap([])
      >>> check_overlap(student, course)
      False
      >>> student = OOPStudent(1, 5, 1, {'aa':0, 'ab': 1, 'ac': 0, 'ad': 0, 'ae': 1}, {'aa': 0, 'ab': 20, 'ac': 30, 'ad': 40, 'ae': 0})
      >>> course = OOPCourse(1, 2, 'aa', 5, '12:00:00', '15:00:00', 'a', 'Monday', 'l', 1, True, [])
      >>> overlap_tmp1 = OOPCourse(3, 5, 'ab', 5, '14:00:00', '17:00:00', 'b', 'Thursday', 'l', 1,\
  True, [])
      >>> overlap_tmp2 = OOPCourse(2, 4, 'ac', 5, '11:00:00', '13:00:00', 'a', 'Sunday', 'l', 1,\
  True, [])
      >>> overlap_tmp3 = OOPCourse(5, 7, 'ad', 5, '12:00:00', '16:00:00', 'a', 'Sunday', 'l', 1,\
  True, [])
      >>> overlap_tmp4 = OOPCourse(3, 6, 'ae', 5, '12:00:00', '14:00:00', 'a', 'Monday', 'l', 1,\
  True, [course])
      >>> course.set_overlap([overlap_tmp1, overlap_tmp2, overlap_tmp3, overlap_tmp4])
      >>> check_overlap(student, course)
      True
      """
    overlap_courses = course_object.get_overlap_list()
    if len(overlap_courses) > 0:  # If there isn't overlap course we can simply say there isn't an overlap course
        output = False  # We'll presume there is no enrolled course such that is overlapped with course_object
        enroll_status = student_object.get_enrolment_status()
        course_name = None
        for overlap in range(len(overlap_courses)):
            if not output:
                course_name = overlap_courses[overlap]
                check = enroll_status[course_name.get_name()]
                if check == 1:  # If The student is enroll to overlap course
                    if not output:
                        output = True
                        break
        if output and cal:
            logger.info("Course: %s , overlap with: %s, for student: %s, reason: overlap algorithm",
                         course_object.get_name(), course_name.get_name(), student_object.get_id())
        return output


    else:
        return False


def SP_calibration(student_list, elective_course_list):
    logger.info("CALIBRATION PROCESS")
    for student in student_list:
        pre = list(student.get_next_preference(False).items())
        for course in elective_course_list:
            if course.get_remaining_capacity() == 0 and pre[0][0] == course.get_name():
                logger.info("student ID: %s, preferred course : %s , bid amount: %d, reason: capacity calibration"
                             , student.get_id(), pre[0][0], pre[0][1])

                student.delete_current_preference()
                student.add_gap(pre[0][1])
                course.enrolled_student_receive(pre[0][1])

            elif check_overlap(student, course, False) and pre[0][0] == course.get_name():
                logger.info("student ID: %s, preferred course : %s , bid amount: %d, reason: overlap calibration"
                             , student.get_id(), pre[0][0], pre[0][1])
                student.delete_current_preference()
                student.add_gap(pre[0][1])


def SP_Algorithm(student_list, elective_course_list, round):
    student_need_to_enroll = copy(student_list)
    first_iteration = True
    while len(student_need_to_enroll) > 0:
        if first_iteration:
            logger.info("START REGULAR ITERATION")

        student_need_to_enroll = list(filter(lambda x: x.get_number_of_enrollments() < round, student_need_to_enroll))
        student_need_to_enroll = list(filter(lambda x: x.get_current_highest_bid() != 0, student_need_to_enroll))
        student_need_to_enroll = list(filter(lambda x: x.get_remaining_capacity() > 0, student_need_to_enroll))
        student_need_to_enroll = sorted(student_need_to_enroll, key=lambda x:
        [x.get_current_highest_bid(), x.current_highest_ordinal()], reverse=True)

        if len(student_need_to_enroll) > 0 and not first_iteration:
            logger.info("Enrolled students or students with no preference has been filtered")

        first_iteration = False
        need_to_break = False
        for student in student_need_to_enroll:
            change_try_to_enroll, try_to_enroll = student.get_next_preference(True)
            tmp_preference = list(change_try_to_enroll.items())
            bid_data = tmp_preference[0]
            original_bid = list(try_to_enroll.values())

            if original_bid[0] != bid_data[1]:
                logger.info("Try to enroll: student ID: %s, preferred course: %s , student bid: %d, original bid: %d",
                             student.get_id(), bid_data[0], bid_data[1], original_bid[0])

            else:
                logger.info("Try to enroll: student ID: %s, preferred course: %s , bid amount: %d.",
                             student.get_id(), bid_data[0], bid_data[1])

            for course in elective_course_list:
                if course.get_name() == bid_data[0]:
                    if course.get_remaining_capacity() > 0:
                        if not check_overlap(student, course):
                            logger.info("Student: %s, enroll to course: %s", student.get_id(), bid_data[0])
                            course.student_enrollment(student.get_id(), student)
                            student.got_enrolled(course.get_name())

                        else:

                            student.delete_current_preference()
                            student.add_gap(bid_data[1])
                            need_to_break = True
                            break

                    else:
                        logger.info("Course: %s, with bid: %d, student ID: %s, reason: capacity algorithm",
                                     bid_data[0], bid_data[1], student.get_id())
                        course.enrolled_student_receive(bid_data[1])
                        student.delete_current_preference()
                        student.add_gap(bid_data[1])
                        need_to_break = True
                        break

            if need_to_break:
                break


def algorithm(student_list, elective_course_list, rounds=5):
    """
      >>> student_list_tmp = [OOPStudent(1, 3, 1, {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0},{'aa 1': 400, 'ab 1': 150, 'ac 1': 230, 'ad 1': 200, 'ae 1': 20}), \
OOPStudent(2, 3, 1, {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0}, {'aa 1': 245, 'ab 1': 252, 'ac 1': 256, 'ad 1': 246, 'ae 1': 1}), \
OOPStudent(3, 3, 1, {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0}, {'aa 1': 243, 'ab 1': 230, 'ac 1': 240, 'ad 1': 245, 'ae 1': 42}),\
OOPStudent(4, 3, 1, {'aa 1': 0, 'ab 1': 0, 'ac 1': 0, 'ad 1': 0, 'ae 1': 0}, {'aa 1': 251, 'ab 1': 235, 'ac 1': 242, 'ad 1': 201, 'ae 1': 71})]
     >>> course1 = OOPCourse(1, 10, 'aa 1', 2, '09:00:00', '11:00:00', 'a', 'Monday',  'l', 1, True)
     >>> course2 = OOPCourse(2, 7, 'ab 1', 3, '11:00:00', '14:00:00', 'a', 'Sunday',  'e', 1, True)
     >>> course3 = OOPCourse(3, 8, 'ac 1', 3, '12:00:00', '16:00:00', 'a', 'Wednesday',  'r', 1, True)
     >>> course4 = OOPCourse(4, 6, 'ad 1', 2, '10:00:00', '13:00:00', 'a', 'Monday',  'e', 1, True)
     >>> course5 = OOPCourse(5, 9, 'ae 1', 2, '12:00:00', '15:00:00', 'a', 'Thursday',  'r', 1, True)
     >>> tmp_course_list = [course1, course2, course3, course4, course5]
     >>> overlap_course(tmp_course_list)
     >>> algorithm(student_list_tmp, tmp_course_list)
     >>> student_list_tmp[0].get_cardinal_utility()
     780
     >>> student_list_tmp[1].get_cardinal_utility()
     754
     >>> student_list_tmp[2].get_cardinal_utility()
     527
     >>> student_list_tmp[3].get_cardinal_utility()
     557
     >>> student_list_tmp[0].get_ordinal_utility()
     11
     >>> student_list_tmp[1].get_ordinal_utility()
     12
     >>> student_list_tmp[2].get_ordinal_utility()
     9
     >>> student_list_tmp[3].get_ordinal_utility()
     9
     """
    for i in range(1, rounds + 1):
        logger.info("Round: %d", i)
        SP_Algorithm(student_list, elective_course_list, i)
        SP_calibration(student_list, elective_course_list)


# Changes the orderDic of courses that we getting from the server and convert to an object OOPCourse
def order_course_data(raw_course_list):
    """
    >>> course_data =  order_course_data([OrderedDict([('id', 10), ('name', 'הסתברות למדעי המחשב 2'), ('is_elective', False),\
('office', 1), ('courses', [OrderedDict([('course_id', '1'), ('Semester', 'א'), ('lecturer', "פרופ' חפץ דן"),\
('capacity', 30), ('day', 'א'), ('time_start', '09:00:00'), ('time_end', '11:00:00'), \
('course_group', 'הסתברות למדעי המחשב 210')]),\
OrderedDict([('course_id', '2'), ('Semester', 'א'), ('lecturer', "פרופ' חפץ דן"), ('capacity', 30),\
('day', 'ב'), ('time_start', '09:00:00'), ('time_end', '11:00:00'), \
('course_group','הסתברות למדעי המחשב 210')])])])\
, OrderedDict([('id', 11), ('name', 'חישוביות'), ('is_elective', False), ('office', 1),\
('courses', [OrderedDict([('course_id', '3'), ('Semester', 'א'), ('lecturer', 'ד"ר פסקין צרניאבסקי ענת'),\
('capacity', 30), ('day', 'ב'), ('time_start', '15:00:00'), ('time_end', '18:00:00'),\
('course_group', 'חישוביות11')]), OrderedDict([('course_id', '4'), ('Semester', 'א'),\
('lecturer', 'ד"ר פסקין צרניאבסקי ענת'), ('capacity', 30), ('day', 'ג'), ('time_start', '11:00:00'),\
('time_end', '14:00:00'), ('course_group', 'חישוביות11')])])])])
    >>> course_data[0][0].get_name()
    'הסתברות למדעי המחשב 2'
    >>> course_data[2][2].get_name()
    'חישוביות 1'
    >>> len(course_data[1])
    0
    >>> len(course_data[2])
    4
    >>> len(course_data[0])
    2
    >>> course_data =  order_course_data([OrderedDict([('id', 10), ('name', 'הסתברות למדעי המחשב 2'),\
('is_elective', False), ('office', 1),\
('courses', [OrderedDict([('course_id', '1'), ('Semester', 'א'), ('lecturer', "פרופ' חפץ דן"), ('capacity', 30),\
('day', 'א'), ('time_start', '09:00:00'), ('time_end', '11:00:00'), ('course_group', 'הסתברות למדעי המחשב 210')]),\
OrderedDict([('course_id', '2'), ('Semester', 'א'), ('lecturer', "פרופ' חפץ דן"), ('capacity', 30), ('day', 'ב'),\
('time_start', '09:00:00'), ('time_end', '11:00:00'), ('course_group', 'הסתברות למדעי המחשב 210')])])]),\
OrderedDict([('id', 11), ('name', 'חישוביות'), ('is_elective', False), ('office', 1),\
('courses', [OrderedDict([('course_id', '3'), ('Semester', 'א'), ('lecturer', 'ד"ר פסקין צרניאבסקי ענת'),\
('capacity', 30), ('day', 'ב'), ('time_start', '15:00:00'), ('time_end', '18:00:00'),\
('course_group', 'חישוביות11')]), OrderedDict([('course_id', '4'), ('Semester', 'א'),\
('lecturer', 'ד"ר פסקין צרניאבסקי ענת'), ('capacity', 30), ('day', 'ג'), ('time_start', '11:00:00'),\
('time_end', '14:00:00'), ('course_group', 'חישוביות11')])])]),\
OrderedDict([('id', 28), ('name', 'מבוא לקריפטוגרפיה'), ('is_elective', True), ('office', 1),\
('courses', [OrderedDict([('course_id', '71'),  ('Semester', 'א'), ('lecturer', '\tד"ר פסקין צרניאבסקי ענת'),\
('capacity', 10), ('day', 'א'), ('time_start', '12:00:00'), ('time_end', '15:00:00'),\
('course_group', 'מבוא לקריפטוגרפיה28')])])])])
    >>> course_data[2][0].get_start()
    '09:00:00'
    >>> course_data[1][0].get_name()
    'מבוא לקריפטוגרפיה 1'
    >>> course_data[2][2].get_name()
    'חישוביות 1'
    >>> len(course_data[1])
    1
   """

    group_course_list = []
    course_list_elective_output = []
    course_list_mandatory_output = []
    possible_list = []

    logger.info("Procedure of creating Group_course and Course")
    create_course = 0
    create_group = 0

    for dic in raw_course_list:
        id_group = int(dic['id'])
        name = dic['name']
        name = name.replace('\t', '')
        id_office = int(dic['office'])
        elect = dic['is_elective']

        counter = 1
        for dic2 in dic['courses']:  # dic2 is representing the courses of group_course (= dic1)
            id = int(dic2['course_id'])
            semester = dic2['Semester']
            lecturer = dic2['lecturer']
            capacity = int(dic2['capacity'])
            day = dic2['day']
            start = dic2['time_start']
            end = dic2['time_end']
            tmp = OOPCourse(id, id_group, name + ' ' + str(counter), capacity, start, end, semester, day, lecturer,
                            id_office, elect)
            logger.info("New course name %s %s", name, str(counter))
            create_course += 1
            counter += 1
            possible_list.append(tmp)

        if elect:
            for co in possible_list:
                course_list_elective_output.append(co)

        else:
            for co in possible_list:
                course_list_mandatory_output.append(co)

        new_group = Course_group(id_group, name, id_office, copy(possible_list))
        create_group += 1
        group_course_list.append(new_group)
        possible_list.clear()

    return group_course_list, course_list_elective_output, course_list_mandatory_output


def overlap_course(course_list):
    # Check which course is overlap each and other, for overlap the courses must be
    # in the same semester and day before checking if they overlap.
    # Afterward we check if course is starting while other course has been starting and finish later or
    # the course is ending while other course has been start and not finish yet or the starting and ending
    # time is the same. this is the three option that if one of that happened we add the other course
    # to the list of overlap courses the course we checking currently

    """
    >>> courses = [OOPCourse(1, 10, 'a', 30, '09:00:00', '11:00:00', 'a', 'monday',  'l', 1, False)]
    >>> courses.append(OOPCourse(2, 7, 'b', 25, '11:00:00', '14:00:00', 'b', 'Thursday',  'e', 1, False))
    >>> courses.append(OOPCourse(3, 5, 'c', 25, '10:00:00', '13:00:00', 'c', 'Thursday',  'r', 2, False))
    >>> overlap_course(courses)
    >>> courses[0].get_overlap_list()
    []
    >>> courses[1].get_overlap_list()
    []
    >>> courses[2].get_overlap_list()
    []
    >>> courses = [OOPCourse(1, 10, 'aa', 30, '09:00:00', '11:00:00', 'a', 'monday',  'l', 1, False)]
    >>> courses.append(OOPCourse(2, 7, 'ab', 25, '11:00:00', '14:00:00', 'a', 'Thursday',  'e', 1, False))
    >>> courses.append(OOPCourse(3, 5, 'ac', 25, '10:00:00', '13:00:00', 'a', 'Thursday',  'r', 1, False))
    >>> overlap_course(courses)
    >>> courses[0].get_overlap_list()
    []
    >>> courses[1].get_overlap_list()[0].get_name()
    'ac'
    >>> courses[2].get_overlap_list()[0].get_name()
    'ab'
    >>> courses = [OOPCourse(1, 10, 'aa', 30, '09:00:00', '11:00:00', 'a', 'monday',  'l', 1, False)]
    >>> courses.append(OOPCourse(2, 7, 'ab', 25, '11:00:00', '14:00:00', 'b', 'monday',  'e', 1, False))
    >>> courses.append(OOPCourse(3, 5, 'ac', 25, '10:00:00', '13:00:00', 'c', 'monday',  'r', 1, False))
    >>> overlap_course(courses)
    >>> courses[0].get_overlap_list()
    []
    >>> courses[1].get_overlap_list()
    []
    >>> courses[2].get_overlap_list()
    []
    >>> courses = [OOPCourse(1, 10, 'aa', 30, '09:00:00', '11:00:00', 'a', 'monday',  'l', 1, False)]
    >>> courses.append(OOPCourse(2, 7, 'ab', 25, '11:00:00', '14:00:00', 'a', 'monday',  'e', 1, False))
    >>> courses.append(OOPCourse(3, 5, 'ac', 25, '14:00:00', '16:00:00', 'a', 'monday',  'r', 1, False))
    >>> overlap_course(courses)
    >>> courses[0].get_overlap_list()
    []
    >>> courses[1].get_overlap_list()
    []
    >>> courses[2].get_overlap_list()
    []
    """

    for i in range(len(course_list)):
        overlap_list_for_i = []
        for j in range(len(course_list)):
            if not i == j:  # If it's not same course
                if course_list[j].get_day() == course_list[i].get_day():  # If it's in the same day
                    if course_list[j].get_semester() == course_list[i].get_semester():  # If it's in the same day
                        if course_list[j].get_start() <= course_list[i].get_start() < course_list[j].get_end():
                            overlap_list_for_i.append(course_list[j])

                        elif course_list[j].get_start() < course_list[i].get_end() <= course_list[j].get_end():
                            overlap_list_for_i.append(course_list[j])

                        elif course_list[j].get_start() == course_list[i].get_start() and \
                                course_list[i].get_end() == course_list[j].get_end():
                            overlap_list_for_i.append(course_list[j])

        course_list[i].set_overlap(overlap_list_for_i)
        overlap_list_for_i.clear()


def order_student_data(raw_student_list, raw_rank_list, elective_course_list, course_list):
    counter = 0
    indexed_enrollment = {}
    cardinal_order = {}
    student_list = []

    for i in course_list:
        indexed_enrollment[i.get_name()] = 0

        if i.get_elective():
            cardinal_order[i.get_name()] = 0

    logger.info("starting procedure of creating students")

    for dic in raw_student_list:
        deepcopy_indexed_enrollment = deepcopy(indexed_enrollment)
        deepcopy_cardinal_order = deepcopy(cardinal_order)
        id = int(dic['student_id'])
        need_to_enroll = int(dic['amount_elective'])
        office = int(dic['office'])

        # Updating the enrollment status for mandatory courses

        for i in range(len(course_list)):
            for dic2 in dic['courses']:
                if course_list[i].get_id() == int(dic2['course_id']):
                    deepcopy_indexed_enrollment[course_list[i].get_name()] = 1

        for rank_dic in raw_rank_list:  # Update the ranking of elective courses for all student in current office
            student_id = int(rank_dic['student'][0:9])  # Taking the student id for checking if is the same student
            course_id = int(rank_dic['course'])
            rank = int(rank_dic['rank'])

            if student_id == id:
                for course in elective_course_list:
                    if course.get_id() == course_id:
                        deepcopy_cardinal_order[course.get_name()] = rank

        logger.info("Create a new student number %d.", counter)

        s = OOPStudent(id, need_to_enroll, office, deepcopy(deepcopy_indexed_enrollment),
                       deepcopy(deepcopy_cardinal_order))
        student_list.append(s)
        counter += 1

    return student_list


def main(raw_student_list, raw_course_list, raw_rank_list):
    course_group_list, course_elect_list, course_mandatory_list = order_course_data(raw_course_list)

    logger.info("Now merging the elective and mandatory courses for checking possible overlap while maintaining the"
                 "separation of courses according to the office number")

    course_list = course_elect_list + course_mandatory_list
    overlap_course(course_list)

    logger.info(
        "while convert the student data from order dictionary to Student we sort student according to their office ")
    student_list = order_student_data(raw_student_list, raw_rank_list, course_elect_list, course_list)

    logger.info("Order the data for the algorithm in a list of dictionaries as each dictionary is represent"
                 " a single office while the data is portrayed by {student id: dictionary of cardinal ranking"
                 " of the same student}")

    logger.info("Activate the algorithm")
    algorithm(student_list, course_elect_list)

    boolean_utility = 0
    cardinal_utility = 0
    ordinal_utility = 0
    min_cardinal = 0
    max_cardinal = 0
    min_ordinal = 0
    max_ordinal = 0
    for i in student_list:
        to_count = True
        boolean_utility += i.get_number_of_enrollments()
        cardinal_utility += i.get_cardinal_utility()

        if max_cardinal < i.get_cardinal_utility():
            max_cardinal = i.get_cardinal_utility()

        if min_cardinal == 0 and i.get_cardinal_utility() > 200:
            to_count = False
            min_cardinal = i.get_cardinal_utility()

        elif min_cardinal > i.get_cardinal_utility() > 200:
            min_cardinal = i.get_cardinal_utility()

        ordinal_utility += i.get_ordinal_utility()

        if max_ordinal < i.get_ordinal_utility():
            max_ordinal = i.get_ordinal_utility()

        if (min_ordinal > i.get_ordinal_utility() or min_ordinal == 0) and to_count:
            min_ordinal = i.get_ordinal_utility()

    logger.info("Boolean utility is: %d", boolean_utility)
    logger.info("Ordinal utility is: %d", ordinal_utility)
    logger.info("Cardinal utility is: %d", cardinal_utility)
    logger.info("Cardinal range is: %d, When the max is: %d", max_cardinal - min_cardinal, max_cardinal)
    logger.info("Ordinal range is: %d, When the max is: %d", max_ordinal - min_ordinal, max_ordinal)

    return student_list, course_elect_list


if __name__ == "__main__":
    import doctest

    logger.setLevel(logging.INFO)
    print(doctest.testmod())
