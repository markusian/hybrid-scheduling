#We are using csv files for easy editing by hand
from HardTask import HardTask
#from SoftTask import SoftTask
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
        if row[0] == "hard":
            task = HardTask(1, row[3], row[1], float(row[2]))
        elif row[0] == "soft":
            task = SoftTask(2, row[3], row[1], 0, row[4])
        else:
            return False
        return task


    
    #Returns the task list with first row skipped
    def getTaskInfo(self):
        return self.taskInfo[1:]

    def getTaskList(self):
        return self.taskList

    #Read the data from file and return it as a list
    #Format is: tasktype,wcet,period,firstArrivalTime,interarrivalTime
    #First row is not passed
    def getTasksFromFile(self):
        with open(self.filename, 'rb') as fh:
            reader = csv.reader(fh)
            for row in reader:
                task = self.createTask(row)
                if task != False:
                    self.taskList.append(task)
                #self.taskInfo.append(row)
                
        #return self.taskInfo[1:]


#test and print the info
#ip = InputParser("test.csv")
#ip.getTasksFromFile()

#for i in range(0, len(ip.getTaskList())):
#    print ip.getTaskList()[i]
