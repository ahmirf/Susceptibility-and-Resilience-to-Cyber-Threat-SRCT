'''
Created on Nov 6, 2014
@author: Anjila
'''
import wx.lib.scrolledpanel as scrollPanel
import os, wx, time, datetime, random, TaskbarModule, globalTracker, utils
import sys
from time import strftime
from BalloonTip import BalloonFrame
# from InstallationDialog import InstallationDialog
from QAPojo import QAPojo, eachQABlock, Option 
from emailModule import emailMainFrame
from globalTracker import PHASE, REPORT, MATH, MATHASSOC_DIALOG, globalVar, RESPONSECODE, CONSTANTS 
from mathUtils import mathUtils
from myTicker import myTicker
from phase3loads.FlashiPadScheme import FlashiPadScheme
from phase3loads.TabExample import MainFrame
from phase3loads.VirusGUIAlert import windowsVirusAlertDialog
from phase3loads.WindowsDefenderDialog import WindowsDefenderDialog
from phase3loads.WindowsDownloadPopup import WindowsDownloadPopup
from phase3loads.newAdobeUpdateDialog import newAdobeUpdateDialog
from phase3loads.newWindowsUpdateDialog import newWindowsUpdateDialog
# from phase3loads.windowsAntiVirusScan import WindowsAVScanDialog
from phase3loads.windowsUpdateDialog import windowsUpdateDialog 
from validators.Int_Validator import Int_Validator


base_dir = os.path.dirname(__file__)

imageWhite = base_dir + "/icons/white.jpg"    
imageredCross = base_dir + "/icons/redCross.jpg"
imageFixationStr = base_dir + "/icons/fixation.jpg"
imageProbeStr = base_dir + "/icons/asterisk.jpg"


postTrailPause = 2000
highDiff = 7.75
lowDiff = 2.75
TRAININGBLOCKINDEX = 0
SERIALNUM_START_INTRIALCODE_IMGDOTPROBE = 1

FIXATION_INTRIALCODE = 1
PROBE_INTRIALCODE = 2
PRACTISEIMAGE_INTRIALCODE = 3
TRAILIMAGE_INTRIALCODE = 4
UP_PROBE_INTRIALCODE = 5
dOWN_PROBE_INTRIALCODE = 6
CORRECT_RESPONSE_INTRIALCODE = 8
INCORRECT_RESPONSE_INTRIALCODE = 7
NONSENSE_INTRIALCODE = 9

UP_char = [ord("I"), ord("i"), ord("T"), ord("t")]
DOWN_char = [ord("M"), ord("m"), ord("V"), ord("v")]
IDLE_response = "IDLE"
CHAR_response = "CHAR"

LEFT = "<"
RIGHT = ">"
WP_LEFT_CHAR = [ord(LEFT), ord(",")]
WP_RIGHT_CHAR = [ord(RIGHT), ord(".")]
WORD_PROBE = [LEFT, RIGHT]
PAD_CHAR = " "
SERIALNUM_START_INTRIALCODE_WORDDOTPROBE = 1
# 1=threat in UP position
threatpositionWP = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# 1= left or <
probetypeWP = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] 
# 1=threat in UP position
threatpositionWPTrial = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]  
probeTypeWPTrial = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]

class MainFrame(wx.Frame):
    def __init__(self):
        ############################################ APPLICAITON START ############################################
        print "************************************* STARTING APPLICAITON ********************************************\n"
        
        self.utils = globalTracker.utils
        self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"************************************* STARTING APPLICAITON ********************************************\n")
        self.threatpositionLen = len(threatpositionWP) - 1
        self.probeTypeLen = len(probetypeWP) - 1
        
        self.threatpositionTrialLen = len(threatpositionWPTrial) - 1
        self.probeTypeTrialLen = len(probeTypeWPTrial) - 1
        
        self.fullSize = wx.DisplaySize()
        
        wx.Frame.__init__(self, parent=None, id=-1, title="parent", pos=(0, 0), size=self.fullSize)
        ############################key combo for Ctrl+Q then close the whole applicaiton ###########
        randomId = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onKeyCombo, id=randomId)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('Q'), randomId )])
        self.SetAcceleratorTable(accel_tbl)
        #################################################
        
        self.load()
        today = datetime.date.today()
        self.todayDat = str(today.month) + "|" + str(today.day) + "|" + str(today.year)
        date = str(today.month) + "-" + str(today.day) + "-" + str(today.year)
        globalVar.date = date
        self.todayTime = strftime("%H:%M:%S:%MS", time.localtime())
        time_ = strftime("%H-%M-%S-%MS", time.localtime())
        print "Program Start Time :", time_
        self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"Program Start Time :"+str( time_)+"\n")
        identity = str(globalVar.subjectId) + "_" + date + "-" + time_
        self.trialNum = 1
        ''''Pattern for journal
        date    subject    trialcode    trialtimeout    correct    latency
        '''
        self.serialNum_DP = SERIALNUM_START_INTRIALCODE_IMGDOTPROBE
        globalTracker.propertyVar.imageDotProbeResult = (globalTracker.propertyVar.imageDotProbeResult).replace("[XXX]", identity)  # mechanism to add subject id and timestamp to the name of each subject related file
        self.utils.write(globalTracker.propertyVar.imageDotProbeResult, REPORT.IMAGEDOTPROBEREPORTHEADER + "\n")
        self.WPReport = ""
        self.serialNum_WP = SERIALNUM_START_INTRIALCODE_WORDDOTPROBE
        globalTracker.propertyVar.wordDotProbeResult = (globalTracker.propertyVar.wordDotProbeResult).replace("[XXX]", identity)  # mechanism to add subject id and timestamp to the name of each subject related file
        self.utils.write(globalTracker.propertyVar.wordDotProbeResult, REPORT.WORDDOTPROBEREPORTHEADER + "\n")
        self.utils.write(globalTracker.propertyVar.responseLog, RESPONSECODE.responseHeader)
        self.utils.write(globalTracker.propertyVar.mathLog, RESPONSECODE.mathsResponseHeader)
        globalTracker.propertyVar.dialogReportResult = (globalTracker.propertyVar.dialogReportResult).replace("[XXX]", identity)
        self.utils.write(globalTracker.propertyVar.dialogReportResult, RESPONSECODE.DAILOG_REPORT_HEADER + "\n")
        self.inactivitylocalTime = 0.0
        self.onCharlocalTime = 0.0
        self.checkForDuality = (float(globalTracker.propertyVar.fixationShowInterval) + float(globalTracker.propertyVar.dotProbeUpDownImageShowInterval) +float(globalTracker.propertyVar.idleResponseTime)+ float(postTrailPause)) / 1000
        self.prevResponseTime = 0.0
        self.currentResponseTime = 0.0
        self.prevResponse = ""
        self.currentResponse = ""
        global acceptChar
        MainFrame.acceptChar = False
        global isRun
        MainFrame.isRun = False
        self.InitUI()
