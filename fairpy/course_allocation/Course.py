from copy import deepcopy

class Course:
    def __init__(self, name:str, price:float, max_capacity:int, capacity:int = 0) -> None:
        self.name = name
        self.price = price
        self.capacity = capacity
        self.max_capacity = max_capacity
        self.mark = False # if cant be helpd we mark course
    
    def comperator(a, b):
        if(a.mark == b.mark):
            return (a.capacity - a.max_capacity) - (b.capacity - b.max_capacity)
        if(a.mark): return -1
        if(b.mark): return 1
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result