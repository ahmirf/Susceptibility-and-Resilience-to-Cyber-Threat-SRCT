# --------------------------------------------------------------------------- #
# BALLOONTIP wxPython IMPLEMENTATION
# Python Code By:
#
# Andrea Gavana, @ 29 May 2005
# Latest Revision: 6 September 2005, 22.00 CET
#
#
# TODO List/Caveats
#
# 1. With wx.ListBox (And Probably Other Controls), The BalloonTip Sometimes
#    Flashes (It Is Created And Suddenly Destroyed). I Don't Know What Is
#    Happening. Probably I Don't Handle Correctly The wx.EVT_ENTER_WINDOW
#    wx.EVT_LEAVE_WINDOW?
#
# 2. wx.RadioBox Seems Not To Receive The wx.EVT_ENTER_WINDOW Event
#
# 3. wx.SpinCtrl (And Probably Other Controls), When Put In A Sizer, Does Not
#    Return The Correct Size/Position. Probably Is Something I Am Missing.
#
# 4. Other Issues?
#
#
# FIXED Problems
#
# 1. Now BalloonTip Control Works Also For TaskBarIcon (Thanks To Everyone
#    For The Suggetions I Read In The wxPython Mailing List)
#
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# andrea.gavana@agip.it
# andrea_gavan@tin.it
#
# Or, Obviously, To The wxPython Mailing List!!!
#
#
# End Of Comments
# --------------------------------------------------------------------------- #

""" Description:

BalloonTip Is A Class That Allows You To Display Tooltips In A Balloon Style
Window (Actually A Frame), Similarly To The Windows XP Balloon Help. There Is
Also An Arrow That Points To The Center Of The Control Designed As A "Target"
For The BalloonTip.


What It Can Do:

- Set The Balloon Shape As A Rectangle Or A Rounded Rectangle;
- Set An Icon To The Top-Left Of The BalloonTip Frame;
- Set A Title At The Top Of The BalloonTip Frame;
- Automatic "Best" Placement Of BalloonTip Frame Depending On The Target
  Control/Window Position;
- Runtime Customization Of Title/Tip Fonts And Foreground Colours;
- Runtime Change Of BalloonTip Frame Shape;
- Set The Balloon Background Colour;
- Possibility To Set The Delay After Which The BalloonTip Is Displayed;
- Possibility To Set The Delay After Which The BalloonTip Is Destroyed;
- Three Different Behaviors For The BalloonTip Window (Regardless The Delay
  Destruction Time Set):
  a) Destroy By Leave: The BalloonTip Is Destroyed When The Mouse Leaves The
     Target Control/Window;
  b) Destroy By Click: The BalloonTip Is Destroyed When You Click On Any Area
     Of The Target Control/Window;
  c) Destroy By Button: The BalloonTip Is Destroyed When You Click On The
     Top-Right Close Button;
- Possibility To Enable/Disable Globally The BalloonTip On You Application.
- Set The BalloonTip Also For The TaskBarIcon (Revised 7 September 2005)


Usage Example:

# Let's Suppose That In Your Application You Have A wx.TextCtrl Defined As:

mytextctrl = wx.TextCtrl(panel, -1, "I Am A TextCtrl")

# You Can Define Your BalloonTip As Follows:

tipballoon = BalloonTip(topicon=None, toptitle="TextCtrl",
                        message="This Is A TextCtrl",
                        shape=BT_ROUNDED,
                        tipstyle=BT_LEAVE)

# Set The BalloonTip Target
tipballoon.SetTarget(mytextctrl)
# Set The BalloonTip Background Colour
tipballoon.SetBalloonColour(wx.WHITE)
# Set The Font For The Balloon Title
tipballoon.SetTitleFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False))
# Set The Colour For The Balloon Title
tipballoon.SetTitleColour(wx.BLACK)
# Leave The Message Font As Default
tipballoon.SetMessageFont()
# Set The Message (Tip) Foreground Colour
tipballoon.SetMessageColour(wx.LIGHT_GREY)
# Set The Start Delay For The BalloonTip
tipballoon.SetStartDelay(1000)
# Set The Time After Which The BalloonTip Is Destroyed
tipballoon.SetEndDelay(3000)


BalloonTip Is Freeware And Distributed Under The wxPython License. 

Latest Revision: Andrea Gavana @ 7 September 2005, 22.00 CET

"""


