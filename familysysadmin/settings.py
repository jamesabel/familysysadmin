
import wx
import ConfigParser

class SettingsDialog(wx.Frame):
    def __init__(self):
        self.save_button_id = 200
        self.border = 10
        self.border_sides = wx.LEFT | wx.RIGHT

        # On Windows this writes to the registry at HKEY_CURRENT_USER\Software\<app>
        self.cfg = wx.Config()
        wx.Frame.__init__(self, None, -1, "Settings", wx.DefaultPosition)

        self.cb_verbose = wx.CheckBox(self, label='Verbose')
        self.tc_guid = wx.TextCtrl(self)
        self.tc_auth_token = wx.TextCtrl(self)
        self.cb_sandbox = wx.CheckBox(self, label='Sandbox')
        self.cb_mute = wx.CheckBox(self, label='Mute')
        self.button_save = wx.Button(self, id=self.save_button_id, label='Save')

        self.LoadState()

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.cb_verbose, 0, self.border_sides, self.border)
        vbox.Add(wx.StaticText(self, label=''), 0, self.border_sides, self.border) # space
        vbox.Add(wx.StaticText(self, label=''), 0, self.border_sides, self.border)

        vbox.Add(self.MakeLabeledSizer('GUID:', self.tc_guid))
        vbox.Add(self.MakeLabeledSizer('Auth Token:', self.tc_auth_token))

        vbox.Add(self.cb_sandbox, 0, self.border_sides, self.border)
        vbox.Add(self.cb_mute, 0, self.border_sides, self.border)

        vbox.Add(wx.StaticText(self, label=''), 0, self.border_sides, self.border)
        vbox.Add(self.button_save, 0, self.border_sides, self.border)

        self.Bind(wx.EVT_BUTTON, self.OnSave, id=self.save_button_id)
        self.statusbar = self.CreateStatusBar()

        self.SetAutoLayout(True)
        self.SetSizerAndFit(vbox)
        self.Centre()

    def MakeLabeledSizer(self, label_str, tc_value):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label=label_str), 0, self.border_sides, self.border)
        hbox.Add(tc_value, 0, self.border_sides, self.border)
        return hbox

    def LoadState(self):
        self.cb_verbose.SetValue(self.cfg.ReadBool('verbose'))

        guid_str = self.cfg.Read('guid')
        self.tc_guid.SetValue(guid_str)
        self.tc_guid.SetMinSize(self.tc_guid.GetTextExtent(guid_str + '__')) # add spacer - for some reason the size ends up short

        auth_token = self.cfg.Read('auth_token')
        self.tc_auth_token.SetValue(auth_token)
        self.tc_auth_token.SetMinSize(self.tc_guid.GetTextExtent(auth_token + '__'))

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