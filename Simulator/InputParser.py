#
#   This module reads a CSV file (example is test.csv) from a file.
#   Methods:
#       createTask(self, row)               -   row is a line of information from CSV-file  -   returns task or False if task could not be made
#       getTasksFromFile(self, filename)    -   uses createTask() to create tasks from formatted text   -   returns True if reading went well
#       addTaskToList(self, row)            -   adds task to a list     -   returns True if task was added
#       getTaskList(self)                   -   returns a list of tasks
#       getHardTaskList(self)               -   returns a list of hard tasks
#       getfotTaskList(self)                -   returns a list of soft tasks
#
#

#We are using csv files for easy editing by hand

#Imports

#Different task types
from PeriodicTask import PeriodicTask
from AperiodicTask import AperiodicTask
from Task import Task
#Needed for csv files
import csv


#Class
class InputParser(object):
    """Parses CSV-files."""
    
    
    #Give input data filename as parameter
    def __init__(self):
        """
        :param taskList: List of tasks
        :type filename: list
        """
        
        self.taskList = []

    #Returns a task list
    def getTaskList(self):
        return self.taskList
    
    #Returns only hard tasks
    def getHardTaskList(self):
        hardTaskList = []
        for i in range(0, len(self.getTaskList())):
            if isinstance(self.getTaskList()[i], PeriodicTask):
                hardTaskList.append(self.getTaskList()[i])
        return hardTaskList
        
        
    #Returns only soft tasks
    def getSoftTaskList(self):
        softTaskList = []
        for i in range(0, len(self.getTaskList())):
            if isinstance(self.getTaskList()[i], AperiodicTask):
                softTaskList.append(self.getTaskList()[i])
        return softTaskList

    #Adds task to a list
    def addTaskToList(self, task):
        #Add task to a list if is a task-type
        if isinstance(task, Task):
            self.taskList.append(task)
            return True
        return False
        
    #Create task object from a row
    def createTask(self, row):
        #Try to read row as a list
        try:
            #Hard task
            if row[0] == "hard":
                # PeriodicTask(self, idx, wcet, period, arrivalTime)
                task = PeriodicTask(row[1], int(row[2]), int(row[3]), int(row[4]))
            #Soft task
            elif row[0] == "soft":
                # AperiodicTask(self, idx, arrivalTime, computationTime, priority)
                task = AperiodicTask(row[1], int(row[4]), int(row[2]), int(row[6]))
            #Wrong type of task or not recognized
            else:
                return False
            #Return task
            return task
        #Catch the error which happens if row is not properly formed
        except IndexError:
            return False

    
    #Read the data from file
    #Format is: tasktype,wcet,period,firstArrivalTime,interarrivalTime,priority
    def getTasksFromFile(self, filename):
		#Try to open a file and create handle as fh
        try:
            with open(filename, "rb") as fh:
                #Create reader object
                reader = csv.reader(fh)
                #Iterate through all lines
                for row in reader:
                    #Create a task from info and add it to a list
                    self.addTaskToList(self.createTask(row))
        #File opening error
        except IOError:
            print
            print "________________________________________"
            print
            print "File opening error in file " + filename
            print "________________________________________"
            print
            return False



#USED FOR TESTING
# ip = InputParser()
# ip.getTasksFromFile("test.csv")

# for i in range(0, len(ip.getTaskList())):
    # print ip.getTaskList()[i]

