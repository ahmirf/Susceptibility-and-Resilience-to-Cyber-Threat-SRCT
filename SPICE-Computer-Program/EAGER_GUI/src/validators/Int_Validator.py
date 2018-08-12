'''
Created on Jan 27, 2015

@author: Anjila
'''
import wx


class Int_Validator (wx.PyValidator):
    def __init__ (self):
        wx.PyValidator . __init__ (self)
        
    def Clone (self):
        return Int_Validator ()
    
    def TransferToWindow (self):
        return True
    
    def TransferFromWindow (self):
        return True
    
    def Validate (self, win):
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

