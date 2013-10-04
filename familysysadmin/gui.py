
import wx

import uiicon
import settings

class SysTray(wx.Frame):
    TBMENU_REFRESH = 1000
    TBMENU_STATUS = 1001
    TBMENU_SETTINGS = 1002
    TBMENU_CLOSE  = 1003

    def __init__(self, app):
        self.app = app
        frame_size = (100,100) # doesn't really matter since it will never be shown
        wx.Frame.__init__(self, None, -1, self.app.GetAppName(), size = frame_size)
        icon = uiicon.uiicon.getIcon()
        self.SetIcon(icon)
        # setup a taskbar icon, and catch some events from it
        self.tbicon = wx.TaskBarIcon()
        self.tbicon.SetIcon(icon, self.app.GetAppName())
        wx.EVT_TASKBAR_LEFT_DOWN(self.tbicon, self.OnTaskBarMenu)
        wx.EVT_TASKBAR_RIGHT_DOWN(self.tbicon, self.OnTaskBarMenu)
        wx.EVT_MENU(self.tbicon, self.TBMENU_REFRESH, self.OnTaskBarRefresh)
        wx.EVT_MENU(self.tbicon, self.TBMENU_STATUS, self.OnTaskBarStatus)
        wx.EVT_MENU(self.tbicon, self.TBMENU_SETTINGS, self.OnTaskBarSettings)
        wx.EVT_MENU(self.tbicon, self.TBMENU_CLOSE, self.OnTaskBarClose)

    def OnTaskBarMenu(self, evt):
        menu = wx.Menu()
        menu.Append(self.TBMENU_REFRESH, "Refresh")
        menu.Append(self.TBMENU_STATUS, "Status")
        menu.Append(self.TBMENU_SETTINGS, "Settings")
        menu.Append(self.TBMENU_CLOSE, "Close")
        self.tbicon.PopupMenu(menu)
        menu.Destroy()

    def OnTaskBarRefresh(self, evt):
        self.app.monitor.update_monitor()

    def OnTaskBarStatus(self, evt):
        pass

    def OnTaskBarSettings(self, evt):
        frame = settings.SettingsFrame()
        frame.Show(True)

    def OnTaskBarClose(self, evt):
        self.app.monitor.stop_monitor()
        self.tbicon.Destroy()
        self.Destroy()

