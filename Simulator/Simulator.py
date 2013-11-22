from Scheduler import Scheduler
from InputParser import InputParser
from EventList import EventList
from Clock import Clock
from PeriodicTask import PeriodicTask
from AperiodicTask import AperiodicTask
from TaskInstance import TaskInstance
from Event import Event
from EventType import EventType
from BackgroundServerInstance import BackgroundServerInstance
from PollingServerInstance import PollingServerInstance
from ExportStats import ExportStats
import logging
logging.basicConfig(level=logging.DEBUG)

class Simulator(object):
    """The main simulator."""
    def __init__(self):
        """
        Init the simulator.

        :param eList: A list of events
        :type eList: EventList
        """
        self.hardScheduler = Scheduler()
        self.softScheduler = Scheduler()
        self.eventList = EventList()
        self.clock = Clock()
        self.stats = ExportStats()

    def reactToEvent(self, event):
        """
        Computes new events lists and perform action on the instance based on 
        an event.

        :param event: The event to compute
        :type event: Event
        """
        logging.debug(str(self.clock.currentTime()) + " - "
                      "Event : " + str(event))

        # Compute the clock
        time = self.clock.advance(event.time)

        # Advance the hard scheduler
        self.hardScheduler.execute(time)

        # Put the new instance on the scheduler if it is an arrival
        if (event.eventType == EventType.NEW_HARD):
            self.hardScheduler.put(event.instance)
        elif (event.eventType == EventType.NEW_SOFT):
            self.softScheduler.put(event.instance)

        # Call the scheduler
        self.hardScheduler.schedule()
        self.softScheduler.schedule()

        # Compute the next interruption
        if (self.hardScheduler.active is not None):
            nextInterrupt = self.hardScheduler.active.nextInterrupt()

            if (nextInterrupt is not None):
                nextInterrupt += self.clock.currentTime()

                newEvent = Event(nextInterrupt, EventType.INTERRUPT)
                self.eventList.insertEvent(newEvent)

    def execute(self):
        """Main loop of the simulator."""
        event = self.eventList.getNextEvent()
        while (event is not None):
            self.reactToEvent(event)
            event = self.eventList.getNextEvent()

    def populateEventList(self, taskList):
        """ 
        The function initializes a list of events from a task list.
        """
        
        for task in taskList:
            if isinstance(task, PeriodicTask) :
                # Generate the periodic instances
                for i in range(10):
                    instance = TaskInstance(task.arrivalTime + i * task.period, task, self.clock, self.stats)
                    event = Event(task.arrivalTime + i * task.period, EventType.NEW_HARD, instance)
                    self.eventList.insertEvent(event)
            elif isinstance(task, AperiodicTask) :
                # Generate only one instance
                instance = TaskInstance(task.arrivalTime, task, self.clock, self.stats)
                event = Event(task.arrivalTime, EventType.NEW_SOFT, instance)
                self.eventList.insertEvent(event)

    def setBackgroundServer(self):
        """
        Initialize a background server.
        """
        instance = BackgroundServerInstance(self.softScheduler)
        self.hardScheduler.put(instance)

    def setPollingServer(self, capacity, period):
        """
        Initialize a polling server.
        """
        for i in range(10):
            instance = PollingServerInstance(self.softScheduler, capacity, period)
            event = Event(i * period, EventType.NEW_HARD, instance)
            self.eventList.insertEvent(event)


if __name__ == "__main__":
    htasks = InputParser()
    htasks.getTasksFromFile("polling_test.csv")

    s = Simulator()
    s.populateEventList(htasks.getTaskList())
    s.setPollingServer(2, 5)
    s.execute()

    s.stats.writeToFile("results.csv")
