from EventType import EventType
from Event import Event
from EventList import EventList
from TaskInstance import TaskInstance
from HardTask import HardTask
from PriorityQueue import PriorityQueue
# TODO : Proper import
from Main import *

class Scheduler:
    """The scheduler executes tasks instance in the simulator."""

    def __init__(self):
        self.executingTask = None
        self.waitingTasks = PriorityQueue()
        self.clock = 0
        self.stats = ExportStats()

    def advanceClock(self, time):
        """
        Move the clock forward.

        :param time: Time to advance the clock
        :type time: int
        """

        diff = time - self.clock

        self.clock = time

        if (self.executingTask is not None):
            self.executingTask.remainingTime -= diff

    def reactToEvent(self, event):
        """
        Computes new events lists and perform action on the instance based on
        an event.

        :param event: The event to compute
        :type event: Event
        """

        # Compute the clock
        self.advanceClock(event.timestamp)

        if (event.eventType == EventType.ARRIVAL):
            # Add the task to waiting tasks
            self.waitingTasks.push(event.taskInstance.task.priority, event.taskInstance)

        if (event.eventType == EventType.FINISHING):
            # Add statistics
            self.stats.addToList(event.taskInstance, self.clock)
            # Remove the task from waiting tasks
            # Since it is the running task it is the most priority
            task = self.waitingTasks.pop()
            task.finishingTime = self.clock

        # Call the scheduler
        return self.schedule()

    def schedule(self):
        """
        Execute the most priority task on the scheduler.

        :return: The finishing event for the new task, None if there is no
        task to run
        :rtype: Event
        """

        if (not self.waitingTasks.isEmpty()):
            task = self.waitingTasks.peak()
            self.executingTask = task

            if (task.startTime == None):
                task.startTime = self.clock

            finishingTime = self.clock + task.remainingTime

            return Event(finishingTime, task, EventType.FINISHING)
        else:
            return None

    def printRunningTasks(self):
        ret = "WAITING : "
        for el in self.waitingTasks.list:
            ret += str(el[1]) + " "
        return ret

if __name__ == "__main__":
    scheduler = Scheduler()

    t1 = HardTask(1, 0, 1, 5)
    t2 = HardTask(2, 0, 2, 10)
    t3 = HardTask(3, 1, 5, 5)
    
    htasks = InputParser()
    htasks.getTasksFromFile("test.csv")
    # print htasks.getHardTaskList()[2].idx

    list = EventList()
    populateEventList(htasks.getHardTaskList(), list)
    # populateEventList([t1, t2, t3], list)

    event = list.getNextEvent()
    i = 0
    while (event is not None):
        #print "CURRENT :" + str(event)
        #print list
        #print scheduler.printRunningTasks()
        i = i + 1
        newEvent = scheduler.reactToEvent(event)
        if (newEvent is not None):
            list.insertEvent(newEvent)
        event = list.getNextEvent()
        #print
    print "Loops: " + str(i)
    scheduler.stats.writeToFile("statistics.csv")
    