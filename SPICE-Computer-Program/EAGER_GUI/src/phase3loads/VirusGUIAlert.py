'''
Created on Apr 1, 2015

@author: Anjila
'''
import wx,CustomDialog,time
from globalTracker import RESPONSECODE
import wx.lib.agw.ultimatelistctrl as ULC
import globalTracker
from time import strftime

width = 550
THREAT_LEVEL = ["HIGH", "CRITICAL", "MEDIUM"]
ACTION = ["Remove"]
STATUS = ["Not Cleaned", "Successful"]

virusName = [("TrustWarrior", THREAT_LEVEL[0], ACTION[0], STATUS[0]), ("Virus: BAT-Gray.705", THREAT_LEVEL[2], ACTION[0], STATUS[0]), ("Virus:DOS/Dos7.419", THREAT_LEVEL[0], ACTION[0], STATUS[0]), ("Trojan-PSW.Win32.Fantast", THREAT_LEVEL[1], ACTION[0], STATUS[0]), ("Trojan-PSW.Win32.Hooker", THREAT_LEVEL[0], ACTION[0], STATUS[0]), ("Trojan-PSW.Win32.Dripper", THREAT_LEVEL[2], ACTION[0], STATUS[0])]

class windowsVirusAlertDialog(CustomDialog.Dialog):
    
    def __init__(self, parent): 
        
        print "===> VirusGUIalert.py initiated"
        
#         stime_= strftime("%H-%M-%S-%MS", time.localtime())
        self.dialogID = "500003"
        self.dialogTag = "VIRUS_ALERT"
        self.name = "Virus alert"
        wx.Dialog.__init__(self, parent=parent, id=-1, name='Virus Defender System') 
        wx.Dialog.SetSize(self, (width, 200 + len(virusName) * 25))
       
        ico = wx.Icon(globalTracker.propertyVar.phase3images + '/firewallIcon.png', wx.BITMAP_TYPE_ANY)
        self.SetIcon(ico)
        self.SetTitle("Virus Alert")
        self.CenterOnScreen()
