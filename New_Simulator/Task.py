from Instance import Instance
from Event import Event

class Task(object):
    def __init__(self, id):
        self.id = id

    def generateEvents(self, until):
        """
        Compute the events for a simulation until the given time.
        """
        pass

class PeriodicTask(Task):
    def __init__(self, id, wcet, period):
        Task.__init__(self, id)
        self.priority = 1.0/float(period)
        self.wcet = wcet
        self.period = period

    def generateEvents(self, until):
        events = list()
        i = 0
        while i < until:
            instance = Instance(Instance.HARD, self, i, self.wcet, self.priority)
            event = Event(Event.ARRIVAL, i, instance)
            events.append(event)
            i += self.period

        return events

class AperiodicTask(Task):
    def __init__(self, id, wcet, release, priority):
        Task.__init__(self, id)
        self.release = release
        self.priority = priority
        self.wcet = wcet

    def generateEvents(self, until):
        instance = Instance(Instance.SOFT, self, self.release, self.wcet, self.priority)
        event = Event(Event.ARRIVAL, self.release, instance)
        return [event]