import time

import wx
from wx.lib.buttons import GenButton
import CustomDialog
from dialogMsgPojo import dialogMsgPojo
from dialogUtils import dialogUtils
import globalTracker,time
from globalTracker import RESPONSECODE,CONSTANTS
from globalTracker import globalVar
import wx.lib.agw.pybusyinfo as PBI

# Define The Values For The BalloonTip Frame Shape
BT_ROUNDED = 1
BT_RECTANGLE = 2

# Define The Value For The BalloonTip Destruction Behavior
BT_LEAVE = 3
BT_CLICK = 4
BT_BUTTON = 5


# ---------------------------------------------------------------
# Class BalloonFrame
# ---------------------------------------------------------------
# This Class Is Called By The Main BalloonTip Class, And It Is
# Responsible For The Frame Creation/Positioning On Screen
# Depending On Target Control/Window, The Frame Can Position
# Itself To NW (Default), NE, SW, SE. The Switch On Positioning
# Is Done By Calculating The Absolute Position Of The Target
# Control/Window Plus/Minus The BalloonTip Size. The Pointing
# Arrow Is Positioned Accordingly.
# ---------------------------------------------------------------

class BalloonFrame(wx.Frame):
    
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, classparent=None):
        """Default Class Constructor.

        Used Internally. Do Not Call Directly This Class In Your Application!
        """        
        
        wx.Frame.__init__(self, None, -1, "BalloonTip", pos, size,
                          style=wx.FRAME_SHAPED | 
                          wx.SIMPLE_BORDER | 
                          wx.FRAME_NO_TASKBAR | 
                          wx.STAY_ON_TOP)

        self._parent = classparent# parent is balloonTip
        #parent is not being used but since parent being set is taskbar6 we can use this to set the position of balloonTio
        self.widgetTosetBalloonTipPosn=parent
        self._toptitle = self._parent._toptitle
        self._topicon = self._parent._topicon
        self._message = self._parent._message
        self._shape = self._parent._shape
        self._tipstyle = self._parent._tipstyle

        self._ballooncolour = self._parent._ballooncolour
        self._balloonmsgcolour = self._parent._balloonmsgcolour
        self._balloonmsgfont = self._parent._balloonmsgfont

        if self._toptitle != "":
            self._balloontitlecolour = self._parent._balloontitlecolour
            self._balloontitlefont = self._parent._balloontitlefont

        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.panel = panel
        
        subsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        subsizer.Add((0, 20), 0, wx.EXPAND)
        
        if self._topicon is not None:
            stb = wx.StaticBitmap(panel, -1, self._topicon)
            hsizer.Add(stb, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
            self._balloonbmp = stb
            
        if self._toptitle != "":
            stt = wx.StaticText(panel, -1, self._toptitle)
            stt.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False))
            if self._topicon is None:
                hsizer.Add((10, 0), 0, wx.EXPAND)

            hsizer.Add(stt, 1, wx.EXPAND | wx.TOP, 10)
            self._balloontitle = stt
            self._balloontitle.SetForegroundColour(self._balloontitlecolour)
            self._balloontitle.SetFont(self._balloontitlefont)

        if self._tipstyle == BT_BUTTON:
            self._closebutton = GenButton(panel, -1, "X", style=wx.NO_BORDER)
            self._closebutton.SetMinSize((16, 16))
            self._closebutton.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False))
            self._closebutton.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterButton)
            self._closebutton.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveButton)
            self._closebutton.SetUseFocusIndicator(False)
            if self._toptitle != "":
                hsizer.Add(self._closebutton, 0, wx.TOP | wx.RIGHT, 5)
            else:
                hsizer.Add((10, 0), 1, wx.EXPAND)
                hsizer.Add(self._closebutton, 0, wx.ALIGN_RIGHT | wx.TOP
                           | wx.RIGHT, 5)
            
        if self._topicon is not None or self._toptitle != "" \
           or self._tipstyle == BT_BUTTON:
            
            subsizer.Add(hsizer, 0, wx.EXPAND | wx.BOTTOM, 5)
        mainstt = wx.StaticText(panel, -1, self._message)

        self._balloonmsg = mainstt
        self._balloonmsg.SetForegroundColour(self._balloonmsgcolour)
        self._balloonmsg.SetFont(self._balloonmsgfont)
        
        padsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        padsizer.Add((29, 1))
        padsizer.Add(self._balloonmsg)
        subsizer.Add(padsizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | 
                     wx.BOTTOM, 10)
        subsizer.Add((0, 0), 1)
        panel.SetSizer(subsizer)
        
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizerAndFit(sizer)
        sizer.Layout()

        if self._tipstyle == BT_CLICK:
            if self._toptitle != "":
                self._balloontitle.Bind(wx.EVT_LEFT_DOWN, self.OnClose)

            if self._topicon is not None:
                self._balloonbmp.Bind(wx.EVT_LEFT_DOWN, self.OnClose)
                
            self._balloonmsg.Bind(wx.EVT_LEFT_DOWN, self.OnClose)
            self.panel.Bind(wx.EVT_LEFT_DOWN, self.OnClose)

        elif self._tipstyle == BT_BUTTON:
            self._closebutton.Bind(wx.EVT_BUTTON, self.OnClose)

        self.panel.SetBackgroundColour(self._ballooncolour)
        
        if wx.Platform == "__WXGTK__":
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetBalloonShape)
        else:
            self.SetBalloonShape()

        self.Show(True)
    
    
    def SetBalloonShape(self, event=None):
        """Sets The Balloon Shape."""

        size = self.GetSize()
        dc = wx.MemoryDC()
        textlabel = self._balloonmsg.GetLabel()
        textfont = self._balloonmsg.GetFont()
        textextent = dc.GetFullTextExtent(textlabel, textfont)

        boxheight = size.y - textextent[1] * len(textlabel.split("\n\r"))
        boxwidth = size.x
 #TODO:  here it takes the mouse position. Instead we have to position it such that it comes out from the taskbar 
