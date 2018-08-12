'''
Created on Jul 25, 2014

@author: Anjila
'''
class emailPojo:
    def __init__(self):
        self.indexId = ""
        self.fromField = ""
        self.to = ""
        self.subject = ""
        self.message = ""   
        self.date = ""
        self.dialogNumber = -1200
        self.hasDialog = False
        self.tag = ""
        self.hasLink=False

    def setHasLink(self,hasLink):
        self.hasLink=hasLink
        
    def getHasLink(self):
        return self.hasLink

    def setEmailtag(self, tag_):
        self.tag = tag_
        
    def getEmailTag(self):
        return self.tag
    
    def get_from_field(self):
        return self.fromField

    def get_indexId(self):
        return self.indexId

    def get_to(self):
        return self.to

    def get_dialogueNumber(self):
        return self.dialogNumber
    
    def get_subject(self):
        return self.subject

    def get_message(self):
        return self.message
    
    def get_date(self):
        return self.date

    def set_from_field(self, value):
        self.fromField = value

    def set_to(self, value):
        self.to = value

    def set_subject(self, value):
        self.subject = value

    def set_indexId(self, value):
        self.indexId = value

    def set_message(self, value):
        self.message = value
        
    def set_date(self, value):
        self.date = value
        
    def set_dialogNumber(self, dialogNumber_):
        self.dialogNumber = dialogNumber_
        self.hasDialog = True
        
    def get_hasDialog(self):
        return self.hasDialog
        
    def toString(self):
        print "\n **********************************************************************************************************************************************************************************"
        print "\n email tag: "+self.getEmailTag()
        print "EMAIL ID \t FROM \t TO \t SUBJECT \n", (self.get_indexId(), self.get_from_field(), self.get_to(), self.get_subject())
        print "\n\n"
        print "MESSAGE\n", (self.get_message())
        print "\n"




    
    
