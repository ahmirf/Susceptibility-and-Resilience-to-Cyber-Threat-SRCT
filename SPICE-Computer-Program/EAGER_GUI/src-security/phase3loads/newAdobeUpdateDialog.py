'''
Created on Jan 24, 2016

@author: AnjilaTam
'''
import wx.html

import CustomDialog
import globalTracker
from dialogUtils import dialogUtils
from globalTracker import MATHASSOC_DIALOG, RESPONSECODE


class newAdobeUpdateDialog(CustomDialog.Dialog):
    text = '''
    <html>
    <head>

</head>
<body  bgcolor="#767676" link="#C0C0C0" >
<table bgcolor="#767676" width="100%%" cellpadding="0" border="0" cellspacing="0" margin="0" outline="0">
<tr>
    <td cellpadding="0" cellspacing="0" >
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="IMG_SRC" height="65" width="60"/>
        
    </td>
    <td cellpadding="0" cellspacing="0" >
        <font size="4" face="calibri" color="white">An update to Adobe Flash Player is available.<br><br>
        <ul>
            <li>Superior HD video performance with hardware acceleration of video</li>
            <li>Support for full screen mode with multiple monitors</li>
            <li>Faster graphics rendering support with Internet Explorer 9</li>
            <li>Bug fixes and security enhancements</li>
        </ul>
        </font>
    </td>
</tr>
<tr>
    <td cellpadding="0" cellspacing="0" >
        <img src="IMG__SRC12" height="65" width="60"/>
        
    </td>
    <td cellpadding="0" cellspacing="0">
        <a href="" target=""><font size="4" face="calibri" color="#73A3D1">See details...</font></a><br>
        <a href="" target=""><font size="4" face="calibri" color="#73A3D1">End User License Agreement</font></a><br>
        <font size="3" face="calibri" color="white">Updating takes under a minute on broadband - no restart is required.<br><br></font>
       
       <!-- <wxp module="wx" class="CheckBox">
                <param name="style" value="wx.ALL|wx.BORDER_NONE">
                <param name="id" value=5100>
        </wxp> 
            
             <wxp module="wx" class="CheckBox">
                <param name="style" value="wx.ALL|wx.BORDER_NONE">
                <param name="label" value="so you dferemdfhdf dufhdjfjk">
            </wxp>
            
           <font size="3" face="calibri" color="white"> &nbsp;&nbsp; Do not remind me about this update.</font> -->
    </td>
</tr>
</table>
</body>
</html>
'''
    
    def __init__(self, parent, loadNumber, mathsQNumber):
        print "===> abodeupdatedialog.py initiated"
        self.dialogID = "500004"
        self.dialogTag = "ADOBE_FLASH_PLAYER_UPDATE"
        self.name = "update Adobe Flash Player dialog"
        self.type = 2
        self.loadNumber = loadNumber
        self.mathsQNumber = mathsQNumber
#         panel=wx.Panel(parent)
#         panel.SetBackgroundColour("Green")
        newAdobeUpdateDialog.allResponses=""
        newAdobeUpdateDialog.allResponseCode=""
        newAdobeUpdateDialog.checkClickCount=0
        
        wx.Dialog.__init__(self, parent=parent, id=-1, name='Update Adobe Flash Player') 
        wx.Dialog.SetSize(self, (552, 354))
        wx.Dialog.SetBackgroundColour(self, "#767676")
        wx.Dialog.SetTitle(self,"Update Adobe Flash Player")
        globalTracker.math.changeStatusFromUntoInitialized(mathsQNumber, loadNumber)
        
        html = wx.html.HtmlWindow(self)
        self.text = self.text.replace("IMG_SRC", globalTracker.propertyVar.phase3images + 'flash2.png')
        self.text = self.text.replace("IMG__SRC12", globalTracker.propertyVar.phase3images + 'flash_icon.png')
        
