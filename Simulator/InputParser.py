#
#   This module reads a CSV file (example is test.csv) from a file defined in Constructor.
#   Methods:
#       createTask(self, row)   -   row is a line of information from CSV-file
#       getTasksFromFile(self)  -   reads a file defined in Constructor
#                                   uses createTask() to create tasks from formatted text
#                                   creates a list of tasks
#       addTaskToList(self, row)-   adds task to a list
#       getTaskList(self)       -   returns a list of tasks
#
#

#We are using csv files for easy editing by hand

#Different task types
from HardTask import HardTask
from SoftTask import SoftTask

#Needed for csv files
import csv

class InputParser(object):
    #Parse csv file

    #Give input data filename as parameter
    def __init__(self, filename):
        self.filename = filename
        self.taskList = []

    #Create task object from a row
    def createTask(self, row):
        #Try to read row as a list
        try:
            #Hard task
            if row[0] == "hard":
                task = HardTask(1, row[3], row[1], float(row[2]))
            #Soft task
            elif row[0] == "soft":
                task = SoftTask(2, row[3], row[1], row[5], row[4])
            #Task type not defined or wrong type
            else:
                task = False
            return task
        #Catch the error which happens if row is not properly formed
        except IndexError:
            return False


    #Returns a task list
    def getTaskList(self):
        return self.taskList

    #Adds task info as a task object to a list
    def addTaskToList(self, row):
        #Create task object
        task = self.createTask(row)
        #Add task to a list if is a task-type (not false)
        if task != False:
            self.taskList.append(task)
    
    #Read the data from file and return it as a list
    #Format is: tasktype,wcet,period,firstArrivalTime,interarrivalTime
    #First row is not passed
    def getTasksFromFile(self):
		#Open file and create handle as fh
        with open(self.filename, 'rb') as fh:
			#Create reader object
            reader = csv.reader(fh)
			#Iterate through all lines
            for row in reader:
				self.addTaskToList(row)



#USED FOR TESTING
#ip = InputParser("test.csv")
#ip.getTasksFromFile()
#
#for i in range(0, len(ip.getTaskList())):
#    print ip.getTaskList()[i]

