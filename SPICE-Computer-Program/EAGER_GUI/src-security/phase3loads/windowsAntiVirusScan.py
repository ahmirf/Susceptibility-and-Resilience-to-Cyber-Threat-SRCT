'''
Created on Feb 24, 2015

@author: Anjila
'''
from multiprocessing import Event
import time

import wx, wx.html
import CustomDialog
from globalTracker import MATHASSOC_DIALOG,RESPONSECODE
import globalTracker


class WindowsAVScanDialog(CustomDialog.Dialog):

    def __init__(self, parent, loadNumber, mathsQNumber,startTime):
        print "windowsAntivirusScan.py initiated"
        self.dialogID="500002"
        self.dialogTag="MALWARE_SCAN"
        self.name = "Windows anti-virus scanner"
        self.startTime=startTime
        self.loadNumber = loadNumber
        self.mathsQNumber = mathsQNumber
        wx.Dialog.__init__(self, parent=parent, id=-1, name='Windows  Anti-virus Scanner') 
        wx.Dialog.SetSize(self, (542, 270))
        wx.Dialog.SetBackgroundColour(self, "#3E3E3E")
        globalTracker.math.changeStatusFromUntoInitialized(mathsQNumber, loadNumber)
        self.hour = 0
        self.min = 0
        self.sec = 0
        
        panel = wx.Panel(self)
        wx.StaticBox(panel, label='', pos=(6, 25), size=(523, 200))
        searchImage = wx.Image(globalTracker.propertyVar.phase3images+"/search.png", type=wx.BITMAP_TYPE_ANY)
        searchImage = searchImage.Scale(30, 30, wx.IMAGE_QUALITY_HIGH)
        panel1 = wx.Panel(panel)
        searchImageBitmap = wx.StaticBitmap(panel1, bitmap=searchImage.ConvertToBitmap())
        PCStatus = wx.StaticText(panel, label="   PC Status: Protected")
        PCStatus.SetBackgroundColour("#057B03")
        PCStatus.SetForegroundColour("#FFFFFF")
        PCStatus.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas'))
        info1 = wx.StaticText(panel, label="Windows Antivirus is scanning your PC", style=wx.EXPAND | wx.ALIGN_LEFT | wx.NO_BORDER)
        info1.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Times New Roman'))
        
        info2 = wx.StaticText(panel, label="This might take some time. Please wait...", style=wx.EXPAND | wx.ALIGN_LEFT | wx.NO_BORDER)
        
        self.gauge = wx.Gauge(panel, -1, 50, (255, 500), (375, 25)) 
        self.gauge.SetBezelFace(1) 
        self.gauge.SetShadowWidth(1) 
        
        buttonCancel = wx.Button(panel, wx.ID_YES, "Cancel Scan")
        buttonCancel.Bind(wx.EVT_BUTTON, self.OnCancelScan, buttonCancel) 
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        scanType = wx.StaticText(panel, label="Scan Type: ", style=wx.EXPAND | wx.CENTER)
        scanTypeValue = wx.StaticText(panel, label="Quick Scan ", style=wx.EXPAND | wx.CENTER)
        scanTypeValue.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas'))
        startTime = wx.StaticText(panel, label="Start Time: ", style=wx.EXPAND | wx.CENTER)
        startTimeValue = wx.TextCtrl(panel, style=wx.CENTER | wx.NO_BORDER)
        startTimeValue.SetValue(time.strftime("%H:%M:%S", time.localtime()))
        timeElapsed = wx.StaticText(panel, label="Time elapsed:  ", style=wx.EXPAND | wx.CENTER)
        self.timeElapsedValue = wx.TextCtrl(panel, style=wx.CENTER | wx.NO_BORDER)
        s = "(%s:%s:%s)" % (self.hour, self.min, self.sec)
        self.timeElapsedValue.SetValue(s)
        
        fSizer = wx.FlexGridSizer(3, 2, hgap=2, vgap=2)
        fSizer.Add(scanType, 0, wx.ALL, 1)
        fSizer.Add(scanTypeValue, 0, wx.ALL, 1)
        fSizer.Add(startTime, 0, wx.ALL, 1)
        fSizer.Add(startTimeValue, 0, wx.ALL, 1)
        fSizer.Add(timeElapsed, 0, wx.ALL, 1)
        fSizer.Add(self.timeElapsedValue, 0, wx.ALL, 1)
     
        gSizer = wx.GridBagSizer(5, 3)
        gSizer.Add(panel1, pos=(1, 0), flag=wx.ALL, border=10)
        gSizer.Add(info1, pos=(1, 1))
        gSizer.Add(info2, pos=(2, 1))
        gSizer.Add(self.gauge, pos=(3, 1))
        gSizer.Add(buttonCancel, pos=(3, 2), flag=wx.ALL | wx.EXPAND, border=1)
        gSizer.Add(fSizer, pos=(4, 1))
        gSizer.Layout()

        vSizer = wx.BoxSizer(wx.VERTICAL) 
        vSizer.Add(PCStatus, 0, wx.EXPAND | wx.ALL, 0) 
        vSizer.Add(gSizer, 0, wx.EXPAND | wx.ALL, 2) 
        self.SetBackgroundColour("White")
        
        panel.SetSizer(vSizer) 
        self.FitInside()
        self.Layout()
       
        self.elapsedTimetimer = wx.Timer(self) 
        self.Bind(wx.EVT_TIMER, self.OnElapsedTimeTimer, self.elapsedTimetimer) 
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.Ontimer, self.timer)
        self.count = 0
        self.elapsedTimetimer.Start(1000)
        self.timer.Start(100)
       
    def getDialogTag(self):
        return self.dialogTag
    
    def getDialogID(self):
        return self.dialogID  

    def OnElapsedTimeTimer(self, evt): 
        self.sec += 1
        if(self.sec >= 60):
            self.min += 1
            self.sec -= 60
        if(self.min >= 60):
            self.hour += 1
            self.min -= 60
        s = "(%s:%s:%s)" % (self.hour, self.min, self.sec)
        self.timeElapsedValue.SetValue(s)
        
    def Ontimer(self, event): 
        self.count = self.count + 1 
        self.gauge.SetValue(self.count)
        if self.count == 50:
            self.timer.Stop()
            time.sleep(1)
            globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
            self.Destroy()
            

    def OnCancelScan(self, event):
        print "... cancelling scanning"
        self.timer.Stop()
        self.elapsedTimetimer.Stop()
        time.sleep(1)
        globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.ANTIVIRUS_SCAN_CANCEL
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
        
        self.Destroy()
    
    def onClose(self, event):
        print "... closing Antivirus scan dialog"
        globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.ANTIVIRUS_SCAN_CLOSE
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
        self.Destroy()

class window(wx.Window):     
    def __init__(self, parent):
        wx.Window.__init__(self, parent=parent, id=wx.ID_ANY, size=(520, 360), name="window")
        wx.Window.SetBackgroundColour(self, "Green")   
             
def main():
    ex = wx.App()
    w = window(wx.Frame(parent=None))
   
    dial = WindowsAVScanDialog(w)
    result = dial.ShowModal()
    w.Show()
    
#     print result
#     if result == wx.ID_CANCEL:
#         dial.getButtonClickResult(wx.ID_CANCEL)
    ex.MainLoop()
if __name__ == "__main__":     
    main()
