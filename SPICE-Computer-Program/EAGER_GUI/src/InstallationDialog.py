'''
Created on Jul 30, 2014

@author: Anjila
'''
import wx.html

import CustomDialog
from dialogMsgPojo import dialogMsgPojo
from dialogUtils import dialogUtils
import globalTracker,time
from globalTracker import RESPONSECODE,CONSTANTS
from globalTracker import globalVar

class InstallationDialog(CustomDialog.Dialog):

    text_1 = ''' <html>
    <body>
        <center>
            <table bgcolor="#FFAD33" cellspacing="3" >
                <tr>
                    <td align="left"><img src="WARN_ICON"></td>
                    <td id="message" align="leftwards"><font size="2">%(message)s</font></td>
                </tr>
            </table>
        </center>
        <table bgcolor="">
    '''
    text_2 = ''' </table>
    </body>
</html>
'''
    text_3 = '''
    '''
    def __init__(self, parent, dialogMsgPojo_,parent_emailPojo_,startTime): 
        print "InstallationDialog.py initiated"
        self.name = "Installation Dialog"
        self.type = 1
        self.dialogTag="INSTALLATION_DIALOG"
        self.count = 0
        self.rowCount = 0
        self.height = 150
        self.startTime=startTime
        self.dict = {}
        if not dialogMsgPojo_ == None and isinstance(dialogMsgPojo_, dialogMsgPojo):
            self.dict["message"] = dialogMsgPojo_.getMessage()
            self.getHMTLFOrNameValue(dialogMsgPojo_.getNameValuePairList())
        self.text_1=self.text_1.replace("WARN_ICON",globalTracker.propertyVar.phase3images+'warn.ico')
        self.text = self.text_1 + self.text_3 + self.text_2 
        wx.Dialog.__init__(self, parent, -1, 'User Account Control') 
        wx.Dialog.SetSize(self, (450, self.height))
        html = wx.html.HtmlWindow(self) 
        html.SetPage(self.text % self.dict)
        self.Layout()
        self.buttonY = wx.Button(self, wx.ID_YES, "Yes") 
        self.buttonY.Bind(wx.EVT_BUTTON, self.OnClickRestartNow, self.buttonY)
        self.buttonN = wx.Button(self, wx.ID_NO, "No")
        self.buttonN.Bind(wx.EVT_BUTTON, self.OnPostpone, self.buttonN) 
        self.buttonN.SetFocus()
        vSizer = wx.BoxSizer(wx.VERTICAL) 
        vSizer.Add(html, 1, wx.EXPAND | wx.ALL, 5) 
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(wx.StaticText(self), 1)
        hSizer.Add(self.buttonY, 0, wx.ALIGN_RIGHT | wx.ALL, 5) 
        hSizer.Add(self.buttonN, 0, wx.ALIGN_RIGHT | wx.ALL, 5) 
        vSizer.Add(hSizer, 0, wx.EXPAND | wx.ALIGN_RIGHT | wx.ALL, 5) 
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.SetSizer(vSizer) 
        self.Layout() 
        globalTracker.RESPONSECODE.responseLogBuffer =str(globalVar.flowNumber) + "\t" + "-1" + "\t" +parent_emailPojo_.get_indexId()  + "\t" + "" + "\t" + "" + "\t" +   ""  + "\t" +dialogMsgPojo_.getID()  + "\t" +self.dialogTag+"\t"
        
    def getHMTLFOrNameValue(self, nameValueList):
#         the name value list of dialogue msg pojo is provided and we can create the no of table rows dynamically by creating custon strign and attaching it to the dialog HTML at the rendering the HTML
        for nameValue in nameValueList:
            self.count += 1
            self.rowCount += 1
            name_value = nameValue.split("|")
            self.text_3 += "<tr><td height="'1'" align="'left'"><font size="'2'">%(" + str(self.count) + ")s </font></td><td align="'leftwards'"><font size="'2'">%(" + str(self.count + 1) + ")s </font></td></tr>"
            self.height += 25
            self.dict[str(self.count)] = name_value[0]
            if len(name_value) > 1 and not name_value[1] == None:
                self.dict[str(self.count + 1)] = name_value[1]
            self.count += 1
            
    def onClose(self,event):  
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.DIALOG_CLOSE
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
        globalTracker.RESPONSECODE.responseLogBuffer+=RESPONSECODE.currentResponse+"\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
        RESPONSECODE.SNo+=1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo)+"\t"+globalTracker.RESPONSECODE.responseLogBuffer)   
        self.Destroy()   
        
    def OnPostpone(self, event):
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.DIALOG_NO
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
        globalTracker.RESPONSECODE.responseLogBuffer+=RESPONSECODE.currentResponse+"\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
        RESPONSECODE.SNo+=1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo)+"\t"+globalTracker.RESPONSECODE.responseLogBuffer)
        self.Destroy()
        
    def OnClickRestartNow(self, event):
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.DIALOG_YES
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
            
        globalTracker.RESPONSECODE.responseLogBuffer+=RESPONSECODE.currentResponse+"\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
        RESPONSECODE.SNo+=1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo)+"\t"+globalTracker.RESPONSECODE.responseLogBuffer)
        self.Destroy()
        
def main():
    ex = wx.App()
    dmodule = dialogUtils()
    dialoglist = dmodule.readDialogFromFile("file/dialogMessages.txt")
    dial = InstallationDialog(None, dialoglist[0])
    result = dial.ShowModal()
    print result
    if result == wx.ID_CANCEL:
        dial.getButtonClickResult(wx.ID_CANCEL)
    ex.MainLoop()
