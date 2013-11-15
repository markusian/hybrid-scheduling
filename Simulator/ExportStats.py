#Different task types
from HardTask import HardTask
from SoftTask import SoftTask
from Task import Task
from TaskInstance import TaskInstance
#Needed for csv files
import csv

#Container for include tasks and clock
class StatsList(object):
    def __init__(self, task, clock):
        self.task = task
        self.clock = clock
        
    def getTask(self):
        return self.task
    
    def getClock(self):
        return self.clock

        
#Exporter
class ExportStats(object):

    def __init__(self):
        self.taskList = []
    
    #Add info to statistics list
    def addToList(self, task, clock):
        self.taskList.append(StatsList(task, str(clock)))
    
    #Actual Filewriter
    def writeToFile(self):
        with open("statistics.csv", "wb") as fh:
            writer = csv.writer(fh)
            #Header for the CSV
            writer.writerow(["Arrival Time", "Finishing Time", "Period", "Time To Deadline", "Task ID"])
            for i in range(0, len(self.taskList)):
                #Define some variables to for easier arglist to writer
                arrivalTime = self.taskList[i].getTask().arrivalTime
                period = self.taskList[i].getTask().task.period
                finishingTime = self.taskList[i].getClock()
                timeToDeadline = str(int(period) + int(arrivalTime) - int(finishingTime))
                taskId = self.taskList[i].getTask().task.idx
                priority = str(self.taskList[i].getTask().task.priority)
                #Actual writing
                writer.writerow([arrivalTime, finishingTime, period, timeToDeadline, taskId])
