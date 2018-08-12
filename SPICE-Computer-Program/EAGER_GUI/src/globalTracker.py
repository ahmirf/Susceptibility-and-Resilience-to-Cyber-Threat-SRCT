'''
Created on Oct 6, 2014

@author: AnjilaTam
'''
from __builtin__ import object
from __builtin__ import str
from propertiesUsingConfigParser import propertyFile   
import utils


class globalVar(object):
    
    def __init__(self):
        print "globalVar in globalTracker.py iniitated"
        pass
    
    indexofEmail = -389
    emailPojo_ = None
    dialogPojo_ = None
    flowNumber = -1
    mathsIndex = -1
    LoadIndex = -1
    dialogIdList = []
    emailIdList = []
    dialogTypeEnum = {}
    
    subjectId = -1
    subjectGroup = -1
    subjectName = None
    date = ""
    
    dialogTypeEnum["INSTALLATION-DIALOG"] = "1"
    dialogTypeEnum["FORM_RESET_EMAIL_PWD"] = "2"
    dialogTypeEnum["FORM_GET_INFO"] = "3"
    dialogTypeEnum["FORM_GET_USERNAME_PWD"] = "4"
    dialogTypeEnum["INVENTORY_INFO_SHOW_GLADSTONE"] = "5" 
    dialogTypeEnum["INVENTORY_INFO_SHOW_DURABLE"] = "6" 
    dialogTypeEnum["INVENTORY_INFO_SHOW"] = "7" 
    
    
class ERRORMESSAGES:
    
    subjectIdAlphaNum = "ID cannot contain letters other than alphabets and numbers"
    subjectIdEmpty = "ID cannot be empty"
    subjectNameEmpty = "Subject Name cannot be empty"
    subjectNameLetter = "Name cannot contain letters other than alphabets"
    duplicateID = "This ID has been already used"
    
class PHASE(object):
    phaseNumber = -1
    phaseGuider = {}
    phaseGuider[1] = "DOT PROBE TRAINING PHASE"
    phaseGuider[2] = "DOT PROBE PHASE"
    phaseGuider[3] = "WORD PROBE PRACTISE PHASE"
    phaseGuider[4] = "WORD PROBE PHASE"
    phaseGuider[5] = "INTERACTIVE ENVIRONMENT PHASE"
    phaseGuider[6] = "SURVEY PHASE"
    
class REPORT(object):
    IMAGEDOTPROBEREPORTHEADER = "#S.N.\tdate\tsubject\tTrials\tcurrentblock\tTrial_value\tup_type\tdown_type\ttrialtimeout\tcorrect\tlatency\n"
    TRIALCODE = {}
    TRIALCODE[1] = "FIXATION"
    TRIALCODE[2] = "PROBE"
    TRIALCODE[3] = "PRACTICE_PIC"
    TRIALCODE[4] = "TRIAL_PIC"
    TRIALCODE[5] = "UP_PROBE"
    TRIALCODE[6] = "DOWN_PROBE"
    TRIALCODE[7] = "0"  # representation on incorrect result
    TRIALCODE[8] = "1"  # representation of correct result
    
    TRIALCODE[9] = "0"  # represents the values that doesnot have any meaning like correct for fixation
    #####################################################################################################################
    ################################## word probe #######################################################################
    
    WORDDOTPROBEREPORTHEADER = "#S.N.\tdate\ttime\tblockcode\ttrialcode\tthreat_word_value\tneutral_word_value\tprobe_position\tcurrent_probe_value\tresponse\tcorrect\tlatency\tvalues_sum_correct\tvalues_sum_correct_PITP\tvalues_count_PITP\tvalues_sum_correct_PINP\tvalues_count_PINP\tvalues_sumtr_PITP\tvalues_sumrt_PINP\tvalues_meanrt_PITP\tvalues_meanrt_PINP\ttrail_probe_PITP_medianLatency\ttrial_probe_PINP_medianLatency\texpression_TBI\n"
    BLOCK_INFO = {}
    BLOCK_INFO[0] = "PRACTICE_BLOCK"
    BLOCK_INFO[1] = "TRIAL_BLOCK_"
    CASE_PITP = "PITP"
    CASE_PINP = "PINP"
    TRIALCODE_WP = {}
    TRIALCODE_WP[0] = "practice_probe"
    TRIALCODE_WP[CASE_PITP] = "probe_" + CASE_PITP
    TRIALCODE_WP[CASE_PINP] = "probe_" + CASE_PINP
    VALUES_PROBEPOSITION = {}
    VALUES_PROBEPOSITION[CASE_PITP] = 1
    VALUES_PROBEPOSITION[CASE_PINP] = 0
    CORRECT_RESPONSE = 1
    INCORRECT_RESPONSE = 0
    
