'''
Created on Jun 10, 2015

@author: Anjila
'''
import CustomDialog,wx

class showInfo():
    def __init__(self, parent,title): 
        
        self.name = "Reset email and password"
        self.type = 1
#         wx.Dialog.__init__(self, parent=parent, id=-1, title=title,style=wx.ALL|wx.CENTER_ON_SCREEN) 
#         wx.Dialog.SetSize(self, (470,170))
        self.loginPnl=wx.Panel(self, id=-1)
        msgBox=wx.MessageBox("INVENTORY_INFO_SHOW_GLADSTONE","Info", wx.ICON_INFORMATION)
        
        self.Loginsizer= wx.BoxSizer(wx.VERTICAL)
        self.Loginsizer.Add(msgBox,1)
        self.SetSizer(self.Loginsizer)
        
class App(wx.App):
   
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect=False, filename=None)
        
    def OnInit(self):
       
        frame = showInfo(parent=None,title="Chance to win a tour to Facebook")
        self.SetTopWindow(frame)
#         frame.ShowModal()
        return True
    
     
        
def main():
    app = App(redirect=True)
#     wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
    
if __name__ == "__main__":
    main()   