'''
Created on Jun 5, 2015

@author: Anjila
'''
import CustomDialog,wx,datetime,globalTracker,time
from globalTracker import CONSTANTS,RESPONSECODE
from globalTracker import globalVar

class GetDOBInfo(CustomDialog.Dialog):
    def __init__(self, parent,title,parentEmailPojo,dialogID, dialogTag,startTime): 
        print "===> Form_DOB.py initated"
        self.name = "Get DOB Info"
        self.startTime=startTime
        self.type = 1
        size123=(3,1)
        self.dialogFieldValues=""
        self.stateString=""
        wx.Dialog.__init__(self, parent=parent, id=-1, name=title) 
        wx.Dialog.SetSize(self, (450,300))
        self.statusSize=(240,-1)
        
        self.loginPnl=wx.Panel(self, id=-1,name=title)
        self.font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, False, u'Consolas')
        self.loginSizer= wx.FlexGridSizer(8, 4,hgap=2, vgap=3)
        
        emailLabel=wx.StaticText(self.loginPnl, id=-1, label="Email :",style=wx.ALL)
        self.emailIdText=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.EXPAND)
        self.emailStatus=wx.TextCtrl(self.loginPnl, id=-1, value="",style=wx.EXPAND|wx.TE_RICH2 | wx.NO_BORDER|wx.TE_READONLY)
        self.Bind(wx.EVT_TEXT, self.onemptyEmailStatus, self.emailIdText)
        self.emailStatus.Hide()
        self.loginSizer.Add(size123, 0, wx.EXPAND, 1)
        self.loginSizer.Add(emailLabel, 0, wx.EXPAND, 1)
        self.loginSizer.Add(self.emailIdText, 1, wx.ALL|wx.EXPAND, 0)
        self.loginSizer.Add(self.emailStatus, 1, wx.ALL|wx.EXPAND, 0)
        
        DOBLabel=wx.StaticText(self.loginPnl, id=-1, label="Date of birth :",style=wx.ALL)
        self.DOBText=wx.DatePickerCtrl(self.loginPnl, id=-1, dt=wx.DefaultDateTime,
               style=wx.DP_DEFAULT|wx.DP_DROPDOWN,
               validator=wx.DefaultValidator, name="datectrl")
        self.DOBText.SetRange(wx.DateTimeFromDMY( 1, 0, 1914),wx.DateTimeFromDMY( 31, 11,datetime.date.today().year))
        self.DOBStatus=wx.TextCtrl(self.loginPnl, id=-1, value="",style=wx.EXPAND|wx.TE_RICH2 | wx.NO_BORDER|wx.TE_READONLY)
        self.DOBStatus.Hide()
        self.loginSizer.Add(size123, 0, wx.EXPAND, 1)
        self.loginSizer.Add(DOBLabel, 0, wx.EXPAND, 10)
        self.loginSizer.Add(self.DOBText, 0,wx.ALL|wx.EXPAND, 1)
        self.loginSizer.Add(self.DOBStatus, 1,wx.ALL|wx.EXPAND, 1)
        
        addressLabel=wx.StaticText(self.loginPnl, id=-1, label="Address :",style=wx.ALL)
        self.addressText=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.EXPAND)
        self.addressStatus=wx.TextCtrl(self.loginPnl, id=-1, value="",style=wx.EXPAND|wx.TE_RICH2 | wx.NO_BORDER|wx.TE_READONLY)
        self.addressStatus.Hide()
        self.loginSizer.Add(size123, 0, wx.EXPAND, 1)
        self.loginSizer.Add(addressLabel, 0, wx.EXPAND, 1)
        self.loginSizer.Add(self.addressText, 1, wx.ALL|wx.EXPAND, 1)
        self.loginSizer.Add(self.addressStatus, 1, wx.ALL|wx.EXPAND, 1)
        
        cityLabel=wx.StaticText(self.loginPnl, id=-1, label="City :",style=wx.ALL)
        self.cityText=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.EXPAND)
        self.cityStatus=wx.TextCtrl(self.loginPnl, id=-1, value="",style=wx.EXPAND|wx.TE_RICH2 | wx.NO_BORDER|wx.TE_READONLY)
        self.cityStatus.Hide()
        self.loginSizer.Add(size123, 0, wx.EXPAND, 1)
        self.loginSizer.Add(cityLabel, 0, wx.EXPAND, 1)
        self.loginSizer.Add(self.cityText, 1, wx.ALL|wx.EXPAND, 1)
        self.loginSizer.Add(self.cityStatus, 1, wx.ALL|wx.EXPAND, 1)
        
        stateLabel=wx.StaticText(self.loginPnl, id=-1, label="State :",style=wx.ALL)
        
        self.stateText= wx.ComboBox(self.loginPnl, pos=(50, 30), choices=CONSTANTS.statesList, style=wx.CB_READONLY)
        self.stateStatus=wx.TextCtrl(self.loginPnl, id=-1, value="",style=wx.EXPAND|wx.TE_RICH2 | wx.NO_BORDER|wx.TE_READONLY)
        self.stateStatus.Hide()
        self.stateText.Bind(wx.EVT_COMBOBOX, self.OnSelectState)
        self.loginSizer.Add(size123, 0, wx.EXPAND, 1)
        self.loginSizer.Add(stateLabel, 0, wx.EXPAND, 1)
        self.loginSizer.Add(self.stateText, 1,wx.ALL|wx.EXPAND, 1)
        self.loginSizer.Add(self.stateStatus, 1, wx.ALL|wx.EXPAND, 1)
        
        zipCodelabel=wx.StaticText(self.loginPnl, id=-1, label="ZIP Code :",style=wx.ALL)
        self.zipCodeText=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.EXPAND)
        self.zipCodeStatus=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.EXPAND|wx.TE_RICH2 | wx.NO_BORDER|wx.TE_READONLY)
        self.zipCodeStatus.Hide()
        self.loginSizer.Add(size123, 0, wx.EXPAND, 1)
        self.loginSizer.Add(zipCodelabel, 0, wx.EXPAND, 1)
        self.loginSizer.Add(self.zipCodeText, 1,wx.ALL|wx.EXPAND, 1)
        self.loginSizer.Add(self.zipCodeStatus, 1, wx.ALL|wx.EXPAND, 1)
        
        #gender
        genderLabel=wx.StaticText(self.loginPnl, id=-1, label="Gender :",style=wx.ALL)
        
        self.radioBox = wx.RadioBox(self.loginPnl, id=-1, label="", choices=CONSTANTS.gender_choices, majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.radioBox.Enable()
        self.radioBox.SetSelection(0)
        self.genderStatus=wx.TextCtrl(self.loginPnl,id=-1, value="", style=wx.ALL)
        self.genderStatus.Hide()
        self.loginSizer.Add(size123, 0, wx.EXPAND, 1)
        self.loginSizer.Add(genderLabel, 0, wx.EXPAND, 1)
        self.loginSizer.Add(self.radioBox, 0, wx.ALL, 1)
        self.loginSizer.Add(self.genderStatus, 1, wx.ALL|wx.EXPAND, 1)
        
#         self.radioBox.Bind(wx.EVT_RADIOBOX, self.onChooseRadioButton, self.radioBox)
        self.button_ok=wx.Button(self.loginPnl, wx.ID_OK,  label="Submit")
        self.button_ok.Bind(wx.EVT_BUTTON, self.onClickOK)
        self.loginSizer.Add(size123, 0, wx.EXPAND, 1)
        self.loginSizer.Add(wx.StaticText(self.loginPnl, id=-1, label="",style=wx.ALL), 0, wx.ALL, 1)
        self.loginSizer.Add(self.button_ok, 0, wx.ALL, 1)
        self.button_cancel=wx.Button(self.loginPnl, wx.ID_CANCEL,  label="Cancel")
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onClickCancel)
        self.loginSizer.Add(self.button_cancel, 0, wx.ALL, 1)
        
        self.loginSizer.Layout()
        self.loginPnl.SetSizer(self.loginSizer)
        
        selfsizer=wx.BoxSizer(wx.VERTICAL)
        selfsizer.Add((100,20))
        selfsizer.Add(self.loginPnl,1,wx.ALL|wx.EXPAND)
        self.SetSizer(selfsizer)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Refresh()
        self.Layout()
       
        self.emailResult=False
        self.DOBResult=False
        self.addressResult=False
        self.cityResult=False
        self.stateResult=False
        self.zipResult=False
        globalTracker.RESPONSECODE.responseLogBuffer =str(globalVar.flowNumber) + "\t" + "" + "\t" +parentEmailPojo.get_indexId()  + "\t" + "" + "\t" + "" + "\t" +   ""  + "\t" +dialogID  + "\t" +dialogTag+"\t"
        globalTracker.RESPONSECODE.dialogSN+=1
        globalTracker.RESPONSECODE.dilaogLogBuffer="%s%s%s%s%s%s%s%s%s%s%s%s%s%s"%(str(globalTracker.RESPONSECODE.dialogSN),"\t",globalVar.date,"\t",dialogID,"\t",dialogTag,"\t",parentEmailPojo.get_indexId(),"\t","0","\t","1","\t")
        
    def onClose(self,event):
        print "dialog closed"
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.DIALOG_CLOSE
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
            
        globalTracker.RESPONSECODE.responseLogBuffer+=RESPONSECODE.currentResponse+"\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
        RESPONSECODE.SNo+=1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo)+"\t"+globalTracker.RESPONSECODE.responseLogBuffer) 
        self.Destroy()
        
    def resetAll(self):
        self.zipCodeStatus.SetValue("")
        self.zipCodeStatus.Hide()
        self.genderStatus.SetValue("")
        self.genderStatus.Hide()
        self.addressStatus.SetValue("")
        self.addressStatus.Hide()
        self.cityStatus.SetValue("")
        self.cityStatus.Hide()
        self.DOBStatus.SetValue("")
        self.DOBStatus.Hide()
        self.emailStatus.SetValue("")
        self.emailStatus.Hide()
        self.stateStatus.SetValue("")
        self.stateStatus.Hide()
        self.emailResult=False
        self.DOBResult=False
        self.addressResult=False
        self.cityResult=False
        self.stateResult=False
        self.zipResult=False
          
    def onClickOK(self,event):
        self.resetAll()
        email=self.emailIdText.GetValue().strip()
        dob=self.DOBText.GetValue()
        
        address=self.addressText.GetValue().strip()
        city=self.cityText.GetValue().strip()
        zip=self.zipCodeText.GetValue().strip()
        genderInt=self.radioBox.GetSelection()
        gender=CONSTANTS.gender_choices[genderInt]
        
        if email==None or len(email)<=0:
            self.changeEmailStatus()
        else:
            self.emailResult=True
        if address==None or len(address)<=0:
            self.changeAddressStatus("Address can't be empty")
        else:
            self.addressResult=True
        if city==None or len(city)<=0:
            self.changeCityStatus("City name can't be empty")
        else:
            self.cityResult=True
        if zip==None or len(zip)<=0:
            self.changeZipStatus("Please enter the zip")
        else:
            self.zipResult=self.validateZip(zip)
        if gender==None or len(gender)<=0:
            self.changeGenderStatus("Please select gender")
     
        if self.stateString==None or len(self.stateString)<=0:
            #info about you  have to choose the combo box for state
            self.changeStateStatus()
        else:
            self.stateResult=True
        self.DOBResult=self.validateDOB(dob)
        
        result=self.emailResult and self.DOBResult and self.addressResult and self.stateResult and self.cityResult and self.zipResult
        if result==True:
            self.dialogFieldValues="EMAIL:"+email+"|DOB:"+str(dob)+"|ADDRESS:"+address+"|CITY:"+city+"|ZIP:"+zip+"|GENDER:"+gender
            globalTracker.RESPONSECODE.dilaogLogBuffer+=self.dialogFieldValues+"\t"+self.startTime+"\t"+(time.strftime("%H:%M:%S", time.localtime()))+"\n"
            RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
            RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
            RESPONSECODE.currentResponse=RESPONSECODE.FORM_DOB_OK
            RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
                
            globalTracker.RESPONSECODE.responseLogBuffer+=RESPONSECODE.currentResponse+"\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
            RESPONSECODE.SNo+=1
            globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo)+"\t"+globalTracker.RESPONSECODE.responseLogBuffer) 
            self.Hide()
            globalTracker.utils.write(globalTracker.propertyVar.dialogReportResult, globalTracker.RESPONSECODE.dilaogLogBuffer) 
            
    def validateZip(self,zipCode):
        import re
        m=re.match("^[0-9]{5}(?:-[0-9]{4})?$", zipCode)
        if not m==None and len(m.group())>0:
            return True
        else:
            self.changeZipStatus("Invalid zip code")
            return False
                
    def changeZipStatus(self,message):
        self.zipCodeStatus.SetValue(message)
        self.zipCodeStatus.SetStyle(0, len(self.zipCodeStatus.GetValue()), wx.TextAttr("red", font=self.font))
        self.zipCodeStatus.SetSize(self.statusSize)
        self.zipCodeStatus.Show()
        self.zipCodeStatus.Refresh()
        self.zipCodeStatus.Layout()
    
    def changeGenderStatus(self,msg):
        self.genderStatus.SetValue(msg)
        self.genderStatus.SetStyle(0, len(self.genderStatus.GetValue()), wx.TextAttr("red", font=self.font))
        self.genderStatus.SetSize(self.statusSize)
        self.genderStatus.Show()
        self.genderStatus.Refresh()
        self.genderStatus.Layout()   
        
    def changeAddressStatus(self,msg):
        self.addressStatus.SetValue(msg)
        self.addressStatus.SetStyle(0, len(self.addressStatus.GetValue()), wx.TextAttr("red", font=self.font))
        self.addressStatus.SetSize(self.statusSize)
        self.addressStatus.Show()
        self.addressStatus.Refresh()
        self.addressStatus.Layout()
        
    
    def changeCityStatus(self,msg):
        self.cityStatus.SetValue(msg)
        self.cityStatus.SetStyle(0, len(self.cityStatus.GetValue()), wx.TextAttr("red", font=self.font))
        self.cityStatus.SetSize(self.statusSize)
        self.cityStatus.Show()
        self.cityStatus.Refresh()
        self.cityStatus.Layout()
        
        
    def changeDOBStatus(self,msg):
        self.DOBStatus.SetValue(msg)
        self.DOBStatus.SetStyle(0, len(self.DOBStatus.GetValue()), wx.TextAttr("red", font=self.font))
        self.DOBStatus.SetSize(self.statusSize)
        self.DOBStatus.Show()
        self.DOBStatus.Refresh()
        self.DOBStatus.Layout()
        
    def changeEmailStatus(self):
        self.emailStatus.SetValue("Email cant be empty")
        self.emailStatus.SetStyle(0, len(self.emailStatus.GetValue()), wx.TextAttr("red", font=self.font))
        self.emailStatus.SetSize(self.statusSize)
        self.emailStatus.Show()
        self.emailStatus.Refresh()
        self.emailStatus.Layout()
          
    def changeStateStatus(self):
        self.stateStatus.SetValue("Please choose the state")
        self.stateStatus.SetStyle(0, len(self.stateStatus.GetValue()), wx.TextAttr("red", font=self.font))
        self.stateStatus.SetSize(self.statusSize)
        self.stateStatus.Show() 
        self.stateStatus.Refresh()
        self.stateStatus.Layout()
        
    def onClickCancel(self,event):
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.FORM_DOB_CANCEL
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
            
        globalTracker.RESPONSECODE.responseLogBuffer+=RESPONSECODE.currentResponse+"\t" +RESPONSECODE.currentResponseCode+ "\t" +RESPONSECODE.previousResponse+ "\t" +RESPONSECODE.previousResponseCode+"\t" +self.startTime+"\t" +(time.strftime("%H:%M:%S", time.localtime()))+"\t"+CONSTANTS.date_today+"\n"
        RESPONSECODE.SNo+=1
        globalTracker.utils.write(globalTracker.propertyVar.responseLog, str(RESPONSECODE.SNo)+"\t"+globalTracker.RESPONSECODE.responseLogBuffer) 
        self.Destroy()
     
    def validateDOB(self,date):
        if date==None:
            self.changeDOBStatus("Please choose your DOB")
            return False
        elif date.IsValid():
            today= datetime.date.today().year
            ymd = map(int, date.FormatISODate().split('-'))
            if len(ymd)>0:
                if (today-ymd[0])>100:
                    self.changeDOBStatus("Your age cannot be greater than 100")
                    return False
                elif (today-ymd[0])<3:
                    self.changeDOBStatus("Your age cannot be less than 3")
                    return False
                else:
                    return True
            
    
        
    def onemptyEmailStatus(self,event):
        if len(self.emailIdText.GetValue().strip())==0:
            self.emailStatus.SetBackgroundColour("white")
            self.emailStatus.SetValue("")
            self.emailStatus.Refresh()
            self.emailStatus.Layout()
            self.emailStatus.Hide()  
            
    def OnSelectState(self,event):
        self.stateString = event.GetString()
        if self.stateString in CONSTANTS.statesList:
            i=CONSTANTS.statesList.index(self.stateString)
            if i>=0 and i<len(CONSTANTS.stateAbbrList):
                stateAbbr=CONSTANTS.stateAbbrList[i]
        
          
class App(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect=False, filename=None)
        
    def OnInit(self):
        frame = GetDOBInfo(parent=None,title="Get Lucky to win XBox")
        self.SetTopWindow(frame)
        frame.ShowModal()
        return True
    
     
        
def main():
    app = App(redirect=True)
    app.MainLoop()
     
   
  
if __name__ == "__main__":
    main()            
        