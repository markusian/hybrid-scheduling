class Clock(object):
    def __init__(self):
        """Initialize the clock at time 0."""
        self.time = 0

    def advance(self, time):
        """
        Move the clock to the given time.

        :return: Elapsed time
        :rtype: int
        """
        diff = time - self.time
        self.time = time
        return diff

    def currentTime(self):
        """
        Return the current time.

        :rtype: int
        """
        return self.time