#         try:
#             self.InitUI()
#         except Exception, e:
#             print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% error %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
#             print e
#             print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% error %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
           
    def onKeyCombo(self, event):
        """"""
        print "You pressed CTRL+Q! ==> Destroying application"
        self.Destroy()
        event.Skip()  
        
        
        
    def InitUI(self):    
        ############## *****INSTRUCTION PANEL  *****  ###########
        self.instructionPnl = wx.Panel(self, id=24, size=self.msgPnlSize, style=wx.SIMPLE_BORDER, name="initial instruction panel")
        self.middleMsg = wx.TextCtrl(self.instructionPnl, size=(self.msgPnlSize[0], self.msgPnlSize[1]), value="", style=wx.ALL | wx.TE_CENTRE |wx.TE_NO_VSCROLL| wx.TE_READONLY|wx.TE_RICH2 | wx.TE_WORDWRAP | wx.NO_BORDER)
        msg_font = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.middleMsg.SetFont(msg_font) 
        self.msgOK_btn = wx.StaticText(self.instructionPnl, label="Press [SPACE] to Continue", size=wx.DefaultSize, style=wx.RIGHT, name="Press space to continue")
        self.middleMsg.Bind(wx.EVT_KEY_UP, self.onKeyStrokeInstructionOK)
        self.msgSizer = wx.BoxSizer(wx.VERTICAL)
        self.msgSizer.Add(self.msgPnlPosn)
        self.msgSizer.Add(self.middleMsg, 1, flag=wx.CENTER, border=10)
        self.msgSizer.Add(self.msgOK_btn, 0, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=self.msgPnlPosn[0])
        self.msgSizer.Add(self.msgPnlPosn)
        self.instructionPnl.SetSizer(self.msgSizer)
        self.instructionPnl.SetBackgroundColour("white")
   
        ############## *****TRAINING PANEL  *****  ###########
        self.dotProbeTrainingPnl = wx.Panel(self, id=28, size=self.fullSize, name="initial dot probetraining panel")
        self.DPtrainingUpPanel = wx.Panel(self.dotProbeTrainingPnl, id=30, name="dotProbeUpPanel in practise dot probe image panel")
        self.DPtrainingDownPanel = wx.Panel(self.dotProbeTrainingPnl, id=31, name="dotProbeDownPanel in practise dot probe image panel")
        self.DPtrainingRedCrossPanel = wx.Panel(self.dotProbeTrainingPnl, id=32, name="fixation Panel in practise dot probe fixation image panel")
        self.trainingUpImageBit = wx.StaticBitmap(self.DPtrainingUpPanel, bitmap=wx.EmptyBitmap(self.dotProbeImageWidth, self.dotProbeImageHeight))
        self.trainingDownImageBit = wx.StaticBitmap(self.DPtrainingDownPanel, bitmap=wx.EmptyBitmap(self.dotProbeImageWidth, self.dotProbeImageHeight))
        self.trainingredCrossImageBit = wx.StaticBitmap(self.DPtrainingRedCrossPanel, bitmap=self.tempFixation)
        self.dotProbeTrainingPnl.SetBackgroundColour("White")
        self.trainingUDPnlSizer = wx.BoxSizer(wx.VERTICAL)
        self.trainingUDPnlSizer.Add(self.dotProbeUpImagePosn)
        self.trainingUDPnlSizer.Add(self.DPtrainingUpPanel, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        self.trainingUDPnlSizer.Add(self.SpaceAfterDotProbeUpImage)
        self.trainingUDPnlSizer.Add(self.DPtrainingRedCrossPanel, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        self.trainingUDPnlSizer.Add((self.SpaceAfterDotProbeUpImage[0], self.SpaceAfterDotProbeUpImage[1] + self.fixationHeight))
        self.trainingUDPnlSizer.Add(self.DPtrainingDownPanel, proportion=0, flag=wx.ALIGN_CENTER, border=0)
        self.dotProbeTrainingPnl.SetSizer(self.trainingUDPnlSizer)
        
        ############## ***** DOT PROBE IMAGE PANEL   *****  ###########
        self.dotProbePnl = wx.Panel(self, id=41, size=self.fullSize, name="dotProbe image Panel in  frame")
        self.dotProbeUpPanel = wx.Panel(self.dotProbePnl, id=21, name="dotProbeUpPanel in dot probe image panel")
        self.dotProbeDownPanel = wx.Panel(self.dotProbePnl, id=23, name="dotProbeDownPanel in dot probe image panel")
        self.dotProbeFixationPanel = wx.Panel(self.dotProbePnl, id=22, name="dotProbe Fixation Panel in dot probe image panel")
        self.dotProbeUpImageBit = wx.StaticBitmap(self.dotProbeUpPanel, bitmap=wx.EmptyBitmap(self.dotProbeImageWidth, self.dotProbeImageHeight))
        self.dotProbeDownImageBit = wx.StaticBitmap(self.dotProbeDownPanel, bitmap=wx.EmptyBitmap(self.dotProbeImageWidth, self.dotProbeImageHeight))
        self.dotProbeFixationImageBit = wx.StaticBitmap(self.dotProbeFixationPanel, bitmap=self.tempFixation)
        self.dotProbePnl.SetBackgroundColour("White")
        self.dotProbeUDPnlSizer = wx.BoxSizer(wx.VERTICAL)
        self.dotProbeUDPnlSizer.Add(self.dotProbeUpImagePosn)
        self.dotProbeUDPnlSizer.Add(self.dotProbeUpPanel, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        self.dotProbeUDPnlSizer.Add(self.SpaceAfterDotProbeUpImage)
        self.dotProbeUDPnlSizer.Add(self.dotProbeFixationPanel, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        self.dotProbeUDPnlSizer.Add((self.SpaceAfterDotProbeUpImage[0], self.SpaceAfterDotProbeUpImage[1] + self.fixationHeight))
        self.dotProbeUDPnlSizer.Add(self.dotProbeDownPanel, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        self.dotProbePnl.SetSizer(self.dotProbeUDPnlSizer)
        
        ############## ***** DOT PROBE WORD TRAINING PANEL   *****  ###########
        
        self.WordProbeTrainingPnl = wx.Panel(self, id=38, size=self.fullSize, name="word Probe training Panel in frame")
        self.WordProbeTrainingPnl.SetBackgroundColour("White")
        self.WPTrainingUpPanel = wx.Panel(self.WordProbeTrainingPnl, id=40, name="word Probe training UpPanel in word probe panel")
        self.WPTrainingUpPanel.Bind(wx.EVT_SET_FOCUS, self.onFocusTrainingUpPanel)
        
        self.WpTrainFixationPanel = wx.Panel(self.WordProbeTrainingPnl, id=42, name="word Probe training Fixation Panel in word probe panel")
        self.WPTrainingDownPanel = wx.Panel(self.WordProbeTrainingPnl, id=41, name="word Probe training DownPanel in word probe panel")
        ###################################################
        self.WPTrainingUpTextCtrl = wx.TextCtrl(self.WPTrainingUpPanel, value="", size=(700, self.WPWordHeight + 0.7 * self.WPWordHeight), style=wx.TE_READONLY | wx.TE_CENTER | wx.TEXT_ALIGNMENT_CENTER | wx.ALL | wx.EXPAND | wx.NO_BORDER)
        WPfont = wx.Font(self.WPWordHeight, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Lucida Consolas')
        self.WPTrainingUpTextCtrl.SetFont(WPfont)
        
        self.WPTrainUPsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.WPTrainUPsizer.Add(self.WPTrainingUpTextCtrl, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
        self.WPTrainingUpPanel.SetSizer(self.WPTrainUPsizer)
        ##################################################################
        self.WPTrainingFixationTextCtrl = wx.TextCtrl(self.WpTrainFixationPanel, size=(-1, 1.6 * 120), style=wx.TE_RICH2 | wx.TE_READONLY | wx.TE_CENTER | wx.TEXT_ALIGNMENT_CENTER | wx.ALL | wx.EXPAND | wx.NO_BORDER)
        self.WPTrainingFixationTextCtrl.SetValue("x")
        WPfontOnWrong = wx.Font(120, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Lucida Consolas')
        attr = wx.TextAttr()
        attr.SetTextColour("Red")
        attr.SetFont(WPfontOnWrong)
        attr.SetLineSpacing(0)
        attr.SetAlignment(wx.TEXT_ALIGNMENT_JUSTIFIED)
        attr.SetParagraphSpacingBefore(0)
        attr.SetParagraphSpacingAfter(0)
        self.WPTrainingFixationTextCtrl.SetStyle(0, len(self.WPTrainingFixationTextCtrl.GetValue()), attr)
        self.WPTrainingFixation1TextCtrl = wx.TextCtrl(self.WpTrainFixationPanel, size=(-1, 1.6 * 120), style=wx.TE_RICH2 | wx.TE_READONLY | wx.TE_CENTER | wx.TEXT_ALIGNMENT_CENTER | wx.ALL | wx.EXPAND | wx.NO_BORDER)
        self.WPTrainingFixation1TextCtrl.SetValue("\n+++")
        self.WPTrainingFixation1TextCtrl.SetFont(WPfont)
        self.WPTrainMidSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.WPTrainMidSizer.Add(self.WPTrainingFixationTextCtrl, proportion=0, flag=wx.ALIGN_CENTER | wx.TE_CENTER | wx.ALL | wx.EXPAND)
        self.WPTrainMidSizer.Add(self.WPTrainingFixation1TextCtrl, proportion=0, flag=wx.ALIGN_CENTER | wx.TE_CENTER | wx.ALL | wx.EXPAND)
        self.WpTrainFixationPanel.SetSizer(self.WPTrainMidSizer)
        ##################################################################
        self.WPTrainingDownTextCtrl = wx.TextCtrl(self.WPTrainingDownPanel, size=(700, self.WPWordHeight + 0.7 * self.WPWordHeight), value="", style=wx.TE_READONLY | wx.TE_CENTER | wx.TEXT_ALIGNMENT_CENTER | wx.ALL | wx.EXPAND | wx.NO_BORDER)
        self.WPTrainingDownTextCtrl.SetFont(WPfont)
        self.WPTrainDOwnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.WPTrainDOwnSizer.Add(self.WPTrainingDownTextCtrl, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
        self.WPTrainingDownPanel.SetSizer(self.WPTrainDOwnSizer)
        ##################################################################
        self.WPTrainingUDPnlSizer = wx.BoxSizer(wx.VERTICAL)
        self.WPTrainingUDPnlSizer.Add((0, self.WPUpWordYPosn))
        self.WPTrainingUDPnlSizer.Add(self.WPTrainingUpPanel, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        self.WPTrainingUDPnlSizer.Add(self.WpTrainFixationPanel, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        self.WPTrainingUDPnlSizer.Add(self.WPTrainingDownPanel, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        self.WordProbeTrainingPnl.SetSizer(self.WPTrainingUDPnlSizer)
          
        ############## ***** DOT PROBE WORD PANEL   *****  ###########
        self.WordProbePnl = wx.Panel(self, id=51, size=self.fullSize, name="dotProbe word Panel in frame")
        self.WordProbePnl.SetBackgroundColour("White")
        self.wordProbeUpPanel = wx.Panel(self.WordProbePnl, id=31, name="word Probe UpPanel in dot probe word panel")
        self.wordProbeFixationPanel = wx.Panel(self.WordProbePnl, id=32, name="dotProbe Fixation Panel in dot probe word panel")
        self.wordProbeDownPanel = wx.Panel(self.WordProbePnl, id=33, name="dotProbeDownPanel in dot probe word panel")
        self.wordProbeUpTextCtrl = wx.TextCtrl(self.wordProbeUpPanel, size=(700, self.WPWordHeight + 0.7 * self.WPWordHeight), value="", style=wx.TE_READONLY | wx.TE_CENTER | wx.TEXT_ALIGNMENT_CENTER | wx.ALL | wx.EXPAND | wx.NO_BORDER)
        self.wordProbeUpTextCtrl.SetFont(WPfont)
        self.WPUPsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.WPUPsizer.Add(self.wordProbeUpTextCtrl, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
        self.wordProbeUpPanel.SetSizer(self.WPUPsizer)
        self.wordProbeFixationTextCtrl = wx.TextCtrl(self.wordProbeFixationPanel, size=(700, self.WPWordHeight + 0.7 * self.WPWordHeight), value="+++", style=wx.TE_READONLY | wx.TE_CENTER | wx.TEXT_ALIGNMENT_CENTER | wx.ALL | wx.EXPAND | wx.NO_BORDER)
        self.wordProbeFixationTextCtrl.SetFont(WPfont)
        self.WPMidSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.WPMidSizer.Add(self.wordProbeFixationTextCtrl, proportion=0, flag=wx.ALIGN_CENTER | wx.TE_CENTER | wx.ALL | wx.EXPAND)
        self.wordProbeFixationPanel.SetSizer(self.WPMidSizer)
        self.wordProbeDownTextCtrl = wx.TextCtrl(self.wordProbeDownPanel, size=(700, self.WPWordHeight + 0.7 * self.WPWordHeight), value="", style=wx.TE_READONLY | wx.TE_CENTER | wx.TEXT_ALIGNMENT_CENTER | wx.ALL | wx.EXPAND | wx.NO_BORDER)
        self.wordProbeDownTextCtrl.SetFont(WPfont)
        self.WPDOwnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.WPDOwnSizer.Add(self.wordProbeDownTextCtrl, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)
        self.wordProbeDownPanel.SetSizer(self.WPDOwnSizer)
        self.wordProbeUDPnlSizer = wx.BoxSizer(wx.VERTICAL)
        self.wordProbeUDPnlSizer.Add((0, self.WPUpWordYPosn1))
        self.wordProbeUDPnlSizer.Add(self.wordProbeUpPanel, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        self.wordProbeUDPnlSizer.Add(self.wordProbeFixationPanel, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        self.wordProbeUDPnlSizer.Add(self.wordProbeDownPanel, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        self.WordProbePnl.SetSizer(self.wordProbeUDPnlSizer)          
        ############## ***** DOT PROBE INTERACTIVE ENVIRONMENT   *****  ###########
        self.interactivePnl = wx.Panel(self, id=52, size=self.fullSize, name="interactive main panel")
        self.interactiveUpPnl = wx.Panel(self.interactivePnl, id=521, size=(self.displaySize[0], -1), style=wx.EXPAND | wx.ALL, name="interactive up panel")
        self.interactiveUpPnl.SetBackgroundColour("White")
        self.interactiveDownPnl = wx.Panel(self.interactivePnl, id=522, style=wx.EXPAND | wx.ALL, name="interactive down panel")
        ############## ***** self.interactiveUpPnl   *****  ###########
        self.QAPnl = scrollPanel.ScrolledPanel(self.interactiveUpPnl, id=5211, size=(self.QPnlWidht, self.QAHeight), style=wx.ALL, name="QA panel in interactive down panel")
        self.OptionPnl = wx.Panel(self.QAPnl, wx.ID_ANY, name="Option panel in QA panel")
        self.QAPnl.SetAutoLayout(1)
        self.QAPnl.SetupScrolling()
        self.QAbtnQ_Submit = wx.Button(self.QAPnl, label="Submit")
        self.QAbtnQ_Submit.Bind(wx.EVT_BUTTON, self.clickQASubmit)
        self.QAsizer = wx.BoxSizer(wx.VERTICAL)
        self.QAsizer.Add(self.OptionPnl, 0, wx.ALL|wx.EXPAND)
        self.QAsizer.Add(self.QAbtnQ_Submit, 0)
        self.QAPnl.SetSizer(self.QAsizer)
        self.QAPnl.Fit()
        self.QAPnl.Layout()
        self.interactiveUpPnlSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.interactiveUpPnlSizer.Add(self.QAPnl, 2)
        self.interactiveUpPnl.SetSizer(self.interactiveUpPnlSizer)
        ################ self.interactiveDownPnl  (ticker and taskbar)################
        self.tickerRpanel = wx.Panel(self.interactiveDownPnl, size=(self.displaySize[0], self.tickerHeight), style=wx.EXPAND | wx.ALL | wx.NO_BORDER, name="ticker panel in frame")
        self.ticker = myTicker(self.tickerRpanel)
        self.taskbarPanel = wx.Panel(self.interactiveDownPnl, size=(self.displaySize[0], self.taskbarHeight), style=wx.EXPAND | wx.ALL | wx.NO_BORDER, name="taskbar")
        self.interactiveDownSizer = wx.BoxSizer(wx.VERTICAL)
        self.interactiveDownSizer.Add(self.tickerRpanel, 0, wx.ALL, 5)
        self.interactiveDownSizer.Add(self.taskbarPanel, 0, wx.ALL, 5)
        self.interactiveDownPnl.SetSizer(self.interactiveDownSizer)
        ################ self.interactivePnl  ################
        self.TickerInitiated = False
        self.interactivePnlSizer = wx.BoxSizer(wx.VERTICAL)
        self.interactivePnlSizer.Add(self.interactiveUpPnl)
        self.interactivePnlSizer.Add(self.interactiveDownPnl, 0, wx.ALIGN_BOTTOM)
        self.interactivePnl.SetSizer(self.interactivePnlSizer)
        ######################## ALL #####################                   
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.instructionPnl, proportion=1, flag=wx.ALL | wx.EXPAND , border=5)
        self.vbox.Add(self.dotProbeTrainingPnl, proportion=0, flag=wx.ALL, border=5)
        self.vbox.Add(self.dotProbePnl, proportion=0, flag=wx.ALL, border=5)
        self.vbox.Add(self.WordProbeTrainingPnl, proportion=0, flag=wx.ALL, border=5)
        self.vbox.Add(self.WordProbePnl, proportion=0, flag=wx.ALL, border=5)
        self.vbox.Add(self.interactivePnl, proportion=0, flag=wx.ALL, border=5)
        self.SetSizer(self.vbox)
        self.trainIndex = 0
        self.dotProbeImgIndex = 0
        self.phaseIndex=self.dotProbeImgIndex
        self.HideInstructionPnl()
        self.HideDotProbeTrainingPnl()
        self.dotProbePnl.Hide()
        self.HideWPTrainingPnl()
        self.WordProbePnl.Hide()
        self.interactivePnl.Hide()  
        self.previousPhase = ""
        self.currentPhase = ""
        self.currentBlockNumnber = TRAININGBLOCKINDEX
        try:
            PHASE.phaseNumber = int(globalTracker.propertyVar.phaseNumber)
        except:
            errordial = wx.MessageDialog(self, "The phaseNumber field in properties.ini file is not a number\n... Starting from default phase ... ", "Error Information", wx.ICON_HAND)
            errordial.ShowModal()
            PHASE.phaseNumber = 1  # 1
        self.stateInPhase = 1
        self.instructionIndex = 0
        ##################wordPanel###############
        self.trainWPIndex = 0
        self.WPFixationError = False
        self.WPWordUPLen = 0
        self.WPWordDOWNLen = 0
        self.prevTime = time.asctime(time.localtime(time.time()))
        self.inactivity = None
        self.wordProbeIndex = 0
        self.emailFrame = None
        self.initiationNumber = 0
        self.FlowOrderNumber = -1
        ######################response logging parameters ##################
        self.MathsIndex = -1
        self.parentID = -1
        ######################taskbar parameters ##################
        self.taskbar = None
        ######################ticker parameters ##################
        self.tickertimer = None
        self.tickerFocustimer = None
        globalTracker.RESPONSECODE.responseLogBuffer = ""
        self.mathsLogBuffer = ""
        self.answerSouce = {}
        self.answerSouceIndex = 0
        self.initiate()
        self.Fit()
        self.Layout()
        if not PHASE.phaseGuider[PHASE.phaseNumber] == "INTERACTIVE ENVIRONMENT PHASE":
#             print "do not hide mouse"
            self.HideMouse()
        self.dialogSN = -1
       
    def initiate(self):
        self.initiationNumber += 1       
        if (self.stateInPhase == 4):  # after the three states are finished,it means it is a new block
            self.stateInPhase = 1
            self.instructionIndex = 0
            self.currentBlockNumnber += 1
            print "self.currentBlockNumnber = " + str(self.currentBlockNumnber)
            self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"self.currentBlockNumnber = " + str(self.currentBlockNumnber)+"\n")
            if PHASE.phaseGuider[PHASE.phaseNumber] == "DOT PROBE PHASE":
                if self.currentBlockNumnber >= len(self.utils.DPPojoList):
                    PHASE.phaseNumber += 1
            elif PHASE.phaseGuider[PHASE.phaseNumber] == "DOT PROBE TRAINING PHASE":
                PHASE.phaseNumber += 1
            elif PHASE.phaseGuider[PHASE.phaseNumber] == "WORD PROBE PRACTISE PHASE":
                PHASE.phaseNumber += 1
            elif PHASE.phaseGuider[PHASE.phaseNumber] == "WORD PROBE PHASE":
                PHASE.phaseNumber += 1
        print "PHASE.phaseNumber = " + str(PHASE.phaseNumber) 
        self.utils.write(globalTracker.propertyVar.diagnosisDPLog,  "PHASE.phaseNumber = " + str(PHASE.phaseNumber)+"\n" )         
        self.previousPhase = self.currentPhase 
        self.currentPhase = PHASE.phaseGuider[PHASE.phaseNumber]
        if not self.previousPhase == self.currentPhase:
            self.trialNum = 1
            self.currentResponseTime = time.clock()
            self.currentResponse = IDLE_response
            wr = "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n&&&&&&&&&&&&&&    " + self.currentPhase + "    &&&&&&&&&&&&&&\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n"
            self.utils.write(globalTracker.propertyVar.eventLog, wr)
            print wr
            self.utils.write(globalTracker.propertyVar.diagnosisDPLog,wr+"\n")
            if self.currentPhase == "WORD PROBE PRACTISE PHASE":
                self.currentBlockNumnber = TRAININGBLOCKINDEX
        self.startPhase()
            
    def startPhase(self):
        self.prepostInstructionMsgList = []
        if self.isValidBlockNumber():  
            if (self.stateInPhase % 2) == 0:
                if PHASE.phaseGuider[PHASE.phaseNumber] == "DOT PROBE TRAINING PHASE":
                    self.startDotProbeTraining()
                elif PHASE.phaseGuider[PHASE.phaseNumber] == "DOT PROBE PHASE":    
                    self.startDotProbeReal()
                elif PHASE.phaseGuider[PHASE.phaseNumber] == "WORD PROBE PRACTISE PHASE":
                    self.WPReport = ""
                    self.WPReport += str(self.serialNum_WP) + "\t" + str(self.todayDat) + "\t" + str(self.todayTime) + "\t" + str(REPORT.BLOCK_INFO[self.currentBlockNumnber]) + "\t" + str(REPORT.TRIALCODE_WP[0]) + "\t"
                    self.startWordProbeTraining()
                elif PHASE.phaseGuider[PHASE.phaseNumber] == "WORD PROBE PHASE":
                    self.WPReport = ""
                    self.WPReport += str(self.serialNum_WP) + "\t" + str(self.todayDat) + "\t" + str(self.todayTime) + "\t" + str(REPORT.BLOCK_INFO[self.currentBlockNumnber] + str(self.currentBlockNumnber)) + "\t" + "[XXX]\t"
                    self.startWordProbeReal()
                elif PHASE.phaseGuider[PHASE.phaseNumber] == "INTERACTIVE ENVIRONMENT PHASE":
                    self.utils.write(globalTracker.propertyVar.diagnosisDPLog, "Showing mouse pointer on the screen/n")
                    print "Showing mouse pointer on the screen"
                    self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"Showing mouse pointer on the screen/n")
                    self.ShowMouse()
                    self.startInteractiveEnvironment()
            else:           
                if self.stateInPhase == 1:  # instruction state before training images appear
                    self.prepostInstructionMsgList = self.getPreBlockInstructionList()
                elif self.stateInPhase == 3:
                    self.prepostInstructionMsgList = self.getPostBlockInstructionList()
                if not self.prepostInstructionMsgList == None and len(self.prepostInstructionMsgList) > 0:
                    self.HideDotProbeTrainingPnl()
                    self.dotProbePnl.Hide()
                    self.WordProbePnl.Hide()
                    self.HideWPTrainingPnl()
                    if self.instructionIndex < len(self.prepostInstructionMsgList):
                        instructionId = self.prepostInstructionMsgList[self.instructionIndex]  # this gives list of id of the instructions to show
                        self.currentInstructionPojo = self.utils.getMessagePojoByID(instructionId)
                        self.middleMsg.Clear()
                        if not self.currentInstructionPojo == None and self.currentInstructionPojo.getID() != "000000":
                            self.middleMsg.AppendText(self.currentInstructionPojo.getMsg()) 
                            self.instructionIndex += 1
                            self.ShowInstructionPnl()
                        else:
                            self.instructionIndex += 1  # this means the currentInstructionPojo has not been used at all
#                         if ((self.instructionIndex+1)>len(self.prepostInstructionMsgList)):
# #                             self.stateInPhase +=1
#                             print "hre you are"000000
                            
                else: 
#                     print "may be this else part can be removed"
                    self.stateInPhase += 1
                    self.initiate()
                    
    def NotifyTimer(self):
        """The Creation Timer Has Expired. Creates The BalloonTip Frame."""
        self.BalloonFrame = BalloonFrame(self._widget, classparent=self)
        self.BalloonFrame.Show(True)
        self.starttime = time.time()
        self.showtime.Stop()
        del self.showtime
        self.destroytime = wx.PyTimer(self.DestroyTimer)
        self.destroytime.Start(self._enddelaytime)
        
    def OntickerTimer(self, event):
        if not self.ticker == None:
            self.ticker.start()    
        event.Skip()

    def OntickerFocusTimer(self, event):
        if not self.ticker == None:
            self.ticker.setFocusonTicker()
        event.Skip()
                   
    def startInteractiveEnvironment(self):
        self.instructionPnl.Hide()
        self.dotProbeTrainingPnl.Hide()
        self.dotProbePnl.Hide()
        self.HideWPTrainingPnl()
        self.WordProbePnl.Hide()
        self.tickerRpanel.Show()
        self.tickerRpanel.Fit()
        self.tickerRpanel.Layout()
        self.dotProbePnl.Hide()
        self.interactivePnl.Show()
        self.interactivePnl.Fit()
        self.interactivePnl.Layout()
        self.interactivePnlSizer.Layout() 
        if self.TickerInitiated == False:
            self.TickerInitiated = True
            if self.tickertimer == None:
                self.tickertimer = wx.Timer(self) 
                self.Bind(wx.EVT_TIMER, self.OntickerTimer, self.tickertimer)
                self.tickertimer.Start(250) 
            if self.tickerFocustimer == None:
                self.tickerFocustimer = wx.Timer(self) 
                self.Bind(wx.EVT_TIMER, self.OntickerFocusTimer, self.tickerFocustimer) 
                self.tickerFocustimer.Start(72000)
        self.initiateEmail()
        if self.taskbar == None:
            self.taskbar = TaskbarModule.MyTaskbar(self.taskbarPanel, self.emailFrame, self.taskbarIconwidth, self.taskbarHeight, self.taskbarRightIconwidth, self.taskbarRemainingWidth)
        self.FlowOrderNumber += 1
        startTime = time.strftime("%H:%M:%S", time.localtime())
        if self.FlowOrderNumber < len(globalTracker.floworderInstance.FLOWORDER):
            flow = globalTracker.floworderInstance.FLOWORDER[self.FlowOrderNumber]  
            if not flow == None and isinstance(flow, str):
                RESPONSECODE.flowSeq += 1
                flow = flow.strip().lower()
                if flow == "m":
                    self.QAbtnQ_Submit.Show()
                    self.MathsIndex += 1
                    globalTracker.floworderInstance.createEmptyEmailControlInfoForMathLoad(self.FlowOrderNumber, self.MathsIndex)
                    self.parentID = -1
                    self.StartQARepeat()
                elif flow.startswith("email-"):
                    self.QAbtnQ_Submit.Show()
                    self.parentID = -1
                    emailInfo = flow.split("-")
                    isForced = False
                    emIndexID = emailInfo[1].strip()
                    if len(emailInfo) >= 3 and len(emailInfo[2].strip()) > 0 and emailInfo[2].strip().lower() == "f":
                        isForced = True
                    if len(emIndexID) == 6 and emIndexID.isdigit() and (emIndexID in globalVar.emailIdList):
                        globalTracker.floworderInstance.createEmptyEmailControlInfoForNonMathLoad(self.FlowOrderNumber)
                        self.emailFrame.emailNext(emIndexID, isForced, self.FlowOrderNumber, -1, -1, -1, "", startTime)
                        self.initiate()
                elif flow == "mp3 download popup":
                    self.parentID = -1
                    downloadPopup = WindowsDownloadPopup(self, -1, -1)
                    downloadPopup.ShowModal()
                    globalTracker.RESPONSECODE.responseLogBuffer = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (str(RESPONSECODE.flowSeq) , "\t" , "-1" , "\t" , "-1" , "\t" , "" , "\t" , "" , "\t" , "" , "\t" , downloadPopup.getDialogID() , "\t" , downloadPopup.getDialogTag() , "\t" , RESPONSECODE.currentResponse , "\t" , RESPONSECODE.currentResponseCode, "\t" , RESPONSECODE.previousResponse, "\t" , RESPONSECODE.previousResponseCode, "\t" , startTime, "\t" , (time.strftime("%H:%M:%S", time.localtime())), "\t", CONSTANTS.date_today, "\n")
                    RESPONSECODE.SNo += 1
                    self.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo) + "\t" + globalTracker.RESPONSECODE.responseLogBuffer)
                    self.initiate()
                elif flow == "ipad-scam":
                    self.QAbtnQ_Submit.Hide()
                    self.parentID = -1
                    ipadScam = FlashiPadScheme(self, -1, -1)
                    ipadScam.ShowModal()
                    globalTracker.RESPONSECODE.responseLogBuffer = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (str(RESPONSECODE.flowSeq) , "\t" , "-1" , "\t" , "-1" , "\t" , "" , "\t" , "" , "\t" , "" , "\t" , ipadScam.getDialogID() , "\t" , ipadScam.getDialogTag() , "\t" , RESPONSECODE.currentResponse , "\t" , RESPONSECODE.currentResponseCode, "\t" , RESPONSECODE.previousResponse, "\t" , RESPONSECODE.previousResponseCode, "\t" , startTime, "\t" , (time.strftime("%H:%M:%S", time.localtime())), "\t", CONSTANTS.date_today, "\n")
                    RESPONSECODE.SNo += 1
                    self.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo) + "\t" + globalTracker.RESPONSECODE.responseLogBuffer)
                    self.initiate()
                elif flow == "virus-alert":
                    self.QAbtnQ_Submit.Hide()
                    self.parentID = -1
                    RESPONSECODE.individualResponse = ""
                    RESPONSECODE.individualResponseCode = ""
                    self.virusAlertDialog = windowsVirusAlertDialog(self)
                    self.virusAlertDialog.ShowModal()
                    globalTracker.RESPONSECODE.responseLogBuffer = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (str(RESPONSECODE.flowSeq) , "\t" , "-1" , "\t" , "-1" , "\t" , "" , "\t" , "" , "\t" , "" , "\t" , self.virusAlertDialog.getDialogID() , "\t" , self.virusAlertDialog.getDialogTag() , "\t" , RESPONSECODE.currentResponse , "\t" , RESPONSECODE.currentResponseCode, "\t" , RESPONSECODE.previousResponse, "\t" , RESPONSECODE.previousResponseCode, "\t" , startTime, "\t" , (time.strftime("%H:%M:%S", time.localtime())), "\t", CONSTANTS.date_today, "\n")
                    RESPONSECODE.SNo += 1
                    self.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo) + "\t" + globalTracker.RESPONSECODE.responseLogBuffer)
                    if len(RESPONSECODE.individualResponse) > 0:
                        globalTracker.RESPONSECODE.responseLogBuffer = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (str(RESPONSECODE.flowSeq) , "\t" , "-1" , "\t" , self.virusAlertDialog.getDialogID() , "\t" , "" , "\t" , "" , "\t" , "" , "\t" , self.virusAlertDialog.getDialogID() , "\t" , self.virusAlertDialog.getDialogTag() , "\t" , RESPONSECODE.individualResponse , "\n")
                        RESPONSECODE.SNo += 1
                        self.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo) + "\t" + globalTracker.RESPONSECODE.responseLogBuffer)
                    self.initiate()
                elif flow == "w2":
                    self.initiate()
                else:
                    print "ERROR: unknown flow desired"
                    self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"ERROR: unknown flow desired/n")
                    
        else:
            print "DESTROYING THE APPLICATION AFTER COMPLETING ALL MATHS QUESTION"  
            self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"DESTROYING THE APPLICATION AFTER COMPLETING ALL MATHS QUESTION/n"  )
            self.currentInstructionPojo = self.utils.getMessagePojoByID("100007")
            self.middleMsg.Clear()
            if not self.currentInstructionPojo == None and self.currentInstructionPojo.getID() != "000000":
                self.middleMsg.AppendText(self.currentInstructionPojo.getMsg()) 
                self.emailFrame.finalClose()
                self.instructionIndex += 1
                self.interactivePnl.Hide()
                self.instructionPnl.SetSizer(self.msgSizer)
                self.instructionPnl.SetBackgroundColour("white")
                self.ShowInstructionPnl()
                self.instructionPnl.Show()               
                self.Layout()    
    firstEmail = True
    firstMathQA = True  
    
    def initiateEmail(self):
        if self.emailFrame == None:
            self.emailFrame = emailMainFrame(parent=self.interactivePnl, id=3, title="Department: Accounting email", pos=self.emailFramePos, size=self.emailFrameSize, style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT, emailFileLocation=os.path.abspath(globalTracker.propertyVar.emailMsgFilePath))
            self.emailFrame.SetMaxSize(self.emailFrameSize)
            self.emailFrame.SetPosition(self.emailFramePos)
            self.emailFrame.Show()
                
    def startDotProbeReal(self):
        self.showdotProbeImagePnl()
        self.updateDotProbeRealImages()
                            
    def startDotProbeTraining(self):
        self.ShowDotProbeTrainingPnl()
        self.updateTrainingImages()
        
    def startWordProbeTraining(self):
        self.ShowWordProbeTrainingPnl()
        self.updateWordProbeTrainingTextCtrlPnl()
    
    def startWordProbeReal(self):
        self.ShowWordProbeRealPnl()
        self.updateWordProbeReal()
        
    def updateTrainingImages(self): 
        self.SetFocus()
        if (self.trainIndex < self.utils.DPPojoList[0].getLength()):
            self.showTrainingFixation()
            wx.CallLater(int(globalTracker.propertyVar.fixationShowInterval), self.showTrainingImages) 
        else:
            self.stateInPhase += 1
            self.instructionIndex = 0
            
    def updateDotProbeRealImages(self):
        self.SetFocus()
        if self.dotProbeImgIndex < self.utils.DPPojoList[self.currentBlockNumnber].getLength():
            self.showDotProbeRealFixation()
            wx.CallLater(int(globalTracker.propertyVar.fixationShowInterval), self.showDotProbeRealImages)
        else:
            self.stateInPhase += 1
            self.dotProbeImgIndex = 0
            self.instructionIndex = 0
            
    def updateWordProbeTrainingTextCtrlPnl(self):
        self.SetFocus()
        if (self.trainWPIndex < self.utils.WPPojoList[self.currentBlockNumnber].getLength()):
            self.showWordProbeTrainingFixation()
            wx.CallLater(int(500), self.showWordsForWPTraining)
        else:
            self.stateInPhase += 1
            self.instructionIndex = 0
            
    def updateWordProbeReal(self):
        self.SetFocus()
        if self.wordProbeIndex < self.utils.WPPojoList[self.currentBlockNumnber].getLength():
            self.showWordProbeFixation()
            wx.CallLater(int(500), self.showWordsForWPReal)
        else:
            self.stateInPhase += 1
            self.wordProbeIndex = 0
            self.instructionIndex = 0
                            
    def showTrainingImages(self):
        # #write for fixation
        self.fixationTimerEnd = time.clock()
        self.fixationTrack = str(self.serialNum_DP) + "\t" + self.todayDat + "\t" + str(globalVar.subjectId) + "\t" + REPORT.TRIALCODE[FIXATION_INTRIALCODE] + "\t" + str(self.currentBlockNumnber) + "\t"+str(self.trainIndex)+"\t" + "\t\t" + globalTracker.propertyVar.fixationShowInterval + "\t" + REPORT.TRIALCODE[NONSENSE_INTRIALCODE] + "\t" + str(self.fixationTimerEnd - self.fixationTimerStart) + "\n"  # latency
        self.serialNum_DP += 1
        self.utils.write(globalTracker.propertyVar.imageDotProbeResult, self.fixationTrack)
        self.DPtrainingRedCrossPanel.Hide()
        if (self.trainIndex < self.utils.DPPojoList[0].getLength()):
            imagestrup = globalTracker.propertyVar.dotProbeImagePath + self.utils.DPPojoList[0].getUpImageList()[self.trainIndex]
            imagestrDown = globalTracker.propertyVar.dotProbeImagePath + self.utils.DPPojoList[0].getDowmImageList()[self.trainIndex]
            imageup = wx.Image(imagestrup, type=wx.BITMAP_TYPE_ANY)
            imagedown = wx.Image(imagestrDown, type=wx.BITMAP_TYPE_ANY)
            self.trainingUpImageBit.SetBitmap(wx.BitmapFromImage(imageup))
            self.trainingDownImageBit.SetBitmap(wx.BitmapFromImage(imagedown))
            self.trainingUpImageBit.Refresh()
            self.trainingDownImageBit.Refresh() 
            self.Fit()
            self.Layout()
            self.imageTimerStart = time.clock()
            wx.FutureCall(int(globalTracker.propertyVar.dotProbeUpDownImageShowInterval), self.showUpDownProbeForTrain)
            
    def showDotProbeRealImages(self):        
        self.fixationTimerEnd = time.clock()
        self.fixationTrack = str(self.serialNum_DP) + "\t" + self.todayDat + "\t" + str(globalVar.subjectId) + "\t" + REPORT.TRIALCODE[FIXATION_INTRIALCODE] + "\t" + str(self.currentBlockNumnber) + "\t"+str(self.dotProbeImgIndex)+"\t" + "\t\t" + globalTracker.propertyVar.fixationShowInterval + "\t" + REPORT.TRIALCODE[NONSENSE_INTRIALCODE] + "\t" + str(self.fixationTimerEnd - self.fixationTimerStart) + "\n"
        self.serialNum_DP += 1
        self.utils.write(globalTracker.propertyVar.imageDotProbeResult, self.fixationTrack)        
        self.dotProbeFixationPanel.Hide()
        if self.dotProbeImgIndex < self.utils.DPPojoList[self.currentBlockNumnber].getLength():
            imagestrUp = globalTracker.propertyVar.dotProbeImagePath + self.utils.DPPojoList[self.currentBlockNumnber].getUpImageList()[self.dotProbeImgIndex]
            imagestrDown = globalTracker.propertyVar.dotProbeImagePath + self.utils.DPPojoList[self.currentBlockNumnber].getDowmImageList()[self.dotProbeImgIndex]
            imageUp = wx.Image(imagestrUp, type=wx.BITMAP_TYPE_ANY) 
            imageDown = wx.Image(imagestrDown, type=wx.BITMAP_TYPE_ANY)
            self.dotProbeUpImageBit.SetBitmap(wx.BitmapFromImage(imageUp))
            self.dotProbeDownImageBit.SetBitmap(wx.BitmapFromImage(imageDown))
            self.dotProbeUpPanel.Refresh()
            self.dotProbeDownPanel.Refresh()
            self.Fit()
            self.Layout()
            self.utils.write(globalTracker.propertyVar.eventLog, "showing both images on dot probe image\n\tup dot probe Image: " + imagestrUp + "\n\t down dot probe image : " + imagestrDown + "\n")
            self.imageTimerStart = time.clock()
            wx.CallLater(int(globalTracker.propertyVar.dotProbeUpDownImageShowInterval), self.showUpDownProbe)            
        
    def showWordsForWPTraining(self):
        self.WPWordUPLen = 0
        self.WPWordDOWNLen = 0
        self.WPTrainingFixationTextCtrl.Hide()
        self.WPTrainingFixation1TextCtrl.Hide()
        self.WpTrainFixationPanel.Hide()
        if self.trainWPIndex < self.utils.WPPojoList[0].getLength():
            ThreatWList = self.utils.WPPojoList[0].getThreatWordList()
            NeutralWList = self.utils.WPPojoList[0].getNeutralWordList()
            threatWord = ThreatWList[self.trainWPIndex].strip()
            neutralWord = NeutralWList[self.trainWPIndex].strip()
            UPWord = ""
            DOWNWord = ""
            self.UP = ""
            self.DOWN = ""
#             if random.randint(0, 1) == 0:  # threat in UP Position
            i = self.defineThreatPositionIndexForTrial()
            if threatpositionWPTrial[i] == 1:  # threat in UP Position
                UPWord = threatWord
                DOWNWord = neutralWord
                self.UP = "THREAT"
                self.DOWN = "NEUTRAL"
            elif threatpositionWPTrial[i] == 0:
                UPWord = neutralWord
                DOWNWord = threatWord
                self.UP = "NEUTRAL"
                self.DOWN = "THREAT"
            self.WPTrainingUpTextCtrl.SetValue(UPWord)
            self.WPWordUPLen = len(UPWord)
            self.WPTrainingDownTextCtrl.SetValue(DOWNWord)
            self.WPWordDOWNLen = len(DOWNWord)
            self.WPTrainingDownTextCtrl.Show()
            self.WPTrainingDownPanel.Show()
            self.WPTrainingUpTextCtrl.Show()
            self.WPTrainingUpPanel.Show()
            self.WPReport += threatWord + "\t" + neutralWord + "\t" + str(threatpositionWPTrial[i]) + "\t"  # report trialNum,threat word and neutral word and if threat is in UP position
            wx.CallLater(int(500), self.showWProbeForTrain)

    from sets import Set
    threatpositionWPSet = Set()
    probetypeWPSet = Set()
    threatpositionWPTrialSet = Set()
    probeTypeWPTrialSet = Set()
               
    def defineThreatPositionIndexForTrial(self):
        foundIndex = False
        while(foundIndex == False):
            index = random.randint(0, self.threatpositionTrialLen)
            if not index in self.threatpositionWPTrialSet:
                foundIndex = True
                self.threatpositionWPTrialSet.add(index)
                return index
            else:
                foundIndex = False
            
    def defineThreatPositionIndexForReal(self):
        foundIndex = False
        while(foundIndex == False):
            index = random.randint(0, self.threatpositionLen)
            if not index in self.threatpositionWPSet:
                foundIndex = True
                self.threatpositionWPSet.add(index)
                return index
            else:
                foundIndex = False
                
    def defineProbeTypeIndexForTrial(self):
        foundProbeIndex = False
        while(foundProbeIndex == False):
            index = random.randint(0, self.probeTypeTrialLen)  
            if not index in self.probeTypeWPTrialSet:
                foundProbeIndex = True
                self.probeTypeWPTrialSet.add(index)
                return index
            else:
                foundProbeIndex = False
           
    def defineprobeTypeIndexForReal(self):
        foundProbeIndex = False
        while(foundProbeIndex == False):
            index = random.randint(0, self.probeTypeLen)  
            if not index in self.probetypeWPSet:
                foundProbeIndex = True
                self.probetypeWPSet.add(index)
                return index
            else:
                foundProbeIndex = False
            
    def showWordsForWPReal(self):
        self.WPWordUPLen = 0
        self.WPWordDOWNLen = 0
        self.wordProbeFixationTextCtrl.Hide()
        self.wordProbeFixationPanel.Hide()
        if self.wordProbeIndex < self.utils.WPPojoList[self.currentBlockNumnber].getLength():
            ThreatWList = self.utils.WPPojoList[self.currentBlockNumnber].getThreatWordList()
            NeutralWList = self.utils.WPPojoList[self.currentBlockNumnber].getNeutralWordList()
            threatWord = ThreatWList[self.wordProbeIndex].strip()
            neutralWord = NeutralWList[self.wordProbeIndex].strip()
            UPWord = ""
            DOWNWord = ""
#             if random.randint(0, 1) == 0:  # threat in UP Position
            i = self.defineThreatPositionIndexForReal()
            if threatpositionWP[i] == 1:  # if value of threat position=1,threat in UP Position
                UPWord = threatWord
                DOWNWord = neutralWord
            elif threatpositionWP[i] == 0:
                UPWord = neutralWord
                DOWNWord = threatWord
            self.wordProbeUpTextCtrl.SetValue(UPWord)
            self.wordProbeDownTextCtrl.SetValue(DOWNWord)
            self.WPWordUPLen = len(UPWord)
            self.WPWordDOWNLen = len(DOWNWord)
            self.wordProbeUpTextCtrl.Show()
            self.wordProbeDownTextCtrl.Show()
            self.wordProbeUpPanel.Show()
            self.wordProbeDownPanel.Show()
#             self.WPReport += threatWord + "\t" + neutralWord + "\t"  # report trialNum,threat word and neutral word
            self.WPReport += threatWord + "\t" + neutralWord + "\t" + str(threatpositionWP[i]) + "\t"  # report trialNum,threat word and neutral word
            wx.CallLater(int(500), self.showWProbeForWPReal)
            
    def showWProbeForWPReal(self):
        self.probe = ""     
        self.Bind(wx.EVT_KEY_UP, self.onChar)
        self.Bind(wx.EVT_SET_FOCUS, self.onFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)
        # here we are not c0ncerned about whether the probe appears at the Up or the DOWN position ;rather we are concerned about what type of probe appears by default "<" or ">", say them as LEFT and RIGHT probe;so self.probeposn will hold whether the probe is a LEFT_PROBE or a RIGHT_PROBE
#         self.probeposn = random.randint(0, 1)
        # if self.probeposn==0, then it is LEFT_PROBE else RIGHT_PROBE
        self.probetypeIndex = self.defineprobeTypeIndexForReal()
        self.probeTypeIndicator = probetypeWP[self.probetypeIndex] - 1  # defines 1 or 2
        # if self.probeTypeIndicator==0, then it is LEFT_PROBE else RIGHT_PROBE
        if random.randint(0, 1) == 0:  # Probe in UP position
            self.createProbeToReplaceWord(self.WPWordUPLen)
            self.wordProbeUpTextCtrl.SetValue(self.probe)
            self.wordProbeDownTextCtrl.SetValue("")
            if self.UP == "THREAT":  # PITP
                self.WPReport += str(REPORT.VALUES_PROBEPOSITION[REPORT.CASE_PITP]) + "\t" + WORD_PROBE[self.probeTypeIndicator] + "\t"  # 1 and id self.probeTypeIndicator==0, "<" else ">"
                self.WPReport = self.WPReport.replace('[XXX]', REPORT.TRIALCODE_WP[REPORT.CASE_PITP])
            else:  # PINP
                self.WPReport += str(REPORT.VALUES_PROBEPOSITION[REPORT.CASE_PINP]) + "\t" + WORD_PROBE[self.probeTypeIndicator] + "\t"  # 0 and id self.probeTypeIndicator==0, "<" else ">"
                self.WPReport = self.WPReport.replace('[XXX]', REPORT.TRIALCODE_WP[REPORT.CASE_PINP])
        else:  # probe in DOWN position
            self.createProbeToReplaceWord(self.WPWordDOWNLen)
            self.wordProbeUpTextCtrl.SetValue("")
            self.wordProbeDownTextCtrl.SetValue(self.probe)
            if self.DOWN == "THREAT":  # PITP
                self.WPReport += str(REPORT.VALUES_PROBEPOSITION[REPORT.CASE_PITP]) + "\t" + WORD_PROBE[self.probeTypeIndicator] + "\t"  # 1 and id self.probeTypeIndicator==0, "<" else ">"
                self.WPReport = self.WPReport.replace('[XXX]', REPORT.TRIALCODE_WP[REPORT.CASE_PITP])
            else:  # PINP 
                self.WPReport += str(REPORT.VALUES_PROBEPOSITION[REPORT.CASE_PINP]) + "\t" + WORD_PROBE[self.probeTypeIndicator] + "\t"  # 0 and id self.probeTypeIndicator==0, "<" else ">"
                self.WPReport = self.WPReport.replace('[XXX]', REPORT.TRIALCODE_WP[REPORT.CASE_PINP])
        self.trialNum += 1 
        self.serialNum_WP += 1
        self.wordProbeUpTextCtrl.Show()
        self.wordProbeFixationTextCtrl.Hide()
        self.wordProbeFixationPanel.Hide()
        self.wordProbeDownTextCtrl.Show()
        self.wordProbeIndex += 1
        if self.wordProbeIndex >= self.utils.WPPojoList[self.currentBlockNumnber].getLength():
            self.wordProbeIndex = 0
            self.stateInPhase += 1
            self.instructionIndex = 0
        self.SetFocus()
#         is this the extra half second??
        wx.CallLater(int(500), self.AcceptCharOnProbe)
             
    def showWProbeForTrain(self):
        self.probe = ""
        self.WPFixationError = False
        self.Bind(wx.EVT_KEY_UP, self.onChar)
        self.Bind(wx.EVT_SET_FOCUS, self.onFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)
        # here we are not c0ncerned about whether the probe appears at the Up or the DOWN position ;rather we are concerned about what type of probe appears by default "<" or ">", say them as LEFT and RIGHT probe;so self.probeposn will hold whether the probe is a LEFT_PROBE or a RIGHT_PROBE
#         self.probeposn = random.randint(0, 1)
        # if self.probeposn==0, then it is LEFT_PROBE else RIGHT_PROBE
        self.probetypeIndex = self.defineProbeTypeIndexForTrial()
        self.probeTypeIndicator = probeTypeWPTrial[self.probetypeIndex] - 1  # defines 1 or 2
        # if self.probeTypeIndicator==0, then it is LEFT_PROBE else RIGHT_PROBE
        if random.randint(0, 1) == 0:  # Probe in UP position
            self.createProbeToReplaceWord(self.WPWordUPLen)
            self.WPTrainingUpTextCtrl.SetValue(self.probe)
            self.WPTrainingDownTextCtrl.SetValue("")
            if self.UP == "THREAT":  # PITP
                self.WPReport += str(REPORT.VALUES_PROBEPOSITION[REPORT.CASE_PITP]) + "\t" + WORD_PROBE[self.probeTypeIndicator] + "\t"  # 1 and id self.probeTypeIndicator==0, "<" else ">"
            else:  # PINP
                self.WPReport += str(REPORT.VALUES_PROBEPOSITION[REPORT.CASE_PINP]) + "\t" + WORD_PROBE[self.probeTypeIndicator] + "\t"  # 0 and id self.probeTypeIndicator==0, "<" else ">"
        else:  # probe in DOWN position
            self.createProbeToReplaceWord(self.WPWordDOWNLen)
            self.WPTrainingUpTextCtrl.SetValue("")
            self.WPTrainingDownTextCtrl.SetValue(self.probe)
            if self.DOWN == "THREAT":  # PITP
                self.WPReport += str(REPORT.VALUES_PROBEPOSITION[REPORT.CASE_PITP]) + "\t" + WORD_PROBE[self.probeTypeIndicator] + "\t"  # 1 and id self.probeTypeIndicator==0, "<" else ">"
            else:  # PINP 
                self.WPReport += str(REPORT.VALUES_PROBEPOSITION[REPORT.CASE_PINP]) + "\t" + WORD_PROBE[self.probeTypeIndicator] + "\t"  # 0 and id self.probeTypeIndicator==0, "<" else ">"
        self.trialNum += 1   
        self.serialNum_WP += 1           
        self.WPTrainingUpTextCtrl.Show()
        self.WpTrainFixationPanel.Hide()
        self.WPTrainingDownTextCtrl.Show()
        self.WPTrainingDownPanel.Show()
        self.WPTrainingUpPanel.Show()
        self.trainWPIndex += 1
        if (self.trainWPIndex) >= self.utils.WPPojoList[0].getLength():
            self.trainWPIndex = 0
#             self.serialNum_WP = 0
            self.stateInPhase += 1
            self.instructionIndex = 0
        self.SetFocus()
        wx.CallLater(int(500), self.AcceptCharOnProbe)
        
    def AcceptCharOnProbe(self):
        MainFrame.acceptChar = True
        # initialte the time start countdown for the probe here and then 
        self.WPProbeTimerStart = time.clock()
        self.SetFocus()
     
    def createProbeToReplaceWord(self, wordCharLength):   
        # inorder to make probe occupy one of the space of the character at postion probeCharPosition of the previously shown word, we need to pad spaces at the front and at the end of the probe so that 
        # it can appear at the designated random character position of one of the character of the word
        probeCharPosition = random.randint(1, wordCharLength)
        for i in range(1, wordCharLength + 1):
            if i == probeCharPosition:
                self.probe += WORD_PROBE[self.probeTypeIndicator]
            else:
                self.probe += PAD_CHAR
  
    def showUpDownProbeForTrain(self):
        self.imageTimerEnd = time.clock()
        self.imageTrack = str(self.serialNum_DP) + "\t" + self.todayDat + "\t" + str(globalVar.subjectId) + "\t" + REPORT.TRIALCODE[PRACTISEIMAGE_INTRIALCODE] + "\t" + str(self.currentBlockNumnber) + "\t" + str(self.trainIndex) + "\t" + self.utils.DPPojoList[0].getUpImageType()[self.trainIndex] + "\t" + self.utils.DPPojoList[0].getDownImageType()[self.trainIndex] + "\t" + globalTracker.propertyVar.dotProbeUpDownImageShowInterval + "\t" + REPORT.TRIALCODE[NONSENSE_INTRIALCODE] + "\t" + str(self.imageTimerEnd - self.imageTimerStart) + "\n"  # latency
        self.serialNum_DP += 1
        self.utils.write(globalTracker.propertyVar.imageDotProbeResult, self.imageTrack)
        self.Bind(wx.EVT_KEY_UP, self.onChar)
        self.Bind(wx.EVT_SET_FOCUS, self.onFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)
        self.probeType = -3478
        if self.utils.DPPojoList[0].getProbePosnList()[self.trainIndex].upper() == utils.PROBE_UP:
            self.trainingUpImageBit.SetBitmap(wx.BitmapFromImage(self.imageProbe))
            self.probeType = 0
            self.trainingDownImageBit.SetBitmap(wx.BitmapFromImage(self.imageDotProbeWhite))
        else:
            self.trainingUpImageBit.SetBitmap(wx.BitmapFromImage(self.imageDotProbeWhite))
            self.trainingDownImageBit.SetBitmap(wx.BitmapFromImage(self.imageProbe))
            self.probeType = 1
        self.DPtrainingUpPanel.Refresh()
        self.DPtrainingDownPanel.Refresh()
        self.trainIndex += 1
        self.probeTimerStart = time.clock()
        if (self.trainIndex) >= self.utils.DPPojoList[0].getLength():
#             self.trainIndex = 0
            self.stateInPhase += 1
            self.instructionIndex = 0

        self.tempInitiationNumber = self.initiationNumber
        self.callNum = self.initiationNumber
        MainFrame.acceptChar = False
        print "acceptchar =False"
        self.utils.write(globalTracker.propertyVar.diagnosisDPLog, "acceptchar =False/n")
        wx.CallLater(int(500), self.AcceptCharOnProbeDP)
        #on 5000 idle response time
        self.inactivity = wx.FutureCall(int(globalTracker.propertyVar.idleResponseTime), self.checkForInactivity)
        self.SetFocus()
        
    def AcceptCharOnProbeDP(self):
        print "after 500 sec, acceptchar =True"
        self.utils.write(globalTracker.propertyVar.diagnosisDPLog, "after 500 sec, acceptchar =True/n")
        MainFrame.acceptChar = True
        self.probeTimerStart = time.clock()
        
    def showUpDownProbe(self):
        self.imageTimerEnd = time.clock()
        self.imageTrack = str(self.serialNum_DP) + "\t" + self.todayDat + "\t" + str(globalVar.subjectId) + "\t" + REPORT.TRIALCODE[TRAILIMAGE_INTRIALCODE] + "\t" + str(self.currentBlockNumnber) + "\t" + str(self.dotProbeImgIndex) + "\t" + self.utils.DPPojoList[self.currentBlockNumnber].getUpImageType()[self.dotProbeImgIndex] + "\t" + self.utils.DPPojoList[self.currentBlockNumnber].getDownImageType()[self.dotProbeImgIndex] + "\t" + globalTracker.propertyVar.dotProbeUpDownImageShowInterval + "\t" + REPORT.TRIALCODE[NONSENSE_INTRIALCODE] + "\t" + str(self.imageTimerEnd - self.imageTimerStart) + "\n"  # latency
        self.serialNum_DP += 1
        self.utils.write(globalTracker.propertyVar.imageDotProbeResult, self.imageTrack)
        # bind here
        # TODO: instead bind to key_UP because for longer key presses there can be multiple keystroke DOWn event coming but a single key stroke UP event 
        self.Bind(wx.EVT_KEY_UP, self.onChar)
        self.Bind(wx.EVT_SET_FOCUS, self.onFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)
        self.probeType = -3478
        if self.utils.DPPojoList[self.currentBlockNumnber].getProbePosnList()[self.dotProbeImgIndex].upper() == utils.PROBE_UP:
            self.probeType = 0
            self.dotProbeUpImageBit.SetBitmap(wx.BitmapFromImage(self.imageProbe))
            self.dotProbeDownImageBit.SetBitmap(wx.BitmapFromImage(self.imageDotProbeWhite))
            self.utils.write(globalTracker.propertyVar.eventLog, "replace by dot on upper dot probe image\n")
        else:
            self.probeType = 1
            self.dotProbeUpImageBit.SetBitmap(wx.BitmapFromImage(self.imageDotProbeWhite))
            self.dotProbeDownImageBit.SetBitmap(wx.BitmapFromImage(self.imageProbe))
            self.utils.write(globalTracker.propertyVar.eventLog, "replace by dot on down dot probe image\n")
        self.dotProbeUpPanel.Refresh()
        self.dotProbeDownPanel.Refresh() 
        self.dotProbeImgIndex += 1
        self.phaseIndex=self.dotProbeImgIndex
        self.probeTimerStart = time.clock()
        if (self.dotProbeImgIndex) >= self.utils.DPPojoList[self.currentBlockNumnber].getLength():
            self.dotProbeImgIndex = 0
            self.stateInPhase += 1
            self.instructionIndex = 0
        self.tempInitiationNumber = self.initiationNumber
        #   TODO:change this 5sec thing to variable
        self.callNum = self.initiationNumber
        wx.CallLater(int(500), self.AcceptCharOnProbeDP)
        self.inactivity = wx.FutureCall(int(globalTracker.propertyVar.idleResponseTime), self.checkForInactivity)
        self.SetFocus()
        
    def checkForInactivity(self):
        # if control reaches here acceot char has already been true for the corresponding cycle so we need to make acceptchar=false so that it can avoid call to next cycle if it has not passed through the 500ms pause of probe part of that cycle
        self.inactivitylocalTime = time.clock()
        self.inactivity.Stop()
        if self.tempInitiationNumber < self.initiationNumber:
            print "went ahead"
            self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"went ahead/n")
        elif self.tempInitiationNumber == self.initiationNumber:
            MainFrame.acceptChar = False
            self.prevResponseTime = self.currentResponseTime
            self.currentResponseTime = time.clock()
            self.prevResponse = self.currentResponse
            self.currentResponse = IDLE_response
            print "5 sec delay"
            print "5sec====> prevresponsetime= " + str(self.prevResponseTime) + "\t prevResponse= " + self.prevResponse + "\tcurrentResponseTime= " + str(self.currentResponseTime) + "\t currentResponse= " + self.currentResponse
            self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"5 sec delay")
            self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"5sec====> prevresponsetime= " + str(self.prevResponseTime) + "\t prevResponse= " + self.prevResponse + "\tcurrentResponseTime= " + str(self.currentResponseTime) + "\t currentResponse= " + self.currentResponse+"\n")
            self.utils.write(globalTracker.propertyVar.eventLog, "+++++++++++++++++++++++++++++++ ideal for 5 sec\n")
            print "diff= " + str(abs(self.currentResponseTime - self.prevResponseTime))
            self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"diff= " + str(abs(self.currentResponseTime - self.prevResponseTime))+"\n")
            MainFrame.isRun = False
            if ((self.prevResponse == IDLE_response and self.currentResponse == IDLE_response) and (abs(self.currentResponseTime - self.prevResponseTime) >= highDiff)) or ((self.prevResponse == CHAR_response and self.currentResponse == CHAR_response) and (abs(self.currentResponseTime - self.prevResponseTime) >= lowDiff)) or ((self.prevResponse == IDLE_response and self.currentResponse == CHAR_response) and (abs(self.currentResponseTime - self.prevResponseTime) >= lowDiff)) or ((self.prevResponse == CHAR_response and self.currentResponse == IDLE_response) and (abs(self.currentResponseTime - self.prevResponseTime) >= highDiff)):
                MainFrame.isRun = True
            elif (self.currentPhase == "DOT PROBE TRAINING PHASE" and self.trainIndex == 1) or (self.currentPhase == "DOT PROBE PHASE" and self.dotProbeImgIndex == 1):
                MainFrame.isRun = True
            if MainFrame.isRun:
                print "after 5 sec idleness======>diff is greater than " + str(self.checkForDuality)
                self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"after 5 sec idleness======>diff is greater than " + str(self.checkForDuality)+"\n")
                if self.currentPhase == "DOT PROBE TRAINING PHASE":
                    self.showTraningWhite()
                    time.sleep(2)
                elif self.currentPhase == "DOT PROBE PHASE":
                    self.showDotProbeRealWhite()
                    time.sleep(2)
                self.probeTrack = ""
                self.probeTimerEnd = time.clock()
                if self.probeType >= 0:
                    if self.probeType == 0:
                        probePosn = UP_PROBE_INTRIALCODE
                    elif self.probeType == 1:
                        probePosn = dOWN_PROBE_INTRIALCODE
                if self.currentPhase == "DOT PROBE TRAINING PHASE":
                    self.probeTrack = str(self.serialNum_DP) + "\t" + self.todayDat + "\t" + str(globalVar.subjectId) + "\t" + REPORT.TRIALCODE[probePosn] + "\t" + str(self.currentBlockNumnber) + "\t"+str(self.trainIndex-1)+"\t" + "\t\t" + globalTracker.propertyVar.dotShowInterval + "\t" + REPORT.TRIALCODE[INCORRECT_RESPONSE_INTRIALCODE] + "\t" + str(self.probeTimerEnd - self.probeTimerStart) + "\t" + str(abs(self.onCharlocalTime - self.inactivitylocalTime)) + "\n"  # latency
                elif self.currentPhase == "DOT PROBE PHASE":
                    self.probeTrack = str(self.serialNum_DP) + "\t" + self.todayDat + "\t" + str(globalVar.subjectId) + "\t" + REPORT.TRIALCODE[probePosn] + "\t" + str(self.currentBlockNumnber) + "\t"+str(self.phaseIndex-1)+"\t" + "\t\t" + globalTracker.propertyVar.dotShowInterval + "\t" + REPORT.TRIALCODE[INCORRECT_RESPONSE_INTRIALCODE] + "\t" + str(self.probeTimerEnd - self.probeTimerStart) + "\t" + str(abs(self.onCharlocalTime - self.inactivitylocalTime)) + "\n"  # latency
                self.serialNum_DP += 1
                self.utils.write(globalTracker.propertyVar.imageDotProbeResult, self.probeTrack)          
                self.initiate()
                      
    def showTrainingFixation(self):
        self.showTraningWhite()  
        self.DPtrainingRedCrossPanel.Show()   
        self.fixationTimerStart = time.clock()
        
    def showDotProbeRealFixation(self):
        self.showDotProbeRealWhite()
        self.dotProbeFixationPanel.Show()
        self.fixationTimerStart = time.clock()
        self.utils.write(globalTracker.propertyVar.eventLog, "showing fixation\n")
        
    def showWordProbeTrainingFixation(self):
        self.showWordProbeTrainingWhite()
        if self.WPFixationError:
            self.WPTrainingFixation1TextCtrl.Hide()
            self.WPTrainingFixationTextCtrl.Center()
            self.WPTrainingFixationTextCtrl.CenterOnParent()
            self.WPTrainingFixationTextCtrl.Show()
        else:
            self.WPTrainingFixationTextCtrl.Hide()
            self.WPTrainingFixation1TextCtrl.Center()
            self.WPTrainingFixation1TextCtrl.CenterOnParent()
            self.WPTrainingFixation1TextCtrl.Show()
        self.WpTrainFixationPanel.Show()
        
    def showWordProbeFixation(self):
        self.showWordProbeRealWhite()
        self.wordProbeFixationTextCtrl.Center()
        self.wordProbeFixationTextCtrl.CenterOnParent()
        self.wordProbeFixationTextCtrl.Show()
        self.wordProbeFixationPanel.Show()
                 
    def showTraningWhite(self):
        self.DPtrainingRedCrossPanel.Hide()
        self.trainingDownImageBit.SetBitmap(wx.BitmapFromImage(self.imageDotProbeWhite))
        self.trainingUpImageBit.SetBitmap(wx.BitmapFromImage(self.imageDotProbeWhite))
        self.trainingUpImageBit.Refresh()
        self.trainingDownImageBit.Refresh()   
        
    def showDotProbeRealWhite(self):
        self.dotProbeFixationPanel.Hide()
        self.dotProbeUpImageBit.SetBitmap(wx.BitmapFromImage(self.imageDotProbeWhite))
        self.dotProbeDownImageBit.SetBitmap(wx.BitmapFromImage(self.imageDotProbeWhite))
        self.dotProbeDownPanel.Refresh()
        self.dotProbeUpPanel.Refresh()
        self.utils.write(globalTracker.propertyVar.eventLog, "removed both images in dot probe image\n")
        
    def showWordProbeTrainingWhite(self):
        self.WPTrainingFixationTextCtrl.Hide()
        self.WPTrainingFixation1TextCtrl.Hide()
        self.WPTrainingUpTextCtrl.SetValue("")
        self.WPTrainingDownTextCtrl.SetValue("")
        self.WPTrainingUpTextCtrl.Hide()  
        self.WPTrainingDownTextCtrl.Hide()
        self.WPTrainingDownPanel.Hide()
        self.WPTrainingUpPanel.Hide()
        
    def showWordProbeRealWhite(self):
        self.wordProbeFixationTextCtrl.Hide()  
        self.wordProbeUpTextCtrl.Hide()
        self.wordProbeUpPanel.Hide()
        self.wordProbeDownTextCtrl.Hide()
        self.wordProbeDownPanel.Hide()
                            
    def isValidBlockNumber(self):
        if PHASE.phaseGuider[PHASE.phaseNumber] == "DOT PROBE TRAINING PHASE" or PHASE.phaseGuider[PHASE.phaseNumber] == "DOT PROBE PHASE":
            if self.currentBlockNumnber < len(self.utils.DPPojoList):
                return True
            return False
        elif PHASE.phaseGuider[PHASE.phaseNumber] == "WORD PROBE PRACTISE PHASE" or PHASE.phaseGuider[PHASE.phaseNumber] == "WORD PROBE PHASE":
            if self.currentBlockNumnber < len(self.utils.WPPojoList):
                return True
            return False
        elif PHASE.phaseGuider[PHASE.phaseNumber] == "INTERACTIVE ENVIRONMENT PHASE":
            return True
                      
    def getPostBlockInstructionList(self):
        if PHASE.phaseGuider[PHASE.phaseNumber] == "DOT PROBE TRAINING PHASE" or PHASE.phaseGuider[PHASE.phaseNumber] == "DOT PROBE PHASE":
            return self.utils.DPPojoList[self.currentBlockNumnber].getAfterBlockMsgList()
        elif PHASE.phaseGuider[PHASE.phaseNumber] == "WORD PROBE PRACTISE PHASE" or PHASE.phaseGuider[PHASE.phaseNumber] == "WORD PROBE PHASE":
            return self.utils.WPPojoList[self.currentBlockNumnber].getAfterBlockInstructionList()
        
    def getPreBlockInstructionList(self):
        if PHASE.phaseGuider[PHASE.phaseNumber] == "DOT PROBE TRAINING PHASE" or PHASE.phaseGuider[PHASE.phaseNumber] == "DOT PROBE PHASE":
            return self.utils.DPPojoList[self.currentBlockNumnber].getBeforeBlockmsgList()    
        elif PHASE.phaseGuider[PHASE.phaseNumber] == "WORD PROBE PRACTISE PHASE" or PHASE.phaseGuider[PHASE.phaseNumber] == "WORD PROBE PHASE":
            return self.utils.WPPojoList[self.currentBlockNumnber].getBeforeBlockInstructionList()
    
    def HideDotProbeTrainingPnl(self):
        self.dotProbeTrainingPnl.Hide()
        
    def HideWPTrainingPnl(self):
        self.WordProbeTrainingPnl.Hide()
        
    def ShowDotProbeTrainingPnl(self):
        self.instructionPnl.Hide()
        self.dotProbePnl.Hide()
        self.WordProbePnl.Hide()
        self.WordProbeTrainingPnl.Hide()
        self.dotProbeTrainingPnl.Show()
        self.Fit()
        self.Layout()
        self.dotProbeTrainingPnl.Fit()
        self.dotProbeTrainingPnl.Layout()
        self.trainingUDPnlSizer.Layout()
        
    def showdotProbeImagePnl(self):
        self.instructionPnl.Hide()
        self.dotProbeTrainingPnl.Hide()
        self.WordProbePnl.Hide()
        self.dotProbePnl.Show()
        self.dotProbePnl.Fit()
        self.dotProbePnl.Layout()
        self.dotProbeUDPnlSizer.Layout()
        
    def HideInstructionPnl(self):
        self.instructionPnl.Hide()
        
    def ShowInstructionPnl(self):
        self.middleMsg.SetFocus()
        self.middleMsg.Show()
        self.middleMsg.HideNativeCaret()        
        self.instructionPnl.Show()
        
    def ShowWordProbeTrainingPnl(self):
        self.instructionPnl.Hide()
        self.dotProbePnl.Hide()
        self.dotProbeTrainingPnl.Hide()
        self.WordProbePnl.Hide()
        self.WordProbeTrainingPnl.Show()
        self.Fit()
        self.Layout()
        self.WordProbeTrainingPnl.Fit()
        self.WordProbeTrainingPnl.Layout()
        self.WPTrainingUDPnlSizer.Layout()
        
    def ShowWordProbeRealPnl(self):
        self.instructionPnl.Hide()
        self.dotProbePnl.Hide()
        self.dotProbeTrainingPnl.Hide()
        self.WordProbeTrainingPnl.Hide()
        self.WordProbePnl.Show()
        self.Fit()
        self.Layout()
        self.WordProbePnl.Fit()
        self.WordProbePnl.Layout()
        self.wordProbeUDPnlSizer.Layout()
       
    def trackDotProbeError(self, clickNumber):
        if self.probeType >= 0:
            if self.probeType == clickNumber:
                self.correct = CORRECT_RESPONSE_INTRIALCODE
                self.utils.write(globalTracker.propertyVar.eventLog, "probe position= " + str(clickNumber) + "  correct=TRUE\n")
            else:
                self.correct = INCORRECT_RESPONSE_INTRIALCODE
                self.utils.write(globalTracker.propertyVar.eventLog, "probe position= " + str(clickNumber) + "  correct=FALSE\n")
        else:
            self.utils.write(globalTracker.propertyVar.eventLog, "probe number has not been initialized\n")
            self.utils.write(globalTracker.propertyVar.eventLog, "*******************************************************\n")
            self.utils.write(globalTracker.propertyVar.eventLog, "probeType for dot probe has not been initialized\n")
            self.utils.write(globalTracker.propertyVar.eventLog, "*******************************************************\n")    
     
    def trackWPTrainError(self, clickNumber):
        if self.probeTypeIndicator >= 0:
            if self.probeTypeIndicator == clickNumber:
                self.WPFixationError = False
                self.WPReport += str(REPORT.CORRECT_RESPONSE) + "\t"
            else:
                self.WPFixationError = True
                self.WPReport += str(REPORT.INCORRECT_RESPONSE) + "\t"
                
    def trackWPError (self, clickNumber):
        if self.probeTypeIndicator >= 0:
            if self.probeTypeIndicator == clickNumber:
                self.WPReport += str(REPORT.CORRECT_RESPONSE) + "\t"
            else:
                self.WPReport += str(REPORT.INCORRECT_RESPONSE) + "\t"
           
    def trackTrainingError(self, clickNumber):
        if self.probeType >= 0:
            if self.probeType == clickNumber:
                self.correct = CORRECT_RESPONSE_INTRIALCODE
                self.utils.write(globalTracker.propertyVar.eventLog, "probe position= " + str(clickNumber) + "  correct=TRUE\n")
                self.trainingredCrossImageBit = wx.StaticBitmap(self.DPtrainingRedCrossPanel, bitmap=self.tempFixation)
                self.trainingredCrossImageBit.Refresh()
            else:
                self.correct = INCORRECT_RESPONSE_INTRIALCODE
                self.utils.write(globalTracker.propertyVar.eventLog, "probe position= " + str(clickNumber) + "  correct=FALSE\n")
                self.trainingredCrossImageBit = wx.StaticBitmap(self.DPtrainingRedCrossPanel, bitmap=self.redFixation)
                self.DPtrainingRedCrossPanel.Show()    
        else:
            self.utils.write(globalTracker.propertyVar.eventLog, "arrowNumber has not been initialized\n")
            self.utils.write(globalTracker.propertyVar.eventLog, "*******************************************************\n")
            self.utils.write(globalTracker.propertyVar.eventLog, "probeType has not been initialized\n")
            self.utils.write(globalTracker.propertyVar.eventLog, "*******************************************************\n")
            
    def HideMouse(self):
        cursor = wx.StockCursor(wx.CURSOR_BLANK)
            # set the cursor for the window
        self.SetCursor(cursor)   
        
    def ShowMouse(self):
        cursor = wx.StockCursor(wx.CURSOR_ARROW)
        self.SetCursor(cursor) 
        
    def reportRemainingForWPTrain(self):
