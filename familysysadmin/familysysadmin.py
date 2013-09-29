import ConfigParser
import psutil
import wx

import fsaevernote
import settings
import gui
import monitor

class FamilySysAdminApp(wx.App):

    def OnInit(self):
        print("AppName", self.GetAppName())
        frame = gui.SysTray(self)
        frame.Show(False) # we have a window, but we never show it

        self.monitor = monitor.Monitor()
        self.monitor.start()

        return True






