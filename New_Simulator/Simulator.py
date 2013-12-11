from Instance import Instance
from Server import Server, BackgroundServer, PollingServer, DeferrableServer
from Event import Event, EventList
from Task import PeriodicTask, AperiodicTask
from PriorityQueue import PriorityQueue
from ReadConfig import ReadConfig
from Statistics import Statistics
from datetime import date
import logging
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#logging.basicConfig(level = logging.DEBUG)

class Simulator(object):
    def __init__(self) :
        self.waiting = PriorityQueue()
        self.server = Server()
        self.active = None
        self.events = EventList()
        self.clock = 0
        self.tasks = []
        self.statistics = Statistics()
        self.until = 0

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

        # Compute statistics
        event.instance.statistics()
        self.statistics.put(event.instance)

    def reactSuspend(self, event):
        # Suspend the server
        self.server.suspend()

    def reactRefill(self, event):
        # Refill the server
        self.server.refill(self.clock)

    def read(self, filename):
        """
        Load a configuration from a file.
        """
        r = ReadConfig()
        r.read(filename)

        self.server = r.server
        self.tasks = r.tasks

    def init(self, until = -1):
        """
        Initialize the server to run until the given time.
        If -1 is given, run until the LCM of periodic tasks.
        """

        logging.debug("Initialization until " + str(until))
        
        if (until == -1):
            until = PeriodicTask.lcm(self.tasks)

        for t in self.tasks:
            logging.debug("Generating events for " + str(t.id))
            for e in t.generateEvents(until):
                self.events.put(e)

        for e in self.server.generateEvents(until):
            self.events.put(e)

        self.until = until

    def run(self):
        """
        Execute the simulation.
        """
        next = self.events.next()
        while next is not None and next.time < self.until:
            self.advance(next.time)

            logging.debug(str(self.clock) + ": Event " + next.type + " " 
                          + (next.instance.task.id 
                              if next.instance is not None else ""))

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

    def write(self, filename, col=6):
        """
        Write the results to a file.
        """
        file = open(filename, "wb")
        
        # Write some comments on the head of the file
        width = 9*(col + 1)

        file.write("Simulator results")

        today = date.today()
        file.write(("Date : " + 
                    str(today.day) + "/" + 
                    str(today.month) + "/" + 
                    str(today.year) + "\n").rjust(width - 17))
        file.write(("Runtime : " + str(self.clock) + "\n").rjust(width))

        file.write("Server : " + 
                    str(self.server.__class__.__name__))
        file.write("\n")

        if isinstance(self.server, PollingServer):
            file.write("Capacity : " + 
                        str(self.server.capacity) +
                        " Period : " + 
                        str(self.server.period) + "\n")

        file.write("\n")

        self.statistics.write(file, col=col)

    def render(self, filename):
        """
        Render the graph of execution.
        """

        plt.subplot('211')
        y_pos = np.arange(len(self.tasks))

        for i in y_pos :
            t = self.tasks[i]
            for instance in t.instances:
                for time in instance.executed:
                    plt.barh(i-0.5, time[1] - time[0], left = time[0], height=1.0)
                plt.plot(instance.arrival, i, "r+")

        plt.yticks(y_pos, [task.id for task in self.tasks])

        plt.subplot('212')
        plt.plot(self.server.stats["times"], self.server.stats["capacities"])
        plt.savefig(filename)
        
if __name__ == '__main__':
    s = Simulator()
    s.read("test.json")
    s.init()
    s.run()
    s.write("results.csv")
