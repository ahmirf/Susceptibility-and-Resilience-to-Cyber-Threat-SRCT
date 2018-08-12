'''
Created on Jan 27, 2016

@author: AnjilaTam
'''

import wx

class Form_getEmail_iPadScam(wx.Frame):
    def __init__(self, parent, loadNumber, mathsQNumber,startTime): 
        print "===> Form_Form_getEmail.py initiated"
        self.startTime = startTime
        self.name = "Get email in iPad Gift Scheme"
        self.type = 1
        self.startTime=startTime
        self.loadNumber = loadNumber
        self.mathsQNumber = mathsQNumber
        wx.Frame.__init__(self, parent=parent, id=-1) 
        wx.Frame.SetSize(self, (240,240))
        wx.Frame.SetBackgroundColour(self,"White")
        self.initiate()
        
        
    def initiate(self):
        self.loginPnl=wx.Panel(self)
        emailLabel=wx.StaticText(self.loginPnl, id=-1, label="email :",style=wx.ALL)
        self.emailIdText=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.EXPAND)
        self.emailStatus=wx.TextCtrl(self.loginPnl, id=-1, value="",style=wx.EXPAND|wx.TE_RICH2 | wx.NO_BORDER|wx.TE_READONLY)
#         self.Bind(wx.EVT_TEXT, self.onemptyEmailStatus, self.emailIdText)
        self.emailStatus.Hide()
        
        nameLabel=wx.StaticText(self.loginPnl, id=-1, label="Name :")
        self.nameText=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.EXPAND)
        self.nameStatus=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.EXPAND|wx.TE_RICH2 | wx.NO_BORDER|wx.TE_READONLY)
        self.nameStatus.Hide()
        
        okImg = wx.Image("../icons/okBtn.jpg", type=wx.BITMAP_TYPE_ANY)
        okImg = okImg.Scale(30, 20, wx.IMAGE_QUALITY_HIGH)
        self.OkBtnBitmap = wx.StaticBitmap(self.loginPnl, bitmap=okImg.ConvertToBitmap())
        self.OkBtnBitmap.Bind(wx.EVT_LEFT_UP, self.onOK, self.OkBtnBitmap)
        
        cancelImg = wx.Image("../icons/cancelbtn.jpg", type=wx.BITMAP_TYPE_ANY)
        cancelImg = cancelImg.Scale(30,20, wx.IMAGE_QUALITY_HIGH)
        self.cancelBtnBitmap = wx.StaticBitmap(self.loginPnl, bitmap=cancelImg.ConvertToBitmap())
        self.cancelBtnBitmap.Bind(wx.EVT_LEFT_UP, self.onCancel, self.cancelBtnBitmap)
        
        
        self.loginSizer= wx.FlexGridSizer(4, 3,hgap=8, vgap=6)
        self.loginSizer.Add(emailLabel, 0, wx.EXPAND, 1)
        self.loginSizer.Add(self.emailIdText, 0, wx.ALL, 1)
        self.loginSizer.Add(self.emailStatus, 0, wx.ALL, 1)
        
        self.loginSizer.Add(nameLabel, 0, wx.ALL, 1)
        self.loginSizer.Add(self.nameText, 1, wx.ALL, 1)
        self.loginSizer.Add(self.nameStatus, 1, wx.ALL, 1)
        
        self.loginSizer.Add(self.OkBtnBitmap, 0, wx.ALL, 1)
        self.loginSizer.Add(self.cancelBtnBitmap, 1, wx.ALL, 1)
        
        self.loginPnl.SetSizer(self.loginSizer)
        
    def onOK(self,event):
        event.Skip()
    
    def onCancel(self,event):
        event.Skip()
        
class App(wx.App):
   
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect=False, filename=None)
        
    def OnInit(self):
        frame = Form_getEmail_iPadScam(None,1,1,0)
        self.SetTopWindow(frame)
        frame.Show()
        return True
    
     
        
def main():
    app = App(redirect=True)
#     wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
    
if __name__ == "__main__":
    main()