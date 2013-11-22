from Task import Task
from BackgroundServerInstance import BackgroundServerInstance
from Event import Event
from EventType import EventType

class BackgroundServerTask(Task):
    def __init__(self, scheduler):
        Task.__init__(self, "Background Server")
        self.scheduler = scheduler

    def generateEvents(self, clock, until):
        instance = BackgroundServerInstance(self.scheduler)
        event = Event(0, EventType.NEW_HARD, instance)
        return [event]