#         globalTracker.math.changeStatusFromUntoInitialized(mathsQNumber, loadNumber)
        
        wx.Dialog.SetBackgroundColour(self, "#FFFFFF")
        panel = wx.Panel(self)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        threatDetectedInfo = wx.StaticText(panel, label="Threat Detected!", style=wx.EXPAND | wx.CENTER | wx.NO_BORDER)
        threatDetectedInfo.SetForegroundColour((255, 0, 0))  # set text color
        threatDetectedInfo.SetBackgroundColour("White")
        
        threatDetectedInfo.SetFont(wx.Font(24, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Times New Roman'))
        
        self.detectedThreatListCtrl = ULC.UltimateListCtrl(panel, wx.ID_ANY, agwStyle=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
        self.detectedThreatListCtrl.InsertColumn(0, "Detected Item", width=0.41 * width)
        self.detectedThreatListCtrl.InsertColumn(1, "Alert Level", width=0.166 * width)
        self.detectedThreatListCtrl.InsertColumn(2, "Action", width=0.166 * width)
        self.detectedThreatListCtrl.InsertColumn(3, "Status", width=0.166 * width)
        
        self.font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')
        self.prepareThreatList()

        sBox = wx.StaticBox(panel, label='', size=(width - 3, -1))
        sBoxsizer = wx.StaticBoxSizer(sBox, wx.VERTICAL)
        sBoxsizer.Add(self.detectedThreatListCtrl, 2, wx.ALL | wx.EXPAND, 2)
        
        self.btnIgnore = wx.Button(panel, wx.ID_YES, "Ignore All")
        self.btnIgnore.Bind(wx.EVT_BUTTON, self.OnVirusIgnoreAll, self.btnIgnore) 
        self.btnHeal = wx.Button(panel, wx.ID_YES, "Heal All")
        self.btnHeal.Bind(wx.EVT_BUTTON, self.OnVirusHealAll, self.btnHeal) 
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(self.btnIgnore, flag=wx.ALL | wx.CENTER | wx.EXPAND, border=4)
        hSizer.Add(self.btnHeal, flag=wx.ALL | wx.CENTER | wx.EXPAND, border=4)
        
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.Add(threatDetectedInfo, flag=wx.EXPAND | wx.ALL | wx.CENTER)
        vSizer.Add(sBoxsizer, 1)
        vSizer.Add(hSizer, flag=wx.CENTER | wx.ALL | wx.EXPAND)
        panel.SetSizer(vSizer, wx.EXPAND | wx.ALL) 
        self.Layout()
#         etime=strftime("%H-%M-%S-%MS", time.localtime())
#         print "time taken for virus alert dialog= %s %s "%(etime,stime_)
        
    def prepareThreatList(self):
        index = 0
        for threatName, alertLevel, action, status in virusName:
            self.threatAlertText = wx.TextCtrl(self.detectedThreatListCtrl, size=(0.163 * width, -1), style=wx.TE_RICH2 | wx.NO_BORDER, value=alertLevel)
            if alertLevel == THREAT_LEVEL[0] or alertLevel == THREAT_LEVEL[1]:  # high or #critical 
                self.threatAlertText.SetStyle(0, len(self.threatAlertText.GetValue()), wx.TextAttr("red", font=self.font))
            elif alertLevel == THREAT_LEVEL[2]:  # medium
                self.threatAlertText.SetStyle(0, len(self.threatAlertText.GetValue()), wx.TextAttr("#A29F55", font=self.font))
                
            self.action = wx.Button(self.detectedThreatListCtrl, id=1000 + index, label=action, size=(0.159 * width, -1), style=wx.CENTER, name="remove button")
            self.action.Bind(wx.EVT_LEFT_DOWN, self.onRemove, self.action)
           
            self.statusText = wx.TextCtrl(self.detectedThreatListCtrl, size=(0.159 * width, -1), style=wx.TE_RICH2 | wx.NO_BORDER, value=status)
            if status == STATUS[0]:  # "Not Cleaned"
                self.statusText.SetStyle(0, len(self.statusText.GetValue()), wx.TextAttr("#777777", font=self.font))  # color=grey
            elif status == STATUS[1]:  # "Successful"
                self.statusText.SetStyle(0, len(self.statusText.GetValue()), wx.TextAttr("#00AA00", font=self.font))  # color=green
                self.Layout()
            index = self.detectedThreatListCtrl.InsertStringItem(index, threatName)
            self.detectedThreatListCtrl.SetItemWindow(index, 1, self.threatAlertText)
            self.detectedThreatListCtrl.SetItemWindow(index, 2, self.action)
            self.detectedThreatListCtrl.SetItemWindow(index, 3, self.statusText)
            self.detectedThreatListCtrl.SetItemData(index, threatName)
            index += 1
            if status == STATUS[1]:  # "Successful"
                self.action.Disable()        

            
    def onRemove(self, event):
#         print "remove clicked"
        index = event.GetId() - 1000
        if index < len(virusName):
            statusText = self.detectedThreatListCtrl.GetItemWindow(index, 3)
            statusText.SetValue(STATUS[1])
            statusText.SetStyle(0, len(statusText.GetValue()), wx.TextAttr("#00AA00", font=self.font))  # color=green
            removeButton = self.detectedThreatListCtrl.GetItemWindow(index, 2)
            removeButton.Disable()  # Disable() dims the button and makes it unfunctional
            RESPONSECODE.individualResponse += self.detectedThreatListCtrl.GetItemData(index)+"|"
            RESPONSECODE.individualResponseCode += self.detectedThreatListCtrl.GetItemWindow(index, 1).GetValue()+"|"
       
        
    def getDialogTag(self):
        return self.dialogTag
    
    def getDialogID(self):
        return self.dialogID  
        
    def onClose(self, event):
#         print "on close" 
#         globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        
        if RESPONSECODE.currentResponse.startswith("VIRUS"):
            RESPONSECODE.currentResponse += "|" + RESPONSECODE.VIRUS_ALERT_CLOSE
            RESPONSECODE.currentResponseCode =RESPONSECODE.currentResponseCode+ "|" + RESPONSECODE.RESPONSE[RESPONSECODE.VIRUS_ALERT_CLOSE]
        else:
            RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
            RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
            RESPONSECODE.currentResponse = RESPONSECODE.VIRUS_ALERT_CLOSE
            RESPONSECODE.currentResponseCode = RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
        self.Destroy()
        
    def OnVirusIgnoreAll(self, event):
        
        if RESPONSECODE.currentResponse.startswith("VIRUS"):
            RESPONSECODE.currentResponse += "|" + RESPONSECODE.VIRUS_ALERT_IGNORE_ALL
            RESPONSECODE.currentResponseCode += "|" + RESPONSECODE.RESPONSE[RESPONSECODE.VIRUS_ALERT_IGNORE_ALL]
        else:
            RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
            RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
            RESPONSECODE.currentResponse = RESPONSECODE.VIRUS_ALERT_IGNORE_ALL
            RESPONSECODE.currentResponseCode = RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
        # todo: DISPLAY A DIALOG SAYING DO U REALLY WANT TO IGNORE THIS VIRUS ON YOUR SYSTEM(y/N)?
        dial = wx.MessageDialog(self, "Are you sure to quit?", "", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = dial.ShowModal()
        if ret == wx.ID_YES:
            self.Destroy()
        else:
            event.Skip()
        
    
    def OnVirusHealAll(self, event):
        # todo: SHOW A DIALOG SHOWING HEALING/ DELETING SOME VIRUS FILES     
        max = 40
        dlg = wx.ProgressDialog("Deleting...",
                               "Detected malicious files are being deleted... ",
                               maximum=max,
                               parent=None,
                               style=wx.PD_CAN_ABORT
                                | wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
                                | wx.PD_ELAPSED_TIME
                                | wx.PD_ESTIMATED_TIME
                                | wx.PD_REMAINING_TIME | wx.PD_SMOOTH
                                )

        keepGoing = True
        count = 0 
        i = 0
        noOfUpdateStatus = max / len(virusName)
        eachTerm = noOfUpdateStatus
#         print "noOfUpdateStatus= " + str(noOfUpdateStatus)
       
        while keepGoing and count < max:
            count += 1
            wx.MilliSleep(50)
            if count == eachTerm:
                
                eachTerm += noOfUpdateStatus
                index = i
                if index < len(virusName):
                    
                    statusText = self.detectedThreatListCtrl.GetItemWindow(index, 3)
                    if statusText.GetValue()==STATUS[0]:
                        statusText.SetValue(STATUS[1])    
                        RESPONSECODE.individualResponse+=self.detectedThreatListCtrl.GetItemData(index)+"|"
                        RESPONSECODE.individualResponseCode += self.detectedThreatListCtrl.GetItemWindow(index, 1).GetValue()+"|"
                    statusText.SetStyle(0, len(statusText.GetValue()), wx.TextAttr("#00AA00", font=self.font))  # color=green
                    removeButton = self.detectedThreatListCtrl.GetItemWindow(index, 2)
                    removeButton.Disable()  # Disable() dims the button and makes it unfunctional
                i += 1
            if count >= max:
                dlg.Destroy()
            else:
                (keepGoing, skip) = dlg.Update(count)
           
       
        dlg.ShowModal()
        if keepGoing == False:
            # progressDialog is closed by the user when the update returns False on this method
            if RESPONSECODE.currentResponse.startswith("VIRUS"):
                RESPONSECODE.currentResponse += RESPONSECODE.individualResponse
                RESPONSECODE.currentResponseCode += RESPONSECODE.individualResponseCode
            else:
                RESPONSECODE.currentResponse += RESPONSECODE.individualResponse
                RESPONSECODE.currentResponseCode += RESPONSECODE.individualResponseCode
                
            dlg.Destroy()
        else:
            #progress bar complete
            if RESPONSECODE.currentResponse.startswith("VIRUS"):
                RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
                RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
                RESPONSECODE.currentResponse = RESPONSECODE.VIRUS_ALERT_HEAL_ALL
                RESPONSECODE.currentResponseCode = RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
            else:   
                RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
                RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
                RESPONSECODE.currentResponse = RESPONSECODE.VIRUS_ALERT_HEAL_ALL
                RESPONSECODE.currentResponseCode = RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
            self.btnIgnore.Disable()
            self.btnHeal.Disable()
 

        
class window(wx.Window):     
    def __init__(self, parent):
        wx.Window.__init__(self, parent=parent, id=wx.ID_ANY, size=(520, 360), name="window")
        wx.Window.SetBackgroundColour(self, "Green")   
                
def main():
    ex = wx.App()
    w = window(wx.Frame(parent=None)) 
    dial = windowsVirusAlertDialog(w)
    dial.ShowModal()
#     print "response= "+RESPONSECODE.currentResponse+"\t"+RESPONSECODE.individualResponse
    ex.MainLoop()
    
    
if __name__ == "__main__":     
    main()
#     print RESPONSECODE.currentResponse
