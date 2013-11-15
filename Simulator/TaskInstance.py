from Instance import Instance

class TaskInstance(Instance):
    """An instance of a task (sometimes called a job)."""
	
    def __init__(self, arrivalTime, task, clock):
        """
        Init the instance.

        :param arrivalTime: Time of arrival of the instance on the system.
        :type arrivalTime: int
        :param clock: A reference to the clock (used for statistics)
        """

        self.arrivalTime = arrivalTime
        self.task = task

        self.computationTime = task.computationTime
        self.remainingTime = task.computationTime

        self.startTime = None
        self.finishingTime = None

        self.hasStarted = False
        self.clock = clock

    def __str__(self):
        return str(self.task.idx)

    def start(self):
        self.startTime = self.clock.currentTime()
        self.hasSstarted = True

    def finish(self):
        # TODO: Compute statistics
        pass

    def execute(self, time):
        self.remainingTime -= time
        
    def nextInterrupt(self):
        return self.remainingTime

    def started(self):
        return self.hasStarted

    def finished(self):
        return self.remainingTime <= 0
