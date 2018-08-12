'''
Created on Sep 2, 2014

@author: Anjila
'''
class messagePojo:
    
    def __init__(self):
        self.message=""
        self.id=3043
        
    def setID(self,id_):
        self.id= id_
        
    def setMsg(self,msg):
        self.message=msg
        
    def getMsg(self):
        return self.message
    
    def getID(self):
        return self.id
    
    def toString(self):
        return "id= "+str(self.id)+"\nmessage content= "+self.message