#         12 zeros
        for ii in range(1, 13):
            if ii == 12:
                zeros = str(0) + "\t"
            else:
                zeros = str(0) + "\n\r" 
        self.WPReport += zeros
        
#####################################################################################
############## *****MATHS  QUESTION  FUNCTIONS FOR RADIO BUTTON *****  ###########
#####################################################################################
   
    currentQAPojo = None
    
    def StartQARepeat(self):
        self.currentQAPojo = None
        # self.QAIndex represents the index of Maths QA
        if(self.QAIndex < len(self.mUtils.QAODict)):
            self.currentQAPojo = self.mUtils.QAODict[self.QAIndex]
            globalTracker.RESPONSECODE.responseLogBuffer = str(RESPONSECODE.flowSeq) + "\t" + str(self.MathsIndex) + "\t"
            self.createQueOptionView(self.currentQAPojo)
            # create an empty dictioanry holding status of all possible dialogs of a particular QA
            globalTracker.math.createEmptyQADictEntry(self.QAIndex)
            self.QAIndex += 1
            self.mathsStartTime = strftime("%H:%M:%S:%MS", time.localtime())
        else:
            print "DESTROYING APPLICATION"
            self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"DESTROYING APPLICATION\n")
            self.Destroy()
          
    def normalizeBeforeMakePaneContent(self):
        self.question.Hide()
        self.queOptionSizer.Remove(self.pane)
        self.queOptionSizer.Layout()
