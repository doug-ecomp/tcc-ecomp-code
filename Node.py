
class Node:
    def __init__(self, id, value, next=None, prev=None, left=None, right=None) -> None:
        self.id = id
        self.value = value
        self.next = next
        self.prev = prev
        self.left = left
        self.right = right

    def getId(self):
        return self.id

    def getValue(self):
        return self.value

    def getNext(self):
        return self.next

    def getPrev(self):
        return self.prev

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setNext(self, next):
        self.next = next

    def setPrev(self, prev):
        self.prev = prev

    def setLeft(self, left):
        self.left = left

    def setRight(self, right):
        self.right = right

