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
        self.idle = []
        self.interrupt = arrival
        self.priority = priority
        
    def advance(self, since, to):
        """
        Execute the instance to the given time.
        """
        logging.info(str(since) + ": Execute " + self.task.id + 
                     " for " + str(to - since))
        # Compute statistics
        if self.interrupt == self.arrival:
            self.start = since
        elif self.interrupt != since:
            self.idle.append((self.interrupt, since))

        self.remaining -= to - since
        self.interrupt = to

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

        if self.type == Instance.HARD:
            self.time_to_deadline = self.task.period + \
                                    self.arrival - self.finish
