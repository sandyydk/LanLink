

import wx
import clientvoicesender


TASK_RANGE = 10

class VoiceRec(wx.Frame):

    def __init__(self,title):

        wx.Frame.__init__(self, None, wx.NewId(),title)
        t1=title
        self.InitUI(t1)

    def InitUI(self,t1):

        self.timer = wx.Timer(self, 1)
        self.count = 0
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.gauge = wx.Gauge(pnl, range=TASK_RANGE, size=(250, 25))
        self.btn1 = wx.Button(pnl,id=-1,label='OK')
        self.btn1.Bind(wx.EVT_BUTTON, lambda event: self.OnOk(event, t1))
        self.text = wx.StaticText(pnl, label='Press Ok to start recording')
        hbox1.Add(self.gauge, proportion=1, flag=wx.ALIGN_CENTRE)
        hbox2.Add(self.btn1, proportion=1, flag=wx.RIGHT, border=10)
        hbox3.Add(self.text, proportion=1)
        vbox.Add((0, 30))
        vbox.Add(hbox1, flag=wx.ALIGN_CENTRE)
        vbox.Add((0, 20))
        vbox.Add(hbox2, proportion=1, flag=wx.ALIGN_CENTRE)
        vbox.Add(hbox3, proportion=1, flag=wx.ALIGN_CENTRE)
        pnl.SetSizer(vbox)
        
        self.SetSize((300, 200))
        self.SetTitle('wx.Gauge')
        self.Centre()
        self.Show(True)
        

    def OnOk(self, e,t1):
        
        if self.count == TASK_RANGE:
            self.Destroy()

        self.timer.Start(900)
        self.text.SetLabel('Voice is being processed...Please wait')
        clientvoicesender.voicerecorder(t1)

    def OnTimer(self, e):
        
        self.count = self.count + 1
        self.gauge.SetValue(self.count)
        if self.count == TASK_RANGE:
            self.timer.Stop()
            self.text.SetLabel('Voice Recording completed..\n Press ok to Send')
            self.Destroy()