class MATH(object):
    OPTION_TYPE = ["fill_in", "radio"]

class FLOWORDER(object):
    # "MP3 download popup"
    FLOWORDER = ["Email-120000", "M", "iPad-scam", "virus-alert", "M", "Email-120002-f", "M", "W2", "M", "Email-120006-f", "M", "M"]
#     FLOWORDER = ["Email-120000", "M",  "M",  "M", "W2", "M", "Email-120006-f", "M", "M", "iPad-scam", "virus-alert","Email-120002-f"]
    EMAIL_STATUS_CODE = [0, 1, 2, 3, 4, 5, -10000]
    EMAIL_STATUS = ["NOT_INSERTED", "INSERTED_NOTOPENED", "OPEN_BUT_LINK_NOT_CLICKED", "OPEN_HAS_NO_LINK", "OPEN_AND_LINK_CLICKED", "REPLIED", "NOT_FORCED"]
    emailControlInfo = {}
    # emailControlInfo is a two dimensional list e.g.
    # emailControlInfo=[[flowNumber, MathsNumber, LoadNumber, emailStatus],[],[]] 
    
    def verifyIfForcedEmailAreOpened(self, flowNumber, mathsQNumber):
        if self.emailControlInfo.has_key(flowNumber):
            if flowNumber >= 0 and flowNumber < len(FLOWORDER.FLOWORDER):
                flow = FLOWORDER.FLOWORDER[flowNumber]
                if not flow == None and isinstance(flow, str):
                    flow = flow.strip().lower()
                    if flow.startswith("email-") and isinstance(self.emailControlInfo[flowNumber], list) and mathsQNumber == -1:
                        emailStatusList = self.emailControlInfo[flowNumber]
                        if len(emailStatusList) == 1:
                            # if status is 1 or 0 then return False else return True
                            if (emailStatusList[0] == self.EMAIL_STATUS_CODE[0] or emailStatusList[0] == self.EMAIL_STATUS_CODE[1]):
                                return False
                            else:
                                return True
                        else:
                            return False
                       
                    elif not flow == None and flow == "m" and isinstance(self.emailControlInfo[flowNumber], dict)  and mathsQNumber >= 0:
                        mathsDict = self.emailControlInfo[flowNumber]
                        if not mathsDict == None and isinstance(mathsDict, dict) and mathsDict.has_key(mathsQNumber):
                            if isinstance(mathsDict[mathsQNumber], list):
                                for emailS in mathsDict[mathsQNumber]:
                                    if emailS == self.EMAIL_STATUS_CODE[1] or emailS == self.EMAIL_STATUS_CODE[0]:
                                        # if status is 1 or 0 then return False else return True
                                        return False
                                return True
        else:
            return True
                                
    def changeEmailStatusFromOpenToReply(self):
        # at this point status should not be 0 or 1 and should be one of (2,3,4)
        if globalVar.flowNumber >= 0 and globalVar.flowNumber < len(FLOWORDER.FLOWORDER) and self.emailControlInfo.has_key(globalVar.flowNumber):
                flow = FLOWORDER.FLOWORDER[globalVar.flowNumber]
                if not flow == None and isinstance(flow, str):
                    flow = flow.strip().lower()
                    if flow.startswith("email-") and isinstance(self.emailControlInfo[globalVar.flowNumber], list) and globalVar.mathsIndex == -1 and globalVar.LoadIndex == -1:
                        emailStatusList = self.emailControlInfo[globalVar.flowNumber]
                        if len(emailStatusList) == 1 and (emailStatusList[0] == self.EMAIL_STATUS_CODE[2] or emailStatusList[0] == self.EMAIL_STATUS_CODE[3] or emailStatusList[0] == self.EMAIL_STATUS_CODE[4]):
                            self.emailControlInfo[globalVar.flowNumber][0] = self.EMAIL_STATUS_CODE[5]
                    elif not flow == None and flow == "m" and isinstance(self.emailControlInfo[globalVar.flowNumber], dict)  and globalVar.mathsIndex >= 0 and globalVar.LoadIndex >= 0:
                        mathsDict = self.emailControlInfo[globalVar.flowNumber]
                        if not mathsDict == None and isinstance(mathsDict, dict) and mathsDict.has_key(globalVar.mathsIndex):
                            if isinstance(mathsDict[globalVar.mathsIndex], list):
                                if globalVar.LoadIndex < len(mathsDict[globalVar.mathsIndex]):
                                    emailS = self.emailControlInfo[globalVar.flowNumber][globalVar.mathsIndex][globalVar.LoadIndex]
                                    if emailS == self.EMAIL_STATUS_CODE[2] or emailS == self.EMAIL_STATUS_CODE[3] or emailS == self.EMAIL_STATUS_CODE[4]:
                                        self.emailControlInfo[globalVar.flowNumber][globalVar.mathsIndex][globalVar.LoadIndex] = self.EMAIL_STATUS_CODE[5]
               
    def  changeEmailStatusFromOpenButNoLinkClickToOpenNLinkClicked(self): 
        # 2 to 4
        # 2(open but no link clicked) to 4(open and link clicked)
        if globalVar.flowNumber >= 0 and globalVar.flowNumber < len(FLOWORDER.FLOWORDER) and self.emailControlInfo.has_key(globalVar.flowNumber):
                flow = FLOWORDER.FLOWORDER[globalVar.flowNumber]
                if not flow == None and isinstance(flow, str):
                    flow = flow.strip().lower()
                    if flow.startswith("email-") and isinstance(self.emailControlInfo[globalVar.flowNumber], list) and globalVar.mathsIndex == -1 and globalVar.LoadIndex == -1:
                        emailStatusList = self.emailControlInfo[globalVar.flowNumber]
                        if len(emailStatusList) == 1 and emailStatusList[0] == self.EMAIL_STATUS_CODE[2]:
                            self.emailControlInfo[globalVar.flowNumber][0] = self.EMAIL_STATUS_CODE[4]
                    elif not flow == None and flow == "m" and isinstance(self.emailControlInfo[globalVar.flowNumber], dict)  and globalVar.mathsIndex >= 0 and globalVar.LoadIndex >= 0:
                        mathsDict = self.emailControlInfo[globalVar.flowNumber]
                        if not mathsDict == None and isinstance(mathsDict, dict) and mathsDict.has_key(globalVar.mathsIndex):
                            if isinstance(mathsDict[globalVar.mathsIndex], list):
                                if globalVar.LoadIndex < len(mathsDict[globalVar.mathsIndex]) and self.emailControlInfo[globalVar.flowNumber][globalVar.mathsIndex][globalVar.LoadIndex] == self.EMAIL_STATUS_CODE[2]:
                                    self.emailControlInfo[globalVar.flowNumber][globalVar.mathsIndex][globalVar.LoadIndex] = self.EMAIL_STATUS_CODE[4]
        
    def changeEmailStatusFromInsertedToOpenAndHasNoLink(self, flowMathLoadNumberList):
        # 1 to (3)
        if not flowMathLoadNumberList == None and len(flowMathLoadNumberList) == 3:
            flowNumber = flowMathLoadNumberList[0]
            mathsQNumber = flowMathLoadNumberList[1]
            loadIndex = flowMathLoadNumberList[2]
            if flowNumber >= 0 and flowNumber < len(FLOWORDER.FLOWORDER) and self.emailControlInfo.has_key(flowNumber):
                flow = FLOWORDER.FLOWORDER[flowNumber]
                if not flow == None and isinstance(flow, str):
                    flow = flow.strip().lower()
                    if flow.startswith("email-") and isinstance(self.emailControlInfo[flowNumber], list) and mathsQNumber == -1 and loadIndex == -1:
                        emailStatusList = self.emailControlInfo[flowNumber]
                        if len(emailStatusList) == 1 and emailStatusList[0] == self.EMAIL_STATUS_CODE[1]:
                            self.emailControlInfo[flowNumber][0] = self.EMAIL_STATUS_CODE[3]
                    elif not flow == None and flow == "m" and isinstance(self.emailControlInfo[flowNumber], dict)  and mathsQNumber >= 0 and loadIndex >= 0:
                        mathsDict = self.emailControlInfo[flowNumber]
                        if not mathsDict == None and isinstance(mathsDict, dict) and mathsDict.has_key(mathsQNumber):
                            if isinstance(mathsDict[mathsQNumber], list):
                                if loadIndex < len(mathsDict[mathsQNumber]) and self.emailControlInfo[flowNumber][mathsQNumber][loadIndex] == self.EMAIL_STATUS_CODE[1]:
                                    self.emailControlInfo[flowNumber][mathsQNumber][loadIndex] = self.EMAIL_STATUS_CODE[3]
    
    def changeEmailStatusFromInsertedToOpenButNoLinkClicked(self, flowMathLoadNumberList):
        # 1 to (2)
        if not flowMathLoadNumberList == None and len(flowMathLoadNumberList) == 3:
            flowNumber = flowMathLoadNumberList[0]
            mathsQNumber = flowMathLoadNumberList[1]
            loadIndex = flowMathLoadNumberList[2]
            if flowNumber >= 0 and flowNumber < len(FLOWORDER.FLOWORDER) and self.emailControlInfo.has_key(flowNumber):
                flow = FLOWORDER.FLOWORDER[flowNumber]
                if not flow == None and isinstance(flow, str):
                    flow = flow.strip().lower()
                    if flow.startswith("email-") and isinstance(self.emailControlInfo[flowNumber], list) and mathsQNumber == -1 and loadIndex == -1:
                        emailStatusList = self.emailControlInfo[flowNumber]
                        if len(emailStatusList) == 1 and emailStatusList[0] == self.EMAIL_STATUS_CODE[1]:
                            self.emailControlInfo[flowNumber][0] = self.EMAIL_STATUS_CODE[2]
                    elif not flow == None and flow == "m" and isinstance(self.emailControlInfo[flowNumber], dict)  and mathsQNumber >= 0 and loadIndex >= 0:
                        mathsDict = self.emailControlInfo[flowNumber]
                        if not mathsDict == None and isinstance(mathsDict, dict) and mathsDict.has_key(mathsQNumber):
                            if isinstance(mathsDict[mathsQNumber], list):
                                if loadIndex < len(mathsDict[mathsQNumber]) and self.emailControlInfo[flowNumber][mathsQNumber][loadIndex] == self.EMAIL_STATUS_CODE[1]:
                                    self.emailControlInfo[flowNumber][mathsQNumber][loadIndex] = self.EMAIL_STATUS_CODE[2]

    def createEmptyEmailControlInfoForMathLoad(self, flowNumber, mathsQNumber): 
        if flowNumber < len(self.FLOWORDER) and mathsQNumber < len(MATHASSOC_DIALOG.DIALOG_INFO) and not self.emailControlInfo.has_key(flowNumber):
            if flowNumber < len(self.FLOWORDER):
                flow = self.FLOWORDER[flowNumber]
                if not flow == None and isinstance(flow, str):
                    flow = flow.strip().lower()
                    if flow == "m":
                        if mathsQNumber < CONSTANTS.mathUtilsQAOdictLen and mathsQNumber < len(MATHASSOC_DIALOG.DIALOG_INFO):
                            dialogInfo = MATHASSOC_DIALOG.DIALOG_INFO[mathsQNumber]
                            mathDictionary = {}
                            mathloadStatus = []
                            # this will create status 0 for each email serially so that if there are two emails then
                            # there will be [0,0] so there is no information about the load number here
                            for mathload in dialogInfo:
                                mathload = mathload.strip().lower()
                                if mathload.startswith("email-"):
                                    if mathload.index("-f") >= 12:  # ["Email-110000-f"] where length of "Email-110000==12 so f should occur only afte 12th char
                                        mathloadStatus.append(self.EMAIL_STATUS_CODE[0])
                                    elif mathload.index("-f") < 0:
                                        mathloadStatus.append(self.EMAIL_STATUS_CODE[6])
                            if len(mathloadStatus) > 0:
                                mathDictionary[mathsQNumber] = mathloadStatus
                                self.emailControlInfo[flowNumber] = mathDictionary
            
    def createEmptyEmailControlInfoForNonMathLoad(self, flowNumber): 
        if not self.emailControlInfo.has_key(flowNumber):
            if flowNumber < len(self.FLOWORDER):
                flow = self.FLOWORDER[flowNumber]
                if not flow == None and isinstance(flow, str):
                    flow = flow.strip().lower()
                    if flow.startswith("email-"):
                        initStatus = []
                        if flow.find("-f") >= 12:  # ["Email-110000-f"] where length of "Email-110000==12 so f should occur only afte 12th char
                            initStatus.append(self.EMAIL_STATUS_CODE[0])
                        elif flow.find("-f") < 0:
                            initStatus.append(self.EMAIL_STATUS_CODE[6])
                        if len(initStatus) > 0:
                            self.emailControlInfo[flowNumber] = initStatus
                        initStatus = None  
    
    def changeEmailStatusFromNotInserteToInserted(self, flowNumber, mathsQNumber, loadIndex): 
        if flowNumber >= 0 and flowNumber < len(FLOWORDER.FLOWORDER) and self.emailControlInfo.has_key(flowNumber):
            flow = FLOWORDER.FLOWORDER[flowNumber]
            if not flow == None and isinstance(flow, str):
                flow = flow.strip().lower()
                if flow.startswith("email-") and isinstance(self.emailControlInfo[flowNumber], list) and mathsQNumber == -1 and loadIndex == -1:
                    emailStatusList = self.emailControlInfo[flowNumber]
                    if len(emailStatusList) == 1 and emailStatusList[0] == self.EMAIL_STATUS_CODE[0]:
                        self.emailControlInfo[flowNumber][0] = self.EMAIL_STATUS_CODE[1]
                elif not flow == None and flow == "m" and isinstance(self.emailControlInfo[flowNumber], dict)  and mathsQNumber >= 0 and loadIndex >= 0:
                    mathsDict = self.emailControlInfo[flowNumber]
                    if not mathsDict == None and isinstance(mathsDict, dict) and mathsDict.has_key(mathsQNumber):
                        if isinstance(mathsDict[mathsQNumber], list):
                            if loadIndex < len(mathsDict[mathsQNumber]):
                                self.emailControlInfo[flowNumber][mathsQNumber][loadIndex] = self.EMAIL_STATUS_CODE[1]
                   
    def changeStatusFromInitializedToClosed(self, QAIndex, loadIndex):    
        if self.DIALOGCONTROLINFO.has_key(QAIndex):
            if self.DIALOGCONTROLINFO.get(QAIndex)[loadIndex] == self.DIALOG_STATUS[1]:  # if initialized
                self.DIALOGCONTROLINFO.get(QAIndex)[loadIndex] = self.DIALOG_STATUS[2]  # change to closed
    
