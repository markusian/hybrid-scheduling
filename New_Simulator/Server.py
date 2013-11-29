from PriorityQueue import PriorityQueue
from Event import Event
import logging

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

class DeferrableServer(PollingServer):
    def advance(self, since, until):
        if self.state == Server.ACTIVE:
            self.current -= until - since
            self.setState(Server.WAITING)
        elif self.state == Server.WAITING:
            pass
        else:
            self.setState(Server.IDLE)
