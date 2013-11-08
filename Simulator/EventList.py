import heapq as hq
from Event import Event


class EventList(object):
    
    def __init__(self):
        self.arrivalList = []
		
	def getNextEvent(self):
		if self.arrivalList[0].timestamp > self.finishEvent.timestamp:
			return hq.heappop(self.list)[1]
		else
			event = self.finishEvent
			self.finishEvent = None
			return event
    

    def getNextEvents(self):
        """Returns a list containing the next concurrent events"""
        if len(self.list) == 0:
            return []
        nextTimestamp = self.list[0][0]
        nextEvents = [hq.heappop(self.list)[1]]
        while (len(self.list)>0 and self.list[0][0] == nextTimestamp):
            nextEvents.append(hq.heappop(self.list)[1])
        return nextEvents
        
    
    def insertEvent(self,event):
        """Insert an event in the list"""
		if (event.type == EventType.ARRIVAL)
			hq.heappush(self.list,(event.timestamp,event))
		else
			self.finishEvent = event
        


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
    


