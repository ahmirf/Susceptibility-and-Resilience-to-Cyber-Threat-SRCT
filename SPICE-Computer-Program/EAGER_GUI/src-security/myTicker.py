'''
Created on Aug 13, 2014

@author: 
'''
"""
    Class StockMarket, creates and handle a list of CompanyStock objects, and provide to the GUI of stuff for
        the scroll ticker
    attributes:
        smarket, list of CompanyStock objects
        thread_actualizar, Thread object to update the stock market each time interval
    methods:
        load_market, load the list with CompanyStock object taking the data from the initial source data.
        update_market, update the objects of the list
        get_one_ticker, getter function to return one securitie data in text format and rotates to the next one
        get_next_character, returns a character of one securitie (if the securitie data is exhausted
            retrieve another securitie) data to the GUI.
"""

import random
import threading
import time

import wx


class StockMarket():

    
    def __init__(self, l_inicial):
        print "in myTicker.py"
        self.smarket = []
        self.load_market(l_inicial)
        self.current_ticker = self.get_one_ticker()
        self.thread_updating = UpdateThread(self)
        self.thread_updating.start()

    def load_market(self, l_inicial):
        for data_ticker in l_inicial:
            simple_ticker = CompanyStock(data_ticker)
            self.smarket.append(simple_ticker)

    def update_market(self):
        for j in range(len(self.smarket)):
            self.smarket[j].update_ticker()

    def get_one_ticker(self):
        self.one_ticker = self.smarket.pop(0)
        self.direction = self.one_ticker.direction
        self.smarket.append(self.one_ticker)
        self.dotProbeImageIndex = 0
        return self.one_ticker.ticker_to_text()

    def get_next_character(self):
        if self.dotProbeImageIndex == len(self.current_ticker):
            self.current_ticker = self.get_one_ticker()
            
            self.dotProbeImageIndex = 0
        self.character_symbol = self.current_ticker[self.dotProbeImageIndex:self.dotProbeImageIndex + 1]
        self.dotProbeImageIndex += 1
        return self.character_symbol

    def get_tag(self):
        return self.one_ticker.direction

class myTicker(wx.PyControl):
    def __init__(self, parent):
        print "===> myTicker.py initiated"
#         wx.Frame.__init__(self,parent=None)
        wx.PyControl.__init__(self, parent)
        self.panelmain = parent
#         self.panelmain.SetBackgroundColour("Red")
        self.initGUI()
#         self.trackCmpStockRise()
#         self.tickerFocustimer = wx.Timer(self) 
#         self.Bind(wx.EVT_TIMER, self.OntickerFocusTimer, self.tickerFocustimer)
#         self.tickerFocustimer.Start(100000)
        
#     def OntickerFocusTimer(self,event):
# #         self.setFocusonTicker()
#         a=self.text.GetValue()
#         
#         self.text.SetValue(a[a.rfind("|")+1:len(a)])
#         self.CharIndex=len(self.text.GetValue())
#         event.Skip()    

    def start(self):
        self.scrollTicker()

   
    def setFocusonTicker(self):
        if not self==None:
            a=self.text.GetValue()
            
            self.text.SetValue(a[a.rfind("|")+1:len(a)])
            self.text.SetStyle(0, len(self.text.GetValue()), wx.TextAttr("blue"))
            self.CharIndex=len(self.text.GetValue())
            
#             self.text.SetFocus()
#             self.text.Layout()
#             self.text.Refresh()
        
        
    def initGUI(self):

        self.isCmpName = False
        self.first = False
        self.NumOfSpace = 0
        self.CharIndex = 0
        self.tag = {CHAR_DOWN: "down", CHAR_EVEN: "even", CHAR_UP: "up"}
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        
        self.text = wx.TextCtrl(self.panelmain, style=wx.TE_RICH2|wx.TE_READONLY|wx.TE_AUTO_SCROLL)
        self.text.Bind(wx.EVT_SET_FOCUS, self.onTickerFocus)
        sizer.Add(self.text, 1, flag=wx.EXPAND | wx.ALL)
        self.text.SetBackgroundColour("White")
        self.panelmain.SetSizer(sizer)
#         self.market_one = StockMarket(stock_market)
        self.market_one = StockMarket(stock_market)
        
#         txtOnPressPnl=wx.TextCtrl(self.parent,value="this is press release",size=wx.DefaultSize,style=wx.ALL|wx.EXPAND|wx.ALIGN_CENTRE)
#     def trackCmpStockRise(self):
#         self.cmpnameCharindex = 0
#         self.cmpNameTracked = ""
#         self.cmpTrackQuote = ""
        
    def scrollTicker(self):
