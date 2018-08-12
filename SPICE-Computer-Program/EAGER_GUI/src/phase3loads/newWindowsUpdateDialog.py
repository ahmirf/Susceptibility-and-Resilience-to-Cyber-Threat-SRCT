'''
Created on Jan 27, 2016

@author: AnjilaTam
'''
import CustomDialog
import globalTracker,wx,wx.html,time
from wx.lib.pubsub import pub
from globalTracker import RESPONSECODE, CONSTANTS


text = ''' <html>
    <body >
        <center>
            <table bgcolor="#FFAD33" width="100%%" cellpadding="0" border="0">
                <tr>
                    <td align="left"><img src="./icons/warn.ico"></td>
                    <td id="message" align="leftwards">%(message)s</font></td>
                </tr>
            </table>
        </center>
        <table width="100%%">
        <tr><td>Windows can't update important files and services while the system is using them. Make sure to save your files before restarting.</td>
        </tr>      
    </table>
    </body>
</html>
'''

OptionSelectedGloba=""
class newWindowsUpdateDialog(CustomDialog.Dialog):
    
    def __init__(self, parent, loadNumber, mathsQNumber, startTime): 
        print "windowsUpdateDialog.py initiated"
        self.name = "Windows Update Dialog"
        self.type = 1
        self.startTime = startTime
        self.height = 230
        self.loadNumber = loadNumber
        self.mathsQNumber = mathsQNumber
        self.dialogID = "500011"
        self.dialogTag = "WINDOWS_UPDATE_NEW"
        self.responseLogContent = globalTracker.RESPONSECODE.responseLogBuffer
        self.selectedOption="" 
#         self.utils=utils
        self.dict = {}
        
#         change the status of dialog from 0(uninitialized) to 1(initialized)
#         if not dialogMsgPojo_ == None and isinstance(dialogMsgPojo_, dialogMsgPojo):
        self.dict["message"] = "Important Updates are available"
#             self.getHMTLFOrNameValue(dialogMsgPojo_.getNameValuePairList())
#         
#         self.text = self.text_1 + self.text_3 + self.text_2 
#         
#         wx.Frame.__init__(self, parent, -1, 'Important Updates are available') 
#         wx.Frame.SetSize(self, (420, self.height))
        wx.Dialog.__init__(self, parent, -1, 'Important Updates') 
        globalTracker.math.changeStatusFromUntoInitialized(mathsQNumber, loadNumber)
        
        wx.Dialog.SetSize(self, (420, self.height))
        
        html = wx.html.HtmlWindow(self)
        html.SetPage(text % self.dict)
        html.Fit()
        self.Layout()
        
        distros = ['Try in 10 Minutes', 'Try in an Hour', 'Try Tonight', 'Remind Me Tomorrow']
        self.cb = wx.ComboBox(self,  choices=distros, 
            style=wx.CB_READONLY)
        self.cb.SetSelection(1)
        OptiionSelectedGloba=distros[self.cb.GetSelection()]
        self.cb.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        
        hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer1.Add(wx.StaticText(self, label="Remind me in :"), 1, wx.ALL, 2)
        hSizer1.Add(self.cb, 1,wx.ALIGN_RIGHT | wx.ALL|wx.EXPAND, 1)
        
        
        self.buttonY = wx.Button(self, wx.ID_YES, "Restart now") 
        self.buttonY.Bind(wx.EVT_BUTTON, self.OnClickRestartNow, self.buttonY)
        
        self.buttonN = wx.Button(self, wx.ID_YES, "Postpone")
        self.buttonN.Bind(wx.EVT_BUTTON, self.OnPostpone, self.buttonN) 
        self.buttonN.SetFocus()
        
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        vSizer = wx.BoxSizer(wx.VERTICAL) 
        vSizer.Add(html, 1, wx.EXPAND, 0)
        vSizer.Add(hSizer1, 0, wx.EXPAND|wx.ALL, 2) 
        
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(wx.StaticText(self), 1)
        hSizer.Add(self.buttonY, 0, wx.ALIGN_RIGHT | wx.ALL, 5) 
        hSizer.Add(self.buttonN, 0, wx.ALIGN_RIGHT | wx.ALL, 5) 
        vSizer.Add(hSizer, 0, wx.EXPAND | wx.ALIGN_RIGHT | wx.ALL, 5) 
        self.SetBackgroundColour("White")
        self.SetSizer(vSizer) 
        self.Layout() 
        
    def getDialogTag(self):
        return self.dialogTag
    
    def getDialogID(self):
        return self.dialogID
        
    def OnPostpone(self, event):
#         self.getButtonClickResult("NO")
        globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        
        RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse = RESPONSECODE.UPDATE_COMPUTER_POSTPONE+"|"+OptionSelectedGloba
        RESPONSECODE.currentResponseCode = RESPONSECODE.RESPONSE[RESPONSECODE.UPDATE_COMPUTER_POSTPONE]
        
#         self.responseLogContent+= "" + "\t" + "" + "\t" + self.getDialogID() + "\t" + self.getDialogTag() + "\t" + RESPONSECODE.currentResponse + "\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
        self.responseLogContent += "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % ("" , "\t" , "" , "\t" , self.getDialogID(), "\t" , self.getDialogTag() , "\t" , RESPONSECODE.currentResponse , "\t" , RESPONSECODE.currentResponseCode, "\t" , RESPONSECODE.previousResponse, "\t" , RESPONSECODE.previousResponseCode, "\t" , self.startTime, "\t" , (time.strftime("%H:%M:%S", time.localtime())), "\t", CONSTANTS.date_today, "\t",self.selectedOption,"\n")
        RESPONSECODE.SNo += 1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo) + "\t" + self.responseLogContent)
