'''
Created on Jun 3, 2015

@author: Anjila
'''
import CustomDialog,wx,re,globalTracker,time
from dialogMsgPojo import dialogMsgPojo
from globalTracker import STRENGTH,RESPONSECODE,CONSTANTS
from validators.Password_Verifier import Password_Verifier
from globalTracker import globalVar

class ResetEmailnPwd(CustomDialog.Dialog):
    
    def __init__(self, parent,title, parentEmailPojo,dialogID,dialogTag,startTime): 
        print "===> Form_resetEmailnPwd.py initiated"
        self.startTime=startTime
        self.name = "Reset email and password"
        self.type = 1
        size123=(3,1)
        wx.Dialog.__init__(self, parent=parent, id=-1, name=title) 
        wx.Dialog.SetSize(self, (380,230))
        self.dialogFieldValues=""
        self.loginPnl=wx.Panel(self, id=-1,name=title)
        self.font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')
        self.loginSizer= wx.FlexGridSizer(6, 4,hgap=2, vgap=2)
        #subject id , group number
#         self.emailBoxSizer=wx.BoxSizer(wx.HORIZONTAL)
        
        emailLabel=wx.StaticText(self.loginPnl, id=-1, label="Email :",style=wx.ALL)
        self.emailIdText=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.EXPAND)
        self.emailStatus=wx.TextCtrl(self.loginPnl, id=-1, value="",style=wx.EXPAND|wx.TE_RICH2 | wx.NO_BORDER|wx.TE_READONLY)
        self.Bind(wx.EVT_TEXT, self.onemptyEmailStatus, self.emailIdText)
        self.emailStatus.Hide()
        self.loginSizer.Add(size123, 0, wx.EXPAND, 1)
        self.loginSizer.Add(emailLabel, 0, wx.EXPAND, 1)
        self.loginSizer.Add(self.emailIdText, 0, wx.ALL, 1)
        self.loginSizer.Add(self.emailStatus, 1, wx.EXPAND, 1)
        
        currentPasswordLabel=wx.StaticText(self.loginPnl, id=-1, label="Current Password :")
        self.currentPwdText=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.EXPAND|wx.PASSWORD)
        fake2=wx.StaticText(self.loginPnl, id=-1, label="",style=wx.ALL)
        self.loginSizer.Add(size123, 0, wx.EXPAND, 1)
        self.loginSizer.Add(currentPasswordLabel, 0, wx.ALL, 1)
        self.loginSizer.Add(self.currentPwdText, 1, wx.ALL, 1)
        self.loginSizer.Add(fake2, 0, wx.EXPAND, 1)
        
        newPasswordLabel=wx.StaticText(self.loginPnl, id=-1, label="New Password :")
        self.newPwdText=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.EXPAND|wx.PASSWORD)
        self.newPwdStengthText=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.EXPAND|wx.TE_RICH2 | wx.NO_BORDER|wx.TE_READONLY)
        self.newPwdStengthText.Hide()
        self.loginSizer.Add(size123, 0, wx.EXPAND, 1)
        self.loginSizer.Add(newPasswordLabel, 0, wx.ALL, 1)
        self.loginSizer.Add(self.newPwdText, 1, wx.ALL, 1)
        self.loginSizer.Add(self.newPwdStengthText, 1, wx.ALL, 1)
        self.Bind(wx.EVT_TEXT, self.onenterNewPwdText, self.newPwdText)
        
        verifyNewPasswordLabel=wx.StaticText(self.loginPnl, id=-1, label="Verify New Password :")
        self.verifyNewPwdText=wx.TextCtrl(self.loginPnl,id=-1, validator=Password_Verifier(),name="abc",value="", style=wx.EXPAND|wx.PASSWORD)
        self.Bind(wx.EVT_TEXT, self.onenterVerifyPwd, self.verifyNewPwdText)
#         self.Bind(wx.EVT_SET_FOCUS, self.onfocusVerifyPwd, self.verifyNewPwdText)
        self.verifyStatus=wx.TextCtrl(self.loginPnl,id=-1, size=(480,-1),value="", style=wx.ALL|wx.EXPAND|wx.TE_RICH2 | wx.NO_BORDER|wx.TE_READONLY)