#         position = wx.GetMousePosition()
        position=self.widgetTosetBalloonTipPosn.GetScreenPosition()
        print self.widgetTosetBalloonTipPosn.GetScreenPosition()
        position[0]=wx.GetDisplaySize()[0]-40
        
        xpos = position[0]
        ypos = position[1]

        if xpos > 20 and ypos > 20:
            
            # This Is NW Positioning
            positioning = "NW"
            xpos = position[0] - boxwidth + 20
            ypos = position[1] - boxheight - 20
            
        elif xpos <= 20 and ypos <= 20:

            # This Is SE Positioning
            positioning = "SE"
            xpos = position[0] - 20
            ypos = position[1] 

        elif xpos > 20 and ypos <= 20:

            # This Is SW Positioning
            positioning = "SW"
            xpos = position[0] - boxwidth + 20
            ypos = position[1] 

        else:

            # This Is NE Positioning
            positioning = "NE"
            xpos = position[0] 
            ypos = position[1] - boxheight + 20
             
        bmp = wx.EmptyBitmap(size.x, size.y)
        dc = wx.BufferedDC(None, bmp)
        dc.BeginDrawing()
        dc.SetBackground(wx.Brush(wx.Colour(0, 0, 0), wx.SOLID))
        dc.Clear()
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1, wx.TRANSPARENT))

        if self._shape == BT_ROUNDED:
            dc.DrawRoundedRectangle(0, 20, boxwidth, boxheight - 20, 12)
                
        elif self._shape == BT_RECTANGLE:
            dc.DrawRectangle(0, 20, boxwidth, boxheight - 20)

        if positioning == "NW":
            dc.DrawPolygon(((boxwidth - 40, boxheight), (boxwidth - 20, boxheight + 20),
                            (boxwidth - 20, boxheight)))
        elif positioning == "SE":
            dc.DrawPolygon(((20, 20), (20, 0), (40, 20)))

        elif positioning == "SW":
            dc.DrawPolygon(((boxwidth - 40, 20), (boxwidth - 20, 0), (boxwidth - 20, 20)))

        else:
            dc.DrawPolygon(((20, boxheight), (20, boxheight + 20), (40, boxheight)))
            
        dc.EndDrawing()

        r = wx.RegionFromBitmapColour(bmp, wx.Colour(0, 0, 0))
        self.hasShape = self.SetShape(r)

        if self._tipstyle == BT_BUTTON:
            colour = self.panel.GetBackgroundColour()
            self._closebutton.SetBackgroundColour(colour)

        self.SetPosition((xpos, ypos))
        

    def OnEnterButton(self, event):
        """Handles The wx.EVT_ENTER_WINDOW For The BalloonTip Button.

        When The BalloonTip Is Created With The TipStyle=BT_BUTTON, This Event
        Provide Some Kind Of 3D Effect When The Mouse Enters The Button Area.
        """
        
        button = event.GetEventObject()
        colour = button.GetBackgroundColour()
        red = colour.Red()
        green = colour.Green()
        blue = colour.Blue()
        
        if red < 30:
            red = red + 30
        if green < 30:
            green = green + 30
        if blue < 30:
            blue = blue + 30
            
        colour = wx.Colour(red - 30, green - 30, blue - 30)
        button.SetBackgroundColour(colour)
        button.SetForegroundColour(wx.WHITE)
        button.Refresh()
        event.Skip()


    def OnLeaveButton(self, event):
        """Handles The wx.EVT_LEAVE_WINDOW For The BalloonTip Button.

        When The BalloonTip Is Created With The TipStyle=BT_BUTTON, This Event
        Restore The Button Appearance When The Mouse Leaves The Button Area.
        """
        
        button = event.GetEventObject()
        colour = self.panel.GetBackgroundColour()
        button.SetBackgroundColour(colour)
        button.SetForegroundColour(wx.BLACK)
        button.Refresh()
        event.Skip()
        

    def OnClose(self, event):
        """ Handles The wx.EVT_CLOSE Event."""

        if isinstance(self._parent._widget, wx.TaskBarIcon):
            self._parent.taskbarcreation = 0
            self._parent.taskbartime.Stop()
            del self._parent.taskbartime
            del self._parent.BalloonFrame
        self.Destroy()        


