from Instance import Instance

class PollingServerInstance(Instance):
    def __init__(self, server):
        self.server = server
        self.capacity = server.capacity

    def execute(self, time):
        self.server.scheduler.execute(time)
        self.capacity -= time

    def nextInterrupt(self):
        if (self.server.scheduler.active is not None):
           return min(self.capacity, self.server.scheduler.active.nextInterrupt())
        else:
            # No pending task, suspends itself
            self.capacity = 0
            return 0

    def started(self):
        return True

    def finished(self):
        return self.capacity <= 0
