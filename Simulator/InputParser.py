import csv


class InputParser(object):

    def __init__(self, filename):
        self.filename = filename
        self.taskList = []

    def getTaskList(self):
        return self.taskList

    def getTasksFromFile(self):
        i = True
        with open(self.filename, 'rb') as fh:
            reader = csv.reader(fh)
            for row in reader:
                self.taskList.append(row)


#ip = InputParser("test.csv")
#ip.getTasksFromFile()

#for i in range(1, len(ip.getTaskList())):
#    print ip.getTaskList()[i]
