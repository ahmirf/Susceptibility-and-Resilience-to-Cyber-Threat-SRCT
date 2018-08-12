'''
Created on Sep 25, 2014

@author: Anjila
'''
from dialogMsgPojo import dialogMsgPojo
from globalTracker import globalVar


INSTRUCTION_START = "<message>"
INSTRUCTION_END = "</message>"
DIALOG_START = "<dialog>"
DIALOG_END = "</dialog>"
TYPE_START = "<type>"
TYPE_END = "</type>"
NAME_VALUE_START = "<name-value>"
NAME_VALUE_END = "</name-value>"
USERNAME_START="<username>"
USERNAME_END="</username>"
PASSWORD_START="<password>"
PASSWORD_END="</password>"
class dialogUtils():
    
    dialogList = []
    load_ = False
    def __init__(self):
        pass
    
    def load(self, dialogFileLocation):
        self.readDialogFromFile(dialogFileLocation)
        dialogUtils.load_ = True
        
    def checkIsValidDialogID(self, dIdNumber):
        if dIdNumber >= 0 and len(dIdNumber) == 4 and dIdNumber in globalVar.dialogIdList :
            return True
        return False
    
    def getDialogPojoFrmDialoglistByID(self, dIdNumber):
        if self.checkIsValidDialogID(dIdNumber) and dialogUtils.load_ == True and dIdNumber in globalVar.dialogIdList:
            dIndex = globalVar.dialogIdList.index(dIdNumber)
            if dIndex >= 0 and dIndex < len(globalVar.dialogIdList):
                return dialogUtils.dialogList[dIndex]
            
          
    def readDialogFromFile(self, dialogFileLocation):
        datafile = open(dialogFileLocation, 'r')
        isADialog = False
        hasAnID = False
        isMsgStart = False
        type = ""
        id = ""
        message = ""
        isNameValue = False
        nameValueList = []
        nameValue = ""
        allline = datafile.readlines()
#         print len(allline)
        for line in allline:
            
            if line.strip() == "" or line.strip()[0] == '#':
                continue
            elif line.strip().isdigit() and len(line.strip()) == 4:
                hasAnID = True
                id = line.strip()
                  
            elif line.strip().startswith(DIALOG_START) and len(line.strip()) == 8:
                isADialog = True
                dialog = dialogMsgPojo()
            else:
                if isADialog and hasAnID:
                    
                    if line.strip().startswith(TYPE_START) and TYPE_END in line:
                        type = line[(line.index(TYPE_START) + len(TYPE_START)):line.index(TYPE_END)].strip()
                        dialog.setID(id)
                        globalVar.dialogIdList.append(id)
                        dialog.setType(type)
                        type = ""
                        nameValueList = []
                        id = ""
                        nameValue = ""
                    elif line.strip().startswith(INSTRUCTION_START):
                        isMsgStart = True
                        if INSTRUCTION_END in line:
                            message = line[(line.index(INSTRUCTION_START) + len(INSTRUCTION_START)):(line.index(INSTRUCTION_END))]
                            if not message == None and len(message.strip()) > 0:
                                dialog.setMessage(message)
                            isMsgStart = False
                            message = ""
                        else:
                            message += line[(line.index(INSTRUCTION_START) + len(INSTRUCTION_START)):]
                    elif isMsgStart and not INSTRUCTION_START in line:
                        if not INSTRUCTION_END in line:
                            message += line
                        elif INSTRUCTION_END in line:
                            message += line[:line.index(INSTRUCTION_END)]
                            if not message == None and len(message.strip()) > 0:
                                dialog.setMessage(message)
                            isMsgStart = False
                            message = ""
                    elif not isMsgStart and NAME_VALUE_START in line:
                        isNameValue = True
                        if NAME_VALUE_END in line:
                            nameValue = line[(line.index(NAME_VALUE_START) + len(NAME_VALUE_START)):line.index(NAME_VALUE_END)]
                            if not nameValue == None and len(nameValue.strip()) > 0:
                                nameValueList.append(nameValue)
                            nameValue = ""
                            isNameValue = False
                        else:
                            nameValue += line[(line.index(NAME_VALUE_START) + len(NAME_VALUE_START)):]
                    elif isNameValue and not NAME_VALUE_START in line:
                        if not NAME_VALUE_END in line:
                            nameValue += line
                        elif NAME_VALUE_END in line:
                            nameValue += line[:line.index(NAME_VALUE_END)]
                            if not nameValue == None and len(nameValue.strip()) > 0:
                                nameValueList.append(nameValue)
                            nameValue = ""
                            isNameValue = False
                    elif not isMsgStart and USERNAME_START in line and USERNAME_END in line:
                        isUsernameStart = True
                        userNameValue = line[(line.index(USERNAME_START) + len(USERNAME_START)):line.index(USERNAME_END)]
                        if not userNameValue == None and len(userNameValue.strip()) > 0:
                            dialog.setUserName(userNameValue)
                        userNameValue = ""
                        isUsernameStart = False
                    elif not isMsgStart and PASSWORD_START in line and PASSWORD_END in line:
                        isPwdStart = True
                        pwdValue = line[(line.index(PASSWORD_START) + len(PASSWORD_START)):line.index(PASSWORD_END)]
                        if not pwdValue == None and len(pwdValue.strip()) > 0:
                            dialog.setPassword(pwdValue)
                        pwdValue = ""
                        isPwdStart = False
                    elif line.startswith(DIALOG_END):
                        if not nameValueList == None and len(nameValueList) > 0:
                            dialog.setNameValuePairList(nameValueList)
                            nameValueList = []
                        dialogUtils.dialogList.append(dialog)
            
# def main():
#     
#     dmodule = dialogUtils()
#     dmodule.readDialogFromFile("file/dialogMessages.txt")
# main() 
