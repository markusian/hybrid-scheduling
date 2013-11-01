#We are using csv files for easy editing by hand
import csv

class InputParser(object):
    #Parse csv file

    #Give input data filename as parameter
    def __init__(self, filename):
        self.filename = filename
        self.taskList = []

    #Returns the task list with first row skipped
    #def getTaskList(self):
    #    return self.taskList[1:]

    #Read the data from file and return it as a list
    #Format is: tasktype,wcet,period,firstArrivalTime,interarrivalTime
    #First row is not passed
    def getTasksFromFile(self):
        with open(self.filename, 'rb') as fh:
            reader = csv.reader(fh)
            for row in reader:
                self.taskList.append(row)
                
        return self.taskList[1:]


#test and print the info
#ip = InputParser("test.csv")
#ip.getTasksFromFile()

#for i in range(0, len(ip.getTaskList())):
#    print ip.getTaskList()[i]
