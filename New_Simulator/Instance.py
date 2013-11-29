from Event import Event
import logging

class Instance(object):
    SOFT = "SOFT"
    HARD = "HARD"

    def __init__(self, type, task, arrival, computation, priority):
        self.type = type
        self.task = task
        self.arrival = arrival
        self.computation = computation
        self.remaining = computation
        self.idle = 0
        self.interrupt = arrival
        self.priority = priority
        
    def advance(self, since, to):
        """
        Execute the instance to the given time.
        """
        logging.info(str(since) + ": Execute " + self.task.id + " for " + str(to - since))
        # Compute statistics
        self.idle += since - self.interrupt

        self.remaining -= to - since
        self.interrupt = to

    def event(self, since):
        """
        Return a finishing event for the instance.
        """
        return Event(Event.FINISH, since + self.remaining, self)