class RESPONSECODE(object):
    responseHeader = "S.No.\tFlow No\tMath#\tparent\tMath_ID\tEmail_ID\tEmail_TAG\tDialog_ID\tDialog_TAG\tResponse\tResponseCode\tPreviousResponse\tPreviousResponseCode\tStartTime\tEndTime\tDate\tLink clicked(if any)\n"
    mathsResponseHeader = "S.No.\tMath#\tMath_ID\tuser_answer\tcorrect_answer\tresult\tStartTime\tEndTime\tDate\n"
    DAILOG_REPORT_HEADER = "#s.n.\tdate\tDialog_ID\tDialogTag\tparent_ID\tparent_isMath\tparent_isEmail\t\Field_Values\tstart_time\tend_time\n"
    RESPONSE = {}
    responseLogBuffer = ""
    dilaogLogBuffer = ""
    SNo = -1
    dialogSN = -1
    flowSeq = -1
    EMAIL_NOT_INSERTED = FLOWORDER.EMAIL_STATUS[0]
    EMAIL_INSERTED_NOTOPENED = FLOWORDER.EMAIL_STATUS[1]
    EMAIL_OPEN_BUT_LINK_NOT_CLICKED = FLOWORDER.EMAIL_STATUS[2]
    EMAIL_OPEN_HAS_NO_LINK = FLOWORDER.EMAIL_STATUS[3]
    EMAIL_OPEN_AND_LINK_CLICKED = FLOWORDER.EMAIL_STATUS[4]
    EMAIL_REPLIED = FLOWORDER.EMAIL_STATUS[5]
    
    DIALOG_NO = "DIALOG_NO"
    DIALOG_YES = "DIALOG_YES"
    DIALOG_CLOSE = "DIALOG_CLOSE"
    SCAN_CANCEL = "SCAN_CANCEL"
    MP3_EMAIL = "EMAIL PROVIDED ON IPAD SCHEME"
    MP3_EMAIL_VALUE = ""
