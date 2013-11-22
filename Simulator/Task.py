class Task(object):
    """Describe a task in the simulator."""

    def __init__(self, idx, arrivalTime, computationTime, priority):
        """
        Init the task.

        :param id: id of the task
        :param arrivalTime: the time when the task will be first released 
        on the system
        :param computationTime: the time the task needs to run before completion
        :param priority: Priority of the task
        :param period: Period of the task (if <0, then the task is aperiodic)
        :type id: int
        :type arrivalTime: int
        :type computationTime: int
        :type priority: int
        :type period: int
        """

        self.idx = idx
        self.arrivalTime = arrivalTime
        self.computationTime = computationTime
        self.priority = priority

    def __str__(self):
        return ("ID : " + str(self.idx) + ""
                "\nArrival time : " + str(self.firstArrivalTime) + ""
                "\nPriority : " + str(self.priority)) + ""

    def __repr__(self):
        return str(self)
