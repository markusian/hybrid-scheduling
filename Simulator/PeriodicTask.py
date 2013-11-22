from Task import Task
from TaskInstance import TaskInstance
from Event import Event
from EventType import EventType

class PeriodicTask(Task):
    """Describe a hard periodic task in the simulator."""

    def __init__(self, idx, wcet, period, arrivalTime):
        """
        Init the task.
        """
        priority = 1.0/float(period)
        Task.__init__(self, idx)
        self.wcet = wcet
        self.arrivalTime = arrivalTime
        self.period = period

    def generateEvents(self, clock, until):
        eventList = list()
        i = self.arrivalTime
        while i < until:
            instance = TaskInstance(i, self.wcet, self, clock)
            event = Event(i, EventType.NEW_HARD, instance)
            eventList.append(event)
            i += self.period

        return eventList
