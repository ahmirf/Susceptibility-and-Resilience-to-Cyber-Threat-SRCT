'''
Created on Jan 13, 2015

@author: Anjila
'''
import BalloonTip as BT

import wx,globalTracker

class MyTaskbar(wx.PyControl):

    def __init__(self, parent, emailFrame, iconWidth, taskbarHeight, rightWidth, remainingWidth):
        print "===> MyTaskbar.py initiated"
        self.displaySize = wx.GetDisplaySize()
        wx.PyControl.__init__(self, parent)
        self.panelmain = parent
        self.emailFrame = emailFrame
        self.iconwidth = iconWidth
        self.height = taskbarHeight
        self.rightwidth = rightWidth
        self.remainingwidth = remainingWidth
        frameWidth = 590
        self.fullSize = wx.DisplaySize()
        self.emailFramePos = ((self.fullSize[0] - frameWidth), 20)
        self.taskbarImg1 = globalTracker.propertyVar.taskbarImg1
        self.taskbarImg2 = globalTracker.propertyVar.taskbarImg2
        self.taskbarImg3 = globalTracker.propertyVar.taskbarImg3
        self.taskbarImg4 = globalTracker.propertyVar.taskbarImg4
        self.taskbarImg5 = globalTracker.propertyVar.taskbarImg5
        self.taskbarImg6 = globalTracker.propertyVar.taskbarImg6
        self.infoImg = globalTracker.propertyVar.InformationSymbol
        self.initiate() 
        
    def initiate(self):
        self.panel1 = wx.Panel(self.panelmain, style=wx.ALL)
        self.panel2 = wx.Panel(self.panelmain, style=wx.ALL)
        self.panel3 = wx.Panel(self.panelmain, style=wx.ALL)
        self.panel4 = wx.Panel(self.panelmain, style=wx.ALL)
        self.panel5 = wx.Panel(self.panelmain, style=wx.ALL)
        self.panel6 = wx.Panel(self.panelmain, style=wx.ALL)
        self.taskbarBit1 = self.getScaledBitmap(self.taskbarImg1, self.iconwidth, self.height)
        self.taskbar1 = wx.StaticBitmap(self.panel1, bitmap=self.taskbarBit1)
        self.taskbarBit2 = self.getScaledBitmap(self.taskbarImg2, self.iconwidth, self.height)
        self.taskbar2 = wx.StaticBitmap(self.panel2, bitmap=self.taskbarBit2)
        # eamil icon
        self.taskbarBit3 = self.getScaledBitmap(self.taskbarImg3, self.iconwidth, self.height)
        self.taskbar3 = wx.StaticBitmap(self.panel3, bitmap=self.taskbarBit3)
        self.taskbar3.Bind(wx.EVT_LEFT_UP, self.onEmailIconClick, self.taskbar3)
        self.taskbar3.Bind(wx.EVT_PAINT, self.onEmailIconClickPaint, self.taskbar3)
        # chat icon
        self.taskbarBit4 = self.getScaledBitmap(self.taskbarImg4, self.iconwidth, self.height)
        self.taskbar4 = wx.StaticBitmap(self.panel4, bitmap=self.taskbarBit4)
        self.taskbar4.Bind(wx.EVT_LEFT_UP, self.onChatIconClick, self.taskbar4)
        self.taskbarBit5 = self.getScaledBitmap(self.taskbarImg5, self.remainingwidth, self.height)
        self.taskbar5 = wx.StaticBitmap(self.panel5, bitmap=self.taskbarBit5)
        self.taskbarBit6 = self.getScaledBitmap(self.taskbarImg6, self.rightwidth, self.height)
        self.taskbar6 = wx.StaticBitmap(self.panel6, bitmap=self.taskbarBit6)
        self.panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panelSizer.Add(self.panel1, 0, wx.ALL, 1)
        self.panelSizer.Add(self.panel2, 0, wx.ALL, 1)
        self.panelSizer.Add(self.panel3, 0, wx.ALL, 1)
        self.panelSizer.Add(self.panel4, 0, wx.ALL, 0)
        self.panelSizer.Add(self.panel5, 0, wx.ALL, 0)
        self.panelSizer.Add(self.panel6, 0, wx.ALL, 0)
        self.psizer = wx.BoxSizer(wx.VERTICAL)
        self.psizer.Add(self.panelSizer)
        self.panelmain.SetSizer(self.psizer)
        message = "A new version of Java is ready to be installed!\n\rClick here to continue."
        toptitle = "Java Update Available"
        tipballoon1 = BT.BalloonTip(topicon=None, toptitle=toptitle,
                                       message=message, shape=BT.BT_RECTANGLE,
                                       tipstyle=BT.BT_BUTTON)
        # Set The Target
        tipballoon1.SetTarget(self.taskbar6)
        # Set The Balloon Colour
        tipballoon1.SetBalloonColour(wx.WHITE)
        # Set The Font For The Top Title
        titleFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        tipballoon1.SetTitleFont(titleFont)
        # Set The Colour For The Top Title
        tipballoon1.SetTitleColour("#002A85")
        # Set The Font For The Tip Message
        msgFont = wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD)
        tipballoon1.SetMessageFont(msgFont)
        # Set The Colour For The Tip Message
        tipballoon1.SetMessageColour(wx.BLACK)