#         self.text = self.text.replace("IMG_SRC", "../icons/" + 'flash2.png')
#         self.text = self.text.replace("IMG__SRC12", "../icons/" + 'flash_icon.png')
       
        html.SetPage(self.text)
        
        self.Layout()
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.buttonY = wx.Button(self, wx.ID_YES, "Yes") 
        self.buttonY.Bind(wx.EVT_BUTTON, self.OnClickRestartNow, self.buttonY)
        btn_font = wx.Font(7, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.buttonY.SetBackgroundColour("#858181")
        
        self.buttonN = wx.Button(self, wx.ID_NO, "No")
        self.buttonN.Bind(wx.EVT_BUTTON, self.OnPostpone, self.buttonN) 
        self.buttonN.SetBackgroundColour("#858181")
        self.buttonN.SetFocus()
        
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.Add(html, 1, wx.EXPAND, 0) 
        
        checkBoxInfo = wx.StaticText(self, label="Do not remind me about this update.", style=wx.EXPAND | wx.CENTER | wx.NO_BORDER)
        checkBoxInfo.SetForegroundColour("White")  # set text color
        checkBoxInfo.SetBackgroundColour("#767676")
        
        checkBoxInfo.SetFont(wx.Font(10.5, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Calibri'))
        
        
        self.cb = wx.CheckBox(self, -1, '', (10, 10))
        self.cb.SetValue(False)
   
        wx.EVT_CHECKBOX(self, self.cb.GetId(), self.ShowTitle)
        
        midhSizer = wx.BoxSizer(wx.HORIZONTAL)
        midhSizer.Add((80,1))
        midhSizer.Add(self.cb, 0, wx.ALL, 0) 
        midhSizer.Add(checkBoxInfo, 0, wx.ALL, 0) 
#         vSizer.Add(midhSizer, 0, wx.EXPAND, 0) 
        vSizer.RecalcSizes()
        vSizer.AddSizer(midhSizer, 0, wx.EXPAND, 0)
        
        hSizer = wx.BoxSizer(wx.HORIZONTAL)       
        hSizer.Add(wx.StaticText(self), 1)
        hSizer.Add(self.buttonY, 0, wx.ALIGN_RIGHT | wx.ALL , 5) 
        hSizer.Add(self.buttonN, 0, wx.ALIGN_RIGHT | wx.ALL, 5) 
        vSizer.Add(hSizer, 0, wx.EXPAND | wx.ALIGN_RIGHT , 0) 
        self.Layout() 
        vSizer.FitInside(self)
        self.SetSizer(vSizer) 
        wx.Dialog.FitInside(self)
        wx.Dialog.Layout(self)
        
    def ShowTitle(self, event):
        
        newAdobeUpdateDialog.checkClickCount += 1
        
        globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
       
        RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode

        if ((newAdobeUpdateDialog.checkClickCount % 2) == 0):

            newAdobeUpdateDialog.allResponses+="|"+ RESPONSECODE.ADOBE_UPDATE_CHECKBOX_UNCHECKED+" CLICK-No:"+str(newAdobeUpdateDialog.checkClickCount)

        else:
            newAdobeUpdateDialog.allResponses+="|"+ RESPONSECODE.ADOBE_UPDATE_CHECKBOX_CHECKED+" CLICK-No:"+str(newAdobeUpdateDialog.checkClickCount)

    def getDialogTag(self):
        return self.dialogTag
    
    def getDialogID(self):
        return self.dialogID  
        
    def OnPostpone(self, event):
        self.getButtonClickResult("NO")
        globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
        
        newAdobeUpdateDialog.allResponses+="|"+ RESPONSECODE.ADOBE_UPDATE_N
        
        RESPONSECODE.currentResponse = newAdobeUpdateDialog.allResponses
        RESPONSECODE.currentResponseCode = RESPONSECODE.RESPONSE[RESPONSECODE.ADOBE_UPDATE_N]
        
        self.Destroy()
        
    def OnClickRestartNow(self, event):
        self.getButtonClickResult("YES")
        globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
        
        newAdobeUpdateDialog.allResponses+="|"+ RESPONSECODE.ADOBE_UPDATE_Y
        
        RESPONSECODE.currentResponse = newAdobeUpdateDialog.allResponses
        RESPONSECODE.currentResponseCode = RESPONSECODE.RESPONSE[RESPONSECODE.ADOBE_UPDATE_Y]
        
        self.Destroy()
                
    def onClose(self, event):
#         print "on close" 
        globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
        
        newAdobeUpdateDialog.allResponses+="|"+ RESPONSECODE.ADOBE_UPDATE_CLOSE
        
        RESPONSECODE.currentResponse = newAdobeUpdateDialog.allResponses
        RESPONSECODE.currentResponseCode = RESPONSECODE.RESPONSE[RESPONSECODE.ADOBE_UPDATE_CLOSE]
        
        self.Destroy()
        
    def getButtonClickResult(self, click):
        if click == "YES" or click == 5103:
            return 5103
        elif click == "NO" or click == 5104:
            return 5104
        elif click == "CANCEL" or click == 5101:
            return 5101
           

class window(wx.Window):     
    def __init__(self, parent):
        wx.Window.__init__(self, parent=parent, id=wx.ID_ANY, size=(520, 360), name="window")
        wx.Window.SetBackgroundColour(self, "Green")
        
        
def main():
    ex = wx.App()
    dmodule = dialogUtils()
    
    w = window(wx.Frame(parent=None))
   
    dial = newAdobeUpdateDialog(w, 1, 2)
    result = dial.ShowModal()
    w.Show()
    
#     print result
#     if result == wx.ID_CANCEL:
#         dial.getButtonClickResult(wx.ID_CANCEL)
    ex.MainLoop()
if __name__ == "__main__":     
    main()
