class Task(object):
    """Describe a task in the simulator."""

    def __init__(self, idx):
        """
        Init the task.
        """

        self.idx = idx
        self.arrivalTime = 0

    def __str__(self):
        return ("ID : " + str(self.idx) + ""
                "\nArrival time : " + str(self.arrivalTime))

    def __repr__(self):
        return str(self)

    def generateEvents(self, clock, until):
        """
        Compute the events for a simulation until the given time
        """
        pass