#     MP3_EMAIL="MP3_OPEN"
#     MP3_SAVE="MP3_SAVE"
    MP3_CANCEL = "MP3_CANCEL"
    
    ADOBE_UPDATE_Y = "ADOBE_UPDATE_YES"
    ADOBE_UPDATE_N = "ADOBE_UPDATE_NO"
    ADOBE_UPDATE_CLOSE = "ADOBE_DIALOG_CLOSE"
    ADOBE_UPDATE_CHECKBOX = "ADOBE_UPDATE_CHECKBOX"
    VIRUS_ALERT_HEAL_ALL = "VIRUS_ALERT_HEAL_ALL"
    VIRUS_ALERT_IGNORE_ALL = "VIRUS_ALERT_IGNORE_ALL"
    VIRUS_ALERT_CLOSE = "VIRUS_ALERT_CLOSE"
    ANTIVIRUS_SCAN_CANCEL = "ANTIVIRUS_SCAN_CANCEL"
    ANTIVIRUS_SCAN_CLOSE = "ANTIVIRUS_SCAN_CLOSE"
    ANTIVIRUS_UPDATE_VIRUS_DEFINITION = "ANTIVIRUS_UPDATE_VIRUS_DEFINITION"
    
    UPDATE_COMPUTER_NO = "UPDATE_COMPUTER_NO"
    UPDATE_COMPUTER_YES = "UPDATE_COMPUTER_YES"
    UPDATE_COMPUTER_CLOSE = "UPDATE_COMPUTER_CLOSE"
    PROGRESSBAR_COMPLETE = "PROGRESSBAR_COMPLETE"
    PROGRESSBAR_INCOMPLETE = "PROGRESSBAR_INCOMPLETE"
    MATHS_CORRECT = "MATHS_ANSWER_CORRECT"
    MATHS_INCORRECT = "MATHS_ANSWER_INCORRECT"
    MATHS_UNKNOWN = "MATHS_ANSWER_UNKNOWN"
    
    # reset Email and Pwd
    RESET_EMAIL_PWD_OK = "RESET_EMAIL_PWD_OK"
    RESET_EMAIL_PWD_CANCEL = "RESET_EMAIL_PWD_CANCEL"
    FORM_DOB_OK = "DOB_ADDRESS_GENDER_FORM_OK"
    FORM_DOB_CANCEL = "DOB_ADDRESS_GENDER_FORM_CANCEL"
    FORM_GET_UNAME_PWD_OK = "FORM_GET_USERNAME_PWD_OK"
    FORM_GET_UNAME_PWD_CANCEL = "FORM_GET_USERNAME_PWD_CANCEL"
    
    UPDATE_COMPUTER_RESTARTNOW = "UPDATE_COMPUTER_RESTART_NOW"
    UPDATE_COMPUTER_POSTPONE = "UPDATE_COMPUTER_RESTART_POSTPONE"
    
    currentResponse = ""
    currentResponseCode = "-100"
    previousResponse = ""
    previousResponseCode = "-100"
    individualResponse = ""
    individualResponseCode = ""
    
    RESPONSE[DIALOG_NO] = "0"
    RESPONSE[DIALOG_YES] = "1"
    RESPONSE[DIALOG_CLOSE] = "2"
    RESPONSE[SCAN_CANCEL] = "3"
    # MP3 DOWNLOAD?
    RESPONSE[MP3_EMAIL] = "4"
    RESPONSE[MP3_EMAIL_VALUE] = '5'
    RESPONSE[MP3_CANCEL] = "6" 
    # ADOBE UPDATE
    RESPONSE[ADOBE_UPDATE_Y] = "7"
    RESPONSE[ADOBE_UPDATE_N] = "8" 
    RESPONSE[ADOBE_UPDATE_CLOSE] = "9" 
    RESPONSE[ADOBE_UPDATE_CHECKBOX] = "36"
    # VIRUS ALERT AND REMOVE
    RESPONSE[VIRUS_ALERT_HEAL_ALL] = "10" 
    RESPONSE[VIRUS_ALERT_IGNORE_ALL] = "11" 
    RESPONSE[VIRUS_ALERT_CLOSE] = "12" 
    #
    RESPONSE[ANTIVIRUS_SCAN_CANCEL] = "13"
    RESPONSE[ANTIVIRUS_SCAN_CLOSE ] = "14"
    RESPONSE[UPDATE_COMPUTER_NO] = "15"
    RESPONSE[UPDATE_COMPUTER_YES] = "16"
    RESPONSE[UPDATE_COMPUTER_CLOSE] = "17"
    # MATHS_ANSWERS
    RESPONSE[MATHS_CORRECT] = "18"
    RESPONSE[MATHS_INCORRECT] = "19"
    RESPONSE[MATHS_UNKNOWN] = "20"
    # EMAIL
    RESPONSE[EMAIL_NOT_INSERTED] = "21"
    RESPONSE[EMAIL_INSERTED_NOTOPENED] = "22"
    RESPONSE[EMAIL_OPEN_BUT_LINK_NOT_CLICKED] = "23"
    RESPONSE[EMAIL_OPEN_HAS_NO_LINK] = "24"
    RESPONSE[EMAIL_OPEN_AND_LINK_CLICKED] = "25"
    RESPONSE[EMAIL_REPLIED] = "26"
    #
    RESPONSE[RESET_EMAIL_PWD_OK] = "27"
    RESPONSE[RESET_EMAIL_PWD_CANCEL] = "28"
    RESPONSE[FORM_DOB_OK] = "29"
    RESPONSE[FORM_DOB_CANCEL] = "30"
    RESPONSE[FORM_GET_UNAME_PWD_OK] = "31"
    RESPONSE[FORM_GET_UNAME_PWD_CANCEL] = "32"
    
    RESPONSE[UPDATE_COMPUTER_RESTARTNOW] = "33"
    RESPONSE[UPDATE_COMPUTER_POSTPONE] = "34"
    RESPONSE[ANTIVIRUS_UPDATE_VIRUS_DEFINITION] = "35"
    
    
    
