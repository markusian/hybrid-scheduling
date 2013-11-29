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
        if self.type == Instance.HARD:
            self.deadline = arrival + task.period
        else:
            self.deadline = float('inf')
        
    def advance(self, since, until):
        """
        Execute the instance to the given time.
        """
        logging.info(str(since) + ": Execute " + self.task.id + 
                     " for " + str(until - since))
        # Compute statistics
        if self.interrupt == self.arrival:
            self.start = since
        elif self.interrupt != since:
            self.idle += until - since

        self.remaining -= until - since
        self.interrupt = until

    def event(self, since):
        """
        Return a finishing event for the instance.
        """
        return Event(Event.FINISH, since + self.remaining, self)

    def statistics(self):
        """
        At the end of the execution, compute statistics.
        """
        self.finish = self.interrupt
        self.time_to_deadline = self.deadline - self.finish
