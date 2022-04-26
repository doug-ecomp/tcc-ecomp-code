'''
o novo cliente se direciona para a fila com menor quantidade de pessoas,
e não com o menor tempo de espera estimado, já que ele não tem domínio dessa informação
'''

from Queue import Queue
from random import randint
from time import time
from time import sleep

def getCounter(counterQueue, queueLimit):
    queue = None
    for idx, counter in enumerate(counterQueue):
        if counter.getSize() == 0:
            return idx
        elif counter.getSize() < queueLimit:
            if (queue is None) or (queue is not None and counter.getFirst().getValue() < counterQueue[queue].getFirst().getValue()):
                queue = idx
    
    return queue


start_time = time()
#constants
totalClients = [10, 25, 50, 100, 500]
maxCapacity = 40
counterAmount = 5

#variables
counterQueue = []
clientQueue = Queue()
excessQueue = Queue()

#fill client queue
for n in range (min(totalClients[0], maxCapacity)):
    clientQueue.add(n, randint(1,10))

if (totalClients[0] - maxCapacity) > 0:
    for n in range (totalClients[0] - maxCapacity):
        excessQueue.add(n, randint(1,10))


print(clientQueue.getListItens())
print(excessQueue.getListItens())

#create queues
for n in range(counterAmount):
    counterQueue.append(Queue())
    
while(clientQueue.getSize()>0):
    idx = getCounter(counterQueue, 1)
    while idx is not None:
        counterQueue[idx].add(clientQueue.getFirst().getId(), clientQueue.getFirst().getValue())
        clientQueue.remove()
        idx = getCounter(counterQueue, 1)

    sleep(1)

    for counter in counterQueue:
        if counter.getSize() > 0:
            counter.getFirst().setValue(counter.getFirst().getValue()-1)
            if counter.getFirst().getValue() == 0:
                counter.remove()

end_time = time()
tt_time = end_time - start_time
print(tt_time)