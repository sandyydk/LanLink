__author__ = 'Sandyman'
import socket
import clientlist
from ChatFrame import MyFrame
import select
import wx
import pyaudio
import wave
import datetime

class Showd(wx.Frame):

   def __init__(self,sender,timestmp):
        wx.Frame.__init__(self, None, wx.NewId(),title=sender)
        self.InitUI(sender,timestmp)

   def InitUI(self,sender,timestmp):
        self.ShowMessage(sender,timestmp)

   def ShowMessage(self,sender,timestmp):
        x=wx.MessageDialog(self,'Want to play the voice message', sender,
            wx.OK |wx.CANCEL | wx.ICON_INFORMATION)
        if x.ShowModal()==wx.ID_OK:
          voicehandler(sender,timestmp)
          self.Destroy()
        else:
          self.Destroy()


def voicehandler(sender,timestmp):
    wf = wave.open(sender+timestmp+".wav", 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

    data = wf.readframes(1024)

    while data != '':
        stream.write(data)
        data = wf.readframes(1024)

    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to handle server emergency messages using a pop-up
def ServerMessage(msg):
        x=wx.MessageDialog(None,str(msg),"Server Alert",wx.OK | wx.ICON_INFORMATION)
        if x.ShowModal()==wx.ID_OK:
            x.Destroy()


"""
 This mainly handles the frame for text messages. It's duty is to identify the appropriate frame to which the received
 messages are to be appended and if not found create one.
"""
def FrameMessageHandler(msg, target):

    try:
        if target == "Server":
            ServerMessage(msg)
        else:
            if target in clientlist.buttonlist:
                fram = wx.FindWindowByName(target)
                result= fram.IsShown()

                print "Result:"+str(result)
                if result == True:
                    if msg!='':
                        fram.history.AppendText(target+":"+msg+"\n")
            else:
                fram=MyFrame(target)
                fram.Show(True)
                clientlist.buttonlist.append(target)
                if msg!='':
                    fram.history.AppendText(target+":"+msg+"\n")
    except Exception,e:
        print e.args

"""
Creating the frames here.
"""
def FrameCreator(title):
    frame = MyFrame(title)
    frame.Show(True)
"""
Finds the name of the client to be used in the backend operations.
"""
def Hostname():
    return socket.gethostname()
"""
Used for testing purpose
"""

def createFrame(target):
    frame=MyFrame(target)
    frame.Show(True)

def callReceiver(host=Hostname()):

    BUFSIZ = 1024
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host,20002))
    sock.listen(3)
    voicereceiversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    voicereceiversock.bind((host, 20008))
    voicereceiversock.listen(3)
    inputs=[sock, voicereceiversock]

    while True:
        while inputs:
            readable, writable, exceptional = select.select(inputs, [], inputs)
            for s in readable:
                if s is sock:
                    serverclientsocket, serveraddress= s.accept()
                    inputs.append(serverclientsocket)
                if s is voicereceiversock:
                    server, serveraddr = s.accept()
                    server.settimeout(30.0)
                    sender = server.recv(1024)
                    # Timestamp to save audio files
                    curtime= datetime.datetime.utcnow()
                    curtime= str(curtime)
                    curtimesplit = curtime.split(",")
                    ts = curtimesplit[0].split(" ")
                    timestmp = ts[0]+"_"+ts[1]
                    f = open(sender+timestmp+".wav",'wb')
                    with f:
                        l = server.recv(1024)
                        while l:
                            f.write(l)
                            l = server.recv(1024)
                        f.close()

                    server.close()
                    showframe = Showd(sender,timestmp)
                else:
                    try:
                        receiveddata = s.recv(BUFSIZ)
                        splitdata = receiveddata.split(",")
                        target = splitdata[2]
                        msg = splitdata[1]
                        wx.CallAfter(FrameMessageHandler,msg,target)
                        s.close()
                        inputs.remove(s)
                    except Exception,e:
                        print e.args