#         self.text.configure()
#         self.text.Clear()
#         self.text.in
        
        character_symbol = self.market_one.get_next_character()
        self.direction = self.market_one.direction
        if character_symbol.isalpha():
#             if(self.cmpnameCharindex==0):
#                 #to nullify the string self.cmpNameTracked only when the next company has arrived
#                 self.cmpNameTracked=""
#                 self.cmpTrackQuote=""
#             self.cmpnameCharindex += 1
#             self.cmpNameTracked += character_symbol
            self.isCmpName = True
#             self.first = True
            self.NumOfSpace = 0
            self.text.SetStyle(len(self.text.GetValue()), self.CharIndex, wx.TextAttr("blue"))
#             if self.cmpnameCharindex == 4:
                # this is a complete company name
#                 print self.cmpNameTracked
#                 self.cmpTrackQuote = self.cmpTrackQuote + self.cmpNameTracked + "|"
        elif character_symbol.isspace():
            self.isCmpName = False
#             self.cmpnameCharindex=0
            self.NumOfSpace += 1
        elif character_symbol == CHAR_DOWN:
            self.text.SetStyle(len(self.text.GetValue()), self.CharIndex, wx.TextAttr("Red"))
#             self.cmpTrackQuote += "|"
        elif character_symbol == CHAR_UP:
            self.text.SetStyle(len(self.text.GetValue()), self.CharIndex, wx.TextAttr("Green"))
#             self.cmpTrackQuote += "|"
        elif character_symbol == CHAR_EVEN:
            self.text.SetStyle(len(self.text.GetValue()), self.CharIndex, wx.TextAttr("Sienna"))  
#             self.cmpTrackQuote += "|"
        elif character_symbol.isdigit() or character_symbol.isdecimal() or character_symbol == CHAR_PER or character_symbol == CHAR_DOT:
            if(self.NumOfSpace > 2):
                
#                 if self.first:
#                     self.cmpTrackQuote += "|"
                if self.direction == CHAR_DOWN:
                    self.text.SetStyle(len(self.text.GetValue()), self.CharIndex, wx.TextAttr("Red"))
                elif self.direction == CHAR_UP:
#                     self.text.SetForegroundColour(wx.GREEN)
                    self.text.SetStyle(len(self.text.GetValue()), self.CharIndex, wx.TextAttr("Green"))
                elif self.direction == CHAR_EVEN:
#                     self.text.SetForegroundColour(wx.YELLOW)
                    self.text.SetStyle(len(self.text.GetValue()), self.CharIndex, wx.TextAttr("Yellow"))
#                 if not character_symbol == CHAR_PER:
#                     self.cmpTrackQuote += character_symbol
#                 else:
#                     self.cmpTrackQuote += "|" + self.tag.get(self.direction)
#                     print "====> "+self.cmpTrackQuote
#                     self.cmpnameCharindex = 0
#                     self.cmpNameTracked = ""
#                     self.cmpTrackQuote = ""
#                     hjj
#                     print self.tag.get(self.direction)
#                 self.first = False
            else:
                # 587.25
#                 self.cmpTrackQuote += character_symbol
                self.text.SetStyle(len(self.text.GetValue()), self.CharIndex, wx.TextAttr("Blue"))
        else:
            self.text.SetStyle(len(self.text.GetValue()), self.CharIndex, wx.TextAttr("Blue"))
        
        self.text.AppendText(character_symbol)
#         self.text.SetFocus()
        self.CharIndex += 1
        
        self.text.ShowPosition(self.text.GetLastPosition()) 
#         wx.CallLater(SPEED, self.scrollTicker)
        
    def onTickerFocus(self,event):
        print "Ticker got the focus event"
        event.Skip()

