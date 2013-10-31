class Scheduler:
	"""The scheduler executes tasks instance in the simulator."""
	executingTask
	clock = 0
	
	def advanceClock(self, addToClock):
		"""
		Move the clock forward.
		
		:param addToClock: Time to advance the clock
		:type addToClock: int
		"""
		
		self.clock += addToClock
		
	def reactToEvent(event):
		"""
		Computes new events lists and perform action on the instance based on
		an event.
		
		:param event: The event to compute
		:type event: Event
		"""
		pass