class STRENGTH(object):
    STRENGTH_BLANK = "Blank"
    STRENGTH_VERYWEAK = "Very Weak"
    STRENGTH_WEAK = "Weak"
    STRENGTH_MEDIUM = "Medium"
    STRENGTH_STRONG = "Strong"
    STRENGTH_VERYSTRONG = "Very Strong"
    
    strength = {}
    strength[0] = STRENGTH_BLANK
    strength[1] = STRENGTH_VERYWEAK
    strength[2] = STRENGTH_WEAK
    strength[3] = STRENGTH_MEDIUM
    strength[4] = STRENGTH_STRONG
    strength[5] = STRENGTH_VERYSTRONG
    
    strengthColor = {}
    strengthColor[STRENGTH_BLANK] = "white"
    strengthColor[STRENGTH_VERYWEAK] = "red"
    strengthColor[STRENGTH_WEAK] = "red"
    strengthColor[STRENGTH_MEDIUM] = "blue"
    strengthColor[STRENGTH_STRONG] = "green"
    strengthColor[STRENGTH_VERYSTRONG] = "green"
    
class CONSTANTS:
    statesList = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
    stateAbbrList = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    gender_choices = ['Male', 'Female']
    GladstoneInfo = "INVENTORY_INFO_SHOW_GLADSTONE"
    DurableInfo = "INVENTORY_INFO_SHOW_DURABLE"
    mathUtilsQAOdictLen = -1
    import datetime
    today = datetime.date.today()
    date_today = str(today.month) + "|" + str(today.day) + "|" + str(today.year)
    import time
    from time import strftime
    startTime = strftime("%H:%M:%S:%MS", time.localtime())
            