#        removing widgets from sizers
        for eachSizer in self.optionsizerInlist:
            self.RemoveAllChildren(eachSizer)
        self.RemoveAllChildren(self.queOptionSizer)
        self.OptionPnl.Layout()
        self.Layout()
        self.Refresh()
        
    firstLoadTrigger = False
    secondLoadTrigger = False
    thirdLoadTrigger = False
    fourthLoadTrigger = False
    fifthLoadTrigger = False
    sixthLoadTrigger = False
    # make a list of lists to validate the values user typed or choosed in qach QA so that user can be alerted 
    
    def  createQueOptionView(self, eachQAPojo):
        # for each QAPojo
        '''Just make a few controls to put on the collapsible pane'''
        if not eachQAPojo == None and isinstance(eachQAPojo, QAPojo):
            self.displayLoadIdentifier = -1
            self.QA = eachQAPojo.getQAList() 
            NumberQ = len(self.QA)
            self.optionsizerInlist = []
            indexQ = 0
            self.queOptionSizer = wx.BoxSizer(wx.VERTICAL)
            answerList = []
            answerListIndex = 0
            while (indexQ < NumberQ):
                self.pane = wx.Panel(self.OptionPnl, wx.ID_ANY, size=(self.QPnlWidht, -1), name="pane in option panel1111111111111", style=wx.ALL)
                self.pane.SetBackgroundColour("#F0F0F0")
                self.qeSizer = None
                self.qeSizer = wx.BoxSizer(wx.VERTICAL)
                if (not self.QA[indexQ] == None) and isinstance(self.QA[indexQ], eachQABlock):
                    labelQ = self.QA[indexQ].getQuestion()
                    self.question = None
                    self.question = wx.TextCtrl(self.pane, value=labelQ, style=wx.TE_CHARWRAP|wx.TE_MULTILINE|wx.NO_BORDER| wx.ALIGN_LEFT|wx.TE_READONLY|wx.ALL|wx.EXPAND)
                    self.question.SetBackgroundColour("White")
                    q_font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
                    self.question.SetFont(q_font)
                    self.question.Layout()
                    self.question.Refresh()
                    optType = self.QA[indexQ].getOptionType()
                    options = self.QA[indexQ].getOptions()
                    optionSizer = wx.BoxSizer(wx.VERTICAL)
                    FillIndex = 0
                    for eachOption in options:
                        box = wx.StaticBox(self.pane, -1, "")
                        if isinstance(eachOption, Option):
                            indexTextValue = 0
                            textList = eachOption.getText()
                            valueList = eachOption.getValue()
                            answer = eachOption.getAnswer()
                            sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
                            while(indexTextValue < len(textList)) :
                                onelineSizer = wx.BoxSizer(wx.HORIZONTAL) 
                                if optType in MATH.OPTION_TYPE and optType == MATH.OPTION_TYPE[1]:
                                    # radio button
                                    self.radioBox = None
                                    self.radioBox = wx.RadioBox(parent=self.pane, id=88, label="", choices=textList, majorDimension=1, style=wx.RA_SPECIFY_COLS)
                                    self.radioBox.Enable()
                                    self.radioBox.SetSelection(0)
                                    self.chooseIndex = 0 
                                    self.radioBox.Bind(wx.EVT_RADIOBOX, self.onChooseRadioButton, self.radioBox)
                                    onelineSizer.Add(self.radioBox, 0, 1)
                                    sizer.Add(onelineSizer, 0, 0)
                                    # index, optiontype,answer, user_answer
                                    answerList.append([answerListIndex, optType, answer, -1])
                                    answerListIndex += 1
                                    break
                                elif optType in MATH.OPTION_TYPE and optType == MATH.OPTION_TYPE[0]:
                                    # fill in 
                                    stext = wx.StaticText(self.pane)
                                    stext.SetLabel(textList[indexTextValue])
                                    stext2 = wx.StaticText(self.pane, -1)
                                    sText2_font = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
                                    stext2.SetFont(sText2_font)
                                    if len(valueList[indexTextValue].strip()) > 0:
                                        stext1 = wx.StaticText(self.pane, -1)
                                        stext1.SetLabel(valueList[indexTextValue])
                                    else:
                                        stext1 = wx.TextCtrl(self.pane, value="", validator=Int_Validator(), style=wx.EXPAND | wx.CENTER | wx.TE_WORDWRAP | wx.TE_PROCESS_TAB)
                                        stext1.SetEditable(True)
                                        stext1.SetMaxLength(10)
                                        stext1.SetMaxSize((200, -1))
                                        stext1.Bind(wx.EVT_CHAR, self.onMathsChar)
                                        answerList.append([answerListIndex, optType, answer, -1])
                                        answerListIndex += 1
                                        if FillIndex == 0:
                                            stext1.Bind(wx.EVT_TEXT, self.firstLoad)
                                            stext2.SetLabel("A");
                                            self.firstLoadTrigger = True
                                            stext1.SetFocus()
                                        elif FillIndex == 1:
                                            stext1.Bind(wx.EVT_TEXT, self.secondLoad)
                                            stext2.SetLabel("B");
                                            self.secondLoadTrigger = True
                                        elif FillIndex == 2:
                                            stext1.Bind(wx.EVT_TEXT, self.thirdLoad)
                                            stext2.SetLabel("C");
                                            self.thirdLoadTrigger = True
                                        elif FillIndex == 3:
                                            stext1.Bind(wx.EVT_TEXT, self.fourthLoad)
                                            stext2.SetLabel("D");
                                            self.fourthLoadTrigger = True
                                        elif FillIndex == 4:
                                            stext1.Bind(wx.EVT_TEXT, self.fifthLoad)
                                            self.fifthLoadTrigger = True
                                        elif FillIndex == 5:
                                            stext1.Bind(wx.EVT_TEXT, self.sixthLoad)
                                            self.sixthLoadTrigger = True
                                        FillIndex += 1
                                    onelineSizer.Add(stext, 0, wx.ALL, 2)
                                    onelineSizer.Add(stext1, 0, wx.ALL, 2)
                                    onelineSizer.Add(stext2, 0, wx.ALL, 2)
                                    stext1 = None
                                    sizer.Add(onelineSizer, 0, 1)
                                indexTextValue += 1
                        optionSizer.Add(sizer, 0, 1)
                self.qeSizer.Add((5, 1))
                self.pane.Layout()
                self.pane.Refresh()
                self.question.Layout()
                self.question.FitInside()
                self.question.SetBestFittingSize()
                if indexQ<1:
                    self.question.SetMaxSize((-1, 80))
                else:
                    self.question.SetMaxSize((-1,60))
                self.question.Refresh()
                self.qeSizer.Add(self.question, 0, wx.ALL | wx.EXPAND, 2)   
                self.qeSizer.Add((5, 1))
                self.qeSizer.Add(optionSizer, 0) 
                self.pane.SetSizer(self.qeSizer)
                self.pane.Fit()
