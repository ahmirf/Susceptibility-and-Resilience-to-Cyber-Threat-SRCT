'''
Created on Jul 29, 2014

@author: Anjila
'''
import ConfigParser
import os
import globalTracker

class propertyFile:
    
    def __init__(self):
#          propertyFile.py initiated
        pass
        
    companyName = ""
    participantName = ""
    base_dir = os.path.dirname(__file__)
    Path = os.path.dirname(base_dir)
    print Path
    propPath = Path + "\\properties.ini"
    reportPathFirst = Path + "\\reports\\"
    reportPath=reportPathFirst+"\\[QQQ]"
    chatMsgFilePath = ""
    emailMsgFilePath = ""
    mathsQAFilePath = ""
    noticeMsgFielPath = ""
    DpScriptFilePath=""
    WpScriptFilePath=""
    dialogPath=""
    taskbarImg1 = ""
    taskbarImg2 = ""
    taskbarImg3 = ""
    taskbarImg4 = ""
    taskbarImg5 = ""
    taskbarImg6 = ""
    iPadSchemeImg=""
    
    def changePath(self):
        print "changing the paths erequired"
        self.reportPath=self.reportPath.replace("[QQQ]",str(globalTracker.globalVar.subjectId))
        self.replyBackEmails = self.reportPath + "\\repliedEmails.txt"
        self.dotProbeImagePath = self.Path + "\\dotProbe\\images\\"
        self.loadFilesPath = self.Path + "\\src\\file\\"
        self.phase3images=self.Path + "\\src\\icons\\"
        self.eventLog  = self.reportPath + "\\eventLog.txt"
        self.diagnosisDPLog = self.reportPath + "\\diagnosisDPLog.txt"
        self.responseLog=self.reportPath + "\\responseLog.dat"
        self.mathLog=self.reportPath + "\\math_responseLog.dat"
        self.imageDotProbeResult=self.reportPath+"\\ImageDotProbeResult_[XXX].dat"
        self.wordDotProbeResult=self.reportPath+"\\WordDotProbeResult_[XXX].iqdat"
        self.dialogReportResult=self.reportPath+"\\DialogReportResutl_[XXX].iqdat"
        Config = ConfigParser.ConfigParser()
        errorMsg = ""
        if os.path.isdir(self.Path):
            if os.path.isfile(self.propPath):
                Config.read(self.propPath)
                self.phaseNumber=Config.get('general-config', 'phaseNumber')
                self.companyName = Config.get('user-company-config', 'Company_name')
                self.companyEmail= Config.get('user-company-config', 'Company_email')
                self.participantName = Config.get('user-company-config', 'Name')
                self.eachQAInterval = Config.get('maths-config', 'eachQA-interval')  # 500
                self.fixationShowInterval = Config.get('dot-probe-config', 'fixation-interval')  # 500
                self.dotProbeUpDownImageShowInterval = Config.get('dot-probe-config', 'dot-probe-image-interval')  # 275
                self.dotShowInterval = Config.get('dot-probe-config', 'dot-interval')  # 500
                self.periodBetTrainingNMsg = Config.get('dot-probe-config', 'inbetween-training-msg-interval')  # 500
                self.idleResponseTime=Config.get('dot-probe-config', 'idle-response-time')  # 5000
                #WORD PROBE CONFIG
                self.wordProbeInterval=Config.get('word-probe-config', 'probe-interval')  # 500
                self.wordProbeFixation=Config.get('word-probe-config', 'word-fixation')  # "+++"
                self.wordProbeFixationInterval=Config.get('word-probe-config', 'fixation-interval')  # 500
                self.wordProbeWordInterval=Config.get('word-probe-config', 'word-Interval')  # 500
                #MATHS QUESTION CONFIG
                self.mathsQAInterval=Config.get('maths-config', 'eachQA-interval')  # 1000
                self.firstMathQAIntervalAfterfirstEmail=Config.get('maths-config', 'firstMathQIntervalAfterFirstEmail')  # 30000
                self.load()
            else:
                errorMsg += "properties.ini file is not available\n"
                
#     [dot-probe-config]
# inbetween-training-msg-interval:500
# fixation-interval:100
# dot-probe-image-interval:100
# dot-interval:100
# 
# [maths-config]
# eachQA-interval:100
    
    def load(self):
#         loading the paths required
        if os.path.isdir(self.loadFilesPath):
            self.chatMsgFilePath = self.loadFilesPath + "chatMessages.txt"
            self.emailMsgFilePath = self.loadFilesPath + "emailMessages.txt"
            self.mathsQAFilePath = self.loadFilesPath + "MathmaticalQuestionScript.txt"
            self.noticeMsgFielPath = self.loadFilesPath + "instructions.txt"
            self.DpScriptFilePath=self.loadFilesPath+"dot-probe.txt"
            self.WpScriptFilePath=self.loadFilesPath+"word-probe.txt"
            self.dialogPath=self.loadFilesPath+"dialogMessages.txt"
            self.taskbarImg1=self.phase3images+"taskbar1.png"
            self.taskbarImg2=self.phase3images+"taskbar2.png"
            self.taskbarImg3=self.phase3images+"email.png"
            self.taskbarImg4=self.phase3images+"chat.png"
            self.taskbarImg5=self.phase3images+"taskbar_long.png"
            self.taskbarImg6=self.phase3images+"taskbar5.png"
            self.InformationSymbol=self.phase3images+"Information_Symbol.png"
            self.iPadSchemeImg=self.phase3images+"freeiPadScheme1.jpg"
    