from algorithm1 import algorithm1,Course,Student,random,TabuList,copy,map_price_demand,reset_update_prices,cmp_to_key,reset_students,time
def test1(): 
    a = Course(name='a', price=0, max_capacity=5)
    b = Course(name='b', price=0, max_capacity=3)
    c = Course(name='c', price=0, max_capacity=5)
    courses = [a, b, c]

    s1 = Student(name='s1', budget=15, preferences=([c, b]))
    s2 = Student(name='s2', budget=15, preferences=([b, c, a]))
    s3 = Student(name='s3', budget=15, preferences=([b, a]))
    s4 = Student(name='s4', budget=15, preferences=([a, c]))
    s5 = Student(name='s5', budget=15, preferences=([a, b, c]))
    students = [s1, s2, s3, s4, s5]
    max_budget = 15
    # #when we giving sufficient time for the algorithm it's getting the (best error == 3)
    assert(algorithm1(students, courses, max_budget, time_to= 1, seed = 3) == [4.5, 4.5, 1.5])

def test2():
    a = Course(name='a', price=0, max_capacity=3)
    b = Course(name='b', price=0, max_capacity=3)
    c = Course(name='c', price=0, max_capacity=3)
    courses = [a, b, c]
    s1 = Student(name='s1', budget=10, courses=[], preferences=([a]))
    s2 = Student(name='s2', budget=10, courses=[], preferences=([b,a]))
    s3 = Student(name='s3', budget=10, courses=[], preferences=([c]))
    s4 = Student(name='s4', budget=10, courses=[], preferences=([c,b]))
    s5 = Student(name='s5', budget=10, courses=[], preferences=([c, a, b]))
    students = [s1, s2, s3, s4, s5]

    max_budget = 10
    assert(algorithm1(students, courses, max_budget, time_to= 1, seed = 3) == [1.0, 2.0, 1.0])

def test3():
    a = Course(name='a', price=0, capacity=0, max_capacity=5)
    b = Course(name='b', price=0, capacity=0, max_capacity=4)
    c = Course(name='c', price=0, capacity=0, max_capacity=5)
    d = Course(name='d', price=0, capacity=0, max_capacity=3)
    e = Course(name='e', price=0, capacity=0, max_capacity=7)
    f = Course(name='f', price=0, capacity=0, max_capacity=2)
    courses = [a, b, c, d, e, f]
    s1 = Student(name='s1', budget=18, year=1, courses=[], preferences=([c, b, e, f]))
    s2 = Student(name='s2', budget=18, year=1, courses=[], preferences=([b, c, a, e]))
    s3 = Student(name='s3', budget=18, year=1, courses=[], preferences=([b, a, d]))
    s4 = Student(name='s4', budget=18, year=1, courses=[], preferences=([a, b, c]))
    s5 = Student(name='s5', budget=18, year=1, courses=[], preferences=([d, a,e, b, c]))
    s6 = Student(name='s6', budget=18, year=1, courses=[], preferences=([a, e,c,f, b]))
    s7 = Student(name='s7', budget=18, year=1, courses=[], preferences=([c,d ,b]))
    s8 = Student(name='s8', budget=18, year=1, courses=[], preferences=([b, c, a]))
    s9 = Student(name='s9', budget=18, year=1, courses=[], preferences=([b,f,e, a]))
    s10 = Student(name='s10', budget=18, year=1, courses=[], preferences=([d ,f]))
    s11 = Student(name='s11', budget=18, year=1, courses=[], preferences=([d,e,f]))
    s12 = Student(name='s12', budget=18, year=1, courses=[], preferences=([d,f,e]))
    students = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12]
    max_budget = 18
    assert(algorithm1(students, courses, max_budget, time_to= 1, seed = 3) == [5.3999999999999995, 14.4, 7.2, 16.2, 1.8, 12.6])#7

'''
disclaimer for testing
the tests are not conclusive since computing power may vary
and they using time which work differently in different machines.
that worked on laptop with this specs:
cpu = i5 6200u
os = ubuntu
graphics card = None
and youtube in the background...
'''