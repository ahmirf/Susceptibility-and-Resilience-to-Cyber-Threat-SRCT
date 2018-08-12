'''
Created on Jun 3, 2015

@author: Anjila
'''
import wx

class Password_Verifier(wx.PyValidator):
    
#     def __init__(self):
#         super(CustomNumValidator, self).__init__()
    def __init__ (self):
        print "init"
        wx.PyValidator . __init__ (self)
        
    def Clone (self):
        return Password_Verifier ()
    
    def TransferToWindow (self):
        return True
    
    def TransferFromWindow (self):
        return True
    
    def Validate (self, win):
        print "here in the password verifier"
        textCtrl = self.GetWindow() 
        text = textCtrl.GetValue() 
        
        if not text == None: 
            len=len(text)
            for index in [0,len]:
                if not ((text[index]>=48 and text[index]<=57 ) or text[index]=="."):
                    textCtrl.SetBackgroundColour("red") 
                    wx.MessageBox("Only numeric values are acceptable!", "Error")
                    textCtrl.SetFocus() 
                    textCtrl.Refresh() 
            return False 
        else:
            return True
  
# def main():
#     a="0h"
#     print a[0]
#     print  ord(a[0])==57
#      
# main()      