'''
Created on Jan 25, 2016

@author: AnjilaTam
'''
import wx

import CustomDialog
import globalTracker,time
from globalTracker import RESPONSECODE
import wx.lib.agw.pybusyinfo as PBI


class FlashiPadScheme(wx.Dialog):
#     def __init__(self, parent, isParentmaths, isParentEmail):
    def __init__(self, parent,isParentmaths,isParentEmail):
        self.dialogID = "500001"
        self.dialogTag = "FLASH iPAD SHOW" 
        self.iPadImg = globalTracker.propertyVar.iPadSchemeImg
        
        self.name = "FLASH iPAD SHOW" 
        no_caption = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.NO_BORDER | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CLIP_CHILDREN|wx.ALIGN_CENTER
        wx.Dialog.__init__(self, parent=parent, id=-1,style=no_caption, name='Windows Download pop-up')
        wx.Dialog.SetSize(self, (295, 247)) 
        wx.Dialog.SetBackgroundColour(self,"White")
        wx.Dialog.CenterOnScreen(self)
        self.initiate()
        
    def initiate(self):
        self.width=290
        self.height=113
        self.height1=61
        self.panel = wx.Panel(self)
        
        self.closeBtnPanel=wx.Panel(self.panel)
        closeImg = wx.Image(globalTracker.propertyVar.phase3images+"closeWithWhitebkg.png", type=wx.BITMAP_TYPE_ANY)
        closeImg = closeImg.Scale(15,15, wx.IMAGE_QUALITY_HIGH)
        closeBmp=closeImg.ConvertToBitmap()
        b = wx.BitmapButton(self.closeBtnPanel, -1, closeBmp, (0, 0),
                            style = wx.NO_BORDER)
        b.SetBitmapSelected(closeBmp)
        self.Bind(wx.EVT_BUTTON, self.OnClose,b)
        
        self.iPadImgPanel=wx.Panel(self.panel)
        image = wx.Image(globalTracker.propertyVar.phase3images+"up1.png", type=wx.BITMAP_TYPE_ANY)
        image = image.Scale(self.width, self.height, wx.IMAGE_QUALITY_HIGH)
        self.flashiPadBitmap = wx.StaticBitmap(self.iPadImgPanel, bitmap=image.ConvertToBitmap())
    
        self.emailPnl=wx.Panel(self.panel)
        emailLabel=wx.StaticText(self.emailPnl, id=-1, label="Enter your email for one time offer:",style=wx.ALL)
        self.emailIdText=wx.TextCtrl(self.emailPnl,id=-1, value="", style=wx.EXPAND)
        self.emailIdText.SetToolTipString("Enter your email here")
        self.Bind(wx.EVT_TEXT, self.onEmailText, self.emailIdText)
        self.emailStatus=wx.TextCtrl(self.emailPnl, id=-1, value="",style=wx.EXPAND|wx.TE_RICH2 | wx.NO_BORDER|wx.TE_READONLY)
        
        vSizer1=wx.BoxSizer(wx.VERTICAL)
        vSizer1.Add(emailLabel,0)
        vSizer1.Add(self.emailStatus,0,wx.EXPAND|wx.ALL)
        
        vSizer1.Add(self.emailIdText,0,wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL,5)
        self.emailPnl.SetSizer(vSizer1)

        self.claimPnl=wx.Panel(self.panel)
        claimImg = wx.Image(globalTracker.propertyVar.phase3images+"up2.png", type=wx.BITMAP_TYPE_ANY)
        claimImg = claimImg.Scale(self.width, self.height1, wx.IMAGE_QUALITY_HIGH)
        self.claimBtnBitmap = wx.StaticBitmap(self.claimPnl, bitmap=claimImg.ConvertToBitmap())
        self.claimBtnBitmap.Bind(wx.EVT_LEFT_UP, self.onClaim, self.claimBtnBitmap)
    
        vSizer = wx.BoxSizer(wx.VERTICAL)
        self.closeBtnPanel.SetBackgroundColour("White")
        vSizer.Add(self.closeBtnPanel,0,flag=wx.ALIGN_RIGHT)
        vSizer.Add(self.iPadImgPanel)
        vSizer.Add(self.emailPnl,1, wx.EXPAND|wx.ALL)
        vSizer.Add(self.claimPnl,0, wx.EXPAND|wx.ALL)
        
        self.panel.SetSizer(vSizer)     
        self.panel.Fit()
        self.emailStatus.Hide()
        self.Layout()
        
    def getDialogTag(self):
        return self.dialogTag
    
    def getDialogID(self):
        return self.dialogID
        
    def onClaim(self,event):
#         print "On enter"
        if not self.emailStatus==None:
            self.emailStatus.Hide()
        if not self.emailIdText==None:
            emailvalue=self.emailIdText.GetValue()
            if self.isValidEmail(emailvalue):
                #user entered valid email
                RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
                RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
                RESPONSECODE.currentResponse=RESPONSECODE.MP3_EMAIL+"||"+emailvalue
                RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.MP3_EMAIL]+"|"+RESPONSECODE.RESPONSE[RESPONSECODE.MP3_EMAIL_VALUE]
        #         print "Save downloaded"
                
                dial = wx.MessageDialog(self, "We will notify by your email about an iPad you have won", "",wx.OK| wx.OK_DEFAULT |wx.ICON_INFORMATION)
                dial.ShowModal()
                
                self.closeFrame()
            else:
                self.font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')
                self.emailStatus.SetValue("Invalid email address")
                self.emailStatus.SetStyle(0, len(self.emailStatus.GetValue()), wx.TextAttr("red", font=self.font))
                self.emailStatus.Show()
        event.Skip()
        
    def closeFrame(self):
        self.Destroy()
        
    def OnClose(self, event):
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.DIALOG_CLOSE
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
#         globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        self.DestroyChildren()
        self.closeFrame()
        
        
    def isValidEmail(self,emailAddress):
#         email = "tamrakar-12angela@gmail"
        import re
        regex=r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+'
#         r'[\w.-]+@[\w.-]+.\w+'

        match = re.search(regex, emailAddress)
    
        if match:
            
#             print "valid email :::", match.group()
            return True
        else:
#             print "not valid:::" 
            return False
        
    def onEmailText(self,event):
        if len(self.emailIdText.GetValue().strip())==0:
            self.emailStatus.Hide()
            


class window(wx.Window):     
    def __init__(self, parent):
        wx.Window.__init__(self, parent=parent, id=wx.ID_ANY, size=(520, 360), name="window")
        wx.Window.SetBackgroundColour(self, "Green")   
                
def main():
    app = wx.App()
    frame = FlashiPadScheme(None)
    frame.Show(True)
    app.MainLoop()
  
    
    
#     print result
#     if result == wx.ID_CANCEL:
#         dial.getButtonClickResult(wx.ID_CANCEL)
#     ex.MainLoop()
if __name__ == "__main__":     
    main()