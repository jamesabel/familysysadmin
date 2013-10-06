import wx

import gui

class FamilySysAdminApp(wx.App):

    def OnInit(self):
        print("AppName", self.GetAppName())
        self.frame = gui.SysTray()
        self.frame.Show(False) # we have a window, but we never show it
        return True
