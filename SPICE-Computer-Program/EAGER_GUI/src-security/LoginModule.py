'''
Created on Feb 3, 2015

@author: Anjila
'''
import sys
import wx,os
import globalTracker
from newOutline import MainFrame
from globalTracker import globalVar,ERRORMESSAGES
from FileOperations import FileOperations


class LoginFrame(wx.Frame):
    def __init__(self, parent,app, size, title, style):
        wx.Frame.__init__(self, parent, id=-1, size=size, title=title, style=style)
        self.app=app
        self.Centre()
        self.initUI()
        self.fileoperation=FileOperations()
        self.Show()
        
    def initUI(self):
        ############## *****LOGIN PANEL  *****  ###########
#          LoginModule.py initiated
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onClose)
        loginPnl = wx.Panel(self, wx.ALL ^ wx.RESIZE_BORDER)
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())
        loginSizer = wx.GridBagSizer(5,13)
        self.duplicateIdError=wx.TextCtrl(loginPnl,id=wx.ID_ANY, size=(269,-1),style=wx.HORIZONTAL|wx.EXPAND|wx.NO_BORDER|wx.TE_RICH2|wx.TE_READONLY)
        loginSizer.Add(self.duplicateIdError, pos=(0,1), span=(1, 8), flag=wx.ALL | wx.EXPAND, border=2)
        # subject id 
        subjectIdLbl = wx.StaticText(loginPnl, label="Subject Id :")
        self.subjectIdText = wx.TextCtrl(loginPnl)
        self.subjectIdError = wx.TextCtrl(loginPnl,id=wx.ID_ANY, size=(269,-1),style=wx.HORIZONTAL|wx.EXPAND|wx.NO_BORDER|wx.TE_RICH2|wx.TE_READONLY)
        loginSizer.Add(subjectIdLbl, pos=(1, 0), flag=wx.LEFT | wx.ALL, border=5)
        loginSizer.Add(self.subjectIdText, pos=(1, 1), span=(1, 3), flag=wx.ALL | wx.EXPAND, border=2)
        loginSizer.Add(self.subjectIdError, pos=(1, 5), span=(1, 8), flag=wx.ALL | wx.EXPAND, border=2)
        participantNameLabel = wx.StaticText(loginPnl, label="Subject Name :")
        self.participantNameText = wx.TextCtrl(loginPnl)
        self.participantNameError = wx.TextCtrl(loginPnl,id=wx.ID_ANY, size=(269,-1),style=wx.NO_BORDER|wx.TE_RICH2|wx.TE_READONLY)
        loginSizer.Add(participantNameLabel, pos=(3, 0), flag=wx.LEFT | wx.ALL | wx.EXPAND, border=5)
        loginSizer.Add(self.participantNameText, pos=(3, 1), span=(1, 3), flag=wx.LEFT | wx.ALL | wx.EXPAND, border=2)
        loginSizer.Add(self.participantNameError, pos=(3, 5), span=(1, 8), flag= wx.ALL | wx.EXPAND, border=2)
        runButton = wx.Button(loginPnl, label="run")
        runButton.Bind(wx.EVT_BUTTON, self.doLogin)
        loginSizer.Add(runButton, pos=(5, 1), flag=wx.LEFT | wx.RIGHT | wx.BOTTOM , border=2)
        loginPnl.SetSizer(loginSizer)
        loginSizer.Layout()
        loginPnl.Refresh()
        loginPnl.Layout()
        self.Layout()
        self.duplicateIdError.Hide()
        self.subjectIdError.Hide()
        self.participantNameError.Hide()
        
    subjectIdInvalid=False
    NameInvalidAlpha=False
    NameEmpty=False
    issubjectIdtipballoon=False
    isgroupIdtipballoon=False
    isparticipantNametipballoonEmpty=False
    isparticipantNametipballoonInvalid=False
    
    def doLogin(self, event):
        doLogin=True
        text = self.subjectIdText.GetValue().strip()
        if self.duplicateIdError.IsShown():
            self.duplicateIdError.Hide()
        if self.subjectIdError.IsShown():
            self.subjectIdError.Hide()
        if  self.participantNameError.IsShown():
            self.participantNameError.Hide()
        if (not text == None and len(text) > 0):
            if text.isalnum():
                self.subjectIdInvalid=False
                globalVar.subjectId = text
            else:
                self.subjectIdInvalid=True
                doLogin=False
                self.subjectIdError.SetValue(ERRORMESSAGES.subjectIdAlphaNum)
                self.subjectIdError.SetStyle(0, len(self.subjectIdError.GetValue()), wx.TextAttr("red"))
                if not self.subjectIdError.IsShown():
                    self.subjectIdError.Show()
        else:
            self.subjectIdInvalid=True
            doLogin=False
            self.subjectIdError.SetValue(ERRORMESSAGES.subjectIdEmpty)
            self.subjectIdError.SetStyle(0, len(self.subjectIdError.GetValue()), wx.TextAttr("red"))
            if not self.subjectIdError.IsShown():
                self.subjectIdError.Show()
        text = self.participantNameText.GetValue().strip()
        if (not text == None and len(text) > 0):    
            if text.isalpha():
                globalVar.subjectName = text
                
                self.NameInvalidAlpha=False
                self.NameEmpty=False
            else:
                self.NameInvalidAlpha=True
                doLogin=False
                self.participantNameError.SetValue(ERRORMESSAGES.subjectNameLetter)
                self.participantNameError.SetStyle(0, len(self.participantNameError.GetValue()), wx.TextAttr("red"))
                if not self.participantNameError.IsShown():
                    self.participantNameError.Show()
        else:
            self.NameEmpty=True
            doLogin=False
            self.participantNameError.SetValue(ERRORMESSAGES.subjectNameEmpty)
            self.participantNameError.SetStyle(0, len(self.participantNameError.GetValue()), wx.TextAttr("red"))
            if not self.participantNameError.IsShown():
                self.participantNameError.Show()
                
        if self.checkForDuplicateID():
            doLogin=False
            self.duplicateIdError.SetValue(ERRORMESSAGES.duplicateID)
            self.duplicateIdError.SetStyle(0, len(self.duplicateIdError.GetValue()), wx.TextAttr("red"))
            if not self.duplicateIdError.IsShown():
                self.duplicateIdError.Show()
        if doLogin==True and not globalVar.subjectName==None:
            self.makeRequireddir()
            globalTracker.propertyVar.participantName=globalVar.subjectName
            mainframe = MainFrame()
            self.app.SetTopWindow(mainframe)
            mainframe.Maximize(True)
            mainframe.ShowFullScreen(True)
            self.Destroy()
            mainframe.Show()
        event.Skip()
        
    def checkForDuplicateID(self):
        if os.path.isdir(globalTracker.propertyVar.reportPathFirst+"\\"+self.subjectIdText.GetValue().strip()):
            return True
        return False
        
    def makeRequireddir(self):
        if not os.path.exists(globalTracker.propertyVar.reportPathFirst):
            os.mkdir(globalTracker.propertyVar.reportPathFirst)
        if os.path.exists(globalTracker.propertyVar.reportPathFirst) and not os.path.exists(globalTracker.propertyVar.reportPathFirst+"\\"+str(globalVar.subjectId)):
            os.mkdir(globalTracker.propertyVar.reportPathFirst+"\\"+str(globalVar.subjectId)) 
            globalTracker.propertyVar.changePath()
           
    def onClose(self,event): 
        event.Skip()
           
class App(wx.App):
   
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect=False, filename=None)
        
    def OnInit(self):
        print "******************************************* STARTING LOG IN **********************************************************************\n"
        frame=LoginFrame(parent=None,app=self, size=(650,-1), title="program", style=wx.DEFAULT_FRAME_STYLE | wx.ALPHA_TRANSPARENT ^ wx.RESIZE_BORDER)
        frame.Show()
        return True

class CommandLineHandler(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect=False, filename=None)

    def OnInit(self):
        globalTracker.globalVar.subjectId=str(sys.argv[1]).strip()
        globalVar.subjectName=str(sys.argv[2]).strip()
        globalTracker.propertyVar.participantName=globalVar.subjectName
        globalTracker.propertyVar.changePath()
        mainframe = MainFrame()
        self.SetTopWindow(mainframe)
        mainframe.Maximize(True)
        mainframe.ShowFullScreen(True)
        mainframe.Show()
        return True

def main():
    print "In Loginmodule"
    if len(sys.argv) < 3 :
        app = App(redirect=False)
        app.MainLoop()
    else:
        app=CommandLineHandler()
        app.MainLoop()
        
if __name__ == "__main__":
    main()
