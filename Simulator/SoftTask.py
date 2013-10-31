class HardTask(Task):
	"""Describe a soft aperiodic task in the simulator."""
	interrarivalTime
	
	def __init__(self, id, firstArrivalTime, computationTime, priority,
		interrarivalTime):
		"""
		Init the task.
		
		:param id: id of the task
		:param firstArrivalTime: the time when the task will be first released 
		on the system
		:param computationTime: the time the task needs to run before completion
		:param priority: Priority of the task
		:param interrarivalTime: A function to get the next arrivalTime of the
		task
		:type id: int
		:type firstArrivalTime: int
		:type computationTime: int
		:type priority: int
		:type interrarivalTime: function
		"""
		super().__init__(self, id, firstArrivalTime, computationTime, priority)
		self.interrarivalTime = interrarivalTime