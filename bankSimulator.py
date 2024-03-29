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

simulatioType = input("""
Select the simulation type:
0 - Single Line
1 - Multiple Queues
""")
if simulatioType == '0':
    simulation_type_text = 'Single Line'
    queueLimit = 1
else:
    simulation_type_text = 'Multiple Queues'
    queueLimit = maxCapacity // counterAmount

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
        while clientQueue.getSize()>0:
            idx = getCounter(counterQueue, queueLimit)
            if idx is None:
                break # there is no spot available in any of the queues
            #add client to counter's queue and remove from client's queue
            counterQueue[idx].add(clientQueue.getFirst().getId(), clientQueue.getFirst().getValue())
            clientQueue.remove()

        sleep(0.01)
        timer += 1
        print(f'-----------Timer:{timer}-----------')
        print(f'Awating List Size: {clientQueue.getSize()}')
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
            if totalClients == 0: # All current costumers may get served before next group of clients arrives
                for x in range(nextBlockTimer - (timer % nextBlockTimer), 0, -1):
                    print(f'No clients at the bank. Time remaining to next group\'s arrival: {x}')
                    sleep(0.01)
                    timer += 1
                    print(f'-----------Timer:{timer}-----------')

            if timer % nextBlockTimer == 0: 
                nextBlock = True

end_time = time()
tt_time = end_time - start_time
print(f'The simulation time with {simulation_type_text} was {tt_time} ({timer} iterations)')