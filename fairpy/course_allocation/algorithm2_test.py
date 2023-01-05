from algorithm2 import algorithm2,Course,Student,csp_mapping,copy,math,cmp_to_key

def test_1(): 
    a = Course(name='a', price=9, max_capacity=5)
    b = Course(name='b', price=2, max_capacity=3)
    c = Course(name='c', price=4.5, max_capacity=5)
    s1 = Student(name='s1', budget=15, preferences=([c, b]))
    s2 = Student(name='s2', budget=15, preferences=([b, c, a]))
    s3 = Student(name='s3', budget=15, preferences=([b, a]))
    s4 = Student(name='s4', budget=15, preferences=([a, c]))
    s5 = Student(name='s5', budget=15, preferences=([a, b, c]))
    courses = [a, b, c]
    students = [s1, s2, s3, s4, s5]
    
    eps = 1
    maximum = 10
    price_vector = [9,2,4.5]
    assert algorithm2(price_vector, maximum, eps, csp_mapping, students, courses) == [9,10,4.5]

def test_2(): 
    a = Course(name='a', price=2.4, capacity=0, max_capacity=5)
    b = Course(name='b', price=5, capacity=0, max_capacity=4)
    c = Course(name='c', price=10.4, capacity=0, max_capacity=5)
    courses = [a, b, c]


    s1 = Student(name='s1', budget=18, year=1, courses=[], preferences=([c, b]))
    s2 = Student(name='s2', budget=18, year=1, courses=[], preferences=([b, c, a]))
    s3 = Student(name='s3', budget=18, year=1, courses=[], preferences=([b, a]))
    s4 = Student(name='s4', budget=18, year=1, courses=[], preferences=([a, c]))
    s5 = Student(name='s5', budget=18, year=1, courses=[], preferences=([a, b, c]))
    s6 = Student(name='s6', budget=18, year=1, courses=[], preferences=([a, c, b]))
    students = [s1, s2, s3, s4, s5, s6]
    eps = 1
    maximum = 10
    price_vector = [2.4,5,10.4]
    assert algorithm2(price_vector, maximum, eps, csp_mapping, students, courses) == [2.4,8.125,10.4]


def test_3():
    a = Course(name='a', price=3, max_capacity=5)
    b = Course(name='b', price=4, max_capacity=3)
    c = Course(name='c', price=3, max_capacity=5)
    courses = [a, b, c]
    s1 = Student(name='s1', budget=10, preferences=([c, b]))
    s2 = Student(name='s2', budget=10, preferences=([b, c, a]))
    s3 = Student(name='s3', budget=10, preferences=([b, a]))
    s4 = Student(name='s4', budget=10, preferences=([a, b, c]))
    s5 = Student(name='s5', budget=10, preferences=([a, b, c]))
    students = [s1, s2, s3, s4, s5]
    eps = 0.1
    maximum = 6
    price_vector = [3,4,3]
    assert(algorithm2(price_vector, maximum, eps, csp_mapping, students, courses)==[3,6,3])

if __name__=="main_":
    import pytest
    pytest.main()