'''
Created on Jul 25, 2014

@author: AnjilaTam
'''

import os, wx, time, codecs,encodings, globalTracker
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from InstallationDialog import InstallationDialog
from dialogMsgPojo import dialogMsgPojo
from dialogUtils import dialogUtils
from emailPojo import emailPojo
from emailUtilsNew import emailUtilsNew
from globalTracker import RESPONSECODE, globalVar, CONSTANTS
from phase3loads import Form_resetEmailnPwd, Form_DOB, Form_username_pwd,InputUsername_Pwd
import wx.html as html
import wx.lib.agw.pybusyinfo as PBI

class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
#     self.inboxPanel, size=(-1, -1), style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL | wx.LC_HRULES
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent,id=-1, size=(-1, -1), style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL | wx.LC_HRULES)
        ListCtrlAutoWidthMixin.__init__(self)
        
class HtmlWindow_(html.HtmlWindow):
    def __init__(self, parent, id, style):
        html.HtmlWindow.__init__(self, parent, id, style=style)
        self.parent = parent

    def OnLinkClicked(self, link):
        startTime = time.strftime("%H:%M:%S", time.localtime())
        if not globalVar.emailPojo_ == None and isinstance(globalVar.emailPojo_, emailPojo):
            # change email status from 2(opne but no link clicked) to 4(open and link clicked)
            # 2 to 4
            globalTracker.floworderInstance.changeEmailStatusFromOpenButNoLinkClickToOpenNLinkClicked()
            RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
            RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
            RESPONSECODE.currentResponse = RESPONSECODE.EMAIL_OPEN_AND_LINK_CLICKED
            RESPONSECODE.currentResponseCode = RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
            globalTracker.RESPONSECODE.responseLogBuffer = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (str(globalVar.flowNumber) , "\t" , "" , "\t" , "" , "\t" , "" , "\t" , (globalVar.emailPojo_).get_indexId() , "\t" , (globalVar.emailPojo_).getEmailTag() , "\t" , "" , "\t" , "" , "\t" , RESPONSECODE.currentResponse , "\t" , RESPONSECODE.currentResponseCode, "\t" , RESPONSECODE.previousResponse, "\t" , RESPONSECODE.previousResponseCode, "\t" , startTime, "\t" , "", "\t", CONSTANTS.date_today, "\t", link.GetHref(), "\n")
            RESPONSECODE.SNo += 1
            globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo) + "\t" + globalTracker.RESPONSECODE.responseLogBuffer)
            
        hasDialog = False   
        if globalVar.indexofEmail >= 0 and not globalVar.dialogPojo_ == None and isinstance(globalVar.dialogPojo_, dialogMsgPojo):
            type_ = (globalVar.dialogPojo_).getType()
            if type_ in globalVar.dialogTypeEnum and not globalVar.dialogPojo_ == None:
                if globalVar.dialogTypeEnum[type_] == "1":
                    dlg = InstallationDialog(self.parent, globalVar.dialogPojo_, globalVar.emailPojo_, startTime)
                    hasDialog = True
                elif globalVar.dialogTypeEnum[type_] == "2":
                    dlg = Form_resetEmailnPwd.ResetEmailnPwd(self.parent, "Reset password", globalVar.emailPojo_, (globalVar.dialogPojo_).getID(), type_, startTime)
                    hasDialog = True
                elif globalVar.dialogTypeEnum[type_] == "3":
                    dlg = Form_DOB.GetDOBInfo(self.parent, "Get Lucky to win XBox", globalVar.emailPojo_, (globalVar.dialogPojo_).getID(), type_, startTime)
                    hasDialog = True
                elif globalVar.dialogTypeEnum[type_] == "4":
                    dlg = Form_username_pwd.GetUserNamenPwd(self.parent, "Login to win a FREE tour to Facebook", globalVar.emailPojo_, (globalVar.dialogPojo_).getID(), type_, startTime)
                    hasDialog = True
                elif globalVar.dialogTypeEnum[type_] == "5":
                    d = PBI.PyBusyInfo("Please wait! The information you requested is being accessed...", title="")
                    wx.Yield()
                    time.sleep(5)
                    del d
                    wx.MessageBox((globalVar.dialogPojo_).getMessage(), "Info", wx.ICON_INFORMATION)
                    hasDialog = False
                elif globalVar.dialogTypeEnum[type_] == "6":
                    d = PBI.PyBusyInfo("Please wait! The information you requested is being accessed...", title="")
                    wx.Yield()
                    time.sleep(5)
                    del d
                    wx.MessageBox((globalVar.dialogPojo_).getMessage(), "Info", wx.ICON_INFORMATION)
                    hasDialog = False
                elif globalVar.dialogTypeEnum[type_] == "7":
                    #show username password input dialog and if username and password matches, then only allow access to the information
                    dlg = InputUsername_Pwd.EmailLinkInputUsernamePwd(self.parent, "Login", globalVar.emailPojo_, (globalVar.dialogPojo_).getID(), type_, startTime)
                    dlg.ShowModal()
                    if dlg.uName_pwd_correct:
                        d = PBI.PyBusyInfo("Please wait! The information you requested is being accessed...", title="")
                        wx.Yield()
                        time.sleep(5)
                        del d
                        wx.MessageBox((globalVar.dialogPojo_).getMessage(), "Info", wx.ICON_INFORMATION)
                    hasDialog = False
                if hasDialog == True:
                    dlg.ShowModal()     
       
        
