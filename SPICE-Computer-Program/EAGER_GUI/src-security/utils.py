'''
Created on Aug 28, 2014

@author: Anjila
'''
import time

import wx

from DPPojo import DPPojo
from WPPojo import WPPojo
from FileOperations import FileOperations
from msgPojo import messagePojo
import wx.lib.agw.pybusyinfo as PBI
import os

#################################################################################
############################ DOT PROBE  ########################################
#################################################################################
INSTRUCTION_START="<instruction"
INSTRUCTION_END="<\instruction>"
DOT_PROBE_START="<dot-probe>"
DOT_PROBE_END="</dot-probe>"
BLOCK_START="<block>"
BLOCK_END="</block>"
UP_START="<up>"
UP_END="</up>"
UP_TYPE_START="<up-type>"
UP_TYPE_END="</up-type>"
DOWN_START="<down>"
DOWN_END="</down>"
DOWN_TYPE_START="<down-type>"
DOWN_TYPE_END="</down-type>"
PROBE_START="<probe-position>"
PROBE_END="</probe-position>"
PROBE_UP="UP"
PROBE_DOWN="DOWN"
INSTRUCTION_BEFORE_BLOCK_START="<before-block-instruction>"
INSTRUCTION_BEFORE_BLOCK_END="</before-block-instruction>"
INSTRUCTION_AFTER_BLOCK_START="<after-block-instruction>"
INSTRUCTION_AFTER_BLOCK_END="</after-block-instruction>"
#################################################################################
############################ WORD PROBE  ########################################
#################################################################################
WORD_PROBE_START="<word-probe>"
WORD_PROBE_END="</word-probe>"
WORD_PROBE_THREAT_WORD_START="<threat-words>"
WORD_PROBE_THREAT_WORD_END="</threat-words>"
WORD_PROBE_NEUTRAL_WORD_START="<neutral-words>"
WORD_PROBE_NEUTRAL_WORD_END="</neutral-words>"

        
class utils:
    messageList=[]
    chatMsgList=[]
    DPPojoList=[]
    WPPojoList=[]
    errorMessage=""
    
    def __init__(self):
        self.message=""   
        print "===> utils.py initiated"
        self.fileOperation=FileOperations()
        
    def write(self, fileLocation, text):
        self.fileOperation.write(fileLocation, text)

    def loadChatMsgFromFile(self, chatFileLocation):
#         loading chat
        lines=self.fileOperation.read(chatFileLocation)
        for line in lines:
            self.chatMsgList.append(line)
            