#         sldk
        self.verifyStatus.Hide()
        self.loginSizer.Add(size123, 0, wx.EXPAND, 1)
        self.loginSizer.Add(verifyNewPasswordLabel, 0, wx.ALL, 1)
        self.loginSizer.Add(self.verifyNewPwdText, 1, wx.ALL, 1)
        self.loginSizer.Add(self.verifyStatus,1, wx.ALL|wx.EXPAND, 1)
        
        dummy=wx.StaticText(self.loginPnl, id=-1, label="")
        self.button_ok=wx.Button(self.loginPnl, wx.ID_OK,  label="Submit")
        self.button_ok.Bind(wx.EVT_BUTTON, self.onClickOK)
        self.loginSizer.Add(size123, 0, wx.EXPAND, 1)
        self.loginSizer.Add(dummy, 0, wx.ALL, 1)
        self.loginSizer.Add(self.button_ok, 1, wx.ALL, 1)
        self.button_cancel=wx.Button(self.loginPnl, wx.ID_CANCEL,  label="Cancel")
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onClickCancel)
        self.loginSizer.Add(self.button_cancel, 1, wx.ALL, 1)

        self.loginSizer.Layout()
        self.loginPnl.SetSizer(self.loginSizer)
        selfsizer=wx.BoxSizer(wx.VERTICAL)
        selfsizer.Add((100,20))
        selfsizer.Add(self.loginPnl,1,wx.ALL|wx.EXPAND)
        self.SetSizer(selfsizer)
        self.Layout()
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        globalTracker.RESPONSECODE.responseLogBuffer =str(globalVar.flowNumber) + "\t" + "-1" + "\t" +parentEmailPojo.get_indexId()  + "\t" + "" + "\t" + "" + "\t" +   ""  + "\t" +dialogID  + "\t" +dialogTag+"\t"
        globalTracker.RESPONSECODE.dialogSN+=1
        globalTracker.RESPONSECODE.dilaogLogBuffer="%s%s%s%s%s%s%s%s%s%s%s%s%s%s"%(str(globalTracker.RESPONSECODE.dialogSN),"\t",globalVar.date,"\t",dialogID,"\t",dialogTag,"\t",parentEmailPojo.get_indexId(),"\t","0","\t","1","\t")
       
    def onClose(self,event): 
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.DIALOG_CLOSE
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
            
        globalTracker.RESPONSECODE.responseLogBuffer+=RESPONSECODE.currentResponse+"\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
        RESPONSECODE.SNo+=1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo)+"\t"+globalTracker.RESPONSECODE.responseLogBuffer)
        self.Destroy() 
        
    def onemptyEmailStatus(self,event):
        
        if len(self.emailIdText.GetValue().strip())==0:
            print "normal du"
            self.emailStatus.SetBackgroundColour("white")
            self.emailStatus.SetValue("")
            self.emailStatus.Refresh()
            self.emailStatus.Layout()
            self.emailStatus.Hide()
            
        
    def onenterVerifyPwd(self,event):
        neewPwd=self.newPwdText.GetValue().strip()
        verifyNewPwd=self.verifyNewPwdText.GetValue().strip()
        if len(neewPwd)>0 and len(verifyNewPwd)>0:
            self.checkPwd(neewPwd,verifyNewPwd)
        if len(verifyNewPwd)==0:
#             print "ehite"
            self.verifyNewPwdText.SetBackgroundColour("white")
            self.verifyStatus.SetValue("")
            self.verifyStatus.Hide()
            self.verifyNewPwdText.Refresh()
            self.verifyNewPwdText.Layout() 
            
    def checkPwd(self,neewPwd, verifyNewPwd):
        
        if len(neewPwd)==len(verifyNewPwd) and neewPwd.lower()==verifyNewPwd.lower():
            self.verifyStatus.SetValue("Passwords Match!!")
            self.verifyStatus.SetStyle(0, len(self.verifyStatus.GetValue()), wx.TextAttr("green", font=self.font))
            self.verifyNewPwdText.SetBackgroundColour("white")     
            self.verifyNewPwdText.Refresh()
            self.verifyNewPwdText.Layout() 
            self.verifyStatus.SetSize((480,-1))
            self.verifyStatus.Show()
            return True
        else:
            self.verifyStatus.SetValue("Passwords do not Match!!")
            self.verifyStatus.SetStyle(0, len(self.verifyStatus.GetValue()), wx.TextAttr("red", font=self.font))
            self.verifyStatus.SetSize((480,-1))
            self.verifyStatus.Show()
            self.verifyNewPwdText.SetBackgroundColour("red") 
            self.verifyNewPwdText.Refresh()
            self.verifyNewPwdText.Layout()        