# ---------------------------------------------------------------
# Class BalloonTip
# ---------------------------------------------------------------
# This Is The Main BalloonTip Implementation
# ---------------------------------------------------------------

class BalloonTip:

    def __init__(self, topicon=None, toptitle="",
                 message="", shape=BT_ROUNDED, tipstyle=BT_LEAVE):
        """Deafult Class Constructor.

        BalloonTip.__init__(self, topicon=None, toptitle="", message="",
                            shape=BT_ROUNDED, tipstyle=BT_LEAVE)

        Parameters:
        
        - topicon: An Icon That Will Be Displayed On The Top-Left Part Of The
          BalloonTip Frame. If Set To None, No Icon Will Be Displayed;
        - toptile: A Title That Will Be Displayed On The Top Part Of The
          BalloonTip Frame. If Set To An Empty String, No Title Will Be Displayed;
        - message: The Tip Message That Will Be Displayed. It Can Not Be Set To
          An Empty String;
        - shape: The BalloonTip Shape. It Can Be One Of:
          a) BT_RECTANGLE (A Rectangle);
          b) BT_ROUNDED (Rounded Rectangle, The Default).
        - tipstyle: The BalloonTip Destruction Behavior. It Can Be One Of:
          a) BT_LEAVE: The BalloonTip Is Destroyed When The Mouse Leaves The
             Target Control/Window;
          b) BT_CLICK: The BalloonTip Is Destroyed When You Click On Any Area
             Of The Target Control/Window;
          c) BT_BUTTON: The BalloonTip Is Destroyed When You Click On The
             Top-Right Close Button;
        """                            


        self._shape = shape
        self._topicon = topicon
        self._toptitle = toptitle
        self._message = message
        self._tipstyle = tipstyle

        app = wx.GetApp()
        self._runningapp = app
        self._runningapp.__tooltipenabled__ = True

        if self._message == "":
            raise "\nERROR: You Should At Least Set The Message For The BalloonTip"

        if self._shape not in [BT_ROUNDED, BT_RECTANGLE]:
            raise '\nERROR: BalloonTip Shape Should Be One Of "BT_ROUNDED", "BT_RECTANGLE"'

        if self._tipstyle not in [BT_LEAVE, BT_CLICK, BT_BUTTON]:
            msg = '\nERROR: BalloonTip TipStyle Should Be One Of "BT_LEAVE", '\
                  '"BT_CLICK", "BT_BUTTON"'
            raise msg

        self.SetStartDelay()
        self.SetEndDelay()
        self.SetBalloonColour()
        
        if toptitle != "":
            self.SetTitleFont()
            self.SetTitleColour()

        if topicon is not None:
            self.SetBalloonIcon(topicon)

        self.SetMessageFont()
        self.SetMessageColour()


    def SetTarget(self, widget):
        """Sets The Target Control/Window For The BalloonTip."""

        self._widget = widget
