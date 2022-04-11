import random

from Constant import max_X, max_Y, min_X, min_Y, center_X, center_Y

class ClientEntity:
    def __init__(self,id):
        self.id = id
        self.x = random.randint(min_X, max_X)
        self.y = random.randint(min_Y, max_Y)
        self.status = "Offline"
        self.consumption = 0
        self.reporting = ""
        
    def getLocation(self):
        return [self.x,self.y]
    
    def getID(self):
        return self.id
    
    def getStatus(self):
        return self.status

    def getConsumption(self):
        return self.consumption
    
    def getReporting(self):
        return self.reporting
    
    def setConsumption(self,consumption):
        self.consumption = consumption
    
    def setStatusOnline(self):
        self.status = "Online"     
    
    def setReporting(self,reporting):
        self.reporting = reporting
        

class HostEntity:
    def __init__(self):
        self.x = center_X
        self.y = center_Y
        self.status = "Offline"
        
    def getLocation(self):
        return [self.x,self.y]
    
    def getStatus(self):
        return self.status
    
    def setStatusOnline(self):
        self.status = "Online" 
