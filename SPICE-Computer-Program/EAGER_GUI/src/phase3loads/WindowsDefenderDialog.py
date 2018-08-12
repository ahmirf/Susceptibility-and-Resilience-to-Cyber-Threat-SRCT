'''
Created on Jan 28, 2016

@author: AnjilaTam
'''
import wx

import CustomDialog,time
import globalTracker
from ttk import Style
from globalTracker import RESPONSECODE

InfoColor="#F5BA14"
timeElapsedGlobal="(%s:%s:%s)" % (0, 0, 0)


class WindowsDefenderDialog(CustomDialog.Dialog):
    
    def __init__(self, parent, loadNumber, mathsQNumber,startTime): 
        global allResponses
        WindowsDefenderDialog.allResponses=""
        global allResponseCode
        WindowsDefenderDialog.allResponseCode=""
#         print "===> VirusGUIalert.py initiated"
        width=520
        height=310
#         stime_= strftime("%H-%M-%S-%MS", time.localtime())
        self.dialogID = "500002"
        self.dialogTag = "WINDOWS_DEFENDER"
        self.name = "Windows Defender Malware Scan"
        self.startTime=startTime
        self.loadNumber = loadNumber
        self.mathsQNumber = mathsQNumber
        wx.Dialog.__init__(self,parent=None, id=-1, name='Virus Defender System') 
        wx.Dialog.SetSize(self, (width, height))
        self.SetTitle("Defender System")
        self.CenterOnScreen()
        globalTracker.math.changeStatusFromUntoInitialized(mathsQNumber, loadNumber)
        
        wx.Dialog.SetBackgroundColour(self, "#FFFFFF")
        panel = wx.Panel(self)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Calibri')
        Info=wx.TextCtrl(panel,value="PC Status: PROTECTED",style=wx.NO_BORDER|wx.TE_READONLY|wx.TE_RICH2)
        Info.SetStyle(0, len(Info.GetValue()), wx.TextAttr("white", font=self.font))
        
        Info.SetBackgroundColour("#067A04")
        nb = wx.Notebook(panel)

        # create the page windows as children of the notebook
        page1 = PageHome(nb)
        page2 = PageUpdate(nb)
        page3 = PageHistory(nb)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Home")
        nb.AddPage(page2, "Update")
        nb.AddPage(page3, "History")
        vSizer=wx.BoxSizer(wx.VERTICAL)
        vSizer.Add(Info,0,wx.EXPAND|wx.ALL,0)
        vSizer.Add(nb,1,wx.EXPAND)
        panel.SetSizer(vSizer)
        wx.CallAfter(nb.Refresh)

               
    def getDialogTag(self):
        return self.dialogTag
    
    def getDialogID(self):
        return self.dialogID 
        
        
    def onClose(self, event):
        globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        
        WindowsDefenderDialog.allResponses+="|"+RESPONSECODE.ANTIVIRUS_SCAN_CLOSE
        WindowsDefenderDialog.allResponseCode+="|"+RESPONSECODE.RESPONSE[RESPONSECODE.ANTIVIRUS_SCAN_CLOSE]
        
        RESPONSECODE.currentResponse=WindowsDefenderDialog.allResponses
        RESPONSECODE.currentResponseCode=WindowsDefenderDialog.allResponseCode
        self.Destroy()
        


class PageHome(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent,style=wx.ALL)
        wx.StaticBox(self, label='', pos=(6, 25), size=(460, 190),style=wx.ALL|wx.ALIGN_CENTER_HORIZONTAL)
        
        pnl=wx.Panel(self,pos=(1000,600),style=wx.ALL|wx.EXPAND)
