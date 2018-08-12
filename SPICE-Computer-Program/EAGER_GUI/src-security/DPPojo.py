'''
Created on Oct 20, 2014

@author: Anjila
'''

class DPPojo:
    def __init__(self):
        self.blockNumber = 0
        self.length = 0
        self.upImageList = []
        self.upImageType = []
        self.downImageList = []
        self.downImageType = []
        self.probePosnList = []
        self.beforeBlockMsgList = []
        self.afterBlockMsgList = []
        print "in DPPojo.py"
        
    def isValid(self):
        len_ = len(self.probePosnList)
        if len(self.upImageList) == len_ and len(self.upImageType) == len_ and len(self.downImageList) == len_ and len(self.downImageType) == len_ and len(self.probePosnList) == len_:
            self.length = len_
            return True
        return False
    
    def setLength(self, length_):
        self.length = length_
    
    def getLength(self):
        return self.length
    
    def setBlockNumber(self, blockNum):
        self.blockNumber = blockNum
        
    def setUpImageList(self, uImageList):
        self.upImageList = uImageList
        
    def setUpImageType(self, uImageType):
        self.upImageType = uImageType
        
    def setDownImageList(self, dImageList):
        self.downImageList = dImageList
        
    def setDownImageType(self, dImageType):
        self.downImageType = dImageType
        
    def setProbePosnList(self, probePosnList):
        self.probePosnList = probePosnList
        
    def setBeforeBlockMsgList(self, msglist_beforeBlock):
        self.beforeBlockMsgList = msglist_beforeBlock
    
    def setAfterBlockMsgList(self, msgList_afterBlock):
        self.afterBlockMsgList = msgList_afterBlock
        
    def getBlockNumber(self):
        return self.blockNumber
    
    def getUpImageList(self):
        return self.upImageList
    
    def getUpImageType(self):
        return self.upImageType
    
    def getDowmImageList(self):
        return self.downImageList
    
    def getDownImageType(self):
        return self.downImageType
    
    def getProbePosnList(self):
        return self.probePosnList
    
    def getBeforeBlockmsgList(self):
        return self.beforeBlockMsgList
    
    def getAfterBlockMsgList(self):
        return self.afterBlockMsgList

    def toString(self):  
        atr = "blockNumber= " + str(self.blockNumber) + "\n length of items= " + str(self.length) 
        if len(self.upImageList) > 0:
            atr += "\n upimage list = ["
            for i in self.upImageList:
                atr+=i+","
            atr+="]"
            
        if len(self.upImageType) > 0:
            atr += "\n up image type  = ["
            for i in self.upImageType:
                atr+=i+","
            atr+="]\n"
            
        if len(self.downImageList) > 0:
            atr += "\n down image list=["
            for i in self.downImageList:
                atr+=i+","
            atr+="]"
            
        if len(self.downImageType) > 0:
            atr += "\n down image type=["
            for i in self.downImageType:
                atr+=i+","
            atr+="]"
            
        if len(self.probePosnList) > 0:
            atr += "\n probe position list=["
            for i in self.probePosnList:
                atr+=i+","
            atr+="]"
        
        if len(self.beforeBlockMsgList) > 0:
            atr += "\n before block instruction id list = ["
            for i in self.beforeBlockMsgList:
                atr+=i+","
            atr+="]\n"
            
        if len(self.afterBlockMsgList) > 0:
            atr += "\n after block instruction id list= "
            for i in self.afterBlockMsgList:
                atr+=i+","
            atr+="]\n"
            
        return atr
            
# def main():
#     base_dir = os.path.dirname(__file__)
#     path=os.path.dirname(base_dir)+"/dotProbe/images/chatMessages.txt"
#     print os.path.dirname(base_dir)
#     print os.path.exists(path)
#     print os.path.isfile(path)
#     dialog=ChildFrame(None,-1,"dilaog")
#     dialog.ShowMessage()


    
    
