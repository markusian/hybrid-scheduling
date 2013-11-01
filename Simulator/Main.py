from EventList import EventList
from Event import Event
from Scheduler import Scheduler
from TaskList import TaskList
from HardTask import HardTask
#from Input import *
from EventType import EventType

"""
NOTE:

the tasks (even the periodic one) should not arrive all at time 0

to avoid this we could have a randomly chosen "offset" for all of them

with this offset chosen randomly, for instance, between 0 and the period of
the taks

"""

def fakeTasks():
    t1 = HardTask(1,1,2,5)
    t2 = HardTask(2,0.5,3,9)
    
    return [t1,t2]
    
    
    
    


def populateEventList(taskList,eventList):
    for task in taskList:
        event = Event(task.firstArrivalTime,task,EventType.ARRIVAL)
        eventList.insertEvent(event)
    pass


if __name__=='__main__':
    
    #initialization phase
    eventList = EventList()
    
    
    
    # take the list of tasks from the input parser
    
    tasks = fakeTasks()
    

    # put the tasks in the tasklist
    
    populateEventList(tasks,eventList)

    # generate initial events from the tasklist

    #initialize the scheduler

    #put information regarding the tasks in the scheduler    
    
    
    
    pass
    