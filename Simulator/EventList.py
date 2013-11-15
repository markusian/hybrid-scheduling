import heapq as hq
from Event import Event
from EventType import EventType
from PriorityQueue import PriorityQueue

class EventList(object):

    def __init__(self):
        self.arrivalList = PriorityQueue()
        self.interruptEvent = None

#    def getNextEvents(self):
#        """Returns a list containing the next concurrent events"""
#        if len(self.arrivalList) == 0:
#            return []
#        nextTimestamp = self.arrivalList[0][0]
#        nextEvents = [hq.heappop(self.arrivalList)[1]]
#        while (len(self.arrivalList)>0 and self.arrivalList[0][0] == nextTimestamp):
#            nextEvents.append(hq.heappop(self.arrivalList)[1])
#        return nextEvents

    def getNextEvent(self):
        """Returns the next Event (According to time)."""
        # TODO : It works but can find a more elegant way ;)
        if (self.interruptEvent is None) and (self.arrivalList.isEmpty()):
            return None
        elif (self.interruptEvent is not None) and (self.arrivalList.isEmpty()):
            event = self.interruptEvent
            self.interruptEvent = None
            return event
        elif (self.interruptEvent is None) or (self.arrivalList.peak().time < self.interruptEvent.time):
            return self.arrivalList.pop()
        else:
            event = self.interruptEvent
            self.interruptEvent = None
            return event

    def insertEvent(self, event):
        """Insert an event in the list"""
        if (event.eventType == EventType.SOFT_ARRIVAL or event.eventType == EventType.HARD_ARRIVAL):
            self.arrivalList.push(event.time, event)
        elif (event.eventType == EventType.INTERRUPT):
            self.interruptEvent = event

    def __str__(self):
        ret = "ARRIVING : "
        for el in self.arrivalList.list:
            ret += str(el[1])
        ret += "\nFINISHING : " + str(self.interruptEvent)

        return ret

def test_EventList():
    e1 = Event(1,23,'uno')
    e2 = Event(2,34,'due')
    e3 = Event(34,22,'33')
    e4 = Event(22,32,'sadas')
    e5 = Event(14,23,'sdsad')
    e6 = Event(-23,232,'asdsad')
    e3_2 = Event(34,23,'33')
    e3_3 = Event(34,24,'33')
    
    eventList = EventList()

    eventList.insertEvent(e5)
    eventList.insertEvent(e4)
    eventList.insertEvent(e3)
    eventList.insertEvent(e6)    
    eventList.insertEvent(e1)
    eventList.insertEvent(e2)
    eventList.insertEvent(e3_3)
    eventList.insertEvent(e3_2)    


    for i in range(8):
        print eventList.getNextEvents()    
    

if __name__=='__main__':
    
    test_EventList()
    


