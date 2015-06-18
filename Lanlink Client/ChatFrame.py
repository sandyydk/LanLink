__author__ = 'Sandyman'

"""
This is the Chat Frame which is seen on clicking on any client button to begin the communication. It basically contains
the GUI wrapper and the function mappings.
"""
import socket
import wx
import datetime
import clientlist
from guage2 import VoiceRec


class MyFrame(wx.Frame):

    def __init__(self,title):

        wx.Frame.__init__(self, None, wx.NewId(),title, name = title, size=(600,500),style=(wx.CLOSE_BOX | wx.MINIMIZE_BOX|wx.CAPTION|wx.SYSTEM_MENU))
        t1=title
        self.Centre()
        i =wx.Frame.GetId(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panel1 = wx.Panel(self, -1,pos=(0,100),size=(500,300),style=wx.SUNKEN_BORDER)
        self.panel2 = wx.Panel(self, -1,pos=(500,200),style=wx.SUNKEN_BORDER)
        self.history = wx.TextCtrl(self.panel1,pos=(0,0),style=wx.TE_MULTILINE,size=(400,200))
        self.history.SetBackgroundColour('white')
        self.history.SetForegroundColour('sky blue')
        wx.StaticText(self.panel1,pos=(0,320), label="Type here")
        self.typer = wx.TextCtrl(self.panel1,pos=(0,350), size=(390, -1))
        self.history.SetEditable(False)
        self.typer.SetBackgroundColour('white')
        self.typer.SetFocus()
        self.button2 = wx.Button(self.panel2, id=-1, label='Voice', pos=(8, 328), size=(175, 28))
        self.button2.Bind(wx.EVT_BUTTON, lambda event: self.Voice(event, t1))
        self.button2.SetBackgroundColour('yellow')
        self.button2.SetToolTip(wx.ToolTip("click to voice chat"))
        self.button3 = wx.Button(self.panel2, id=-1, label='Send', pos=(8, 358), size=(175, 28))
        self.button3.Bind(wx.EVT_BUTTON, lambda event: self.Send(event,t1))
        self.button3.SetBackgroundColour('sky blue')
        # optional tooltip
        self.button3.SetToolTip(wx.ToolTip("click to send"))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.panel1,2,wx.EXPAND|wx.ALL,border=2)
        sizer.Add(self.panel2,0,wx.EXPAND|wx.ALL,border=2)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()
        # A Statusbar in the bottom of the window
        self.CreateStatusBar(2)
        # Set the second field to be double in width wrt the first
        self.SetStatusWidths([-2,-1])
        # Setting up the menu
        file_menu = wx.Menu()
        edit_menu=wx.Menu()
        #Appending to File menu
        file_menu.Append(wx.ID_ABOUT, '&About','Information about this application')
        file_menu.AppendSeparator()
        Exit_action = file_menu.Append(wx.ID_EXIT, 'Exit', 'Exit the application')
        self.Bind(wx.EVT_MENU, self.OnExit, Exit_action)
        #Apppending to Edit menu
        edit_menu.Append(wx.ID_COPY,'&copy','copy to clipboard')
        edit_menu.Append(wx.ID_CUT,'&cut','cut to clipboard')
        edit_menu.Append(wx.ID_PASTE,'&paste','paste from clipboard')
        # Bind the "copy menu event" to the OnCopy method
        self.Bind(wx.EVT_MENU, self.OnCopy, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU,self.OnCut,id=wx.ID_CUT)
        self.Bind(wx.EVT_MENU,self.OnPaste,id=wx.ID_PASTE)
        # Creating the menubar
        menu_bar = wx.MenuBar()
        #Appending the File,Edit menu to Menu Bar
        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(edit_menu,'&Edit')
        # Get today date via datetime
        today = datetime.datetime.today()
        today = today.strftime('%d-%b-%Y')
        # Set today date in the second field
        self.SetStatusText(today, 1)
        # Adding the menu bar to the frame content
        self.SetMenuBar(menu_bar)
        self.Show(True)
        self.Bind(wx.EVT_CLOSE, lambda event:self.OnClose(event,title))

    def OnClose(self,event,title):
        clientlist.buttonlist.remove(title)
        self.Destroy()

    def Voice(self,event,t1):
        self.SetStatusText("Voice messaging !!")
        voc=VoiceRec(t1)
        voc.Show(True)

    # Message is being sent here
    def Send(self,event,t1):
        text=""
        self.SetStatusText("Sending the message !!")
        text = self.typer.GetValue()
        name = socket.gethostname()
        if(text):
            self.history.AppendText("Me : "+text+"\n")
            self.typer.Clear()
            sendingdata = t1+","+text+","+name
            try:
                sendsock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sendsock.connect((clientlist.serverip, 20001))
            except Exception,e:
                print e.args
            try:
                sendsock.send(sendingdata)
            except Exception,e:
                print e.args
            sendsock.close()
            self.SetStatusText("Message Sent!!")

    def OnExit(self, event):

        dlg = wx.MessageDialog(self, 'Are you sure you want to quit?', 'Caution!!',
                           wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION | wx.CLOSE)
        if dlg.ShowModal() == wx.ID_YES:
         self.Destroy()
        else:
         event.Veto()


    def OnCut(self, event):
        self.control.Cut()

    def OnCopy(self, event):
        self.control.Copy()

    def OnPaste(self, event):
        self.control.Paste()

