from copy import deepcopy
from Course import Course
class Student:
    def __init__(self,name, budget, preferences, courses = [], year=1):
        self.name = name
        self.budget = budget
        self.courses = courses
        self.preferences = preferences   
        self.year = year 

    def __str__(self) -> str:
        return self.name + " year: " + str(self.year) + "with budget of (" + str(self.budget)  + ") \n" + str(self.courses) + "\n " + str(self.preferences) 
    
    def comperator(a, b):
        if(a.year - b.year == 0):
            return (a.budget - b.budget)
        return a.year - b.year