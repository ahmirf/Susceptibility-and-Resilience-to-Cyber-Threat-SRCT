'''
Created on Sep 24, 2014

@author: Anjila
'''
import wx.html

import CustomDialog
from dialogUtils import dialogUtils
from globalTracker import MATHASSOC_DIALOG, RESPONSECODE
import globalTracker


class AdobeUpdateDialog(CustomDialog.Dialog):
#     adobeImage=globalTracker.propertyVar.phase3images+"\adobe.png"
    text = '''
<html>
<body link="#C0C0C0" >
<table bgcolor="#3E3E3E" width="100%%" cellpadding="0" border="0" cellspacing="0" margin="0" outline="0">
<tr>
    <td cellpadding="0" cellspacing="0" >
    
        <img src="IMG_SRC"/>
        
    </td>
</tr>

<tr >
    <td cellpadding="0" cellspacing="0" valign="0">
       &nbsp;&nbsp;&nbsp;
            <wxp module="wx" class="CheckBox">
                <param name="style" value="wx.ALL|wx.BORDER_NONE">
                <param name="id" value=5100>
            </wxp> 
            <font size="2" face="calibri" color="white">&nbsp;&nbsp I have read and agree to the terms of the Flash Player License Agreement.</font>
    
    </td>
</tr>

<tr>
    <td >
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp<a href="" target=""><font size="2" face="calibri" color="white">Read the license here.</font></a>
    </td>
</tr>
<tr>
    <td >
        &nbsp;&nbsp;
    </td>
</tr>

</table>
</body>
</html>
    '''
  
  
  # <tr>
#     <td>
#     <p>
#            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<button type="button"><img src="icons/quitbtn.png" /></button>
#            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
#            <button type="button"><img src="icons/installbtn.png"/></button>
#            </p>
#     </td>
# </tr>
  
    def __init__(self, parent, loadNumber, mathsQNumber):
        print "===> abodeupdatedialog.py initiated"
        self.dialogID = "500004"
        self.dialogTag = "ADOBE_FLASH_PLAYER_UPDATE"
        self.name = "update Adobe Flash Player dialog"
        self.type = 2
        AdobeUpdateDialog.allResponses=""
        AdobeUpdateDialog.allResponseCode=""
        self.loadNumber = loadNumber
        self.mathsQNumber = mathsQNumber
#         panel=wx.Panel(parent)
#         panel.SetBackgroundColour("Green")
        
        wx.Dialog.__init__(self, parent=parent, id=-1, name='Update Adobe Flash Player') 
        wx.Dialog.SetSize(self, (502, 304))
        wx.Dialog.SetBackgroundColour(self, "#3E3E3E")
        globalTracker.math.changeStatusFromUntoInitialized(mathsQNumber, loadNumber)
        
        html = wx.html.HtmlWindow(self)
        self.text=self.text.replace("IMG_SRC", globalTracker.propertyVar.phase3images+'adobe.png')
        html.SetPage(self.text)

        self.Layout()
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.buttonY = wx.Button(self, wx.ID_YES, "Yes") 
        self.buttonY.Bind(wx.EVT_BUTTON, self.OnClickRestartNow, self.buttonY)
        btn_font = wx.Font(7, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.buttonY.SetBackgroundColour("#3E3E3E")
        
        self.buttonN = wx.Button(self, wx.ID_NO, "No")
        self.buttonN.Bind(wx.EVT_BUTTON, self.OnPostpone, self.buttonN) 
        self.buttonN.SetBackgroundColour("#3E3E3E")
        self.buttonN.SetFocus()
        
        vSizer = wx.BoxSizer(wx.VERTICAL) 
        vSizer.Add(html, 1, wx.EXPAND, 0) 
        
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
        
        
    def getDialogTag(self):
        return self.dialogTag
    
    def getDialogID(self):
        return self.dialogID  
        
    def OnPostpone(self, event):
        self.getButtonClickResult("NO")
        globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
        
        AdobeUpdateDialog.allResponses+="|"+ RESPONSECODE.ADOBE_UPDATE_N
        AdobeUpdateDialog.allResponseCode+="|"+RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
        
        RESPONSECODE.currentResponse = AdobeUpdateDialog.allResponses
        RESPONSECODE.currentResponseCode = AdobeUpdateDialog.allResponseCode
        self.Destroy()
        
    def OnClickRestartNow(self, event):
        self.getButtonClickResult("YES")
        globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
        
        AdobeUpdateDialog.allResponses+="|"+ RESPONSECODE.ADOBE_UPDATE_Y
        AdobeUpdateDialog.allResponseCode+="|"+RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
        
        RESPONSECODE.currentResponse = AdobeUpdateDialog.allResponses
        RESPONSECODE.currentResponseCode = AdobeUpdateDialog.allResponseCode
        self.Destroy()
                
    def onClose(self, event):
#         print "on close" 
        globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        RESPONSECODE.previousResponse = RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode = RESPONSECODE.currentResponseCode
        
        AdobeUpdateDialog.allResponses+="|"+ RESPONSECODE.ADOBE_UPDATE_CLOSE
        AdobeUpdateDialog.allResponseCode+="|"+RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
        
        RESPONSECODE.currentResponse = AdobeUpdateDialog.allResponses
        RESPONSECODE.currentResponseCode = AdobeUpdateDialog.allResponseCode
        self.Destroy()
        
    def getButtonClickResult(self, click):
        if click == "YES" or click == 5103:
            return 5103
        elif click == "NO" or click == 5104:
            return 5104
        elif click == "CANCEL" or click == 5101:
            return 5101
           
# image="icons/adobe.png"
# class Bitmap1(wx.StaticBitmap):
#     def __init__(self, *args, **kwargs):
#         image=wx.Image(image, type=wx.BITMAP_TYPE_ANY)
#         image=image.Scale(200,17, wx.IMAGE_QUALITY_HIGH)
#         bmp = image.ConvertToBitmap()
#         kwargs['bitmap'] = bmp
#         wx.StaticBitmap.__init__(self, *args, **kwargs)
class window(wx.Window):     
    def __init__(self, parent):
        wx.Window.__init__(self, parent=parent, id=wx.ID_ANY, size=(520, 360), name="window")
        wx.Window.SetBackgroundColour(self, "Green")
        
        
def main():
    ex = wx.App()
    dmodule = dialogUtils()
    
    w = window(wx.Frame(parent=None))
   
    dial = AdobeUpdateDialog(w,1,2)
    result = dial.ShowModal()
    w.Show()
    
#     print result
#     if result == wx.ID_CANCEL:
#         dial.getButtonClickResult(wx.ID_CANCEL)
    ex.MainLoop()
if __name__ == "__main__":     
    main()
