from Instance import Instance
from Event import Event
from numpy import random
import Gaussians
import logging

LIMIT_ARRIVAL_TIME = 6

class Task(object):
    def __init__(self, id):
        self.id = id
        self.instances = list()

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
        self.first = True

    def getNextExecutionTime(self):
        low_lim = self.wcet*0.7
        return random.random_sample()*(self.wcet-low_lim) + low_lim

    def nextArrival(self, time):
        """
        Compute the next arrival event, based on the given time.
        Return the event
        """
        if self.first:
            arrival = random.uniform(0, LIMIT_ARRIVAL_TIME)
            self.first = False
        else:
            arrival = time + self.period
        computation = self.getNextExecutionTime()
        instance = Instance(Instance.HARD, self, arrival, computation, self.priority)
        event = Event(Event.ARRIVAL, arrival, instance)
        return event

    @staticmethod
    def lcm(tasks):
        """
        Compute LCM of period for a list of tasks (ignore aperiodic tasks)
        """
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a

        def lcm(a, b):
            return a * b // gcd(a, b)

        res = 1
        for t in tasks:
            if isinstance(t, PeriodicTask):
                res = lcm(res, t.period)

        return res

class AperiodicTask(Task):
    def __init__(self, id, computation, release):
        """
        Init the task.
        release : The mean interarrival time
        computation : The mean computation time
        """
        Task.__init__(self, id)
        self.computation = computation
        self.release = release
        self.priority = 0
        self.last_arrival = 0

    def nextArrival(self, time):
        """
        Compute the next arrival event
        Return the event
        """
        arrival = time + random.poisson(self.release)
        computation = random.exponential(self.computation)
        instance = Instance(Instance.SOFT, self, arrival, computation, self.priority)
        event = Event(Event.ARRIVAL, arrival, instance)
        return event