#loads message.txt
    def loadMessages(self,msgFileName):
        lines=self.fileOperation.read(msgFileName) 
        isAMessage=False
        message=""
        lineNumber=0
        for eachLine in lines:
            lineNumber+=1
            if eachLine.strip() == "" or eachLine.strip()[0] == '#':
                continue
            elif eachLine.strip().startswith(INSTRUCTION_START):
                if isAMessage:
                    d = PBI.PyBusyInfo("Your message in file ======> "+msgFileName+" is missing message end "'</message>'" /n")
                    wx.Yield()
                    time.sleep(3)
                    del d
                    quit()
                isAMessage = True
                msgPojo=messagePojo()
                id_= self.getIdFromString(eachLine)
                if id_.isdigit() and len(id_) == 6:
                    msgPojo.setID(id_)
                else:
                    d = PBI.PyBusyInfo("Your message in file ======> "+msgFileName+" <======= lineNumber= "+lineNumber+" given id "+ id_+" is not a valid id/n")
                    wx.Yield()
                    time.sleep(3)
                    del d
                    quit()
                if self.MsgStartIndex>0 and not INSTRUCTION_END in eachLine:
                    message+=eachLine[self.MsgStartIndex:]
            elif isAMessage and not INSTRUCTION_START in eachLine and not INSTRUCTION_END in eachLine:
                message+=eachLine+"\n"
            if isAMessage and INSTRUCTION_END in eachLine:
                if self.MsgStartIndex>0:
                    if(eachLine.strip().startswith(INSTRUCTION_START)):
                        message+=eachLine[(self.MsgStartIndex):eachLine.index(INSTRUCTION_END)]+"\n"
                    elif len(eachLine[:eachLine.index(INSTRUCTION_END)].strip())>0:
                        message+=eachLine[:eachLine.index(INSTRUCTION_END)]+"\n"
                isAMessage=False
                msgPojo.setMsg(message)
                self.messageList.append(msgPojo)
                message=""
        return self.messageList
            
    def getIdFromString(self,line):
        self.MsgStartIndex=-1
        isSpaceInBetwnNum=False
        if "id" in line and "=" in line:
            index=line.index("=")
            id_=""
            cnt=0
            for chr_ in line[index:]:
                cnt+=1
                if chr_==" " :
                    if len(id_)>0:
                        isSpaceInBetwnNum=True
                    continue
                if chr_.isdigit():
                    if not isSpaceInBetwnNum:
                        id_+=chr_
                    else:
                        return "has invalid ID"
                elif chr_==">":
                    self.MsgStartIndex=index+cnt
                    break
            if(len(id_.strip())==6 and id_.strip().isdigit()):
                return id_.strip()
        else:
            return " has No ID"
    
    def readWPScript(self,WPFilename):
        lines=self.fileOperation.read(WPFilename) 
        str_=""
        list_=[]
        errorMessage=""
        threatEndMet=True
        neutralEndMet=True
        for eachLine in lines:
            if eachLine.strip() == "" or eachLine.strip()[0] == '#':
                continue
            else:
                text=eachLine.strip()
                if text.startswith(WORD_PROBE_START) and len(text)==len(WORD_PROBE_START):
                    wppojo=WPPojo()
                elif text.startswith(BLOCK_START) and BLOCK_END in text:
                    blocknumber=eachLine[(eachLine.index(BLOCK_START)+len(BLOCK_START)):eachLine.index(BLOCK_END)].strip()
                    if blocknumber.isdigit():
                        wppojo.setBlockNumber(blocknumber)
                    else:
                        errorMessage+="the block number for word probe is not a number!!"
                elif text.startswith(INSTRUCTION_BEFORE_BLOCK_START) and INSTRUCTION_BEFORE_BLOCK_END in text:
                    listTxt=eachLine[(eachLine.index(INSTRUCTION_BEFORE_BLOCK_START)+len(INSTRUCTION_BEFORE_BLOCK_START)):eachLine.index(INSTRUCTION_BEFORE_BLOCK_END)].strip()
                    if not listTxt==None and len(listTxt)>0:
                        list_=listTxt.split(",")
                        if not list_==None and len(list_)>0:
                            wppojo.setBeforeBlockInstructionList(list_)
                elif text.startswith(WORD_PROBE_THREAT_WORD_START):
                    if  WORD_PROBE_THREAT_WORD_END in text:
                        threatEndMet=True
                        str_=eachLine[(eachLine.index(WORD_PROBE_THREAT_WORD_START)+len(WORD_PROBE_THREAT_WORD_START)):eachLine.index(WORD_PROBE_THREAT_WORD_END)].strip() 
                        list_=[]
                        list_=str_.split(",")
                        wppojo.setThreatWordList(list_)
                        list_=[]
                        str_=""
                    else:
                        str_ =eachLine[(eachLine.index(WORD_PROBE_THREAT_WORD_START)+len(WORD_PROBE_THREAT_WORD_START)):].strip()
                        threatEndMet=False
                elif not threatEndMet:
                    if WORD_PROBE_THREAT_WORD_END in text:
                        threatEndMet=True
                        str_=str_+eachLine[:eachLine.index(WORD_PROBE_THREAT_WORD_END)].strip()
                        list_=str_.split(",")
                        wppojo.setThreatWordList(list_)
                        list_=[]
                        str_=""
                    else:
                        str_=str_+eachLine.strip()
                        threatEndMet=False
                elif threatEndMet and text.startswith(WORD_PROBE_NEUTRAL_WORD_START):
                    if WORD_PROBE_NEUTRAL_WORD_END in text:
                        neutralEndMet=True
                        str_=eachLine[(eachLine.index(WORD_PROBE_NEUTRAL_WORD_START)+len(WORD_PROBE_NEUTRAL_WORD_START)):eachLine.index(WORD_PROBE_NEUTRAL_WORD_END)].strip() 
                        list_=str_.split(",")
                        wppojo.setNeutralWordList(list_)
                        list_=[]
                        str_=""
                    else:
                        str_ =eachLine[(eachLine.index(WORD_PROBE_NEUTRAL_WORD_START)+len(WORD_PROBE_NEUTRAL_WORD_START)):].strip()
                        neutralEndMet=False
                elif not neutralEndMet:
                    if WORD_PROBE_NEUTRAL_WORD_END in text:
                        neutralEndMet=True
                        str_=str_+eachLine[:eachLine.index(WORD_PROBE_NEUTRAL_WORD_END)].strip()
                        list_=str_.split(",")
                        wppojo.setNeutralWordList(list_)
                        list_=[]
                        str_=""
                    else:
                        str_=str_+eachLine.strip()
                        neutralEndMet=False
                elif neutralEndMet and text.startswith(INSTRUCTION_AFTER_BLOCK_START) and INSTRUCTION_AFTER_BLOCK_END in text:
                    listTxt=eachLine[(eachLine.index(INSTRUCTION_AFTER_BLOCK_START)+len(INSTRUCTION_AFTER_BLOCK_START)):eachLine.index(INSTRUCTION_AFTER_BLOCK_END)].strip()
                    if not listTxt==None and len(listTxt)>0:
                        list_=listTxt.split(",")
                        if not list_==None and len(list_)>0:
                            wppojo.setAfterBlockInstructionList(list_)
                elif text.startswith(WORD_PROBE_END):
                    if wppojo.isValid():
                        self.WPPojoList.append(wppojo)
                    else:
                        errorMessage=self.message+" \nnumber of words or its types or number of probes-position are unequal for block "+blocknumber    
                    
    def readAllScripts(self,DPfilename,WPFilename):
