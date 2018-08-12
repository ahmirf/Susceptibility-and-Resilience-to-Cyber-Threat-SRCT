'''
Created on Aug 20, 2014

@author: Anjila
'''
class QAPojo():
    def __init__(self):
        self.QA=[]
        self.instruction=""
        self.mathsID=""
        
    def setMathsID(self,QID):
        self.mathsID=QID;
        
    def getMathsID(self):
        return self.mathsID
    
    def setQA(self,eachQAPojo):
        if isinstance(eachQAPojo,eachQABlock):
            self.QA.append(eachQAPojo)
            
    def getQAList(self):
        return self.QA
    
    def setInstruction(self,instructionStr):
        self.instruction=instructionStr
         
    def getInstructionMsg(self):
        return self.instruction
    
class eachQABlock(object):
    def __init__(self):
        self.question=""
        self.options=[]
        self.OptionType=""
       
    def getOptionType(self):
        return self.OptionType.strip()
        
    def setQuestion(self,question):
        self.question=question
        
    def setOption(self,OptionPojo):
        if isinstance(OptionPojo, Option):
            self.options.append(OptionPojo)
        
    def getQuestion(self):
        return self.question
    
    def getOptions(self):
        return self.options

    
class Option:
    def __init__(self):
        self.text=[]
        self.value=[]
        self.answer=""
    
    def setOption(self,text,value):    
        self.setText(text)
        self.setValue(value)
        
    def setText(self,text_):
        self.text.append(text_)
        
    def getText(self):
        return self.text
    
    def setValue(self,value_):
        self.value.append(value_)
        
    def getValue(self):
        return self.value
    
    def getAnswer(self):
        return self.answer
    
    def setAnswer(self,answer):
        self.answer=answer
            