'''
Created on Jun 9, 2015

@author: Anjila
'''
import CustomDialog,wx,globalTracker,time
from globalTracker import RESPONSECODE,CONSTANTS
from globalTracker import globalVar


class GetUserNamenPwd(CustomDialog.Dialog):
    def __init__(self, parent,title,parentEmailPojo,dialogID, dialogTag,startTime): 
        print "===> form_username_ped.py initiatex"
        self.name = "Reset email and password"
        self.type = 1
        self.startTime=startTime
        wx.Dialog.__init__(self, parent=parent, id=-1, title=title,style=wx.ALL|wx.CENTER_ON_SCREEN)
        self.dialogFieldValues="" 
        wx.Dialog.SetSize(self, (470,170))
        size123=(3,1)
        size1234=(3,25)
        self.statusSize=(300,-1)
        self.loginPnl=wx.Panel(self, id=-1)
        self.font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')
        
        self.Loginsizer= wx.BoxSizer(wx.VERTICAL)
        userNameLabel=wx.StaticText(self.loginPnl, id=-1, label="Username :",style=wx.ALL)
        self.userNameText=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.EXPAND)
        self.userNameStatus=wx.TextCtrl(self.loginPnl, id=-1, value="",style=wx.TE_RICH2 |wx.NO_BORDER|wx.TE_READONLY)
        self.userNameStatus.SetSize(self.statusSize)
