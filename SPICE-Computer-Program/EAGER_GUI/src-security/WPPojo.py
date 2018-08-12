'''
Created on Nov 18, 2014

@author: Anjila
'''
class WPPojo:
    def __init__(self):
        print "==> WPPojo.py initiated"
        self.blockNumber = 0
        self.length = 0
        self.threatWordList = []
        self.neutralWordList = []
        self.probePosnIsRandom=True
        ##if  self.probePosnList is empty then just choose randomly
        self.beforeBlockInstructionList = []
        self.afterBlockInstructionList = []
        
    def getLength(self):
        return self.length   
    
    def isValid(self):
        if len(self.threatWordList) == len(self.neutralWordList):
            self.length = len(self.threatWordList)
            return True
        return False
    
    def setBlockNumber(self,_blockNumber):
        self.blockNumber=_blockNumber
        
    def setBeforeBlockInstructionList(self,instructionlist_):
        self.beforeBlockInstructionList=instructionlist_
        
    def getBeforeBlockInstructionList(self):
        return self.beforeBlockInstructionList
        
    def setThreatWordList(self,wordList):
        self.threatWordList=wordList
        
    def getThreatWordList(self):
        return self.threatWordList
  
    def setNeutralWordList(self,neutralWordList):
        self.neutralWordList=neutralWordList
        
    def getNeutralWordList(self):
        return self.neutralWordList
    
    def setAfterBlockInstructionList(self,instructionlist_):
        self.afterBlockInstructionList=instructionlist_
        
    def getAfterBlockInstructionList(self):
        return self.afterBlockInstructionList
    
    def toString(self):  
        atr = "blockNumber= " + str(self.blockNumber) + "\n length of items= " + str(self.length) 
        if len(self.threatWordList) > 0:
            atr += "\n up word list = ["
            for i in self.threatWordList:
                atr+=i+","
            atr+="]"
        if len(self.neutralWordList) > 0:
            atr += "\n down image list=["
            for i in self.neutralWordList:
                atr+=i+","
            atr+="]"
        if len(self.beforeBlockInstructionList) > 0:
            atr += "\n before block instruction id list = ["
            for i in self.beforeBlockInstructionList:
                atr+=i+","
            atr+="]\n"
        if len(self.afterBlockInstructionList) > 0:
            atr += "\n after block instruction id list= "
            for i in self.afterBlockInstructionList:
                atr+=i+","
            atr+="]\n"
        return atr
        