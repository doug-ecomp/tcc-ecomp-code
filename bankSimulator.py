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

def debug(text):
    if(LOG_LEVEL in ('DEBUG')): print(text)

def info(text):
    if(LOG_LEVEL in ('DEBUG', 'INFO')): print(text)

#constants
CLIENT_BLOCKS = [10, 15, 25, 15, 10, 5, 15, 15, 10, 5, 10, 25, 30, 10, 5]
MAX_CAPACITY = 60
COUNTER_AMOUNT = 5
MULTIPLE_QUEUE = True
CLIENT_BLOCK_INTERVAL = 10 #Interval between blocks of clients
EXECUTION_AMOUNT = 1
LOG_LEVEL = "DEBUG"



simulatioType = input("""
Select the simulation type:
0 - Single Line
1 - Multiple Queues
""")

for x in range(EXECUTION_AMOUNT):
    start_time = time()

    #variables
    timer = 0
    order = 0 #Holds the number of passwords distributed 
    totalClients = 0 #Number of clients currently in the bank
    counterQueue = []
    clientQueue = Queue() #all clients go through this queue before go to a counter

    if simulatioType == '0':
        simulation_type_text = 'Single Line'
        queueLimit = 1
    else:
        simulation_type_text = 'Multiple Queues'
        queueLimit = MAX_CAPACITY // COUNTER_AMOUNT

    #create counters' queues
    for n in range(COUNTER_AMOUNT):
        counterQueue.append(Queue())

    for iBlock, blockSize in enumerate(CLIENT_BLOCKS):
        #fill client queue
        debug(f"New block of clients: {iBlock}")
        for n in range(order, order+blockSize):
            #each client has a service time
            clientQueue.add(n, randint(1,10))
        
        order += blockSize
        totalClients += blockSize

        debug(f'Awating List: {clientQueue.getListItens()}')
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

            timer += 1
            info(f'Timer: {timer} | Total Clients: {totalClients}')
            debug(f'Awating List Size: {clientQueue.getSize()}')
            debug(f'Total Clients: {totalClients}')
            #decrement the service time for the clients at the counter and remove those who the service time has been compĺeted
            for idx, counter in enumerate(counterQueue):
                debug(f"Counter {idx}: {counter.getListItens()}")
                if counter.getSize() > 0:
                    counter.getFirst().setValue(counter.getFirst().getValue()-1)
                    if counter.getFirst().getValue() == 0:
                        counter.remove()
                        totalClients -= 1

            #At multiples of nextBlockTimer, set the flag to get next client block. Do it only when the loop is not already at the last iteration
            if (iBlock + 1)<len(CLIENT_BLOCKS):
                if totalClients == 0: # All current costumers may get served before next group of clients arrives
                    for x in range(CLIENT_BLOCK_INTERVAL - (timer % CLIENT_BLOCK_INTERVAL), 0, -1):
                        debug(f'No clients at the bank. Time remaining to next group\'s arrival: {x}')
                        timer += 1
                        info(f'Timer: {timer} | Total Clients: {totalClients}')

                if timer % CLIENT_BLOCK_INTERVAL == 0: 
                    nextBlock = True

    end_time = time()
    tt_time = end_time - start_time
    print(f'{simulation_type_text} | Time: {round(tt_time, 5)} | Iterations: {timer}')