class TaskInstance:
	"""An instance of a task (sometimes called a job)."""
	arrivalTime
	startTime
	computationTime
	finishingTime
	preemptedTimes
	
	def __init__(self, arrivalTime):
		"""
		Init the instance.
		
		:param arrivalTime: Time of arrival of the instance on the system.
		:type arrivalTime: int
		"""
		
		self.arrivalTime = arrivalTime