from Scheduler import Scheduler
from InputParser import InputParser
from EventList import EventList
from Clock import Clock
from PeriodicTask import PeriodicTask
from AperiodicTask import AperiodicTask
from TaskInstance import TaskInstance
from Event import Event
from EventType import EventType
from BackgroundServerTask import BackgroundServerTask
from BackgroundServerInstance import BackgroundServerInstance
from PollingServerTask import PollingServerTask
from PollingServerInstance import PollingServerInstance
from ExportStats import ExportStats
import logging
logging.basicConfig(level=logging.INFO)

class Simulator(object):
    """The main simulator."""
    def __init__(self):
        """
        Init the simulator.

        :param eList: A list of events
        :type eList: EventList
        """
        def rmPriority(instance):
            if (isinstance(instance, BackgroundServerInstance)):
                return 0

            if (isinstance(instance, PollingServerInstance)):
                return 1.0/float(instance.server.period)
            
            return 1.0/float(instance.task.period)

        def fixedPriority(instance):
            return instance.task.priority

        self.hardScheduler = Scheduler(rmPriority)
        self.softScheduler = Scheduler(fixedPriority)
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
            for event in task.generateEvents(self.clock, self.stats, 50):
                self.eventList.insertEvent(event)

if __name__ == "__main__":
    tasks = InputParser()
    tasks.getTasksFromFile("polling_test.csv")

    s = Simulator()
    tasks.addTaskToList(PollingServerTask(2, 5, s.softScheduler))
    s.populateEventList(tasks.getTaskList())
    s.execute()

    s.stats.writeToFile("results.csv")
