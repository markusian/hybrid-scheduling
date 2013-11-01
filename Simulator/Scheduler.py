class Scheduler:
	"""The scheduler executes tasks instance in the simulator."""
	executingTask = None
	clock = 0
	
	def advanceClock(self, time):
		"""
		Move the clock forward.
		
		:param time: Time to advance the clock
		:type time: int
		"""
		
		diff = time - self.clock
		
		self.clock = time
		
		if (executingTask is not None):
			executingTask.remainingTime -= diff
		
	def reactToEvent(self, event):
		"""
		Computes new events lists and perform action on the instance based on
		an event.
		
		:param event: The event to compute
		:type event: Event
		"""
		
		# Compute the clock
		self.advanceClock(event.timestamp)
		
		# If it´s an arrival task, put the task on the CPU if it´s free
		# or if the task is more priory
		if (event.type == EventType.ARRIVAL) and
			((self.executingTask is None) or 
			(self.executingTask.priority < event.task.priority)):
				self.switchTask(event.task)
				
		# If it´s a finishing event, remove the task from the scheduler
		# and start the next one (If available)
		if (event.type == EventType.FINISHING):
			pass
				
	def switchTask(self, task):
		"""
		Switch the task on the scheduler.
		
		:param task: The new task to put on the scheduler
		:type task: TaskInstance
		:return: The finishing event for the new task
		:rtype: Event
		"""
		
		self.executingTask = task
		
		if (task.startTime == None):
			task.startTime = self.clock
			
		finishingTime = self.clock + task.remainingTime
		
		return new Event(finishingTime, task, EventType.FINISHING)
		