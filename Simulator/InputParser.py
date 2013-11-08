#
#   This module reads a CSV file (example is test.csv) from a file.
#   Methods:
#       createTask(self, row)               -   row is a line of information from CSV-file
#       getTasksFromFile(self, filename)    -   uses createTask() to create tasks from formatted text
#       addTaskToList(self, row)            -   adds task to a list
#       getTaskList(self)                   -   returns a list of tasks
#

#We are using csv files for easy editing by hand

#Imports

#Different task types
from HardTask import HardTask
from SoftTask import SoftTask
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

    #Adds task to a list
    def addTaskToList(self, task):
        #Add task to a list if is a task-type
        if isinstance(task, Task):
            self.taskList.append(task)
        
    #Create task object from a row
    def createTask(self, row):
        #Try to read row as a list
        try:
            #Hard task
            if row[0] == "hard":
                #HardTask(self, id, firstArrivalTime, computationTime, period)
                task = HardTask(1, row[3], row[1], row[2])
            #Soft task
            elif row[0] == "soft":
                #SoftTask(self, id, firstArrivalTime, computationTime, priority, interrarivalTime)
                task = SoftTask(2, row[3], row[1], row[5], row[4])
            #Wrong type of task or not recognized
            else:
                task = False
            #Adds task to a list
            self.addTaskToList(task)
        #Catch the error which happens if row is not properly formed
        except IndexError:
            return False

    
    #Read the data from file
    #Format is: tasktype,wcet,period,firstArrivalTime,interarrivalTime,priority
    def getTasksFromFile(self, filename):
		#Try to open a file and create handle as fh
        try:
            with open(filename, 'r') as fh:
                #Create reader object
                reader = csv.reader(fh)
                #Iterate through all lines
                for row in reader:
                    #Create a task from info
                    self.createTask(row)
        #File opening error
        except IOError:
            return False



#USED FOR TESTING
# ip = InputParser()
# ip.getTasksFromFile("test.csv")

# for i in range(0, len(ip.getTaskList())):
    # print ip.getTaskList()[i]

