from Instance import Instance
from Server import Server, BackgroundServer, PollingServer, DeferrableServer
from Event import Event, EventList
from Task import PeriodicTask, AperiodicTask
from Queue import PriorityQueue
from ReadConfig import ReadConfig
from datetime import date
import logging
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
#logging.basicConfig(level = logging.DEBUG)

class Simulator(object):
    def __init__(self,
            stats = None,
            render = None) :
        self.waiting = PriorityQueue()
        self.server = Server()
        self.active = None
        self.events = EventList()
        self.clock = 0
        self.tasks = []
        self.until = 0

        # Statistics
        if stats is not None:
            self.stats = True
            self.stats_file = open(stats, "wb")
            self.stats_writer = csv.writer(self.stats_file, delimiter='|', lineterminator='\n')
            self.write_headers()
        else:
            self.stats = False

        # Rendering
        if render is not None:
            self.render = True
            self.render_file = render
            self.render_data = dict()
        else:
            self.render = False

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

        # Compute the next arrival
        self.events.put(event.instance.task.nextArrival(event.time))

    def reactFinish(self, event):
        # Remove the instance from its waiting list
        if event.instance.type == Instance.SOFT:
            self.server.pop()
        elif event.instance.type == Instance.HARD:
            self.waiting.pop()

        # Compute statistics
        if self.stats :
            event.instance.statistics()
            self.write_instance(event.instance)

        # Compute rendering
        if self.render :
            task = event.instance.task
            if not task.id in self.render_data:
                self.render_data[task.id] = dict()
                self.render_data[task.id]["executed"] = list()
                self.render_data[task.id]["arrivals"] = list()

            for t in event.instance.executed:
                self.render_data[task.id]["executed"].append(t)
            self.render_data[task.id]["arrivals"].append(event.instance.arrival)

    def reactSuspend(self, event):
        # Suspend the server
        self.server.suspend()

    def reactRefill(self, event):
        # Refill the server
        self.server.refill()
        self.events.put(self.server.nextRefill(event.time))

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
            self.events.put(t.nextArrival(0));

        self.events.put(self.server.nextRefill(0))

        self.until = until

    def run(self):
        """
        Execute the simulation.
        """
        next = self.events.next()
        while next.time < self.until:
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

        if self.stats:
            self.write_footers()

        if self.render:
            self.rendering()

    def write_headers(self):
        """
        Write the results to a file.
        """
        col = 6

        # Write some comments on the head of the file
        width = 9*(col + 1)

        self.stats_file.write("Simulator results")

        today = date.today()
        self.stats_file.write(("Date : " +
                    str(today.day) + "/" +
                    str(today.month) + "/" +
                    str(today.year) + "\n").rjust(width - 17))
        self.stats_file.write("\n")

        # Write the table headers
        self.stats_writer.writerow(["id"[0:col].center(col),
                         "type"[0:col].center(col),
                         "arrival"[0:col].center(col),
                         "start"[0:col].center(col),
                         "finish"[0:col].center(col),
                         "computation"[0:col].center(col),
                         "idle"[0:col].center(col),
                         "deadline"[0:col].center(col),
                         "TTD"[0:col].center(col)])

    def write_instance(self, instance):
        col = 10
        self.stats_writer.writerow([instance.task.id[0:col].rjust(col),
                         instance.type[0:col].rjust(col),
                         str(instance.arrival)[0:col].rjust(col),
                         str(instance.start)[0:col].rjust(col),
                         str(instance.finish)[0:col].rjust(col),
                         str(instance.computation)[0:col].rjust(col),
                         str(instance.idle)[0:col].rjust(col),
                         str(instance.deadline)[0:col].rjust(col),
                         str(instance.time_to_deadline)[0:col].rjust(col)])

    def write_footers(self):
        col = 6
        width = 9*(col + 1)
        self.stats_file.write(("Runtime : " + str(self.clock) + "\n").rjust(width))

        self.stats_file.write("Server : " +
                    str(self.server.__class__.__name__))
        self.stats_file.write("\n")

        if isinstance(self.server, PollingServer):
            self.stats_file.write("Capacity : " +
                        str(self.server.capacity) +
                        " Period : " +
                        str(self.server.period) + "\n")
        self.stats_file.close()



    def rendering(self):
        """
        Render the graph of execution.
        """

        plt.clf()

        plt.subplot('311')
        y_pos = np.arange(len(self.render_data))

        i = 0
        for key, data in self.render_data.iteritems():
            for time in data["executed"]:
                plt.barh(i-0.5, time[1] - time[0], left = time[0], height=1.0)
            for arrival in data["arrivals"]:
                plt.plot(arrival, i, "r+")
            i += 1

        plt.yticks(y_pos, [key for key in self.render_data])

        #print self.server.stats["ctimes"]

        plt.subplot('312')
        plt.plot(self.server.stats["ctimes"], self.server.stats["cvalues"])

        plt.subplot('313')
        plt.plot(self.server.stats["itimes"], self.server.stats["ivalues"])
        plt.savefig(self.render_file)

if __name__ == '__main__':
    s = Simulator(stats = "results.csv", render = "results.svg")
    s.read("polling.json")
    s.init()
    s.run()
