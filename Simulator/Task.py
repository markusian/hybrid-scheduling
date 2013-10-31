class Task:
	"""Describe a task in the simulator."""
	id
	firstArrivalTime
	computationTime
	
	def __init__(self, id, firstArrivalTime, computationTime):
		"""
		Init the task.
		
		:param id: id of the task
		:param firstArrivalTime: the time when the task will be first released 
		on the system
		:param computationTime: the time the task needs to run before completion
		:type id: int
		:type firstArrivalTime: int
		:type computationTime: int
		"""
		
		self.id = id
		self.firstArrivalTime = firstArrivalTime
		self.computationTime = computationTime