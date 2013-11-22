from Instance import Instance
import logging 

class BackgroundServerInstance(Instance):
    """An instance of the background server."""

    def __init__(self, scheduler):
        """
        Init the instance.

        :param softScheduler: The scheduler attached to this server.
        :type softScheduler: scheduler
        """

        self.scheduler = scheduler

    def execute(self, time):
        self.scheduler.execute(time)

    def nextInterrupt(self):
        if (self.scheduler.active is not None):
            return self.scheduler.active.nextInterrupt()
        else:
            return None

    def started(self):
        return True

    def finised(self):
        return False

    def priority(self):
        return 0
