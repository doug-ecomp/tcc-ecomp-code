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

def amountInLine(counterQueue):
    clientsInLine = 0
    for counter in counterQueue:
        clientsInLine += counter.getSize()

    return clientsInLine


start_time = time()
#constants
totalClients = [10, 15, 25, 50, 400]
maxCapacity = 40
counterAmount = 5
multipleQueue = True

#variables

timer = 0
nextBlockTimer = 10
clientToBeServed = 0
order = 0
counterQueue = []
clientQueue = Queue()
excessQueue = Queue()
queueLimit = 1 if not multipleQueue else maxCapacity // counterAmount
#create queues
for n in range(counterAmount):
    counterQueue.append(Queue())

for iBlock, blockSize in enumerate(totalClients):
    #fill client queue
    print(f"New block of clients: {iBlock}")
    for n in range(order, order+blockSize):
        if clientQueue.getSize() + amountInLine(counterQueue) < maxCapacity:
            clientQueue.add(n, randint(1,10))
        else:
            excessQueue.add(n, randint(1,10))
    
    order += blockSize

    print(f'Awating List: {clientQueue.getListItens()}')
    print(f'Excess List: {excessQueue.getListItens()}')
    clientsBeingServed = 1
    nextBlock = False    
    while(clientsBeingServed > 0 and not nextBlock):
        if clientQueue.getSize()>0 or excessQueue.getSize() > 0:
            idx = getCounter(counterQueue, queueLimit)
            while idx is not None:
                auxCounter = clientQueue if clientQueue.getSize()>0 else excessQueue
                counterQueue[idx].add(auxCounter.getFirst().getId(), auxCounter.getFirst().getValue())
                auxCounter.remove()
                if (amountInLine(counterQueue) + clientQueue.getSize()) < maxCapacity:
                    clientQueue.add(excessQueue.getFirst().getId(), excessQueue.getFirst().getValue())
                    excessQueue.remove()
                idx = getCounter(counterQueue, queueLimit)

        sleep(0.01)
        timer += 1
        print(f'-----------Timer:{timer}-----------')
        print(f'Awating List: {clientQueue.getSize()}')
        print(f'Excess List: {excessQueue.getSize()}')
        print(f'Being Served: {amountInLine(counterQueue)}')
        for idx, counter in enumerate(counterQueue):
            if counter.getSize() > 0:
                counter.getFirst().setValue(counter.getFirst().getValue()-1)
                if counter.getFirst().getValue() == 0:
                    counter.remove()
            print(f"Counter {idx}: {counter.getListItens()}")
        
        if (iBlock + 1)<len(totalClients):
            if timer % nextBlockTimer == 0: 
                nextBlock = True
        else:
            clientsBeingServed = amountInLine(counterQueue)

end_time = time()
tt_time = end_time - start_time
print(tt_time)