#                 self.OptionPnl.SetAutoLayout(1)
#                 self.OptionPnl.SetupScrolling()
                self.optionsizerInlist.append(self.qeSizer)
                self.queOptionSizer.Add(self.pane, 0, wx.ALL|wx.EXPAND, 1)
                indexQ += 1
               
                self.OptionPnl.SetSizer(self.queOptionSizer)
                self.OptionPnl.Fit()
                self.OptionPnl.Layout()
                self.sizerItems = []
             
            self.QAPnl.SetAutoLayout(1)
            self.QAPnl.SetupScrolling()
            self.answerSouce[self.answerSouceIndex] = answerList
            self.answerSouceIndex += 1
            self.mathsLogBuffer = "1\t\t" + self.currentQAPojo.getMathsID() + "\t"
            
    def onMathsChar(self, event):   
        
        keycode = event.GetKeyCode()
        widget = event.GetEventObject()
        if wx.WXK_TAB == keycode:
            widget.Navigate()
        event.Skip()
        
    displayLoadIdentifier = -1 
               
    def displayLoad(self, loadIndex):
        # comes here when maths fields are hit active
        currentQAIndex = self.QAIndex - 1
        if currentQAIndex < len(self.mUtils.QAODict) and currentQAIndex < len(MATHASSOC_DIALOG.DIALOG_INFO) and loadIndex < len(MATHASSOC_DIALOG.DIALOG_INFO[currentQAIndex]):
            self.parentID = self.currentQAPojo.getMathsID()
            
            globalTracker.RESPONSECODE.responseLogBuffer = str(RESPONSECODE.flowSeq) + "\t" + str(self.MathsIndex) + "\t"
            globalTracker.RESPONSECODE.responseLogBuffer += self.parentID + "\t" + self.currentQAPojo.getMathsID() + "\t"
            thisLoad = MATHASSOC_DIALOG.DIALOG_INFO[currentQAIndex][loadIndex]
            startTime = time.strftime("%H:%M:%S", time.localtime())
            if isinstance(thisLoad, str):
                thisLoad = str(thisLoad.strip()).lower()
                if  thisLoad == "windowsupdate":
                    self.displayLoadIdentifier += 1
                    self.loadDialog = windowsUpdateDialog(self, self.displayLoadIdentifier, currentQAIndex, startTime)
                    # TODO: track result here of what user pressed or did with the dialog box
                    # mode-less form of dialog uses Show() instead of ShowModal()
                    self.loadDialog.ShowModal()  
                elif thisLoad == "adobe1":
                    self.displayLoadIdentifier += 1
                    self.loadDialog = newAdobeUpdateDialog(self, self.displayLoadIdentifier, currentQAIndex)
                    self.loadDialog.ShowModal()
                    globalTracker.RESPONSECODE.responseLogBuffer += "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % ("" , "\t" , "" , "\t" , self.loadDialog.getDialogID() , "\t" , self.loadDialog.getDialogTag() , "\t" , RESPONSECODE.currentResponse, "\t" , RESPONSECODE.currentResponseCode, "\t" , RESPONSECODE.previousResponse, "\t" , RESPONSECODE.previousResponseCode, "\t" , startTime, "\t" , (time.strftime("%H:%M:%S", time.localtime())), "\t", CONSTANTS.date_today, "\n")
                    RESPONSECODE.SNo += 1
                    self.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo) + "\t" + globalTracker.RESPONSECODE.responseLogBuffer)
                elif thisLoad == "windowsupdate_new":
                    self.displayLoadIdentifier += 1
                    self.loadnewDialog = newWindowsUpdateDialog(self, self.displayLoadIdentifier, currentQAIndex, startTime)
                    # mode-less form of dialog uses Show() instead of ShowModal()
                    self.loadnewDialog.ShowModal()
                elif thisLoad == "java":
                    self.displayLoadIdentifier += 1
                    self.taskbar.showJavaUpdate(self.displayLoadIdentifier, currentQAIndex, startTime)
                    
