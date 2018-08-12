'''
Created on Jul 25, 2014

@author: Anjila
'''
import datetime,wx

from emailPojo import emailPojo
from globalTracker import globalVar

TAG_START = "<tag>"
TAG_END = "</tag>"
FROM_START = "<from>"
FROM_END = "</from>"
TO_START = "<to>"
TO_END = "</to>"
SUBJECT_START = "<subject>"
SUBJECT_END = "</subject>"
INSTRUCTION_START = "<message>"
INSTRUCTION_END = "</message>"
DIALOG_START = "<dialog>"
DIALOG_END = "</dialog>"

class emailUtilsNew:
    def __init__(self):
        print "===>emailUtils.py initiated"
        self.load_ = False
        
    def load(self, emailFileLocation):
        self.lenInbox = -1
        self.myEmailDict = {}
        self.readAllEmailsFromFile(emailFileLocation)
        self.load_ = True
        
        
        # #reads all the emails from file to the list of emailPojo
    def readAllEmailsFromFile(self, emailFileLocation):
        datafile = open(emailFileLocation, 'r')
        isAnEmail = False
        isMessage = False
        dialogId = -1200
        self.emailShownIndexList = []
        self.index = 0  # represents the index of self.emailList
        self.emailList = []
        for line in datafile.readlines():
            sline=line.strip()
            if sline == "" or sline[0] == '#':
                continue
            elif sline.isdigit() and len(sline) == 6:
                isAnEmail = True
                eachEmail = emailPojo()
                # #set the index as in email file
                eachEmail.set_indexId(sline)
                #add all the email index ID to the globalTracker emailIdlist array
                globalVar.emailIdList.append(sline)
                message = ""
     
            elif isAnEmail or isMessage:
                if sline.startswith(TAG_START) and line.find(TAG_END) >= 0:
                    endIndex = line.index(TAG_END)
                    eachEmail.setEmailtag(line[(line.index(TAG_START)+len(TAG_START)):endIndex].strip())
                elif sline.startswith(FROM_START) and line.find(FROM_END) >= 0:
                    endIndex = line.index(FROM_END)
                    eachEmail.set_from_field(line[(line.index(FROM_START)+len(FROM_START)):endIndex].strip())

                elif line.startswith(TO_START) and line.find(TO_END) >= 0:
                    endIndex = line.index(TO_END)
                    eachEmail.set_to(line[(line.index(TO_START)+len(TO_START)):endIndex].strip())

                elif line.startswith(SUBJECT_START) and line.find(SUBJECT_END) >= 0:
                    endIndex = line.index(SUBJECT_END)
                    eachEmail.set_subject(line[(line.index(SUBJECT_START)+len(SUBJECT_START)):endIndex].strip())
                elif sline.startswith(DIALOG_START) and DIALOG_END in line:
                   
                    dialogId = line[(line.index(DIALOG_START) + len(DIALOG_START)):line.index(DIALOG_END)].strip()
                    if dialogId.isdigit() and len(dialogId) == 4 and dialogId > 0:
                        eachEmail.set_dialogNumber(dialogId)
                elif line.startswith(INSTRUCTION_START):
                    isMessage = True
                    if INSTRUCTION_END in line and line.find(INSTRUCTION_END) >= 0:
                        message = line[(line.index(INSTRUCTION_START)+len(INSTRUCTION_START)):line.index(INSTRUCTION_END)] + "<br>"
                    else:
                        message += line[(line.index(INSTRUCTION_START)+len(INSTRUCTION_START)):] + "<br>"
                    
                elif isMessage and  not INSTRUCTION_END in line :
                        message += line + "<br>"
                        
                if INSTRUCTION_END in line:
                    eachEmail.set_message(message)
                    if message.find("<a href=")>=0:
                        eachEmail.setHasLink(True)
                    isMessage = False
                    isAnEmail = False
                    self.emailList.append(eachEmail)
        datafile.close()
        return self.emailList
    
    def getePojoFromEmailIndexID(self,indexID):
        index=-1
        for each_ePojo in self.emailList:
            index+=1
            if each_ePojo.get_indexId()==indexID:
                return each_ePojo
        return None
         
                
    # add such that the new added email will always be at the zeroth Index and the initial email at the zeroth index is moved at the corresponding index
    def addtoInboxFromReverse(self, inboxListCtrl, indexofFileEmailListToAdd,emailVar):
        if self.lenInbox >= 0 and self.checkIsValidEmailIndexInEmailList(indexofFileEmailListToAdd):  # means there is need to add in reverse manner
            ePojo2 = self.emailList[indexofFileEmailListToAdd]
            ind=self.getePojoFromEmailIndexID(ePojo2.get_indexId())
            inboxListCtrl.InsertStringItem(0, ePojo2.get_from_field() %emailVar)
            inboxListCtrl.SetStringItem(0, 1, ePojo2.get_subject()%emailVar)
            inboxListCtrl.SetStringItem(0, 2, datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S"))
            inboxListCtrl.SetItemData(0, 0)
            # first shift all the items by one index and make sure zeroth index is empty
            reverseIndex = len(self.myEmailDict)
            while reverseIndex >= 1:
                ePojo1 = self.getAndDelEmailPojoFromDictByUUID(reverseIndex - 1)
                if not ePojo1 == None:
                    self.myEmailDict[reverseIndex] = ePojo1
                    reverseIndex -= 1
                else:
                    break
            self.myEmailDict[0] = ePojo2
            self.updateInboxLength()
        elif self.checkIsValidEmailIndexInEmailList(indexofFileEmailListToAdd):
            # need to check this part
#             inbox contains no item so no swapping
            ePojo3 = self.emailList[indexofFileEmailListToAdd]
            inboxListCtrl.InsertStringItem(0, ePojo3.get_from_field()%emailVar)
            inboxListCtrl.SetStringItem(0, 1, ePojo3.get_subject()%emailVar)
            inboxListCtrl.SetStringItem(0, 2, datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S"))
            inboxListCtrl.SetItemData(0, 0)
            self.myEmailDict[0] = ePojo2
            self.updateInboxLength()
#         inboxListCtrl.SetItemFont(0, wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD,False, u'Arial')) 
            
    def addePojotoInboxFromReverse(self, inboxListCtrl,ePojoObj,emailVar):
        if self.lenInbox >= 0:  # means there is need to add in reverse manner
            inboxListCtrl.InsertStringItem(0, ePojoObj.get_from_field()%emailVar)
            inboxListCtrl.SetStringItem(0, 1, ePojoObj.get_subject()%emailVar)
            inboxListCtrl.SetStringItem(0, 2, datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S"))
            inboxListCtrl.SetItemData(0, 0)
            
            # first shift all the items by one index and make sure zeroth index is empty
            reverseIndex = len(self.myEmailDict)
            while reverseIndex >= 1:
                ePojo1 = self.getAndDelEmailPojoFromDictByUUID(reverseIndex - 1)
                if not ePojo1 == None:
                    self.myEmailDict[reverseIndex] = ePojo1
                    reverseIndex -= 1
                else:
                    break
            self.myEmailDict[0] = ePojoObj
            self.updateInboxLength()
        else:
            # need to check this part
#             inbox contains no item so no swapping
            inboxListCtrl.InsertStringItem(0, ePojoObj.get_from_field()%emailVar)
            inboxListCtrl.SetStringItem(0, 1, ePojoObj.get_subject()%emailVar)
            inboxListCtrl.SetStringItem(0, 2, datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S"))
            inboxListCtrl.SetItemData(0, 0)
            
            self.myEmailDict[0] = ePojoObj
            self.updateInboxLength()
        inboxListCtrl.SetItemFont(0, wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD,False, u'Arial'))    
            
    def updateInboxLength(self):
        self.lenInbox += 1
                
    def checkIsValidEmailIndexInEmailList(self, emailIndex):
        if emailIndex >= 0 and emailIndex < len(self.emailList):
            return True
        return False 
    
    def checkIsValidEmailIndexInDict(self, emailIndex):
        if emailIndex >= 0 and emailIndex < len(self.myEmailDict):
            return True
        return False
    
    def getEmailFromDictMessageByUUID(self, emailIndex):
        if self.checkIsValidEmailIndexInDict(emailIndex):
            return self.myEmailDict[emailIndex].get_message()
            
    def getAndDelEmailPojoFromDictByUUID(self, emailIndex):
        if self.checkIsValidEmailIndexInDict(emailIndex):
            ePojo = self.myEmailDict[emailIndex]
            del self.myEmailDict[emailIndex]
            return ePojo
        
    def getEmailPojoFromDictByUUID(self, emailIndex):
        if self.checkIsValidEmailIndexInDict(emailIndex):
            ePojo = self.myEmailDict[emailIndex]
            return ePojo        
    
def main():
    emodule = emailUtilsNew()
    emailList = emodule.load("file/emailMessages.txt")
    print "emali list count", len(emailList)
    for ePojo in emailList:
        ePojo.toString()

################################
#main()    