class MATHASSOC_DIALOG(object):
    
#     DIALOG_INFO = [["Email-120009-f", "Email-120004-f"], ["Email-120005-f", "Email-120008-f"], ["Email-120007-f", "Email-120009-f"], ["Email-120001-f"],["Defender Scan", "Adobe1"], ["WindowsUpdate_new", "Java"]]
    DIALOG_INFO = [["WindowsUpdate", "Adobe1"], ["WindowsUpdate_new", "Java"], ["Email-120003-f", "Email-120004-f", "Defender Scan"], ["Email-120005-f", "Email-120008-f"], ["Email-120007-f", "Email-120009-f"], ["Email-120001-f"]]
    DIALOG_STATUS = [0, 1, 2]  # 0=uninitialized #1 initialized
    DIALOGCONTROLINFO = {}

    def changeStatusFromUntoInitialized(self, QAIndex, loadIndex):
        if self.DIALOGCONTROLINFO.has_key(QAIndex):
            if self.DIALOGCONTROLINFO.get(QAIndex)[loadIndex] == self.DIALOG_STATUS[0]:  # if uninitialized
                self.DIALOGCONTROLINFO.get(QAIndex)[loadIndex] = self.DIALOG_STATUS[1]  # change to initialized
            
    def changeStatusFromInitializedToClosed(self, QAIndex, loadIndex):    
        if self.DIALOGCONTROLINFO.has_key(QAIndex):
            if self.DIALOGCONTROLINFO.get(QAIndex)[loadIndex] == self.DIALOG_STATUS[1]:  # if initialized
                self.DIALOGCONTROLINFO.get(QAIndex)[loadIndex] = self.DIALOG_STATUS[2]  # change to closed
                
    # for that particular QA to close all the dialog boxes spawned by that must be closed before switching to next QA
    # return -1 if atleast one of the dialog box is initialized and not closed
    # return 0 else
    def checkForQACloseValidity(self, QAIndex):
        if  self.DIALOGCONTROLINFO.has_key(QAIndex):
            status = self.DIALOGCONTROLINFO.get(QAIndex)
            for eachStatus in status:
                 
                if not eachStatus == self.DIALOG_STATUS[0] and not eachStatus == self.DIALOG_STATUS[2]:
                    return -1
            return 0
                
            
    # 0 = dialog has not been initiated
    # 1 = dialog has been initiated
    # 2=dialog has been closed        
    def createEmptyQADictEntry(self, QAIndex):
        if not self.DIALOGCONTROLINFO.has_key(QAIndex):
            if QAIndex < len(self.DIALOG_INFO):
                initStatus = []
                l = len(self.DIALOG_INFO[QAIndex])
                for i in range(0, l):
                    initStatus.append(self.DIALOG_STATUS[0])
                self.DIALOGCONTROLINFO[QAIndex] = initStatus
                initStatus = None
    
    def getNoOfDialogForAQA(self, QAIndex):
        if QAIndex < len(self.DIALOG_INFO):
            return len(self.DIALOG_INFO[QAIndex])
        
   