#                  TODO:response capture or logging required
                elif thisLoad.startswith("email-"):
                    emailInfo = thisLoad.split("-")
                    desiredEmailIndexID = emailInfo[1].strip()
                    if len(desiredEmailIndexID) == 6 and desiredEmailIndexID.isdigit():
                        isForced = False
                        if len(emailInfo) >= 3 and len(emailInfo[2].strip()) > 0 and emailInfo[2].strip().lower() == "f":
                            isForced = True
                        if len(desiredEmailIndexID) == 6 and desiredEmailIndexID.isdigit() and (desiredEmailIndexID in globalVar.emailIdList):
                            globalTracker.floworderInstance.createEmptyEmailControlInfoForNonMathLoad(self.FlowOrderNumber)
                            self.emailFrame.emailNext(desiredEmailIndexID, isForced, self.FlowOrderNumber, self.MathsIndex, loadIndex, self.parentID, self.currentQAPojo.getMathsID(), startTime)
                        # TODO: response of link click required
                elif thisLoad == "defender scan":
                    self.displayLoadIdentifier += 1
                    self.loadDialog = WindowsDefenderDialog(self, self.displayLoadIdentifier, currentQAIndex, startTime)
                    self.loadDialog.ShowModal()
                    globalTracker.RESPONSECODE.responseLogBuffer += "" + "\t" + "" + "\t" + self.loadDialog.getDialogID() + "\t" + self.loadDialog.getDialogTag() + "\t" + RESPONSECODE.currentResponse + "\t" + RESPONSECODE.currentResponseCode + "\t" + RESPONSECODE.previousResponse + "\t" + RESPONSECODE.previousResponseCode + "\t" + startTime + "\t" + (time.strftime("%H:%M:%S", time.localtime())) + "\t" + CONSTANTS.date_today + "\n"
                    RESPONSECODE.SNo += 1
                    self.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo) + "\t" + globalTracker.RESPONSECODE.responseLogBuffer)
                elif thisLoad == "" or len(thisLoad) <= 0:
                    pass

    def firstLoad(self, event):
