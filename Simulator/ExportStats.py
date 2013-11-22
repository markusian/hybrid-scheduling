#
#   This module writes a CSV file from tasklist.
#   Methods:
#       addToList(task, finishingTime)  -   void
#       writeToFile(self, filename)     -   returns True if everything went well
#
#
#   This module also has StatsList class which is used to
#   contain task and finishingTime (until task itself has it)
#
#

#Imports

#Different task types
from Task import Task
from TaskInstance import TaskInstance
#Needed for csv files
import csv

#Container for include tasks and finishing time
class StatsList(object):
    def __init__(self, task, clock):
        self.task = task
        self.finishingTime = clock
        
    def getTask(self):
        return self.task
    
    def getFinishingTime(self):
        return self.finishingTime

        
#Exporter
class ExportStats(object):
    """Outputs task information to a CSV-file."""
    
    def __init__(self):
        self.taskList = []
    
    #Add info to statistics list
    def addToList(self, task, clock):
        stat = StatsList(task, str(clock))
        self.taskList.append(stat)
    
    #Actual Filewriter
    def writeToFile(self, filename):
        try:
            with open(filename, "wb") as fh:
                writer = csv.writer(fh)
                #Header for the CSV
                writer.writerow(["Task Type", "Arrival Time", "Finishing Time", "Period", "Time To Deadline", "Task ID"])
                for i in range(0, len(self.taskList)):
                    try: 
                        #Define some variables to for easier arglist to writer
                        arrivalTime = self.taskList[i].getTask().arrivalTime
                        period = self.taskList[i].getTask().task.period
                        finishingTime = self.taskList[i].getFinishingTime()
                        timeToDeadline = str(int(period) + int(arrivalTime) - int(finishingTime))
                        taskId = self.taskList[i].getTask().task.idx
                        priority = str(self.taskList[i].getTask().task.priority)
                        #Actual writing
                        writer.writerow(["hard", arrivalTime, finishingTime, period, timeToDeadline, taskId])
                    except AttributeError:
                        #Define some variables to for easier arglist to writer
                        arrivalTime = self.taskList[i].getTask().arrivalTime
                        period = 0
                        finishingTime = self.taskList[i].getFinishingTime()
                        timeToDeadline = 0
                        taskId = self.taskList[i].getTask().task.idx
                        priority = str(self.taskList[i].getTask().task.priority)
                        #Actual writing
                        writer.writerow(["soft", arrivalTime, finishingTime, period, timeToDeadline, taskId])
            return True
        #File opening error
        except IOError:
            print
            print "________________________________________"
            print
            print "File opening error in file " + filename
            print "________________________________________"
            print
            return False