#         self.userNameStatus.Hide()
        
        userNamesizer=wx.BoxSizer(wx.HORIZONTAL)
        userNamesizer.Add(size123, 0,flag= wx.ALL)
        userNamesizer.Add(userNameLabel, 1,flag= wx.ALL)
        userNamesizer.Add(self.userNameText,1,flag= wx.ALL|wx.EXPAND,border=0)
        userNamesizer.Add(self.userNameStatus, 0,flag=wx.ALL|wx.EXPAND,border=0)
        
        pwdLabel=wx.StaticText(self.loginPnl, id=-1, label="Password :",style=wx.ALL)
        self.pwdText=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.EXPAND|wx.PASSWORD)
        self.pwdStatus=wx.TextCtrl(self.loginPnl, id=-1, value="",style=wx.TE_RICH2 | wx.NO_BORDER|wx.TE_READONLY)
        self.pwdStatus.SetSize(self.statusSize)
        
        pwdsizer=wx.BoxSizer(wx.HORIZONTAL)
        pwdsizer.Add(size123, 0,flag= wx.ALL)
        pwdsizer.Add(pwdLabel, 1,flag=wx.ALL)
        pwdsizer.Add(self.pwdText,1,flag= wx.ALL|wx.EXPAND)
        pwdsizer.Add(self.pwdStatus, 1,flag=wx.ALL|wx.EXPAND)
        
        self.button_ok=wx.Button(self.loginPnl, wx.ID_OK,  label="Submit")
        self.button_ok.Bind(wx.EVT_BUTTON, self.onClickOK)
        
        btnSizer=wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(size1234, 0,flag= 1)
        btnSizer.Add(self.button_ok, 0, flag= wx.ALL)
        
        self.button_cancel=wx.Button(self.loginPnl, wx.ID_CANCEL,  label="Cancel")
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onClickCancel)
        btnSizer.Add(self.button_cancel,0, flag= wx.ALL)
        
        self.Loginsizer.Add(userNamesizer,1,wx.ALL,2)
        self.Loginsizer.Add(pwdsizer,1,wx.ALL,2)
        self.Loginsizer.Add((5,9))
        self.Loginsizer.Add(btnSizer,0,wx.ALL,2)
        self.Loginsizer.Layout()
        self.loginPnl.SetSizer(self.Loginsizer)
        self.loginPnl.Layout()
        self.loginPnl.Fit()
        selfsizer=wx.BoxSizer(wx.VERTICAL)
        selfsizer.Add((100,20))
        selfsizer.Add(self.loginPnl,0,wx.ALL|wx.EXPAND)
        self.SetSizer(selfsizer)
        self.Bind(wx.EVT_CLOSE, self.onClose)     
        self.Layout()
        self.pwdStatus.Hide()
        self.userNameStatus.Hide()
        globalTracker.RESPONSECODE.responseLogBuffer =str(globalVar.flowNumber) + "\t" + "-1" + "\t" +parentEmailPojo.get_indexId()  + "\t" + "" + "\t" + "" + "\t" +   ""  + "\t" +dialogID  + "\t" +dialogTag+"\t"
        globalTracker.RESPONSECODE.dialogSN+=1
        globalTracker.RESPONSECODE.dilaogLogBuffer="%s%s%s%s%s%s%s%s%s%s%s%s%s%s"%(str(globalTracker.RESPONSECODE.dialogSN),"\t",globalVar.date,"\t",dialogID,"\t",dialogTag,"\t",parentEmailPojo.get_indexId(),"\t","0","\t","1","\t")
        
    def resetAll(self):
        self.userNameStatus.SetValue("")
        self.userNameStatus.Hide()
        self.pwdStatus.SetValue("")
        self.pwdStatus.Hide()
    
    def onClose(self,event):   
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.DIALOG_CLOSE
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
            
        globalTracker.RESPONSECODE.responseLogBuffer+=RESPONSECODE.currentResponse+"\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
        RESPONSECODE.SNo+=1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo)+"\t"+globalTracker.RESPONSECODE.responseLogBuffer)
        self.Destroy()
        
    def onClickOK(self,event):
        self.resetAll()
        result=True
        userName=self.userNameText.GetValue().strip()
        pwd=self.pwdText.GetValue().strip()
        if  userName==None or len(userName)<=0:
            result=False
            self.changeUserNameStatus("Username cannot be empty")
        elif len(userName)>0 and  (userName.isdigit()):
            result=False
            self.changeUserNameStatus("Username cannot be number only")
        if pwd==None or len(pwd)<=0:
            result=False
            self.changePwdStatus("Password cannot be empty")
        if result==True:
            self.dialogFieldValues="USERNAME:"+userName+"|PASSWORD:"+pwd
            globalTracker.RESPONSECODE.dilaogLogBuffer+=self.dialogFieldValues+"\t"+self.startTime+"\t"+(time.strftime("%H:%M:%S", time.localtime()))+"\n"
            RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
            RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
            RESPONSECODE.currentResponse=RESPONSECODE.FORM_GET_UNAME_PWD_OK
            RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
                
            globalTracker.RESPONSECODE.responseLogBuffer+=RESPONSECODE.currentResponse+"\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
            RESPONSECODE.SNo+=1
            globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo)+"\t"+globalTracker.RESPONSECODE.responseLogBuffer)
            self.Hide()
            globalTracker.utils.write(globalTracker.propertyVar.dialogReportResult, globalTracker.RESPONSECODE.dilaogLogBuffer) 
            
    
    def changeUserNameStatus(self,message):
        self.userNameStatus.SetValue(message)
        self.userNameStatus.SetStyle(0, len(self.userNameStatus.GetValue()), wx.TextAttr("red", font=self.font))
        self.userNameStatus.SetSize(self.statusSize)
        self.userNameStatus.Show()
        self.userNameStatus.Refresh()
        self.userNameStatus.Layout()
        
    def changePwdStatus(self,message):
        self.pwdStatus.SetValue(message)
        self.pwdStatus.SetStyle(0, len(self.pwdStatus.GetValue()), wx.TextAttr("red", font=self.font))
        self.pwdStatus.SetSize(self.statusSize)
        self.pwdStatus.Show()
        self.pwdStatus.Refresh()
        self.pwdStatus.Layout()
    
    def onClickCancel(self,event):
#         print "cancel"
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.FORM_GET_UNAME_PWD_CANCEL
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
            
        globalTracker.RESPONSECODE.responseLogBuffer+=RESPONSECODE.currentResponse+"\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
        RESPONSECODE.SNo+=1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo)+"\t"+globalTracker.RESPONSECODE.responseLogBuffer)
        self.Destroy()
        
class App(wx.App):
   
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect=False, filename=None)
        
    def OnInit(self):
       
        frame = GetUserNamenPwd(parent=None,title="Login to  win a tour to Facebook")
        self.SetTopWindow(frame)
        frame.ShowModal()
        return True
    
     
        
def main():
    app = App(redirect=True)
#     wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
    
if __name__ == "__main__":
    main()     