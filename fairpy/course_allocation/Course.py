from copy import deepcopy

class Course:
    def __init__(self, name:str, price:float, max_capacity:int, capacity:int = 0) -> None:
        self.name = name
        self.price = price
        self.capacity = capacity
        self.max_capacity = max_capacity
    
    def comperator(a, b):
        return (a.capacity - a.max_capacity) - (b.capacity - b.max_capacity)
        
    
    def __str__(self) -> str:
        return  f"course name: {self.name} capacity {self.capacity}/{self.max_capacity} and priced {self.price}"