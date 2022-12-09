class Course:
    def __init__(self, name:str, price:float, max_capacity:int, capacity:int = 0) -> None:
        self.name = name
        self.price = price
        self.capacity = capacity
        self.max_capacity = max_capacity