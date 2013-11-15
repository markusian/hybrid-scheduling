
class Event(object):
    def __init__(self, time, eventType, instance = None):
        self.instance = instance
        self.eventType = eventType
        self.time = time
    
    def __str__(self):
        
        var = [str(el) for el in [self.time, self.instance, self.eventType]]
        s = "("+",".join(var) + ")"
        return s
        
    def __repr__(self):
        return self.__str__() 
