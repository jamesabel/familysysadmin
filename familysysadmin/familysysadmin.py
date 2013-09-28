import platform
import threading
import sys
import ConfigParser
import psutil
import wx

import fsaevernote
import fsaconfig
import systray
import monitor

class FamilySysAdmin(wx.App):

    def OnInit(self):
        frame = systray.SysTray(self)
        frame.Show(False) # we have a window, but we never show it

        self.monitor = monitor.Monitor()
        self.monitor.start()

        return True






