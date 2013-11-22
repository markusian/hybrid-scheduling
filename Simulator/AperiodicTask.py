from Task import Task
from TaskInstance import TaskInstance
from Event import Event
from EventType import EventType

class AperiodicTask(Task):
    # TODO : Handle interArrivalTime
    def __init__(self, idx, arrivalTime, computationTime, priority):
        """
        Init the task.
        """
        Task.__init__(self, idx)
        self.arrivalTime = arrivalTime
        self.computationTime = computationTime
        self.priority = priority

    def generateEvents(self, clock, until):
         # TODO : Generate more events using interarrivalTime
        instance = TaskInstance(self.arrivalTime, self.computationTime, self, clock)
        event = Event(self.arrivalTime, EventType.NEW_SOFT, instance)
        return [event]
