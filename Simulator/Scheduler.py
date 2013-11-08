import heapq as hq
from EventType import EventType
from Event import Event
from EventList import EventList
from TaskInstance import TaskInstance
from HardTask import HardTask

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
		
		if (self.executingTask is not None):
			self.executingTask.remainingTime -= diff
		
	def reactToEvent(self, event):
		"""
		Computes new events lists and perform action on the instance based on
		an event.
		
		:param event: The event to compute
		:type event: Event
		"""
		
		# Compute the clock
		self.advanceClock(event.timestamp)
		
		if (event.eventType == EventType.ARRIVAL):
			# Add the task to waiting tasks
			hq.heappush(self.waitingTasks, (event.taskInstance.task.priority, event.taskInstance))

		if (event.eventType == EventType.FINISHING):
			# Remove the task from waiting tasks
			# Since it is the running task it is the most priority
			task = hq.heappop(self.waitingTasks)[1]
			task.finishingTime = self.clock
			# TODO : Compute the statistics
			
		# Call the scheduler
		return self.schedule()
				
	def schedule(self):
		"""
		Execute the most priority task on the scheduler.

		:return: The finishing event for the new task, None if there is no
		task to run
		:rtype: Event
		"""
		
        if (len(self.waitingTasks) > 0):
			task = self.waitingTasks[0][1]
			self.executingTask = task
			
			if (task.startTime == None):
				task.startTime = self.clock
				
			finishingTime = self.clock + task.remainingTime
			
			return Event(finishingTime, task, EventType.FINISHING)
        else:
			return None
			
if __name__ == "__main__":
	scheduler = Scheduler()

	t1 = HardTask(1, 0, 1, 5)
	t2 = HardTask(2, 0, 2, 10)
	
	ti11 = TaskInstance(0, t1)
	ti12 = TaskInstance(5, t1)
	ti13  = TaskInstance(10, t1)
	
	ti21 = TaskInstance(0, t2)
	ti22 = TaskInstance(10, t2)
	ti23 = TaskInstance(20, t2)
	
	e11 = Event(0, ti11, EventType.ARRIVAL)
	e12 = Event(5, ti12, EventType.ARRIVAL)
	e13 = Event(10, ti13, EventType.ARRIVAL)
	
	e21 = Event(0, ti21, EventType.ARRIVAL)
	e22 = Event(10, ti22, EventType.ARRIVAL)
	e23 = Event(20, ti23, EventType.ARRIVAL)
	
	list = EventList()
	
	list.insertEvent(e11)
	list.insertEvent(e12)
	list.insertEvent(e13)
	list.insertEvent(e21)
	list.insertEvent(e22)
	list.insertEvent(e23)
	
	event = list.getNextEvent()
	while (event is not None):
		print event
		list.insertEvent(scheduler.reactToEvent(event))
		event = list.getNextEvent()