#         first load      
#         self.QAIndex is the first index and firstLoad is index 0
        if self.firstLoadTrigger == True:
            self.firstLoadTrigger = False
            self.displayLoad(0)
        event.Skip()
        
    def secondLoad(self, event):
        #       second load
        if self.secondLoadTrigger == True:
            self.secondLoadTrigger = False
            self.displayLoad(1)
        event.Skip()
        
    def thirdLoad(self, event):
        #        third load
        if self.thirdLoadTrigger == True:
            self.thirdLoadTrigger = False
            self.displayLoad(2)
        event.Skip()
        
    def fourthLoad(self, event):
        #      fourth load
        if self.fourthLoadTrigger == True:
            self.fourthLoadTrigger = False
            self.displayLoad(3)
        event.Skip()
    
    def fifthLoad(self, event):
        #             fifth load
        if self.fifthLoadTrigger == True:
            self.fifthLoadTrigger = False
            self.displayLoad(4)
        event.Skip()
        
    def sixthLoad(self, event):
        #             sixth load
        if self.sixthLoadTrigger == True:
            self.sixthLoadTrigger = False
            self.displayLoad(5)
        event.Skip()
              
    def initialImageLoad(self):
        self.imageDotProbeWhite = wx.Image(imageWhite, type=wx.BITMAP_TYPE_ANY)
        self.imageDotProbeWhite = self.imageDotProbeWhite.Scale(self.dotProbeImageWidth, self.dotProbeImageHeight, wx.IMAGE_QUALITY_HIGH)
        imageRedCross = wx.Image(imageredCross, type=wx.BITMAP_TYPE_ANY)
        imageRedCross = imageRedCross.Scale(self.fixationWidth, self.fixationHeight, wx.IMAGE_QUALITY_HIGH)
        self.redFixation = imageRedCross.ConvertToBitmap()
        imageFixation = wx.Image(imageFixationStr, type=wx.BITMAP_TYPE_ANY) 
        imageFixation = imageFixation.Scale(self.fixationWidth, self.fixationHeight, wx.IMAGE_QUALITY_HIGH)
        self.tempFixation = imageFixation.ConvertToBitmap()
        self.imageProbe = wx.Image(imageProbeStr, type=wx.BITMAP_TYPE_ANY)
             
    def load(self):
        self.mUtils = mathUtils()
        self.mUtils.load(os.path.abspath(globalTracker.propertyVar.mathsQAFilePath))
        globalTracker.CONSTANTS.mathUtilsQAOdictLen = len(self.mUtils.QAODict)
        self.utils.loadMessages(globalTracker.propertyVar.noticeMsgFielPath)
        self.utils.readAllScripts(globalTracker.propertyVar.DpScriptFilePath, globalTracker.propertyVar.WpScriptFilePath)
        self.QAIndex = 0;
        self.setSizes()
        self.initialImageLoad()   
        
    def setSizes(self):
        self.displaySize = wx.GetDisplaySize()
        print "screen size= " + str(self.displaySize)
        self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"screen size= " + str(self.displaySize)+"\n")
        self.loginWidth = self.displaySize[0] / 3
        self.loginHeight = self.displaySize[1] / 3
        self.reaminingWidth = self.displaySize[0] 
        self.QPnlWidht = 0.6 * self.reaminingWidth
        self.tickerHeight = 0.03 * self.displaySize[1]
        self.taskbarHeight = 0.0375 * self.displaySize[1]
        self.taskbarIconwidth = 3.125 / 100 * self.displaySize[0]
        self.taskbarRightIconwidth = 8.07 / 100 * self.displaySize[0]
        self.taskbarRemainingWidth = self.displaySize[0] - (4 * self.taskbarIconwidth + self.taskbarRightIconwidth)
        self.reaminingHeight = self.displaySize[1] - self.tickerHeight - self.taskbarHeight
        self.QAHeight = 0.97 * self.reaminingHeight
        self.fixationWidth = 42
        self.fixationHeight = 49
        self.dotProbeImageWidth = 360
        self.dotProbeImageHeight = 270
        self.dotProbeUpImagePosn = (((self.displaySize[0] / 2) - (self.dotProbeImageWidth / 2)), ((self.displaySize[1] / 4) - (self.dotProbeImageHeight / 2)))
        self.dotProbeDownImagePosn = (((self.displaySize[0] / 2) - (self.dotProbeImageWidth / 2)), ((self.displaySize[1] * 3 / 4) - (self.dotProbeImageHeight / 2)))
        self.probeUpPosn = ((self.displaySize[0] / 2), (self.displaySize[1] / 4))
        self.probeDownPosn = ((self.displaySize[0] / 2), (self.displaySize[1] * 3 / 4))
        self.fixationPosn = (((self.displaySize[0] / 2) - (self.fixationWidth / 2)), ((self.displaySize[1] / 2) - (self.fixationHeight / 2)))
        self.SpaceAfterDotProbeUpImage = (self.fixationPosn[0], (self.fixationPosn[1] - self.dotProbeUpImagePosn[1] - self.dotProbeImageHeight))
        self.msgPnlSize = ((self.displaySize[0] / 1.5), ((self.displaySize[1] / 1.5) ))
        self.msgPnlPosn = (((self.displaySize[0]/2 ) - (self.msgPnlSize[0] / 2)+50), ((self.displaySize[1] / 2) - (self.msgPnlSize[1] / 2)))
        self.WPUpWordYPosn = 0.37 * self.displaySize[1]
        self.WPUpWordYPosn1 = 0.40 * self.displaySize[1]
        self.WPWordHeight = 2.5 / 100 * self.displaySize[1]
        self.ErrorWordHeight = 10 / 100 * self.displaySize[1]
        self.WPUPWordHeightWithSpace = 1.7 * self.WPWordHeight
        self.WPDownYPosn = self.displaySize[1] - 2 * self.WPUpWordYPosn - 2 * self.WPUPWordHeightWithSpace
        self.remaining = self.displaySize[1] - 2 * self.WPUpWordYPosn - 2 * self.WPUPWordHeightWithSpace
        self.spaceInBetweenY = (1 - 0.85) / 2 * self.remaining
        self.WPErrorY = self.WPUpWordYPosn + self.WPWordHeight + self.spaceInBetweenY
        ######################## email size ###########################
        frameWidth = 610
        frameHeight = 480 
        self.emailFrameSize = (frameWidth, frameHeight)
        self.emailFramePos = ((self.fullSize[0] - frameWidth), 20)
        self.messageShow = False

#####################################################################################
############## *****EVENT FUNCTIONS *****  ###########
##################################################################################### 
    
    def validateAllChildren(self, item):
        for sizerItem in item.GetChildren():
            widget = sizerItem.GetWindow()
            if not widget:
                # then it's probably a sizer
                sizer = sizerItem.GetSizer()
                if isinstance(sizer, wx.Sizer):
                    self.validateAllChildren(sizer)
            else:
                self.sizerItems.append(widget)
                if isinstance(widget, wx.TextCtrl):
                    text = widget.GetValue().strip(" \t")
                    if not text == None and not len(text) <= 0:
                        if len(text)>11:
                            #it should not come here
                            continue
                        else:
                            if not self.is_number(text):
                                widget.SetBackgroundColour("Red")
                                self.messageShow = True
                    else:
                        widget.SetBackgroundColour("Red")
                        self.messageShow = True
                elif isinstance(widget, wx.RadioBox):
                    pass
                
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
 
        return False
                    
    def RemoveAllChildren(self, item):     
        for sizerItem in item.GetChildren():
            widget = sizerItem.GetWindow()
            if not widget:
                # then it's probably a sizer
                sizer = sizerItem.GetSizer()
                if isinstance(sizer, wx.Sizer):
                    self.RemoveAllChildren(sizer)
            else:
                if isinstance(widget, wx.TextCtrl):
                    item.Hide(widget)
                    item.Remove(widget)
#                     if not text == None: i.e. "remove text value= " + text
                elif isinstance(widget, wx.StaticText):
#                     remove Statictext====> widget.GetLabel()
                    item.Hide(widget)
                    item.Remove(widget)
                elif isinstance(widget, wx.RadioBox):
#                     remove Radiobox
                    item.Hide(widget)
                    item.Remove(widget)
                elif isinstance(widget, wx.Panel):
                    item.Hide(widget)
                    item.Remove(widget)
        
    def onChooseRadioButton(self, event):
