from Instance import Instance
from Event import Event
from numpy import random
import Gaussians

LIMIT_ARRIVAL_TIME = 6

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

    def getNextExecutionTime(self):
#        low_lim = self.wcet*0.7
#        return random.random_sample()*(self.wcet-low_lim) + low_lim
        return self.wcet

    def generateEvents(self, until):
        events = list()
        i = random.uniform(0, LIMIT_ARRIVAL_TIME)
        while i < until:
            # Compute the computation time
            computation = self.getNextExecutionTime()
            while computation < 0.0 or computation > self.wcet :
                print "ERROR : " + str(computation)
                print "WCET: " + str(self.wcet)
                computation = self.getNextExecutionTime()
            instance = Instance(Instance.HARD, self, i, computation, self.priority)
            event = Event(Event.ARRIVAL, i, instance)
            events.append(event)
            i += self.period

        return events

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

    def generateEvents(self, until):
        events = list()
        i = random.poisson(self.release)
        while i < until:
            computation = random.exponential(self.computation)
            instance = Instance(Instance.SOFT, self, i, computation, self.priority)
            event = Event(Event.ARRIVAL, i, instance)
            events.append(event)
            i += random.poisson(self.release)
        return events
