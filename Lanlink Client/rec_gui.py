import wx
import clientCallReceiver

class Rec_voice(wx.Frame):

     def __init__(self,sender):

        wx.Frame.__init__(self, None, wx.NewId(),sender)
        self.ShowMessage(sender)

     def ShowMessage(self,sender):

        x=wx.MessageDialog(self,'VOICE RECIEVED...Choose options to play or ignore', 'YOU HAVE 1 NEW VOICE MESSAGE',
            wx.OK |wx.CANCEL | wx.ICON_INFORMATION)
        if x.ShowModal()==wx.ID_OK:
          clientCallReceiver.voicehandler(sender)
        else:
          self.Destroy()

