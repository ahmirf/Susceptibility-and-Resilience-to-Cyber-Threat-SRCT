'''
Created on Apr 5, 2015

@author: Anjila
'''
from wx import BoxSizer

import CustomDialog, wx, time,globalTracker
from globalTracker import MATHASSOC_DIALOG,RESPONSECODE
import wx.lib.agw.pybusyinfo as PBI


class WindowsDownloadPopup(CustomDialog.Dialog):
    def __init__(self, parent,isParentmaths,isParentEmail): 
        print "WindowsDownloadPopup.py initiated"
        self.dialogID="500001"
        self.dialogTag="WINDOWS_MP3_DOWNLOAD"
        
        self.name = "MP3 download"
        wx.Dialog.__init__(self, parent=parent, id=-1, name='Windows Download pop-up') 
        
        wx.Dialog.SetSize(self, (450, 220))
        self.SetTitle("File Download")
        self.CenterOnScreen()
        wx.Dialog.SetBackgroundColour(self, "#FFFFFF")
        
        panel = wx.Panel(self)
        
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        DialogQ = wx.StaticText(panel, label="Do you want to open or save this file?")
        hSizer.Add((20, 0))
        hSizer.Add(DialogQ)
        hSizer.Add((100, 40))
        
        NameFile = wx.StaticText(panel, label="Name")
        NameFileValue = wx.TextCtrl(panel, style=wx.CENTER | wx.NO_BORDER|wx.TE_READONLY)
        NameFileValue.SetValue("song.exe")
        fileType = wx.StaticText(panel, label="Type")
        fileTypeValue = wx.TextCtrl(panel, style=wx.CENTER | wx.NO_BORDER|wx.TE_READONLY)
        fileTypeValue.SetValue("mp3")
        fileFrom = wx.StaticText(panel, label="From")
        fileFromValue = wx.StaticText(panel, label="https://s3-eu-west1-itune.com",style=wx.CENTER | wx.NO_BORDER|wx.TE_READONLY|wx.TE_DONTWRAP)
#         fileFromValue.SetValue("https://s3-eu-west1-itune.com")
        buttonOpen = wx.Button(panel, wx.ID_YES, "Open")
        buttonOpen.Bind(wx.EVT_BUTTON, self.OnFileOpen, buttonOpen) 
        buttonSave = wx.Button(panel, wx.ID_YES, "Save")
        buttonSave.Bind(wx.EVT_BUTTON, self.OnFileSave, buttonSave) 
        buttonCancel = wx.Button(panel, wx.ID_YES, "Cancel")
        buttonCancel.Bind(wx.EVT_BUTTON, self.OnCancel, buttonCancel) 
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        gSizer = wx.GridBagSizer(5, 5)
        gSizer.Add(NameFile, pos=(0, 1), flag=wx.ALL, border=2)
        gSizer.Add(NameFileValue, pos=(0, 2))
        gSizer.Add(fileType, pos=(1, 1), flag=wx.ALL, border=2)
        gSizer.Add(fileTypeValue, pos=(1, 2))
        gSizer.Add(fileFrom, pos=(2, 1), flag=wx.ALL, border=2)
        gSizer.Add(fileFromValue, pos=(2, 2))
        gSizer.Add(buttonOpen, pos=(4, 2))
        gSizer.Add(buttonSave, pos=(4, 3))
        gSizer.Add(buttonCancel, pos=(4, 4))
        
        fileImage = wx.Image(globalTracker.propertyVar.phase3images+"/blankFile.jpg", type=wx.BITMAP_TYPE_ANY)
        fileImage = fileImage.Scale(30, 30, wx.IMAGE_QUALITY_HIGH)
        fileImageBitmap = wx.StaticBitmap(panel, bitmap=fileImage.ConvertToBitmap())
        
        hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer1.Add(fileImageBitmap, flag=wx.ALL)
        hSizer1.Add(gSizer, flag=wx.ALL | wx.EXPAND, border=0)
#         stBox = wx.StaticBox(panel, label='', pos=(4, 0), size=(404, 190))
        
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.Add((50, 10))
        vSizer.Add(hSizer)
        vSizer.Add(hSizer1)
        
        panel.SetSizer(vSizer) 
        self.Layout()
            
    def getDialogTag(self):
        return self.dialogTag
    
    def getDialogID(self):
        return self.dialogID
        
    def OnFileOpen(self, event):
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.MP3_OPEN
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
#         print "Open downloaded file"
        dial = wx.MessageDialog(self, "The file cannot be opened due to codec error", "ERROR", wx.OK | wx.OK_DEFAULT | wx.ICON_QUESTION)
        ret = dial.ShowModal()
        if ret == wx.ID_YES:
            self.Destroy()
        else:
            event.Skip()
        self.Destroy()
    
    def OnFileSave(self, event):
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.MP3_SAVE
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
#         print "Save downloaded"
        
        d = PBI.PyBusyInfo("Downloaded file saved", title="")
        wx.Yield()
        time.sleep(2)
        del d
        self.Destroy()
    
    def OnCancel(self, event):
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.MP3_CANCEL
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
#         globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        self.Destroy()
    
    def onClose(self, event):
        RESPONSECODE.previousResponse=RESPONSECODE.currentResponse
        RESPONSECODE.previousResponseCode=RESPONSECODE.currentResponseCode
        RESPONSECODE.currentResponse=RESPONSECODE.DIALOG_CLOSE
        RESPONSECODE.currentResponseCode=RESPONSECODE.RESPONSE[RESPONSECODE.currentResponse]
#         globalTracker.math.changeStatusFromInitializedToClosed(self.mathsQNumber, self.loadNumber)
        self.Destroy()
        
class window(wx.Window):     
    def __init__(self, parent):
        wx.Window.__init__(self, parent=parent, id=wx.ID_ANY, size=(520, 360), name="window")
        wx.Window.SetBackgroundColour(self, "Green")   
                
def main():
    ex = wx.App()
    w = window(wx.Frame(parent=None))
   
    dial = WindowsDownloadPopup(w)
    dial.ShowModal()
    
    
#     print result
#     if result == wx.ID_CANCEL:
#         dial.getButtonClickResult(wx.ID_CANCEL)
    ex.MainLoop()
if __name__ == "__main__":     
    main()
