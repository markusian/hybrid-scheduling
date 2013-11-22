
class Event(object):
    def __init__(self, time, eventType, instance = None):
        self.instance = instance
        self.eventType = eventType
        self.time = time
    
    def __str__(self):
        return ("[Time : " + str(self.time) + ", "
                "Instance : " + str(self.instance) + ", "
                "Type : " + str(self.eventType) + "]")
        
    def __repr__(self):
        return self.__str__() 

    def __cmp__(self, other):
        return self.time - other.time
