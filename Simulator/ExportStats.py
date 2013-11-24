#
#   This module writes a CSV file from tasklist.
#   Methods:
#       addToList(task, finishingTime)  -   void
#       writeToFile(self, filename)     -   returns True if everything went well
#
#
#

#Imports

#Different task types
from Task import Task
from TaskInstance import TaskInstance
#Needed for csv files
import csv


#Exporter
class ExportStats(object):
    """Outputs task information to a CSV-file."""
    
    def __init__(self):
        self.taskList = []
    
    #Add info to statistics list
    def addToList(self, task):
        #stat = StatsList(task, str(clock))
        self.taskList.append(task)
    
    #Actual Filewriter
    def writeToFile(self, filename):
        try:
            with open(filename, "wb") as fh:
                writer = csv.writer(fh)
                #Header for the CSV
                writer.writerow(["Task Type", "Arrival Time", "Finishing Time", "Period", "Time To Deadline", "Task ID"])
                for i in range(0, len(self.taskList)):
                    #Hard task (if a soft task, throws AttributeError)
                    try: 
                        #Define some variables to for easier arglist to writer
                        arrivalTime = self.taskList[i].arrivalTime
                        period = self.taskList[i].task.period
                        finishingTime = self.taskList[i].finishingTime
                        timeToDeadline = str(int(period) + int(arrivalTime) - int(finishingTime))
                        taskId = self.taskList[i].task.idx
                        #priority = str(self.taskList[i].task.priority)
                        #Actual writing
                        writer.writerow(["hard", arrivalTime, finishingTime, period, timeToDeadline, taskId])
                    #Soft task
                    except AttributeError:
                        #Define some variables to for easier arglist to writer
                        arrivalTime = self.taskList[i].arrivalTime
                        period = ""
                        finishingTime = self.taskList[i].finishingTime
                        timeToDeadline = ""
                        taskId = self.taskList[i].task.idx
                        #priority = str(self.taskList[i].task.priority)
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
