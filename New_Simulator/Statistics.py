from Task import Task
from Instance import Instance
import csv

class Statistics(object):
    def __init__(self):
        self.instances = []

    def put(self, instance):
        self.instances.append(instance)

    def write(self, filename, col=12):
        file = open(filename, "wb")
        writer = csv.writer(file, delimiter='|')

        # Write the headers
        writer.writerow(["id"[0:col].center(col),
                         "type"[0:col].center(col), 
                         "arrival"[0:col].center(col), 
                         "finish"[0:col].center(col), 
                         "period"[0:col].center(col), 
                         "TTD"[0:col].center(col)])

        for i in self.instances:
            if i.type == Instance.HARD:
                writer.writerow([i.task.id[0:col].rjust(col),
                                 "hard"[0:col].rjust(col),
                                 str(i.arrival)[0:col].rjust(col),
                                 str(i.finish)[0:col].rjust(col),
                                 str(i.task.period)[0:col].rjust(col),
                                 str(i.time_to_deadline)[0:col].rjust(col)])
            elif i.type == Instance.SOFT:
                writer.writerow([i.task.id[0:col].rjust(col),
                                 "soft"[0:col].rjust(col),
                                 str(i.arrival)[0:col].rjust(col),
                                 str(i.finish)[0:col].rjust(col),
                                 ""[0:col].rjust(col),
                                 ""[0:col].rjust(col)])
