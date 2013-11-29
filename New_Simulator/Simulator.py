from Instance import Instance
from Server import Server, BackgroundServer, PollingServer, DeferrableServer
from Event import Event, EventList
from Task import PeriodicTask, AperiodicTask
from PriorityQueue import PriorityQueue
import logging
logging.basicConfig(level = logging.DEBUG)

class Simulator(object):
    def __init__(self) :
        self.waiting = PriorityQueue()
        self.server = DeferrableServer(2, 5)
        self.active = None
        self.events = EventList()
        self.clock = 0
        self.tasks = []

    def update(self):
        """
        Update simulator state after any event.
        """
        # Which instance to execute ?
        self.selectInstance()

        # If there is no instance, nothing to do
        if self.active is None:
            return
        else:
            # Compute finish event
            self.events.put(self.active.event(self.clock))

            # Compute server event
            self.events.put(self.server.event(self.clock))

    def advance(self, time):
        """
        Advance the simulator to the given time.
        """
        if self.active is not None:
            self.active.advance(self.clock, time)
            
        self.server.advance(self.clock, time)

        self.clock = time

    def selectInstance(self):
        """
        Select (set the variables) the instance to execute on the simulator
        according to the state of various entities.
        """
        if self.server.state != Server.WAITING:
            if self.waiting.isEmpty():
                self.active = None
            else:
                self.active = self.waiting.first()
        elif self.waiting.isEmpty():
            self.active = self.server.activate()
        else:
            if self.waiting.first().priority > self.server.priority:
                self.active = self.waiting.first()
            else:
                self.active = self.server.activate()

    def reactArrival(self, event):
        # Put the new instance on its waiting list
        if event.instance.type == Instance.SOFT:
            self.server.put(event.instance)
        elif event.instance.type == Instance.HARD:
            self.waiting.put(event.instance, event.instance.priority)

    def reactFinish(self, event):
        # Remove the instance from its waiting list
        if event.instance.type == Instance.SOFT:
            self.server.pop()
        elif event.instance.type == Instance.HARD:
            self.waiting.pop()

        # TODO: Compute statistics

    def reactSuspend(self, event):
        # Suspend the server
        self.server.suspend()

    def reactRefill(self, event):
        # Refill the server
        self.server.refill()

    def init(self, until):
        """
        Initialize the server to run until the given time.
        """
        for t in self.tasks:
            for e in t.generateEvents(until):
                self.events.put(e)

        for e in self.server.generateEvents(until):
            self.events.put(e)

    def run(self):
        next = self.events.next()
        while next is not None:
            self.advance(next.time)

            logging.debug(str(self.clock) + ": Event " + next.type + " " + (next.instance.task.id if next.instance is not None else ""))

            if next.type == Event.ARRIVAL:
                self.reactArrival(next)
            elif next.type == Event.FINISH:
                self.reactFinish(next)
            elif next.type == Event.SUSPEND:
                self.reactSuspend(next)
            elif next.type == Event.REFILL:
                self.reactRefill(next)

            self.update()
            next = self.events.next()

if __name__ == '__main__':
    s = Simulator()
    
    t1 = PeriodicTask('H1', 1, 4)
    t2 = PeriodicTask('H2', 2, 6)

    s1 = AperiodicTask('S1', 2, 2, 1)
    s2 = AperiodicTask('S2', 1, 8, 1)
    s3 = AperiodicTask('S3', 2, 12, 1)
    s4 = AperiodicTask('S4', 1, 19, 1)

    s.tasks = [t1, t2, s1, s2, s3, s4]

    s.init(24)

    s.run()
