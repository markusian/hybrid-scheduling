#Different task types
from HardTask import HardTask
from SoftTask import SoftTask
from Task import Task
from TaskInstance import TaskInstance
#Needed for csv files
import csv

class StatsList(object):
    def __init__(self, task, clock):
        self.task = task
        self.clock = clock
        
    def getTask(self):
        return self.task
    
    def getClock(self):
        return self.clock

class ExportStats(object):

    def __init__(self):
        self.taskList = []
    
    def addToList(self, task, clock):
        self.taskList.append(StatsList(task, str(clock)))
        
    def writeToFile(self):
        with open("statistics.csv", "wb") as fh:
            writer = csv.writer(fh)
            writer.writerow(["Arrival Time", "Finishing Time", "Period", "Time To Deadline"])
            for i in range(0, len(self.taskList)):
                arrivalTime = self.taskList[i].getTask().arrivalTime
                period = self.taskList[i].getTask().task.period
                finishingTime = self.taskList[i].getClock()
                timeToDeadline = str(int(period) + int(arrivalTime) - int(finishingTime))
                writer.writerow([arrivalTime, finishingTime, period, timeToDeadline])
