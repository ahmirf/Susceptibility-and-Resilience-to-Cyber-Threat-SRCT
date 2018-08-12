'''
Created on Sep 12, 2014

@author: Anjila
'''
class dialogMsgPojo:
    def __init__(self):
        self.id=""
        self.type=""
        self.message=""
        self.iconPath=""
        self.name_valueList=[]
        self.username=""
        self.password=""
        
    def setID(self,id_):
        self.id=id_
    def setType(self,type_):
        self.type=type_
    def setMessage(self,msg):
        self.message=msg
    def setIconPath(self,iconPath):
        self.iconPath=iconPath
    def setNameValuePairList(self,list_):
        self.name_valueList=list_
  
    def setUserName(self,username_):
        self.username=username_
    
    def getUserName(self):
        return self.username
    
    def setPassword(self,password_):
        self.password=password_
        
    def getPassword(self):
        return self.password
  
    def getID(self):
        return self.id
    def getType(self):
        return self.type
    def getMessage(self):
        return self.message
    def getIconPath(self):
        return self.iconPath
    def getNameValuePairList(self):
        return self.name_valueList
    
    def printSelf(self):
        if not self.id==None:
            print "id= ",self.id
        if not self.type==None:
            print "type= ",self.type
        if not self.message==None:
            print "message= ",self.message
        if not self.name_valueList==None and len(self.name_valueList)>0:
            print "***** name value list start*****"
            for line in self.name_valueList:
                print line
            print "***** name value list end*****"
    