#         print "here1"
#         print type(widget.GetParent())
#         print widget.GetParent().GetScreenPosition()
        
        if isinstance(widget, wx.TaskBarIcon):
            self._widget.Bind(wx.EVT_TASKBAR_MOVE, self.OnTaskBarMove)
            self._widget.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
            self.taskbarcreation = 0
        else:
            self._widget.Bind(wx.EVT_ENTER_WINDOW, self.OnWidgetEnter)
            self._widget.Bind(wx.EVT_LEAVE_WINDOW, self.OnWidgetLeave)
            self._widget.Bind(wx.EVT_MOTION, self.OnWidgetMotion)
            self._widget.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        

    def GetTarget(self):
        """Returns The Target Window For The BalloonTip."""
        
        if not hasattr(self, "_widget"):
            raise "\nERROR: BalloonTip Target Has Not Been Set"

        return self._widget
    

    def SetStartDelay(self, delay=1):
        """Sets The Delay Time After Which The BalloonTip Is Created."""
        
        if delay < 1:
            raise "\nERROR: Delay Time For BalloonTip Creation Should Be Greater Than 1 ms"
        
        self._startdelaytime = float(delay)        
        

    def GetStartDelay(self):
        """Returns The Delay Time After Which The BalloonTip Is Created."""

        return self._startdelaytime
    

    def SetEndDelay(self, delay=1e6):
        """Sets The Delay Time After Which The BalloonTip Is Destroyed."""
        
        if delay < 1:
            raise "\nERROR: Delay Time For BalloonTip Destruction Should Be Greater Than 1 ms"

        self._enddelaytime = float(delay)
        

    def GetEndDelay(self):
        """Returns The Delay Time After Which The BalloonTip Is Destroyed."""
        
        return self._enddelaytime
    

    def OnWidgetEnter(self, event):
        """Starts The BalloonTip Timer For Creation."""
        
        if hasattr(self, "BalloonFrame"):
            if self.BalloonFrame:
                return

        if not self._runningapp.__tooltipenabled__:
            return
        
        
        #TODO: donot do // this triggers the start of the balloon tip
