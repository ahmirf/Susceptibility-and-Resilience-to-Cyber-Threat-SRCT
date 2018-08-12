'''
Created on Aug 20, 2014

@author: Anjila
'''
from QAPojo import QAPojo
from QAPojo import eachQABlock
from QAPojo import Option
import re
from  globalTracker import MATH as maths

############################
#PATTERN:
############################
# <Question>
# <Q>Is apple a fruit?</Q>
# <Options>Yes,No</Options>
# <A>Yes</A>
# </Question>
QUESTION_START_TAG = "<Question>"
QUESTION_eND_TAG = "</Question>"
QUESTION_START = "<Q>"
QUESTION_END = "</Q>"
OPTION_START_TAG = "<Options_list"
OPTION_END_TAG = "</Options_list>"
OPTION_START = "<option>"
OPTION_END = "</option>"
OPTION_TEXT_START = "[!"
OPTION_TEXT_END = "]"
OPTION_VALUE_START = "["
OPTION_VALUE_END= "]"
INSTRUCTION_TAG_START="<Instruction>"
INSTRUCTION_TAG_END="</Instruction>"
ANSWER_TAG_START="<Answer>"
ANSWER_TAG_END="</Answer>"
INSTRUCTION_BEFORE_BLOCK_START="<before-block-instruction>"
INSTRUCTION_BEFORE_BLOCK_END="</before-block-instruction>"

OPTION_SEPARATOR=[]

class mathUtils:
    def __init__(self):
        self.load_ = False
#          mathUtils.py initiated

    def load(self, mathsQAFile):
        
        self.lenQuestions = -1
        self.QAODict = {}
        self.readQAO(mathsQAFile)
        self.load_ = True
        
    def readQAO(self, QAFileLocation):
        datafile = open(QAFileLocation, 'r')
        isAQuestionID=False
        isAQuestion = False
        isAQ = False
        areOptions = False
        isAOption=False
        isAnswer = False
        isAInstruction=False
        QNumber = -1
        lines=datafile.readlines()
        lineNum=0
        questionID=0
        type=""
        buffer=""
        while lineNum< len(lines) and len(lines[lineNum])>0:
            line=lines[lineNum].strip()
            lineNum+=1
            if line.strip() == "" or line.strip()[0] == '#':
                continue
            elif line.isdigit() and len(line) == 6:
                isAQuestionID = True
                # #set the question ID
                questionID=line
            elif line.strip().startswith(QUESTION_START_TAG):
                isAQuestion = True
                QNumber += 1
                eachQAPojo = QAPojo()
                eachQAPojo.setMathsID(questionID)
                questionID=0
            elif line.strip().startswith(QUESTION_eND_TAG):
                self.QAODict[QNumber] =eachQAPojo
                isAQuestion=False
            elif isAQuestion and line.strip().startswith(QUESTION_START):
                isAQ=True
                eachQABlockPojo=eachQABlock()
                startIndex = line.index(QUESTION_START)
                if QUESTION_END in line and line.find(QUESTION_END) >= 0:
                    endIndex = line.index(QUESTION_END)
                    eachQABlockPojo.setQuestion(line[startIndex + len(QUESTION_START):endIndex].strip())
                    isAQ=False
                else:
                    startPos=startIndex + len(QUESTION_START)
                    while lineNum< len(lines) and isAQ and (not QUESTION_END in line):
                        buffer+=line[startPos:len(line)]
                        startPos=0
                        line=lines[lineNum]
                        lineNum+=1
                    if QUESTION_END in line and line.find(QUESTION_END)>=0:
                        buffer+=line[startPos:line.index(QUESTION_END)]
                        eachQABlockPojo.setQuestion(buffer)
                        isAQ = False
                        buffer=""
                areOptions = False
                isAnswer = False            
            elif isAQuestion and line.strip().startswith(OPTION_START_TAG):
                startIndex = line.index(OPTION_START_TAG)
                isAQ = False
                areOptions = True
                isAnswer = False
                if maths.OPTION_TYPE[0] in line and line.find(maths.OPTION_TYPE[0])>=0:
                    eachQABlockPojo.OptionType=maths.OPTION_TYPE[0]
                elif maths.OPTION_TYPE[1] in line and line.find(maths.OPTION_TYPE[1])>=0:
                    eachQABlockPojo.OptionType=maths.OPTION_TYPE[1]
            elif isAQuestion and line.strip().startswith(OPTION_END_TAG):
#                 need to add optionPojo list to the eachQABlockPojo
                areOptions = False
                eachQAPojo.setQA(eachQABlockPojo)
            elif isAQuestion and line.strip().startswith(INSTRUCTION_TAG_START):
                isAInstruction=True
                startIndex=line.find(INSTRUCTION_TAG_START)
                if INSTRUCTION_TAG_END in line and line.find(INSTRUCTION_TAG_END)>=0:
                    endIndex=line.index(INSTRUCTION_TAG_END)
                    eachQAPojo.setInstruction(line[startIndex + len(INSTRUCTION_TAG_START):endIndex].strip())
                else:
                    buffer=""
                    startPos=startIndex + len(INSTRUCTION_TAG_START)
                    while lineNum< len(lines) and isAInstruction and INSTRUCTION_TAG_END in line and line.find(INSTRUCTION_TAG_END)<0:
                        buffer+=line[startPos:len(line)]
                        startPos=0
                        lineNum+=1
                        line=lines[lineNum]
                    if isAInstruction and INSTRUCTION_TAG_END in line and line.find(INSTRUCTION_TAG_END)>=0:
                        buffer+=line[startPos:line.index(INSTRUCTION_TAG_END)]
                        QAPojo.setInstruction( buffer)
                        buffer=""
                        isAInstruction=False
                        lineNum+=1
            elif isAQuestion and areOptions:
                if line.strip().startswith(OPTION_START):
                    # recursively store the optionPojo list until the end of OPTION_END
                    isAOption=True
                    optionPojo=Option()
                    line=lines[lineNum]
                    while  (not line.strip() == OPTION_END):
                        optionText = line.strip()
                        if optionText.startswith(OPTION_TEXT_START):
                            res=re.split('\].*\[',optionText )#split where it finds ] and [ with at any or none character in between them                            result = re.search('\].*\[', '[!Warehouse 1 (In Units sold)]ioi::=[124]')
                            optionPojo.setOption(res[0].replace(OPTION_TEXT_START,""), res[1].replace(OPTION_VALUE_END,""))
                        elif line.strip().startswith(ANSWER_TAG_START):
                            startIndex = line.index(ANSWER_TAG_START)
                            if ANSWER_TAG_END in line and line.find(ANSWER_TAG_END)>=0:
                                endIndex=line.index(ANSWER_TAG_END)
                                optionPojo.setAnswer(line[startIndex+len(ANSWER_TAG_START):endIndex])
                        lineNum+=1
                        line=lines[lineNum]
                    if line.strip() == OPTION_END:
                        lineNum+=1
                        isAOption=False
                        eachQABlockPojo.setOption(optionPojo)

    def printQA(self):
        eachQA=None
        for i in self.QAODict:
            eachQA =self.QAODict[i]
#             print eachQA.getMathsID()
            ListQ=eachQA.getQAList()
            for j in ListQ:
                Q=j
                questiontxt=Q.getQuestion()
                optList=Q.getOptions()
                #for eachOption in optList:
#                     print eachOption.getText()
#                     print eachOption.getValue()
                
def main():
    mUtils = mathUtils()
    mUtils.load("file/MathmaticalQuestionScript.txt")
    
# main()
