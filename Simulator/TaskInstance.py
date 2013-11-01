class TaskInstance:
	"""An instance of a task (sometimes called a job)."""
	arrivalTime = None
	startTime = None
	computationTime = None
	remainingTime = None
	finishingTime = None
	preemptedTimes = None
	
	task = None
	
	def __init__(self, arrivalTime, task):
		"""
		Init the instance.
		
		:param arrivalTime: Time of arrival of the instance on the system.
		:type arrivalTime: int
		"""
		
		self.arrivalTime = arrivalTime
		self.task = task
		
		self.computationTime = task.computationTime
		self.remainingTime = task.remainingTime