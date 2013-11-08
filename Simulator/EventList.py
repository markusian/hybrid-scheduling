import heapq as hq
from Event import Event
from EventType import EventType
from PriorityQueue import PriorityQueue

class EventList(object):

    def __init__(self):
        self.arrivalList = PriorityQueue()
        self.finishEvent = None

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
        if (self.finishEvent is None) and (self.arrivalList.isEmpty()):
            return None
        elif (self.finishEvent is not None) and (self.arrivalList.isEmpty()):
            event = self.finishEvent
            self.finishEvent = None
            return event
        elif (self.finishEvent is None) or (self.arrivalList.peak().timestamp < self.finishEvent.timestamp):
            return self.arrivalList.pop()
        else:
            event = self.finishEvent
            self.finishEvent = None
            return event

    def insertEvent(self, event):
        """Insert an event in the list"""
        if (event.eventType == EventType.ARRIVAL):
            self.arrivalList.push(event.timestamp,event)
        elif (event.eventType == EventType.FINISHING):
            self.finishEvent = event

    def __str__(self):
        ret = "ARRIVING : "
        for el in self.arrivalList.list:
            ret += str(el[1])
        ret += "\nFINISHING : " + str(self.finishEvent)

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
    


