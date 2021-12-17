import random

from common.Constant import max_X, max_Y, min_X, min_Y

class ClientEntity:
    def __init__(self,id):
        self.id = id
        self.x = random.randint(min_X, max_X)
        self.y = random.randint(min_Y, max_Y)
    
    def getLocation(self):
        return [self.x,self.y]
    
class HostEntity:
    def __init__(self):
        self.x = 0
        self.y = 0
        
    def getLocation(self):
        return [self.x,self.y]
