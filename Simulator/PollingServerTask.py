from Task import Task
from PollingServerInstance import PollingServerInstance
from Event import Event
from EventType import EventType

class PollingServerTask(Task):
    def __init__(self, capacity, period, scheduler):
        Task.__init__(self, "Polling Server")
        self.capacity = capacity
        self.period = period
        self.scheduler = scheduler

    def generateEvents(self, clock, stats, until):
        eventList = list()
        i = 0
        while i < until:
            instance = PollingServerInstance(self)
            event = Event(i, EventType.NEW_HARD, instance)
            eventList.append(event)
            i += self.period
            
        return eventList
