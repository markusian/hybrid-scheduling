import json
from Task import PeriodicTask, AperiodicTask
from Server import BackgroundServer, PollingServer, DeferrableServer

class ReadConfig(object):
    def __init__(self):
        self.tasks = []
        self.server = None

    def read(self, filename):
        file = open(filename, 'rb')
        data = json.load(file)

        server = data["server"]
        periodics = data["periodics"]
        aperiodics = data["aperiodics"]

        # Configure server
        if server["type"] == "polling":
            self.server = PollingServer(server["capacity"], server["period"])
        elif server["type"] == "deferrable":
            self.server = DeferrableServer(server["capacity"], server["period"])
        else:
            self.server = BackgroundServer()

        # Retrieve periodics tasks
        for t in periodics:
            self.tasks.append(PeriodicTask(t["id"], t["wcet"], t["period"]))

        # Retrieve aperiodics tasks
        for t in aperiodics:
            self.tasks.append(AperiodicTask(t["id"], t["computation"], t["release"]))
