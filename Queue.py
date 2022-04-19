from List import List
from Node import Node

class Queue(List):
    def __init__(self) -> None:
        super().__init__()

    def add(self, id, value):
        super().add(id, value, index = -1)
    
    def remove(self):
        top = self.getFirst()
        super().remove(index = 0)
        return top

    
    
