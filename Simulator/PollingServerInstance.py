from Instance import Instance

class PollingServerInstance(Instance):
    def __init__(self, scheduler, capacity, period):
        self.scheduler = scheduler
        self.capacity = capacity
        self.period = period

    def execute(self, time):
        self.scheduler.execute(time)
        self.capacity -= time

    def nextInterrupt(self):
        if (self.scheduler.active is not None):
           return min(self.capacity, self.scheduler.active.nextInterrupt())
        else:
            # No pending task, suspends itself
            self.capacity = 0
            return 0

    def started(self):
        return True

    def finished(self):
        return self.capacity <= 0

    def priority(self):
        return 1.0/float(self.period)