#         # Set The Delay After Which The BalloonTip Is Created
#         tipballoon1.SetStartDelay(1000)
#         # Set The Delay After Which The BalloonTip Is Destroyed
#         tipballoon1.SetEndDelay(3000)
        #tipballoon1.OnDestroy(self,event)
        self.tip = tipballoon1  
        
    def showJavaUpdate(self, loadNumber, mathsQNumber, startTime):
        #print str(loadNumber) + str(mathsQNumber) + str(startTime)
        self.tip.setValues(loadNumber, mathsQNumber, startTime)
        self.StartJavaUpdate()
        self.tip.onMySanket()
       
    def StartJavaUpdate(self):
        #shows the balloon tip after 1000ms upto 3000 ms from the time of showing 
        # Set The Delay After Which The BalloonTip Is Created
        self.tip.SetStartDelay(1000)
        # Set The Delay After Which The BalloonTip Is Destroyed
        self.tip.SetEndDelay(7000)
       
    def ontaskbar1Click(self, event):
        print "taskbar1"
        event.Skip()
        
    def ontaskbar2Click(self, event):
        print "taskbar2"
        self.tip.EnableTip(True)
        event.Skip()
        
    def onEmailIconClick(self, event):
        # email window should open 
        print "email icon has been clicked"
        if not self.emailFrame == None:
            print "email frame maximized"
            self.emailFrame.SetPosition(self.emailFramePos)
            self.emailFrame.Maximize()
            self.emailFrame.Raise()
            if not self.emailFrame.IsShown():
                self.emailFrame.Show()
        event.Skip()
        
    def onEmailIconClickPaint(self,event):
        dc = wx.PaintDC(self.panelmain)
        dc.SetBrush(wx.Brush('Red'))
        dc.DrawRectangle(self.emailFramePos[0], self.emailFramePos[1], 200, 800)
        wx.Sleep(3)
        event.Skip()
        
    def onChatIconClick(self, event):
        # chat window should open
        event.Skip()
        
    def ontaskbar5Click(self, event):
#         "taskbar5
        event.Skip()
        
    def getBitmap(self, imageStr):
        image = wx.Image(imageStr, type=wx.BITMAP_TYPE_ANY)
        return image.ConvertToBitmap()
    
    def getScaledBitmap(self, imageStr, width, height):
        image = wx.Image(imageStr, type=wx.BITMAP_TYPE_ANY)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        return image.ConvertToBitmap()
    
class ChildFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title=title)     
    
if __name__ == '__main__':    
    app = wx.App()
    displaySize = wx.GetDisplaySize()
    print "screen size= "+ str(displaySize)
#     frame = MyTaskbar(None, (displaySize[0], 0.1 * displaySize[1]))
    emailFrame=ChildFrame(None, 1, "email")
    
    displaySize = wx.GetDisplaySize()
    taskbarHeight = 0.0375 * displaySize[1]
    taskbarIconwidth = 3.125 / 100 * displaySize[0]
    taskbarRightIconwidth = 8.07 / 100 * displaySize[0]
    taskbarRemainingWidth = displaySize[0] - (4 * taskbarIconwidth + taskbarRightIconwidth)
    taskbar = MyTaskbar(emailFrame, emailFrame, taskbarIconwidth, taskbarHeight, taskbarRightIconwidth, taskbarRemainingWidth)
#     frame.Show(True)
    taskbar.Show(True)
    
#     print "postion of panel 6=================>"+str(taskbar.panel6.GetScreenPosition())
#     print "postion of mainpanel=================>"+str(taskbar.panelmain.GetScreenPosition())
    
    app.MainLoop()
    

        

        