#         This method is fired when its corresponding button is pressed
        self.chooseIndex = event.GetInt()
        event.Skip() 
      
    def onMistakeKeyStrokeInstructionOK(self,event):
        self.middleMsg.SetFocus()
        event.Skip()
        
    def onKeyStrokeInstructionOK(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SPACE:
#             pressed the spacebar!
            if self.stateInPhase == 1 or self.stateInPhase == 3 and not PHASE.phaseGuider[PHASE.phaseNumber] == "INTERACTIVE ENVIRONMENT PHASE":
                if ((self.instructionIndex + 1) > len(self.prepostInstructionMsgList)):
                    self.stateInPhase += 1               
                self.initiate()
            elif PHASE.phaseGuider[PHASE.phaseNumber] == "INTERACTIVE ENVIRONMENT PHASE":
                print "FINISHED ALL TASK\nCLOSING APPLICATION..."
                self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"FINISHED ALL TASK\nCLOSING APPLICATION...\n")
                self.Close()   
        event.Skip()
    
    def onKillFocus(self, event):
        event.Skip()
        
    def onFocusTrainingUpPanel(self, event):   
        self.SetFocus()
        event.Skip()
        
    def onFocus(self, event):
        event.Skip()
       
    def clickQASubmit(self, event):
        self.userAnswer = ""
        self.actualAnswer = ""
        self.mathsResult = ""
        
        self.mathsPressSubmitTime = strftime("%H:%M:%S:%MS", time.localtime())
        self.messageShow = False
        for eachSizer in self.optionsizerInlist:
            self.validateAllChildren(eachSizer)  
        if self.messageShow == True:
            wx.MessageBox("Only numeric values are accepted", "Error", wx.ICON_ERROR) 
            self.messageShow = False
        elif globalTracker.math.checkForQACloseValidity(self.QAIndex - 1) == -1:
            wx.MessageBox("One or more dialog boxes are still open", "Error", wx.ICON_ERROR)    
        elif globalTracker.floworderInstance.verifyIfForcedEmailAreOpened(self.FlowOrderNumber, self.MathsIndex) == False:
            wx.MessageBox("You have some unopened emails.", "Error", wx.ICON_ERROR)
        else:
            # TODO: check for the correct answers of the maths problem
            self.answerCheckIndex = 0 
            for eachSizer in self.optionsizerInlist:
                self.answerCheck(eachSizer)
            self.mathsLogBuffer += self.userAnswer + "\t" + self.actualAnswer + "\t" + self.mathsResult
            self.mathsLogBuffer += "\t" + str(self.mathsStartTime) + "\t" + str(self.mathsPressSubmitTime) + "\t" + self.todayDat + "\n"
            self.utils.write(globalTracker.propertyVar.mathLog, self.mathsLogBuffer)
            self.normalizeBeforeMakePaneContent() 
            self.initiate() 
        event.Skip()  
    
    def answerCheck(self, item):
        for sizerItem in item.GetChildren():
            widget = sizerItem.GetWindow()
            if not widget:
                # then it's probably a sizer
                sizer = sizerItem.GetSizer()
                if isinstance(sizer, wx.Sizer):
                    self.answerCheck(sizer)
            else:
                self.sizerItems.append(widget)
                if isinstance(widget, wx.TextCtrl):
                    
                    text = widget.GetValue().strip(" \t")
                    if not text == None and not text.strip() == 0:
                        if len(self.answerSouce) - 1 == self.answerSouceIndex - 1 and self.answerCheckIndex < len(self.answerSouce[self.answerSouceIndex - 1]):
                            self.answerSouce[self.answerSouceIndex - 1][self.answerCheckIndex][3] = text
                            self.userAnswer += text + "|"
                            self.actualAnswer += self.answerSouce[self.answerSouceIndex - 1][self.answerCheckIndex][2] + "|"
                            if text == self.answerSouce[self.answerSouceIndex - 1][self.answerCheckIndex][2]:
                                self.mathsResult += RESPONSECODE.MATHS_CORRECT + "|"
                            elif self.answerSouce[self.answerSouceIndex - 1][self.answerCheckIndex][2] == None or len(self.answerSouce[self.answerSouceIndex - 1][self.answerCheckIndex][2]) <= 0:
                                self.mathsResult += RESPONSECODE.MATHS_UNKNOWN + "|"
                            elif not self.answerSouce[self.answerSouceIndex - 1][self.answerCheckIndex][2] == text:
                                self.mathsResult += RESPONSECODE.MATHS_INCORRECT + "|"
                            self.answerCheckIndex += 1
                elif isinstance(widget, wx.RadioBox):
                    if len(self.answerSouce) - 1 == self.answerSouceIndex - 1 and self.answerCheckIndex < len(self.answerSouce[self.answerSouceIndex - 1]):
                        self.answerSouce[self.answerSouceIndex - 1][self.answerCheckIndex][3] = widget.GetStringSelection()
                        self.userAnswer += widget.GetStringSelection() + "|"
                        self.actualAnswer += self.answerSouce[self.answerSouceIndex - 1][self.answerCheckIndex][2]
                        if widget.GetStringSelection() == self.answerSouce[self.answerSouceIndex - 1][self.answerCheckIndex][2]:
                            self.mathsResult += RESPONSECODE.MATHS_CORRECT + "|"
                        elif len(self.answerSouce[self.answerSouceIndex - 1][self.answerCheckIndex][2]) <= 0:
                            self.mathsResult += RESPONSECODE.MATHS_UNKNOWN + "|"
                        elif not self.answerSouce[self.answerSouceIndex - 1][self.answerCheckIndex][2] == widget.GetStringSelection():
                            self.mathsResult += RESPONSECODE.MATHS_INCORRECT + "|"
                        self.answerCheckIndex += 1
                               
    def onChar(self, event):
        if not self.inactivity == None and self.inactivity.IsRunning() and MainFrame.acceptChar == True:
            self.inactivity.Stop()
        
    #######################################
        localtime = time.asctime(time.localtime(time.time()))
        key = event.GetKeyCode()
        MainFrame.isRun = False
        if self.prevTime == localtime:
            self.prevTime = localtime
        elif (self.currentPhase == "DOT PROBE TRAINING PHASE" or self.currentPhase == "DOT PROBE PHASE") and MainFrame.acceptChar == True and ((key in UP_char) or (key in DOWN_char)):
            MainFrame.acceptChar = False    
            self.prevResponseTime = self.currentResponseTime
            self.currentResponseTime = time.clock()
            self.prevResponse = self.currentResponse
            self.currentResponse = CHAR_response
            self.onCharlocalTime = time.clock()
            self.prevTime = localtime
#             if(abs(self.currentResponseTime - self.prevResponseTime)<2.5):==> this is "error indicator"
            if (MainFrame.isRun == False and (self.prevResponse == IDLE_response and self.currentResponse == IDLE_response) and (abs(self.currentResponseTime - self.prevResponseTime) >= highDiff)) or ((self.prevResponse == CHAR_response and self.currentResponse == CHAR_response) and (abs(self.currentResponseTime - self.prevResponseTime) >= lowDiff)) or ((self.prevResponse == IDLE_response and self.currentResponse == CHAR_response) and (abs(self.currentResponseTime - self.prevResponseTime) >= lowDiff)) or ((self.prevResponse == CHAR_response and self.currentResponse == IDLE_response) and (abs(self.currentResponseTime - self.prevResponseTime) >= highDiff)):
                MainFrame.isRun = True
                print "prev response= "+self.prevResponse+"      current response= "+self.currentResponse +"      differnce in time=  "+str(abs(self.currentResponseTime - self.prevResponseTime))
                self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"prev response= "+self.prevResponse+"      current response= "+self.currentResponse +"      differnce in time=  "+str(abs(self.currentResponseTime - self.prevResponseTime))+"\n")
            elif (self.currentPhase == "DOT PROBE TRAINING PHASE" and self.trainIndex == 1) or (self.currentPhase == "DOT PROBE PHASE" and self.dotProbeImgIndex == 1):
                MainFrame.isRun = True 
                print "training index ="+str(self.trainIndex)+"  thus isRun=TRUE"
                self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"training index ="+str(self.trainIndex)+"  thus isRun=TRUE\n")       
            
            if MainFrame.isRun:
                print "onChar() MainFrame.isRun=  "+str(MainFrame.isRun)
                self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"onChar() MainFrame.isRun=  "+str(MainFrame.isRun)+"\n")
                # this solved the problem of flipping twice when we press keystoke at the same time when 5 sec would e triggered
                #this if part kept here becuse of problem that arises when 500 sec already passed and accptchar is true but then difference of time response doesnt satisfy to run; In this case 5000 sec ideleness was being stopped since this if statement was being placed in upper part without checking if isRun is true;;;;;when isRun came to be False tand the idleness was already stopped, * was being showd in the screen since isRun is False and idleness was already stopped
                #putting if statement here makes it with isRun=True of go to 5000 sec idleness part
                
                self.Unbind(wx.EVT_KEY_UP, handler=self.onChar)
                if (key in UP_char) or (key in DOWN_char):
                    self.probeTrack = ""
                    self.probeTimerEnd = time.clock()
                    if self.probeType >= 0:
                        if self.probeType == 0:
                            probePosn = UP_PROBE_INTRIALCODE
                        elif self.probeType == 1:
                            probePosn = dOWN_PROBE_INTRIALCODE
                        self.probeTrack = str(self.serialNum_DP) + "\t" + self.todayDat + "\t" + str(globalVar.subjectId) + "\t" + REPORT.TRIALCODE[probePosn] + "\t" + str(self.currentBlockNumnber) + "\t"
                    if (key in UP_char):
                        if self.currentPhase == "DOT PROBE TRAINING PHASE":
                            self.trackTrainingError(0)
                            if self.probeType >= 0:
                                self.probeTrack = self.probeTrack +str(self.trainIndex-1)+"\t" + "\t\t" + globalTracker.propertyVar.dotShowInterval + "\t"+ REPORT.TRIALCODE[self.correct]
                            self.utils.write(globalTracker.propertyVar.eventLog, "UPDOWN TRAINING\n******Key stroke*****\nUP\n")
                        elif self.currentPhase == "DOT PROBE PHASE":
                            self.trackDotProbeError(0)
                            if self.probeType >= 0:
                                self.probeTrack = self.probeTrack +str(self.phaseIndex-1)+"\t" + "\t\t" + globalTracker.propertyVar.dotShowInterval + "\t"+ REPORT.TRIALCODE[self.correct]
                            self.utils.write(globalTracker.propertyVar.eventLog, "DOTPROBE\t******Key stroke*****\nUP\n")
                            
                    elif (key in DOWN_char):
                        if self.currentPhase == "DOT PROBE TRAINING PHASE":
                            self.trackTrainingError(1)
                            if self.probeType >= 0:
                                self.probeTrack = self.probeTrack +str(self.trainIndex-1)+"\t" + "\t\t" + globalTracker.propertyVar.dotShowInterval + "\t"+ REPORT.TRIALCODE[self.correct]
                            self.utils.write(globalTracker.propertyVar.eventLog, "UPDOWN TRAINING\n******Key stroke*****\nDOWN\n")
                        elif self.currentPhase == "DOT PROBE PHASE":
                            self.trackDotProbeError(1)
                            if self.probeType >= 0:
                                self.probeTrack = self.probeTrack+str(self.phaseIndex-1)+"\t" + "\t\t" + globalTracker.propertyVar.dotShowInterval + "\t" + REPORT.TRIALCODE[self.correct]
                            self.utils.write(globalTracker.propertyVar.eventLog, "DOTPROBE\t******Key stroke*****\nDOWN\n")
                self.probeTrack = self.probeTrack + "\t" + str(self.probeTimerEnd - self.probeTimerStart) + "\t" + str(abs(self.onCharlocalTime - self.inactivitylocalTime)) + "\n"  # latency       
                self.serialNum_DP += 1
                self.utils.write(globalTracker.propertyVar.imageDotProbeResult, self.probeTrack)
                # uhbind the frame to key event so that users keypresses is taken only after the probe is shown on the screen and is unbinded or user key press event wont be handled by this function when at most one user 
                # key press has occured===> This will ensure that pressing "i","m" or other valid key for multiple time wont flip the images weirdly    
                
                if self.currentPhase == "DOT PROBE TRAINING PHASE":
                    self.showTraningWhite()
                    time.sleep(2)
                    print "show white for 2 sec"
                    self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"show white for 2 sec\n")
                    self.initiate()
                elif self.currentPhase == "DOT PROBE PHASE":
                    self.showDotProbeRealWhite()
                    time.sleep(2)
                    print "show white for 2 sec"
                    self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"show white for 2 sec\n")
                    self.initiate()
            elif ((self.currentPhase == "DOT PROBE TRAINING PHASE" or self.currentPhase == "DOT PROBE PHASE")and MainFrame.isRun==False):
                #this situation ever comes?
                print "when MainFrame.isRun==False and acceptChar= "+MainFrame.acceptChar +" and here self.inactivity.Stop() has been called"
                self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"when MainFrame.isRun==False and acceptChar= "+MainFrame.acceptChar +" and here self.inactivity.Stop() has been called")
        elif MainFrame.acceptChar == True and ((key in WP_LEFT_CHAR) or (key in WP_RIGHT_CHAR)):
            MainFrame.acceptChar = False
            if self.currentPhase == "WORD PROBE PRACTISE PHASE":
                self.WPProbeTimerEnd = time.clock()
                if key in WP_LEFT_CHAR:
                    self.WPReport += LEFT + "\t"  # record response
                    self.trackWPTrainError(0)
                else:
                    self.WPReport += RIGHT + "\t"  # record response
                    self.trackWPTrainError(1)
                self.WPReport += str(self.WPProbeTimerEnd - self.WPProbeTimerStart) + "\t"  # record latency 
                self.reportRemainingForWPTrain()   
                self.WPReport += "\n"
                self.utils.write(globalTracker.propertyVar.wordDotProbeResult, self.WPReport)
                self.showWordProbeTrainingWhite()
                self.initiate()
            elif self.currentPhase == "WORD PROBE PHASE":
                self.WPProbeTimerEnd = time.clock()
                if key in WP_LEFT_CHAR:
                    self.WPReport += LEFT + "\t"  # record response
                    self.trackWPError(0)
                else:
                    self.WPReport += RIGHT + "\t"  # record response
                    self.trackWPError(1)
                self.WPReport += str(self.WPProbeTimerEnd - self.WPProbeTimerStart) + "\t"  # record latency 
                self.WPReport += "\n"
                self.utils.write(globalTracker.propertyVar.wordDotProbeResult, self.WPReport)
                self.showWordProbeRealWhite()
                self.initiate() 

class App(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect=False, filename=None)
        
    def OnInit(self):
        print "************************************* STARTING APPLICAITON ********************************************\n"
        self.utils.write(globalTracker.propertyVar.diagnosisDPLog,"************************************* STARTING APPLICAITON ********************************************\n")
        frame = MainFrame()
        self.SetTopWindow(frame)
        frame.Maximize(True)
        frame.ShowFullScreen(True)
        frame.Show()
        return True
        
def main():
    app = App(redirect=True)
#     wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
    
