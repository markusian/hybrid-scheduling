from Task import Task
from Instance import Instance
import csv

class Statistics(object):
    def __init__(self):
        self.instances = []

    def put(self, instance):
        self.instances.append(instance)

    def write(self, file, col=6):
        writer = csv.writer(file, delimiter='|', lineterminator='\n')

        # Write the headers
        writer.writerow(["id"[0:col].center(col),
                         "type"[0:col].center(col), 
                         "arrival"[0:col].center(col), 
                         "start"[0:col].center(col),
                         "finish"[0:col].center(col), 
                         "computation"[0:col].center(col),
                         "idle"[0:col].center(col),
                         "deadline"[0:col].center(col), 
                         "TTD"[0:col].center(col)])

        for i in self.instances:
            writer.writerow([i.task.id[0:col].rjust(col),
                             "hard"[0:col].rjust(col),
                             str(i.arrival)[0:col].rjust(col),
                             str(i.start)[0:col].rjust(col),
                             str(i.finish)[0:col].rjust(col),
                             str(i.computation)[0:col].rjust(col),
                             str(i.idle)[0:col].rjust(col),
                             str(i.deadline)[0:col].rjust(col),
                             str(i.time_to_deadline)[0:col].rjust(col)])