#             print "password do not match"
            return False
          
    def onClickOK(self,event):
        email=self.emailIdText.GetValue().strip()
        currentpwd=self.currentPwdText.GetValue().strip()
        neewPwd=self.newPwdText.GetValue().strip()
        verifyNewPwd=self.verifyNewPwdText.GetValue().strip()
        result=False
        if len(neewPwd)>0 and len(verifyNewPwd)>0 and len(email)>0 and len(currentpwd)>0:
            result1=self.email(self.emailIdText.GetValue())
            if result1==False:
                self.emailStatus.SetValue("Not a valid email")
                self.emailStatus.SetStyle(0, len(self.emailStatus.GetValue()), wx.TextAttr("red", font=self.font))
                self.emailStatus.SetSize((190,-1))
                self.emailStatus.Refresh()
                self.emailStatus.Layout()
                self.emailStatus.Show()
            
            result2=self.checkPwd(neewPwd,verifyNewPwd)   
            result=result1 and result2  
        else:
            wx.MessageBox("All the fields are required", "Error", wx.ICON_ERROR) 
            result=False
        if result==True:
            self.dialogFieldValues="EMAIL:"+email+"|CURRENT_PASSWORD:"+currentpwd+"|NEW_PASSWORD:"+neewPwd
            globalTracker.RESPONSECODE.dilaogLogBuffer+=self.dialogFieldValues+"\t"+self.startTime+"\t"+(time.strftime("%H:%M:%S", time.localtime()))+"\n"
            RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
            RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
            RESPONSECODE.currentResponse=RESPONSECODE.RESET_EMAIL_PWD_OK
            RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
                
            globalTracker.RESPONSECODE.responseLogBuffer+=RESPONSECODE.currentResponse+"\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
            RESPONSECODE.SNo+=1
            globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo)+"\t"+globalTracker.RESPONSECODE.responseLogBuffer) 
            self.Hide()
            globalTracker.utils.write(globalTracker.propertyVar.dialogReportResult, globalTracker.RESPONSECODE.dilaogLogBuffer) 
            
        
    def onClickCancel(self,event):
#         print "click Cancel"
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.RESET_EMAIL_PWD_CANCEL
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
            
        globalTracker.RESPONSECODE.responseLogBuffer+=RESPONSECODE.currentResponse+"\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
        RESPONSECODE.SNo+=1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo)+"\t"+globalTracker.RESPONSECODE.responseLogBuffer)
        self.Destroy()
        
    def onenterNewPwdText(self,event):
        #comes here on each character entered
        if len(self.newPwdText.GetValue().strip())==0:
            self.newPwdStengthText.SetValue("")
            self.newPwdStengthText.Hide()
        else:
            strength_= self.CheckPassword(self.newPwdText.GetValue())
            self.setStrength(strength_)
        
    def setStrength(self,strength_):
        if not strength_==None and strength_ in STRENGTH.strength.values() and strength_ in STRENGTH.strengthColor.keys():
            self.newPwdStengthText.SetValue(strength_)
            self.newPwdStengthText.SetStyle(0, len(self.newPwdStengthText.GetValue()), wx.TextAttr(STRENGTH.strengthColor[strength_], font=self.font))
#             STRENGTH.strengthColor[strength_]         
            self.newPwdStengthText.Show()
            

       
    def email(self,emailAddress):
#         email = "tamrakar-12angela@gmail"
        regex=r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+'
        match = re.search(regex, emailAddress)
    
        if match:
            
            print "valid email :::", match.group()
            return True
        else:
            print "not valid:::" 
            return False
    
    
    def CheckPassword(self,password):     
        score = 1  
        if len(password) < 1:
            return STRENGTH.strength[0]
        if len(password) < 4:
            return STRENGTH.strength[1]
     
        if len(password) >=8:
            score = score + 1
        if len(password) >=10:
            score = score + 1
         
        if re.search('\d+',password):
            score = score + 1
        if re.search('[a-z]',password) and re.search('[A-Z]',password):
            score = score + 1
        if re.search('.,[,!,@,#,$,%,^,&,*,(,),_,~,-,]',password):
            score = score + 1
     
        return STRENGTH.strength[score]
        
        
#         if not dialogMsgPojo_ == None and isinstance(dialogMsgPojo_, dialogMsgPojo):
#             self.dict["message"] = dialogMsgPojo_.getMessage()
#             self.getHMTLFOrNameValue(dialogMsgPojo_.getNameValuePairList())
        
class App(wx.App):
   
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect=False, filename=None)
        
    def OnInit(self):
        displaySize = wx.GetDisplaySize()
        loginWidth=displaySize[0]/3
        loginHeight=displaySize[1]/3
        frame = ResetEmailnPwd(parent=None,title="Reset password")
        self.SetTopWindow(frame)
        frame.ShowModal()
#         self.email()
        return True
    
     
        
def main():
    app = App(redirect=True)
#     wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
    
if __name__ == "__main__":
    main()            
        