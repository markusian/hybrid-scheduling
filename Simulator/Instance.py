class Instance(object):
    def start(self):
        """Operation to perform when the instance is started for the first time."""
        pass

    def finish(self):
        """Operation to perform when the instance finish."""
        pass

    def execute(self, time):
        """
        Execute the task for a certain time.

        :param time: Time to execute
        :type time: int
        """
        pass

    def nextInterrupt(self):
        """Determine when the instance will launch an interruption."""
        pass

    def started(self):
        """
        Determine if the task has already been started.

        :rtype: Boolean
        """
        return False

    def finished(self):
        """
        Determine if the task is finished.

        :rtype: Boolean
        """
        return False


    def priority(self):
        return -1

    def __cmp__(self, other):
        return self.priority() - other.priority()
