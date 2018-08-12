'''
Created on Jan 28, 2016

@author: AnjilaTam
'''

import wx


# Some classes to use for the notebook pages.  Obviously you would
# want to use something more meaningful for your application, these
# are just for illustration.
openTabNumber=1

class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
#         parent.SetBackgroundColour("Red")
        t = wx.StaticText(self, -1, "This is a PageOne object", (20,20))

class PageTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
#         parent.SetBackgroundColour("Green")
        t = wx.StaticText(self, -1, "This is a PageTwo object", (40,40))

class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a PageThree object", (40,40))


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Simple Notebook Example")

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        page1 = PageOne(nb)
#         page1.SetBackgroundColour("Green")
        page2 = PageTwo(nb)
#         page2.SetBackgroundColour("Red")
        page3 = PageThree(nb)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Home")
        nb.AddPage(page2, "Update")
        nb.AddPage(page3, "History")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(nb, 1, wx.EXPAND)
#         staticte=wx.StaticText(p,label="static")
#         sizer.Add(staticte, 0, wx.ALL)
        p.SetSizer(sizer)
        wx.CallAfter(nb.Refresh)


if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
    