#         print "changed status"
        self.Destroy()
        
    def onClose(self, event):
#         print "changed status"
        globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse = RESPONSECODE.UPDATE_COMPUTER_CLOSE
        RESPONSECODE.currentResponseCode = RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
#         self.responseLogContent+= "" + "\t" + "" + "\t" + self.getDialogID() + "\t" + self.getDialogTag() + "\t" + RESPONSECODE.currentResponse + "\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
        self.responseLogContent = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % ("" , "\t" , "" , "\t" , self.getDialogID(), "\t" , self.getDialogTag() , "\t" , RESPONSECODE.currentResponse , "\t" , RESPONSECODE.currentResponseCode, "\t" , RESPONSECODE.previousResponse, "\t" , RESPONSECODE.previousResponseCode, "\t" , self.startTime, "\t" , (time.strftime("%H:%M:%S", time.localtime())), "\t", CONSTANTS.date_today,"\t",self.selectedOption, "\n")
        RESPONSECODE.SNo += 1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo) + "\t" + self.responseLogContent)
        self.Destroy()
        
    def OnClickRestartNow(self, event): 
        max = 40        
        RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse = RESPONSECODE.UPDATE_COMPUTER_RESTARTNOW
        RESPONSECODE.currentResponseCode = RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
#         
        dlg = wx.ProgressDialog("Automatic updates",
                               "Updates are being installed... ",
                               maximum=max,
                               parent=None,
                               style=wx.PD_CAN_ABORT
                                | wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
                                | wx.PD_ELAPSED_TIME
                                | wx.PD_ESTIMATED_TIME
                                | wx.PD_REMAINING_TIME | wx.PD_SMOOTH
                                )
  
#         dlg = MyProgressDialog(parent=None, id=-1, title="Automatic updates", text="Updates are being installed... ")
#         self.Bind(wx.EVT_CLOSE, self.onProgressBarClosed, dlg)
#         re = dlg.ShowModal()
#         print re
        keepGoing = True
        count = 0
#         
        st = wx.GetCurrentTime()
        while keepGoing and count < max:
            count += 1
            wx.MilliSleep(200)
   
            if count >= max:
                dlg.Destroy()
                globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
#                 print "changed status"
                self.Destroy()
            else:
                (keepGoing, skip) = dlg.Update(count)
        dlg.ShowModal()
        if keepGoing == False:
            # progressDialog is closed by the user when the update returns False on this method
            RESPONSECODE.currentResponse += "|" + RESPONSECODE.PROGRESSBAR_INCOMPLETE
        else:
            RESPONSECODE.currentResponse += "|" + RESPONSECODE.PROGRESSBAR_COMPLETE
        
#         self.responseLogContent+= "" + "\t" + "" + "\t" + self.getDialogID() + "\t" + self.getDialogTag() + "\t" + RESPONSECODE.currentResponse + "\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
        self.responseLogContent = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % ("" , "\t" , "" , "\t" , self.getDialogID(), "\t" , self.getDialogTag() , "\t" , RESPONSECODE.currentResponse , "\t" , RESPONSECODE.currentResponseCode, "\t" , RESPONSECODE.previousResponse, "\t" , RESPONSECODE.previousResponseCode, "\t" , self.startTime, "\t" , (time.strftime("%H:%M:%S", time.localtime())), "\t", CONSTANTS.date_today, "\t",self.selectedOption,"\n")
        RESPONSECODE.SNo += 1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo) + "\t" + self.responseLogContent)
        dlg.Destroy()
#         self.getButtonClickResult("YES")
        
    def OnSelect(self,event):
        self.selectedOption = event.GetString()
        OptionSelectedGloba= self.selectedOption

        
    def getResult(self):
        return self.click
        

       
class MyProgressDialog(wx.Dialog):
    def __init__(self, parent, id, title, text=''):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 90), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.count = 0
        self.text = wx.StaticText(self, -1, text)
        self.gauge = wx.Gauge(parent=self, id=-1, range=20, size=(270, -1), style=wx.GA_HORIZONTAL)
#         Gauge(parent, id=ID_ANY, range=100, pos=DefaultPosition,
#       size=DefaultSize, style=GA_HORIZONTAL, validator=DefaultValidator,
#       name=GaugeNameStr)
#         
        self.closebutton = wx.Button(self, wx.ID_CLOSE)
        self.closebutton.Bind(wx.EVT_BUTTON, self.OnButtonClose)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text, 0 , wx.EXPAND)
        sizer.Add(self.gauge, 0, wx.ALIGN_CENTER)
        sizer.Add(self.closebutton, 0, wx.ALIGN_CENTER)

        self.SetSizer(sizer)
        self.Show()
        pub.subscribe(self.updateProgress, "update")
        for i in range(20):
            time.sleep(1)
            wx.CallAfter(pub.sendMessage, "update", msg="")
   
        
    def OnButtonClose(self, event):
        self.Destroy() 
        # can add stuff here to do in parent.
        
    def updateProgress(self, msg):
        """"""
        self.count += 1
 
        if self.count >= 20:
            self.Destroy()
 
        self.gauge.SetValue(self.count)
        

     
def main():
    ex = wx.App()
#     dmodule = dialogUtils()
#     dialoglist = dmodule.readDialogFromFile("file/dialogMessages.txt")


    dial = newWindowsUpdateDialog(None, 1, 3,time.localtime())
#     dial.ShowModal()
    dial.ShowModal()


    ex.MainLoop()
if __name__ == '__main__': 
    main()
     

