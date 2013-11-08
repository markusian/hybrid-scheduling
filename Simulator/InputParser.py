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
        self.taskInfo = []
        self.taskList = []

    #Stub for creating actual tasks from info
    def createTask(self, row):
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
        except IndexError:
            return False


    
    #Returns the task list with first row skipped
    def getTaskInfo(self):
        return self.taskInfo[1:]

    def getTaskList(self):
        return self.taskList

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
				#Create task object
                task = self.createTask(row)
				#Add task to a list if is a task-type (not false)
                if task != False:
                    self.taskList.append(task)
                #self.taskInfo.append(row)
                
        #return self.taskInfo[1:]


#test and print the info
#ip = InputParser("test.csv")
#ip.getTasksFromFile()
#
#for i in range(0, len(ip.getTaskList())):
#    print ip.getTaskList()[i]


