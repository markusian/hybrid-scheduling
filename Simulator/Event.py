
class Event(object):
    def __init__(self, time, eventType):
        self.eventType = eventType
        self.time = time

    def __init__(self, time, instance, eventType):
        self.instance = instance
        self.eventType = eventType
        self.time = time
    
    def __str__(self):
        
        var = [str(el) for el in [self.timestamp,self.taskInstance,self.eventType]]
        s = "("+",".join(var) + ")"
        return s
        
    def __repr__(self):
        return self.__str__()

                
        
