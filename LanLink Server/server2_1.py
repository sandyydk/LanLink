__author__ = 'Sandyman'

import socket,select
import threading
import wx
import clientsetup
import server_refresh
import shareddata

BUFSIZ = 1024

mutex = threading.Lock()

def broadcasthandler(bmsg):

    clients = shareddata.lst
    for i in clients:
        targetip = shareddata.clientmapdict[i]
        sendingdata = i+","+bmsg+","+"Server"

        try:
            sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((targetip,20002))
            sock.sendall(sendingdata)
            sock.close()
        except Exception,e:
            sock.close()
            print e.args
            continue

def routehandler(msg):

    splitdata = msg.split(",")
    dest = splitdata[0]
    targetip = shareddata.clientmapdict[dest]
    message = splitdata[1]
    threadname = threading.currentThread().getName()
    try:
        sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((targetip, 20002))
        sock.send(msg)
        sock.close()
    except Exception,e:
        print e.args
        sock.close()


def voicefilesender(sender,receiver):

    targetip = shareddata.clientmapdict[receiver]
    sendingsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sendingsock.connect((targetip, 20008))
        sendingsock.settimeout(40.0)
        sendingsock.sendall(sender)
    except Exception,e:
        print e.args
    try:
        f = open(sender+receiver+".wav",'rb')
        l = f.read(1024)
        while l:
            sendingsock.send(l)
            l = f.read(1024)
        f.close()
        sendingsock.close()
    except Exception,e:
        sendingsock.close()
        if f:
            f.close()
        print e.args





def Hostname():
    return socket.gethostname()

class App(wx.App):

    def OnInit(self):
       frame = testserver()
       frame.Show()
       self.SetTopWindow(frame)
       return True


class testserver(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.NewId(),"LanLink Server",size=(450,550))

        self.Centre()
        self.CreateStatusBar()
        self.panel1 = wx.Panel(self,size=(800,60), pos=(0,0), style=wx.SIMPLE_BORDER)
        self.label = wx.StaticText(self.panel1, pos=(0,20),label="Input Emergency Message:")
        wx.StaticText(self.panel1,pos=(0,40),label="")
        self.field = wx.TextCtrl(self.panel1, value="", size=(450,30),pos=(0,70))
        self.okbutton = wx.Button(self.panel1, label="SEND", id=wx.ID_OK,pos=(330,105))
        self.Bind(wx.EVT_BUTTON, self.onsend, id=wx.ID_OK)
        self.Bind(wx.EVT_TEXT_ENTER, self.onsend)
        bSizer = wx.BoxSizer( wx.HORIZONTAL)
        bSizer.Add(self.label)
        bSizer.Add(self.field)
        bSizer.Add(self.okbutton)
        font1 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.label.SetFont(font1)
        self.image = wx.Image('D:\LanLink Server GUI\logo_final.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(self.panel1, -1,self.image,pos=(25,140))

        self.thread = threading.Thread(name = 'clientsetup',target=clientsetup.clientset,args= ())
        self.thread.setDaemon(True)
        self.thread.start()
        self.refresh = threading.Thread(target=server_refresh.ref_fun,args=())
        self.refresh.setDaemon(True)
        self.refresh.start()
        self.runthread = threading.Thread(target = runner,args=(),name="Runner")
        self.runthread.setDaemon(True)
        self.runthread.start()
        self.bthread = threading.Thread(target=broadcst,args=(),name = "BThread")
        self.bthread.setDaemon(True)
        self.bthread.start()

    def onsend(self, event):

        msg = self.field.GetValue()
        try:
            mutex.acquire()
            shareddata.q.put(msg)
            shareddata.flag=1

        except Exception,e:
            print e.args
        finally:
            mutex.release()
        shareddata.e.set()
        check = shareddata.e.isSet()
        self.field.Clear()

def broadcst():

    while 1:
        event_is_set = shareddata.e.wait()
        if shareddata.flag == 1:
            try:
                bdata = shareddata.q.get()
                bthread = threading.Thread(name = "Broadcast Thread",target= broadcasthandler,args =(bdata,))
                bthread.setDaemon(True)
                bthread.start()
                shareddata.e.clear()
            except Exception,e:
                print e.args
            try:
                mutex.acquire()
                shareddata.flag = 0
            finally:
                mutex.release()



def runner():

    host = Hostname()
    recport = 20001
    sendport = 20002
    voicereceiverport = 20007
    voicereceiversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    voicereceiversock.bind((host, voicereceiverport))
    voicereceiversock.listen(5)
    voicereceiversock.settimeout(6.0)
    addr = (host, recport)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(addr)
    sock.listen(5)
    sock.settimeout(5.0)
    inputs = [sock, voicereceiversock]
    outputs = []
    while True:
        while inputs:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            for s in readable:
                if s is sock:
                    try:
                        connection, address = sock.accept()
                        connection.settimeout(40.0)
                        msg = connection.recv(BUFSIZ)
                        sendername = socket.gethostbyaddr(address[0])
                        t= threading.Thread(name= sendername[0], target= routehandler, args =(msg,))
                        t.setDaemon(True)
                        t.start()
                        connection.close()
                    except Exception,e:
                        print e.args
                        connection.close()
                if s is voicereceiversock:
                    vconnection, address = voicereceiversock.accept()
                    vconnection.settimeout(40.0)
                    data=vconnection.recv(1024)
                    splitdata=data.split(",")
                    sender=splitdata[0]
                    receiver=splitdata[1]
                    f = open(sender+receiver+".wav", 'wb')
                    with f:
                        l = vconnection.recv(1024)
                        while l:
                            f.write(l)
                            l = vconnection.recv(1024)
                    f.close()
                    vconnection.close()
                    t = threading.Thread(name = sender+receiver, target = voicefilesender, args = (sender, receiver))
                    t.setDaemon(True)
                    t.start()


app = App(False)
app.MainLoop()