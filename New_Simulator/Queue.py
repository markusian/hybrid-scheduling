import heapq as hq
class FIFO(object):
    def __init__(self):
        self.list = []

    def put(self, elem):
        self.list.append(elem)

    def isEmpty(self):
        return len(self.list) == 0

    def pop(self):
        return self.list.pop(0)

    def first(self):
        return self.list[0]

class PriorityQueue(object):
    def __init__(self):
        self.list = []

    def put(self, elem, priority):
        """
        Add an element to the list with the given priority.
        """
        hq.heappush(self.list, (-priority, elem))

    def isEmpty(self):
        """
        Return true if the list is empty.
        """
        return len(self.list) == 0

    def pop(self):
        """
        Remove and return the most priority element.
        """
        if (self.isEmpty()):
            return None

        return hq.heappop(self.list)[1]

    def first(self):
        """
        Return the most priority element (without removing it).
        """
        if (self.isEmpty()):
            return None

        return self.list[0][1]
