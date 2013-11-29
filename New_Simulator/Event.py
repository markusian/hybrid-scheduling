class Event(object):
    ARRIVAL = "ARRIVAL" # A new instance arrive
    FINISH = "FINISH" # An instance finish
    SUSPEND = "SUSPEND" # The server suspends itself
    REFILL = "REFILL" # The server is refilled

    def __init__(self, type, time, instance = None):
        self.type = type
        self.time = time
        self.instance = instance

from PriorityQueue import PriorityQueue

class EventList(object):
    def __init__(self):
        self.finish = None
        self.suspend = None
        self.arrivals = PriorityQueue()

    def next(self):
        """
        Return the next event to compute.
        Discard some events.
        """
        finish = self.finish
        self.finish = None

        suspend = self.suspend
        self.suspend = None

        other = self.arrivals.first()

        earliest = min(finish.time if finish is not None else float('inf'), 
                       suspend.time if suspend is not None else float('inf'),
                       other.time if other is not None else float('inf'))

        if earliest == float('inf'):
            return None
        elif finish is not None and earliest == finish.time:
            return finish
        elif suspend is not None and earliest == suspend.time:
            return suspend
        else:
            return self.arrivals.pop()

    def put(self, event):
        """
        Put an event on the list.
        """
        if event is not None:
            if event.type == Event.SUSPEND:
                self.suspend = event
            elif event.type == Event.FINISH:
                self.finish = event
            else:
                self.arrivals.put(event, -event.time)
