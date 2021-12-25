import random

from Constant import max_X, max_Y, min_X, min_Y, center_X, center_Y

class ClientEntity:
    def __init__(self,id):
        self.id = id
        self.x = random.randint(min_X, max_X)
        self.y = random.randint(min_Y, max_Y)
    
    def getLocation(self):
        return [self.x,self.y]
    
    def getID(self):
        return self.id
    
class HostEntity:
    def __init__(self):
        self.x = center_X
        self.y = center_Y
        
    def getLocation(self):
        return [self.x,self.y]
