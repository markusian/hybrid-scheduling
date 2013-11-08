class Task:
	"""Describe a task in the simulator."""
	
	def __init__(self, idx, firstArrivalTime, computationTime, priority):
		"""
		Init the task.
		
		:param id: id of the task
		:param firstArrivalTime: the time when the task will be first released 
		on the system
		:param computationTime: the time the task needs to run before completion
		:param priority: Priority of the task
		:type id: int
		:type firstArrivalTime: int
		:type computationTime: int
		:type priority: int
		"""
		
		self.idx = idx
		self.firstArrivalTime = firstArrivalTime
		self.computationTime = computationTime
		self.priority = priority