#         searchImage = wx.Image(globalTracker.propertyVar.phase3images+"/search.png", type=wx.BITMAP_TYPE_ANY)
        searchImage = wx.Image(globalTracker.propertyVar.phase3images+"search.jpg", type=wx.BITMAP_TYPE_ANY)
        searchImage = searchImage.Scale(30, 30, wx.IMAGE_QUALITY_HIGH)
        searchImageBitmap = wx.StaticBitmap(pnl, bitmap=searchImage.ConvertToBitmap())
        self.hour = 0
        self.min = 0
        self.sec = 0
        
        info1 = wx.TextCtrl(pnl, value=" Your PC is being scanned ", size=(160,-1),style= wx.ALIGN_LEFT | wx.NO_BORDER|wx.TE_READONLY|wx.TE_RICH2)
        info1.SetStyle(0, len(info1.GetValue()), wx.TextAttr("Grey", font=wx.Font(9, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Times New Roman')))
        
        info2 = wx.TextCtrl(pnl, value="This might take some time, depending upon the size of files", size=(350,-1),style=wx.EXPAND | wx.ALIGN_LEFT | wx.NO_BORDER|wx.TE_READONLY|wx.TE_RICH2)
        info2.SetStyle(0, len(info2.GetValue()), wx.TextAttr("Grey", font=wx.Font(9, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Times New Roman')))
        
        self.gauge = wx.Gauge(pnl,-1, 50, pos=(205, 500), size=(295, 20)) 
        self.gauge.SetBezelFace(1) 
        self.gauge.SetShadowWidth(1) 
        
        buttonCancel = wx.Button(pnl, wx.ID_YES, "Cancel Scan")
        buttonCancel.Bind(wx.EVT_BUTTON, self.OnCancelScan, buttonCancel) 
#         self.Bind(wx.EVT_CLOSE, self.onClose)
        
        scanType = wx.StaticText(pnl, label="Scan Type: ", style=wx.EXPAND | wx.CENTER)
        scanTypeValue = wx.StaticText(pnl, label="Quick Scan ", style=wx.EXPAND | wx.CENTER)
        scanTypeValue.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas'))
        startTime = wx.StaticText(pnl, label="Start Time: ", style=wx.EXPAND | wx.CENTER)
        startTimeValue = wx.TextCtrl(pnl, style=wx.CENTER | wx.NO_BORDER|wx.TE_READONLY)
        startTimeValue.SetBackgroundColour("White")
        startTimeValue.SetValue(time.strftime("%H:%M:%S", time.localtime()))
        timeElapsed = wx.StaticText(pnl, label="Time elapsed:  ", style=wx.EXPAND | wx.CENTER)
        self.timeElapsedValue = wx.TextCtrl(pnl, style=wx.CENTER | wx.NO_BORDER|wx.TE_READONLY)
        self.timeElapsedValue.SetBackgroundColour("White")
        s = "(%s:%s:%s)" % (self.hour, self.min, self.sec)
        self.timeElapsedValue.SetValue(s)
        timeElapsedGlobal=s
        
        fSizer = wx.FlexGridSizer(3, 2, hgap=2, vgap=2)
        fSizer.Add(scanType, 0, wx.ALL, 1)
        fSizer.Add(scanTypeValue, 0, wx.ALL, 1)
        fSizer.Add(startTime, 0, wx.ALL, 1)
        fSizer.Add(startTimeValue, 0, wx.ALL, 1)
        fSizer.Add(timeElapsed, 0, wx.ALL, 1)
        fSizer.Add(self.timeElapsedValue, 0, wx.ALL, 1)
        
        infoSizer = wx.GridBagSizer(4, 2)
        infoSizer.Add(searchImageBitmap, pos=(0, 0),span=(2, 1), flag=wx.ALL|wx.EXPAND, border=5)
        infoSizer.Add(info1, pos=(0, 1), flag=wx.ALL, border=5)
        infoSizer.Add(info2, pos=(1, 1),span=(1, 2),flag=wx.ALL|wx.EXPAND, border=5)
        infoSizer.Add(self.gauge, pos=(2, 1),flag=wx.ALL|wx.EXPAND, border=6)
        infoSizer.Add(buttonCancel, pos=(2, 2), flag=wx.ALL | wx.EXPAND, border=2)
        infoSizer.Add(fSizer, pos=(3, 1))
        infoSizer.Layout()
        pnl.SetSizer(infoSizer)
        
        hSizer=wx.GridBagSizer(4,1)
        hSizer.Add(pnl,pos=(2,1))
        hSizer.AddGrowableCol(1)
        hSizer.AddGrowableRow(2)
        self.SetSizerAndFit(hSizer)
#         self.SetSizer(hSizer)
#         self.FitInside()
        self.Layout()
        self.elapsedTimetimer = wx.Timer(self) 
        self.Bind(wx.EVT_TIMER, self.OnElapsedTimeTimer, self.elapsedTimetimer) 
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.Ontimer, self.timer)
        self.count = 0
        self.elapsedTimetimer.Start(1000)
        self.timer.Start(100)

    isEnd=False        
    def OnElapsedTimeTimer(self, evt): 
        self.sec += 1
        if(self.sec >= 60):
            self.min += 1
            self.sec -= 60
        if(self.min >= 60):
            self.hour += 1
            self.min -= 60
        if not self.isEnd:
            s = "(%s:%s:%s)" % (self.hour, self.min, self.sec)
            self.timeElapsedValue.SetValue(s)
            timeElapsedGlobal=s
        
    def Ontimer(self, event): 
        self.count = self.count + 1 
        self.gauge.SetValue(self.count)
        if self.count == 50:
            self.timer.Stop()
            time.sleep(1)
            self.isEnd=True
#             self.Destroy()
            
    def OnCancelScan(self, event):
        print "... cancelling scanning"
        self.timer.Stop()
        self.elapsedTimetimer.Stop()
        time.sleep(1)
        
        WindowsDefenderDialog.allResponses+="|"+RESPONSECODE.ANTIVIRUS_SCAN_CANCEL
        WindowsDefenderDialog.allResponseCode+="|"+RESPONSECODE.RESPONSE[RESPONSECODE.ANTIVIRUS_SCAN_CANCEL]
#         self.Destroy()  


class PageUpdate(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
#         wx.Frame.SetSize(self, (width, height))
        wx.Panel.SetBackgroundColour(self,"White")

        panel = wx.Panel(self,size=(200,25))
        panel.SetBackgroundColour("White")
        wx.StaticBox(panel,id=-1, label='', pos=(5, 6), size=(520, 90),style=wx.ALL|wx.ALIGN_CENTER_HORIZONTAL)
        
        self.font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Calibri')
        Info=wx.TextCtrl(self,value="Check for new definitions",style=wx.NO_BORDER|wx.TE_READONLY|wx.TE_RICH2|wx.EXPAND)
        Info.SetStyle(0, len(Info.GetValue()), wx.TextAttr("white", font=self.font))
        Info.SetBackgroundColour(InfoColor)
        
        virusDefn_info = wx.StaticText(panel, label="New malware definitions help detect new harmful components\n and help better protect your system", style=wx.EXPAND | wx.CENTER)
        self.chkUpdateBtn = wx.Button(panel, wx.ID_YES, "Check for updates now")
        self.chkUpdateBtn.Bind(wx.EVT_BUTTON, self.OnCheckForVirusDefn_Update, self.chkUpdateBtn) 
        self.chkUpdateBtn.Show()
        
        fSizer = wx.GridBagSizer(3, 2)
        fSizer.Add(virusDefn_info, pos=(1,1),span=(2,1),flag=wx.ALL|wx.EXPAND, border=5)
        fSizer.Add(self.chkUpdateBtn, pos=(1,2),span=(3,1),flag=wx.ALL|wx.EXPAND, border=5)
        panel.SetSizer(fSizer)

        gbSizer=wx.BoxSizer(wx.VERTICAL)
        gbSizer.Add((100,15))
        gbSizer.Add(Info,0,wx.ALL|wx.EXPAND,2)
        gbSizer.Add(panel,1,wx.ALL|wx.EXPAND,2)
        gbSizer.Add((100,55))
       
        self.SetSizer(gbSizer)
        self.FitInside()
        self.Layout()
        
    def OnCheckForVirusDefn_Update(self,event):
#         print "check for new virus definition"
        WindowsDefenderDialog.allResponses+="|"+RESPONSECODE.ANTIVIRUS_UPDATE_VIRUS_DEFINITION
        WindowsDefenderDialog.allResponseCode+="|"+RESPONSECODE.RESPONSE[RESPONSECODE.ANTIVIRUS_UPDATE_VIRUS_DEFINITION]
        event.Skip()

class PageHistory(wx.Panel):
    def __init__(self, parent):
    
        self.startTimeValue= time.localtime()
        self.dialogID = "500003"
        self.dialogTag = "VIRUS_ALERT"
        self.name = "Virus alert"
#         wx.Frame.__init__(self,parent=None, id=-1, name='Virus Defender System') 
#         wx.Frame.SetSize(self, (width, height))
        wx.Panel.__init__(self, parent,style=wx.ALL)
        wx.Panel.SetBackgroundColour(self,"White")

        panel = wx.Panel(self,size=(200,25))
#         panel.SetBackgroundColour("Green")
        wx.StaticBox(panel, label='', pos=(-1, -7), size=(450, 70),style=wx.ALL|wx.ALIGN_CENTER_HORIZONTAL)
        
        self.font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Calibri')
        Info=wx.TextCtrl(self,value="Scan Statistics",style=wx.NO_BORDER|wx.TE_READONLY|wx.TE_RICH2|wx.EXPAND)
        Info.SetStyle(0, len(Info.GetValue()), wx.TextAttr("white", font=self.font))
        Info.SetBackgroundColour(InfoColor)
        
        scanType = wx.StaticText(panel, label="Scan Type: ", style=wx.EXPAND | wx.CENTER)
        scanTypeValue = wx.StaticText(panel, label="Quick Scan ", style=wx.EXPAND | wx.CENTER)
        scanTypeValue.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas'))
        startTime = wx.StaticText(panel, label="Start Time: ", style=wx.EXPAND | wx.CENTER)
        startTimeValue = wx.TextCtrl(panel, style=wx.CENTER | wx.NO_BORDER|wx.TE_READONLY)
        startTimeValue.SetBackgroundColour("White")
        startTimeValue.SetValue(time.strftime("%H:%M:%S", time.localtime()))
        timeElapsed = wx.StaticText(panel, label="Time elapsed:  ", style=wx.EXPAND | wx.CENTER)
        self.timeElapsedValue = wx.TextCtrl(panel, style=wx.CENTER | wx.NO_BORDER|wx.TE_READONLY)
        self.timeElapsedValue.SetBackgroundColour("White")
        self.timeElapsedValue.SetValue(timeElapsedGlobal)
        
        fSizer = wx.FlexGridSizer(3, 2, hgap=2, vgap=2)
        fSizer.Add(scanType, 0, wx.ALL, 2)
        fSizer.Add(scanTypeValue, 0, wx.ALL, 2)
        fSizer.Add(startTime, 0, wx.ALL, 2)
        fSizer.Add(startTimeValue, 0, wx.ALL, 2)
        fSizer.Add(timeElapsed, 0, wx.ALL, 2)
        fSizer.Add(self.timeElapsedValue, 0, wx.ALL, 2)
        panel.SetSizer(fSizer)
        
         
        panelStatus = wx.Panel(self,size=(200,100))
#         panelStatus.SetBackgroundColour("Red")
        wx.StaticBox(panelStatus, label='', pos=(-1, -7), size=(450, 90),style=wx.ALL|wx.ALIGN_CENTER_HORIZONTAL)
        InfoStatus=wx.TextCtrl(self,value="Status",style=wx.NO_BORDER|wx.TE_READONLY|wx.TE_RICH2|wx.EXPAND)
        InfoStatus.SetStyle(0, len(InfoStatus.GetValue()), wx.TextAttr("White", font=self.font))
        InfoStatus.SetBackgroundColour(InfoColor)
        
        lastScan = wx.StaticText(panelStatus, label="Last scan : ", style=wx.EXPAND | wx.CENTER)
        lastScanValue = wx.StaticText(panelStatus, label="Yesterday  ", style=wx.EXPAND | wx.CENTER)
        lastScanValue.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
        scanSchedule = wx.StaticText(panelStatus, label="Scan schedule: ", style=wx.EXPAND | wx.CENTER)
        scanScheduleValue = wx.TextCtrl(panelStatus, style=wx.EXPAND|wx.CENTER | wx.NO_BORDER|wx.TE_READONLY)
        scanScheduleValue.SetBackgroundColour("White")
#         scanScheduleValue.SetValue("Daily around "+time.strftime("%H:%M:%S", time.localtime())+" (Quick scan)")
        scanScheduleValue.SetValue("Daily around "+time.strftime("%H:%M:%S", self.startTimeValue)+" (Quick scan)")
        
        realTimepro = wx.StaticText(panelStatus, label="Real-time protection:  ", style=wx.EXPAND | wx.CENTER)
        self.realTimeproValue = wx.TextCtrl(panelStatus, value="On", style=wx.CENTER | wx.NO_BORDER|wx.TE_READONLY)
        self.realTimeproValue.SetBackgroundColour("White")
        
        StatusSizer = wx.FlexGridSizer(3, 2, hgap=2, vgap=2)
        StatusSizer.Add(lastScan, 0, wx.ALL, 2)
        StatusSizer.Add(lastScanValue, 1, wx.ALL|wx.EXPAND, 2)
        StatusSizer.Add(scanSchedule, 0, wx.ALL, 2)
        StatusSizer.Add(scanScheduleValue, 1, wx.ALL|wx.EXPAND, 2)
        StatusSizer.Add(realTimepro, 0, wx.ALL, 2)
        StatusSizer.Add(self.realTimeproValue, 1, wx.ALL|wx.EXPAND, 2)
        panelStatus.SetSizer(StatusSizer)
 
        gbSizer=wx.BoxSizer(wx.VERTICAL)
        gbSizer.Add((100,15))
        gbSizer.Add(Info,0,wx.ALL|wx.EXPAND,2)
        gbSizer.Add(panel,1,wx.ALL|wx.EXPAND)
        gbSizer.Add((100,35))
        
        gbSizer.Add(InfoStatus,0,wx.ALL|wx.EXPAND,2)
        gbSizer.Add(panelStatus,1,wx.ALL|wx.EXPAND)
        
        hsizer=wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add((25,5))
        hsizer.Add(gbSizer,1,wx.ALL)
        hsizer.Add((49,5))
        
        self.SetSizer(hsizer)
        self.FitInside()
        self.Layout() 
  
                
def main():
    ex = wx.App()
#     w = window(wx.Frame()) 
    dial = WindowsDefenderDialog()
    dial.Show()
#     dial.ShowModal()
#     print "response= "+RESPONSECODE.currentResponse+"\t"+RESPONSECODE.individualResponse
    ex.MainLoop()
    
    
if __name__ == "__main__":     
    main()
#     print RESPONSECODE.currentResponse