class TaskInstance:
    """An instance of a task (sometimes called a job)."""
	
    def __init__(self, arrivalTime, task):
		"""
		Init the instance.
		
		:param arrivalTime: Time of arrival of the instance on the system.
		:type arrivalTime: int
		"""
		
		self.arrivalTime = arrivalTime
		self.task = task
		
		self.computationTime = task.computationTime
		self.remainingTime = task.computationTime
		
		self.startTime = None
		self.finishingTime = None

    def __str__(self):
        return str(self.task.idx)
