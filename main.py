from Node import Node
from List import List

lista = List()
lista.addNode(3, 'd', 0)
lista.addNode(0, 'a', 0)
lista.addNode(1, 'b', 1)
lista.addNode(2, 'c', -1)
print(lista.getListItens())
lista.removeNode(-1)
print(lista.getListItens())
print(lista.getNode(0))
