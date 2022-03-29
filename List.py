from Node import Node

class List:
    def __init__(self) -> None:
        self.size = 0
        self.first = None
        self.last = None


    def getsize (self):
        return self.size

    def getfirst (self):
        return self.first

    def getlast (self):
        return self.last
    
    def addNode(self, id, value, index = -1):
        node = Node(id, value)
        if self.size == 0: #lista vazia
            self.first = node
            self.last = self.first
        elif (index == -1) or (index>=self.size):
            self.last.setNext(node)
            self.last = node
        elif index == 0:
            node.setNext(self.first)
            self.first = node
        else:
            aux = 0
            currentNode = self.first
            while(aux<index):
                aux += 1
                prevNode = currentNode
                currentNode = currentNode.getNext()
            prevNode.setNext(node)
            node.setNext(currentNode)
                    
        self.size += 1

    def removeNode(self, index = -1):
        if self.size == 0: return
        elif self.size == 1:
            self.fitst = None
            self.last = None
        elif index == 0:
            self.first = self.first.getNext()
        else:
            if index == -1:
                index = self.size - 1
            aux = 0
            currentNode = self.first
            while(aux<index):
                aux += 1
                prevNode = currentNode
                currentNode = currentNode.getNext()
            prevNode.setNext(currentNode.getNext())
            if prevNode.getNext() is None:
                self.last = prevNode
            
        self.size -= 1

    def getNode(self, index = -1):
        if self.size == 0: return 'List is empty'
        elif (index == -1) or (index >= self.size - 1): return [self.size - 1, self.last.getId(), self.last.getValue()]
        else:
            aux = 0
            currentNode = self.first
            while(aux<index):
                aux += 1
                prevNode = currentNode
                currentNode = currentNode.getNext()
            return [aux, currentNode.getId(), currentNode.getValue()]
    
    def getListItens(self):
        if self.size == 0: return 'List is empty'
        else:
            node = self.first
            list_itens = []
            while(node is not None):
                list_itens.append((node.getId(), node.getValue()))
                node = node.getNext()
            return list_itens

    