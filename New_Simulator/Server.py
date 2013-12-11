from PriorityQueue import PriorityQueue
from Event import Event
import logging
import math
import numpy as np

class Server(object):
    ACTIVE = "ACTIVE" # The server is executing on the simulator
    WAITING = "WAITING" # The server is waiting for its execution
    SUSPENDED = "SUSPENDED" # The server suspends itself (Typically because its capacity dropped to 0)
    IDLE = "IDLE" # No task to execute on the server

    def __init__(self):
        self.setState(Server.IDLE)
        self.waiting = PriorityQueue()
        self.priority = 0

    def advance(self, since, until):
        """
        Advance the server to the given time.
        Update its state.
        """
        if self.state == Server.ACTIVE:
            self.setState(Server.WAITING)

    def activate(self):
        """
        Activate the server, return the instance to execute.
        """
        self.setState(Server.ACTIVE)

        return self.waiting.first()

    def put(self, instance):
        """
        Put an instance on the server.
        """
        self.waiting.put(instance, instance.priority)

        self.setState(Server.WAITING)

    def suspend(self):
        """
        Suspend the server.
        """
        self.setState(Server.SUSPENDED)

    def refill(self):
        """
        Refill the server.
        """
        pass

    def event(self, since):
        """
        Return the next suspend event (eventually None).
        """
        return None

    def generateEvents(self, until):
        """
        Compute the events for a simulation until the given time.
        """
        return []

    def pop(self):
        """
        Return the most priority instance and remove it from the waiting list.
        """
        instance = self.waiting.pop()

        if self.waiting.isEmpty():
            self.setState(Server.IDLE)

        return instance

    def setState(self, state):
        """
        Change server state.
        """
        logging.debug("Change state : " + state)
        self.state = state

class BackgroundServer(Server):
    pass

class PollingServer(Server):
    def __init__(self, capacity, period):
        Server.__init__(self)
        self.period = period
        self.capacity = capacity
        self.current = 0
        self.priority = 1.0/float(period)

    def generateEvents(self, until):
        events = list()
        i = 0
        while i < until:
            event = Event(Event.REFILL, i)
            events.append(event)
            i += self.period

        return events

    def advance(self, since, until):
        if self.state == Server.ACTIVE:
            self.current -= until - since
            self.setState(Server.WAITING)
        elif self.state == Server.WAITING:
            pass
        else:
            self.current = 0
            self.setState(Server.IDLE)

    def put(self, instance):
        Server.put(self, instance)

        if self.current <= 0:
            self.setState(Server.SUSPENDED)

    def refill(self):
        self.current = self.capacity

        if self.waiting.isEmpty():
            self.setState(Server.IDLE)
        else:
            self.setState(Server.WAITING)

    def event(self, since):
        if self.state == Server.ACTIVE:
            return Event(Event.SUSPEND, since + self.current)
        else:
            return None

    @staticmethod
    def util(up):
        """Returns the maximum polling server utilization factor for the given
        periodic load up"""
        exup = math.exp(up)
        return (2.0/exup)-1

    def ps_util_n(up,n):
        a = 0.5*(1+up/n)**n
        return 1./a -1

    def ps_basic(up):
        return math.log(2)-up



class DeferrableServer(PollingServer):
    def advance(self, since, until):
        if self.state == Server.ACTIVE:
            self.current -= until - since
            self.setState(Server.WAITING)
        elif self.state == Server.WAITING:
            pass
        else:
            self.setState(Server.IDLE)

    @staticmethod
    def util(up):
        """Returns the maximum deferrable server utilization factor for the given
        periodic load up, version 1"""
        first = DeferrableServer.ds1(up)
        if first > 1./3 and first < 1./2:
            return first
        else:
            return DeferrableServer.ds2(up)
    @staticmethod
    def util2(up):
        """Returns the maximum deferrable server utilization factor for the given
        periodic load up, version 2"""
        exup = math.exp(up)
        return (2-exup)/(2*exup-1)


    @staticmethod
    def ds1(up):
        exup = math.exp(up)
        return 1-exup/2.0

    @staticmethod
    def ds2(up):
        exup = math.exp(up)
        sqrt_d = sqrt_delta(exup)
        a_men = (1-2.0*exup)
        x1 = (a_men + sqrt_d)/2.0
        x2 = (a_men - sqrt_d)/2.0
        return max([x1,x2])

def sqrt_delta(up):
    return math.sqrt(4*up*up-8*up+9)

