import heapq as hq

class Scheduler:
	"""The scheduler executes tasks instance in the simulator."""
	
	def __init__(self):
		self.executingTask = None
		self.waitingTasks = []
		self.clock = 0
	
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
		
		if (event.type == EventType.ARRIVAL):
			# Add the task to waiting tasks
			hq.heappush(self.waitingTasks, (event.task.priority, event.task))

		if (event.type == EventType.FINISHING):
			# Remove the task from waiting tasks
			# Since it is the running task it is the most priority
			hq.heappop(self.waitingTasks)
			
		# Call the scheduler
		return self.schedule()
				
	def schedule(self):
		"""
		Execute the most priority task on the scheduler.

		:return: The finishing event for the new task
		:rtype: Event
		"""
		
		task = self.waitingTask[0]
		self.executingTask = self.waitingTasks[0]
		
		if (task.startTime == None):
			task.startTime = self.clock
			
		finishingTime = self.clock + task.remainingTime
		
		return new Event(finishingTime, task, EventType.FINISHING)
		