class emailMainFrame(wx.Frame):
    def __init__(self, parent, id, title, pos, size, style, emailFileLocation):
        print "emailModule.py initiated"
        wx.Frame.__init__(self, parent=parent, id=id, title=title, pos=pos, size=size, style=style)
        self.emailUtils = emailUtilsNew()
        self.emailUtils.load(emailFileLocation)
        self.dialogUtils_ = dialogUtils()
        self.emailVar = {}
        ############################key combo for Ctrl+Q then close the whole applicaiton ###########
        randomId = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onKeyCombo, id=randomId)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('Q'), randomId )])
        self.SetAcceleratorTable(accel_tbl)
        #################################################   
        self.dialogUtils_.load(os.path.abspath(globalTracker.propertyVar.dialogPath))
#         self.emailVar["name"] = globalTracker.propertyVar.participantName
        self.emailVar["name"] = globalTracker.globalVar.subjectName.encode('ascii', 'ignore')
        
        self.emailVar["company_name"] = globalTracker.propertyVar.companyName
        self.emailVar["company_email"] = globalTracker.propertyVar.companyEmail
        self.InitUI()
        
    def onKeyCombo(self, event):
        """"""
        print "You pressed CTRL+Q ==> Destroying email module"  
        self.Hide()
        self.Destroy()   
        event.Skip() 
        
    def InitUI(self):
        self.Bind(wx.EVT_CLOSE,self.onclose)
        self.mainPanel = wx.Panel(self)
        main_pnlSizer = wx.BoxSizer(wx.VERTICAL)
        main_pnlSizer.Add(self.mainPanel, 1, wx.EXPAND | wx.ALL, border=5)
        self.SetSizer(main_pnlSizer)
        self.leftPanel = wx.Panel(self.mainPanel)
        self.rightPanel = wx.Panel(self.mainPanel, style=wx.EXPAND)
        self.rightPanel.SetBackgroundColour('#FFFFFF')
        self.inboxPanel = wx.Panel(self.rightPanel, style=wx.DEFAULT | wx.EXPAND | wx.ALL)
        self.emailMsgPanel = wx.Panel(self.rightPanel, style=wx.DEFAULT | wx.EXPAND | wx.ALL)
        childEmail_msgPnlUpSizer = wx.GridBagSizer(7, 3)
        emailMsg_fieldTo = wx.StaticText(self.emailMsgPanel, label="To :")
        emailMsg_fieldFrom = wx.StaticText(self.emailMsgPanel, label="From :")
        emailMsg_fieldSubject = wx.StaticText(self.emailMsgPanel, label="Subject :")
        self.emailMsg_txto = wx.TextCtrl(self.emailMsgPanel, style=wx.EXPAND | wx.TE_READONLY)
        self.emailMsg_txtfrom = wx.TextCtrl(self.emailMsgPanel, style=wx.EXPAND | wx.TE_READONLY)
        self.emailMsg_txtsubject = wx.TextCtrl(self.emailMsgPanel, style=wx.EXPAND | wx.TE_READONLY)
        self.emailTextMessage = HtmlWindow_(self.emailMsgPanel, -1, style=html.HW_SCROLLBAR_AUTO)
        self.emailMsgPanel.SetBackgroundColour("#8080880")
        # email id that is unique to it is load but is hidden to the user
        self.emailMsg_txtemailId = wx.wx.TextCtrl(self.emailMsgPanel, style=wx.EXPAND | wx.TE_READONLY)
        self.emailMsg_txtemailId.Hide()
        
        childEmail_msgPnlUpSizer.Add(emailMsg_fieldTo, pos=(0, 0), flag=wx.ALL, border=3)
        childEmail_msgPnlUpSizer.Add(emailMsg_fieldFrom, pos=(1, 0), flag=wx.ALL, border=3)
        childEmail_msgPnlUpSizer.Add(emailMsg_fieldSubject, pos=(2, 0), flag=wx.ALL, border=3)
        childEmail_msgPnlUpSizer.Add(self.emailMsg_txto, pos=(0, 1), span=(1, 2), flag=wx.ALL | wx.EXPAND, border=3)
        childEmail_msgPnlUpSizer.Add(self.emailMsg_txtfrom, pos=(1, 1), span=(1, 2), flag=wx.ALL | wx.EXPAND, border=3)
        childEmail_msgPnlUpSizer.Add(self.emailMsg_txtsubject, pos=(2, 1), span=(1, 2), flag=wx.ALL | wx.EXPAND, border=3)
        childEmail_msgPnlUpSizer.Add(self.emailTextMessage, pos=(3, 0), span=(2, 3), flag=wx.ALL | wx.EXPAND, border=3)
        childEmail_msgPnlUpSizer.Add(self.emailMsg_txtemailId, pos=(6, 1), flag=wx.ALL | wx.EXPAND, border=3)
        childEmail_msgPnlUpSizer.AddGrowableRow(3)
        childEmail_msgPnlUpSizer.AddGrowableRow(4)
        childEmail_msgPnlUpSizer.AddGrowableCol(1)
        childEmail_msgPnlUpSizer.AddGrowableCol(2)
        inboxPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.emailMsgPanel.SetSizer(childEmail_msgPnlUpSizer)
        self.inboxListCtrl = AutoWidthListCtrl(self.inboxPanel)
        self.inboxListCtrl.InsertColumn(0, 'From')
        self.inboxListCtrl.InsertColumn(1, 'Subject')
        self.inboxListCtrl.InsertColumn(2, 'Date')
        
        self.inboxListCtrl.Bind(wx.EVT_LIST_INSERT_ITEM, self.OnInsertNewEmail, self.inboxListCtrl)
        self.inboxListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectEachEmail, self.inboxListCtrl)
        
        wx.EVT_LIST_KEY_DOWN
        
        inboxPanelSizer.Add(self.inboxListCtrl, 1, wx.EXPAND)
        self.inboxPanel.SetSizer(inboxPanelSizer)
        
        self.myEmailDict = {}
        
        hidePanelSizer = wx.BoxSizer(wx.VERTICAL)
        hidePanelSizer.Add(self.inboxPanel, 1, wx.EXPAND | wx.ALL, border=5)
        hidePanelSizer.Add(self.emailMsgPanel, 1, wx.EXPAND | wx.ALL, border=5)
        
        self.rightPanel.SetSizer(hidePanelSizer)
        self.rightPanel.Fit()  # #solved the issue of compose panel beign smaller than the inbox panel
        self.inbox_button = wx.Button(self.leftPanel, id=2, label="Inbox", size=wx.DefaultSize)
        self.Bind(wx.EVT_BUTTON, self.OnClickInbox, self.inbox_button, id=2)
        
        self.back_button = wx.Button(self.leftPanel, id=2, label="Back", size=wx.DefaultSize)
        self.Bind(wx.EVT_BUTTON, self.OnClickInbox, self.back_button, id=3)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.inbox_button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        vbox.Add(self.back_button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        self.leftPanel.Fit()
        self.leftPanel.SetSizer(vbox)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.leftPanel, flag=wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, border=10)
        hbox.Add(self.rightPanel, proportion=1, flag=wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, border=10)
        # #solved the issue of compose panel not expanding to the full screen 
        self.mainPanel.SetSizer(hbox)
        self.mainPanel.Fit()
        self.mainPanel.Layout() 
        self.inboxPanel.Show()
        self.emailMsgPanel.Hide()
        
    def onclose(self,event):