#         readAllScripts from utils
        self.readDPScript(DPfilename)
        self.readWPScript(WPFilename)
        if len(self.errorMessage)>0:
            dial = wx.MessageDialog(None, self.errorMessage, "abcd", wx.OK| wx.ICON_INFORMATION)
            dial.ShowModal()
            quit
        
    def readDPScript(self,DPfilename):
        lines=self.fileOperation.read(DPfilename) 
        str_=""
        list_=[]
        base_dir = os.path.dirname(__file__)
        path=os.path.dirname(base_dir)+"/dotProbe/images/"
        for eachLine in lines:
            if eachLine.strip() == "" or eachLine.strip()[0] == '#':
                continue
            else:
                text=eachLine.strip()
                if text.startswith(DOT_PROBE_START) and len(text)==len(DOT_PROBE_START):
                    #start of each dot probe task block
                    dpPojo=DPPojo()
                elif text.startswith(BLOCK_START) and BLOCK_END in text:
                    blocknumber=eachLine[(eachLine.index(BLOCK_START)+len(BLOCK_START)):eachLine.index(BLOCK_END)].strip()
                    if blocknumber.isdigit():
                        dpPojo.setBlockNumber(int(blocknumber))
                    else:
                        self.errorMessage+="the block number for dot probe is not a number!!"
                elif text.startswith(INSTRUCTION_BEFORE_BLOCK_START) and INSTRUCTION_BEFORE_BLOCK_END in text:
                    listTxt=eachLine[(eachLine.index(INSTRUCTION_BEFORE_BLOCK_START)+len(INSTRUCTION_BEFORE_BLOCK_START)):eachLine.index(INSTRUCTION_BEFORE_BLOCK_END)].strip()
                    if not listTxt==None and len(listTxt)>0:
                        list_=listTxt.split(",")
                        if not list_==None and len(list_)>0:
                            dpPojo.setBeforeBlockMsgList(list_)
                elif text.startswith(UP_START) and UP_END in text:
                    str_=eachLine[(eachLine.index(UP_START)+len(UP_START)):eachLine.index(UP_END)].strip()
                    list_=str_.split(",")
                    self.message=""
                    if not self.validateImageFile(path,list_):
                        if len(self.message)>0:
                            self.errorMessage+=self.message
                    else:
                        dpPojo.setUpImageList(list_)
                elif text.startswith(UP_TYPE_START) and UP_TYPE_END in text:
                    str_=eachLine[(eachLine.index(UP_TYPE_START)+len(UP_TYPE_START)):eachLine.index(UP_TYPE_END)].strip()
                    list_=str_.split(",")
                    
                    dpPojo.setUpImageType(list_)
                elif text.startswith(DOWN_START) and DOWN_END in text:
                    str_=eachLine[(eachLine.index(DOWN_START)+len(DOWN_START)):eachLine.index(DOWN_END)].strip()
                    list_=str_.split(",")
                    self.message=""
                    if not self.validateImageFile(path,list_):
                        if len(self.message)>0:
                            self.errorMessage+=self.message
                    else:
                        dpPojo.setDownImageList(list_)
                elif text.startswith(DOWN_TYPE_START) and DOWN_TYPE_END in text:
                    str_=eachLine[(eachLine.index(DOWN_TYPE_START)+len(DOWN_TYPE_START)):eachLine.index(DOWN_TYPE_END)].strip()
                    list_=str_.split(",")
                    dpPojo.setDownImageType(list_)
                elif text.startswith(PROBE_START) and PROBE_END in text:
                    str_=eachLine[(eachLine.index(PROBE_START)+len(PROBE_START)):eachLine.index(PROBE_END)].strip()
                    list_=str_.split(",")
                    if not self.validateType(list_):
                        if len(self.message)>0:
                            self.errorMessage=self.message+self.errorMessage
                    else:
                        dpPojo.setProbePosnList(list_)
                elif text.startswith(INSTRUCTION_AFTER_BLOCK_START) and INSTRUCTION_AFTER_BLOCK_END in text:
                    listTxt=eachLine[(eachLine.index(INSTRUCTION_AFTER_BLOCK_START)+len(INSTRUCTION_AFTER_BLOCK_START)):eachLine.index(INSTRUCTION_AFTER_BLOCK_END)].strip()
                    if not listTxt==None and len(listTxt)>0:
                        list_=listTxt.split(",")
                        if not list_==None and len(list_)>0:
                            dpPojo.setAfterBlockMsgList(list_)
                elif text.startswith(DOT_PROBE_END):
                    if dpPojo.isValid():
                        self.DPPojoList.append(dpPojo)
                    else:
                        self.errorMessage=self.message+" \nnumber of images or its types or probes are unequal for block "+blocknumber
            
    def printDPPojoList(self):
        for DPPojo in self.DPPojoList:
            print DPPojo.toString() 
            
    def printWPPojoList(self):
        for WpPojo_ in self.WPPojoList:
            print WpPojo_.toString()     
                   
    def validateImageFile(self,path,imageFileNameList):
        if len(imageFileNameList)<=0:
            self.message="no image file listed in the script\n"
            self.dialog.ShowMessage('Status Check',self.message)
            return False
        else:
            result=True
            for filename in imageFileNameList:
                if not (os.path.isfile(path+filename)):
                    self.message+=path+filename+" is not a valid file.\n"   
                    result=False
        return result
    
    def validateType(self,typeList):
        result=True
        if len(typeList)<=0:
            self.message="no probe type listed in the script\n"
        for eachType in typeList:
            if not (eachType.upper()==PROBE_DOWN or eachType.upper()==PROBE_UP):
                self.message="PROBE cannot be other than up or down.\n"
                result=False
        return result
    
    def getMessagePojoByID(self,num_id):
        for msg in self.messageList:
            if msg.getID()==num_id:
                return msg
        return None
                         
class App(wx.App):
   
    def __init__(self):
        wx.App.__init__(self, redirect=False, filename=None)
        
    def OnInit(self):
        u=utils()
        u.readAllScripts("file/dot-probe.txt","file/word-probe.txt")
        return True
    
def main():
    app = App()
    app.MainLoop()
    
if __name__ == "__main__":
    main() 