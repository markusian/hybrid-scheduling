import heapq as hq

class PriorityQueue(object):
    def __init__(self):
        self.list = []

    def push(self, elem, priority):
        """Add an element to the list with the given priority."""
        hq.heappush(self.list, (priority, elem))

    def isEmpty(self):
        """Return true if the list is empty."""
        return len(self.list) == 0

    def pop(self):
        """Remove and return the most priority element."""
        if (self.isEmpty()):
            return None

        return hq.heappop(self.list)[1]

    def peak(self):
        """Return the most priority element (without removing it)."""
        if (self.isEmpty()):
            return None

        return self.list[0][1]