#         print "hide instead of cancel"
        self.Hide()
        
    def finalClose(self):
        self.Hide()
        self.Destroy()
        
    def OnInsertNewEmail(self, event):
        d = PBI.PyBusyInfo("You have new email in your inbox.", title="")
#         wx.Yield()
        time.sleep(1)
        del d
        event.Skip()
        
    def emailAddUpdate(self, event):
        self.emailUtils.addtoInboxFromReverse(self.inboxListCtrl, self.emailUtils.index,self.emailVar)
        self.emailUtils.index += 1
        
    def emailInSeries(self):
        self.emailUtils.addtoInboxFromReverse(self.inboxListCtrl, self.emailUtils.index,self.emailVar)
        self.emailUtils.index += 1
        
    def emailNext(self, emailIndexID, isForced, flowNummber, mathsQNumber, loadNumber, parent, mathsID, startTime): 
        ePojoObj = self.emailUtils.getePojoFromEmailIndexID(emailIndexID)
        self.emailUtils.addePojotoInboxFromReverse(self.inboxListCtrl, ePojoObj,self.emailVar)    
        self.emailUtils.index += 1
        mathsNumber = -1  
        if mathsQNumber == -1 and  loadNumber == -1:
            # for email not a maths load but independent of any math load
            mathsNumber = -1          
        elif mathsQNumber >= 0 and  loadNumber >= 0:
            mathsNumber = mathsQNumber          
        if isForced:
            # if we want user to forcefully see the email associated with the loads of the maths fields then pass True for isForced  
        # mathsQNumber, loadNumber fields will be used only when isForced is true and we need this two fields to keep track of their initialization 
        # along with the first openning of the email
        # since these email are associated as the property of the email
            globalTracker.floworderInstance.changeEmailStatusFromNotInserteToInserted(flowNummber, mathsQNumber, loadNumber)          
        RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse = RESPONSECODE.EMAIL_INSERTED_NOTOPENED
        RESPONSECODE.currentResponseCode = RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
        globalTracker.RESPONSECODE.responseLogBuffer = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (str(RESPONSECODE.flowSeq) , "\t" , str(mathsNumber), "\t", str(parent), "\t", mathsID, "\t", emailIndexID , "\t" , ePojoObj.getEmailTag() , "\t" , "" , "\t" , "" , "\t" , RESPONSECODE.currentResponse, "\t" , RESPONSECODE.currentResponseCode, "\t" , RESPONSECODE.previousResponse, "\t" , RESPONSECODE.previousResponseCode, "\t" , startTime, "\t" , "", "\t", CONSTANTS.date_today, "\n")
        RESPONSECODE.SNo += 1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo) + "\t" + globalTracker.RESPONSECODE.responseLogBuffer)  
    
    def OnSelectEachEmail(self, event):
        startTime = time.strftime("%H:%M:%S", time.localtime())
        index_selectedemail = event.GetIndex()
        self.inboxListCtrl.SetItemState(index_selectedemail, 0, wx.LIST_STATE_SELECTED)
        self.inboxListCtrl.SetItemFont(index_selectedemail, wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL,False, u'Arial'))  
        self.inboxPanel.Hide()
        ePojo = self.emailUtils.getEmailPojoFromDictByUUID(index_selectedemail)
        # #for tracking opened email:
        globalVar.indexofEmail = index_selectedemail
        if not ePojo == None:
            globalVar.emailPojo_ = ePojo
            globalVar.dialogPojo_ = self.dialogUtils_.getDialogPojoFrmDialoglistByID(ePojo.get_dialogueNumber())
            self.epojo = ePojo
            self.emailMsg_txto.SetValue((ePojo.get_to()) % self.emailVar)
            self.emailMsg_txtfrom.SetValue(ePojo.get_from_field() % self.emailVar)
            self.emailMsg_txtsubject.SetValue((ePojo.get_subject()) % self.emailVar)
            msg = ePojo.get_message()
           
            self.emailTextMessage.SetPage(msg % self.emailVar)
            self.emailMsg_txtemailId.SetValue(ePojo.get_indexId())
            self.emailMsgPanel.Layout()
            self.emailMsgPanel.Show()
            # check if the email has link
            # if has link: then change status from 1(inserted but not opened) to 2(open but no link clicked)
            # else if has no link: then change status from 1(inserted but not opened) to 3(open and has no link)
            # 1 to (2 or 3)
            flowMathLoadNumberList = globalTracker.getFlowNMathNAndLoadIndexFromEmailIndexID(self.epojo.get_indexId())
            RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
            RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
            if not flowMathLoadNumberList == None and len(flowMathLoadNumberList) == 3:
                globalVar.flowNumber = flowMathLoadNumberList[0]
                globalVar.mathsIndex = flowMathLoadNumberList[1]
                globalVar.LoadIndex = flowMathLoadNumberList[2]
                if self.epojo.getHasLink():
                    # 1 to (2)
                    globalTracker.floworderInstance.changeEmailStatusFromInsertedToOpenButNoLinkClicked(flowMathLoadNumberList)
                    RESPONSECODE.currentResponse = RESPONSECODE.EMAIL_OPEN_BUT_LINK_NOT_CLICKED
                else:
                    # 1 to (3)
                    globalTracker.floworderInstance.changeEmailStatusFromInsertedToOpenAndHasNoLink(flowMathLoadNumberList)
                    RESPONSECODE.currentResponse = RESPONSECODE.EMAIL_OPEN_HAS_NO_LINK
            
            RESPONSECODE.currentResponseCode = RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
            globalTracker.RESPONSECODE.responseLogBuffer = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (str(globalVar.flowNumber) , "\t" , "" , "\t" , "" , "\t" , "", "\t"  , self.epojo.get_indexId() , "\t" , self.epojo.getEmailTag() , "\t" , "" , "\t" , "" , "\t" , RESPONSECODE.currentResponse, "\t" , RESPONSECODE.currentResponseCode, "\t" , RESPONSECODE.previousResponse, "\t" , RESPONSECODE.previousResponseCode, "\t" , "", "\t" , startTime, "\t", CONSTANTS.date_today, "\n")
            RESPONSECODE.SNo += 1
            globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo) + "\t" + globalTracker.RESPONSECODE.responseLogBuffer)
        self.Layout()
    
    def OnClickInbox(self, event):
        # #method for showing inbox emails
        if event.Id == self.inbox_button.GetId():
#             print "click inbox"
            self.SetTitle("Department Email")
            self.inboxPanel.Show()
            self.emailMsgPanel.Hide()
        elif event.Id == self.compose_button.GetId():
#             print "click compose"
            self.SetTitle("Showing compose panel")
            self.inboxPanel.Hide()
            self.emailMsgPanel.Hide()
        self.Layout()
        
class App(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False, filename=None)
        
        
    def OnInit(self):
        emailFileLocation = "file/emailMessages.txt"
        frame = emailMainFrame(None, 1, "title", (10, 20), (590, 480), wx.DEFAULT_FRAME_STYLE, emailFileLocation)
        self.SetTopWindow(frame)
        frame.Show()
        return True
        
def main():
    print "in emailModule.py"
    app = App()
#     wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
    
if __name__ == "__main__":
    main()
   
    