#         self.showtime = wx.PyTimer(self.NotifyTimer)
#         self.showtime.Start(self._startdelaytime)
    
        event.Skip()
        
    def onMySanket(self):
        if hasattr(self, "BalloonFrame"):
            if self.BalloonFrame:
                return

        if not self._runningapp.__tooltipenabled__:
            return
        
        self.showtime = wx.PyTimer(self.NotifyTimer)
        # this triggers the start of the balloon tip
        self.showtime.Start(self._startdelaytime)
    

        
    def OnWidgetLeave(self, event):
        """Handles The wx.EVT_LEAVE_WINDOW For The Target Control/Window.

        If The BalloonTip tipstyle Is Set To BT_LEAVE, The BalloonTip Is Destroyed.
        """

        if hasattr(self, "showtime"):
            if self.showtime:
                self.showtime.Stop()
                del self.showtime

        if hasattr(self, "BalloonFrame"):
            if self.BalloonFrame:
                if self._tipstyle == BT_LEAVE:
                    endtime = time.time()
                    if endtime - self.starttime > 0.1:
                        try:
                            self.BalloonFrame.Destroy()
                        except:
                            pass
                else:
                    event.Skip()
            else:
                event.Skip()
        else:
            event.Skip()
            

    def OnTaskBarMove(self, event):
        """ Handles The Mouse Motion Inside The TaskBar Icon. """
        
        if not hasattr(self, "BalloonFrame"):
            if self.taskbarcreation == 0:
                self.mousepos = wx.GetMousePosition()
                self.currentmousepos = self.mousepos
                self.taskbartime = wx.PyTimer(self.TaskBarTimer)
                self.taskbartime.Start(100)
                self.showtime = wx.PyTimer(self.NotifyTimer)
                self.showtime.Start(self._startdelaytime)
                    
            if self.taskbarcreation == 0:
                self.taskbarcreation = 1

            return
        
        event.Skip()
        

    def OnWidgetMotion(self, event):
        """Handle The Mouse Motion Inside The Target.

        This Prevents The Annoying Behavior Of BalloonTip To Display When The
        User Does Something Else Inside The Window. The BalloonTip Window Is
        Displayed Only When The Mouse Does *Not* Move For The Start Delay Time.
        """
        
#         if hasattr(self, "BalloonFrame"):
#             if self.BalloonFrame:
#                 return
#             
#         if hasattr(self, "showtime"):
#             if self.showtime:
#                 self.showtime.Start(self._startdelaytime)

        event.Skip()
        

    def NotifyTimer(self):
        """The Creation Timer Has Expired. Creates The BalloonTip Frame."""
        
        self.BalloonFrame = BalloonFrame(self._widget, classparent=self)
        self.BalloonFrame.Show(True)
        self.starttime = time.time()
        
        self.showtime.Stop()
        del self.showtime
#         print "here ============================>"
        self.destroytime = wx.PyTimer(self.DestroyTimer)
        self.destroytime.Start(self._enddelaytime)
        

    def TaskBarTimer(self):
        """This Timer Check Periodically The Mouse Position.

        If The Current Mouse Position Is Sufficiently Far From The Coordinates
        It Had When Entered The TaskBar Icon And The BalloonTip Style Is
        BT_LEAVE, The BalloonTip Frame Is Destroyed.
        """
        
        self.currentmousepos = wx.GetMousePosition()
        mousepos = self.mousepos

        if abs(self.currentmousepos[0] - mousepos[0]) > 30 or \
           abs(self.currentmousepos[1] - mousepos[1]) > 30:
            if hasattr(self, "BalloonFrame"):
                if self._tipstyle == BT_LEAVE:
                    try:
                        self.BalloonFrame.Destroy()
                        self.taskbartime.Stop()
                        del self.taskbartime
                        del self.BalloonFrame
                        self.taskbarcreation = 0
                    except:
                        pass

        
    def DestroyTimer(self):
        """The Destruction Timer Has Expired. Destroys The BalloonTip Frame."""
        
        self.destroytime.Stop()
        del self.destroytime
        
        try:
            self.BalloonFrame.Destroy()
        except:
            pass


    def SetBalloonShape(self, shape=BT_ROUNDED):
        """Sets The BalloonTip Frame Shape.

        It Should Be One Of BT_ROUNDED, BT_RECTANGLE.
        """
        
        if shape not in [BT_ROUNDED, BT_RECTANGLE]:
            raise '\nERROR: BalloonTip Shape Should Be One Of "BT_ROUNDED", "BT_RECTANGLE"'

        self._shape = shape


    def GetBalloonShape(self):
        """Returns The BalloonTip Frame Shape."""
        
        return self._shape


    def SetBalloonIcon(self, icon):
        """Sets The BalloonTip Top-Left Icon."""
        
        if icon.Ok():
            self._topicon = icon
        else:
            raise "\nERROR: Invalid Image Passed To BalloonTip"


    def GetBalloonIcon(self):
        """Returns The BalloonTip Top-Left Icon."""
        
        return self._topicon


    def SetBalloonTitle(self, title=""):
        """Sets The BalloonTip Top Title."""
        
        self._toptitle = title


    def GetBalloonTitle(self):
        """Returns The BalloonTip Top Title."""
        
        return self._toptitle


    def SetBalloonMessage(self, message):
        """Sets The BalloonTip Tip Message. It Should Not Be Empty."""
        
        if len(message.strip()) < 1:
            raise "\nERROR: BalloonTip Message Can Not Be Empty"
        
        self._message = message


    def GetBalloonMessage(self):
        """Returns The BalloonTip Tip Message."""
        
        return self._message


    def SetBalloonTipStyle(self, tipstyle=BT_LEAVE):
        """Sets The BalloonTip TipStyle.

        It Should Be One Of BT_LEAVE, BT_CLICK, BT_BUTTON.
        """
        
        if tipstyle not in [BT_LEAVE, BT_CLICK, BT_BUTTON]:
            msg = '\nERROR: BalloonTip TipStyle Should Be One Of "BT_LEAVE", '\
                  '"BT_CLICK", "BT_BUTTON"'
            raise msg

        self._tipstyle = tipstyle


    def GetBalloonTipStyle(self):
        """Returns The BalloonTip TipStyle."""
        
        return self._tipstyle
    

    def SetBalloonColour(self, colour=None):
        """Sets The BalloonTip Background Colour."""
        
        if colour is None:
#             colour = wx.Color(255, 250, 205)
            colour = wx.Colour(255, 250, 205)
        

        self._ballooncolour = colour


    def GetBalloonColour(self):
        """Returns The BalloonTip Background Colour."""

        return self._ballooncolour
    

    def SetTitleFont(self, font=None):
        """Sets The Font For The Top Title."""
        
        if font is None:
            font = wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False)

        self._balloontitlefont = font


    def GetTitleFont(self):
        """Returns The Font For The Top Title."""
        
        return self._balloontitlefont
    

    def SetMessageFont(self, font=None):
        """Sets The Font For The Tip Message."""
        
        if font is None:
            font = wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False)

        self._balloonmsgfont = font


    def GetMessageFont(self):
        """Returns The Font For The Tip Message."""

        return self._balloonmsgfont
    

    def SetTitleColour(self, colour=None):
        """Sets The Colour For The Top Title."""
        
        if colour is None:
            colour = wx.BLACK

        self._balloontitlecolour = colour


    def GetTitleColour(self):
        """Returns The Colour For The Top Title."""

        return self._balloontitlecolour        


    def SetMessageColour(self, colour=None):
        """Sets The Colour For The Tip Message."""
        
        if colour is None:
            colour = wx.BLACK

        self._balloonmsgcolour = colour


    def GetMessageColour(self):
        """Returns The Colour For The Tip Message."""

        return self._balloonmsgcolour        


    def OnDestroy(self, event):
        """Handles The Target Destruction."""
        print "Balloon Destroyed"
        if hasattr(self, "BalloonFrame"):
            if self.BalloonFrame:
                try:
                    if isinstance(self._widget, wx.TaskBarIcon):
                        self._widget.UnBind(wx.EVT_TASKBAR_MOVE)
                        self.taskbartime.Stop()
                        del self.taskbartime
#                     else:
#                         self._widget.Unbind(wx.EVT_MOTION)
#                         self._widget.Unbind(wx.EVT_LEAVE_WINDOW)
#                         self._widget.Unbind(wx.EVT_ENTER_WINDOW)
                        
                    self.BalloonFrame.Destroy()
                    
                except:
                    pass
                
                del self.BalloonFrame


    def EnableTip(self, enable=True):
        """Enabel/Disable Globally The BalloonTip."""

        self._runningapp.__tooltipenabled__ = enable

