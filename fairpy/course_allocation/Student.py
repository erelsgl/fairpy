class Student:
    def __init__(self,name:str, budget:float, preferences:list, courses:list = [], year:int=1) -> None:
        self.name = name
        self.budget = budget
        self.courses = courses
        self.preferences = preferences   