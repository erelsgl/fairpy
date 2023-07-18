from copy import deepcopy

class OOPCourse:

    def __init__(self, id_num, id_g, course_name, capacity_bounds, start_time, end_time, semester, day, lec,
                 office_num, elect, overlap_courses=[]):
        self.id = id_num
        self.id_group = id_g
        self.name = course_name
        self.capacity = capacity_bounds
        self.students = []
        self.students_name = []
        self.overlap = set(overlap_courses)
        self.start = start_time
        self.end = end_time
        self.sem = semester
        self.d = day
        self.lecturer = lec
        self.office = office_num
        self.elective = elect
        self.highest_bid_rejected = 0


    def enrolled_student_receive(self, given_rejected_bid=0):
        if self.capacity == 0 and given_rejected_bid > 0:
            if self.highest_bid_rejected < given_rejected_bid:
                self.highest_bid_rejected = given_rejected_bid
                for stu in self.students:
                    stu.receive_unspent_points(self.highest_bid_rejected, self.name)


    def student_enrollment(self, student_name, student_element):
        """

        """
        if self.capacity == 0:
            raise Exception(f"The course named {self.name} have no remaining capacity")
        elif student_name in self.students_name:
            raise Exception(f"The student {student_name} had been enrolled already for course {self.name}")
        elif student_element.get_remaining_capacity() ==0:
            raise Exception(f"Student {student_name} got to his capacity of enrollments for course: {self.name}")
        else:
            self.capacity -= 1
            self.students.append(student_element)
            self.students_name.append(student_name)


    def set_overlap(self, overlap_list):
        self.overlap = deepcopy(overlap_list)

    def get_id(self):
        return self.id

    def get_id_group(self):
        return self.id_group

    def get_office(self):
        return self.office

    def get_elective(self):
        return self.elective

    def get_lowest_bid(self):
        return self.lowest_bid

    def get_overlap_list(self):
        return self.overlap

    def get_name(self):
        return self.name

    def get_remaining_capacity(self):
        return self.capacity

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_semester(self):
        return self.sem

    def get_day(self):
        return self.d

    def to_string(self):
        print("Course name: ", self.name, ", Capacity: ", self.capacity, "\n" 
              "Number of student that enroll to this course is: ", len(self.students), "\n"
              "Student list: ", self.students_name, "\n")

        print("Overlap courses are: ")
        for i in self.overlap:
            print(i.get_name())

if __name__ == "__main__":
    import doctest
    doctest.testmod()