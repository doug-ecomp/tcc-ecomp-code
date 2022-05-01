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
            if (queue is None) or (queue is not None and counter.getSize() < counterQueue[queue].getSize()):
                queue = idx
    
    return queue

def amountInLine(counterQueue):
    clientsInLine = 0
    for counter in counterQueue:
        clientsInLine += counter.getSize()

    return clientsInLine


start_time = time()

#constants
clientBlocks = [10, 15, 25, 50, 400]
maxCapacity = 40
counterAmount = 5
multipleQueue = True

#variables
timer = 0
nextBlockTimer = 10 #Interval between blocks f clients
order = 0 #Holds the number of passwords distributed 
totalClients = 0 #Number of clients currently in the bank
counterQueue = []
clientQueue = Queue() #all clients go through this queue before go to a counter
queueLimit = 1 if not multipleQueue else maxCapacity // counterAmount

#create counters' queues
for n in range(counterAmount):
    counterQueue.append(Queue())

for iBlock, blockSize in enumerate(clientBlocks):
    #fill client queue
    print(f"New block of clients: {iBlock}")
    for n in range(order, order+blockSize):
        #each client has a service time
        clientQueue.add(n, randint(1,10))
    
    order += blockSize
    totalClients += blockSize

    print(f'Awating List: {clientQueue.getListItens()}')
    nextBlock = False #aux variable to indicate when accept new block of clients   
    while(totalClients > 0 and not nextBlock):
        #get a counter queue with spot available
        idx = getCounter(counterQueue, queueLimit) 
        while idx is not None and clientQueue.getSize()>0:
            #add client to counter's queue and remove from client's queue
            counterQueue[idx].add(clientQueue.getFirst().getId(), clientQueue.getFirst().getValue())
            clientQueue.remove()
            idx = getCounter(counterQueue, queueLimit)

        sleep(0.01)
        timer += 1
        print(f'-----------Timer:{timer}-----------')
        print(f'Awating List: {clientQueue.getSize()}')
        print(f'Total Clients: {totalClients}')
        #decrement the service time for the clients at the counter and remove those who the service time has been compĺeted
        for idx, counter in enumerate(counterQueue):
            print(f"Counter {idx}: {counter.getListItens()}")
            if counter.getSize() > 0:
                counter.getFirst().setValue(counter.getFirst().getValue()-1)
                if counter.getFirst().getValue() == 0:
                    counter.remove()
                    totalClients -= 1
        

        #At multiples of nextBlockTimer, set the flag to get next client block. Do it only when the loop is not already at the last iteration
        if (iBlock + 1)<len(clientBlocks):
            if timer % nextBlockTimer == 0: 
                nextBlock = True

end_time = time()
tt_time = end_time - start_time
print(tt_time)