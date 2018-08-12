'''
Created on Feb 19, 2015

@author: Anjila
'''
import time

import wx.html
from wx.lib.pubsub import pub

import CustomDialog
import globalTracker
from globalTracker import RESPONSECODE,CONSTANTS

text = ''' <html>
    <body>
        <center>
            <table bgcolor="#FFAD33" width="100%%" >
                <tr>
                    <td align="left"><img src="./icons/warn.ico"></td>
                    <td id="message" align="leftwards">%(message)s</font></td>
                </tr>
            </table>
        </center>
        <table bgcolor="" width="100%%">
        <tr><td>updates related to computer performance are available.<br>Do you want to update your computer?</td>
        </tr>
        
    </table>
    </body>
</html>
'''

class windowsUpdateDialog(CustomDialog.Dialog):
    
    def __init__(self, parent, loadNumber, mathsQNumber,startTime): 
        print "windowsUpdateDialog.py initiated"
        self.name = "Windows Update Dialog"
        self.type = 1
        self.click = ""
        self.count = 0
        self.rowCount = 0
        self.startTime=startTime
        self.height = 220
        self.loadNumber = loadNumber
        self.mathsQNumber = mathsQNumber
        self.dialogID = "500000"
        self.dialogTag = "WINDOWS_UPDATE"
        self.responseLogContent=globalTracker.RESPONSECODE.responseLogBuffer 
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
        wx.Dialog.__init__(self, parent, -1, 'Important Updates are available') 
        globalTracker.math.changeStatusFromUntoInitialized(mathsQNumber, loadNumber)
        
        wx.Dialog.SetSize(self, (420, self.height))
        html = wx.html.HtmlWindow(self)
        html.SetPage(text % self.dict)
        
        self.Layout()
        self.buttonY = wx.Button(self, wx.ID_YES, "Yes") 
        self.buttonY.Bind(wx.EVT_BUTTON, self.OnClickRestartNow, self.buttonY)
        
        self.buttonN = wx.Button(self, wx.ID_YES, "No")
        self.buttonN.Bind(wx.EVT_BUTTON, self.OnPostpone, self.buttonN) 
        self.buttonN.SetFocus()
        
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        vSizer = wx.BoxSizer(wx.VERTICAL) 
        vSizer.Add(html, 1, wx.EXPAND | wx.ALL, 5) 
        
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
        self.getButtonClickResult("NO")
        globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.UPDATE_COMPUTER_NO
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
#        self.responseLogContent+= "" + "\t" + "" + "\t" + self.getDialogID() + "\t" + self.getDialogTag() + "\t" + RESPONSECODE.currentResponse + "\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
#        self.responseLogContent+="%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s"%("" , "\t" , "" , "\t" ,self.getDialogID(), "\t" , self.getDialogTag() , "\t" , RESPONSECODE.currentResponse ,"\t" ,RESPONSECODE.currentResponseCode,"\t" ,RESPONSECODE.previousResponse, "\t" ,RESPONSECODE.previousResponseCode,"\t" ,self.startTime,"\t" ,(time.strftime("%H:%M:%S", time.localtime())),"\t",CONSTANTS.date_today,"\n")
#        self.responseLogContent+="%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (str(RESPONSECODE.flowSeq) , "\t" , "" , "\t" , "-1" , "\t" , "" , "\t" , "" , "\t" , "" , "\t" , self.getDialogID() , "\t" , self.getDialogTag() , "\t" , RESPONSECODE.currentResponse , "\t" , RESPONSECODE.currentResponseCode, "\t" , RESPONSECODE.previousResponse, "\t" , RESPONSECODE.previousResponseCode, "\t" , startTime, "\t" , (time.strftime("%H:%M:%S", time.localtime())), "\t", CONSTANTS.date_today, "\n")
        self.responseLogContent+="\t".join(( "" , "" , self.getDialogID() , self.getDialogTag() , RESPONSECODE.currentResponse , RESPONSECODE.currentResponseCode, RESPONSECODE.previousResponse, RESPONSECODE.previousResponseCode, self.startTime, (time.strftime("%H:%M:%S", time.localtime())), CONSTANTS.date_today, "\n"))
        RESPONSECODE.SNo+=1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo)+"\t"+self.responseLogContent)
#         print "changed status"
        self.Destroy()
        
    def onClose(self, event):
#         print "changed status"
        globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.UPDATE_COMPUTER_CLOSE
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
#         self.responseLogContent+= "" + "\t" + "" + "\t" + self.getDialogID() + "\t" + self.getDialogTag() + "\t" + RESPONSECODE.currentResponse + "\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
        self.responseLogContent+="\t".join(( "" , "" , self.getDialogID() , self.getDialogTag() , RESPONSECODE.currentResponse , RESPONSECODE.currentResponseCode, RESPONSECODE.previousResponse, RESPONSECODE.previousResponseCode, self.startTime, (time.strftime("%H:%M:%S", time.localtime())), CONSTANTS.date_today, "\n"))
        RESPONSECODE.SNo+=1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo)+"\t"+self.responseLogContent)
        self.Destroy()
        
    def OnClickRestartNow(self, event):
        self.responseLogContent=globalTracker.RESPONSECODE.responseLogBuffer 
        max = 40        
        RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse = RESPONSECODE.UPDATE_COMPUTER_YES
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
            dlg.Destroy()
        else:
            RESPONSECODE.currentResponse += "|" + RESPONSECODE.PROGRESSBAR_COMPLETE
            dlg.Destroy()
        
#         self.responseLogContent+= "" + "\t" + "" + "\t" + self.getDialogID() + "\t" + self.getDialogTag() + "\t" + RESPONSECODE.currentResponse + "\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
#        self.responseLogContent = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % ("" , "\t" , "" , "\t" , self.getDialogID(), "\t" , self.getDialogTag() , "\t" , RESPONSECODE.currentResponse , "\t" , RESPONSECODE.currentResponseCode, "\t" , RESPONSECODE.previousResponse, "\t" , RESPONSECODE.previousResponseCode, "\t" , self.startTime, "\t" , (time.strftime("%H:%M:%S", time.localtime())), "\t", CONSTANTS.date_today, "\t",self.selectedOption,"\n")
        self.responseLogContent+="\t".join(( "" , "" , self.getDialogID() , self.getDialogTag() , RESPONSECODE.currentResponse , RESPONSECODE.currentResponseCode, RESPONSECODE.previousResponse, RESPONSECODE.previousResponseCode, self.startTime, (time.strftime("%H:%M:%S", time.localtime())), CONSTANTS.date_today, "\n"))

        RESPONSECODE.SNo += 1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo) + "\t" + self.responseLogContent)
        self.responseLogContent=globalTracker.RESPONSECODE.responseLogBuffer 
        
    def getResult(self):
        return self.click
        
    def getButtonClickResult(self, click):
        self.click = click
        if click == "YES" or click == 5103:
            
            return 5103
        elif click == "NO" or click == 5104:
            return 5104
        elif click == "CANCEL" or click == 5101:
            return 5101
       
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
        print "onclose =="
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


    dial = windowsUpdateDialog(None, 1, 3)
#     dial.ShowModal()
    dial.ShowModal()


    ex.MainLoop()
if __name__ == '__main__': 
    main()
     
