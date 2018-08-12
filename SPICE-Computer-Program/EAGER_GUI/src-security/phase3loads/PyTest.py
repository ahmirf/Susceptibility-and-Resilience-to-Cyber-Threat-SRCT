'''
Created on Jan 28, 2016

@author: AnjilaTam
'''
import wx


class pYtest():
    
    def __init__(self): 
        global var
        pYtest.var=1
        print pYtest.var
        pYtest2()
        print pYtest.var
        pYtest3()
        print pYtest.var

class pYtest2():
    
    def __init__(self): 
        pYtest.var=2
        
class pYtest3():
    
    def __init__(self): 
        pYtest.var=3


                   
def main():
    ex = wx.App()
#     w = window(wx.Frame()) 
    dial = pYtest()

#     dial.ShowModal()
#     print "response= "+RESPONSECODE.currentResponse+"\t"+RESPONSECODE.individualResponse
    ex.MainLoop()
    
    
if __name__ == "__main__":     
    main()
#     print RESPONSECODE.currentResponse