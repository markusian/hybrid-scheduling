class TaskList(object):
    """This class is simply a container for the hard and soft tasks
    """
    
    def __init__(self,softTasks, hardTasks):
        """ Init the TaskList object
        
        :param softTasks: list of sofTasks
        :param hardTasks: list of hardTasks
        
        """
        
        self.softTasks = softTasks
        self.hardTasks = hardTasks
        
        