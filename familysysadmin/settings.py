
import wx
import ConfigParser

# This settings window uses wxPython.  The settings window is built up from a collection of
# sub-windows (as is typical for this kind of UI programming).  This might seem like a lot of code for such
# a simple window, but that's just how wx (and windows in general) works.  Each window (or sub-window) is a class.
# It starts with a Frame (there is exactly one Frame window).  Inside the frame are 2 sub-windows - one
# is a Notebook (Notebooks provide the tabs) and the other a Panel where the common buttons (e.g. Save, Cancel)
# are placed.  The notebook has yet another set of sub-windows (Panels) that represent each tab.
# 'Sizers' are used to size the windows.  Sizers are a way for the windows to automatically size themselves
# based on the dimensions of their child windows (and add border margins, etc.).

BORDER_SIZE = 10
# TLR = top, left, right (all but bottom) - good for all but the bottom items, which should be wx.ALL
BORDER_TLR = wx.TOP | wx.LEFT | wx.RIGHT
BUTTON_SPACER = 10

class SettingsFrame(wx.Frame):
    """
    # The one-and-only frame window.  It also does the access into the persistent storage.
    """
    def __init__(self):
        wx.Frame.__init__(self, None, title="Test")

        # On Windows this writes to the registry at HKEY_CURRENT_USER\Software\<app>
        self.cfg = wx.Config()

        self.settings_notebook = SettingsNotebook(self)
        self.common_buttons_panel = CommonButtonsPanel(self)

        # match the background of the frame to the notebook
        self.SetBackgroundColour(self.settings_notebook.GetBackgroundColour())

        # sizers for the notebook (tabs) and buttons panels
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.settings_notebook, flag=wx.ALIGN_CENTER | BORDER_TLR, border=BORDER_SIZE)
        sizer.Add(self.common_buttons_panel, flag=wx.ALIGN_RIGHT | wx.ALL, border=BORDER_SIZE)
        self.SetSizerAndFit(sizer)

    def LoadState(self):
        self.settings_notebook.general_tab.cb_verbose.SetValue(self.cfg.ReadBool('verbose'))

        guid_str = self.cfg.Read('guid')
        self.settings_notebook.advanced_tab.tc_guid.SetValue(guid_str)
        # add spacer - for some reason the size ends up short
        self.settings_notebook.advanced_tab.tc_guid.SetMinSize(self.settings_notebook.advanced_tab.tc_guid.GetTextExtent(guid_str + '__'))

        auth_token = self.cfg.Read('auth_token')
        self.settings_notebook.advanced_tab.tc_auth_token.SetValue(auth_token)
        self.settings_notebook.advanced_tab.tc_auth_token.SetMinSize(self.settings_notebook.advanced_tab.tc_guid.GetTextExtent(auth_token + '__'))

        self.settings_notebook.advanced_tab.cb_sandbox.SetValue(self.cfg.ReadBool('sandbox'))
        self.settings_notebook.advanced_tab.cb_mute.SetValue(self.cfg.ReadBool('mute'))

    def OnSave(self, event):
        self.set('verbose', self.settings_notebook.general_tab.cb_verbose.GetValue())
        self.set('guid', self.settings_notebook.advanced_tab.tc_guid.GetValue())
        self.set('auth_token', self.settings_notebook.advanced_tab.tc_auth_token.GetValue())
        self.set('sandbox', self.settings_notebook.advanced_tab.cb_sandbox.GetValue())
        self.set('mute', self.settings_notebook.advanced_tab.cb_mute.GetValue())
        self.GetTopLevelParent().Close()

    def OnCancel(self, event):
        self.GetTopLevelParent().Close()

    def set(self, key, value):
        if value is True or value is False:
            self.cfg.WriteBool(key, value)
        else:
            self.cfg.Write(key, value)
        self.cfg.Flush()

    def get(self, key):
        val = self.cfg.Read(key)
        if len(val) < 1:
            val = None
        return(val)

class SettingsNotebook(wx.Notebook):
    """
    The tabbed window.  A tabbed window is called a Notebook in wx.
    """
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent)

        self.general_tab = GeneralSettingsPanel(self)
        self.AddPage(self.general_tab, "General")
        self.advanced_tab = AdvancedSettingsPanel(self)
        self.AddPage(self.advanced_tab, "Advanced")

class GeneralSettingsPanel(wx.Panel):
    """
    General settings tab.
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.cb_verbose = wx.CheckBox(self, label='Verbose')

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.cb_verbose, 0, BORDER_TLR, BORDER_SIZE)

        self.SetSizerAndFit(vbox)

class AdvancedSettingsPanel(wx.Panel):
    """
    Advanced settings tab.
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.tc_guid = wx.TextCtrl(self)
        self.tc_auth_token = wx.TextCtrl(self)
        self.cb_sandbox = wx.CheckBox(self, label='Sandbox')
        self.cb_mute = wx.CheckBox(self, label='Mute')
        vbox.Add(self.cb_sandbox, flag=BORDER_TLR, border=BORDER_SIZE)
        vbox.Add(self.cb_mute, flag=BORDER_TLR, border=BORDER_SIZE)

        vbox.Add(self.MakeLabeledSizer('GUID:', self.tc_guid))
        vbox.Add(self.MakeLabeledSizer('Auth Token:', self.tc_auth_token, wx.ALL))

        self.SetSizerAndFit(vbox)

    def MakeLabeledSizer(self, label_str, tc_value, flag=BORDER_TLR):
        """
        Make a horizontal sizer for static text (StaticText) + text control (TextCtrl)
        """
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label=label_str), flag=flag, border=BORDER_SIZE)
        hbox.Add(tc_value, flag=flag, border=BORDER_SIZE)
        return hbox

# the common buttons at the bottom of the settings window
class CommonButtonsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        self.button_save = wx.Button(self, id=wx.ID_SAVE)
        self.Bind(wx.EVT_BUTTON, self.GetParent().OnSave, id=wx.ID_SAVE)
        self.button_cancel = wx.Button(self, id=wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.GetParent().OnCancel, id=wx.ID_CANCEL)
        vbox.Add(self.button_save)
        vbox.AddSpacer(BUTTON_SPACER)
        vbox.Add(self.button_cancel)
        self.SetSizerAndFit(vbox)

# for testing
if __name__ == "__main__":

    class TestApp(wx.App):
        def OnInit(self):
            print("AppName", self.GetAppName())
            self.test_frame = SettingsFrame()

            # set up some test data (actually writes it out)
            self.test_frame.set('verbose', True)
            self.test_frame.set('sandbox', True)
            self.test_frame.set('guid', 'test_guid')
            self.test_frame.set('auth_token', 'test_auth_token')
            self.test_frame.LoadState() # load the data just written

            self.test_frame.Show()
            return True

    app = TestApp()
    app.MainLoop()