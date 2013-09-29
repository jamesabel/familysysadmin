
import wx
import ConfigParser

class SettingsDialog(wx.Frame):
    def __init__(self):
        self.save_button_id = 200

        # On Windows this writes to the registry at HKEY_CURRENT_USER\Software\<app>
        self.cfg = wx.Config()
        wx.Frame.__init__(self, None, -1, "Settings", wx.DefaultPosition)

        self.cb_verbose = wx.CheckBox(self, label='Verbose')
        self.tc_guid = wx.TextCtrl(self)
        self.string_auth_token = wx.StaticText(self, label='Auth Token:')
        self.tc_auth_token = wx.TextCtrl(self)
        self.cb_sandbox = wx.CheckBox(self, label='Sandbox')
        self.cb_mute = wx.CheckBox(self, label='Mute')
        self.button_save = wx.Button(self, id=self.save_button_id, label='Save')

        self.LoadState()

        border = 10
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.cb_verbose, 0, wx.LEFT, border)
        vbox.Add(wx.StaticText(self, label=''), 0, wx.LEFT, border) # space
        vbox.Add(wx.StaticText(self, label=''), 0, wx.LEFT, border)
        vbox.Add(wx.StaticText(self, label='--- ADVANCED ---'), 0, wx.LEFT, border)
        vbox.Add(self.tc_guid, 0, wx.LEFT, border)
        vbox.Add(self.string_auth_token, 0, wx.LEFT, border)
        vbox.Add(self.tc_auth_token, 0, wx.LEFT, border)
        vbox.Add(self.cb_sandbox, 0, wx.LEFT, border)
        vbox.Add(self.cb_mute, 0, wx.LEFT, border)
        vbox.Add(wx.StaticText(self, label='----------------'), 0, wx.LEFT, border)
        vbox.Add(wx.StaticText(self, label=''), 0, wx.LEFT, border)
        vbox.Add(self.button_save, 0, wx.LEFT, border)

        self.Bind(wx.EVT_BUTTON, self.OnSave, id=self.save_button_id)
        self.statusbar = self.CreateStatusBar()

        self.SetAutoLayout(True)
        self.SetSizerAndFit(vbox)
        self.Centre()

    def LoadState(self):
        self.cb_verbose.SetValue(self.cfg.ReadBool('verbose'))
        self.tc_guid.SetValue(self.cfg.Read('guid'))
        self.tc_auth_token.SetValue(self.cfg.Read('auth_token'))
        self.cb_sandbox.SetValue(self.cfg.ReadBool('sandbox'))
        self.cb_mute.SetValue(self.cfg.ReadBool('mute'))

    def OnSave(self, event):
        self.cfg.WriteBool('verbose', self.cb_verbose.GetValue())
        self.cfg.Write('guid', self.tc_guid.GetValue())
        self.cfg.Write('auth_token', self.tc_auth_token.GetValue())
        self.cfg.WriteBool('sandbox', self.cb_sandbox.GetValue())
        self.cfg.WriteBool('mute', self.cb_mute.GetValue())
        self.statusbar.SetStatusText('Saved.')

    def set(self, key, value):
        self.cfg.Write(key, value)
        self.cfg.Flush()

    def get(self, key):
        val = self.cfg.Read(key)
        if len(val) < 1:
            val = None
        return(val)