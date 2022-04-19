from Node import Node
from List import List
from Queue import Queue

lista = Queue()
lista.add(3, 'd')
lista.add(0, 'a')
lista.add(1, 'b')
lista.add(2, 'c')
lista.remove()
print(lista.getListItens())
lista.remove()
print(lista.getListItens())
lista.remove()
print(lista.getListItens())
quit()
print(lista.getListItens())
print(lista.getNode(0))