math = MATHASSOC_DIALOG()  
floworderInstance = FLOWORDER()
utils = utils.utils()
propertyVar = propertyFile()
# propertyVar.init()
# fileOperation=FileOperation()
def __init__():
#     initiation of class file not class in globaltracker
    pass
# return list of [flowNumber, mathsNumber, loadIndex]
def getFlowNMathNAndLoadIndexFromEmailIndexID(emailIndexID):
    flowNumber = 0
    mathIndex = 0
    for eachFlow in floworderInstance.FLOWORDER:
        eachFlow = eachFlow.strip().lower()
        if eachFlow.startswith("email-"):
            emailInfo = eachFlow.split("-")
            emIndexID = emailInfo[1].strip()
            if emailIndexID == emIndexID:
                return [flowNumber, -1, -1]
            
        elif eachFlow == "m":
            loadIndex = 0
            for eachLoad in math.DIALOG_INFO[mathIndex]:
                eachLoad = eachLoad.strip().lower()
                if eachLoad.startswith("email-"):
                    emailInfo = eachLoad.split("-")
                    emIndexID = emailInfo[1].strip()
                    if emailIndexID == emIndexID:
                        return [flowNumber, mathIndex, loadIndex]
                loadIndex += 1
            mathIndex += 1
        flowNumber += 1