class CompanyStock():
    """
    Class CompanyStock, handle each stock symbol and their data
    attributes:
        symbol, string, the abbreviature of the securitie
        price, string, the current price of the securitie
        direction, string(1), is a character that indicates its las fix price went up, down or even
        change, string, is the value of the last change surrounded by '()', the first character is '+' or '-'
    methods:
        update_ticker, update the securitie price, direction and change with random values
        ticker_to_text, returns a formatted string with all the data of the securitie
    """
    def __init__(self, list_data):
        self.symbol, self.price, self.direction, self.change = list_data
        self.changePer = "{:.2f}".format((float(self.change) / float(self.price)) * 100)

    def update_ticker(self):
        flt_price = float(self.price)
        try:
            if random.randint(0, 9) == 0:
                self.direction = CHAR_EVEN
            else:
                increase_percent = random.randrange(-5, 5)
                # TODO: may need to remove randomization to present every participant with the same data
                # TODO: implementar normalvariate(0, 0.02) o gauss(0, 0.02)
                flt_change = flt_price * increase_percent / 100
                flt_new_price = flt_price + flt_change
                self.price = "{:.2f}".format(flt_new_price)
                if flt_change < 0:
                    self.direction = CHAR_DOWN
                elif flt_change == 0:
                    self.direction = CHAR_EVEN
                else:
                    self.direction = CHAR_UP
                self.change = "{:.2f}".format(flt_change)
        except:
            import sys
            sys.exc_info()[0]
#             write_to_page("<p>Error: %s</p>" % e)
        
                

    def ticker_to_text(self):
        return u'{}  {}  {}  {}  {}  {}  | '.format(self.symbol, self.price, self.change, self.direction, self.changePer, CHAR_PER)
    
      
# Here starts the program working process, until here was the GUI
# CONSTANTS
CHAR_UP = u'\u25B2'
CHAR_DOWN = u'\u25BC'
CHAR_EVEN = "="
CHAR_PER = u'\u0025'
CHAR_DOT = u'\u002E'
SPEED = 250
UPDATE_TIME = 60
# INITIAL DATA, this must be changed to implement the load of a external source
stock_market = [["GOOG", "587.25", CHAR_UP, "12.14"],
                ["AAPL", "237.14", CHAR_UP, "7.25"],
                ["GTAT", "87.47", CHAR_DOWN, "1.18"],
                ["KNDI", "167.32", CHAR_UP, "6.85"],
                ["ORCL", "482.91", CHAR_DOWN, "24.65"],
                ["FBOK", "327.67", CHAR_DOWN, "11.78"],
                ["TWTR", "842.41", CHAR_UP, "15.45"]]


class UpdateThread(threading.Thread):
    """
    Class UpdateThread(), subclass of Thread, handle the time to the next update of the stock market values
    args:
        market_1, a StockMarket class object to update
    attributes:
        my_check, string for debugging purpouses, it'll be implemented the source data management
        the_market, StockMarket object that will be updated
    methods:
        run, overrides the Thread run method, and calls the update_market method of StockMarket class each interval
    """
    def __init__(self, market_1):
        self.my_check = " CHECK "  # TODO replace with initial source data.
        self.the_market = market_1
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(UPDATE_TIME)
        self.the_market.update_market()
        print(" UPDATED!!!")  # for debugging
#         self.run()   
    
    

# class SimpleApp(wx.App):
#     def __init__(self):
#         wx.App.__init__(self,redirect=None, filename=None)
#     
#          
#     def OnInit(self):
# #         f=wx.Frame(None)
#         f = wx.Frame(None)
#         f.SetBackgroundColour("Green")
#         p = wx.Panel(f)
#         ticker = myTicker(p)
#         s = wx.BoxSizer(wx.VERTICAL)
#         s.Add(ticker, proportion=1, flag=wx.EXPAND|wx.ALL)
#         p.SetSizer(s)
#         f.Show()
#         return True
         
    
# 
# # STARTS THE PROGRAM
# def main():
#     app = SimpleApp()
#     app.MainLoop()
#     
    
      


if __name__ == '__main__':
    
    app = wx.PySimpleApp()
    f = wx.Frame(None)
    f.SetBackgroundColour("Green")
    p = wx.Panel(f)
#     graphviz = GraphvizOutput()
#     graphviz.output_file = 'C:\Users\Anjila\Desktop/profile.png'
#     service_filter = GlobbingFilter(include=['*storageservice.*',
#                                              '*ptcompat.*'])
#     config = Config(groups=True, verbose=True)
#     config.trace_filter = service_filter
#  
#     print('RUN PROFILE')
#     with PyCallGraph(output=graphviz):
    t = myTicker(p) 
    t.start()
#     print('DONE RUN PROFILE')
      
    # set ticker properties here if you want
#     s = wx.BoxSizer(wx.VERTICAL)
#     s.Add(t, flag=wx.GROW, proportion=0)
#     p.SetSizer(s)
    f.Show()
    app.MainLoop()
    
     
        
        
