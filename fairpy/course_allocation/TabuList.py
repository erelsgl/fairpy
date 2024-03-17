class TabuList:
    def __init__(self, size):
        self.size = size
        self.items = []

    def add(self, item):
        if item not in self.items:
            self.items.append(item)
        while len(self.items) > self.size:
            self.items.pop(0)
    
    def __iter__(self):
        return iter(self.items)
    

    