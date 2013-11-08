from Task import Task

class HardTask(Task):
    """Describe a hard periodic task in the simulator."""

    def __init__(self, id, firstArrivalTime, computationTime, period):
        """
        Init the task.
        
        :param id: id of the task
        :param firstArrivalTime: the time when the task will be first released 
        on the system
        :param computationTime: the time the task needs to run before completion
        :param period: Period of the task
        :param priority: Priority of the task
        :type id: int
        :type firstArrivalTime: int
        :type computationTime: int
        :type period: int
        :type priority: int
        """
        priority = 1.0/period  
        Task.__init__(self, id, firstArrivalTime, computationTime, priority)
        self.period = period