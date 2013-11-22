from Instance import Instance
import logging

class TaskInstance(Instance):
    """An instance of a task (sometimes called a job)."""
	
    def __init__(self, arrival, computation, task, clock, stats):
        """
        Init the instance.
        """

        self.arrivalTime = arrival
        self.task = task

        self.computationTime = computation
        self.remainingTime = computation

        self.startTime = None
        self.finishingTime = None

        self.hasStarted = False
        self.clock = clock
        self.stats = stats

    def __str__(self):
        return str(self.task.idx)

    def start(self):
        logging.debug(str(self.clock.currentTime()) + " - "
                   "Started : " + str(self))
        self.startTime = self.clock.currentTime()
        self.hasStarted = True

    def finish(self):
        logging.debug(str(self.clock.currentTime()) + " - "
                   "Finished : " + str(self))
        self.finishingTime = self.clock.currentTime()
        self.stats.addToList(self)

    def execute(self, time):
        logging.debug(str(self.clock.currentTime()) + " - "
                   "Executed : " + str(self) + " "
                   "for " + str(time))
        self.remainingTime -= time
        
    def nextInterrupt(self):
        return self.remainingTime

    def started(self):
        return self.hasStarted

    def finished(self):
        return self.remainingTime <= 0
