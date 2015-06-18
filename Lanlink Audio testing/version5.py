import wx
import client
import time
import ChatFrame
import socket
import threading
import clientlist
import clientCallReceiver
import wx.lib.scrolledpanel
from functools import partial

title='chat'
ips = 'localhost'
button_dict={}

#MainFrame is the frame containing initial launch screen(frame)

class App(wx.App):

    def OnInit(self):
       frame = MainFrame()
       frame.Show()
       self.SetTopWindow(frame)
       return True

class MainFrame(wx.Frame):

    title = "LANlink"
    def __init__(self):
        wx.Frame.__init__(self, None, wx.NewId(),self.title,size=(450,650))
        self.Centre()
        menubar = wx.MenuBar()
        help_menu= wx.Menu()
        setup_menu=wx.Menu()
        help_menu.Append(100, '&About','Here is where you  get some help')
        self.Bind(wx.EVT_MENU, self.OnAboutBox, id=100)
        menubar.Append(help_menu, '&Help')
        self.SetMenuBar(menubar)
        self.CreateStatusBar()
        self.panel1 = wx.Panel(self,size=(800,60), pos=(0,0), style=wx.SIMPLE_BORDER)
        self.panel1.SetBackgroundColour('sky blue')
        self.panel2 = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(800,590), pos=(0,60), style=wx.SIMPLE_BORDER)
        self.panel2.SetupScrolling()
        self.panel2.SetBackgroundColour('orange')
        self.refresh = wx.Button(self.panel1,label="Refresh",pos=(0,50),size=(75,40))
        self.refresh.Bind(wx.EVT_BUTTON,self.refreshbutton_handler)
        self.refresh.Disable()
        config= wx.Button(self.panel1,label="Configure",pos=(0,100),size=(75,40))
        config.Bind(wx.EVT_BUTTON,self.Cserver)
        self.disconnect_gui = wx.Button(self.panel1,label="Disconnect",pos=(0,150),size=(75,40))
        self.disconnect_gui.Bind(wx.EVT_BUTTON,self.disconnect_function)
        self.disconnect_gui.Disable()

        bSizer = wx.BoxSizer( wx.HORIZONTAL)
        bSizer.Add(self.refresh,0,wx.ALL,5)
        bSizer.Add(config,0,wx.ALL,5)
        bSizer.Add(self.disconnect_gui,0,wx.ALL,5)

        self.panel2.SetSizer( bSizer )
        self.panel1.SetSizer( bSizer )
        self.Dynamic()

        self.thread= threading.Thread(target=clientCallReceiver.callReceiver,args=())
        self.thread.setDaemon(True)
        self.thread.start()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def refreshbutton_handler(self,evt):
        client.refresh_req()
        time.sleep(3)
        self.Dynamic()

    def Dynamic(self):
       host = socket.gethostname()
       self.RemoveButtons(self)
       j=0
       posy=10
       for i in clientlist.lst:
           if i == host:
               pass
           else:
               button=wx.Button(self.panel2,label=i,id=j,pos=(10,posy))
               button.Bind(wx.EVT_BUTTON,partial(self.on_button,button_label=i))
               button_dict[i]= j
               posy+=40
               j=j+1
       for x in button_dict:
           print x

    def RemoveButtons(self,e):
        button_dict.clear()


    def OnClose(self,event):
        dlg = wx.MessageDialog(self, "Do you really want to close this application?","Confirm Exit", wx.YES|wx.NO|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_YES:
            self.Destroy()


    def OnQuit(self, event):

        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            sock.connect((clientlist.serverip,20009))
        except Exception,e:
            q=e.args
            x=wx.MessageDialog(self,str(q),"Alert",wx.OK | wx.ICON_INFORMATION)
            if x.ShowModal()==wx.ID_OK:
                x.Destroy()
        self.Close()

# The chat frame is launched here. Checking should preferably be also done here.

    def on_button(self,evt,button_label):

        x= evt.GetId()
        title=button_label
        if title not in clientlist.buttonlist:
            frame=ChatFrame.MyFrame(title)
            clientlist.buttonlist.append(title)
            clientlist.framelist.append(title)
            frame.Show(True)
        else:
            pass

    def OnAboutBox(self, e):

        description = """Voice and Text Communication Over Lan """
        licence = """ This is an open source project and can
                   be used freely giving appropriate credits to the makers """
        info = wx.AboutDialogInfo()
        info.SetName('LANLINK')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C)Copyright@LanLink Inc, 2015 ')
        info.SetLicence(licence)
        info.AddDeveloper('Sandeep H Bhat\nVinyas N R\nVinay Hosamane\nVinit N Shanbhag')
        wx.AboutBox(info)

    def valid_ip(self,address):

        try:
            host_bytes = address.split('.')
            valid = [int(b) for b in host_bytes]
            valid = [b for b in valid if b >= 0 and b<=255]
            return len(host_bytes) == 4 and len(valid) == 4
        except:
            return False

    def Cserver(self, event):

        dlg = wx.TextEntryDialog(self, 'Server IP Address','IP Address')
        if dlg.ShowModal() == wx.ID_OK:
            ips=dlg.GetValue()
            validity = self.valid_ip(ips)
            if validity == 0:
                print "Invalid address format"
                q="Invalid Address"
                x=wx.MessageDialog(self,str(q),"Alert",wx.OK | wx.ICON_INFORMATION)
                if x.ShowModal()==wx.ID_OK:
                    x.Destroy()
            else:
                sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                try:
                    sock.connect((ips,20009))
                    self.SetStatusText('Server IP: %s\n' % ips)
                    clientlist.serverip = ips
                    time.sleep(1.0)
                    self.panel2.Enable()
                    client.refresh_req()
                    time.sleep(3)
                    self.Dynamic()
                    print "After dynamic"
                    self.refresh.Enable()   # Refresh is enabled once configuration is done
                    self.disconnect_gui.Enable()
                except Exception,e:
                    print e.args
                    print "Config error"
                    x=wx.MessageDialog(self,str("Wrong Server Address"),"Alert",wx.OK | wx.ICON_INFORMATION)
                    if x.ShowModal()==wx.ID_OK:
                        x.Destroy()
                self.SetStatusText('Server IP: %s\n' % ips)

        dlg.Destroy()

    def disconnect_function(self,evt):

        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            sock.connect((clientlist.serverip,20009))
        except Exception,e:
            print e.args
            q=e.args
            x=wx.MessageDialog(self,str(q),"Alert",wx.OK | wx.ICON_INFORMATION)
            if x.ShowModal()==wx.ID_OK:
                x.Destroy()
        self.disconnect_gui.Disable()
        self.refresh.Disable()
        self.panel2.Disable()

if __name__ == '__main__':
    app = App(False)
    app.MainLoop()
