import wx

import uiicon

class SysTray(wx.Frame):
    TBMENU_STATUS = 1000
    TBMENU_CLOSE  = 1001

    def __init__(self, fsa):
        self.fsa = fsa
        name = 'FSA'
        frame_size = (100,100) # doesn't really matter since it will never be shown
        wx.Frame.__init__(self, None, -1, name, size = frame_size)
        icon = uiicon.uiicon.getIcon()
        self.SetIcon(icon)
        # setup a taskbar icon, and catch some events from it
        self.tbicon = wx.TaskBarIcon()
        self.tbicon.SetIcon(icon, name)
        wx.EVT_TASKBAR_LEFT_DOWN(self.tbicon, self.OnTaskBarMenu)
        wx.EVT_TASKBAR_RIGHT_DOWN(self.tbicon, self.OnTaskBarMenu)
        wx.EVT_MENU(self.tbicon, self.TBMENU_STATUS, self.OnTaskBarStatus)
        wx.EVT_MENU(self.tbicon, self.TBMENU_CLOSE, self.OnTaskBarClose)

    def OnTaskBarMenu(self, evt):
        menu = wx.Menu()
        menu.Append(self.TBMENU_STATUS, "Status")
        menu.Append(self.TBMENU_CLOSE, "Close")
        self.tbicon.PopupMenu(menu)
        menu.Destroy()

    def OnTaskBarStatus(self, evt):
        # todo: make a window and populate it
        pass

    def OnTaskBarClose(self, evt):
        self.tbicon.Destroy()
        self.Destroy()

